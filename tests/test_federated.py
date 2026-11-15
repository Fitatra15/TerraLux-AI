"""
Tests de validation de l'Innovation I3 : Apprentissage Fédéré Souverain (tests/test_federated.py).
Vérifie :
1. Calcul des gradients locaux avec confidentialité différentielle (DP ε=1.0)
2. Scellement cryptographique SHA-256 de chaque gradient transmis
3. Algorithme d'agrégation FedAvg et gain de précision sur 3 rounds
4. Absence de transfert de données brutes (souveraineté garantie)
5. Endpoints REST /federated/round et /federated/status
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db import SessionLocal, init_db
from app.models import FederatedRound
from app.federated_node import FederatedNode
from app.federated_coordinator import FederatedCoordinator

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    init_db()

def test_federated_node_dp_and_hashing():
    """Vérifie le calcul local différentiellement privé et le hash SHA-256."""
    node_lux = FederatedNode("node_lux", "LUX", n_samples=100)
    weights = [0.5] * 12

    update = node_lux.compute_local_update(weights, round_number=1, epsilon=1.0)

    assert update["node_id"] == "node_lux"
    assert update["country"] == "LUX"
    assert len(update["gradients"]) == 12
    assert "gradient_hash" in update
    assert len(update["gradient_hash"]) == 64, "Le hash SHA-256 du gradient doit comporter 64 caractères."
    assert "Gaussian Mechanism" in update["dp_guarantee"]
    assert 0.0 <= update["local_accuracy"] <= 1.0

def test_fedavg_simulation_convergence():
    """Vérifie l'amélioration de la précision globale sur 3 rounds d'apprentissage."""
    db = SessionLocal()
    try:
        coord = FederatedCoordinator()
        res = coord.run_simulation(n_rounds=3, db=db, epsilon=1.0)

        assert res["status"] == "COMPLETED"
        assert res["rounds_executed"] == 3
        assert res["final_accuracy"] >= res["initial_accuracy"], (
            f"La précision finale {res['final_accuracy']} doit converger au-dessus de {res['initial_accuracy']}."
        )
        assert res["raw_data_transferred"] is False, "Aucune donnée brute ne doit être transférée hors du noeud."
        assert len(res["rounds"]) == 3

        # Vérifier l'insertion dans la table federated_rounds
        saved_rounds = db.query(FederatedRound).all()
        assert len(saved_rounds) >= 6 # 2 noeuds * 3 rounds = 6 enregistrements
    finally:
        db.close()

def test_federated_api_endpoints():
    """Vérifie les endpoints REST pour l'apprentissage fédéré."""
    # 1. POST /federated/round (Simulation 3 rounds)
    resp = client.post("/federated/round?simulate_3_rounds=true&epsilon=1.0")
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["status"] == "COMPLETED"
    assert data["rounds_executed"] == 3
    assert data["data_sovereignty_verified"] is True

    # 2. GET /federated/status
    resp_status = client.get("/federated/status")
    assert resp_status.status_code == 200
    st_data = resp_status.json()
    assert st_data["network_active"] is True
    assert len(st_data["nodes"]) == 2
    assert st_data["total_rounds_logged"] >= 6
    assert len(st_data["recent_history"]) >= 1
    assert "gradient_hash" in st_data["recent_history"][0]
