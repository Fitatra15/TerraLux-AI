"""
TerraLux AI — Module de Géographie Administrative et SIG du Luxembourg (luxembourg_geo.py)
Hiérarchie territoriale complète :
1. Régions naturelles (Oesling, Gutland)
2. 12 Cantons administratifs
3. Communes avec flag is_city pour les 12 villes officielles
4. Localités et villages rattachés avec coordonnées GPS (lat, lon)
"""
import re
import logging
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from app.models import Region, Canton, Commune, Locality, Parcel

logger = logging.getLogger("terralux.lux_geo")

# =============================================================================
# RÉFÉRENTIEL OFFICIEL SIG DU LUXEMBOURG
# =============================================================================
LUX_REGIONS = [
    {
        "name": "Oesling",
        "alt_names": ["Éislek", "Eislek", "Oesling", "Nord"],
        "description": "Plateau ardennais septentrional (altitudes 400-560m). Climat plus frais et rude, gelées tardives. Sols schisto-quartziteux bruns acides (Cambisols dystriques, Leptosols).",
        "temp_offset_c": -1.8, # Climat plus frais par rapport à la plaine
        "rain_offset_mm": 120.0, # Pluies plus abondantes sur le relief
        "typical_ph": 5.9,
        "soil_type": "Sols schisteux et quartziteux ardennais (Cambisols dystriques)"
    },
    {
        "name": "Gutland",
        "alt_names": ["Bon Pays", "Gutland", "Centre", "Sud"],
        "description": "Région centre et sud (altitudes 130-350m). Climat tempéré et doux, vallées fluviales (Moselle). Sols marno-calcaires, limoneux et alluviaux profonds (Cambisols calcaro-eutriques, Luvisols).",
        "temp_offset_c": 0.0,
        "rain_offset_mm": 0.0,
        "typical_ph": 6.7,
        "soil_type": "Sols marno-calcaires et alluviaux fertiles (Cambisols calcaro-eutriques / Luvisols)"
    }
]

# Les 12 Cantons rattachés à leur région naturelle
LUX_CANTONS = [
    # Oesling (Nord ardennais)
    {"name": "Clervaux", "region": "Oesling"},
    {"name": "Wiltz", "region": "Oesling"},
    {"name": "Vianden", "region": "Oesling"},

    # Gutland (Centre, Sud, Est, Ouest)
    {"name": "Diekirch", "region": "Gutland"},
    {"name": "Redange", "region": "Gutland"},
    {"name": "Echternach", "region": "Gutland"},
    {"name": "Mersch", "region": "Gutland"},
    {"name": "Grevenmacher", "region": "Gutland"},
    {"name": "Capellen", "region": "Gutland"},
    {"name": "Luxembourg", "region": "Gutland"},
    {"name": "Esch-sur-Alzette", "region": "Gutland"},
    {"name": "Remich", "region": "Gutland"},
]

