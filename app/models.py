import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, Numeric, Float, Integer, Boolean,
    DateTime, Date, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from app.db import Base
from app.config import settings

def generate_uuid():
    return str(uuid.uuid4())

IdColumn = lambda: Column(String(36), primary_key=True, default=generate_uuid)

# =====================================================================
# V1 Core Tables
# =====================================================================

class User(Base):
    __tablename__ = "users"

    id = IdColumn()
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(Text, nullable=False)
    role = Column(String(50), nullable=False, default="farmer") # 'farmer', 'government', 'ngo'
    language = Column(String(10), default="fr")
    created_at = Column(DateTime, default=datetime.utcnow)

    parcels = relationship("Parcel", back_populates="user", cascade="all, delete-orphan")


class Parcel(Base):
    __tablename__ = "parcels"

    id = IdColumn()
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    name = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    country = Column(String(10), nullable=True) # LUX, MDG
    region = Column(String(100), nullable=True)
    region_natural = Column(String(100), nullable=True) # Oesling, Gutland, Diana
    canton = Column(String(100), nullable=True) # Canton Clervaux, Canton Esch-sur-Alzette, etc.
    area_ha = Column(Numeric(10, 2), nullable=True, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="parcels")
    photos = relationship("ParcelPhoto", back_populates="parcel", cascade="all, delete-orphan")
    observations = relationship("Observation", back_populates="parcel", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="parcel", cascade="all, delete-orphan")
    soil_profiles = relationship("SoilProfile", back_populates="parcel", cascade="all, delete-orphan")
    crop_histories = relationship("CropHistory", back_populates="parcel", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="parcel", cascade="all, delete-orphan")
    disease_risks = relationship("DiseaseRisk", back_populates="parcel", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="parcel", cascade="all, delete-orphan")
    passports = relationship("ResiliencePassport", back_populates="parcel", cascade="all, delete-orphan")


class ParcelPhoto(Base):
    __tablename__ = "parcel_photos"

    id = IdColumn()
    parcel_id = Column(String(36), ForeignKey("parcels.id"), nullable=False)
    path = Column(Text, nullable=False)
    taken_at = Column(DateTime, default=datetime.utcnow)
    size_bytes = Column(Integer, nullable=True)
    consent_given = Column(Boolean, default=False) # RGPD
    delete_after = Column(DateTime, nullable=True) # Rétention 24 mois

    parcel = relationship("Parcel", back_populates="photos")


class Observation(Base):
    __tablename__ = "observations"

    id = IdColumn()
    parcel_id = Column(String(36), ForeignKey("parcels.id"), nullable=True)
    variable = Column(String(100), nullable=False) # rain, temp, soil_moisture, ndvi, soc, ph...
    date = Column(Date, nullable=True)
    value = Column(Float, nullable=False)
    source = Column(String(100), nullable=True) # nasa_power, soilgrids
    resolution_km = Column(Float, nullable=True)

    parcel = relationship("Parcel", back_populates="observations")


class Event(Base):
    __tablename__ = "events"

    id = IdColumn()
    parcel_id = Column(String(36), ForeignKey("parcels.id"), nullable=False)
    type = Column(String(100), nullable=False) # drought, cyclone, flood
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    source = Column(String(100), nullable=True) # nasa_power, ibtracs
    confidence = Column(Float, nullable=True, default=0.90)

    parcel = relationship("Parcel", back_populates="events")


class SoilProfile(Base):
    __tablename__ = "soil_profiles"

    id = IdColumn()
    parcel_id = Column(String(36), ForeignKey("parcels.id"), nullable=False)
    depth_cm = Column(String(50), nullable=False) # '0-5', '5-15', '15-30'
    soc = Column(Float, nullable=True) # Soil Organic Carbon (g/kg)
    nitrogen = Column(Float, nullable=True) # Total Nitrogen (g/kg)
    cec = Column(Float, nullable=True) # Cation Exchange Capacity (cmol/kg)
    ph = Column(Float, nullable=True) # pH H2O
    clay = Column(Float, nullable=True)
    sand = Column(Float, nullable=True)
    silt = Column(Float, nullable=True)
    wrb_class = Column(String(100), nullable=True)
    richness_index = Column(Float, nullable=True) # 0-100
    source = Column(String(100), default="soilgrids")
    uncertainty = Column(Float, nullable=True)

    parcel = relationship("Parcel", back_populates="soil_profiles")


class Plant(Base):
    __tablename__ = "plants"

    id = IdColumn()
    name_fr = Column(String(255), nullable=False)
    name_en = Column(String(255), nullable=True)
    scientific_name = Column(String(255), nullable=True)
    family = Column(String(100), nullable=True)
    type = Column(String(50), nullable=True) # cereal, legume, tree, tuber...
    temp_min = Column(Float, nullable=True)
    temp_max = Column(Float, nullable=True)
    rain_min = Column(Float, nullable=True)
    rain_max = Column(Float, nullable=True)
    ph_min = Column(Float, nullable=True)
    ph_max = Column(Float, nullable=True)
    source = Column(String(100), default="FAO ECOCROP")

    countries = relationship("PlantCountry", back_populates="plant", cascade="all, delete-orphan")


