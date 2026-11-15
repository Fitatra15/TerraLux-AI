import pytest
from app.db import SessionLocal, init_db
from app.models import Parcel
from app.chat_agent import run_chat_agent

@pytest.fixture(autouse=True)
def setup_db():
    init_db()

@pytest.fixture
def db():
    session = SessionLocal()
    yield session
    session.close()

@pytest.fixture
def sample_parcel(db):
    parcel = db.query(Parcel).filter(Parcel.name.like("%Diego%")).first()
    if not parcel:
        parcel = Parcel(
            name="Parcelle Diego Test",
            latitude=-12.2794,
            longitude=49.2914,
            country="MDG",
            region="Diana"
        )
        db.add(parcel)
        db.commit()
    return parcel

def test_chat_greeting(db, sample_parcel):
    """TEST 4: 'Bonjour' → réponse conversationnelle simple, sans appel d'outil."""
    res = run_chat_agent("Bonjour", sample_parcel.id, db)
    assert len(res["tool_calls"]) == 0
    assert "TerraLux AI" in res["response"]

def test_chat_why_crop(db, sample_parcel):
    """TEST 1: 'Pourquoi du maïs ?' → doit appeler get_parcel_diagnosis et citer les raisons."""
    res = run_chat_agent("Pourquoi du maïs ?", sample_parcel.id, db)
    assert len(res["tool_calls"]) > 0
    tools_called = [t["tool"] for t in res["tool_calls"]]
    assert "get_parcel_diagnosis" in tools_called
    # Doit citer des sources vérifiables
    assert any(src in res["response"] for src in ["NASA POWER", "SoilGrids"])

def test_chat_soil_ph(db, sample_parcel):
    """TEST 2: 'Quel est le pH de mon sol ?' → doit appeler get_soil_richness."""
    res = run_chat_agent("Quel est le pH de mon sol ?", sample_parcel.id, db)
    assert len(res["tool_calls"]) > 0
    tools_called = [t["tool"] for t in res["tool_calls"]]
    assert "get_soil_richness" in tools_called
    assert "SoilGrids" in res["response"]
    assert "pH" in res["response"]

def test_chat_leaf_spots(db, sample_parcel):
    """TEST 3: 'J'ai une tache sur mes feuilles' → doit demander une photo puis appeler diagnose_leaf_image."""
    res = run_chat_agent("J'ai une tache sur mes feuilles", sample_parcel.id, db)
    assert len(res["tool_calls"]) > 0
    tools_called = [t["tool"] for t in res["tool_calls"]]
    assert "diagnose_leaf_image" in tools_called
    assert any(term in res["response"].lower() for term in ["photo", "diagnostiqu", "image"])
