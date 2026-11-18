"""
TerraLux AI — Moteur de Décision Agronomique Explicable (engine.py)
Système expert agronomique :
1. Filtre pays (F9) strict via plant_countries
2. Scoring multicritère (0-100) : Climat (40%), Pédologie (30%), Rotation (30%)
3. Génération explicite de justifications scientifiques avec valeurs numériques et plages de référence
4. Top 3 des cultures recommandées persisté dans la table recommendations
"""
from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models import (
    Parcel, Plant, PlantCountry, SoilProfile, Observation,
    CropHistory, Recommendation
)
from app.schemas import CropRecommendationItem, RecommendationReason
from app.config import settings
from app.realtime_weather import get_realtime_weather_open_meteo

def calculate_climate_score(plant: Plant, mean_temp: float, annual_rain: float) -> tuple[float, list[str], list[str]]:
    """
    Calcule l'adéquation climatique (0-100) et génère les justifications.
    Pondération : 50% température, 50% pluviométrie.
    """
    positives = []
    negatives = []

    # 1. Température
    t_min = plant.temp_min or 15.0
    t_max = plant.temp_max or 30.0
    t_opt = (t_min + t_max) / 2.0
    t_span = max(1.0, (t_max - t_min) / 2.0)

    if t_min <= mean_temp <= t_max:
        # Score entre 90 et 100 selon proximité du centre optimal
        proximity = 1.0 - (abs(mean_temp - t_opt) / t_span)
        temp_score = 90.0 + 10.0 * max(0.0, min(1.0, proximity))
        positives.append(f"Température moyenne {mean_temp:.1f}°C dans l'optimum ({t_min:.1f}-{t_max:.1f}°C)")
    elif mean_temp < t_min:
        diff = t_min - mean_temp
        temp_score = max(0.0, 90.0 - diff * 15.0)
        negatives.append(f"Température moyenne {mean_temp:.1f}°C trop basse (optimum {t_min:.1f}-{t_max:.1f}°C)")
    else:
        diff = mean_temp - t_max
        temp_score = max(0.0, 90.0 - diff * 15.0)
        negatives.append(f"Température moyenne {mean_temp:.1f}°C trop élevée (optimum {t_min:.1f}-{t_max:.1f}°C)")

    # 2. Pluviométrie
    r_min = plant.rain_min or 600.0
    r_max = plant.rain_max or 1500.0
    r_opt = (r_min + r_max) / 2.0
    r_span = max(50.0, (r_max - r_min) / 2.0)

    if r_min <= annual_rain <= r_max:
        r_prox = 1.0 - (abs(annual_rain - r_opt) / r_span)
        rain_score = 90.0 + 10.0 * max(0.0, min(1.0, r_prox))
        positives.append(f"Pluviométrie annuelle {annual_rain:.0f} mm dans la plage optimale ({r_min:.0f}-{r_max:.0f} mm)")
    elif annual_rain < r_min:
        diff = r_min - annual_rain
        rain_score = max(0.0, 90.0 - (diff / 10.0))
        negatives.append(f"Déficit hydrique : {annual_rain:.0f} mm pour un besoin minimal de {r_min:.0f} mm")
    else:
        diff = annual_rain - r_max
        rain_score = max(0.0, 90.0 - (diff / 15.0))
        negatives.append(f"Excédent pluviométrique : {annual_rain:.0f} mm (plage optimale {r_min:.0f}-{r_max:.0f} mm)")

    # Climat : si la température OU la pluie est hors seuil létal/critique, pénalité sévère
    if mean_temp < (t_min - 10.0) or mean_temp > (t_max + 10.0):
        temp_score = 0.0
    if annual_rain < (r_min * 0.3) or annual_rain > (r_max * 2.5):
        rain_score = 0.0

    climate_score = 0.5 * temp_score + 0.5 * rain_score
    return round(climate_score, 1), positives, negatives

