"""
ERP Integration Main Application
Aplicação principal para integração com sistemas ERP
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from datetime import datetime
from typing import Dict, Any

from .api.v1.erp_integration import router as erp_router
from .core.erp_auth import ERPAuthManager, AuthMethod, AuthCredentials
from .core.data_sync import DataSynchronizer, SyncScheduler

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Criar aplicação FastAPI
app = FastAPI(
    title="GuardFlow ERP Integration",
    description="Sistema de integração com ERPs (SAP, Oracle, Dynamics, TOTVS)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar componentes
auth_manager = ERPAuthManager()
synchronizer = DataSynchronizer()
scheduler = SyncScheduler(synchronizer)

# Incluir routers
app.include_router(erp_router, prefix="/api/v1/erp", tags=["ERP Integration"])

@app.on_event("startup")
async def startup_event():
    """Evento de inicialização"""
    logger.info("Iniciando GuardFlow ERP Integration...")
    
    # Registrar autenticadores padrão
    try:
        # Basic Auth para SAP
        auth_manager.register_authenticator(
            "sap", 
            AuthMethod.BASIC_AUTH, 
            {"host": "sap-server", "port": 8000}
        )
        
        # OAuth2 para Oracle
        auth_manager.register_authenticator(
            "oracle", 
            AuthMethod.OAUTH2, 
            {
                "auth_url": "https://oracle-server/oauth2/auth",
                "token_url": "https://oracle-server/oauth2/token"
            }
        )
        
        # API Key para Dynamics
        auth_manager.register_authenticator(
            "dynamics", 
            AuthMethod.API_KEY, 
            {"api_base_url": "https://dynamics-server/api"}
        )
        
        # JWT para TOTVS
        auth_manager.register_authenticator(
            "totvs", 
            AuthMethod.JWT, 
            {"secret_key": "totvs-secret-key", "algorithm": "HS256"}
        )
        
        logger.info("Autenticadores registrados com sucesso")
        
    except Exception as e:
        logger.error(f"Erro ao registrar autenticadores: {e}")
    
    # Iniciar agendador de sincronização
    try:
        # Executar agendador em background
        import asyncio
        asyncio.create_task(scheduler.start_scheduler())
        logger.info("Agendador de sincronização iniciado")
        
    except Exception as e:
        logger.error(f"Erro ao iniciar agendador: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Evento de encerramento"""
    logger.info("Encerrando GuardFlow ERP Integration...")
    
    try:
        # Parar agendador
        await scheduler.stop_scheduler()
        logger.info("Agendador de sincronização parado")
        
    except Exception as e:
        logger.error(f"Erro ao parar agendador: {e}")

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "GuardFlow ERP Integration API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health",
            "erp": "/api/v1/erp"
        }
    }

@app.get("/health")
async def health_check():
    """Health check da aplicação"""
    try:
        # Verificar componentes
        auth_sessions = len(auth_manager.get_active_sessions())
        sync_jobs = len(synchronizer.get_all_jobs())
        scheduled_jobs = len(scheduler.get_scheduled_jobs())
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "components": {
                "auth_manager": {
                    "status": "healthy",
                    "active_sessions": auth_sessions
                },
                "synchronizer": {
                    "status": "healthy",
                    "total_jobs": sync_jobs
                },
                "scheduler": {
                    "status": "healthy" if scheduler.is_running else "stopped",
                    "scheduled_jobs": scheduled_jobs
                }
            },
            "erp_support": [
                "SAP",
                "Oracle", 
                "Microsoft Dynamics",
                "TOTVS"
            ],
            "auth_methods": [
                "Basic Auth",
                "OAuth2",
                "API Key",
                "JWT"
            ]
        }
        
    except Exception as e:
        logger.error(f"Erro no health check: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )

@app.get("/status")
async def get_status():
    """Status detalhado da aplicação"""
    try:
        # Obter estatísticas
        active_sessions = auth_manager.get_active_sessions()
        all_jobs = synchronizer.get_all_jobs()
        scheduled_jobs = scheduler.get_scheduled_jobs()
        
        # Estatísticas por ERP
        erp_stats = {}
        for session in active_sessions.values():
            erp_type = session["erp_type"]
            if erp_type not in erp_stats:
                erp_stats[erp_type] = {"sessions": 0, "jobs": 0}
            erp_stats[erp_type]["sessions"] += 1
        
        for job in all_jobs:
            erp_type = job.erp_type
            if erp_type not in erp_stats:
                erp_stats[erp_type] = {"sessions": 0, "jobs": 0}
            erp_stats[erp_type]["jobs"] += 1
        
        return {
            "application": {
                "name": "GuardFlow ERP Integration",
                "version": "1.0.0",
                "uptime": "running",
                "timestamp": datetime.now().isoformat()
            },
            "statistics": {
                "active_sessions": len(active_sessions),
                "total_jobs": len(all_jobs),
                "scheduled_jobs": len(scheduled_jobs),
                "erp_breakdown": erp_stats
            },
            "job_status": {
                "pending": len([j for j in all_jobs if j.status.value == "pending"]),
                "running": len([j for j in all_jobs if j.status.value == "running"]),
                "completed": len([j for j in all_jobs if j.status.value == "completed"]),
                "failed": len([j for j in all_jobs if j.status.value == "failed"]),
                "cancelled": len([j for j in all_jobs if j.status.value == "cancelled"])
            },
            "scheduler": {
                "running": scheduler.is_running,
                "scheduled_jobs": list(scheduled_jobs.keys())
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter status: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/metrics")
async def get_metrics():
    """Métricas da aplicação"""
    try:
        all_jobs = synchronizer.get_all_jobs()
        active_sessions = auth_manager.get_active_sessions()
        
        # Calcular métricas
        total_records_processed = sum(job.records_processed for job in all_jobs)
        total_records_success = sum(job.records_success for job in all_jobs)
        total_records_failed = sum(job.records_failed for job in all_jobs)
        
        success_rate = (total_records_success / total_records_processed * 100) if total_records_processed > 0 else 0
        
        return {
            "timestamp": datetime.now().isoformat(),
            "performance": {
                "total_records_processed": total_records_processed,
                "total_records_success": total_records_success,
                "total_records_failed": total_records_failed,
                "success_rate_percent": round(success_rate, 2)
            },
            "sessions": {
                "active_sessions": len(active_sessions),
                "sessions_by_erp": {
                    erp_type: len([s for s in active_sessions.values() if s["erp_type"] == erp_type])
                    for erp_type in set(s["erp_type"] for s in active_sessions.values())
                }
            },
            "jobs": {
                "total_jobs": len(all_jobs),
                "jobs_by_status": {
                    status.value: len([j for j in all_jobs if j.status.value == status.value])
                    for status in set(job.status for job in all_jobs)
                },
                "jobs_by_erp": {
                    erp_type: len([j for j in all_jobs if j.erp_type == erp_type])
                    for erp_type in set(job.erp_type for job in all_jobs)
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter métricas: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handler para HTTPException"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url)
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handler para exceções gerais"""
    logger.error(f"Erro não tratado: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Erro interno do servidor",
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url)
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8003,
        reload=True,
        log_level="info"
    )