class PlantCountry(Base):
    __tablename__ = "plant_countries"

    plant_id = Column(String(36), ForeignKey("plants.id"), primary_key=True)
    country_code = Column(String(10), primary_key=True) # MDG, LUX
    status = Column(String(50), default="cultivated") # cultivated, native, introduced

    plant = relationship("Plant", back_populates="countries")


class CropHistory(Base):
    __tablename__ = "crop_history"

    id = IdColumn()
    parcel_id = Column(String(36), ForeignKey("parcels.id"), nullable=False)
    plant_id = Column(String(36), ForeignKey("plants.id"), nullable=False)
    season = Column(String(50), nullable=True)
    year = Column(Integer, nullable=False)
    source = Column(String(100), default="farmer_declaration")

    parcel = relationship("Parcel", back_populates="crop_histories")
    plant = relationship("Plant")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = IdColumn()
    parcel_id = Column(String(36), ForeignKey("parcels.id"), nullable=False)
    plant_id = Column(String(36), ForeignKey("plants.id"), nullable=False)
    score = Column(Float, nullable=False)
    reasons = Column(JSON, nullable=False) # {positive:[], negative:[], rotation:str}
    created_at = Column(DateTime, default=datetime.utcnow)
    engine_version = Column(String(50), default="rules-v2")

    parcel = relationship("Parcel", back_populates="recommendations")
    plant = relationship("Plant")


class Disease(Base):
    __tablename__ = "diseases"

    id = IdColumn()
    name = Column(String(255), nullable=False)
    plant_family = Column(String(100), nullable=True)
    favorable_humidity_min = Column(Float, nullable=True)
    favorable_temp_min = Column(Float, nullable=True)
    favorable_temp_max = Column(Float, nullable=True)
    source = Column(String(100), default="EPPO / CABI")


class DiseaseRisk(Base):
    __tablename__ = "disease_risks"

    id = IdColumn()
    parcel_id = Column(String(36), ForeignKey("parcels.id"), nullable=False)
    disease_id = Column(String(36), ForeignKey("diseases.id"), nullable=False)
    risk_level = Column(String(50), nullable=False) # low, medium, high
    confidence = Column(Float, default=0.85)
    created_at = Column(DateTime, default=datetime.utcnow)

    parcel = relationship("Parcel", back_populates="disease_risks")
    disease = relationship("Disease")


class Alert(Base):
    __tablename__ = "alerts"

    id = IdColumn()
    parcel_id = Column(String(36), ForeignKey("parcels.id"), nullable=False)
    type = Column(String(100), nullable=False) # weather, disease, soil
    severity = Column(String(50), nullable=False) # warning, info, critical
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    read = Column(Boolean, default=False)

    parcel = relationship("Parcel", back_populates="alerts")


class ReforestationZone(Base):
    __tablename__ = "reforestation_zones"

    id = IdColumn()
    name = Column(String(255), nullable=True)
    risk_type = Column(String(100), nullable=True)
    polygon_geojson = Column(JSON, nullable=True)
    species_proposed = Column(JSON, nullable=True)
    area_ha = Column(Float, nullable=True)

# =====================================================================
# V2 Tables: Fiabilité, Chatbot V2, I1, I2, I3, RGPD
# =====================================================================

