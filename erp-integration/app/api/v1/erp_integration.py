"""
ERP Integration API - Endpoints para integração com sistemas ERP
SAP, Oracle, Microsoft Dynamics, TOTVS, etc.
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
from enum import Enum

from ..core.erp_connectors import ERPConnectorFactory, ERPConnector
from ..core.data_mapping import DataMapper, ERPType, DataValidator
from ..core.data_sync import DataSynchronizer, SyncType, SyncStatus, SyncScheduler

logger = logging.getLogger(__name__)
router = APIRouter()

# Instâncias globais
synchronizer = DataSynchronizer()
scheduler = SyncScheduler(synchronizer)

class ERPConfig(BaseModel):
    """Configuração de ERP"""
    erp_type: str = Field(..., description="Tipo de ERP (sap, oracle, dynamics, totvs)")
    host: str = Field(..., description="Host do ERP")
    port: int = Field(..., description="Porta do ERP")
    username: str = Field(..., description="Usuário do ERP")
    password: str = Field(..., description="Senha do ERP")
    database: Optional[str] = Field(None, description="Nome do banco de dados")
    additional_config: Optional[Dict[str, Any]] = Field(None, description="Configurações adicionais")

class SyncRequest(BaseModel):
    """Request para sincronização"""
    erp_config: ERPConfig
    store_id: str = Field(..., description="ID da loja")
    sync_type: str = Field("batch", description="Tipo de sincronização (real_time, batch, manual)")
    data_types: List[str] = Field(["products", "inventory", "customers", "orders"], description="Tipos de dados para sincronizar")

class SyncResponse(BaseModel):
    """Response de sincronização"""
    job_id: str
    status: str
    message: str
    created_at: datetime

class JobStatusResponse(BaseModel):
    """Response de status do job"""
    job_id: str
    erp_type: str
    sync_type: str
    status: str
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    records_processed: int
    records_success: int
    records_failed: int
    error_message: Optional[str]

class ProductResponse(BaseModel):
    """Response de produto"""
    id: str
    name: str
    category: str
    price: float
    unit: str
    sustainable: bool
    carbon_footprint: float
    source_erp: str
    mapped_at: datetime

class CustomerResponse(BaseModel):
    """Response de cliente"""
    id: str
    name: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    postal_code: str
    source_erp: str
    mapped_at: datetime

class InventoryResponse(BaseModel):
    """Response de estoque"""
    product_id: str
    store_id: str
    quantity: int
    reserved: int
    available: int
    location: str
    source_erp: str
    mapped_at: datetime

class OrderResponse(BaseModel):
    """Response de pedido"""
    id: str
    customer_id: str
    order_date: str
    total_amount: float
    status: str
    items: List[Dict[str, Any]]
    source_erp: str
    mapped_at: datetime

@router.post("/connect", response_model=Dict[str, Any])
async def connect_erp(erp_config: ERPConfig):
    """
    Conectar ao sistema ERP
    """
    try:
        # Criar conector ERP
        connector = ERPConnectorFactory.create_connector(
            erp_config.erp_type,
            {
                "host": erp_config.host,
                "port": erp_config.port,
                "username": erp_config.username,
                "password": erp_config.password,
                "database": erp_config.database,
                **erp_config.additional_config or {}
            }
        )
        
        # Conectar
        is_connected = await connector.connect()
        
        if is_connected:
            return {
                "success": True,
                "message": f"Conexão estabelecida com {erp_config.erp_type.upper()}",
                "erp_type": erp_config.erp_type,
                "connected_at": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=400, detail="Falha ao conectar ao ERP")
            
    except Exception as e:
        logger.error(f"Erro ao conectar ERP: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/sync", response_model=SyncResponse)
async def sync_erp_data(sync_request: SyncRequest, background_tasks: BackgroundTasks):
    """
    Sincronizar dados do ERP
    """
    try:
        # Criar conector ERP
        connector = ERPConnectorFactory.create_connector(
            sync_request.erp_config.erp_type,
            {
                "host": sync_request.erp_config.host,
                "port": sync_request.erp_config.port,
                "username": sync_request.erp_config.username,
                "password": sync_request.erp_config.password,
                "database": sync_request.erp_config.database,
                **sync_request.erp_config.additional_config or {}
            }
        )
        
        # Conectar
        await connector.connect()
        
        # Determinar tipo de sincronização
        sync_type = SyncType(sync_request.sync_type)
        
        # Executar sincronização baseada nos tipos de dados
        jobs = []
        
        if "products" in sync_request.data_types:
            job = await synchronizer.sync_products(connector, sync_request.store_id, sync_type)
            jobs.append(job)
        
        if "inventory" in sync_request.data_types:
            job = await synchronizer.sync_inventory(connector, sync_request.store_id, sync_type)
            jobs.append(job)
        
        if "customers" in sync_request.data_types:
            job = await synchronizer.sync_customers(connector, sync_type)
            jobs.append(job)
        
        if "orders" in sync_request.data_types:
            job = await synchronizer.sync_orders(connector, sync_type)
            jobs.append(job)
        
        # Retornar primeiro job (ou criar um job consolidado)
        main_job = jobs[0] if jobs else None
        
        if main_job:
            return SyncResponse(
                job_id=main_job.id,
                status=main_job.status.value,
                message="Sincronização iniciada com sucesso",
                created_at=main_job.created_at
            )
        else:
            raise HTTPException(status_code=400, detail="Nenhum tipo de dados especificado")
            
    except Exception as e:
        logger.error(f"Erro na sincronização: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/sync/jobs", response_model=List[JobStatusResponse])
async def get_sync_jobs():
    """
    Obter todos os jobs de sincronização
    """
    try:
        jobs = synchronizer.get_all_jobs()
        
        return [
            JobStatusResponse(
                job_id=job.id,
                erp_type=job.erp_type,
                sync_type=job.sync_type.value,
                status=job.status.value,
                created_at=job.created_at,
                started_at=job.started_at,
                completed_at=job.completed_at,
                records_processed=job.records_processed,
                records_success=job.records_success,
                records_failed=job.records_failed,
                error_message=job.error_message
            )
            for job in jobs
        ]
        
    except Exception as e:
        logger.error(f"Erro ao obter jobs: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/sync/jobs/{job_id}", response_model=JobStatusResponse)
async def get_sync_job_status(job_id: str):
    """
    Obter status de um job específico
    """
    try:
        job = synchronizer.get_job_status(job_id)
        
        if not job:
            raise HTTPException(status_code=404, detail="Job não encontrado")
        
        return JobStatusResponse(
            job_id=job.id,
            erp_type=job.erp_type,
            sync_type=job.sync_type.value,
            status=job.status.value,
            created_at=job.created_at,
            started_at=job.started_at,
            completed_at=job.completed_at,
            records_processed=job.records_processed,
            records_success=job.records_success,
            records_failed=job.records_failed,
            error_message=job.error_message
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter status do job: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/sync/jobs/{job_id}/cancel")
async def cancel_sync_job(job_id: str):
    """
    Cancelar um job de sincronização
    """
    try:
        success = await synchronizer.cancel_job(job_id)
        
        if success:
            return {"message": "Job cancelado com sucesso"}
        else:
            raise HTTPException(status_code=404, detail="Job não encontrado ou não pode ser cancelado")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao cancelar job: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/sync/jobs/{job_id}/retry")
async def retry_sync_job(job_id: str):
    """
    Tentar novamente um job que falhou
    """
    try:
        job = await synchronizer.retry_failed_job(job_id)
        
        if job:
            return {"message": "Job será executado novamente", "job_id": job.id}
        else:
            raise HTTPException(status_code=404, detail="Job não encontrado ou não pode ser executado novamente")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao tentar novamente job: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/products", response_model=List[ProductResponse])
async def get_products(erp_config: ERPConfig, filters: Optional[Dict[str, Any]] = None):
    """
    Obter produtos do ERP
    """
    try:
        # Criar conector ERP
        connector = ERPConnectorFactory.create_connector(
            erp_config.erp_type,
            {
                "host": erp_config.host,
                "port": erp_config.port,
                "username": erp_config.username,
                "password": erp_config.password,
                "database": erp_config.database,
                **erp_config.additional_config or {}
            }
        )
        
        # Conectar
        await connector.connect()
        
        # Obter produtos
        products = await connector.get_products(filters)
        
        # Mapear produtos
        mapper = DataMapper(ERPType(erp_config.erp_type))
        mapped_products = mapper.map_products(products)
        
        # Validar produtos
        valid_products = []
        for product in mapped_products:
            if DataValidator.validate_product(product):
                valid_products.append(ProductResponse(**product))
        
        return valid_products
        
    except Exception as e:
        logger.error(f"Erro ao obter produtos: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/customers", response_model=List[CustomerResponse])
async def get_customers(erp_config: ERPConfig, filters: Optional[Dict[str, Any]] = None):
    """
    Obter clientes do ERP
    """
    try:
        # Criar conector ERP
        connector = ERPConnectorFactory.create_connector(
            erp_config.erp_type,
            {
                "host": erp_config.host,
                "port": erp_config.port,
                "username": erp_config.username,
                "password": erp_config.password,
                "database": erp_config.database,
                **erp_config.additional_config or {}
            }
        )
        
        # Conectar
        await connector.connect()
        
        # Obter clientes
        customers = await connector.get_customers(filters)
        
        # Mapear clientes
        mapper = DataMapper(ERPType(erp_config.erp_type))
        mapped_customers = mapper.map_customers(customers)
        
        # Validar clientes
        valid_customers = []
        for customer in mapped_customers:
            if DataValidator.validate_customer(customer):
                valid_customers.append(CustomerResponse(**customer))
        
        return valid_customers
        
    except Exception as e:
        logger.error(f"Erro ao obter clientes: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/inventory/{store_id}", response_model=List[InventoryResponse])
async def get_inventory(store_id: str, erp_config: ERPConfig):
    """
    Obter estoque do ERP
    """
    try:
        # Criar conector ERP
        connector = ERPConnectorFactory.create_connector(
            erp_config.erp_type,
            {
                "host": erp_config.host,
                "port": erp_config.port,
                "username": erp_config.username,
                "password": erp_config.password,
                "database": erp_config.database,
                **erp_config.additional_config or {}
            }
        )
        
        # Conectar
        await connector.connect()
        
        # Obter estoque
        inventory = await connector.get_inventory(store_id)
        
        # Mapear estoque
        mapper = DataMapper(ERPType(erp_config.erp_type))
        mapped_inventory = mapper.map_inventory(inventory)
        
        # Validar estoque
        valid_inventory = []
        for item in mapped_inventory:
            if DataValidator.validate_inventory_item(item):
                valid_inventory.append(InventoryResponse(**item))
        
        return valid_inventory
        
    except Exception as e:
        logger.error(f"Erro ao obter estoque: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/orders", response_model=List[OrderResponse])
async def get_orders(erp_config: ERPConfig, filters: Optional[Dict[str, Any]] = None):
    """
    Obter pedidos do ERP
    """
    try:
        # Criar conector ERP
        connector = ERPConnectorFactory.create_connector(
            erp_config.erp_type,
            {
                "host": erp_config.host,
                "port": erp_config.port,
                "username": erp_config.username,
                "password": erp_config.password,
                "database": erp_config.database,
                **erp_config.additional_config or {}
            }
        )
        
        # Conectar
        await connector.connect()
        
        # Obter pedidos
        orders = await connector.get_sales_orders(filters)
        
        # Mapear pedidos
        mapper = DataMapper(ERPType(erp_config.erp_type))
        mapped_orders = mapper.map_orders(orders)
        
        # Validar pedidos
        valid_orders = []
        for order in mapped_orders:
            if DataValidator.validate_order(order):
                valid_orders.append(OrderResponse(**order))
        
        return valid_orders
        
    except Exception as e:
        logger.error(f"Erro ao obter pedidos: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/schedule")
async def schedule_sync(erp_config: ERPConfig, store_id: str, interval_minutes: int = 60):
    """
    Agendar sincronização automática
    """
    try:
        # Criar conector ERP
        connector = ERPConnectorFactory.create_connector(
            erp_config.erp_type,
            {
                "host": erp_config.host,
                "port": erp_config.port,
                "username": erp_config.username,
                "password": erp_config.password,
                "database": erp_config.database,
                **erp_config.additional_config or {}
            }
        )
        
        # Agendar sincronização
        await scheduler.schedule_batch_sync(connector, store_id, interval_minutes)
        
        return {
            "message": f"Sincronização agendada para {erp_config.erp_type} (loja {store_id})",
            "interval_minutes": interval_minutes,
            "scheduled_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Erro ao agendar sincronização: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/schedule")
async def get_scheduled_syncs():
    """
    Obter sincronizações agendadas
    """
    try:
        scheduled_jobs = scheduler.get_scheduled_jobs()
        
        return {
            "scheduled_jobs": scheduled_jobs,
            "total_jobs": len(scheduled_jobs)
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter sincronizações agendadas: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.delete("/schedule/{job_id}")
async def remove_scheduled_sync(job_id: str):
    """
    Remover sincronização agendada
    """
    try:
        success = await scheduler.remove_scheduled_job(job_id)
        
        if success:
            return {"message": "Sincronização agendada removida com sucesso"}
        else:
            raise HTTPException(status_code=404, detail="Sincronização agendada não encontrada")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao remover sincronização agendada: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/health")
async def health_check():
    """
    Health check da integração ERP
    """
    try:
        return {
            "status": "healthy",
            "synchronizer_active": True,
            "scheduler_active": scheduler.is_running,
            "total_jobs": len(synchronizer.get_all_jobs()),
            "scheduled_jobs": len(scheduler.get_scheduled_jobs()),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Erro no health check: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

