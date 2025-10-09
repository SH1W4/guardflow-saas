"""
GuardFlow SaaS - Main Application
Plataforma de IA para Mercados com Ecossistema GST
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging
import uvicorn
from prometheus_fastapi_instrumentator import Instrumentator

# Importar configurações
from app.core.config import settings
from app.core.database import init_db
from app.core.redis import init_redis
from app.core.celery import init_celery

# Importar routers
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.markets import router as markets_router
from app.api.v1.products import router as products_router
from app.api.v1.scanner import router as scanner_router
from app.api.v1.payments import router as payments_router
from app.api.v1.esg import router as esg_router
from app.api.v1.gst import router as gst_router
from app.api.v1.blockchain import router as blockchain_router
from app.api.v1.ai import router as ai_router
from app.api.v1.integrations import router as integrations_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.health import router as health_router

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("guardflow_saas")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerenciar ciclo de vida da aplicação"""
    logger.info("🚀 Iniciando GuardFlow SaaS...")
    
    # Inicializar banco de dados
    await init_db()
    logger.info("✅ Banco de dados inicializado")
    
    # Inicializar Redis
    await init_redis()
    logger.info("✅ Redis inicializado")
    
    # Inicializar Celery
    init_celery()
    logger.info("✅ Celery inicializado")
    
    yield
    
    logger.info("🛑 Encerrando GuardFlow SaaS...")

# Criar aplicação FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version="1.0.0",
    docs_url=settings.API_DOCS_URL,
    redoc_url=settings.API_REDOC_URL,
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar Trusted Host
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

# Configurar Prometheus
if settings.ENVIRONMENT == "production":
    Instrumentator().instrument(app).expose(app)

# Incluir routers
app.include_router(auth_router, prefix="/api/v1", tags=["Autenticação"])
app.include_router(users_router, prefix="/api/v1", tags=["Usuários"])
app.include_router(markets_router, prefix="/api/v1", tags=["Mercados"])
app.include_router(products_router, prefix="/api/v1", tags=["Produtos"])
app.include_router(scanner_router, prefix="/api/v1", tags=["Scanner"])
app.include_router(payments_router, prefix="/api/v1", tags=["Pagamentos"])
app.include_router(esg_router, prefix="/api/v1", tags=["ESG"])
app.include_router(gst_router, prefix="/api/v1", tags=["GST Tokens"])
app.include_router(blockchain_router, prefix="/api/v1", tags=["Blockchain"])
app.include_router(ai_router, prefix="/api/v1", tags=["IA"])
app.include_router(integrations_router, prefix="/api/v1", tags=["Integrações"])
app.include_router(analytics_router, prefix="/api/v1", tags=["Analytics"])
app.include_router(health_router, prefix="/api/v1", tags=["Health"])

# Servir arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "GuardFlow SaaS - Plataforma de IA para Mercados",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs",
        "health": "/api/v1/health"
    }

@app.get("/health")
async def health_check():
    """Health check básico"""
    return {
        "status": "healthy",
        "service": "GuardFlow SaaS API",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handler para exceções HTTP"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url)
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handler para exceções gerais"""
    logger.error(f"❌ Erro não tratado: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Erro interno do servidor",
            "status_code": 500,
            "path": str(request.url)
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
