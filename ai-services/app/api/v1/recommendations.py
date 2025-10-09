"""
GuardFlow AI Services - Recommendations API
Sistema de recomendações inteligentes para produtos
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Dict, Any, Optional
import logging

from app.core.config import settings
from app.core.models import ModelManager
from app.core.schemas import (
    ProductRecommendationRequest,
    ProductRecommendationResponse,
    UserRecommendationRequest,
    UserRecommendationResponse,
    SimilarProductsRequest,
    SimilarProductsResponse
)
from app.core.exceptions import AIException, ValidationException

logger = logging.getLogger(__name__)
router = APIRouter()

# Inicializar gerenciador de modelos
model_manager = ModelManager()

@router.post("/products", response_model=ProductRecommendationResponse)
async def recommend_products(request: ProductRecommendationRequest):
    """
    Recomenda produtos baseado em contexto
    
    Args:
        request: Contexto para recomendação (carrinho, histórico, preferências)
    
    Returns:
        Lista de produtos recomendados com scores
    """
    try:
        # Validar contexto
        if not request.context:
            raise ValidationException("Contexto é obrigatório para recomendação")
        
        # Carregar modelo de recomendação
        model = await model_manager.get_model("product_recommendation")
        
        # Processar recomendação
        recommendations = await model.recommend_products(
            context=request.context,
            user_id=request.user_id,
            n_recommendations=request.n_recommendations,
            filters=request.filters
        )
        
        return ProductRecommendationResponse(
            user_id=request.user_id,
            recommendations=recommendations["products"],
            scores=recommendations["scores"],
            reasons=recommendations["reasons"],
            model_used=recommendations["model_used"],
            confidence=recommendations["confidence"]
        )
        
    except Exception as e:
        logger.error(f"Erro na recomendação de produtos: {str(e)}")
        raise AIException(f"Erro na recomendação de produtos: {str(e)}")

@router.post("/user", response_model=UserRecommendationResponse)
async def recommend_for_user(request: UserRecommendationRequest):
    """
    Recomenda produtos para um usuário específico
    
    Args:
        request: Dados do usuário e preferências
    
    Returns:
        Recomendações personalizadas para o usuário
    """
    try:
        # Validar usuário
        if not request.user_id:
            raise ValidationException("user_id é obrigatório")
        
        # Carregar modelo de recomendação personalizada
        model = await model_manager.get_model("user_recommendation")
        
        # Processar recomendação personalizada
        recommendations = await model.recommend_for_user(
            user_id=request.user_id,
            user_profile=request.user_profile,
            purchase_history=request.purchase_history,
            preferences=request.preferences,
            n_recommendations=request.n_recommendations
        )
        
        return UserRecommendationResponse(
            user_id=request.user_id,
            recommendations=recommendations["products"],
            categories=recommendations["categories"],
            personalized_score=recommendations["personalized_score"],
            diversity_score=recommendations["diversity_score"],
            model_used=recommendations["model_used"]
        )
        
    except Exception as e:
        logger.error(f"Erro na recomendação personalizada: {str(e)}")
        raise AIException(f"Erro na recomendação personalizada: {str(e)}")

@router.post("/similar", response_model=SimilarProductsResponse)
async def find_similar_products(request: SimilarProductsRequest):
    """
    Encontra produtos similares a um produto base
    
    Args:
        request: Produto base e critérios de similaridade
    
    Returns:
        Lista de produtos similares
    """
    try:
        # Validar produto base
        if not request.base_product_id:
            raise ValidationException("base_product_id é obrigatório")
        
        # Carregar modelo de similaridade
        model = await model_manager.get_model("product_similarity")
        
        # Processar similaridade
        similar_products = await model.find_similar_products(
            base_product_id=request.base_product_id,
            similarity_type=request.similarity_type,
            n_similar=request.n_similar,
            filters=request.filters
        )
        
        return SimilarProductsResponse(
            base_product_id=request.base_product_id,
            similar_products=similar_products["products"],
            similarity_scores=similar_products["scores"],
            similarity_type=request.similarity_type,
            model_used=similar_products["model_used"]
        )
        
    except Exception as e:
        logger.error(f"Erro na busca de produtos similares: {str(e)}")
        raise AIException(f"Erro na busca de produtos similares: {str(e)}")

@router.post("/cross-sell")
async def cross_sell_recommendations(
    cart_items: List[str],
    user_id: Optional[str] = None,
    n_recommendations: int = 5
):
    """
    Recomendações de cross-sell baseadas no carrinho
    
    Args:
        cart_items: Itens no carrinho
        user_id: ID do usuário (opcional)
        n_recommendations: Número de recomendações
    
    Returns:
        Recomendações de cross-sell
    """
    try:
        # Validar carrinho
        if not cart_items or len(cart_items) == 0:
            raise ValidationException("Carrinho não pode estar vazio")
        
        # Carregar modelo de cross-sell
        model = await model_manager.get_model("cross_sell")
        
        # Processar cross-sell
        recommendations = await model.cross_sell_recommendations(
            cart_items=cart_items,
            user_id=user_id,
            n_recommendations=n_recommendations
        )
        
        return {
            "cart_items": cart_items,
            "cross_sell_recommendations": recommendations["products"],
            "scores": recommendations["scores"],
            "reasons": recommendations["reasons"],
            "total_recommendations": len(recommendations["products"])
        }
        
    except Exception as e:
        logger.error(f"Erro nas recomendações de cross-sell: {str(e)}")
        raise AIException(f"Erro nas recomendações de cross-sell: {str(e)}")

@router.post("/upsell")
async def upsell_recommendations(
    product_id: str,
    user_id: Optional[str] = None,
    n_recommendations: int = 3
):
    """
    Recomendações de upsell para um produto
    
    Args:
        product_id: ID do produto
        user_id: ID do usuário (opcional)
        n_recommendations: Número de recomendações
    
    Returns:
        Recomendações de upsell
    """
    try:
        # Validar produto
        if not product_id:
            raise ValidationException("product_id é obrigatório")
        
        # Carregar modelo de upsell
        model = await model_manager.get_model("upsell")
        
        # Processar upsell
        recommendations = await model.upsell_recommendations(
            product_id=product_id,
            user_id=user_id,
            n_recommendations=n_recommendations
        )
        
        return {
            "base_product_id": product_id,
            "upsell_recommendations": recommendations["products"],
            "scores": recommendations["scores"],
            "price_differences": recommendations["price_differences"],
            "total_recommendations": len(recommendations["products"])
        }
        
    except Exception as e:
        logger.error(f"Erro nas recomendações de upsell: {str(e)}")
        raise AIException(f"Erro nas recomendações de upsell: {str(e)}")

@router.get("/trending")
async def get_trending_products(
    category: Optional[str] = Query(None),
    period_days: int = Query(default=7),
    n_products: int = Query(default=10)
):
    """
    Produtos em tendência
    
    Args:
        category: Categoria de produtos
        period_days: Período em dias
        n_products: Número de produtos
    
    Returns:
        Lista de produtos em tendência
    """
    try:
        # Carregar modelo de tendências
        model = await model_manager.get_model("trending_products")
        
        # Processar tendências
        trending = await model.get_trending_products(
            category=category,
            period_days=period_days,
            n_products=n_products
        )
        
        return {
            "trending_products": trending["products"],
            "trend_scores": trending["scores"],
            "category": category,
            "period_days": period_days,
            "total_products": len(trending["products"])
        }
        
    except Exception as e:
        logger.error(f"Erro nas tendências: {str(e)}")
        raise AIException(f"Erro nas tendências: {str(e)}")

@router.get("/models/recommendation")
async def list_recommendation_models():
    """
    Lista modelos de recomendação disponíveis
    
    Returns:
        Lista de modelos com suas configurações
    """
    try:
        models = await model_manager.list_recommendation_models()
        return {
            "models": models,
            "total": len(models)
        }
    except Exception as e:
        logger.error(f"Erro ao listar modelos de recomendação: {str(e)}")
        raise AIException(f"Erro ao listar modelos de recomendação: {str(e)}")

@router.post("/feedback")
async def submit_recommendation_feedback(
    recommendation_id: str,
    user_id: str,
    feedback_type: str,  # "positive", "negative", "neutral"
    rating: Optional[int] = None,
    comments: Optional[str] = None
):
    """
    Envia feedback sobre recomendações
    
    Args:
        recommendation_id: ID da recomendação
        user_id: ID do usuário
        feedback_type: Tipo de feedback
        rating: Avaliação (1-5)
        comments: Comentários adicionais
    
    Returns:
        Confirmação do feedback
    """
    try:
        # Validar feedback
        if feedback_type not in ["positive", "negative", "neutral"]:
            raise ValidationException("feedback_type deve ser 'positive', 'negative' ou 'neutral'")
        
        if rating and (rating < 1 or rating > 5):
            raise ValidationException("rating deve estar entre 1 e 5")
        
        # Processar feedback
        result = await model_manager.submit_feedback(
            recommendation_id=recommendation_id,
            user_id=user_id,
            feedback_type=feedback_type,
            rating=rating,
            comments=comments
        )
        
        return {
            "status": "success",
            "feedback_id": result["feedback_id"],
            "message": "Feedback registrado com sucesso"
        }
        
    except Exception as e:
        logger.error(f"Erro no feedback: {str(e)}")
        raise AIException(f"Erro no feedback: {str(e)}")
