import pytest
from app.db import SessionLocal, init_db
from app.models import Parcel, Observation, SoilProfile
from app.context_fusion import contextualize_diagnosis, calculate_disease_plausibility

@pytest.fixture(autouse=True)
def setup_db():
    init_db()

@pytest.fixture
def db():
    session = SessionLocal()
    yield session
    session.close()

def test_context_fusion_diana_humidity(db):
    """TEST : sur une parcelle de Diana avec humidité simulée > 85%, l'ICC doit être > 0.75 pour le mildiou."""
    # Création d'une parcelle à Antsiranana (Diana)
    parcel = Parcel(
        name="Parcelle Diana Fusion Test",
        latitude=-12.2794,
        longitude=49.2914,
        country="MDG",
        region="Diana"
    )
    db.add(parcel)
    db.commit()

    # Observation simulée : humidité 92% (> 85%), temp 22°C
    db.add(Observation(
        parcel_id=parcel.id,
        variable="humidity",
        value=92.0,
        source="nasa_power"
    ))
    db.add(Observation(
        parcel_id=parcel.id,
        variable="temp",
        value=22.0,
        source="nasa_power"
    ))
    # Sol ferrallitique
    db.add(SoilProfile(
        parcel_id=parcel.id,
        depth_cm="0-5cm",
        ph=5.8,
        nitrogen=1.5,
        soc=20.0,
        cec=14.0,
        wrb_class="Ferralsol"
    ))
    db.commit()

    image_result = {
        "disease_id": "potato_late_blight",
        "label": "Mildiou de la pomme de terre",
        "confidence": 0.85,
        "top_3": [{"label": "Mildiou", "confidence": 0.85}]
    }

    fusion_res = contextualize_diagnosis(image_result, parcel.id, db)

    # Vérifications Prompt 6
    icc = fusion_res["contextual_confidence"]
    assert icc > 0.75, f"ICC {icc} doit être > 0.75"
    assert fusion_res["climate_plausibility"] >= 0.85
    assert "NASA POWER" in fusion_res["explanation"]
    assert "SoilGrids" in fusion_res["explanation"]
    assert fusion_res["warning"] is None

def test_context_fusion_low_confidence_warning(db):
    """Vérifie que si l'ICC < 0.50, une alerte est levée."""
    parcel = Parcel(
        name="Parcelle Incompatible",
        latitude=-12.2794,
        longitude=49.2914,
        country="MDG"
    )
    db.add(parcel)
    db.commit()

    # Image incertaine (confiance 0.30)
    image_result = {
        "disease_id": "unknown_rust",
        "label": "Rouille jaune",
        "confidence": 0.30,
        "top_3": []
    }

    fusion_res = contextualize_diagnosis(image_result, parcel.id, db)
    if fusion_res["contextual_confidence"] < 0.50:
        assert fusion_res["warning"] is not None
        assert "incertain" in fusion_res["warning"].lower()
