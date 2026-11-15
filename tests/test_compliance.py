"""
Tests de validation de la Souveraineté, RGPD & Auditabilité (tests/test_compliance.py).
Prompt 12 :
1. Droit à l'effacement / Droit à l'oubli (DELETE /parcels/{id}/photos)
2. Registre des activités de traitement (GET /compliance/registre - Art. 30 RGPD)
3. Journal d'audit souverain des inférences LLM (GET /audit/llm)
4. Intégrité des empreintes SHA-256 et configuration Docker souveraine
"""
import os
import io
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db import SessionLocal, init_db
from app.models import Parcel, ParcelPhoto, LLMAudit
from app.config import settings

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    init_db()

def test_right_to_erasure_photo_deletion():
    """
    Vérifie l'Article 17 du RGPD (Droit à l'effacement) :
    La suppression doit purger physiquement le fichier du disque et de la base.
    """
    db = SessionLocal()
    try:
        p = db.query(Parcel).first()
        assert p is not None

        # 1. Création d'une photo réelle sur le disque
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        dummy_file_path = os.path.join(settings.UPLOAD_DIR, f"test_compliance_{p.id}.jpg")
        with open(dummy_file_path, "wb") as f:
            f.write(b"FAKE_IMAGE_BYTES_FOR_COMPLIANCE_TEST")

        photo = ParcelPhoto(
            parcel_id=p.id,
            path=dummy_file_path,
            size_bytes=len(b"FAKE_IMAGE_BYTES_FOR_COMPLIANCE_TEST")
        )
        db.add(photo)
        db.commit()

        assert os.path.exists(dummy_file_path), "Le fichier temporaire doit exister avant suppression."

        # 2. Appel de l'endpoint DELETE /parcels/{id}/photos
        resp = client.delete(f"/parcels/{p.id}/photos")
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["status"] == "success"
        assert data["deleted_count"] >= 1
        assert data["freed_bytes"] > 0

        # 3. Vérification de la disparition physique du disque
        assert not os.path.exists(dummy_file_path), "Le fichier doit avoir été physiquement effacé du disque."

        # 4. Vérification de la suppression en base de données
        count_db = db.query(ParcelPhoto).filter(ParcelPhoto.parcel_id == p.id).count()
        assert count_db == 0, "Aucune photo ne doit subsister en base pour cette parcelle."
    finally:
        db.close()

def test_article_30_processing_registry():
    """Vérifie le registre officiel des activités de traitement (Art. 30 RGPD)."""
    resp = client.get("/compliance/registre")
    assert resp.status_code == 200, resp.text
    reg = resp.json()

    assert "responsable_traitement" in reg
    assert "hebergement_souverain" in reg
    assert "activites_de_traitement" in reg
    assert len(reg["activites_de_traitement"]) >= 4

    # Vérification des garanties de souveraineté anti-Cloud Act
    heberg = reg["hebergement_souverain"]
    assert "Zéro transfert US Cloud Act" in heberg["transfert_hors_ue"]

    # Vérification des droits des personnes
    assert "droits_personnes" in reg
    assert "effacement" in reg["droits_personnes"]

def test_llm_inference_audit_trail():
    """Vérifie la traçabilité souveraine des inférences (table llm_audit)."""
    # 1. Envoi d'une question au chatbot pour déclencher l'inférence
    chat_resp = client.post("/chat", json={"message": "Quel est le pH de mon sol ?"})
    assert chat_resp.status_code == 200

    # 2. Consultation du journal d'audit
    audit_resp = client.get("/audit/llm?limit=10")
    assert audit_resp.status_code == 200
    logs = audit_resp.json()
    assert len(logs) >= 1

    last_log = logs[0]
    assert "prompt_hash" in last_log
    assert len(last_log["prompt_hash"]) == 64, "Le hash du prompt doit être une empreinte SHA-256 de 64 caractères."
    assert "response_hash" in last_log
    assert len(last_log["response_hash"]) == 64, "Le hash de la réponse doit être une empreinte SHA-256 de 64 caractères."
    assert last_log["sovereignty_status"] == "LOCAL_EU_NO_THIRD_PARTY_TRANSFER"

def test_sovereign_docker_compose_file():
    """Vérifie l'existence et la validité du fichier de déploiement souverain européen."""
    compose_path = "docker-compose.eu.yml"
    assert os.path.exists(compose_path), "Le fichier docker-compose.eu.yml doit exister à la racine."
    with open(compose_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "DATA_RESIDENCY=EU-LUXEMBOURG" in content
    assert "CLOUD_ACT_IMMUNITY=TRUE" in content
    assert "terralux-sovereign-net" in content
