import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, Numeric, Float, Integer, Boolean,
    DateTime, Date, ForeignKey, JSON
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from app.db import Base
from app.config import settings

def generate_uuid():
    return str(uuid.uuid4())

# Compatibility helper: uses PG_UUID if postgresql else String(36)
IdColumn = lambda: Column(String(36), primary_key=True, default=generate_uuid)

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


class ParcelPhoto(Base):
    __tablename__ = "parcel_photos"

    id = IdColumn()
    parcel_id = Column(String(36), ForeignKey("parcels.id"), nullable=False)
    path = Column(Text, nullable=False)
    taken_at = Column(DateTime, default=datetime.utcnow)
    size_bytes = Column(Integer, nullable=True)

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
    nitrogen = Column(Float, nullable=True) # Total Nitrogen (cg/kg or g/kg)
    cec = Column(Float, nullable=True) # Cation Exchange Capacity (cmol/kg)
    ph = Column(Float, nullable=True) # pH H2O
    clay = Column(Float, nullable=True) # % or g/kg
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
    engine_version = Column(String(50), default="rules-v1")

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
    risk_type = Column(String(100), nullable=True) # drought, cyclone, erosion
    polygon_geojson = Column(JSON, nullable=True) # GeoJSON polygon geometry
    species_proposed = Column(JSON, nullable=True) # List of proposed tree species
    area_ha = Column(Float, nullable=True)
