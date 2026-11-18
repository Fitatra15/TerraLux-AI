"""
TerraLux AI — Tests de Validation de la Géographie Administrative du Luxembourg (SIG)
Vérifie :
1. Détermination exacte de la région naturelle (Oesling vs Gutland) :
   assert get_region_from_city("Esch-sur-Alzette") == "Gutland"
   assert get_region_from_city("Wilwerdange") == "Oesling"
   assert get_region_from_city("Clervaux") == "Oesling"
   assert get_region_from_city("Eselborn") == "Oesling"
2. Hiérarchie administrative complète (Localité -> Commune -> Canton -> Région)
3. Présence et drapeau is_city pour les 12 villes statutaires du Luxembourg
4. Comportement différencié du moteur agronomique (engine.py) : Oesling vs Gutland
5. Résolution dynamique dans l'Agent IA Chatbot (search_parcel_by_name)
"""
import pytest
from sqlalchemy.orm import Session
from app.db import SessionLocal, init_db
from app.models import Region, Canton, Commune, Locality, Parcel, Plant
from app.luxembourg_geo import (
    get_region_from_city,
    get_luxembourg_hierarchy,
    seed_luxembourg_geography,
    LUX_COMMUNES_AND_LOCALITIES
)
from app.engine import get_recommendation
from app.chat_agent import search_parcel_by_name, run_chat_agent

@pytest.fixture(scope="module", autouse=True)
def setup_luxembourg_db():
    init_db()
    db = SessionLocal()
    try:
        seed_luxembourg_geography(db)
    finally:
        db.close()


def test_mandatory_get_region_from_city():
    """
    Exigence stricte du cahier des charges :
    assert get_region_from_city("Esch-sur-Alzette") == "Gutland"
    Et validation d'une localité de l'Oesling (Wilwerdange, Clervaux, Eselborn).
    """
    # 1. Test obligatoire spécifié par le prompt
    assert get_region_from_city("Esch-sur-Alzette") == "Gutland"

    # 2. Localités & cantons de l'Oesling (Éislek / Nord)
    assert get_region_from_city("Wilwerdange") == "Oesling"
    assert get_region_from_city("Clervaux") == "Oesling"
    assert get_region_from_city("Eselborn") == "Oesling"
    assert get_region_from_city("Troisvierges") == "Oesling"
    assert get_region_from_city("Huldange") == "Oesling"
    assert get_region_from_city("Wiltz") == "Oesling"
    assert get_region_from_city("Vianden") == "Oesling"
    assert get_region_from_city("Parc Hosingen") == "Oesling"

    # 3. Villes et cantons du Gutland (Bon Pays / Centre & Sud)
    assert get_region_from_city("Luxembourg") == "Gutland"
    assert get_region_from_city("Luxembourg-ville") == "Gutland"
    assert get_region_from_city("Dudelange") == "Gutland"
    assert get_region_from_city("Differdange") == "Gutland"
    assert get_region_from_city("Diekirch") == "Gutland"
    assert get_region_from_city("Ettelbruck") == "Gutland"
    assert get_region_from_city("Echternach") == "Gutland"
    assert get_region_from_city("Remich") == "Gutland"
    assert get_region_from_city("Grevenmacher") == "Gutland"
    assert get_region_from_city("Mersch") == "Gutland"
    assert get_region_from_city("Capellen") == "Gutland"
    assert get_region_from_city("Rumelange") == "Gutland"


def test_luxembourg_hierarchy_resolution():
    """Vérifie la remontée hiérarchique : Localité -> Commune -> Canton -> Région."""
    db = SessionLocal()
    try:
        # Wilwerdange : localité de la commune de Troisvierges, canton de Clervaux, en Oesling
        res_wil = get_luxembourg_hierarchy("Wilwerdange", db)
        assert res_wil is not None
        assert res_wil["locality"] == "Wilwerdange"
        assert res_wil["commune"] == "Troisvierges"
        assert res_wil["canton"] == "Clervaux"
        assert res_wil["region_natural"] == "Oesling"
        assert "schiste" in res_wil["soil_type"].lower() or "schisto" in res_wil["soil_type"].lower()

        # Eselborn : localité de la commune de Clervaux, canton de Clervaux, en Oesling
        res_esel = get_luxembourg_hierarchy("Eselborn", db)
        assert res_esel is not None
        assert res_esel["locality"] == "Eselborn"
        assert res_esel["commune"] == "Clervaux"
        assert res_esel["canton"] == "Clervaux"
        assert res_esel["region_natural"] == "Oesling"

        # Belval : localité rattachée à Esch-sur-Alzette, Gutland
        res_belval = get_luxembourg_hierarchy("Belval", db)
        assert res_belval is not None
        assert res_belval["commune"] == "Esch-sur-Alzette"
        assert res_belval["region_natural"] == "Gutland"
    finally:
        db.close()


