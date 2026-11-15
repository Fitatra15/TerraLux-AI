"""
Tests de validation de l'Innovation I2 : Jumeau de Rupture (tests/test_rupture.py).
Vérifie :
1. Simulation de stress hydrique et rupture au Luxembourg (sécheresse)
2. Simulation de choc cyclonique et submersion à Madagascar (Diana)
3. Modélisation de propagation spatiale par graphe de voisinage
4. Structure cartographique GeoJSON (FeatureCollection)
5. Endpoints REST /rupture/simulate, /rupture/zones et /rupture/geojson
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db import SessionLocal, init_db
from app.models import Parcel, RuptureZone
from app.rupture_twin import simulate_stress_propagation, haversine_distance_km

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    init_db()

def test_haversine_distance_calculation():
    """Vérifie l'exactitude mathématique de la distance géodésique."""
    # Distance Luxembourg-ville à Esch-sur-Alzette (~17-18 km)
    d = haversine_distance_km(49.6116, 6.1319, 49.4958, 5.9806)
    assert 15.0 <= d <= 20.0, f"Distance inattendue : {d:.1f} km"

    # Même point -> 0 km
    d_zero = haversine_distance_km(49.6116, 6.1319, 49.6116, 6.1319)
    assert round(d_zero, 3) == 0.0

def test_simulate_drought_luxembourg():
    """Vérifie la simulation d'une sécheresse sévère de 45 jours au Luxembourg."""
    db = SessionLocal()
    try:
        res = simulate_stress_propagation(
            region="Luxembourg",
            stress_type="drought",
            duration_days=45,
            country="LUX",
            db=db
        )

        assert res["country"] == "LUX"
        assert res["stress_type"] == "drought"
        assert "territorial_vulnerability_score" in res
        assert 0.0 <= res["territorial_vulnerability_score"] <= 100.0
        assert res["time_to_first_rupture_days"] > 0
        assert len(res["countermeasures"]) >= 2
        assert "geojson" in res
        assert res["geojson"]["type"] == "FeatureCollection"
        assert len(res["geojson"]["features"]) >= 1
    finally:
        db.close()

def test_simulate_cyclone_madagascar_diana():
    """Vérifie la simulation d'un épisode cyclonique majeur dans la région Diana."""
    db = SessionLocal()
    try:
        res = simulate_stress_propagation(
            region="Diana",
            stress_type="cyclone",
            duration_days=14,
            country="MDG",
            db=db
        )

        assert res["country"] == "MDG"
        assert res["stress_type"] == "cyclone"
        assert res["summary"]["total_parcels"] >= 1
        assert "countermeasures" in res
        # Vérification des contre-mesures spécifiques aux inondations/cyclones
        assert any("fossés" in c or "agroforest" in c or "vétiver" in c for c in res["countermeasures"])
    finally:
        db.close()

def test_rupture_api_endpoints():
    """Vérifie les endpoints REST pour le Jumeau de Rupture."""
    # 1. POST /rupture/simulate
    payload = {
        "region": "Gutland",
        "stress_type": "drought",
        "duration_days": 30,
        "country": "LUX"
    }
    resp = client.post("/rupture/simulate", json=payload)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert "simulation_id" in data
    assert "territorial_vulnerability_score" in data
    sim_id = data["simulation_id"]

    # 2. GET /rupture/zones
    resp_list = client.get("/rupture/zones?stress_type=drought")
    assert resp_list.status_code == 200
    zones = resp_list.json()
    assert len(zones) >= 1
    assert any(z["id"] == sim_id for z in zones)

    # 3. GET /rupture/geojson
    resp_geo = client.get("/rupture/geojson?region=Gutland")
    assert resp_geo.status_code == 200
    geo = resp_geo.json()
    assert geo["type"] == "FeatureCollection"
    assert "features" in geo
