"""
Tests de validation de l'Innovation I1 : Passeport de Résilience (tests/test_passport.py).
Vérifie :
1. Calcul des 4 piliers de résilience et formule de score global
2. Attribution des grades bancables (AAA, AA, A, B)
3. Génération physique du PDF certifié, QR Code et empreinte SHA-256
4. Endpoint public de vérification d'authenticité /passport/verify/{hash}
5. Rejet immédiat de faux certificats (404 Not Found)
"""
import os
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db import SessionLocal, init_db
from app.models import Parcel, ResiliencePassport
from app.passport_generator import calculate_passport_metrics, compute_resilience_passport

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    init_db()

def test_passport_formula_and_pillars():
    """Vérifie la formule de pondération des 4 piliers."""
    db = SessionLocal()
    try:
        p = db.query(Parcel).first()
        assert p is not None, "Une parcelle doit exister."

        components, grade, score = calculate_passport_metrics(p.id, db)

        # Vérification des bornes des 4 piliers (0-100)
        assert 0.0 <= components["richness_index"] <= 100.0
        assert 0.0 <= components["climate_resilience"] <= 100.0
        assert 0.0 <= components["water_security"] <= 100.0
        assert 0.0 <= components["disease_risk_score"] <= 100.0

        # Vérification arithmétique exacte
        expected_score = round(
            0.35 * components["richness_index"] +
            0.30 * components["climate_resilience"] +
            0.20 * (100.0 - components["water_stress_risk"]) +
            0.15 * (100.0 - components["disease_risk_score"]),
            1
        )
        assert score == expected_score, f"Erreur de calcul du score : {score} != {expected_score}"

        # Vérification du grade
        if score >= 85.0:
            assert grade == "AAA"
        elif score >= 70.0:
            assert grade == "AA"
        elif score >= 55.0:
            assert grade == "A"
        else:
            assert grade == "B"
    finally:
        db.close()

def test_compute_passport_and_pdf_generation():
    """Vérifie la génération complète du passeport et du PDF scellé sur disque."""
    db = SessionLocal()
    try:
        p = db.query(Parcel).first()
        passport = compute_resilience_passport(p.id, db)

        assert passport.content_hash is not None
        assert len(passport.content_hash) == 64, "L'empreinte SHA-256 doit comporter 64 caractères hexadécimaux."
        assert passport.pdf_path is not None
        assert os.path.exists(passport.pdf_path), "Le PDF certifié doit être écrit sur disque."
        assert os.path.getsize(passport.pdf_path) > 1000, "Le PDF certifié ne doit pas être vide."
    finally:
        db.close()

def test_passport_api_endpoints_and_verification():
    """Vérifie les endpoints REST et la vérification publique par hash."""
    db = SessionLocal()
    try:
        p = db.query(Parcel).first()
        parcel_id = p.id

        # 1. Génération via POST /passport/{id}
        resp = client.post(f"/passport/{parcel_id}")
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["status"] == "success"
        assert "content_hash" in data
        assert "global_score" in data
        hash_code = data["content_hash"]

        # 2. Téléchargement PDF
        resp_pdf = client.get(f"/passport/{parcel_id}/pdf")
        assert resp_pdf.status_code == 200
        assert resp_pdf.headers.get("content-type") == "application/pdf"

        # 3. Vérification publique d'authenticité bancaire
        resp_verify = client.get(f"/passport/verify/{hash_code}")
        assert resp_verify.status_code == 200
        v_data = resp_verify.json()
        assert v_data["verified"] is True
        assert v_data["certification_status"] == "CERTIFIÉ CONFORME & AUDITABLE"
        assert v_data["parcel_id"] == parcel_id
        assert v_data["cryptographic_hash"] == hash_code

        # 4. Rejet d'un faux hash ou certificat altéré
        fake_hash = "0" * 64
        resp_fake = client.get(f"/passport/verify/{fake_hash}")
        assert resp_fake.status_code == 404, "Un hash inexistant doit être rejeté avec code 404."
    finally:
        db.close()
