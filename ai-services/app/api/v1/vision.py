"""
GuardFlow AI Services - Computer Vision API
Serviços de visão computacional para reconhecimento de produtos
"""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional
import cv2
import numpy as np
from PIL import Image
import io
import base64
import logging

from app.core.config import settings
from app.core.models import ModelManager
from app.core.schemas import (
    VisionRecognitionRequest,
    VisionRecognitionResponse,
    ProductDetection,
    OCRResult,
    PriceDetection
)
from app.core.exceptions import AIException, ValidationException

logger = logging.getLogger(__name__)
router = APIRouter()

# Inicializar gerenciador de modelos
model_manager = ModelManager()

@router.post("/recognize", response_model=VisionRecognitionResponse)
async def recognize_products(
    image: UploadFile = File(...),
    confidence_threshold: float = Form(default=0.8),
    model_name: str = Form(default="product_recognition"),
    include_ocr: bool = Form(default=True)
):
    """
    Reconhece produtos em uma imagem
    
    Args:
        image: Imagem para análise
        confidence_threshold: Limiar de confiança (0.0-1.0)
        model_name: Nome do modelo a usar
        include_ocr: Incluir OCR para leitura de preços
    
    Returns:
        Lista de produtos detectados com coordenadas e confiança
    """
    try:
        # Validar arquivo
        if not image.content_type.startswith('image/'):
            raise ValidationException("Arquivo deve ser uma imagem")
        
        # Ler imagem
        image_data = await image.read()
        image_array = np.frombuffer(image_data, np.uint8)
        image_cv = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        if image_cv is None:
            raise ValidationException("Imagem inválida ou corrompida")
        
        # Carregar modelo
        model = await model_manager.get_model(model_name)
        
        # Processar imagem
        results = await process_image(
            image_cv, 
            model, 
            confidence_threshold,
            include_ocr
        )
        
        return VisionRecognitionResponse(
            products=results["products"],
            ocr_results=results.get("ocr", []),
            processing_time=results["processing_time"],
            model_used=model_name,
            confidence_threshold=confidence_threshold
        )
        
    except Exception as e:
        logger.error(f"Erro no reconhecimento de produtos: {str(e)}")
        raise AIException(f"Erro no processamento da imagem: {str(e)}")

@router.post("/detect-prices")
async def detect_prices(
    image: UploadFile = File(...),
    language: str = Form(default="pt")
):
    """
    Detecta e lê preços em uma imagem
    
    Args:
        image: Imagem contendo preços
        language: Idioma para OCR (pt, en, es)
    
    Returns:
        Lista de preços detectados
    """
    try:
        # Ler imagem
        image_data = await image.read()
        image_array = np.frombuffer(image_data, np.uint8)
        image_cv = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        # Processar OCR
        ocr_results = await process_ocr(image_cv, language)
        
        return {
            "prices": ocr_results,
            "language": language,
            "total_detected": len(ocr_results)
        }
        
    except Exception as e:
        logger.error(f"Erro na detecção de preços: {str(e)}")
        raise AIException(f"Erro na detecção de preços: {str(e)}")

@router.post("/analyze-shelf")
async def analyze_shelf(
    image: UploadFile = File(...),
    store_layout: str = Form(default="standard")
):
    """
    Analisa uma prateleira de produtos
    
    Args:
        image: Imagem da prateleira
        store_layout: Layout da loja (standard, corner, endcap)
    
    Returns:
        Análise da prateleira com produtos, preços e disponibilidade
    """
    try:
        # Ler imagem
        image_data = await image.read()
        image_array = np.frombuffer(image_data, np.uint8)
        image_cv = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        # Processar análise da prateleira
        analysis = await process_shelf_analysis(image_cv, store_layout)
        
        return {
            "shelf_analysis": analysis,
            "layout": store_layout,
            "products_count": len(analysis.get("products", [])),
            "availability_score": analysis.get("availability_score", 0.0)
        }
        
    except Exception as e:
        logger.error(f"Erro na análise da prateleira: {str(e)}")
        raise AIException(f"Erro na análise da prateleira: {str(e)}")

@router.get("/models")
async def list_available_models():
    """
    Lista modelos de visão computacional disponíveis
    
    Returns:
        Lista de modelos com suas configurações
    """
    try:
        models = await model_manager.list_vision_models()
        return {
            "models": models,
            "total": len(models)
        }
    except Exception as e:
        logger.error(f"Erro ao listar modelos: {str(e)}")
        raise AIException(f"Erro ao listar modelos: {str(e)}")

# Funções auxiliares
async def process_image(
    image: np.ndarray, 
    model: Any, 
    confidence_threshold: float,
    include_ocr: bool
) -> Dict[str, Any]:
    """Processa imagem com modelo de IA"""
    import time
    start_time = time.time()
    
    # Detectar produtos
    detections = await model.predict(image, confidence_threshold)
    
    # Processar OCR se solicitado
    ocr_results = []
    if include_ocr:
        ocr_results = await process_ocr(image, "pt")
    
    processing_time = time.time() - start_time
    
    return {
        "products": detections,
        "ocr": ocr_results,
        "processing_time": processing_time
    }

async def process_ocr(image: np.ndarray, language: str) -> List[OCRResult]:
    """Processa OCR na imagem"""
    # Implementar OCR usando Tesseract ou Google Vision API
    # Por enquanto, retornar mock
    return [
        OCRResult(
            text="R$ 4,99",
            confidence=0.95,
            bbox=[100, 200, 150, 220],
            language=language
        )
    ]

async def process_shelf_analysis(image: np.ndarray, layout: str) -> Dict[str, Any]:
    """Analisa prateleira de produtos"""
    # Implementar análise de prateleira
    # Por enquanto, retornar mock
    return {
        "products": [
            {
                "name": "Produto 1",
                "price": "R$ 4,99",
                "position": [100, 100, 200, 200],
                "availability": True
            }
        ],
        "availability_score": 0.85,
        "layout_optimization": "good"
    }