# Communes et leurs localités rattachées (avec les 12 Villes officielles: is_city = True)
LUX_COMMUNES_AND_LOCALITIES = [
    # --- CANTON DE CLERVAUX (Oesling) ---
    {
        "commune": "Clervaux",
        "canton": "Clervaux",
        "is_city": False,
        "localities": [
            {"name": "Clervaux", "lat": 50.055, "lon": 6.030},
            {"name": "Eselborn", "lat": 49.996, "lon": 6.007},
            {"name": "Reuler", "lat": 50.057, "lon": 6.035},
            {"name": "Urspelt", "lat": 50.075, "lon": 6.046},
            {"name": "Munshausen", "lat": 50.033, "lon": 6.037},
            {"name": "Drauffelt", "lat": 50.016, "lon": 6.004},
            {"name": "Mecher", "lat": 50.027, "lon": 5.992},
            {"name": "Weicherdange", "lat": 50.039, "lon": 5.989}
        ]
    },
    {
        "commune": "Troisvierges",
        "canton": "Clervaux",
        "is_city": False,
        "localities": [
            {"name": "Troisvierges", "lat": 50.120, "lon": 5.990},
            {"name": "Wilwerdange", "lat": 50.138, "lon": 6.021},
            {"name": "Huldange", "lat": 50.165, "lon": 6.015},
            {"name": "Basbellain", "lat": 50.155, "lon": 5.975},
            {"name": "Hautbellain", "lat": 50.161, "lon": 5.955},
            {"name": "Drinklange", "lat": 50.141, "lon": 6.002},
            {"name": "Goedange", "lat": 50.145, "lon": 6.047}
        ]
    },
    {
        "commune": "Parc Hosingen",
        "canton": "Clervaux",
        "is_city": False,
        "localities": [
            {"name": "Hosingen", "lat": 50.012, "lon": 6.089},
            {"name": "Dorscheid", "lat": 50.028, "lon": 6.096},
            {"name": "Holzthum", "lat": 49.988, "lon": 6.067},
            {"name": "Consthum", "lat": 49.974, "lon": 6.054}
        ]
    },

    # --- CANTON DE WILTZ (Oesling) ---
    {
        "commune": "Wiltz",
        "canton": "Wiltz",
        "is_city": True, # Ville officielle 1/12
        "localities": [
            {"name": "Wiltz", "lat": 49.967, "lon": 5.933},
            {"name": "Roullingen", "lat": 49.954, "lon": 5.925},
            {"name": "Weidingen", "lat": 49.962, "lon": 5.949},
            {"name": "Eschweiler", "lat": 49.998, "lon": 5.952},
            {"name": "Erpeldange-Wiltz", "lat": 49.979, "lon": 5.932}
        ]
    },
    {
        "commune": "Lac de la Haute-Sûre",
        "canton": "Wiltz",
        "is_city": False,
        "localities": [
            {"name": "Bavigne", "lat": 49.923, "lon": 5.852},
            {"name": "Kaundorf", "lat": 49.921, "lon": 5.903},
            {"name": "Mecher-Haute-Sûre", "lat": 49.926, "lon": 5.875}
        ]
    },

    # --- CANTON DE VIANDEN (Oesling) ---
    {
        "commune": "Vianden",
        "canton": "Vianden",
        "is_city": True, # Ville officielle 2/12
        "localities": [
            {"name": "Vianden", "lat": 49.934, "lon": 6.209}
        ]
    },

    # --- CANTON DE DIEKIRCH (Gutland) ---
    {
        "commune": "Diekirch",
        "canton": "Diekirch",
        "is_city": True, # Ville officielle 3/12
        "localities": [
            {"name": "Diekirch", "lat": 49.868, "lon": 6.160}
        ]
    },
    {
        "commune": "Ettelbruck",
        "canton": "Diekirch",
        "is_city": True, # Ville officielle 4/12
        "localities": [
            {"name": "Ettelbruck", "lat": 49.847, "lon": 6.104},
            {"name": "Warken", "lat": 49.858, "lon": 6.096}
        ]
    },

    # --- CANTON D'ECHTERNACH (Gutland) ---
    {
        "commune": "Echternach",
        "canton": "Echternach",
        "is_city": True, # Ville officielle 5/12
        "localities": [
            {"name": "Echternach", "lat": 49.812, "lon": 6.421}
        ]
    },

    # --- CANTON DE GREVENMACHER (Gutland) ---
    {
        "commune": "Grevenmacher",
        "canton": "Grevenmacher",
        "is_city": True, # Ville officielle 6/12
        "localities": [
            {"name": "Grevenmacher", "lat": 49.681, "lon": 6.441}
        ]
    },

    # --- CANTON DE REMICH (Gutland) ---
    {
        "commune": "Remich",
        "canton": "Remich",
        "is_city": True, # Ville officielle 7/12
        "localities": [
            {"name": "Remich", "lat": 49.544, "lon": 6.368}
        ]
    },
    {
        "commune": "Mondorf-les-Bains",
        "canton": "Remich",
        "is_city": False,
        "localities": [
            {"name": "Mondorf-les-Bains", "lat": 49.505, "lon": 6.281},
            {"name": "Altwies", "lat": 49.511, "lon": 6.257}
        ]
    },

    # --- CANTON DE LUXEMBOURG (Gutland) ---
    {
        "commune": "Luxembourg",
        "canton": "Luxembourg",
        "is_city": True, # Ville officielle 8/12 (Capitale)
        "localities": [
            {"name": "Luxembourg-ville", "lat": 49.611, "lon": 6.131},
            {"name": "Kirchberg", "lat": 49.627, "lon": 6.160},
            {"name": "Limpertsberg", "lat": 49.621, "lon": 6.121},
            {"name": "Gasperich", "lat": 49.589, "lon": 6.121},
            {"name": "Bonnevoie", "lat": 49.599, "lon": 6.141},
            {"name": "Cents", "lat": 49.619, "lon": 6.164},
            {"name": "Clausen", "lat": 49.614, "lon": 6.142},
            {"name": "Grund", "lat": 49.610, "lon": 6.134},
            {"name": "Pfaffenthal", "lat": 49.617, "lon": 6.133},
            {"name": "Beggen", "lat": 49.643, "lon": 6.133},
            {"name": "Hamm", "lat": 49.611, "lon": 6.168},
            {"name": "Merl", "lat": 49.602, "lon": 6.101},
            {"name": "Belair", "lat": 49.612, "lon": 6.110},
            {"name": "Hollerich", "lat": 49.599, "lon": 6.119}
        ]
    },
    {
        "commune": "Hesperange",
        "canton": "Luxembourg",
        "is_city": False,
        "localities": [
            {"name": "Hesperange", "lat": 49.573, "lon": 6.152},
            {"name": "Alzingen", "lat": 49.568, "lon": 6.162},
            {"name": "Fentange", "lat": 49.564, "lon": 6.144}
        ]
    },
    {
        "commune": "Strassen",
        "canton": "Luxembourg",
        "is_city": False,
        "localities": [
            {"name": "Strassen", "lat": 49.620, "lon": 6.073}
        ]
    },

    # --- CANTON D'ESCH-SUR-ALZETTE (Gutland) ---
    {
        "commune": "Esch-sur-Alzette",
        "canton": "Esch-sur-Alzette",
        "is_city": True, # Ville officielle 9/12
        "localities": [
            {"name": "Esch-sur-Alzette", "lat": 49.497, "lon": 5.981},
            {"name": "Belval", "lat": 49.502, "lon": 5.928},
            {"name": "Lallange", "lat": 49.510, "lon": 5.990},
            {"name": "Sommet", "lat": 49.490, "lon": 5.980}
        ]
    },
    {
        "commune": "Differdange",
        "canton": "Esch-sur-Alzette",
        "is_city": True, # Ville officielle 10/12
        "localities": [
            {"name": "Differdange", "lat": 49.524, "lon": 5.891},
            {"name": "Niederkorn", "lat": 49.537, "lon": 5.892},
            {"name": "Oberkorn", "lat": 49.514, "lon": 5.894},
            {"name": "Lasauvage", "lat": 49.513, "lon": 5.845}
        ]
    },
    {
        "commune": "Dudelange",
        "canton": "Esch-sur-Alzette",
        "is_city": True, # Ville officielle 11/12
        "localities": [
            {"name": "Dudelange", "lat": 49.481, "lon": 6.084},
            {"name": "Burange", "lat": 49.492, "lon": 6.083}
        ]
    },
    {
        "commune": "Rumelange",
        "canton": "Esch-sur-Alzette",
        "is_city": True, # Ville officielle 12/12
        "localities": [
            {"name": "Rumelange", "lat": 49.460, "lon": 6.031}
        ]
    },
    {
        "commune": "Bettembourg",
        "canton": "Esch-sur-Alzette",
        "is_city": False,
        "localities": [
            {"name": "Bettembourg", "lat": 49.518, "lon": 6.103},
            {"name": "Noertzange", "lat": 49.511, "lon": 6.059}
        ]
    },
    {
        "commune": "Sanem",
        "canton": "Esch-sur-Alzette",
        "is_city": False,
        "localities": [
            {"name": "Sanem", "lat": 49.548, "lon": 5.930},
            {"name": "Belvaux", "lat": 49.511, "lon": 5.928},
            {"name": "Soleuvre", "lat": 49.525, "lon": 5.941}
        ]
    },
    {
        "commune": "Pétange",
        "canton": "Esch-sur-Alzette",
        "is_city": False,
        "localities": [
            {"name": "Pétange", "lat": 49.556, "lon": 5.875},
            {"name": "Rodange", "lat": 49.546, "lon": 5.841}
        ]
    },

    # --- CANTON DE CAPELLEN (Gutland) ---
    {
        "commune": "Mamer",
        "canton": "Capellen",
        "is_city": False,
        "localities": [
            {"name": "Mamer", "lat": 49.627, "lon": 6.024},
            {"name": "Capellen", "lat": 49.645, "lon": 5.990}
        ]
    },
    {
        "commune": "Steinfort",
        "canton": "Capellen",
        "is_city": False,
        "localities": [
            {"name": "Steinfort", "lat": 49.661, "lon": 5.914}
        ]
    },

    # --- CANTON DE MERSCH (Gutland) ---
    {
        "commune": "Mersch",
        "canton": "Mersch",
        "is_city": False,
        "localities": [
            {"name": "Mersch", "lat": 49.749, "lon": 6.106},
            {"name": "Rollingen", "lat": 49.739, "lon": 6.113},
            {"name": "Beringen", "lat": 49.757, "lon": 6.118}
        ]
    },

    # --- CANTON DE REDANGE (Gutland) ---
    {
        "commune": "Redange-sur-Attert",
        "canton": "Redange",
        "is_city": False,
        "localities": [
            {"name": "Redange-sur-Attert", "lat": 49.765, "lon": 5.890}
        ]
    }
]