def calculate_soil_score(plant: Plant, ph: float, clay: float) -> tuple[float, list[str], list[str]]:
    """
    Calcule l'adéquation pédologique (0-100) et génère les justifications.
    """
    positives = []
    negatives = []

    ph_min = plant.ph_min or 5.5
    ph_max = plant.ph_max or 7.0
    ph_opt = (ph_min + ph_max) / 2.0
    ph_span = max(0.5, (ph_max - ph_min) / 2.0)

    if ph_min <= ph <= ph_max:
        ph_prox = 1.0 - (abs(ph - ph_opt) / ph_span)
        ph_score = 90.0 + 10.0 * max(0.0, min(1.0, ph_prox))
        positives.append(f"pH de surface {ph:.1f} idéal pour la culture ({ph_min:.1f}-{ph_max:.1f})")
    elif ph < ph_min:
        diff = ph_min - ph
        ph_score = max(0.0, 90.0 - diff * 70.0)
        negatives.append(f"Sol trop acide : pH {ph:.1f} inférieur à la tolérance ({ph_min:.1f}-{ph_max:.1f})")
    else:
        diff = ph - ph_max
        ph_score = max(0.0, 90.0 - diff * 70.0)
        negatives.append(f"Sol trop basique : pH {ph:.1f} supérieur à la tolérance ({ph_min:.1f}-{ph_max:.1f})")

    # Pénalité texture si sol très lourd pour tubercules/racines sensibles
    texture_penalty = 0.0
    if plant.type in ["tuber", "legume"] and clay > 44.0:
        if plant.name_fr == "Manioc":
            # Le manioc tolère les sols tropicaux lourds
            texture_penalty = 5.0 if clay > 52.0 else 0.0
        else:
            texture_penalty = 15.0
            negatives.append(f"Texture argileuse lourde ({clay:.0f}% argile) limitant le grossissement racinaire")
    elif clay >= 20.0:
        positives.append(f"Bonne capacité de rétention hydrique et minérale ({clay:.0f}% argile)")

    soil_score = max(0.0, ph_score - texture_penalty)
    return round(soil_score, 1), positives, negatives

def calculate_rotation_penalty(plant: Plant, parcel_id: str, db: Session, current_year: int) -> tuple[float, str]:
    """
    Règle de rotation des cultures :
    - Pénalité 100 (score = 0) si même famille cultivée l'année N-1
    - Pénalité 50 (score = 50) si même famille cultivée en N-2
    - Pénalité 0 (score = 100) sinon
    """
    history = db.query(CropHistory).filter(CropHistory.parcel_id == parcel_id).all()
    if not history:
        return 0.0, "Aucun précédent cultural de même famille recensé (rotation libre)"

    family = plant.family
    same_family_prev_year = any(
        h.year == (current_year - 1) and h.plant and h.plant.family == family
        for h in history
    )
    if same_family_prev_year:
        return 100.0, f"Même famille botanique ({family}) cultivée l'an passé : risque majeur de propagation parasitaire"

    same_family_2years = any(
        h.year == (current_year - 2) and h.plant and h.plant.family == family
        for h in history
    )
    if same_family_2years:
        return 50.0, f"Même famille botanique ({family}) présente il y a 2 ans : rotation modérément serrée"

    return 0.0, f"Aucune {family} cultivée depuis 3 ans : excellente tête d'assolement"

