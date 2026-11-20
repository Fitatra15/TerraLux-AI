import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import SessionLocal, init_db
from app.models import Parcel, SoilProfile
from app.dynamic_engine import DynamicDataEngine
from app.chat_agent import run_chat_agent

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    init_db()

@pytest.fixture
def db_session():
    session = SessionLocal()
    yield session
    session.close()

def test_tavily_search_dynamic():
    """Verify Tavily web search returns structured scientific sources with live URLs."""
    res = DynamicDataEngine.search_tavily("drought resistant tree species Ferralsol Diana Madagascar", max_results=3)
    assert "results" in res
    assert len(res["results"]) > 0
    first_result = res["results"][0]
    assert "url" in first_result and first_result["url"].startswith("http")
    assert "title" in first_result

def test_dynamic_restoration_plan_endpoint(db_session):
    """Verify GET /api/restoration/plan returns zero hardcoded species and live Tavily sources."""
    resp = client.get("/api/restoration/plan")
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert "recommended_species" in data
    assert len(data["recommended_species"]) >= 3
    for sp in data["recommended_species"]:
        assert "scientific_name" in sp
        assert "source_url" in sp and sp["source_url"].startswith("http")
        assert "soil_compatibility_score" in sp
        assert "drought_resistance" in sp

def test_dynamic_dashboard_summary_endpoint():
    """Verify GET /api/dashboard/dynamic-summary returns live web trends and real parcel counts."""
    resp = client.get("/api/dashboard/dynamic-summary")
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert "total_parcels" in data
    assert "executive_summary" in data
    assert len(data["executive_summary"]) > 20
    assert "live_web_insights" in data

def test_dynamic_past_events_endpoint(db_session):
    """Verify GET /api/parcels/{id}/dynamic-events returns historical shocks fused with web."""
    parcel = db_session.query(Parcel).first()
    pid = parcel.id if parcel else "demo-diana"
    resp = client.get(f"/api/parcels/{pid}/dynamic-events")
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert "events" in data
    assert len(data["events"]) > 0
    assert any("title" in e for e in data["events"])

def test_parcel_delete_cascade_endpoint(db_session):
    """Verify DELETE /api/parcels/{id} removes the parcel and cascades to related records."""
    # Create test parcel
    test_p = Parcel(
        name="Temporary Delete Test Parcel",
        latitude=49.61,
        longitude=6.13,
        country="LUX",
        region="Gutland",
        area_ha=2.0
    )
    db_session.add(test_p)
    db_session.commit()
    target_id = test_p.id

    # Verify exists
    assert db_session.query(Parcel).filter(Parcel.id == target_id).first() is not None

    # Delete via API
    resp = client.delete(f"/api/parcels/{target_id}")
    assert resp.status_code == 200, resp.text
    assert resp.json()["status"] == "success"

    # Verify removed
    assert db_session.query(Parcel).filter(Parcel.id == target_id).first() is None

def test_chat_agent_with_tavily_tool(db_session):
    """Verify chat agent executes search_web_tavily when asked about tree or agroforestry species."""
    parcel = db_session.query(Parcel).first()
    pid = parcel.id if parcel else None
    res = run_chat_agent("Quels arbres ou espèces agroforestières me conseilles-tu via Tavily ?", pid, db_session)
    assert len(res["tool_calls"]) > 0
    tools_called = [tc["tool"] for tc in res["tool_calls"]]
    assert any(t in tools_called for t in ["search_web_tavily", "get_parcel_diagnosis"])
