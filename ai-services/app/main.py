"""
GuardFlow AI Services - Main Application
Sistema de IA SaaS para análise inteligente de varejo
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import init_db
from app.api.v1 import (
    vision,
    analytics,
    nlp,
    recommendations,
    optimization,
    health
)
from app.core.middleware import (
    RateLimitMiddleware,
    LoggingMiddleware,
    SecurityMiddleware
)
from app.core.exceptions import (
    AIException,
    ModelNotFoundException,
    ValidationException
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerenciar ciclo de vida da aplicação"""
    # Startup
    logger.info("🚀 Iniciando GuardFlow AI Services...")
    await init_db()
    logger.info("✅ Database inicializada")
    
    # Carregar modelos de IA
    from app.core.models import ModelManager
    model_manager = ModelManager()
    await model_manager.load_models()
    logger.info("🤖 Modelos de IA carregados")
    
    yield
    
    # Shutdown
    logger.info("🛑 Finalizando GuardFlow AI Services...")

# Criar aplicação FastAPI
app = FastAPI(
    title="GuardFlow AI Services",
    description="Sistema de IA SaaS para análise inteligente de varejo",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Middleware de segurança
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware customizado
app.add_middleware(RateLimitMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(SecurityMiddleware)

# Incluir routers
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(vision.router, prefix="/ai/v1/vision", tags=["Computer Vision"])
app.include_router(analytics.router, prefix="/ai/v1/analytics", tags=["Analytics"])
app.include_router(nlp.router, prefix="/ai/v1/nlp", tags=["Natural Language Processing"])
app.include_router(recommendations.router, prefix="/ai/v1/recommendations", tags=["Recommendations"])
app.include_router(optimization.router, prefix="/ai/v1/optimization", tags=["Optimization"])

# Exception handlers
@app.exception_handler(AIException)
async def ai_exception_handler(request, exc: AIException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "AI Processing Error",
            "message": str(exc),
            "type": "ai_error"
        }
    )

@app.exception_handler(ModelNotFoundException)
async def model_not_found_handler(request, exc: ModelNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "Model Not Found",
            "message": str(exc),
            "type": "model_error"
        }
    )

@app.exception_handler(ValidationException)
async def validation_exception_handler(request, exc: ValidationException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Validation Error",
            "message": str(exc),
            "type": "validation_error"
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP Error",
            "message": exc.detail,
            "type": "http_error"
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    logger.error(f"Erro não tratado: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "Erro interno do servidor",
            "type": "internal_error"
        }
    )

# Root endpoint
@app.get("/")
async def root():
    """Endpoint raiz da API"""
    return {
        "message": "GuardFlow AI Services",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs",
        "health": "/health"
    }

# Health check
@app.get("/ping")
async def ping():
    """Health check simples"""
    return {"status": "pong", "service": "guardflow-ai"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
