"""
GuardFlow AI Services - Configuration
Configurações centralizadas do sistema
"""

from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import List, Optional, Dict, Any
import os
from pathlib import Path

class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # Application
    APP_NAME: str = "GuardFlow AI Services"
    VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, env="DEBUG")
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    
    # API
    API_V1_STR: str = "/ai/v1"
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # CORS
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        env="ALLOWED_ORIGINS"
    )
    ALLOWED_HOSTS: List[str] = Field(
        default=["localhost", "127.0.0.1"],
        env="ALLOWED_HOSTS"
    )
    
    # Database
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    DATABASE_POOL_SIZE: int = Field(default=10, env="DATABASE_POOL_SIZE")
    DATABASE_MAX_OVERFLOW: int = Field(default=20, env="DATABASE_MAX_OVERFLOW")
    
    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    REDIS_TTL: int = Field(default=3600, env="REDIS_TTL")
    
    # AI Models
    MODEL_PATH: str = Field(default="/models", env="MODEL_PATH")
    MODEL_CACHE_TTL: int = Field(default=3600, env="MODEL_CACHE_TTL")
    MODEL_BATCH_SIZE: int = Field(default=32, env="MODEL_BATCH_SIZE")
    MODEL_MAX_WORKERS: int = Field(default=4, env="MODEL_MAX_WORKERS")
    
    # External APIs
    GOOGLE_VISION_API_KEY: Optional[str] = Field(default=None, env="GOOGLE_VISION_API_KEY")
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    HUGGINGFACE_API_KEY: Optional[str] = Field(default=None, env="HUGGINGFACE_API_KEY")
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    RATE_LIMIT_WINDOW: int = Field(default=60, env="RATE_LIMIT_WINDOW")
    
    # Monitoring
    SENTRY_DSN: Optional[str] = Field(default=None, env="SENTRY_DSN")
    PROMETHEUS_ENABLED: bool = Field(default=True, env="PROMETHEUS_ENABLED")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(default="json", env="LOG_FORMAT")
    
    # Security
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    PASSWORD_MIN_LENGTH: int = Field(default=8, env="PASSWORD_MIN_LENGTH")
    
    # AI Services Configuration
    VISION_CONFIDENCE_THRESHOLD: float = Field(default=0.8, env="VISION_CONFIDENCE_THRESHOLD")
    NLP_LANGUAGE_DETECTION: bool = Field(default=True, env="NLP_LANGUAGE_DETECTION")
    ANALYTICS_PREDICTION_HORIZON: int = Field(default=7, env="ANALYTICS_PREDICTION_HORIZON")
    
    # Model-specific settings
    PRODUCT_RECOGNITION_MODEL: str = Field(default="yolov8n", env="PRODUCT_RECOGNITION_MODEL")
    SENTIMENT_ANALYSIS_MODEL: str = Field(default="bert-base-multilingual", env="SENTIMENT_ANALYSIS_MODEL")
    RECOMMENDATION_MODEL: str = Field(default="collaborative_filtering", env="RECOMMENDATION_MODEL")
    
    # Performance
    MAX_CONCURRENT_REQUESTS: int = Field(default=100, env="MAX_CONCURRENT_REQUESTS")
    REQUEST_TIMEOUT: int = Field(default=30, env="REQUEST_TIMEOUT")
    MODEL_LOAD_TIMEOUT: int = Field(default=60, env="MODEL_LOAD_TIMEOUT")
    
    # File Upload
    MAX_FILE_SIZE: int = Field(default=10 * 1024 * 1024, env="MAX_FILE_SIZE")  # 10MB
    ALLOWED_FILE_TYPES: List[str] = Field(
        default=["image/jpeg", "image/png", "image/webp"],
        env="ALLOWED_FILE_TYPES"
    )
    
    # Cache
    CACHE_ENABLED: bool = Field(default=True, env="CACHE_ENABLED")
    CACHE_DEFAULT_TTL: int = Field(default=300, env="CACHE_DEFAULT_TTL")  # 5 minutes
    
    # Feature Flags
    ENABLE_VISION: bool = Field(default=True, env="ENABLE_VISION")
    ENABLE_ANALYTICS: bool = Field(default=True, env="ENABLE_ANALYTICS")
    ENABLE_NLP: bool = Field(default=True, env="ENABLE_NLP")
    ENABLE_RECOMMENDATIONS: bool = Field(default=True, env="ENABLE_RECOMMENDATIONS")
    ENABLE_OPTIMIZATION: bool = Field(default=True, env="ENABLE_OPTIMIZATION")
    
    @validator("ALLOWED_ORIGINS", pre=True)
    def parse_allowed_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @validator("ALLOWED_HOSTS", pre=True)
    def parse_allowed_hosts(cls, v):
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v
    
    @validator("ALLOWED_FILE_TYPES", pre=True)
    def parse_allowed_file_types(cls, v):
        if isinstance(v, str):
            return [file_type.strip() for file_type in v.split(",")]
        return v
    
    @validator("MODEL_PATH")
    def validate_model_path(cls, v):
        path = Path(v)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        return str(path.absolute())
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Instância global das configurações
settings = Settings()

# Configurações específicas por ambiente
ENVIRONMENT_CONFIGS = {
    "development": {
        "DEBUG": True,
        "LOG_LEVEL": "DEBUG",
        "CACHE_ENABLED": False,
    },
    "staging": {
        "DEBUG": False,
        "LOG_LEVEL": "INFO",
        "CACHE_ENABLED": True,
    },
    "production": {
        "DEBUG": False,
        "LOG_LEVEL": "WARNING",
        "CACHE_ENABLED": True,
        "PROMETHEUS_ENABLED": True,
    }
}

def get_environment_config() -> Dict[str, Any]:
    """Retorna configurações específicas do ambiente"""
    return ENVIRONMENT_CONFIGS.get(settings.ENVIRONMENT, {})

# Configurações de modelos de IA
AI_MODEL_CONFIGS = {
    "product_recognition": {
        "model_name": "yolov8n",
        "confidence_threshold": 0.8,
        "max_detections": 100,
        "input_size": (640, 640),
    },
    "sentiment_analysis": {
        "model_name": "bert-base-multilingual-uncased",
        "max_length": 512,
        "batch_size": 16,
    },
    "demand_forecasting": {
        "model_name": "lstm_forecaster",
        "sequence_length": 30,
        "prediction_horizon": 7,
    },
    "recommendation": {
        "model_name": "collaborative_filtering",
        "n_recommendations": 10,
        "min_rating": 3.0,
    }
}

def get_model_config(model_name: str) -> Dict[str, Any]:
    """Retorna configuração específica do modelo"""
    return AI_MODEL_CONFIGS.get(model_name, {})
