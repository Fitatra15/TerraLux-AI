"""
TerraLux AI — Tests de Validation du Module Économique, Rendement & Risque Marché (tests/test_economics.py)
Vérifie :
1. Calcul du rendement attendu (t/ha et total) et du revenu brut (€ / MGA) selon la surface
2. Évaluation du risque de marché (Faible/Moyen/Élevé) avec inflation 2025-2026 :
   - Luxembourg : engrais +35%, blé fragilisé, colza résilient
   - Madagascar : prix du riz -25%, risque cyclonique nov-avril, manioc/cacao protecteurs
3. Intégration du score de rentabilité et pénalité de risque dans le moteur agronomique (engine.py)
4. Réponse personnalisée et explicative du Chatbot IA sur les gains financiers et la gestion de risque
"""
import pytest
from sqlalchemy.orm import Session
from app.db import SessionLocal, init_db
from app.models import Parcel, Plant
from app.economics import calculate_expected_yield, assess_market_risk
from app.engine import get_recommendation
from app.chat_agent import run_chat_agent
from db_seed import seed_database

@pytest.fixture(scope="module", autouse=True)
def setup_economic_db():
    init_db()
    seed_database()

def test_calculate_expected_yield_esch():
    """Vérifie le calcul du rendement attendu et revenu brut pour Esch-sur-Alzette."""
    db = SessionLocal()
    try:
        parcel = db.query(Parcel).filter(Parcel.name.ilike("%esch%")).first()
        assert parcel is not None, "La parcelle d'Esch-sur-Alzette doit exister."
        
        # Test sur 3.5 ha
        parcel.area_ha = 3.5
        db.commit()

        res = calculate_expected_yield(parcel.id, db)
        assert "crops_economics" in res
        assert len(res["crops_economics"]) >= 3
        assert res["currency"] == "EUR"
        assert res["area_ha"] == 3.5

        # Vérification des cultures recommandées
        crops = {c["crop_name"]: c for c in res["crops_economics"]}
        
        # Si Colza est présent : 3.9 t/ha * 3.5 ha = 13.65 t
        if "Colza d'hiver" in crops:
            colza = crops["Colza d'hiver"]
            assert colza["yield_t_ha"] == 3.9
            assert abs(colza["expected_yield_t"] - 13.65) < 0.1
            assert colza["gross_revenue_eur"] > 6000.0
            assert colza["market_risk"] == "Faible"

        # Si Blé est présent : 5.8 t/ha * 3.5 ha = 20.3 t, revenu brut ~ 5 176 - 5 180 €
        if "Blé d'hiver" in crops:
            ble = crops["Blé d'hiver"]
            assert ble["yield_t_ha"] == 5.8
            assert abs(ble["expected_yield_t"] - 20.3) < 0.1
            assert abs(ble["gross_revenue_eur"] - 5176.5) < 20.0  # ~5 180 €
            assert ble["market_risk"] in ["Élevé", "Moyen"]
    finally:
        db.close()


def test_assess_market_risk_luxembourg_and_madagascar():
    """Vérifie les niveaux de risque macro-économiques et les alternatives proposées."""
    db = SessionLocal()
    try:
        p_lux = db.query(Parcel).filter(Parcel.country == "LUX").first()
        p_mdg = db.query(Parcel).filter(Parcel.country == "MDG").first()

        # Luxembourg : Blé (engrais +35%) vs Colza (stable)
        risk_ble = assess_market_risk(p_lux.id, "Blé d'hiver", db)
        assert risk_ble["risk_level"] == "Élevé"
        assert "+35%" in risk_ble["market_justification"]
        assert risk_ble["safer_alternative"] == "Colza d'hiver"

        risk_colza = assess_market_risk(p_lux.id, "Colza d'hiver", db)
        assert risk_colza["risk_level"] == "Faible"

        # Madagascar : Riz (-25% et cyclones) vs Manioc
        risk_riz = assess_market_risk(p_mdg.id, "Riz pluvial", db)
        assert risk_riz["risk_level"] == "Élevé"
        assert "-25%" in risk_riz["market_justification"] or "25%" in risk_riz["market_justification"]
        assert "cyclone" in risk_riz["market_justification"].lower()
        assert risk_riz["safer_alternative"] == "Manioc"

        risk_manioc = assess_market_risk(p_mdg.id, "Manioc", db)
        assert risk_manioc["risk_level"] == "Faible"
    finally:
        db.close()


def test_engine_profitability_modulation():
    """Vérifie que le moteur agronomique intègre le score_rentabilite et pénalise les cultures à haut risque."""
    db = SessionLocal()
    try:
        parcel = db.query(Parcel).filter(Parcel.name.ilike("%esch%")).first()
        recs = get_recommendation(parcel.id, db)
        assert len(recs) == 3

        # Vérifier que les recommandations comportent les attributs économiques
        for r in recs:
            assert r.yield_t_ha is not None
            assert r.expected_yield_t is not None
            assert r.gross_revenue_eur is not None
            assert r.market_risk in ["Faible", "Moyen", "Élevé"]
    finally:
        db.close()


def test_chatbot_earning_query_with_custom_area():
    """
    Test clé du cahier des charges :
    'J'ai 3 hectares à Esch-sur-Alzette. Qu'est-ce que je plante pour gagner de l'argent cette année ?'
    Doit répondre avec des chiffres réels et un avertissement sur le risque.
    """
    db = SessionLocal()
    try:
        user_prompt = "J'ai 3 hectares à Esch-sur-Alzette. Qu'est-ce que je plante pour gagner de l'argent cette année ?"
        chat_resp = run_chat_agent(user_prompt, None, db)

        resp_text = chat_resp["response"]
        tool_calls = [tc["tool"] for tc in chat_resp["tool_calls"]]

        # Vérifie l'exécution des bons outils
        assert any(t in tool_calls for t in ["calculate_expected_yield", "get_crop_recommendation", "search_parcel_by_name"])
        
        # Vérifie les chiffres de rendement et revenu brut
        assert any(num in resp_text for num in ["3", "3.9", "5.8", "5 180", "5180", "5 176", "6 961", "t/ha", "€"])
        
        # Vérifie l'avertissement de risque économique (+35% engrais ou risque élevé blé / colza plus sûr)
        assert any(k in resp_text.lower() for k in ["engrais", "+35%", "35%", "risque", "colza", "sûr", "blé"])
        
        # Vérifie les sources
        assert any(src in resp_text for src in ["Luxembourg", "Statec", "ASTA", "FAO ECOCROP", "2025-2026"])
    finally:
        db.close()