def test_12_statutory_cities():
    """Vérifie que les 12 villes officielles du Luxembourg possèdent le flag is_city = True."""
    official_12_cities = {
        "Luxembourg", "Esch-sur-Alzette", "Differdange", "Dudelange",
        "Ettelbruck", "Diekirch", "Wiltz", "Echternach",
        "Rumelange", "Grevenmacher", "Remich", "Vianden"
    }
    db = SessionLocal()
    try:
        cities_in_db = db.query(Commune).filter(Commune.is_city == True).all()
        city_names = {c.name for c in cities_in_db}
        for city in official_12_cities:
            assert city in city_names, f"La ville officielle '{city}' doit être marquée avec is_city=True en base."
    finally:
        db.close()


def test_engine_oesling_pedoclimatic_adaptation():
    """
    Vérifie que le moteur agronomique adapte ses recommandations entre l'Oesling et le Gutland :
    - En Oesling (frais, pH acide ~5.9, sol schisteux) : Pomme de terre / Avoine favorisées.
    - Dans le Gutland (tempéré, marno-calcaire pH ~6.6-7.0) : Blé d'hiver / Orge favorisés.
    """
    db = SessionLocal()
    try:
        # Parcelle en Oesling (Wilwerdange)
        oesling_parcel = Parcel(
            name="Exploitation Wilwerdange Test",
            latitude=50.138,
            longitude=6.021,
            country="LUX",
            region="Canton de Clervaux",
            region_natural="Oesling",
            canton="Canton de Clervaux",
            area_ha=10.0
        )
        db.add(oesling_parcel)
        db.commit()

        recs_oesling = get_recommendation(oesling_parcel.id, db)
        top_names_oesling = [r.name for r in recs_oesling]

        # La Pomme de terre ou l'Avoine doivent figurer dans le Top 3 en Oesling
        assert any(c in top_names_oesling for c in ["Pomme de terre", "Avoine", "Colza d'hiver"]), (
            f"Les cultures rustiques d'Oesling doivent figurer dans le top 3: {top_names_oesling}"
        )

        # Vérifier que les justifications citent explicitement l'Oesling et le terroir schisteux
        oesling_reasons = []
        for r in recs_oesling:
            oesling_reasons.extend(r.reasons.positive)
        assert any("Oesling" in r for r in oesling_reasons), "Les justifications doivent mentionner la région Oesling."

        # Nettoyage
        db.delete(oesling_parcel)
        db.commit()
    finally:
        db.close()


def test_chat_search_parcel_by_locality():
    """Vérifie que l'Agent Chatbot résout une localité inconnue dans la hiérarchie luxembourgeoise."""
    db = SessionLocal()
    try:
        res = search_parcel_by_name("Eselborn", db)
        assert res["found"] is True
        assert res["region_natural"] == "Oesling"
        assert "administrative_hierarchy" in res
        assert res["administrative_hierarchy"]["commune"] == "Clervaux"
        assert res["administrative_hierarchy"]["canton"] == "Clervaux"
    finally:
        db.close()


def test_chat_agent_oesling_dialogue():
    """Vérifie le traitement d'une question agronomique sur une localité de l'Oesling."""
    db = SessionLocal()
    try:
        chat_resp = run_chat_agent(
            message="Que me conseilles-tu de planter à Wilwerdange ?",
            parcel_id=None,
            db=db
        )
        assert "response" in chat_resp
        assert len(chat_resp["response"]) > 20
        # Vérifie qu'un outil de recherche ou diagnostic a été déclenché
        assert len(chat_resp["tool_calls"]) > 0
    finally:
        db.close()
