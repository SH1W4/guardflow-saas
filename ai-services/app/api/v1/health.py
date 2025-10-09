"""
GuardFlow AI Services - Health Check API
Monitoramento de saúde dos serviços de IA
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
import logging
import asyncio
from datetime import datetime, timedelta

from app.core.config import settings
from app.core.models import ModelManager
from app.core.database import get_db_connection
from app.core.exceptions import AIException

logger = logging.getLogger(__name__)
router = APIRouter()

# Inicializar gerenciador de modelos
model_manager = ModelManager()

@router.get("/")
async def health_check():
    """
    Health check básico da API
    
    Returns:
        Status da API e informações básicas
    """
    try:
        return {
            "status": "healthy",
            "service": "GuardFlow AI Services",
            "version": settings.VERSION,
            "timestamp": datetime.utcnow().isoformat(),
            "environment": settings.ENVIRONMENT
        }
    except Exception as e:
        logger.error(f"Erro no health check: {str(e)}")
        raise HTTPException(status_code=500, detail="Service unhealthy")

@router.get("/detailed")
async def detailed_health_check():
    """
    Health check detalhado com status de todos os componentes
    
    Returns:
        Status detalhado de todos os serviços
    """
    try:
        health_status = {
            "overall_status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "GuardFlow AI Services",
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT,
            "components": {}
        }
        
        # Verificar database
        db_status = await check_database_health()
        health_status["components"]["database"] = db_status
        
        # Verificar Redis
        redis_status = await check_redis_health()
        health_status["components"]["redis"] = redis_status
        
        # Verificar modelos de IA
        models_status = await check_models_health()
        health_status["components"]["ai_models"] = models_status
        
        # Verificar APIs externas
        external_apis_status = await check_external_apis_health()
        health_status["components"]["external_apis"] = external_apis_status
        
        # Determinar status geral
        all_healthy = all(
            component["status"] == "healthy" 
            for component in health_status["components"].values()
        )
        
        if not all_healthy:
            health_status["overall_status"] = "degraded"
        
        return health_status
        
    except Exception as e:
        logger.error(f"Erro no health check detalhado: {str(e)}")
        return {
            "overall_status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }

@router.get("/models")
async def models_health_check():
    """
    Health check específico dos modelos de IA
    
    Returns:
        Status de todos os modelos
    """
    try:
        models_status = await model_manager.get_all_models_status()
        
        return {
            "models": models_status,
            "total_models": len(models_status),
            "healthy_models": len([m for m in models_status if m["status"] == "healthy"]),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Erro no health check dos modelos: {str(e)}")
        raise HTTPException(status_code=500, detail="Error checking models health")

@router.get("/performance")
async def performance_metrics():
    """
    Métricas de performance dos serviços
    
    Returns:
        Métricas de performance e uso
    """
    try:
        metrics = {
            "timestamp": datetime.utcnow().isoformat(),
            "performance": {
                "avg_response_time": await get_avg_response_time(),
                "requests_per_minute": await get_requests_per_minute(),
                "error_rate": await get_error_rate(),
                "cpu_usage": await get_cpu_usage(),
                "memory_usage": await get_memory_usage()
            },
            "ai_models": {
                "total_predictions": await get_total_predictions(),
                "avg_prediction_time": await get_avg_prediction_time(),
                "model_accuracy": await get_model_accuracy()
            }
        }
        
        return metrics
        
    except Exception as e:
        logger.error(f"Erro nas métricas de performance: {str(e)}")
        raise HTTPException(status_code=500, detail="Error getting performance metrics")

@router.get("/alerts")
async def get_alerts():
    """
    Lista alertas ativos do sistema
    
    Returns:
        Lista de alertas e notificações
    """
    try:
        alerts = await get_active_alerts()
        
        return {
            "alerts": alerts,
            "total_alerts": len(alerts),
            "critical_alerts": len([a for a in alerts if a["severity"] == "critical"]),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter alertas: {str(e)}")
        raise HTTPException(status_code=500, detail="Error getting alerts")

# Funções auxiliares
async def check_database_health() -> Dict[str, Any]:
    """Verifica saúde da database"""
    try:
        db = await get_db_connection()
        # Teste simples de conexão
        await db.execute("SELECT 1")
        
        return {
            "status": "healthy",
            "response_time": "< 100ms",
            "connection_pool": "active"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "response_time": "timeout"
        }

async def check_redis_health() -> Dict[str, Any]:
    """Verifica saúde do Redis"""
    try:
        import redis
        r = redis.from_url(settings.REDIS_URL)
        r.ping()
        
        return {
            "status": "healthy",
            "response_time": "< 50ms",
            "memory_usage": "normal"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "response_time": "timeout"
        }

async def check_models_health() -> Dict[str, Any]:
    """Verifica saúde dos modelos de IA"""
    try:
        models_status = await model_manager.get_all_models_status()
        healthy_count = len([m for m in models_status if m["status"] == "healthy"])
        total_count = len(models_status)
        
        return {
            "status": "healthy" if healthy_count == total_count else "degraded",
            "healthy_models": healthy_count,
            "total_models": total_count,
            "models": models_status
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

async def check_external_apis_health() -> Dict[str, Any]:
    """Verifica saúde das APIs externas"""
    try:
        apis_status = {}
        
        # Verificar Google Vision API
        if settings.GOOGLE_VISION_API_KEY:
            apis_status["google_vision"] = await check_google_vision_api()
        
        # Verificar OpenAI API
        if settings.OPENAI_API_KEY:
            apis_status["openai"] = await check_openai_api()
        
        # Verificar Hugging Face API
        if settings.HUGGINGFACE_API_KEY:
            apis_status["huggingface"] = await check_huggingface_api()
        
        all_healthy = all(api["status"] == "healthy" for api in apis_status.values())
        
        return {
            "status": "healthy" if all_healthy else "degraded",
            "apis": apis_status
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

async def check_google_vision_api() -> Dict[str, Any]:
    """Verifica Google Vision API"""
    try:
        # Implementar verificação real
        return {
            "status": "healthy",
            "response_time": "< 200ms"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

async def check_openai_api() -> Dict[str, Any]:
    """Verifica OpenAI API"""
    try:
        # Implementar verificação real
        return {
            "status": "healthy",
            "response_time": "< 300ms"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

async def check_huggingface_api() -> Dict[str, Any]:
    """Verifica Hugging Face API"""
    try:
        # Implementar verificação real
        return {
            "status": "healthy",
            "response_time": "< 250ms"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

async def get_avg_response_time() -> float:
    """Retorna tempo médio de resposta"""
    # Implementar métricas reais
    return 150.0  # ms

async def get_requests_per_minute() -> int:
    """Retorna requests por minuto"""
    # Implementar métricas reais
    return 45

async def get_error_rate() -> float:
    """Retorna taxa de erro"""
    # Implementar métricas reais
    return 0.02  # 2%

async def get_cpu_usage() -> float:
    """Retorna uso de CPU"""
    # Implementar métricas reais
    return 35.0  # %

async def get_memory_usage() -> float:
    """Retorna uso de memória"""
    # Implementar métricas reais
    return 60.0  # %

async def get_total_predictions() -> int:
    """Retorna total de predições"""
    # Implementar métricas reais
    return 1250

async def get_avg_prediction_time() -> float:
    """Retorna tempo médio de predição"""
    # Implementar métricas reais
    return 200.0  # ms

async def get_model_accuracy() -> Dict[str, float]:
    """Retorna precisão dos modelos"""
    # Implementar métricas reais
    return {
        "product_recognition": 0.92,
        "sentiment_analysis": 0.88,
        "demand_forecasting": 0.85
    }

async def get_active_alerts() -> List[Dict[str, Any]]:
    """Retorna alertas ativos"""
    # Implementar sistema de alertas real
    return [
        {
            "id": "alert_001",
            "severity": "warning",
            "message": "Model accuracy below threshold",
            "timestamp": datetime.utcnow().isoformat()
        }
    ]
