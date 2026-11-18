from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime, date

# --- Health ---
class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "1.0.0"

# --- Auth ---
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: str = Field(default="farmer", pattern="^(farmer|government|ngo)$")
    language: str = "fr"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    role: str

class UserProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    email: str
    role: str
    language: str
    created_at: Optional[datetime] = None

# --- Parcels ---
class ParcelCreate(BaseModel):
    name: Optional[str] = "Ma Parcelle"
    latitude: float
    longitude: float
    area_ha: Optional[float] = 1.0
    elevation_m: Optional[float] = 250.0
    slope_pct: Optional[float] = 2.0
    canton: Optional[str] = None
    region_natural: Optional[str] = None

class ParcelOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: Optional[str] = None
    latitude: float
    longitude: float
    country: Optional[str] = None
    region: Optional[str] = None
    canton: Optional[str] = None
    region_natural: Optional[str] = None
    area_ha: Optional[float] = 1.0
    elevation_m: Optional[float] = 250.0
    slope_pct: Optional[float] = 2.0
    created_at: Optional[datetime] = None
    soil_type: Optional[str] = None
    score: Optional[float] = None
    status: Optional[str] = "Ready"

class ParcelPhotoOut(BaseModel):
    photo_id: str
    url: str

# --- Recommendations ---
class RecommendationReason(BaseModel):
    positive: List[str] = []
    negative: List[str] = []
    rotation: Optional[str] = None

class CropRecommendationItem(BaseModel):
    plant_id: str
    name: str
    scientific_name: Optional[str] = None
    score: float
    reasons: RecommendationReason
    yield_t_ha: Optional[float] = None
    expected_yield_t: Optional[float] = None
    price_eur_t: Optional[float] = None
    gross_revenue_eur: Optional[float] = None
    gross_revenue_mga: Optional[float] = None
    input_cost_eur: Optional[float] = None
    net_margin_eur: Optional[float] = None
    market_risk: Optional[str] = "Faible" # Faible, Moyen, Élevé
    market_risk_justification: Optional[str] = None

class CropEconomicItem(BaseModel):
    crop_name: str
    scientific_name: Optional[str] = None
    area_ha: float
    yield_t_ha: float
    expected_yield_t: float
    price_eur_t: float
    gross_revenue_eur: float
    gross_revenue_mga: Optional[float] = None
    input_cost_eur_ha: float
    input_cost_total_eur: float
    net_margin_eur: float
    profitability_score: float
    market_risk: str
    market_risk_justification: str

class ParcelEconomicsResponse(BaseModel):
    parcel_id: str
    parcel_name: str
    country: str
    area_ha: float
    elevation_m: Optional[float] = None
    slope_pct: Optional[float] = None
    currency: str
    economic_items: List[CropEconomicItem]
    inflation_context: str

class RecommendationResponse(BaseModel):
    parcel_id: str
    top3: List[CropRecommendationItem]
    engine_version: str = "rules-v1"

# --- Events ---
class EventOut(BaseModel):
    id: Optional[str] = None
    type: str
    start: Optional[str] = None
    end: Optional[str] = None
    source: Optional[str] = None
    confidence: Optional[float] = 0.90

# --- Soil ---
class SoilPropertyItem(BaseModel):
    value: float
    unit: str
    depth: str
    status: str

class SoilProfileResponse(BaseModel):
    parcel_id: str
    wrb_class: str
    richness_index: float
    richness_label: str
    properties: Dict[str, SoilPropertyItem]
    deficiencies: List[str]
    interpretation: str

# --- Diseases ---
class DiseaseRiskOut(BaseModel):
    disease: str
    risk_level: str # low, medium, high
    confidence: float

# --- Diagnosis (Leaf & Multimodal Context Fusion) ---
class DiagnosisResponse(BaseModel):
    image_confidence: float
    climate_plausibility: float
    soil_plausibility: float
    contextual_confidence: float
    final_diagnosis: str
    explanation: str
    warning: Optional[str] = None
    top_3_image: Optional[List[Dict[str, Any]]] = None

# --- Chat ---
class ChatRequest(BaseModel):
    message: str
    parcel_id: Optional[str] = None
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    tool_calls: List[Dict[str, Any]] = []
    session_id: Optional[str] = None
    message_id: Optional[str] = None

class ChatFeedbackCreate(BaseModel):
    message_id: str
    rating: int # 1 for up, -1 for down
    comment: Optional[str] = None

class ChatFeedbackOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    message_id: str
    rating: int
    comment: Optional[str] = None
    created_at: datetime

class ChatMessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    role: str
    content: str
    tool_calls: Optional[Any] = None
    created_at: datetime

class ChatSessionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    parcel_id: Optional[str] = None
    created_at: datetime
    messages: List[ChatMessageOut] = []

# --- Crops (Fiche Plante) ---
class PlantDetailOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name_fr: str
    name_en: Optional[str] = None
    scientific_name: Optional[str] = None
    family: Optional[str] = None
    type: Optional[str] = None
    temp_min: Optional[float] = None
    temp_max: Optional[float] = None
    rain_min: Optional[float] = None
    rain_max: Optional[float] = None
    ph_min: Optional[float] = None
    ph_max: Optional[float] = None
    source: Optional[str] = "FAO ECOCROP"
    suitable_countries: List[str] = []

# --- Alerts ---
class AlertOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    parcel_id: str
    type: str
    severity: str
    text: str
    created_at: datetime
    read: bool

# --- Dashboard Stats ---
class RegionStat(BaseModel):
    region: str
    country: str
    parcels_count: int
    avg_soil_richness: float
    top_recommended_crop: str
    cyclone_risk: str
    drought_risk: str

class StatsOverviewResponse(BaseModel):
    total_parcels: int
    total_area_ha: float
    active_farmers: int
    regions: List[RegionStat]

# --- Reforestation ---
class ReforestationZoneOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: Optional[str] = None
    risk_type: Optional[str] = None
    polygon_geojson: Optional[Dict[str, Any]] = None
    species_proposed: Optional[List[str]] = None
    area_ha: Optional[float] = None

# --- Jumeau de Rupture (Innovation I2) ---
class RuptureSimulateRequest(BaseModel):
    region: str = "Luxembourg"
    stress_type: str = "drought" # drought, cyclone, flood, pathogen
    duration_days: int = 30
    country: Optional[str] = None