class GroundTruth(Base):
    """Vérité terrain pour le backtesting (Prompt 8)."""
    __tablename__ = "ground_truth"

    id = IdColumn()
    parcel_id = Column(String(36), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    country = Column(String(10), nullable=False)
    region = Column(String(100), nullable=True)
    actual_crop_id = Column(String(36), ForeignKey("plants.id"), nullable=False)
    season = Column(String(50), nullable=True)
    year = Column(Integer, nullable=True)
    source = Column(String(100), default="field_survey") # 'field_survey', 'faostat', 'cooperative'
    confidence = Column(Float, default=1.0)

    actual_crop = relationship("Plant")


class BacktestRun(Base):
    """Rapports d'évaluation du backtesting (Prompt 8)."""
    __tablename__ = "backtest_runs"

    id = IdColumn()
    run_at = Column(DateTime, default=datetime.utcnow)
    engine_version = Column(String(50), default="rules-v2")
    n_parcels = Column(Integer, nullable=False)
    top1_accuracy = Column(Float, nullable=False)
    top3_accuracy = Column(Float, nullable=False)
    mrr = Column(Float, nullable=False) # Mean Reciprocal Rank
    report_path = Column(Text, nullable=True)
    metrics_breakdown = Column(JSON, nullable=True)


class ChatSession(Base):
    """Sessions de conversation chatbot avec mémoire (Prompt 7)."""
    __tablename__ = "chat_sessions"

    id = IdColumn()
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    parcel_id = Column(String(36), ForeignKey("parcels.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")


class ChatMessage(Base):
    """Messages avec rôle, contenu et appels d'outils (Prompt 7)."""
    __tablename__ = "chat_messages"

    id = IdColumn()
    session_id = Column(String(36), ForeignKey("chat_sessions.id"), nullable=False)
    role = Column(String(20), nullable=False) # 'user', 'assistant', 'tool'
    content = Column(Text, nullable=False)
    tool_calls = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages")
    feedbacks = relationship("ChatFeedback", back_populates="message", cascade="all, delete-orphan")


class ChatFeedback(Base):
    """Évaluation utilisateur (thumbs up / thumbs down + commentaire) (Prompt 7)."""
    __tablename__ = "chat_feedback"

    id = IdColumn()
    message_id = Column(String(36), ForeignKey("chat_messages.id"), nullable=False)
    rating = Column(Integer, nullable=False) # 1 (up) or -1 (down)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    message = relationship("ChatMessage", back_populates="feedbacks")


class LLMAudit(Base):
    """Logs d'auditabilité souveraine des inférences LLM (Prompt 12)."""
    __tablename__ = "llm_audit"

    id = IdColumn()
    session_id = Column(String(36), nullable=True)
    prompt_hash = Column(String(64), nullable=False)
    tools_called = Column(JSON, nullable=True)
    response_hash = Column(String(64), nullable=False)
    model_name = Column(String(100), default="qwen2.5:7b-local")
    latency_ms = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class ResiliencePassport(Base):
    """Innovation I1 : Passeport de Résilience certifié bancable (Prompt 9)."""
    __tablename__ = "resilience_passports"

    id = IdColumn()
    parcel_id = Column(String(36), ForeignKey("parcels.id"), nullable=False)
    issued_at = Column(DateTime, default=datetime.utcnow)
    valid_until = Column(DateTime, nullable=False)
    richness_index = Column(Float, nullable=False)
    climate_resilience_score = Column(Float, nullable=False)
    water_stress_risk = Column(Float, nullable=False)
    disease_risk_score = Column(Float, nullable=False)
    global_score = Column(Float, nullable=False) # 0.35 richness + 0.30 climate + 0.20 water + 0.15 (100-disease)
    pdf_path = Column(Text, nullable=True)
    qr_code_url = Column(Text, nullable=True)
    content_hash = Column(String(64), nullable=False) # SHA-256
    engine_version = Column(String(50), default="rules-v2")
    data_sources = Column(JSON, nullable=True)

    parcel = relationship("Parcel", back_populates="passports")


class RuptureZone(Base):
    """Innovation I2 : Jumeau de Rupture et propagation de stress (Prompt 10)."""
    __tablename__ = "rupture_zones"

    id = IdColumn()
    region = Column(String(100), nullable=False)
    country = Column(String(10), nullable=False)
    polygon_geojson = Column(JSON, nullable=True)
    stress_type = Column(String(50), nullable=False) # drought, cyclone, flood
    vulnerability_score = Column(Float, nullable=False)
    propagation_risk = Column(JSON, nullable=True)
    computed_at = Column(DateTime, default=datetime.utcnow)


class FederatedRound(Base):
    """Innovation I3 : Apprentissage fédéré souverain (Prompt 11)."""
    __tablename__ = "federated_rounds"

    id = IdColumn()
    node_id = Column(String(100), nullable=False) # 'luxembourg', 'madagascar_diana'
    round_number = Column(Integer, nullable=False)
    model_version = Column(String(50), nullable=False)
    n_samples = Column(Integer, nullable=False)
    metrics = Column(JSON, nullable=False)
    gradient_hash = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# =====================================================================
# Luxembourg Administrative Geography (SIG & Territoire)
# =====================================================================

class Region(Base):
    """Région naturelle (Oesling, Gutland)"""
    __tablename__ = "regions"

    id = IdColumn()
    name = Column(String(100), unique=True, nullable=False, index=True)

    cantons = relationship("Canton", back_populates="region", cascade="all, delete-orphan")


class Canton(Base):
    """Canton administratif du Luxembourg (12 cantons)"""
    __tablename__ = "cantons"

    id = IdColumn()
    name = Column(String(100), nullable=False, index=True)
    region_id = Column(String(36), ForeignKey("regions.id"), nullable=False)

    region = relationship("Region", back_populates="cantons")
    communes = relationship("Commune", back_populates="canton", cascade="all, delete-orphan")


class Commune(Base):
    """Commune administrative avec statut de Ville (is_city)"""
    __tablename__ = "communes"

    id = IdColumn()
    name = Column(String(100), nullable=False, index=True)
    canton_id = Column(String(36), ForeignKey("cantons.id"), nullable=False)
    is_city = Column(Boolean, default=False, nullable=False)

    canton = relationship("Canton", back_populates="communes")
    localities = relationship("Locality", back_populates="commune", cascade="all, delete-orphan")


class Locality(Base):
    """Localité ou village rattaché à une commune avec géolocalisation"""
    __tablename__ = "localities"

    id = IdColumn()
    name = Column(String(100), nullable=False, index=True)
    commune_id = Column(String(36), ForeignKey("communes.id"), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    commune = relationship("Commune", back_populates="localities")
