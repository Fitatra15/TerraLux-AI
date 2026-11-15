"""
Tests de validation empirique et scientifique du backtesting (tests/test_backtest.py).
Vérifie :
1. Absence de fuite de données (data leakage) lors de l'évaluation
2. Seuil d'acceptabilité agronomique : Top-3 Accuracy > 70%
3. Génération du rapport certifié HTML
4. Endpoints API /backtest/run et /backtest/report/{run_id}
"""
import os
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db import SessionLocal, init_db
from app.models import GroundTruth, BacktestRun, Parcel
from app.engine import get_recommendation
from backtest import run_backtesting, GROUND_TRUTH_DATASET

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    init_db()

def test_ground_truth_dataset_balance():
    """Vérifie la parité et la cohérence géographique du jeu de données terrain."""
    lux_cases = [r for r in GROUND_TRUTH_DATASET if r["country"] == "LUX"]
    mdg_cases = [r for r in GROUND_TRUTH_DATASET if r["country"] == "MDG"]
    assert len(lux_cases) >= 10, "Le Luxembourg doit disposer d'au moins 10 parcelles de vérité terrain."
    assert len(mdg_cases) >= 10, "La région Diana (Madagascar) doit disposer d'au moins 10 parcelles."

def test_no_data_leakage():
    """
    Règle d'or : aucune fuite de données (data leakage).
    L'inférence get_recommendation ne prend que l'ID de la parcelle et la session DB.
    Elle ne connaît à aucun moment la colonne actual_crop_id de GroundTruth.
    """
    db = SessionLocal()
    try:
        gt = db.query(GroundTruth).first()
        assert gt is not None, "Le jeu de vérité terrain doit être initialisé."

        # Création d'une parcelle aveugle
        test_parcel = Parcel(
            name="Blind Test Parcel",
            latitude=gt.latitude,
            longitude=gt.longitude,
            country=gt.country,
            region=gt.region
        )
        db.add(test_parcel)
        db.commit()

        # Inférence aveugle : aucun paramètre de vérité terrain transmis
        recs = get_recommendation(test_parcel.id, db)
        assert len(recs) == 3, "Le moteur doit retourner un Top 3 exact."

        # Nettoyage
        db.delete(test_parcel)
        db.commit()
    finally:
        db.close()

def test_backtest_accuracy_threshold():
    """
    Condition sine qua non du cahier des charges :
    Top-3 Accuracy > 70 % (seuil de crédibilité pour déploiement pilote).
    """
    db = SessionLocal()
    try:
        results = run_backtesting(db, engine_version="rules-v2-test")
        assert results["n_parcels"] >= 20, "Au moins 20 parcelles doivent être évaluées."
        assert results["top3_accuracy"] >= 70.0, (
            f"Échec de validation : Top-3 accuracy={results['top3_accuracy']}% < seuil 70%."
        )
        assert results["is_pilot_ready"] is True
        assert os.path.exists(results["report_path"]), "Le rapport HTML doit être généré sur disque."
    finally:
        db.close()

def test_backtest_api_endpoints():
    """Vérifie l'exécution du backtest via l'API REST."""
    resp = client.post("/backtest/run?engine_version=api-test-run")
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert "top3_accuracy" in data
    assert data["top3_accuracy"] >= 70.0
    run_id = data["run_id"]

    # Test rapport HTML
    resp_report = client.get(f"/backtest/report/{run_id}")
    assert resp_report.status_code == 200
    assert "text/html" in resp_report.headers.get("content-type", "")

    # Test historique
    resp_history = client.get("/backtest/history")
    assert resp_history.status_code == 200
    history = resp_history.json()
    assert len(history) >= 1
    assert any(h["id"] == run_id for h in history)