# Table de correspondance rapide en mémoire (nom en minuscule -> région naturelle)
_CITY_TO_REGION_CACHE = {}

def _init_memory_cache():
    global _CITY_TO_REGION_CACHE
    if _CITY_TO_REGION_CACHE:
        return

    # Cantons
    canton_to_region = {c["name"].lower(): c["region"] for c in LUX_CANTONS}

    # Pour chaque commune et localité
    for item in LUX_COMMUNES_AND_LOCALITIES:
        commune_name = item["commune"].lower()
        canton_name = item["canton"].lower()
        region_natural = canton_to_region.get(canton_name, "Gutland")

        _CITY_TO_REGION_CACHE[commune_name] = region_natural
        _CITY_TO_REGION_CACHE[f"commune de {commune_name}"] = region_natural
        _CITY_TO_REGION_CACHE[f"commune d'{commune_name}"] = region_natural

        for loc in item["localities"]:
            loc_name = loc["name"].lower()
            _CITY_TO_REGION_CACHE[loc_name] = region_natural

    # Cantons mapping
    for c in LUX_CANTONS:
        _CITY_TO_REGION_CACHE[c["name"].lower()] = c["region"]
        _CITY_TO_REGION_CACHE[f"canton de {c['name'].lower()}"] = c["region"]
        _CITY_TO_REGION_CACHE[f"canton d'{c['name'].lower()}"] = c["region"]

    # Alias fréquents
    _CITY_TO_REGION_CACHE["esch"] = "Gutland"
    _CITY_TO_REGION_CACHE["esch-sur-alzette"] = "Gutland"
    _CITY_TO_REGION_CACHE["esch/alzette"] = "Gutland"
    _CITY_TO_REGION_CACHE["luxembourg"] = "Gutland"
    _CITY_TO_REGION_CACHE["luxembourg-ville"] = "Gutland"
    _CITY_TO_REGION_CACHE["kirchberg"] = "Gutland"
    _CITY_TO_REGION_CACHE["belval"] = "Gutland"
    _CITY_TO_REGION_CACHE["clervaux"] = "Oesling"
    _CITY_TO_REGION_CACHE["wilwerdange"] = "Oesling"
    _CITY_TO_REGION_CACHE["eselborn"] = "Oesling"
    _CITY_TO_REGION_CACHE["urspelt"] = "Oesling"
    _CITY_TO_REGION_CACHE["reuler"] = "Oesling"
    _CITY_TO_REGION_CACHE["troisvierges"] = "Oesling"
    _CITY_TO_REGION_CACHE["wiltz"] = "Oesling"
    _CITY_TO_REGION_CACHE["vianden"] = "Oesling"
    _CITY_TO_REGION_CACHE["hosingen"] = "Oesling"

