"""
TerraLux AI — Module Richesse du Sol 3D & Intelligence Pédologique
Multi-profondeur (0-5cm, 5-15cm, 15-30cm), Indice de Richesse 0-100, Détection des Carences.
"""
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models import Parcel, SoilProfile
from app.config import settings

def normalize_soc(soc: float) -> float:
    """Normalise la teneur en Carbone Organique du Sol (g/kg) sur une échelle 0-100."""
    if soc is None or soc <= 0:
        return 0.0
    # 30 g/kg ou plus = 100/100
    score = (soc / 30.0) * 100.0
    return min(100.0, max(0.0, score))

def normalize_cec(cec: float) -> float:
    """Normalise la Capacité d'Échange Cationique (cmol/kg) sur une échelle 0-100."""
    if cec is None or cec <= 0:
        return 0.0
    # 25 cmol/kg ou plus = 100/100
    score = (cec / 25.0) * 100.0
    return min(100.0, max(0.0, score))

def normalize_nitrogen(nitrogen: float) -> float:
    """Normalise l'Azote Total (g/kg) sur une échelle 0-100."""
    if nitrogen is None or nitrogen <= 0:
        return 0.0
    # 3.0 g/kg ou plus = 100/100
    score = (nitrogen / 3.0) * 100.0
    return min(100.0, max(0.0, score))

def normalize_ph(ph: float) -> float:
    """Normalise le pH (H2O) : optimum agronomique entre 6.0 et 7.0."""
    if ph is None:
        return 50.0
    if 6.0 <= ph <= 7.0:
        return 100.0
    elif ph < 6.0:
        # Dégressif jusqu'à pH 4.0 (score 0)
        return max(0.0, 100.0 - (6.0 - ph) * 50.0)
    else:
        # Dégressif au-dessus de 7.0 jusqu'à pH 9.0 (score 0)
        return max(0.0, 100.0 - (ph - 7.0) * 50.0)

def compute_richness_index(soc: float, cec: float, nitrogen: float, ph: float) -> float:
    """
    Calcule l'Indice de Richesse du Sol (0-100) pondéré :
    - 40% SOC (Carbone organique du sol)
    - 30% CEC (Capacité d'échange cationique)
    - 20% Azote total (N)
    - 10% pH normalisé
    """
    s_soc = normalize_soc(soc)
    s_cec = normalize_cec(cec)
    s_n = normalize_nitrogen(nitrogen)
    s_ph = normalize_ph(ph)

    index = (
        settings.WEIGHT_RICHNESS_SOC * s_soc +
        settings.WEIGHT_RICHNESS_CEC * s_cec +
        settings.WEIGHT_RICHNESS_N * s_n +
        settings.WEIGHT_RICHNESS_PH * s_ph
    )
    return round(index, 1)

