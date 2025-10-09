"""
Data Synchronization - Sincronização de dados entre ERPs e GuardFlow SaaS
Sistema de sincronização em tempo real e batch
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
from enum import Enum
import json
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

class SyncType(Enum):
    """Tipos de sincronização"""
    REAL_TIME = "real_time"
    BATCH = "batch"
    MANUAL = "manual"

class SyncStatus(Enum):
    """Status de sincronização"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class SyncJob:
    """Job de sincronização"""
    id: str
    erp_type: str
    sync_type: SyncType
    status: SyncStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    records_processed: int = 0
    records_success: int = 0
    records_failed: int = 0

class DataSynchronizer:
    """Sincronizador de dados entre ERPs e GuardFlow SaaS"""
    
    def __init__(self, max_workers: int = 5):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.sync_jobs: Dict[str, SyncJob] = {}
        self.sync_callbacks: List[Callable] = []
        self.is_running = False
    
    def add_sync_callback(self, callback: Callable):
        """Adicionar callback para eventos de sincronização"""
        self.sync_callbacks.append(callback)
    
    async def _notify_callbacks(self, job: SyncJob):
        """Notificar callbacks sobre mudanças no job"""
        for callback in self.sync_callbacks:
            try:
                await callback(job)
            except Exception as e:
                logger.error(f"Erro no callback: {e}")
    
    async def sync_products(self, erp_connector, store_id: str, sync_type: SyncType = SyncType.BATCH) -> SyncJob:
        """Sincronizar produtos do ERP"""
        job_id = f"sync_products_{erp_connector.__class__.__name__}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        job = SyncJob(
            id=job_id,
            erp_type=erp_connector.__class__.__name__,
            sync_type=sync_type,
            status=SyncStatus.PENDING,
            created_at=datetime.now()
        )
        
        self.sync_jobs[job_id] = job
        await self._notify_callbacks(job)
        
        try:
            job.status = SyncStatus.RUNNING
            job.started_at = datetime.now()
            await self._notify_callbacks(job)
            
            # Obter produtos do ERP
            products = await erp_connector.get_products()
            job.records_processed = len(products)
            
            # Processar produtos
            for product in products:
                try:
                    # Aqui seria a lógica de processamento/salvamento
                    # Por enquanto, apenas simular
                    await asyncio.sleep(0.01)  # Simular processamento
                    job.records_success += 1
                except Exception as e:
                    logger.error(f"Erro ao processar produto: {e}")
                    job.records_failed += 1
            
            job.status = SyncStatus.COMPLETED
            job.completed_at = datetime.now()
            
        except Exception as e:
            job.status = SyncStatus.FAILED
            job.error_message = str(e)
            job.completed_at = datetime.now()
            logger.error(f"Erro na sincronização de produtos: {e}")
        
        await self._notify_callbacks(job)
        return job
    
    async def sync_inventory(self, erp_connector, store_id: str, sync_type: SyncType = SyncType.BATCH) -> SyncJob:
        """Sincronizar estoque do ERP"""
        job_id = f"sync_inventory_{erp_connector.__class__.__name__}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        job = SyncJob(
            id=job_id,
            erp_type=erp_connector.__class__.__name__,
            sync_type=sync_type,
            status=SyncStatus.PENDING,
            created_at=datetime.now()
        )
        
        self.sync_jobs[job_id] = job
        await self._notify_callbacks(job)
        
        try:
            job.status = SyncStatus.RUNNING
            job.started_at = datetime.now()
            await self._notify_callbacks(job)
            
            # Obter estoque do ERP
            inventory = await erp_connector.get_inventory(store_id)
            job.records_processed = len(inventory)
            
            # Processar estoque
            for item in inventory:
                try:
                    # Aqui seria a lógica de processamento/salvamento
                    await asyncio.sleep(0.01)  # Simular processamento
                    job.records_success += 1
                except Exception as e:
                    logger.error(f"Erro ao processar item de estoque: {e}")
                    job.records_failed += 1
            
            job.status = SyncStatus.COMPLETED
            job.completed_at = datetime.now()
            
        except Exception as e:
            job.status = SyncStatus.FAILED
            job.error_message = str(e)
            job.completed_at = datetime.now()
            logger.error(f"Erro na sincronização de estoque: {e}")
        
        await self._notify_callbacks(job)
        return job
    
    async def sync_customers(self, erp_connector, sync_type: SyncType = SyncType.BATCH) -> SyncJob:
        """Sincronizar clientes do ERP"""
        job_id = f"sync_customers_{erp_connector.__class__.__name__}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        job = SyncJob(
            id=job_id,
            erp_type=erp_connector.__class__.__name__,
            sync_type=sync_type,
            status=SyncStatus.PENDING,
            created_at=datetime.now()
        )
        
        self.sync_jobs[job_id] = job
        await self._notify_callbacks(job)
        
        try:
            job.status = SyncStatus.RUNNING
            job.started_at = datetime.now()
            await self._notify_callbacks(job)
            
            # Obter clientes do ERP
            customers = await erp_connector.get_customers()
            job.records_processed = len(customers)
            
            # Processar clientes
            for customer in customers:
                try:
                    # Aqui seria a lógica de processamento/salvamento
                    await asyncio.sleep(0.01)  # Simular processamento
                    job.records_success += 1
                except Exception as e:
                    logger.error(f"Erro ao processar cliente: {e}")
                    job.records_failed += 1
            
            job.status = SyncStatus.COMPLETED
            job.completed_at = datetime.now()
            
        except Exception as e:
            job.status = SyncStatus.FAILED
            job.error_message = str(e)
            job.completed_at = datetime.now()
            logger.error(f"Erro na sincronização de clientes: {e}")
        
        await self._notify_callbacks(job)
        return job
    
    async def sync_orders(self, erp_connector, sync_type: SyncType = SyncType.BATCH) -> SyncJob:
        """Sincronizar pedidos do ERP"""
        job_id = f"sync_orders_{erp_connector.__class__.__name__}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        job = SyncJob(
            id=job_id,
            erp_type=erp_connector.__class__.__name__,
            sync_type=sync_type,
            status=SyncStatus.PENDING,
            created_at=datetime.now()
        )
        
        self.sync_jobs[job_id] = job
        await self._notify_callbacks(job)
        
        try:
            job.status = SyncStatus.RUNNING
            job.started_at = datetime.now()
            await self._notify_callbacks(job)
            
            # Obter pedidos do ERP
            orders = await erp_connector.get_sales_orders()
            job.records_processed = len(orders)
            
            # Processar pedidos
            for order in orders:
                try:
                    # Aqui seria a lógica de processamento/salvamento
                    await asyncio.sleep(0.01)  # Simular processamento
                    job.records_success += 1
                except Exception as e:
                    logger.error(f"Erro ao processar pedido: {e}")
                    job.records_failed += 1
            
            job.status = SyncStatus.COMPLETED
            job.completed_at = datetime.now()
            
        except Exception as e:
            job.status = SyncStatus.FAILED
            job.error_message = str(e)
            job.completed_at = datetime.now()
            logger.error(f"Erro na sincronização de pedidos: {e}")
        
        await self._notify_callbacks(job)
        return job
    
    async def full_sync(self, erp_connector, store_id: str, sync_type: SyncType = SyncType.BATCH) -> List[SyncJob]:
        """Sincronização completa (produtos, estoque, clientes, pedidos)"""
        jobs = []
        
        # Sincronizar produtos
        products_job = await self.sync_products(erp_connector, store_id, sync_type)
        jobs.append(products_job)
        
        # Sincronizar estoque
        inventory_job = await self.sync_inventory(erp_connector, store_id, sync_type)
        jobs.append(inventory_job)
        
        # Sincronizar clientes
        customers_job = await self.sync_customers(erp_connector, sync_type)
        jobs.append(customers_job)
        
        # Sincronizar pedidos
        orders_job = await self.sync_orders(erp_connector, sync_type)
        jobs.append(orders_job)
        
        return jobs
    
    def get_job_status(self, job_id: str) -> Optional[SyncJob]:
        """Obter status de um job"""
        return self.sync_jobs.get(job_id)
    
    def get_all_jobs(self) -> List[SyncJob]:
        """Obter todos os jobs"""
        return list(self.sync_jobs.values())
    
    def get_jobs_by_status(self, status: SyncStatus) -> List[SyncJob]:
        """Obter jobs por status"""
        return [job for job in self.sync_jobs.values() if job.status == status]
    
    def get_jobs_by_erp(self, erp_type: str) -> List[SyncJob]:
        """Obter jobs por tipo de ERP"""
        return [job for job in self.sync_jobs.values() if job.erp_type == erp_type]
    
    async def cancel_job(self, job_id: str) -> bool:
        """Cancelar um job"""
        if job_id in self.sync_jobs:
            job = self.sync_jobs[job_id]
            if job.status in [SyncStatus.PENDING, SyncStatus.RUNNING]:
                job.status = SyncStatus.CANCELLED
                job.completed_at = datetime.now()
                await self._notify_callbacks(job)
                return True
        return False
    
    async def retry_failed_job(self, job_id: str) -> Optional[SyncJob]:
        """Tentar novamente um job que falhou"""
        if job_id in self.sync_jobs:
            job = self.sync_jobs[job_id]
            if job.status == SyncStatus.FAILED:
                # Resetar job para tentar novamente
                job.status = SyncStatus.PENDING
                job.started_at = None
                job.completed_at = None
                job.error_message = None
                job.records_processed = 0
                job.records_success = 0
                job.records_failed = 0
                
                await self._notify_callbacks(job)
                return job
        return None

