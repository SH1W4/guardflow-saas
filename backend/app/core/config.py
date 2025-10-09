"""
GuardFlow SaaS - Configuration
Configurações centralizadas da aplicação
"""
from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # ===========================================
    # API CONFIGURATION
    # ===========================================
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_VERSION: str = "v1"
    API_TITLE: str = "GuardFlow SaaS API"
    API_DESCRIPTION: str = "Plataforma de IA para Mercados com Ecossistema GST"
    API_DOCS_URL: str = "/docs"
    API_REDOC_URL: str = "/redoc"
    
    # ===========================================
    # SECURITY CONFIGURATION
    # ===========================================
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    JWT_SECRET_KEY: str = "your-jwt-secret-key-here"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # ===========================================
    # DATABASE CONFIGURATION
    # ===========================================
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/guardflow_saas"
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "guardflow_saas"
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "password"
    
    # ===========================================
    # REDIS CONFIGURATION
    # ===========================================
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    
    # ===========================================
    # GUARDPASS INTEGRATION
    # ===========================================
    GUARDPASS_API_KEY: Optional[str] = None
    GUARDPASS_API_URL: str = "https://api.guardpass.com"
    GUARDPASS_CLIENT_ID: Optional[str] = None
    GUARDPASS_CLIENT_SECRET: Optional[str] = None
    GUARDPASS_REDIRECT_URI: str = "http://localhost:3000/auth/callback"
    
    # ===========================================
    # AI SERVICES
    # ===========================================
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4"
    HUGGINGFACE_API_KEY: Optional[str] = None
    GOOGLE_VISION_API_KEY: Optional[str] = None
    GOOGLE_VISION_PROJECT_ID: Optional[str] = None
    
    # ===========================================
    # PAYMENT SERVICES
    # ===========================================
    MERCADO_PAGO_ACCESS_TOKEN: Optional[str] = None
    MERCADO_PAGO_PUBLIC_KEY: Optional[str] = None
    MERCADO_PAGO_WEBHOOK_SECRET: Optional[str] = None
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_PUBLISHABLE_KEY: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None
    
    # ===========================================
    # BLOCKCHAIN CONFIGURATION
    # ===========================================
    POLYGON_RPC_URL: str = "https://polygon-rpc.com"
    POLYGON_CHAIN_ID: int = 137
    PRIVATE_KEY: Optional[str] = None
    CONTRACT_ADDRESS: Optional[str] = None
    GAS_LIMIT: int = 1000000
    GAS_PRICE: int = 20000000000
    
    # ===========================================
    # EMAIL CONFIGURATION
    # ===========================================
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    
    # ===========================================
    # NOTIFICATION SERVICES
    # ===========================================
    FIREBASE_SERVER_KEY: Optional[str] = None
    FIREBASE_PROJECT_ID: Optional[str] = None
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_PHONE_NUMBER: Optional[str] = None
    
    # ===========================================
    # FILE STORAGE
    # ===========================================
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    AWS_S3_BUCKET: Optional[str] = None
    MINIO_ENDPOINT: str = "http://localhost:9000"
    MINIO_ACCESS_KEY: str = "admin"
    MINIO_SECRET_KEY: str = "password123"
    
    # ===========================================
    # MONITORING & LOGGING
    # ===========================================
    SENTRY_DSN: Optional[str] = None
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    KIBANA_URL: str = "http://localhost:5601"
    PROMETHEUS_URL: str = "http://localhost:9090"
    GRAFANA_URL: str = "http://localhost:3001"
    
    # ===========================================
    # CELERY CONFIGURATION
    # ===========================================
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    CELERY_TASK_SERIALIZER: str = "json"
    CELERY_RESULT_SERIALIZER: str = "json"
    CELERY_ACCEPT_CONTENT: List[str] = ["json"]
    CELERY_TIMEZONE: str = "America/Sao_Paulo"
    CELERY_ENABLE_UTC: bool = True
    
    # ===========================================
    # DEVELOPMENT CONFIGURATION
    # ===========================================
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    TESTING: bool = False
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:19000"]
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1", "0.0.0.0"]
    
    # ===========================================
    # FEATURE FLAGS
    # ===========================================
    FEATURE_AI_ENABLED: bool = True
    FEATURE_BLOCKCHAIN_ENABLED: bool = True
    FEATURE_ESG_ENABLED: bool = True
    FEATURE_NFT_ENABLED: bool = True
    FEATURE_DEFI_ENABLED: bool = False
    FEATURE_METAVERSE_ENABLED: bool = False
    
    # ===========================================
    # RATE LIMITING
    # ===========================================
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60
    RATE_LIMIT_BURST: int = 200
    
    # ===========================================
    # CACHE CONFIGURATION
    # ===========================================
    CACHE_TTL: int = 3600
    CACHE_MAX_SIZE: int = 1000
    CACHE_BACKEND: str = "redis"
    CACHE_PREFIX: str = "guardflow_saas"
    
    # ===========================================
    # BACKUP CONFIGURATION
    # ===========================================
    BACKUP_ENABLED: bool = True
    BACKUP_SCHEDULE: str = "0 2 * * *"
    BACKUP_RETENTION_DAYS: int = 30
    BACKUP_S3_BUCKET: Optional[str] = None
    
    # ===========================================
    # HEALTH CHECK CONFIGURATION
    # ===========================================
    HEALTH_CHECK_ENABLED: bool = True
    HEALTH_CHECK_INTERVAL: int = 30
    HEALTH_CHECK_TIMEOUT: int = 10
    HEALTH_CHECK_RETRIES: int = 3
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Instância global das configurações
settings = Settings()

# Configurações específicas por ambiente
if settings.ENVIRONMENT == "production":
    settings.DEBUG = False
    settings.CORS_ORIGINS = [
        "https://app.guardflow.com",
        "https://dashboard.guardflow.com"
    ]
    settings.ALLOWED_HOSTS = [
        "app.guardflow.com",
        "dashboard.guardflow.com",
        "api.guardflow.com"
    ]
elif settings.ENVIRONMENT == "staging":
    settings.DEBUG = True
    settings.CORS_ORIGINS = [
        "https://staging-app.guardflow.com",
        "https://staging-dashboard.guardflow.com"
    ]
    settings.ALLOWED_HOSTS = [
        "staging-app.guardflow.com",
        "staging-dashboard.guardflow.com",
        "staging-api.guardflow.com"
    ]
