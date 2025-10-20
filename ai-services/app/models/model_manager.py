"""
Model Manager - Sistema de gerenciamento de modelos de IA
Versionamento, deploy, monitoramento e atualização de modelos
"""

import os
import json
import logging
import shutil
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import joblib
import torch
import numpy as np
import pandas as pd
from pathlib import Path
import yaml

logger = logging.getLogger(__name__)

class ModelStatus(Enum):
    """Status do modelo"""
    TRAINING = "training"
    TRAINED = "trained"
    VALIDATING = "validating"
    VALIDATED = "validated"
    DEPLOYED = "deployed"
    DEPRECATED = "deprecated"
    FAILED = "failed"

class ModelType(Enum):
    """Tipo do modelo"""
    COMPUTER_VISION = "computer_vision"
    NLP = "nlp"
    ANALYTICS = "analytics"
    RECOMMENDATION = "recommendation"
    OPTIMIZATION = "optimization"

@dataclass
class ModelMetadata:
    """Metadados do modelo"""
    model_id: str
    name: str
    version: str
    model_type: ModelType
    status: ModelStatus
    created_at: datetime
    updated_at: datetime
    description: str
    tags: List[str]
    performance_metrics: Dict[str, float]
    training_data_info: Dict[str, Any]
    model_size: int
    checksum: str
    dependencies: List[str]
    author: str
    environment: str

@dataclass
class ModelVersion:
    """Versão do modelo"""
    version: str
    model_id: str
    created_at: datetime
    status: ModelStatus
    performance_metrics: Dict[str, float]
    model_path: str
    config_path: str
    metadata_path: str

