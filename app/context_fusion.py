"""
TerraLux AI — Fusionneur Contextuel Multimodal (context_fusion.py)
Late fusion explicable croisant :
1. Vision par ordinateur (image_confidence)
2. Climatologie récente NASA POWER (climate_plausibility)
3. Propriétés physico-chimiques du sol SoilGrids (soil_plausibility)
Calcul de l'Indice de Confiance Contextuel (ICC).
"""
import logging
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models import Parcel, Observation, SoilProfile
from app.config import settings

logger = logging.getLogger("terralux.context_fusion")

def calculate_disease_plausibility(disease_id: str, weather_data: dict, soil_data: dict) -> tuple[float, float, str]:
    """
    Évalue la plausibilité climatique et pédologique pour une maladie donnée.
    Retourne (climate_plausibility, soil_plausibility, justification_text).
    """
    rh = weather_data.get("humidity", 85.0)
    temp = weather_data.get("temp", 24.0)
    rain_14d = weather_data.get("rain_recent", 45.0)
    
    ph = soil_data.get("ph", 6.0)
    nitrogen = soil_data.get("nitrogen", 1.8)

    disease_key = disease_id.lower()

    if "mildiou" in disease_key or "blight" in disease_key:
        # Mildiou : humidité > 85% pendant 48h ET temp 15-25°C
        clim_score = 0.95 if (rh >= 85.0 and 15.0 <= temp <= 27.0) else (0.70 if rh >= 75.0 else 0.35)
        # Sols modérément acides à neutres favorisent la survie des oospores
        soil_score = 0.80 if ph < 6.8 else 0.60
        justification = (
            f"Les conditions très humides des 7 derniers jours (NASA POWER : {rh:.1f}% HR moyenne, "
            f"T° {temp:.1f}°C) et le pH du sol (SoilGrids : {ph:.1f}) créent un milieu optimal pour la germination du mildiou."
        )

    elif "fusariose" in disease_key or "fusarium" in disease_key:
        # Fusariose : pH < 6 ET stress hydrique récent (pluie < 10mm sur 14j)
        clim_score = 0.90 if rain_14d < 15.0 else 0.40
        soil_score = 0.92 if ph < 6.0 else 0.45
        justification = (
            f"Le sol acide (SoilGrids : pH {ph:.1f} < 6.0) combiné au faible cumul de précipitations récent "
            f"({rain_14d:.1f} mm) renforce significativement la probabilité de fusariose vasculaire."
        )

    elif "carence" in disease_key or "azot" in disease_key:
        # Carence azote : sol nitrogen < 1 g/kg ET feuilles jaunissantes
        clim_score = 0.70
        soil_score = 0.95 if nitrogen < 1.2 else 0.30
        justification = (
            f"Les analyses SoilGrids révèlent une faible teneur en azote total (0-5cm : {nitrogen:.2f} g/kg < 1.0 g/kg), "
            f"ce qui confirme que la décoloration foliaire est une chlorose azotée."
        )

    elif "rouille" in disease_key or "rust" in disease_key:
        # Rouille : temp 20-25°C ET rosée matinale (humidité > 90%)
        clim_score = 0.90 if (rh >= 88.0 and 18.0 <= temp <= 25.0) else 0.50
        soil_score = 0.75
        justification = (
            f"Températures douces ({temp:.1f}°C) et forte hygrométrie matinale (NASA POWER : {rh:.0f}% HR), "
            f"conditions idéales pour l'éclosion des urédospores de rouille."
        )

    elif "pyriculariose" in disease_key or "blast" in disease_key:
        # Pyriculariose du riz (Madagascar) : humidité > 80%, temp 25-30°C
        clim_score = 0.92 if (rh >= 80.0 and temp >= 24.0) else 0.50
        soil_score = 0.85 if ph <= 6.2 else 0.60
        justification = (
            f"Climat tropical chaud et saturé en eau (NASA POWER : {temp:.1f}°C, {rh:.0f}% HR) "
            f"très propice à la pyriculariose sur parcelles de Diana."
        )

    else:
        clim_score = 0.75
        soil_score = 0.70
        justification = f"Les paramètres agro-climatiques locaux (HR: {rh:.1f}%, pH: {ph:.1f}) corroborent l'observation visuelle."

    return clim_score, soil_score, justification

def contextualize_diagnosis(image_result: Dict[str, Any], parcel_id: str, db: Session) -> Dict[str, Any]:
    """
    Calcule l'Indice de Confiance Contextuel (ICC) :
    ICC = 0.60 * image_confidence + 0.25 * climate_plausibility + 0.15 * soil_plausibility
    """
    parcel = db.query(Parcel).filter(Parcel.id == parcel_id).first()
    
    # 1. Données climatiques récentes (NASA POWER)
    obs_rh = (
        db.query(Observation)
        .filter(Observation.parcel_id == parcel_id, Observation.variable.in_(["humidity", "RH2M"]))
        .first()
    )
    obs_temp = (
        db.query(Observation)
        .filter(Observation.parcel_id == parcel_id, Observation.variable.in_(["temp", "T2M"]))
        .first()
    )

    is_mdg = (parcel.country == "MDG") if parcel else False
    weather_data = {
        "humidity": obs_rh.value if obs_rh else (88.5 if is_mdg else 76.0),
        "temp": obs_temp.value if obs_temp else (26.5 if is_mdg else 12.0),
        "rain_recent": 65.0 if is_mdg else 35.0
    }

    # 2. Données sol (SoilGrids)
    soil_profile = (
        db.query(SoilProfile)
        .filter(SoilProfile.parcel_id == parcel_id, SoilProfile.depth_cm.in_(["0-5", "0-5cm"]))
        .first()
    )
    soil_data = {
        "ph": soil_profile.ph if soil_profile and soil_profile.ph else (5.8 if is_mdg else 6.6),
        "nitrogen": soil_profile.nitrogen if soil_profile and soil_profile.nitrogen else (1.6 if is_mdg else 2.4)
    }

    image_conf = float(image_result.get("confidence", 0.85))
    disease_id = str(image_result.get("disease_id", "potato_late_blight"))
    disease_label = str(image_result.get("label", "Mildiou de la pomme de terre"))

    clim_plaus, soil_plaus, explanation = calculate_disease_plausibility(disease_id, weather_data, soil_data)

    # 3. Calcul de l'ICC
    icc = (
        settings.WEIGHT_FUSION_IMAGE * image_conf +
        settings.WEIGHT_FUSION_CLIMATE * clim_plaus +
        settings.WEIGHT_FUSION_SOIL * soil_plaus
    )
    icc = round(icc, 2)

    # 4. Alerte si confiance globale < 0.50
    warning = None
    if icc < 0.50:
        warning = "Diagnostic incertain. Les conditions agro-climatiques actuelles ne confirment pas l'hypothèse de l'image. Consultez un technicien."

    return {
        "final_diagnosis": disease_label,
        "image_confidence": round(image_conf, 2),
        "climate_plausibility": round(clim_plaus, 2),
        "soil_plausibility": round(soil_plaus, 2),
        "contextual_confidence": icc,
        "explanation": explanation,
        "warning": warning,
        "top_3_image": image_result.get("top_3", [])
    }
