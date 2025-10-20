"""
Computer Vision Models - Modelos de visão computacional
Reconhecimento de produtos, análise de preços, detecção de qualidade
"""

import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision.models import resnet50, efficientnet_b0
import cv2
import numpy as np
from PIL import Image
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import json
import base64
from io import BytesIO

logger = logging.getLogger(__name__)

@dataclass
class ProductDetection:
    """Resultado de detecção de produto"""
    product_id: str
    confidence: float
    bbox: Tuple[int, int, int, int]  # x, y, width, height
    category: str
    brand: str
    price: Optional[float] = None
    sustainability_score: Optional[float] = None

@dataclass
class PriceDetection:
    """Resultado de detecção de preço"""
    price: float
    confidence: float
    currency: str
    bbox: Tuple[int, int, int, int]

@dataclass
class QualityAssessment:
    """Resultado de avaliação de qualidade"""
    quality_score: float
    defects: List[str]
    freshness_score: float
    sustainability_indicators: List[str]

class ProductRecognitionModel(nn.Module):
    """Modelo para reconhecimento de produtos"""
    
    def __init__(self, num_classes: int = 1000, pretrained: bool = True):
        super().__init__()
        self.backbone = resnet50(pretrained=pretrained)
        self.backbone.fc = nn.Linear(self.backbone.fc.in_features, num_classes)
        
        # Headers adicionais
        self.brand_classifier = nn.Linear(num_classes, 100)  # 100 marcas
        self.category_classifier = nn.Linear(num_classes, 50)  # 50 categorias
        self.sustainability_classifier = nn.Linear(num_classes, 1)  # Score de sustentabilidade
        
    def forward(self, x):
        features = self.backbone(x)
        
        # Classificação principal
        product_logits = self.backbone.fc(features)
        
        # Classificações secundárias
        brand_logits = self.brand_classifier(features)
        category_logits = self.category_classifier(features)
        sustainability_score = torch.sigmoid(self.sustainability_classifier(features))
        
        return {
            'product_logits': product_logits,
            'brand_logits': brand_logits,
            'category_logits': category_logits,
            'sustainability_score': sustainability_score
        }

class PriceOCRModel(nn.Module):
    """Modelo para OCR de preços"""
    
    def __init__(self):
        super().__init__()
        # Usar EfficientNet como backbone
        self.backbone = efficientnet_b0(pretrained=True)
        self.backbone.classifier = nn.Identity()
        
        # Headers para diferentes tarefas
        self.digit_classifier = nn.Linear(1280, 10)  # Dígitos 0-9
        self.currency_classifier = nn.Linear(1280, 5)  # Moedas (R$, $, €, £, ¥)
        self.price_regressor = nn.Linear(1280, 1)  # Regressão de preço
        
    def forward(self, x):
        features = self.backbone(x)
        
        digit_logits = self.digit_classifier(features)
        currency_logits = self.currency_classifier(features)
        price_value = self.price_regressor(features)
        
        return {
            'digit_logits': digit_logits,
            'currency_logits': currency_logits,
            'price_value': price_value
        }

class QualityAssessmentModel(nn.Module):
    """Modelo para avaliação de qualidade de produtos"""
    
    def __init__(self):
        super().__init__()
        self.backbone = resnet50(pretrained=True)
        self.backbone.fc = nn.Identity()
        
        # Headers para diferentes aspectos de qualidade
        self.quality_regressor = nn.Linear(2048, 1)
        self.freshness_classifier = nn.Linear(2048, 5)  # 5 níveis de frescor
        self.defect_detector = nn.Linear(2048, 10)  # 10 tipos de defeitos
        self.sustainability_analyzer = nn.Linear(2048, 5)  # 5 indicadores de sustentabilidade
        
    def forward(self, x):
        features = self.backbone(x)
        
        quality_score = torch.sigmoid(self.quality_regressor(features))
        freshness_logits = self.freshness_classifier(features)
        defect_logits = torch.sigmoid(self.defect_detector(features))
        sustainability_logits = torch.sigmoid(self.sustainability_analyzer(features))
        
        return {
            'quality_score': quality_score,
            'freshness_logits': freshness_logits,
            'defect_logits': defect_logits,
            'sustainability_logits': sustainability_logits
        }

