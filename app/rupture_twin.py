"""
TerraLux AI — Innovation I2 : Jumeau de Rupture (rupture_twin.py)
Modélisation prédictive des points de rupture agronomique et de la propagation des stress
(sécheresses sévères, crues cycloniques, épidémies foliaires).
Positionnement : 'Les autres outils disent quoi planter. TerraLux prédit où et quand le système s'effondre.'
"""
import math
import json
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.orm import Session

from app.models import Parcel, SoilProfile, Observation, RuptureZone
from app.soil_intelligence import get_soil_profile

def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calcule la distance géodésique en kilomètres entre deux coordonnées GPS."""
    R = 6371.0 # Rayon de la Terre en km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0)**2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c

def simulate_stress_propagation(
    region: str,
    stress_type: str = "drought",
    duration_days: int = 30,
    country: Optional[str] = None,
    db: Session = None
) -> Dict[str, Any]:
    """
    Simule la cascade de stress territorial sur le graphe de parcelles :
    - Détermine la vulnérabilité intrinsèque de chaque parcelle (sol, eau, exposition)
    - Propage le stress aux parcelles voisines dans un rayon d'influence (< 15 km)
    - Identifie les points de rupture critiques et le temps avant défaillance
    - Génère la cartographie GeoJSON et les contre-mesures d'urgence.
    """
    if db is None:
        raise ValueError("Session de base de données requise pour la simulation.")

    # 1. Sélection des parcelles cibles
    query = db.query(Parcel)
    if country:
        query = query.filter(Parcel.country == country)
    elif region:
        query = query.filter(Parcel.region.ilike(f"%{region}%"))
    
    parcels = query.all()
    if not parcels:
        # Fallback : charger toutes les parcelles du pays déduit
        c_code = "MDG" if any(w in region.lower() for w in ["diana", "madagascar", "antsiranana", "ambanja", "nosy"]) else "LUX"
        parcels = db.query(Parcel).filter(Parcel.country == c_code).all()
        if not parcels:
            parcels = db.query(Parcel).all()

    if not parcels:
        raise ValueError("Aucune parcelle trouvée pour lancer la simulation de rupture.")

    country_detected = parcels[0].country

    # 2. Construction de l'état initial des parcelles
    parcel_states = {}
    for p in parcels:
        soil = get_soil_profile(p.id, db)
        richness = soil.get("richness_index", 70.0)
        clay = soil.get("properties", {}).get("clay", {}).get("value", 30.0)
        
        # Facteur de vulnérabilité de base selon le stress
        if stress_type == "drought":
            # Sol sableux/pauvre en argile et faible SOC -> rupture rapide
            base_vuln = max(20.0, 100.0 - (richness * 0.7 + clay * 0.8))
        elif stress_type == "cyclone" or stress_type == "flood":
            # Sols très argileux compactés et fortes pentes -> ruissellement et érosion
            base_vuln = min(95.0, 30.0 + (clay * 0.9) + (20.0 if p.country == "MDG" else 0.0))
        else: # pathogen / maladie
            base_vuln = 50.0 + (10.0 if richness < 60.0 else -10.0)

        # Intensification avec la durée du choc
        duration_factor = min(1.8, 1.0 + (duration_days / 60.0))
        accumulated_stress = min(100.0, base_vuln * duration_factor)

        parcel_states[p.id] = {
            "parcel": p,
            "richness": richness,
            "clay": clay,
            "base_vuln": round(base_vuln, 1),
            "accumulated_stress": round(accumulated_stress, 1),
            "status": "RESILIENT",
            "neighbors": []
        }

    # 3. Graphe spatial et cascade de propagation (Rayon 15 km)
    propagation_links = []
    p_ids = list(parcel_states.keys())
    
    for i in range(len(p_ids)):
        for j in range(i + 1, len(p_ids)):
            id_a, id_b = p_ids[i], p_ids[j]
            p_a, p_b = parcel_states[id_a]["parcel"], parcel_states[id_b]["parcel"]
            dist = haversine_distance_km(p_a.latitude, p_a.longitude, p_b.latitude, p_b.longitude)
            
            if dist <= 15.0:
                parcel_states[id_a]["neighbors"].append(id_b)
                parcel_states[id_b]["neighbors"].append(id_a)
                propagation_links.append({
                    "from_parcel_id": id_a,
                    "to_parcel_id": id_b,
                    "distance_km": round(dist, 2),
                    "transmission_risk": round(max(0.1, 1.0 - (dist / 15.0)), 2)
                })

    # Propagation des parcelles les plus fragiles vers leurs voisines
    for link in propagation_links:
        source_id = link["from_parcel_id"]
        target_id = link["to_parcel_id"]
        trans_weight = link["transmission_risk"]

        # Si source sous fort stress, ajoute une pression de voisinage à la cible
        if parcel_states[source_id]["accumulated_stress"] > 60.0:
            added_stress = (parcel_states[source_id]["accumulated_stress"] - 60.0) * trans_weight * 0.25
            parcel_states[target_id]["accumulated_stress"] = min(
                100.0,
                round(parcel_states[target_id]["accumulated_stress"] + added_stress, 1)
            )

    # 4. Détermination des états finaux
    n_rupture = 0
    n_stressed = 0
    total_area_rupture = 0.0

    features = []
    rupture_parcels_detail = []

    for p_id, data in parcel_states.items():
        p = data["parcel"]
        stress = data["accumulated_stress"]
        area = float(p.area_ha) if p.area_ha is not None else 4.0

        if stress >= 70.0:
            status = "RUPTURE"
            n_rupture += 1
            total_area_rupture += area
            rupture_parcels_detail.append({
                "parcel_id": p.id,
                "name": p.name,
                "stress_score": stress,
                "rupture_cause": f"Sensibilité critique au stress {stress_type} (durée {duration_days} jours)"
            })
        elif stress >= 45.0:
            status = "STRESSED"
            n_stressed += 1
        else:
            status = "RESILIENT"

        data["status"] = status

        # Feature GeoJSON
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [p.longitude, p.latitude]
            },
            "properties": {
                "parcel_id": p.id,
                "name": p.name,
                "country": p.country,
                "region": p.region,
                "status": status,
                "stress_score": stress,
                "richness_index": data["richness"],
                "clay_pct": data["clay"]
            }
        }
        features.append(feature)

    # Temps avant 1ère rupture (en jours)
    if n_rupture > 0:
        time_to_first_rupture = max(7, round(duration_days * (1.0 - (max(d["accumulated_stress"] for d in parcel_states.values()) / 120.0))))
    else:
        time_to_first_rupture = duration_days + 15

    # 5. Contre-mesures agro-écologiques d'urgence
    if stress_type == "drought":
        countermeasures = [
            "Activation du paillage organique systématique (mulch) pour bloquer l'évaporation du sol",
            "Introduction de cultures de rupture hydrique (Sorgho, Niébé à cycle court, Avoine rustique)",
            "Irrigation déficitaire régulée par les capteurs de tension racinaire GWETROOT"
        ]
    elif stress_type in ["cyclone", "flood"]:
        countermeasures = [
            "Creusement immédiat de fossés d'interception et de talus végétalisés anti-ravinement",
            "Bandes d'arrêt agroforestières (vétiver, haies de bocage, cannelier de Madagascar)",
            "Évacuation préventive de la nappe superficielle pour éviter l'asphyxie racinaire"
        ]
    else:
        countermeasures = [
            "Arrêt immédiat des aspersions foliaires et maintien d'un espacement d'aération des rangs",
            "Barrière végétale barrière de légumineuses non hôtes pour casser la dispersion des spores"
        ]

    # Global territorial vulnerability score
    avg_vulnerability = round(sum(d["accumulated_stress"] for d in parcel_states.values()) / len(parcel_states), 1)

    geojson_collection = {
        "type": "FeatureCollection",
        "features": features
    }

    # 6. Persistance dans la table rupture_zones
    rz = RuptureZone(
        region=region or ("Luxembourg" if country_detected == "LUX" else "Diana"),
        country=country_detected,
        polygon_geojson=geojson_collection,
        stress_type=stress_type,
        vulnerability_score=avg_vulnerability,
        propagation_risk={
            "duration_days": duration_days,
            "parcels_evaluated": len(parcels),
            "rupture_count": n_rupture,
            "stressed_count": n_stressed,
            "time_to_rupture_days": time_to_first_rupture,
            "area_at_risk_ha": round(total_area_rupture, 1),
            "countermeasures": countermeasures
        }
    )
    db.add(rz)
    db.commit()
    db.refresh(rz)

    return {
        "simulation_id": rz.id,
        "region": rz.region,
        "country": country_detected,
        "stress_type": stress_type,
        "duration_days": duration_days,
        "territorial_vulnerability_score": avg_vulnerability,
        "time_to_first_rupture_days": time_to_first_rupture,
        "summary": {
            "total_parcels": len(parcels),
            "rupture_count": n_rupture,
            "stressed_count": n_stressed,
            "resilient_count": len(parcels) - (n_rupture + n_stressed),
            "total_area_at_risk_ha": round(total_area_rupture, 1)
        },
        "countermeasures": countermeasures,
        "rupture_hotspots": rupture_parcels_detail[:5],
        "propagation_links_count": len(propagation_links),
        "geojson": geojson_collection
    }