class ModelManager:
    """Gerenciador de modelos de IA"""
    
    def __init__(self, base_path: str = "./models"):
        self.base_path = Path(base_path)
        self.models_path = self.base_path / "models"
        self.versions_path = self.base_path / "versions"
        self.configs_path = self.base_path / "configs"
        self.metadata_path = self.base_path / "metadata"
        
        # Criar diretórios se não existirem
        self._create_directories()
        
        # Cache de modelos
        self.model_cache = {}
        self.metadata_cache = {}
        
        # Carregar metadados existentes
        self._load_metadata()
    
    def _create_directories(self):
        """Criar diretórios necessários"""
        for path in [self.models_path, self.versions_path, self.configs_path, self.metadata_path]:
            path.mkdir(parents=True, exist_ok=True)
    
    def _load_metadata(self):
        """Carregar metadados existentes"""
        try:
            metadata_file = self.metadata_path / "models.json"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    self.metadata_cache = json.load(f)
            else:
                self.metadata_cache = {}
        except Exception as e:
            logger.error(f"Erro ao carregar metadados: {e}")
            self.metadata_cache = {}
    
    def _save_metadata(self):
        """Salvar metadados"""
        try:
            metadata_file = self.metadata_path / "models.json"
            with open(metadata_file, 'w') as f:
                json.dump(self.metadata_cache, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Erro ao salvar metadados: {e}")
    
    def _calculate_checksum(self, file_path: str) -> str:
        """Calcular checksum do arquivo"""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                return hashlib.md5(content).hexdigest()
        except Exception as e:
            logger.error(f"Erro ao calcular checksum: {e}")
            return ""
    
    def register_model(self, model_id: str, name: str, model_type: ModelType, 
                     description: str = "", tags: List[str] = None, 
                     author: str = "system", environment: str = "production") -> str:
        """Registrar novo modelo"""
        try:
            # Gerar versão inicial
            version = "1.0.0"
            
            # Criar metadados
            metadata = ModelMetadata(
                model_id=model_id,
                name=name,
                version=version,
                model_type=model_type,
                status=ModelStatus.TRAINING,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                description=description,
                tags=tags or [],
                performance_metrics={},
                training_data_info={},
                model_size=0,
                checksum="",
                dependencies=[],
                author=author,
                environment=environment
            )
            
            # Salvar metadados
            self.metadata_cache[model_id] = asdict(metadata)
            self._save_metadata()
            
            logger.info(f"Modelo {model_id} registrado com sucesso")
            return model_id
            
        except Exception as e:
            logger.error(f"Erro ao registrar modelo: {e}")
            raise
    
    def save_model(self, model_id: str, model: Any, config: Dict[str, Any] = None,
                  performance_metrics: Dict[str, float] = None) -> str:
        """Salvar modelo"""
        try:
            if model_id not in self.metadata_cache:
                raise ValueError(f"Modelo {model_id} não encontrado")
            
            # Obter versão atual
            current_version = self.metadata_cache[model_id]["version"]
            version_parts = current_version.split(".")
            version_parts[-1] = str(int(version_parts[-1]) + 1)
            new_version = ".".join(version_parts)
            
            # Criar diretório da versão
            version_dir = self.versions_path / model_id / new_version
            version_dir.mkdir(parents=True, exist_ok=True)
            
            # Salvar modelo
            model_path = version_dir / "model.pkl"
            if hasattr(model, 'state_dict'):  # PyTorch model
                torch.save(model.state_dict(), model_path)
            else:  # Scikit-learn model
                joblib.dump(model, model_path)
            
            # Salvar configuração
            if config:
                config_path = version_dir / "config.json"
                with open(config_path, 'w') as f:
                    json.dump(config, f, indent=2)
            
            # Calcular checksum
            checksum = self._calculate_checksum(str(model_path))
            
            # Atualizar metadados
            self.metadata_cache[model_id]["version"] = new_version
            self.metadata_cache[model_id]["updated_at"] = datetime.now()
            self.metadata_cache[model_id]["status"] = ModelStatus.TRAINED.value
            self.metadata_cache[model_id]["model_size"] = os.path.getsize(model_path)
            self.metadata_cache[model_id]["checksum"] = checksum
            
            if performance_metrics:
                self.metadata_cache[model_id]["performance_metrics"] = performance_metrics
            
            # Salvar metadados da versão
            version_metadata = ModelVersion(
                version=new_version,
                model_id=model_id,
                created_at=datetime.now(),
                status=ModelStatus.TRAINED,
                performance_metrics=performance_metrics or {},
                model_path=str(model_path),
                config_path=str(config_path) if config else "",
                metadata_path=str(version_dir / "metadata.json")
            )
            
            version_metadata_path = version_dir / "metadata.json"
            with open(version_metadata_path, 'w') as f:
                json.dump(asdict(version_metadata), f, indent=2, default=str)
            
            self._save_metadata()
            
            logger.info(f"Modelo {model_id} versão {new_version} salvo com sucesso")
            return new_version
            
        except Exception as e:
            logger.error(f"Erro ao salvar modelo: {e}")
            raise
    
    def load_model(self, model_id: str, version: str = None) -> Any:
        """Carregar modelo"""
        try:
            if model_id not in self.metadata_cache:
                raise ValueError(f"Modelo {model_id} não encontrado")
            
            # Usar versão mais recente se não especificada
            if version is None:
                version = self.metadata_cache[model_id]["version"]
            
            # Verificar se modelo está em cache
            cache_key = f"{model_id}_{version}"
            if cache_key in self.model_cache:
                return self.model_cache[cache_key]
            
            # Carregar modelo do disco
            model_path = self.versions_path / model_id / version / "model.pkl"
            if not model_path.exists():
                raise FileNotFoundError(f"Modelo {model_id} versão {version} não encontrado")
            
            # Carregar modelo
            if str(model_path).endswith('.pth'):  # PyTorch model
                model = torch.load(model_path, map_location='cpu')
            else:  # Scikit-learn model
            model = joblib.load(model_path)
            
            # Adicionar ao cache
            self.model_cache[cache_key] = model
            
            logger.info(f"Modelo {model_id} versão {version} carregado com sucesso")
            return model
            
        except Exception as e:
            logger.error(f"Erro ao carregar modelo: {e}")
            raise
    
    def deploy_model(self, model_id: str, version: str = None, environment: str = "production") -> bool:
        """Fazer deploy do modelo"""
        try:
            if model_id not in self.metadata_cache:
                raise ValueError(f"Modelo {model_id} não encontrado")
            
            # Usar versão mais recente se não especificada
            if version is None:
                version = self.metadata_cache[model_id]["version"]
            
            # Verificar se modelo existe
            model_path = self.versions_path / model_id / version / "model.pkl"
            if not model_path.exists():
                raise FileNotFoundError(f"Modelo {model_id} versão {version} não encontrado")
            
            # Criar link simbólico para deploy
            deploy_path = self.models_path / f"{model_id}_deployed.pkl"
            if deploy_path.exists():
                deploy_path.unlink()
            
            shutil.copy2(model_path, deploy_path)
            
            # Atualizar status
            self.metadata_cache[model_id]["status"] = ModelStatus.DEPLOYED.value
            self.metadata_cache[model_id]["environment"] = environment
            self.metadata_cache[model_id]["updated_at"] = datetime.now()
            
            self._save_metadata()
            
            logger.info(f"Modelo {model_id} versão {version} deployado com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao fazer deploy do modelo: {e}")
            return False
    
    def validate_model(self, model_id: str, version: str, test_data: Any, 
                     validation_metrics: Dict[str, float]) -> bool:
        """Validar modelo"""
        try:
            if model_id not in self.metadata_cache:
                raise ValueError(f"Modelo {model_id} não encontrado")
            
            # Atualizar status para validação
            self.metadata_cache[model_id]["status"] = ModelStatus.VALIDATING.value
            self._save_metadata()
            
            # Simular validação
            # Em produção, aqui seria feita a validação real com dados de teste
            await asyncio.sleep(1)  # Simular tempo de validação
            
            # Atualizar métricas de performance
            self.metadata_cache[model_id]["performance_metrics"] = validation_metrics
            self.metadata_cache[model_id]["status"] = ModelStatus.VALIDATED.value
            self.metadata_cache[model_id]["updated_at"] = datetime.now()
            
            self._save_metadata()
            
            logger.info(f"Modelo {model_id} versão {version} validado com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro na validação do modelo: {e}")
            self.metadata_cache[model_id]["status"] = ModelStatus.FAILED.value
            self._save_metadata()
            return False
    
    def get_model_info(self, model_id: str) -> Dict[str, Any]:
        """Obter informações do modelo"""
        try:
            if model_id not in self.metadata_cache:
                raise ValueError(f"Modelo {model_id} não encontrado")
            
            return self.metadata_cache[model_id]
            
        except Exception as e:
            logger.error(f"Erro ao obter informações do modelo: {e}")
            return {}
    
    def list_models(self, model_type: ModelType = None, status: ModelStatus = None) -> List[Dict[str, Any]]:
        """Listar modelos"""
        try:
            models = []
            
            for model_id, metadata in self.metadata_cache.items():
                # Filtrar por tipo se especificado
                if model_type and metadata["model_type"] != model_type.value:
                    continue
                
                # Filtrar por status se especificado
                if status and metadata["status"] != status.value:
                    continue
                
                models.append(metadata)
            
            return models
            
        except Exception as e:
            logger.error(f"Erro ao listar modelos: {e}")
            return []
    
    def get_model_versions(self, model_id: str) -> List[Dict[str, Any]]:
        """Obter versões do modelo"""
        try:
            if model_id not in self.metadata_cache:
                raise ValueError(f"Modelo {model_id} não encontrado")
            
            versions = []
            model_dir = self.versions_path / model_id
            
            if model_dir.exists():
                for version_dir in model_dir.iterdir():
                    if version_dir.is_dir():
                        metadata_file = version_dir / "metadata.json"
                        if metadata_file.exists():
                            with open(metadata_file, 'r') as f:
                                version_data = json.load(f)
                                versions.append(version_data)
            
            # Ordenar por data de criação
            versions.sort(key=lambda x: x["created_at"], reverse=True)
            
            return versions
            
        except Exception as e:
            logger.error(f"Erro ao obter versões do modelo: {e}")
            return []
    
    def deprecate_model(self, model_id: str, version: str = None) -> bool:
        """Deprecar modelo"""
        try:
            if model_id not in self.metadata_cache:
                raise ValueError(f"Modelo {model_id} não encontrado")
            
            # Deprecar versão específica ou todas
            if version:
                # Deprecar versão específica
                version_dir = self.versions_path / model_id / version
                if version_dir.exists():
                    metadata_file = version_dir / "metadata.json"
                    if metadata_file.exists():
                        with open(metadata_file, 'r') as f:
                            version_data = json.load(f)
                        version_data["status"] = ModelStatus.DEPRECATED.value
                        with open(metadata_file, 'w') as f:
                            json.dump(version_data, f, indent=2, default=str)
            else:
                # Deprecar modelo inteiro
                self.metadata_cache[model_id]["status"] = ModelStatus.DEPRECATED.value
                self.metadata_cache[model_id]["updated_at"] = datetime.now()
                self._save_metadata()
            
            logger.info(f"Modelo {model_id} deprecado com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao deprecar modelo: {e}")
            return False
    
    def cleanup_old_versions(self, model_id: str, keep_versions: int = 5) -> bool:
        """Limpar versões antigas do modelo"""
        try:
            if model_id not in self.metadata_cache:
                raise ValueError(f"Modelo {model_id} não encontrado")
            
            versions = self.get_model_versions(model_id)
            
            # Manter apenas as versões mais recentes
            if len(versions) > keep_versions:
                versions_to_remove = versions[keep_versions:]
                
                for version_data in versions_to_remove:
                    version_dir = self.versions_path / model_id / version_data["version"]
                    if version_dir.exists():
                        shutil.rmtree(version_dir)
                        logger.info(f"Versão {version_data['version']} removida")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro na limpeza de versões: {e}")
            return False
    
    def get_model_performance(self, model_id: str) -> Dict[str, Any]:
        """Obter performance do modelo"""
        try:
            if model_id not in self.metadata_cache:
                raise ValueError(f"Modelo {model_id} não encontrado")
            
            metadata = self.metadata_cache[model_id]
            
            performance = {
                'model_id': model_id,
                'current_version': metadata["version"],
                'status': metadata["status"],
                'performance_metrics': metadata["performance_metrics"],
                'last_updated': metadata["updated_at"],
                'model_size': metadata["model_size"],
                'environment': metadata["environment"]
            }
            
            return performance
            
        except Exception as e:
            logger.error(f"Erro ao obter performance do modelo: {e}")
            return {}
    
    def export_model(self, model_id: str, version: str, export_path: str) -> bool:
        """Exportar modelo"""
        try:
            if model_id not in self.metadata_cache:
                raise ValueError(f"Modelo {model_id} não encontrado")
            
            # Caminho do modelo
            model_path = self.versions_path / model_id / version / "model.pkl"
            if not model_path.exists():
                raise FileNotFoundError(f"Modelo {model_id} versão {version} não encontrado")
            
            # Copiar modelo
            shutil.copy2(model_path, export_path)
            
            # Copiar metadados se existir
            metadata_path = self.versions_path / model_id / version / "metadata.json"
            if metadata_path.exists():
                export_metadata_path = export_path.replace('.pkl', '_metadata.json')
                shutil.copy2(metadata_path, export_metadata_path)
            
            logger.info(f"Modelo {model_id} versão {version} exportado para {export_path}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao exportar modelo: {e}")
            return False

