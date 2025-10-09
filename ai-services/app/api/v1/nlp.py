"""
GuardFlow AI Services - Natural Language Processing API
Serviços de processamento de linguagem natural
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Dict, Any, Optional
import logging

from app.core.config import settings
from app.core.models import ModelManager
from app.core.schemas import (
    SentimentAnalysisRequest,
    SentimentAnalysisResponse,
    TextClassificationRequest,
    TextClassificationResponse,
    LanguageDetectionRequest,
    LanguageDetectionResponse,
    TextSummarizationRequest,
    TextSummarizationResponse
)
from app.core.exceptions import AIException, ValidationException

logger = logging.getLogger(__name__)
router = APIRouter()

# Inicializar gerenciador de modelos
model_manager = ModelManager()

@router.post("/sentiment", response_model=SentimentAnalysisResponse)
async def analyze_sentiment(request: SentimentAnalysisRequest):
    """
    Análise de sentimento em texto
    
    Args:
        request: Texto para análise e configurações
    
    Returns:
        Análise de sentimento com scores e confiança
    """
    try:
        # Validar texto
        if not request.text or len(request.text.strip()) == 0:
            raise ValidationException("Texto não pode estar vazio")
        
        if len(request.text) > 10000:
            raise ValidationException("Texto muito longo (máximo 10000 caracteres)")
        
        # Carregar modelo de sentimento
        model = await model_manager.get_model("sentiment_analysis")
        
        # Processar texto
        result = await model.analyze_sentiment(
            request.text,
            language=request.language,
            model_name=request.model_name
        )
        
        return SentimentAnalysisResponse(
            text=request.text,
            sentiment=result["sentiment"],
            confidence=result["confidence"],
            scores=result["scores"],
            language=result["language"],
            model_used=result["model_used"]
        )
        
    except Exception as e:
        logger.error(f"Erro na análise de sentimento: {str(e)}")
        raise AIException(f"Erro na análise de sentimento: {str(e)}")

@router.post("/classify", response_model=TextClassificationResponse)
async def classify_text(request: TextClassificationRequest):
    """
    Classificação de texto em categorias
    
    Args:
        request: Texto e categorias para classificação
    
    Returns:
        Classificação do texto com probabilidades
    """
    try:
        # Validar texto
        if not request.text or len(request.text.strip()) == 0:
            raise ValidationException("Texto não pode estar vazio")
        
        # Carregar modelo de classificação
        model = await model_manager.get_model("text_classification")
        
        # Processar classificação
        result = await model.classify_text(
            request.text,
            categories=request.categories,
            language=request.language
        )
        
        return TextClassificationResponse(
            text=request.text,
            predicted_category=result["category"],
            confidence=result["confidence"],
            all_scores=result["all_scores"],
            language=result["language"]
        )
        
    except Exception as e:
        logger.error(f"Erro na classificação de texto: {str(e)}")
        raise AIException(f"Erro na classificação de texto: {str(e)}")

@router.post("/detect-language", response_model=LanguageDetectionResponse)
async def detect_language(request: LanguageDetectionRequest):
    """
    Detecção automática de idioma
    
    Args:
        request: Texto para detecção de idioma
    
    Returns:
        Idioma detectado com confiança
    """
    try:
        # Validar texto
        if not request.text or len(request.text.strip()) == 0:
            raise ValidationException("Texto não pode estar vazio")
        
        # Carregar modelo de detecção de idioma
        model = await model_manager.get_model("language_detection")
        
        # Processar detecção
        result = await model.detect_language(request.text)
        
        return LanguageDetectionResponse(
            text=request.text,
            language=result["language"],
            confidence=result["confidence"],
            alternative_languages=result["alternatives"]
        )
        
    except Exception as e:
        logger.error(f"Erro na detecção de idioma: {str(e)}")
        raise AIException(f"Erro na detecção de idioma: {str(e)}")

@router.post("/summarize", response_model=TextSummarizationResponse)
async def summarize_text(request: TextSummarizationRequest):
    """
    Sumarização automática de texto
    
    Args:
        request: Texto para sumarização e configurações
    
    Returns:
        Resumo do texto com métricas
    """
    try:
        # Validar texto
        if not request.text or len(request.text.strip()) == 0:
            raise ValidationException("Texto não pode estar vazio")
        
        if len(request.text) < 100:
            raise ValidationException("Texto muito curto para sumarização (mínimo 100 caracteres)")
        
        # Carregar modelo de sumarização
        model = await model_manager.get_model("text_summarization")
        
        # Processar sumarização
        result = await model.summarize_text(
            request.text,
            max_length=request.max_length,
            min_length=request.min_length,
            language=request.language
        )
        
        return TextSummarizationResponse(
            original_text=request.text,
            summary=result["summary"],
            compression_ratio=result["compression_ratio"],
            key_points=result["key_points"],
            language=result["language"]
        )
        
    except Exception as e:
        logger.error(f"Erro na sumarização: {str(e)}")
        raise AIException(f"Erro na sumarização: {str(e)}")

@router.post("/extract-entities")
async def extract_entities(
    text: str,
    entity_types: Optional[List[str]] = None,
    language: str = "pt"
):
    """
    Extração de entidades nomeadas do texto
    
    Args:
        text: Texto para extração
        entity_types: Tipos de entidades a extrair
        language: Idioma do texto
    
    Returns:
        Lista de entidades extraídas
    """
    try:
        # Validar texto
        if not text or len(text.strip()) == 0:
            raise ValidationException("Texto não pode estar vazio")
        
        # Carregar modelo de extração de entidades
        model = await model_manager.get_model("entity_extraction")
        
        # Processar extração
        result = await model.extract_entities(
            text,
            entity_types=entity_types,
            language=language
        )
        
        return {
            "text": text,
            "entities": result["entities"],
            "total_entities": len(result["entities"]),
            "entity_types": result["entity_types"],
            "language": language
        }
        
    except Exception as e:
        logger.error(f"Erro na extração de entidades: {str(e)}")
        raise AIException(f"Erro na extração de entidades: {str(e)}")

@router.post("/translate")
async def translate_text(
    text: str,
    target_language: str,
    source_language: Optional[str] = None
):
    """
    Tradução automática de texto
    
    Args:
        text: Texto para tradução
        target_language: Idioma de destino
        source_language: Idioma de origem (opcional)
    
    Returns:
        Texto traduzido com metadados
    """
    try:
        # Validar texto
        if not text or len(text.strip()) == 0:
            raise ValidationException("Texto não pode estar vazio")
        
        # Carregar modelo de tradução
        model = await model_manager.get_model("translation")
        
        # Processar tradução
        result = await model.translate_text(
            text,
            target_language=target_language,
            source_language=source_language
        )
        
        return {
            "original_text": text,
            "translated_text": result["translated_text"],
            "source_language": result["source_language"],
            "target_language": target_language,
            "confidence": result["confidence"]
        }
        
    except Exception as e:
        logger.error(f"Erro na tradução: {str(e)}")
        raise AIException(f"Erro na tradução: {str(e)}")

@router.get("/supported-languages")
async def get_supported_languages():
    """
    Lista idiomas suportados pelos modelos
    
    Returns:
        Lista de idiomas com códigos e nomes
    """
    try:
        languages = await model_manager.get_supported_languages()
        return {
            "languages": languages,
            "total": len(languages)
        }
    except Exception as e:
        logger.error(f"Erro ao listar idiomas: {str(e)}")
        raise AIException(f"Erro ao listar idiomas: {str(e)}")

@router.get("/models/nlp")
async def list_nlp_models():
    """
    Lista modelos de NLP disponíveis
    
    Returns:
        Lista de modelos com suas configurações
    """
    try:
        models = await model_manager.list_nlp_models()
        return {
            "models": models,
            "total": len(models)
        }
    except Exception as e:
        logger.error(f"Erro ao listar modelos NLP: {str(e)}")
        raise AIException(f"Erro ao listar modelos NLP: {str(e)}")