def get_soil_profile(parcel_id: str, db: Session) -> Dict[str, Any]:
    """
    Récupère le profil multi-profondeurs pour une parcelle,
    calcule l'indice global pondéré (50% 0-5cm, 30% 5-15cm, 20% 15-30cm),
    identifie les carences et formule une interprétation agronomique.
    """
    parcel = db.query(Parcel).filter(Parcel.id == parcel_id).first()
    profiles = db.query(SoilProfile).filter(SoilProfile.parcel_id == parcel_id).all()

    # Si pas encore en base, profil contextualisé par défaut
    if not profiles:
        is_mdg = (parcel.country == "MDG") if parcel else False
        wrb = "Ferralsol rhodi-lixique" if is_mdg else "Cambisol calcaro-eutrique"
        surface_soc = 21.4 if is_mdg else 28.2
        surface_cec = 14.2 if is_mdg else 22.8
        surface_n = 1.6 if is_mdg else 2.4
        surface_ph = 5.8 if is_mdg else 6.6
        richness = compute_richness_index(surface_soc, surface_cec, surface_n, surface_ph)
    else:
        # Trouver profil de surface 0-5
        prof_0_5 = next((p for p in profiles if p.depth_cm in ["0-5", "0-5cm"]), profiles[0])
        prof_5_15 = next((p for p in profiles if p.depth_cm in ["5-15", "5-15cm"]), None)
        prof_15_30 = next((p for p in profiles if p.depth_cm in ["15-30", "15-30cm"]), None)

        wrb = prof_0_5.wrb_class or ("Ferralsol" if parcel and parcel.country == "MDG" else "Cambisol")
        surface_soc = prof_0_5.soc or 20.0
        surface_cec = prof_0_5.cec or 15.0
        surface_n = prof_0_5.nitrogen or 1.5
        surface_ph = prof_0_5.ph or 6.2

        # Calcul multi-profondeur pondéré
        idx_0_5 = compute_richness_index(surface_soc, surface_cec, surface_n, surface_ph)
        idx_5_15 = compute_richness_index(prof_5_15.soc, prof_5_15.cec, prof_5_15.nitrogen, prof_5_15.ph) if prof_5_15 else idx_0_5 * 0.9
        idx_15_30 = compute_richness_index(prof_15_30.soc, prof_15_30.cec, prof_15_30.nitrogen, prof_15_30.ph) if prof_15_30 else idx_0_5 * 0.8

        richness = round(0.50 * idx_0_5 + 0.30 * idx_5_15 + 0.20 * idx_15_30, 1)

    # Détection des carences
    deficiencies: List[str] = []
    if surface_soc < 10.0:
        deficiencies.append("Carbon deficiency")
    if surface_n < 1.0:
        deficiencies.append("Nitrogen deficiency")
    if surface_cec < 10.0:
        deficiencies.append("Low nutrient retention capacity")
    if surface_ph < 5.5:
        deficiencies.append("Excessive acidity (phosphorus lock-up risk)")

    # Qualification du score
    if richness >= 80:
        richness_label = "Excellent"
    elif richness >= 65:
        richness_label = "Good"
    elif richness >= 50:
        richness_label = "Moderate"
    else:
        richness_label = "Degraded / Low"

    # Interprétation experte
    lat = float(parcel.latitude) if (parcel and parcel.latitude is not None) else 0.0
    is_diana = (lat < 0) or (parcel and (parcel.country == "MDG" or (parcel.region and "Diana" in parcel.region)))
    if is_diana or "Ferralsol" in wrb:
        interpretation = (
            f"Tropical {wrb} soil characteristic of the Diana region. Good surface organic matter content ({surface_soc} g/kg), "
            f"but nitrogen and phosphorus can be limiting for demanding crops. Organic amendments and bio-mulching recommended."
        )
    else:
        interpretation = (
            f"Temperate {wrb} soil with high natural fertility (index {richness}/100). "
            f"Excellent plant available water capacity and optimal pH ({surface_ph}) for Luxembourg cereals and legumes."
        )

    return {
        "parcel_id": parcel_id,
        "wrb_class": wrb,
        "richness_index": richness,
        "richness_label": richness_label,
        "properties": {
            "soc": {
                "value": float(surface_soc),
                "unit": "g/kg",
                "depth": "0-5cm",
                "status": "Good" if surface_soc >= 20 else ("Moderate" if surface_soc >= 10 else "Low")
            },
            "nitrogen": {
                "value": float(surface_n),
                "unit": "g/kg",
                "depth": "0-5cm",
                "status": "Satisfactory" if surface_n >= 2.0 else ("Moderate" if surface_n >= 1.0 else "Deficient")
            },
            "cec": {
                "value": float(surface_cec),
                "unit": "cmol/kg",
                "depth": "0-5cm",
                "status": "High" if surface_cec >= 20 else ("Moderate" if surface_cec >= 10 else "Low")
            },
            "ph": {
                "value": float(surface_ph),
                "unit": "pH H2O",
                "depth": "0-5cm",
                "status": "Optimal" if 6.0 <= surface_ph <= 7.2 else ("Acidic" if surface_ph < 6.0 else "Alkaline")
            }
        },
        "deficiencies": deficiencies if deficiencies else ["No major deficiency detected"],
        "interpretation": interpretation
    }
