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

from app.all_geo_data import (
    GEO_REGIONS,
    GEO_CANTONS,
    GEO_COMMUNES_AND_LOCALITIES
)

# Rétrocompatibilité pour les imports existants
LUX_REGIONS = GEO_REGIONS
LUX_CANTONS = GEO_CANTONS
LUX_COMMUNES_AND_LOCALITIES = GEO_COMMUNES_AND_LOCALITIES

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
    Renvoie la hiérarchie administrative et agronomique complète pour une localité/commune STRICTEMENT luxembourgeoise.
    Exemple: Wilwerdange -> Commune Troisvierges, Canton Clervaux, Région Oesling.
    Ne renvoie JAMAIS de localités malgaches.
    """
    clean_q = query.strip().lower() if query else ""
    if not clean_q:
        return None

    # Recherche directe en base de données restreinte à LUXEMBOURG (country == 'LUX')
    if db:
        loc = (
            db.query(Locality)
            .join(Commune)
            .join(Canton)
            .join(Region)
            .filter(
                Region.country == "LUX",
                Locality.name.ilike(f"%{clean_q}%")
            )
            .first()
        )
        if loc and loc.commune:
            comm = loc.commune
            cant = comm.canton
            reg = cant.region if cant else None
            return {
                "locality": loc.name,
                "commune": comm.name,
                "canton": cant.name if cant else "Clervaux",
                "region_natural": reg.name if reg else "Oesling",
                "country": "LUX",
                "is_city": comm.is_city,
                "latitude": loc.latitude,
                "longitude": loc.longitude,
                "soil_type": "Cambisol calcaro-eutrique" if (reg and reg.name == "Gutland") else "Cambisol squelettique schisteux (Oesling)",
                "climate_note": "Climat ardennais frais" if (reg and reg.name == "Oesling") else "Climat tempéré de plaine"
            }

    # Fallback in-memory STRICTEMENT pour le Luxembourg
    lux_canton_names = {c["name"] for c in GEO_CANTONS if c.get("country") == "LUX"}
    for item in LUX_COMMUNES_AND_LOCALITIES:
        if item.get("canton") not in lux_canton_names:
            continue
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
                    "country": "LUX",
                    "is_city": item.get("is_city", False),
                    "latitude": l["lat"],
                    "longitude": l["lon"],
                    "soil_type": "Cambisol calcaro-eutrique" if reg_name == "Gutland" else "Cambisol squelettique schisteux (Oesling)",
                    "climate_note": "Climat ardennais frais" if reg_name == "Oesling" else "Climat tempéré de plaine"
                }

    for item in LUX_COMMUNES_AND_LOCALITIES:
        if item.get("canton") not in lux_canton_names:
            continue
        if item["commune"].lower() in clean_q:
            cant_name = item["canton"]
            reg_name = get_region_from_city(cant_name) or "Gutland"
            main_loc = item["localities"][0]
            return {
                "locality": main_loc["name"],
                "commune": item["commune"],
                "canton": cant_name,
                "region_natural": reg_name,
                "country": "LUX",
                "is_city": item.get("is_city", False),
                "latitude": main_loc["lat"],
                "longitude": main_loc["lon"],
                "soil_type": "Cambisol calcaro-eutrique" if reg_name == "Gutland" else "Cambisol squelettique schisteux (Oesling)",
                "climate_note": "Climat ardennais frais" if reg_name == "Oesling" else "Climat tempéré de plaine"
            }

    return None


def get_madagascar_hierarchy(query: str, db: Optional[Session] = None) -> Optional[Dict[str, Any]]:
    """
    Renvoie la hiérarchie administrative et agronomique complète pour une commune/localité de Madagascar (Diana).
    Exemple: Mangaoka -> District Antsiranana II, Région Diana, Sol Ferralsol.
    """
    clean_q = query.strip().lower() if query else ""
    if not clean_q:
        return None

    if db:
        loc = (
            db.query(Locality)
            .join(Commune)
            .join(Canton)
            .join(Region)
            .filter(
                Region.country == "MDG",
                Locality.name.ilike(f"%{clean_q}%")
            )
            .first()
        )
        if loc and loc.commune:
            comm = loc.commune
            cant = comm.canton
            reg = cant.region if cant else None
            return {
                "locality": loc.name,
                "commune": comm.name,
                "canton": f"District d'{cant.name}" if cant and not cant.name.startswith("District") else (cant.name if cant else "District d'Antsiranana II"),
                "district": cant.name if cant else "Antsiranana II",
                "region_natural": "Diana",
                "country": "MDG",
                "is_city": comm.is_city,
                "latitude": loc.latitude,
                "longitude": loc.longitude,
                "soil_type": "Ferralsol rhodi-lixique",
                "climate_note": "Climat tropical de mousson à saison sèche marquée"
            }

    # Fallback in-memory pour Madagascar
    mdg_canton_names = {c["name"] for c in GEO_CANTONS if c.get("country") == "MDG"}
    for item in LUX_COMMUNES_AND_LOCALITIES:
        if item.get("canton") not in mdg_canton_names:
            continue
        c_name = item["commune"]
        cant_name = item["canton"]
        for l in item["localities"]:
            if l["name"].lower() in clean_q or clean_q in l["name"].lower():
                return {
                    "locality": l["name"],
                    "commune": c_name,
                    "canton": f"District d'{cant_name}" if not cant_name.startswith("District") else cant_name,
                    "district": cant_name,
                    "region_natural": "Diana",
                    "country": "MDG",
                    "is_city": item.get("is_city", False),
                    "latitude": l["lat"],
                    "longitude": l["lon"],
                    "soil_type": "Ferralsol rhodi-lixique",
                    "climate_note": "Climat tropical chaud et humide"
                }

    return None


def get_territorial_hierarchy(query: str, lat: Optional[float] = None, lon: Optional[float] = None, db: Optional[Session] = None) -> Optional[Dict[str, Any]]:
    """
    Détermine la hiérarchie appropriée en fonction des coordonnées GPS ou de la requête textuelle.
    """
    if lat is not None:
        if lat < 0:
            return get_madagascar_hierarchy(query, db)
        elif lat > 45:
            return get_luxembourg_hierarchy(query, db)

    # Si pas de coordonnées, tester Madagascar puis Luxembourg
    mdg = get_madagascar_hierarchy(query, db)
    if mdg:
        return mdg
    return get_luxembourg_hierarchy(query, db)


def seed_luxembourg_geography(db: Session):
    """
    Peuple les tables PostGIS : regions, cantons, communes, localities
    pour le Luxembourg et Madagascar (Région Diana).
    Met également à jour les parcelles existantes avec region_natural et canton.
    Idempotent : ne duplique pas si déjà existant.
    """
    logger.info("Ensemencement de la géographie administrative (Luxembourg & Madagascar - Diana)...")

    # 1. Régions
    region_objs = {}
    for r_data in GEO_REGIONS:
        reg = db.query(Region).filter(Region.name == r_data["name"]).first()
        if not reg:
            reg = Region(name=r_data["name"], country=r_data.get("country", "LUX"))
            db.add(reg)
            db.flush()
        else:
            if not getattr(reg, "country", None):
                reg.country = r_data.get("country", "LUX")
        region_objs[r_data["name"]] = reg

    # 2. Cantons / Districts
    canton_objs = {}
    for c_data in GEO_CANTONS:
        cant = db.query(Canton).filter(Canton.name == c_data["name"]).first()
        reg_parent = region_objs.get(c_data["region"])
        c_country = c_data.get("country", "LUX")
        if not cant and reg_parent:
            cant = Canton(name=c_data["name"], region_id=reg_parent.id, country=c_country)
            db.add(cant)
            db.flush()
        elif cant and not getattr(cant, "country", None):
            cant.country = c_country
        canton_objs[c_data["name"]] = cant

    # 3. Communes et Localités
    for comm_data in GEO_COMMUNES_AND_LOCALITIES:
        cant_parent = canton_objs.get(comm_data["canton"])
        if not cant_parent:
            continue

        comm_country = comm_data.get("country", "LUX")
        comm = db.query(Commune).filter(
            Commune.name == comm_data["commune"],
            Commune.canton_id == cant_parent.id
        ).first()

        if not comm:
            comm = Commune(
                name=comm_data["commune"],
                canton_id=cant_parent.id,
                is_city=comm_data["is_city"],
                country=comm_country
            )
            db.add(comm)
            db.flush()
        else:
            if not getattr(comm, "country", None):
                comm.country = comm_country
            comm.is_city = comm_data["is_city"]

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
                    longitude=loc_data["lon"],
                    country=comm_country
                )
                db.add(loc)
            else:
                loc.latitude = loc_data["lat"]
                loc.longitude = loc_data["lon"]
                if not getattr(loc, "country", None):
                    loc.country = comm_country

    db.commit()

    # 4. Mise à jour des parcelles existantes avec canton et region_natural
    all_parcels = db.query(Parcel).all()
    for p in all_parcels:
        if p.country == "MDG":
            p.region_natural = "Diana"
            if "ambilobe" in (p.name or "").lower():
                p.canton = "District d'Ambilobe"
            elif "ambanja" in (p.name or "").lower():
                p.canton = "District d'Ambanja"
            elif "nosy be" in (p.name or "").lower() or "hell-ville" in (p.name or "").lower():
                p.canton = "District de Nosy Be"
            else:
                p.canton = "District d'Antsiranana I"
        else:
            reg_nat = get_region_from_city(p.name or "") or ("Oesling" if (p.latitude or 0) > 49.90 else "Gutland")
            cant_name = "Canton de Clervaux" if reg_nat == "Oesling" else ("Canton d'Esch-sur-Alzette" if (p.latitude or 0) < 49.55 else "Canton de Luxembourg")
            
            if "esch" in (p.name or "").lower():
                cant_name = "Canton d'Esch-sur-Alzette"
                reg_nat = "Gutland"
            elif "luxembourg" in (p.name or "").lower():
                cant_name = "Canton de Luxembourg"
                reg_nat = "Gutland"

            p.region_natural = reg_nat
            p.canton = cant_name

    db.commit()
    logger.info("Géographie administrative (Luxembourg & Madagascar - Diana) ensemencée avec succès.")


def get_all_locations_data(db: Session) -> Dict[str, Any]:
    """
    Renvoie l'arbre géographique et la liste plate pour les dropdowns du frontend.
    Endpoint: GET /api/locations
    """
    localities = db.query(Locality).join(Commune).join(Canton).join(Region).all()
    
    flat_list = []
    for loc in localities:
        comm = loc.commune
        cant = comm.canton if comm else None
        reg = cant.region if cant else None
        c_code = getattr(loc, "country", None) or (reg.country if reg else "LUX")
        
        country_label = "Luxembourg" if c_code == "LUX" else "Madagascar (Diana)"
        label = f"{loc.name} ({cant.name if cant else ''}, {reg.name if reg else ''} - {c_code})"
        if getattr(comm, "is_city", False):
            label = f"★ {label}"

        flat_list.append({
            "id": loc.id,
            "name": loc.name,
            "commune": comm.name if comm else "",
            "canton": cant.name if cant else "",
            "region": reg.name if reg else "",
            "country": c_code,
            "country_label": country_label,
            "is_city": getattr(comm, "is_city", False),
            "latitude": loc.latitude,
            "longitude": loc.longitude,
            "label": label
        })

    # Tri : Villes d'abord, puis par pays et nom alphabétique
    flat_list.sort(key=lambda x: (x["country"], not x["is_city"], x["name"]))

    # Arborescence par pays
    countries = [
        {
            "code": "LUX",
            "name": "Luxembourg",
            "regions": ["Oesling", "Gutland"]
        },
        {
            "code": "MDG",
            "name": "Madagascar (Diana)",
            "regions": ["Diana"]
        }
    ]

    return {
        "total": len(flat_list),
        "countries": countries,
        "locations": flat_list
    }
