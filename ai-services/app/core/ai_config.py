"""
AI Configuration - Configurações para modelos de IA
Configurações de modelos, treinamento e inferência
"""

import os
from typing import Dict, List, Any, Optional
from pydantic import BaseSettings, Field
from enum import Enum

class ModelType(str, Enum):
    """Tipos de modelos de IA"""
    COMPUTER_VISION = "computer_vision"
    NLP = "nlp"
    ANALYTICS = "analytics"
    RECOMMENDATION = "recommendation"
    OPTIMIZATION = "optimization"

class AIConfig(BaseSettings):
    """Configurações de IA"""
    
    # Configurações gerais
    AI_ENABLED: bool = Field(True, description="Habilitar serviços de IA")
    AI_DEBUG: bool = Field(False, description="Modo debug para IA")
    AI_LOG_LEVEL: str = Field("INFO", description="Nível de log para IA")
    
    # Configurações de modelos
    MODEL_CACHE_SIZE: int = Field(10, description="Tamanho do cache de modelos")
    MODEL_LOAD_TIMEOUT: int = Field(30, description="Timeout para carregar modelos (segundos)")
    MODEL_INFERENCE_TIMEOUT: int = Field(60, description="Timeout para inferência (segundos)")
    
    # Configurações de Computer Vision
    CV_MODEL_PATH: str = Field("./models/cv", description="Caminho dos modelos de CV")
    CV_BATCH_SIZE: int = Field(32, description="Tamanho do lote para CV")
    CV_IMAGE_SIZE: tuple = Field((224, 224), description="Tamanho das imagens")
    CV_CONFIDENCE_THRESHOLD: float = Field(0.5, description="Threshold de confiança para CV")
    
    # Configurações de NLP
    NLP_MODEL_PATH: str = Field("./models/nlp", description="Caminho dos modelos de NLP")
    NLP_MAX_LENGTH: int = Field(512, description="Comprimento máximo do texto")
    NLP_BATCH_SIZE: int = Field(16, description="Tamanho do lote para NLP")
    NLP_CONFIDENCE_THRESHOLD: float = Field(0.7, description="Threshold de confiança para NLP")
    
    # Configurações de Analytics
    ANALYTICS_MODEL_PATH: str = Field("./models/analytics", description="Caminho dos modelos de Analytics")
    ANALYTICS_BATCH_SIZE: int = Field(64, description="Tamanho do lote para Analytics")
    ANALYTICS_PREDICTION_HORIZON: int = Field(30, description="Horizonte de predição (dias)")
    
    # Configurações de treinamento
    TRAINING_DATA_PATH: str = Field("./data/training", description="Caminho dos dados de treinamento")
    TRAINING_RESULTS_PATH: str = Field("./results/training", description="Caminho dos resultados de treinamento")
    TRAINING_BATCH_SIZE: int = Field(32, description="Tamanho do lote para treinamento")
    TRAINING_EPOCHS: int = Field(100, description="Número de épocas de treinamento")
    TRAINING_LEARNING_RATE: float = Field(0.001, description="Taxa de aprendizado")
    TRAINING_VALIDATION_SPLIT: float = Field(0.2, description="Divisão de validação")
    
    # Configurações de GPU
    GPU_ENABLED: bool = Field(False, description="Habilitar GPU")
    GPU_DEVICE_ID: int = Field(0, description="ID do dispositivo GPU")
    GPU_MEMORY_FRACTION: float = Field(0.8, description="Fração de memória GPU a usar")
    
    # Configurações de cache
    CACHE_ENABLED: bool = Field(True, description="Habilitar cache")
    CACHE_TTL: int = Field(3600, description="TTL do cache (segundos)")
    CACHE_MAX_SIZE: int = Field(1000, description="Tamanho máximo do cache")
    
    # Configurações de monitoramento
    MONITORING_ENABLED: bool = Field(True, description="Habilitar monitoramento")
    METRICS_ENABLED: bool = Field(True, description="Habilitar métricas")
    PERFORMANCE_TRACKING: bool = Field(True, description="Habilitar rastreamento de performance")
    
    # Configurações de segurança
    MODEL_ENCRYPTION: bool = Field(False, description="Criptografar modelos")
    API_KEY_REQUIRED: bool = Field(True, description="Requer chave de API")
    RATE_LIMIT_ENABLED: bool = Field(True, description="Habilitar rate limiting")
    RATE_LIMIT_REQUESTS: int = Field(100, description="Limite de requisições por minuto")
    
    # Configurações de deploy
    AUTO_DEPLOY: bool = Field(False, description="Deploy automático de modelos")
    MODEL_VERSIONING: bool = Field(True, description="Versionamento de modelos")
    ROLLBACK_ENABLED: bool = Field(True, description="Habilitar rollback de modelos")
    
    # Configurações de dados
    DATA_VALIDATION: bool = Field(True, description="Validação de dados")
    DATA_PREPROCESSING: bool = Field(True, description="Pré-processamento de dados")
    DATA_AUGMENTATION: bool = Field(True, description="Aumento de dados")
    
    # Configurações de inferência
    INFERENCE_BATCH_SIZE: int = Field(32, description="Tamanho do lote para inferência")
    INFERENCE_TIMEOUT: int = Field(30, description="Timeout para inferência")
    INFERENCE_RETRY_COUNT: int = Field(3, description="Número de tentativas")
    INFERENCE_RETRY_DELAY: int = Field(1, description="Delay entre tentativas (segundos)")
    
    # Configurações de modelos específicos
    MODELS_CONFIG: Dict[str, Dict[str, Any]] = Field(
        default_factory=lambda: {
            "product_recognition": {
                "model_type": "computer_vision",
                "framework": "pytorch",
                "input_size": (3, 224, 224),
                "num_classes": 1000,
                "confidence_threshold": 0.5
            },
            "price_ocr": {
                "model_type": "computer_vision",
                "framework": "pytorch",
                "input_size": (3, 224, 224),
                "num_classes": 10,
                "confidence_threshold": 0.7
            },
            "quality_assessment": {
                "model_type": "computer_vision",
                "framework": "pytorch",
                "input_size": (3, 224, 224),
                "num_classes": 5,
                "confidence_threshold": 0.6
            },
            "sentiment_analysis": {
                "model_type": "nlp",
                "framework": "transformers",
                "model_name": "neuralmind/bert-base-portuguese-cased",
                "max_length": 512,
                "confidence_threshold": 0.7
            },
            "text_classification": {
                "model_type": "nlp",
                "framework": "transformers",
                "model_name": "neuralmind/roberta-base-portuguese-cased",
                "max_length": 512,
                "confidence_threshold": 0.7
            },
            "entity_recognition": {
                "model_type": "nlp",
                "framework": "transformers",
                "model_name": "neuralmind/bert-base-portuguese-cased",
                "max_length": 512,
                "confidence_threshold": 0.6
            },
            "demand_forecasting": {
                "model_type": "analytics",
                "framework": "pytorch",
                "input_size": 10,
                "hidden_size": 64,
                "output_size": 1,
                "confidence_threshold": 0.8
            },
            "sales_analysis": {
                "model_type": "analytics",
                "framework": "sklearn",
                "algorithm": "random_forest",
                "n_estimators": 100,
                "confidence_threshold": 0.8
            },
            "inventory_optimization": {
                "model_type": "analytics",
                "framework": "sklearn",
                "algorithm": "gradient_boosting",
                "n_estimators": 100,
                "confidence_threshold": 0.8
            }
        }
    )
    
    # Configurações de treinamento por modelo
    TRAINING_CONFIG: Dict[str, Dict[str, Any]] = Field(
        default_factory=lambda: {
            "computer_vision": {
                "epochs": 100,
                "batch_size": 32,
                "learning_rate": 0.001,
                "optimizer": "adam",
                "scheduler": "cosine",
                "early_stopping_patience": 10,
                "data_augmentation": True
            },
            "nlp": {
                "epochs": 50,
                "batch_size": 16,
                "learning_rate": 0.00001,
                "optimizer": "adamw",
                "scheduler": "linear",
                "early_stopping_patience": 5,
                "data_augmentation": False
            },
            "analytics": {
                "epochs": 200,
                "batch_size": 64,
                "learning_rate": 0.01,
                "optimizer": "adam",
                "scheduler": "step",
                "early_stopping_patience": 20,
                "data_augmentation": False
            }
        }
    )
    
    # Configurações de validação
    VALIDATION_CONFIG: Dict[str, Any] = Field(
        default_factory=lambda: {
            "cross_validation_folds": 5,
            "test_size": 0.2,
            "random_state": 42,
            "scoring_metrics": ["accuracy", "precision", "recall", "f1", "auc"],
            "validation_threshold": 0.8
        }
    )
    
    # Configurações de deploy
    DEPLOY_CONFIG: Dict[str, Any] = Field(
        default_factory=lambda: {
            "auto_deploy": False,
            "deploy_threshold": 0.85,
            "rollback_threshold": 0.7,
            "monitoring_window": 24,  # horas
            "performance_threshold": 0.8
        }
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Instância global de configuração
ai_config = AIConfig()

def get_ai_config() -> AIConfig:
    """Obter configuração de IA"""
    return ai_config

def update_ai_config(**kwargs) -> None:
    """Atualizar configuração de IA"""
    global ai_config
    for key, value in kwargs.items():
        if hasattr(ai_config, key):
            setattr(ai_config, key, value)

def get_model_config(model_name: str) -> Dict[str, Any]:
    """Obter configuração de um modelo específico"""
    return ai_config.MODELS_CONFIG.get(model_name, {})

def get_training_config(model_type: str) -> Dict[str, Any]:
    """Obter configuração de treinamento para um tipo de modelo"""
    return ai_config.TRAINING_CONFIG.get(model_type, {})

def get_validation_config() -> Dict[str, Any]:
    """Obter configuração de validação"""
    return ai_config.VALIDATION_CONFIG

def get_deploy_config() -> Dict[str, Any]:
    """Obter configuração de deploy"""
    return ai_config.DEPLOY_CONFIG