def get_recommendation(parcel_id: str, db: Session) -> List[CropRecommendationItem]:
    """
    Point d'entrée du moteur TerraLux AI :
    Évalue toutes les plantes autorisées pour le pays de la parcelle.
    Retourne le Top 3 avec explications complètes.
    """
    parcel = db.query(Parcel).filter(Parcel.id == parcel_id).first()
    if not parcel:
        raise ValueError(f"Parcelle ID '{parcel_id}' introuvable.")

    country_code = parcel.country
    if not country_code or country_code == "UNKNOWN":
        country_code = "MDG" if parcel.latitude < 0 else "LUX"

    # 1. FILTRE PAYS STRICT (F9)
    plant_entries = (
        db.query(Plant)
        .join(PlantCountry, Plant.id == PlantCountry.plant_id)
        .filter(PlantCountry.country_code == country_code)
        .all()
    )

    if not plant_entries:
        raise ValueError(f"Aucune plante répertoriée pour le pays '{country_code}' (Filtre F9).")

    # 2. Récupération des observations climatiques (NASA POWER)
    obs_temp = (
        db.query(Observation)
        .filter(Observation.parcel_id == parcel.id, Observation.variable == "temp")
        .order_by(Observation.date.desc())
        .first()
    )
    obs_rain = (
        db.query(Observation)
        .filter(Observation.parcel_id == parcel.id, Observation.variable == "rain")
        .order_by(Observation.date.desc())
        .first()
    )

    soil_profile = (
        db.query(SoilProfile)
        .filter(SoilProfile.parcel_id == parcel.id, SoilProfile.depth_cm.in_(["0-5", "0-5cm"]))
        .first()
    )

    # 3. Récupération météo temps réel & observations certifiées récentes
    live_temp = None
    live_rain = None
    try:
        live_weather = get_realtime_weather_open_meteo(parcel.latitude, parcel.longitude)
        curr = live_weather.get("current", {})
        if curr.get("temperature_c") is not None:
            live_temp = float(curr["temperature_c"])
    except Exception:
        pass

    # Si pas d'observation directe, interpolation spatiale vers le point calibré le plus proche ayant des données
    if not obs_temp or not soil_profile:
        closest_parcel = (
            db.query(Parcel)
            .join(Observation, Parcel.id == Observation.parcel_id)
            .filter(Parcel.country == country_code, Parcel.id != parcel.id)
            .order_by(
                (Parcel.latitude - parcel.latitude) * (Parcel.latitude - parcel.latitude) +
                (Parcel.longitude - parcel.longitude) * (Parcel.longitude - parcel.longitude)
            )
            .first()
        )
        if closest_parcel:
            if not obs_temp:
                obs_temp = db.query(Observation).filter(Observation.parcel_id == closest_parcel.id, Observation.variable == "temp").first()
            if not obs_rain:
                obs_rain = db.query(Observation).filter(Observation.parcel_id == closest_parcel.id, Observation.variable == "rain").first()
            if not soil_profile:
                soil_profile = db.query(SoilProfile).filter(SoilProfile.parcel_id == closest_parcel.id, SoilProfile.depth_cm.in_(["0-5", "0-5cm"])).first()

    # Priorité aux observations directes et données récentes
    mean_temp = obs_temp.value if obs_temp else (live_temp if live_temp is not None else (26.5 if country_code == "MDG" else 10.5))
    annual_rain = obs_rain.value if obs_rain else (1350.0 if country_code == "MDG" else 845.0)
    ph = soil_profile.ph if soil_profile and soil_profile.ph else (5.8 if country_code == "MDG" else 6.6)
    clay = soil_profile.clay if soil_profile and soil_profile.clay else (48.0 if country_code == "MDG" else 24.0)

    current_year = datetime.utcnow().year

    scored_crops = []

    for plant in plant_entries:
        # Climat (40%)
        clim_score, clim_pos, clim_neg = calculate_climate_score(plant, mean_temp, annual_rain)
        
        # Pédologie (30%)
        soil_score, soil_pos, soil_neg = calculate_soil_score(plant, ph, clay)
        
        # Rotation (30%)
        rot_penalty, rot_reason = calculate_rotation_penalty(plant, parcel.id, db, current_year)
        rot_score = max(0.0, 100.0 - rot_penalty)

        # Score global pondéré avec pondération de priorité agronomique et alimentaire
        base_score = (
            settings.WEIGHT_CLIMATE * clim_score +
            settings.WEIGHT_SOIL * soil_score +
            settings.WEIGHT_ROTATION * rot_score
        )

        # Facteur agronomique : valorise les cultures vivrières et de rente majeures
        priority_multiplier = 1.0
        if plant.type in ["cereal", "tree", "cash_crop", "vine", "oilseed"]:
            priority_multiplier = 1.05
        elif plant.type in ["tuber"]:
            priority_multiplier = 1.03
        elif plant.type in ["legume", "fruit"]:
            priority_multiplier = 1.01

        final_score = min(100.0, round(base_score * priority_multiplier, 1))

        all_positives = clim_pos + soil_pos
        all_negatives = clim_neg + soil_neg
        if not all_negatives:
            all_negatives.append("Aucune contrainte agronomique majeure identifiée")
        if not all_positives:
            all_positives.append("Tolérance écologique générale")

        reasons = RecommendationReason(
            positive=all_positives,
            negative=all_negatives,
            rotation=rot_reason
        )

        item = CropRecommendationItem(
            plant_id=plant.id,
            name=plant.name_fr,
            scientific_name=plant.scientific_name,
            score=final_score,
            reasons=reasons
        )
        scored_crops.append(item)

    # Trier par score décroissant
    scored_crops.sort(key=lambda x: x.score, reverse=True)
    top3 = scored_crops[:3]

    # Enregistrer les recommandations dans la table recommendations (engine_version='rules-v1')
    try:
        # Supprimer anciennes recommandations pour cette parcelle
        db.query(Recommendation).filter(Recommendation.parcel_id == parcel.id).delete()
        for rec in top3:
            db.add(Recommendation(
                parcel_id=parcel.id,
                plant_id=rec.plant_id,
                score=rec.score,
                reasons=rec.reasons.model_dump(),
                engine_version="rules-v1"
            ))
        db.commit()
    except Exception:
        db.rollback()

    return top3
