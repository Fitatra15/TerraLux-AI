import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env", extra="allow")
    PROJECT_NAME: str = "TerraLux AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = ""
    
    # LLM & Function Calling (OpenAI, Groq, Ollama)
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY")
    OLLAMA_URL: Optional[str] = os.getenv("OLLAMA_URL", os.getenv("OLLAMA_HOST"))
    LLM_MODEL: str = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./terralux.db")
    
    # Auth
    JWT_SECRET: str = os.getenv("JWT_SECRET", "terralux_hackathon_super_secret_jwt_2026")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 24 hours
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    
    # Uploads
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
    
    # Scoring weights (Prompt 3)
    WEIGHT_CLIMATE: float = 0.40
    WEIGHT_SOIL: float = 0.30
    WEIGHT_ROTATION: float = 0.30

    # Soil richness weights (Prompt 2 & 4)
    WEIGHT_DEPTH_0_5: float = 0.50
    WEIGHT_DEPTH_5_15: float = 0.30
    WEIGHT_DEPTH_15_30: float = 0.20
    
    # Soil Richness index component weights (Prompt 2)
    WEIGHT_RICHNESS_SOC: float = 0.40
    WEIGHT_RICHNESS_CEC: float = 0.30
    WEIGHT_RICHNESS_N: float = 0.20
    WEIGHT_RICHNESS_PH: float = 0.10

    # Multimodal context fusion weights (Prompt 6)
    WEIGHT_FUSION_IMAGE: float = 0.60
    WEIGHT_FUSION_CLIMATE: float = 0.25
    WEIGHT_FUSION_SOIL: float = 0.15



settings = Settings()