_init_memory_cache()


# =============================================================================
# FONCTIONS UTILITAIRES PUBLIQUES
# =============================================================================

def get_region_from_city(city_or_locality: str) -> Optional[str]:
    """
    Détermine la région naturelle (Oesling ou Gutland) à partir du nom d'une ville,
    commune, localité ou canton du Luxembourg.
    Exemple obligatoire : assert get_region_from_city("Esch-sur-Alzette") == "Gutland"
    """
    if not city_or_locality:
        return None

    clean = city_or_locality.strip().lower()
    _init_memory_cache()

    # 1. Correspondance exacte dans le cache
    if clean in _CITY_TO_REGION_CACHE:
        return _CITY_TO_REGION_CACHE[clean]

    # 2. Correspondance sous-chaîne
    for key, reg in _CITY_TO_REGION_CACHE.items():
        if key in clean or clean in key:
            return reg

    # 3. Mots clés géographiques spécifiques
    if any(k in clean for k in ["clervaux", "wiltz", "vianden", "troisvierges", "wilwerdange", "eselborn", "hosingen", "huldange", "eislek", "oesling"]):
        return "Oesling"
    if any(k in clean for k in ["esch", "luxembourg", "dudelange", "differdange", "ettelbruck", "diekirch", "remich", "grevenmacher", "echternach", "rumelange", "mersch", "capellen", "gutland"]):
        return "Gutland"

    return "Gutland" # Région majoritaire par défaut


