import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import init_db

@pytest.fixture(autouse=True)
def setup_database():
    init_db()

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data

def test_create_parcel_country_detection():
    # Luxembourg City: 49.6116, 6.1319
    lux_payload = {
        "name": "Parcelle Kirchberg",
        "latitude": 49.6116,
        "longitude": 6.1319,
        "area_ha": 2.5
    }
    lux_resp = client.post("/parcels", json=lux_payload)
    assert lux_resp.status_code == 201
    lux_data = lux_resp.json()
    assert lux_data["country"] == "LUX"
    
    # Antsiranana (Diana, Madagascar): -12.2794, 49.2914
    mdg_payload = {
        "name": "Parcelle Diego Suarez",
        "latitude": -12.2794,
        "longitude": 49.2914,
        "area_ha": 5.0
    }
    mdg_resp = client.post("/parcels", json=mdg_payload)
    assert mdg_resp.status_code == 201
    mdg_data = mdg_resp.json()
    assert mdg_data["country"] == "MDG"
    assert "Diana" in (mdg_data["region"] or "")

def test_recommendation_endpoint():
    # Create parcel first
    p_resp = client.post("/parcels", json={"latitude": -12.2794, "longitude": 49.2914})
    p_id = p_resp.json()["id"]

    rec_resp = client.get(f"/parcels/{p_id}/recommendation")
    assert rec_resp.status_code == 200
    data = rec_resp.json()
    assert len(data["top3"]) == 3
    assert all("reasons" in item for item in data["top3"])