class SyncScheduler:
    """Agendador de sincronizações"""
    
    def __init__(self, synchronizer: DataSynchronizer):
        self.synchronizer = synchronizer
        self.scheduled_jobs: Dict[str, Dict[str, Any]] = {}
        self.is_running = False
    
    async def schedule_batch_sync(self, erp_connector, store_id: str, interval_minutes: int = 60):
        """Agendar sincronização em lote"""
        job_id = f"batch_sync_{erp_connector.__class__.__name__}_{store_id}"
        
        self.scheduled_jobs[job_id] = {
            "erp_connector": erp_connector,
            "store_id": store_id,
            "interval_minutes": interval_minutes,
            "last_run": None,
            "next_run": datetime.now() + timedelta(minutes=interval_minutes)
        }
        
        logger.info(f"Sincronização em lote agendada: {job_id} (intervalo: {interval_minutes} min)")
    
    async def start_scheduler(self):
        """Iniciar agendador"""
        self.is_running = True
        logger.info("Agendador de sincronização iniciado")
        
        while self.is_running:
            current_time = datetime.now()
            
            for job_id, job_config in self.scheduled_jobs.items():
                if job_config["next_run"] <= current_time:
                    try:
                        # Executar sincronização
                        await self.synchronizer.full_sync(
                            job_config["erp_connector"],
                            job_config["store_id"],
                            SyncType.BATCH
                        )
                        
                        # Atualizar próxima execução
                        job_config["last_run"] = current_time
                        job_config["next_run"] = current_time + timedelta(minutes=job_config["interval_minutes"])
                        
                        logger.info(f"Sincronização agendada executada: {job_id}")
                        
                    except Exception as e:
                        logger.error(f"Erro na sincronização agendada {job_id}: {e}")
            
            # Aguardar 1 minuto antes de verificar novamente
            await asyncio.sleep(60)
    
    async def stop_scheduler(self):
        """Parar agendador"""
        self.is_running = False
        logger.info("Agendador de sincronização parado")
    
    def get_scheduled_jobs(self) -> Dict[str, Dict[str, Any]]:
        """Obter jobs agendados"""
        return self.scheduled_jobs.copy()
    
    async def remove_scheduled_job(self, job_id: str) -> bool:
        """Remover job agendado"""
        if job_id in self.scheduled_jobs:
            del self.scheduled_jobs[job_id]
            logger.info(f"Job agendado removido: {job_id}")
            return True
        return False