def get_luxembourg_hierarchy(query: str, db: Optional[Session] = None) -> Optional[Dict[str, Any]]:
    """
    Renvoie la hiérarchie administrative et agronomique complète pour une localité/commune.
    Exemple: Wilwerdange -> Commune Troisvierges, Canton Clervaux, Région Oesling.
    """
    clean_q = query.strip().lower() if query else ""

    # Recherche directe en base de données si session DB disponible
    if db:
        loc = db.query(Locality).filter(Locality.name.ilike(f"%{clean_q}%")).first()
        if loc and loc.commune:
            comm = loc.commune
            cant = comm.canton
            reg = cant.region if cant else None
            return {
                "locality": loc.name,
                "commune": comm.name,
                "canton": cant.name if cant else "Clervaux",
                "region_natural": reg.name if reg else "Oesling",
                "is_city": comm.is_city,
                "latitude": loc.latitude,
                "longitude": loc.longitude,
                "soil_type": "Sols schisteux et quartziteux (Oesling)" if (reg and reg.name == "Oesling") else "Sols marno-calcaires profonds (Gutland)",
                "climate_note": "Climat ardennais frais" if (reg and reg.name == "Oesling") else "Climat tempéré de plaine"
            }

    # Fallback in-memory
    for item in LUX_COMMUNES_AND_LOCALITIES:
        c_name = item["commune"]
        cant_name = item["canton"]
        reg_name = get_region_from_city(cant_name) or "Gutland"
        for l in item["localities"]:
            if l["name"].lower() in clean_q or clean_q in l["name"].lower():
                return {
                    "locality": l["name"],
                    "commune": c_name,
                    "canton": cant_name,
                    "region_natural": reg_name,
                    "is_city": item["is_city"],
                    "latitude": l["lat"],
                    "longitude": l["lon"],
                    "soil_type": "Sols schisteux et quartziteux (Oesling)" if reg_name == "Oesling" else "Sols marno-calcaires profonds (Gutland)",
                    "climate_note": "Climat ardennais frais" if reg_name == "Oesling" else "Climat tempéré de plaine"
                }

    # Si la recherche est sur le nom de commune
    for item in LUX_COMMUNES_AND_LOCALITIES:
        if item["commune"].lower() in clean_q:
            cant_name = item["canton"]
            reg_name = get_region_from_city(cant_name) or "Gutland"
            main_loc = item["localities"][0]
            return {
                "locality": main_loc["name"],
                "commune": item["commune"],
                "canton": cant_name,
                "region_natural": reg_name,
                "is_city": item["is_city"],
                "latitude": main_loc["lat"],
                "longitude": main_loc["lon"],
                "soil_type": "Sols schisteux et quartziteux (Oesling)" if reg_name == "Oesling" else "Sols marno-calcaires profonds (Gutland)",
                "climate_note": "Climat ardennais frais" if reg_name == "Oesling" else "Climat tempéré de plaine"
            }

    return None