class ComputerVisionService:
    """Serviço de visão computacional"""
    
    def __init__(self, model_path: str = None, device: str = "cpu"):
        self.device = torch.device(device)
        self.model_path = model_path
        
        # Inicializar modelos
        self.product_model = ProductRecognitionModel()
        self.price_model = PriceOCRModel()
        self.quality_model = QualityAssessmentModel()
        
        # Carregar modelos se disponível
        if model_path:
            self.load_models(model_path)
        
        # Configurar transforms
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        # Mover modelos para device
        self.product_model.to(self.device)
        self.price_model.to(self.device)
        self.quality_model.to(self.device)
        
        # Configurar modo de avaliação
        self.product_model.eval()
        self.price_model.eval()
        self.quality_model.eval()
    
    def load_models(self, model_path: str):
        """Carregar modelos salvos"""
        try:
            checkpoint = torch.load(model_path, map_location=self.device)
            
            if 'product_model' in checkpoint:
                self.product_model.load_state_dict(checkpoint['product_model'])
            
            if 'price_model' in checkpoint:
                self.price_model.load_state_dict(checkpoint['price_model'])
            
            if 'quality_model' in checkpoint:
                self.quality_model.load_state_dict(checkpoint['quality_model'])
            
            logger.info("Modelos carregados com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao carregar modelos: {e}")
    
    def preprocess_image(self, image_data: str) -> torch.Tensor:
        """Pré-processar imagem"""
        try:
            # Decodificar imagem base64
            if image_data.startswith('data:image'):
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_bytes)).convert('RGB')
            
            # Aplicar transforms
            tensor = self.transform(image)
            tensor = tensor.unsqueeze(0)  # Adicionar dimensão de batch
            
            return tensor.to(self.device)
            
        except Exception as e:
            logger.error(f"Erro no pré-processamento: {e}")
            raise
    
    def recognize_products(self, image_data: str) -> List[ProductDetection]:
        """Reconhecer produtos na imagem"""
        try:
            # Pré-processar imagem
            image_tensor = self.preprocess_image(image_data)
            
            # Fazer predição
            with torch.no_grad():
                outputs = self.product_model(image_tensor)
            
            # Processar resultados
            product_logits = outputs['product_logits']
            brand_logits = outputs['brand_logits']
            category_logits = outputs['category_logits']
            sustainability_score = outputs['sustainability_score']
            
            # Obter predições
            product_probs = torch.softmax(product_logits, dim=1)
            brand_probs = torch.softmax(brand_logits, dim=1)
            category_probs = torch.softmax(category_logits, dim=1)
            
            # Criar detecções
            detections = []
            
            # Simular detecção de múltiplos produtos
            for i in range(3):  # Máximo 3 produtos por imagem
                if product_probs[0, i] > 0.1:  # Threshold de confiança
                    detection = ProductDetection(
                        product_id=f"PROD_{i:03d}",
                        confidence=float(product_probs[0, i]),
                        bbox=(100 + i*200, 100 + i*150, 150, 150),  # Bbox simulado
                        category=f"Category_{torch.argmax(category_probs[0]).item()}",
                        brand=f"Brand_{torch.argmax(brand_probs[0]).item()}",
                        sustainability_score=float(sustainability_score[0, 0])
                    )
                    detections.append(detection)
            
            return detections
            
        except Exception as e:
            logger.error(f"Erro no reconhecimento de produtos: {e}")
            return []
    
    def detect_prices(self, image_data: str) -> List[PriceDetection]:
        """Detectar preços na imagem"""
        try:
            # Pré-processar imagem
            image_tensor = self.preprocess_image(image_data)
            
            # Fazer predição
            with torch.no_grad():
                outputs = self.price_model(image_tensor)
            
            # Processar resultados
            digit_logits = outputs['digit_logits']
            currency_logits = outputs['currency_logits']
            price_value = outputs['price_value']
            
            # Obter predições
            digit_probs = torch.softmax(digit_logits, dim=1)
            currency_probs = torch.softmax(currency_logits, dim=1)
            
            # Criar detecções de preço
            detections = []
            
            # Simular detecção de preços
            currencies = ['R$', '$', '€', '£', '¥']
            currency_idx = torch.argmax(currency_probs[0]).item()
            
            detection = PriceDetection(
                price=float(price_value[0, 0]),
                confidence=float(torch.max(currency_probs[0])),
                currency=currencies[currency_idx],
                bbox=(50, 50, 200, 50)  # Bbox simulado
            )
            detections.append(detection)
            
            return detections
            
        except Exception as e:
            logger.error(f"Erro na detecção de preços: {e}")
            return []
    
    def assess_quality(self, image_data: str) -> QualityAssessment:
        """Avaliar qualidade do produto"""
        try:
            # Pré-processar imagem
            image_tensor = self.preprocess_image(image_data)
            
            # Fazer predição
            with torch.no_grad():
                outputs = self.quality_model(image_tensor)
            
            # Processar resultados
            quality_score = outputs['quality_score']
            freshness_logits = outputs['freshness_logits']
            defect_logits = outputs['defect_logits']
            sustainability_logits = outputs['sustainability_logits']
            
            # Obter predições
            freshness_probs = torch.softmax(freshness_logits, dim=1)
            defect_probs = torch.sigmoid(defect_logits)
            sustainability_probs = torch.sigmoid(sustainability_logits)
            
            # Processar defeitos detectados
            defects = []
            defect_names = ['mancha', 'amassado', 'rasgado', 'mofo', 'inseto', 
                           'deformado', 'descolorido', 'machucado', 'sujo', 'danificado']
            
            for i, prob in enumerate(defect_probs[0]):
                if prob > 0.5:
                    defects.append(defect_names[i])
            
            # Processar indicadores de sustentabilidade
            sustainability_indicators = []
            indicator_names = ['orgânico', 'reciclável', 'biodegradável', 'local', 'justo']
            
            for i, prob in enumerate(sustainability_probs[0]):
                if prob > 0.5:
                    sustainability_indicators.append(indicator_names[i])
            
            # Calcular score de frescor
            freshness_score = float(torch.max(freshness_probs[0]))
            
            assessment = QualityAssessment(
                quality_score=float(quality_score[0, 0]),
                defects=defects,
                freshness_score=freshness_score,
                sustainability_indicators=sustainability_indicators
            )
            
            return assessment
            
        except Exception as e:
            logger.error(f"Erro na avaliação de qualidade: {e}")
            return QualityAssessment(
                quality_score=0.0,
                defects=[],
                freshness_score=0.0,
                sustainability_indicators=[]
            )
    
    def analyze_shelf(self, image_data: str) -> Dict[str, Any]:
        """Analisar prateleira completa"""
        try:
            # Reconhecer produtos
            products = self.recognize_products(image_data)
            
            # Detectar preços
            prices = self.detect_prices(image_data)
            
            # Avaliar qualidade
            quality = self.assess_quality(image_data)
            
            # Análise da prateleira
            shelf_analysis = {
                'products_detected': len(products),
                'products': [
                    {
                        'id': p.product_id,
                        'confidence': p.confidence,
                        'category': p.category,
                        'brand': p.brand,
                        'sustainability_score': p.sustainability_score
                    }
                    for p in products
                ],
                'prices_detected': len(prices),
                'prices': [
                    {
                        'price': p.price,
                        'currency': p.currency,
                        'confidence': p.confidence
                    }
                    for p in prices
                ],
                'quality_assessment': {
                    'overall_score': quality.quality_score,
                    'freshness_score': quality.freshness_score,
                    'defects': quality.defects,
                    'sustainability_indicators': quality.sustainability_indicators
                },
                'shelf_metrics': {
                    'product_diversity': len(set(p.category for p in products)),
                    'average_sustainability': np.mean([p.sustainability_score for p in products]) if products else 0,
                    'quality_issues': len(quality.defects),
                    'sustainability_indicators_count': len(quality.sustainability_indicators)
                }
            }
            
            return shelf_analysis
            
        except Exception as e:
            logger.error(f"Erro na análise da prateleira: {e}")
            return {
                'error': str(e),
                'products_detected': 0,
                'products': [],
                'prices_detected': 0,
                'prices': [],
                'quality_assessment': {
                    'overall_score': 0.0,
                    'freshness_score': 0.0,
                    'defects': [],
                    'sustainability_indicators': []
                },
                'shelf_metrics': {
                    'product_diversity': 0,
                    'average_sustainability': 0.0,
                    'quality_issues': 0,
                    'sustainability_indicators_count': 0
                }
            }

