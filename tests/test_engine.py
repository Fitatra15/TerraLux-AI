import pytest
from datetime import datetime
from app.db import SessionLocal, init_db
from app.models import Parcel, Plant, PlantCountry, CropHistory, SoilProfile, Observation
from app.engine import (
    get_recommendation, calculate_climate_score,
    calculate_soil_score, calculate_rotation_penalty
)

@pytest.fixture(autouse=True)
def setup_db():
    init_db()

@pytest.fixture
def db():
    session = SessionLocal()
    yield session
    session.close()

def seed_sample_plants(db):
    """Seed sample plants for testing."""
    # Luxembourg wheat
    wheat = db.query(Plant).filter(Plant.scientific_name == "Triticum aestivum").first()
    if not wheat:
        wheat = Plant(
            name_fr="Blé d'hiver",
            scientific_name="Triticum aestivum",
            family="Poaceae",
            type="cereal",
            temp_min=3.0,
            temp_max=24.0,
            rain_min=500.0,
            rain_max=950.0,
            ph_min=6.0,
            ph_max=7.5
        )
        db.add(wheat)
        db.flush()
        db.add(PlantCountry(plant_id=wheat.id, country_code="LUX", status="cultivated"))

    # Madagascar rice
    rice = db.query(Plant).filter(Plant.scientific_name == "Oryza sativa").first()
    if not rice:
        rice = Plant(
            name_fr="Riz pluvial",
            scientific_name="Oryza sativa",
            family="Poaceae",
            type="cereal",
            temp_min=20.0,
            temp_max=35.0,
            rain_min=900.0,
            rain_max=1600.0,
            ph_min=5.0,
            ph_max=6.8
        )
        db.add(rice)
        db.flush()
        db.add(PlantCountry(plant_id=rice.id, country_code="MDG", status="cultivated"))

    # Madagascar cassava
    cassava = db.query(Plant).filter(Plant.scientific_name == "Manihot esculenta").first()
    if not cassava:
        cassava = Plant(
            name_fr="Manioc",
            scientific_name="Manihot esculenta",
            family="Euphorbiaceae",
            type="tuber",
            temp_min=20.0,
            temp_max=38.0,
            rain_min=600.0,
            rain_max=2000.0,
            ph_min=4.5,
            ph_max=7.5
        )
        db.add(cassava)
        db.flush()
        db.add(PlantCountry(plant_id=cassava.id, country_code="MDG", status="cultivated"))

    # Madagascar cowpea (Fabaceae)
    cowpea = db.query(Plant).filter(Plant.scientific_name == "Vigna unguiculata").first()
    if not cowpea:
        cowpea = Plant(
            name_fr="Niébé",
            scientific_name="Vigna unguiculata",
            family="Fabaceae",
            type="legume",
            temp_min=20.0,
            temp_max=35.0,
            rain_min=400.0,
            rain_max=900.0,
            ph_min=5.5,
            ph_max=7.5
        )
        db.add(cowpea)
        db.flush()
        db.add(PlantCountry(plant_id=cowpea.id, country_code="MDG", status="cultivated"))

    db.commit()

def test_filtre_pays(db):
    """TEST 1: Une plante LUX ne doit JAMAIS apparaître pour une parcelle MDG."""
    seed_sample_plants(db)

    # Création d'une parcelle à Antsiranana (MDG)
    parcel = Parcel(
        name="Parcelle Test Diana",
        latitude=-12.2794,
        longitude=49.2914,
        country="MDG",
        region="Diana"
    )
    db.add(parcel)
    db.commit()

    recs = get_recommendation(parcel.id, db)
    assert len(recs) > 0
    
    # Vérifier que toutes les plantes recommandées sont bien enregistrées pour MDG et jamais LUX
    for r in recs:
        pc_mdg = db.query(PlantCountry).filter(
            PlantCountry.plant_id == r.plant_id,
            PlantCountry.country_code == "MDG"
        ).first()
        assert pc_mdg is not None, f"La plante {r.name} n'est pas autorisée à Madagascar !"

        pc_lux = db.query(PlantCountry).filter(
            PlantCountry.plant_id == r.plant_id,
            PlantCountry.country_code == "LUX"
        ).first()
        assert pc_lux is None, f"Une plante exclusive du Luxembourg ({r.name}) a été recommandée pour Madagascar !"

def test_score_parfait(db):
    """TEST 2: Conditions idéales → score ≥ 90."""
    seed_sample_plants(db)
    rice = db.query(Plant).filter(Plant.scientific_name == "Oryza sativa").first()

    # Conditions idéales pour riz pluvial : T = 26°C, pluie = 1200mm, pH = 6.0, argile = 30%
    clim_score, pos_c, neg_c = calculate_climate_score(rice, mean_temp=26.0, annual_rain=1200.0)
    soil_score, pos_s, neg_s = calculate_soil_score(rice, ph=6.0, clay=30.0)

    # 40% clim + 30% soil + 30% rotation (100)
    total = 0.40 * clim_score + 0.30 * soil_score + 0.30 * 100.0
    assert total >= 90.0

def test_score_nul_ou_incompatible(db):
    """TEST 3: Conditions incompatibles → plante éliminée ou score < 20."""
    seed_sample_plants(db)
    rice = db.query(Plant).filter(Plant.scientific_name == "Oryza sativa").first()

    # Conditions incompatibles : T = 5°C (gel/froid intense), Pluie = 100mm (désert), pH = 3.5 (très acide)
    clim_score, pos_c, neg_c = calculate_climate_score(rice, mean_temp=5.0, annual_rain=100.0)
    soil_score, pos_s, neg_s = calculate_soil_score(rice, ph=3.5, clay=60.0)

    # Score combiné avec rotation nulle ou modérée < 20
    total_score = 0.40 * clim_score + 0.30 * soil_score + 0.30 * 0.0
    assert total_score < 20.0
    assert clim_score == 0.0
    assert soil_score == 0.0

def test_rotation(db):
    """TEST 4: Culture de la même famille N-1 → pénalité appliquée."""
    seed_sample_plants(db)
    parcel = Parcel(
        name="Parcelle Rotation Test",
        latitude=-12.2794,
        longitude=49.2914,
        country="MDG"
    )
    db.add(parcel)
    db.commit()

    current_year = datetime.utcnow().year
    rice = db.query(Plant).filter(Plant.scientific_name == "Oryza sativa").first()

    # Enregistrer du riz (Poaceae) l'année dernière N-1
    db.add(CropHistory(
        parcel_id=parcel.id,
        plant_id=rice.id,
        year=current_year - 1
    ))
    db.commit()

    # Vérification de la pénalité sur le riz (même famille Poaceae)
    penalty, reason = calculate_rotation_penalty(rice, parcel.id, db, current_year)
    assert penalty == 100.0
    assert "Poaceae" in reason

def test_raisons_presentes(db):
    """TEST 5: Chaque recommandation a au moins 1 positive et 1 negative."""
    seed_sample_plants(db)
    parcel = Parcel(
        name="Parcelle Justifications Test",
        latitude=-12.2794,
        longitude=49.2914,
        country="MDG"
    )
    db.add(parcel)
    db.commit()

    recs = get_recommendation(parcel.id, db)
    assert len(recs) > 0
    for r in recs:
        assert len(r.reasons.positive) >= 1
        assert len(r.reasons.negative) >= 1
        assert r.reasons.rotation is not None