def seed_luxembourg_geography(db: Session):
    """
    Peuple les tables PostGIS : regions, cantons, communes, localities.
    Met également à jour les parcelles existantes au Luxembourg avec region_natural et canton.
    Idempotent : ne duplique pas si déjà existant.
    """
    logger.info("Ensemencement de la géographie administrative du Luxembourg...")

    # 1. Régions
    region_objs = {}
    for r_data in LUX_REGIONS:
        reg = db.query(Region).filter(Region.name == r_data["name"]).first()
        if not reg:
            reg = Region(name=r_data["name"])
            db.add(reg)
            db.flush()
        region_objs[r_data["name"]] = reg

    # 2. Cantons
    canton_objs = {}
    for c_data in LUX_CANTONS:
        cant = db.query(Canton).filter(Canton.name == c_data["name"]).first()
        reg_parent = region_objs.get(c_data["region"])
        if not cant and reg_parent:
            cant = Canton(name=c_data["name"], region_id=reg_parent.id)
            db.add(cant)
            db.flush()
        canton_objs[c_data["name"]] = cant

    # 3. Communes et Localités
    for comm_data in LUX_COMMUNES_AND_LOCALITIES:
        cant_parent = canton_objs.get(comm_data["canton"])
        if not cant_parent:
            continue

        comm = db.query(Commune).filter(
            Commune.name == comm_data["commune"],
            Commune.canton_id == cant_parent.id
        ).first()

        if not comm:
            comm = Commune(
                name=comm_data["commune"],
                canton_id=cant_parent.id,
                is_city=comm_data["is_city"]
            )
            db.add(comm)
            db.flush()

        for loc_data in comm_data["localities"]:
            loc = db.query(Locality).filter(
                Locality.name == loc_data["name"],
                Locality.commune_id == comm.id
            ).first()

            if not loc:
                loc = Locality(
                    name=loc_data["name"],
                    commune_id=comm.id,
                    latitude=loc_data["lat"],
                    longitude=loc_data["lon"]
                )
                db.add(loc)

    db.commit()

    # 4. Mise à jour des parcelles existantes avec canton et region_natural
    lux_parcels = db.query(Parcel).filter(Parcel.country == "LUX").all()
    for p in lux_parcels:
        reg_nat = get_region_from_city(p.name or "") or ("Oesling" if p.latitude > 49.90 else "Gutland")
        cant_name = "Canton de Clervaux" if reg_nat == "Oesling" else ("Canton d'Esch-sur-Alzette" if p.latitude < 49.55 else "Canton de Luxembourg")
        
        if "esch" in (p.name or "").lower():
            cant_name = "Canton d'Esch-sur-Alzette"
            reg_nat = "Gutland"
        elif "luxembourg" in (p.name or "").lower():
            cant_name = "Canton de Luxembourg"
            reg_nat = "Gutland"

        p.region_natural = reg_nat
        p.canton = cant_name

    db.commit()
    logger.info("Géographie administrative du Luxembourg ensemencée avec succès.")
