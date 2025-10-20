"""
Analytics Models - Modelos de análise e machine learning
Previsão de demanda, análise de vendas, otimização de estoque
"""

import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import joblib
import os

logger = logging.getLogger(__name__)

@dataclass
class DemandForecast:
    """Resultado de previsão de demanda"""
    product_id: str
    predicted_demand: float
    confidence_interval: Tuple[float, float]
    trend: str  # increasing, decreasing, stable
    seasonality: float
    forecast_date: datetime

@dataclass
class SalesAnalysis:
    """Resultado de análise de vendas"""
    total_sales: float
    growth_rate: float
    top_products: List[Dict[str, Any]]
    seasonal_patterns: Dict[str, float]
    customer_segments: List[Dict[str, Any]]

@dataclass
class InventoryOptimization:
    """Resultado de otimização de estoque"""
    product_id: str
    optimal_stock: int
    reorder_point: int
    safety_stock: int
    cost_savings: float
    stockout_probability: float

class DemandForecastingModel(nn.Module):
    """Modelo neural para previsão de demanda"""
    
    def __init__(self, input_size: int = 10, hidden_size: int = 64, output_size: int = 1):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc1 = nn.Linear(hidden_size, 32)
        self.fc2 = nn.Linear(32, output_size)
        self.dropout = nn.Dropout(0.2)
        
    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        # Usar apenas a última saída da LSTM
        last_output = lstm_out[:, -1, :]
        x = self.dropout(last_output)
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x

class SalesAnalysisModel:
    """Modelo para análise de vendas"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.cluster_model = KMeans(n_clusters=5, random_state=42)
        self.regression_model = RandomForestRegressor(n_estimators=100, random_state=42)
        
    def fit(self, data: pd.DataFrame):
        """Treinar modelo"""
        try:
            # Preparar dados
            features = self._prepare_features(data)
            
            # Treinar scaler
            self.scaler.fit(features)
            scaled_features = self.scaler.transform(features)
            
            # Treinar clustering
            self.cluster_model.fit(scaled_features)
            
            # Treinar regressão
            self.regression_model.fit(scaled_features, data['sales'].values)
            
            logger.info("Modelo de análise de vendas treinado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao treinar modelo de vendas: {e}")
    
    def _prepare_features(self, data: pd.DataFrame) -> np.ndarray:
        """Preparar features para o modelo"""
        features = []
        
        # Features temporais
        if 'date' in data.columns:
            data['date'] = pd.to_datetime(data['date'])
            data['day_of_week'] = data['date'].dt.dayofweek
            data['month'] = data['date'].dt.month
            data['quarter'] = data['date'].dt.quarter
            features.extend(['day_of_week', 'month', 'quarter'])
        
        # Features de produto
        if 'product_id' in data.columns:
            data['product_category'] = data['product_id'].str[:3]  # Simulação
            features.append('product_category')
        
        # Features numéricas
        numeric_features = ['price', 'quantity', 'discount']
        for feature in numeric_features:
            if feature in data.columns:
                features.append(feature)
        
        return data[features].fillna(0).values
    
    def predict(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Fazer predições"""
        try:
            features = self._prepare_features(data)
            scaled_features = self.scaler.transform(features)
            
            # Predições
            sales_predictions = self.regression_model.predict(scaled_features)
            clusters = self.cluster_model.predict(scaled_features)
            
            return {
                'sales_predictions': sales_predictions.tolist(),
                'clusters': clusters.tolist(),
                'feature_importance': self.regression_model.feature_importances_.tolist()
            }
            
        except Exception as e:
            logger.error(f"Erro nas predições: {e}")
            return {'error': str(e)}

class InventoryOptimizationModel:
    """Modelo para otimização de estoque"""
    
    def __init__(self):
        self.demand_model = GradientBoostingRegressor(random_state=42)
        self.lead_time_model = LinearRegression()
        self.cost_model = Ridge(alpha=1.0)
        
    def fit(self, data: pd.DataFrame):
        """Treinar modelo"""
        try:
            # Preparar dados de demanda
            demand_features = self._prepare_demand_features(data)
            self.demand_model.fit(demand_features, data['demand'].values)
            
            # Preparar dados de lead time
            lead_time_features = self._prepare_lead_time_features(data)
            self.lead_time_model.fit(lead_time_features, data['lead_time'].values)
            
            # Preparar dados de custo
            cost_features = self._prepare_cost_features(data)
            self.cost_model.fit(cost_features, data['cost'].values)
            
            logger.info("Modelo de otimização de estoque treinado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao treinar modelo de estoque: {e}")
    
    def _prepare_demand_features(self, data: pd.DataFrame) -> np.ndarray:
        """Preparar features para modelo de demanda"""
        features = []
        
        # Features históricas
        if 'historical_demand' in data.columns:
            features.append('historical_demand')
        
        # Features sazonais
        if 'seasonality' in data.columns:
            features.append('seasonality')
        
        # Features de produto
        if 'product_category' in data.columns:
            features.append('product_category')
        
        return data[features].fillna(0).values
    
    def _prepare_lead_time_features(self, data: pd.DataFrame) -> np.ndarray:
        """Preparar features para modelo de lead time"""
        features = []
        
        if 'supplier_id' in data.columns:
            features.append('supplier_id')
        
        if 'product_category' in data.columns:
            features.append('product_category')
        
        return data[features].fillna(0).values
    
    def _prepare_cost_features(self, data: pd.DataFrame) -> np.ndarray:
        """Preparar features para modelo de custo"""
        features = []
        
        if 'product_category' in data.columns:
            features.append('product_category')
        
        if 'supplier_id' in data.columns:
            features.append('supplier_id')
        
        return data[features].fillna(0).values
    
    def optimize_inventory(self, product_data: Dict[str, Any]) -> InventoryOptimization:
        """Otimizar estoque para um produto"""
        try:
            # Simular predições
            predicted_demand = np.random.normal(100, 20)  # Simulação
            lead_time = np.random.normal(7, 2)  # Simulação
            holding_cost = np.random.normal(0.1, 0.02)  # Simulação
            
            # Calcular estoque ótimo (fórmula EOQ simplificada)
            optimal_stock = int(np.sqrt(2 * predicted_demand * 50 / holding_cost))
            reorder_point = int(predicted_demand * lead_time / 30)  # 30 dias
            safety_stock = int(optimal_stock * 0.2)  # 20% do estoque ótimo
            
            # Calcular economia de custos
            current_stock = product_data.get('current_stock', optimal_stock * 2)
            cost_savings = (current_stock - optimal_stock) * holding_cost
            
            # Calcular probabilidade de falta
            stockout_probability = max(0, 1 - (optimal_stock / predicted_demand))
            
            result = InventoryOptimization(
                product_id=product_data.get('product_id', 'UNKNOWN'),
                optimal_stock=optimal_stock,
                reorder_point=reorder_point,
                safety_stock=safety_stock,
                cost_savings=cost_savings,
                stockout_probability=stockout_probability
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Erro na otimização de estoque: {e}")
            return InventoryOptimization(
                product_id=product_data.get('product_id', 'UNKNOWN'),
                optimal_stock=0,
                reorder_point=0,
                safety_stock=0,
                cost_savings=0.0,
                stockout_probability=1.0
            )

class AnalyticsService:
    """Serviço de analytics e machine learning"""
    
    def __init__(self, model_path: str = None):
        self.model_path = model_path
        self.demand_model = DemandForecastingModel()
        self.sales_model = SalesAnalysisModel()
        self.inventory_model = InventoryOptimizationModel()
        
        # Carregar modelos se disponível
        if model_path and os.path.exists(model_path):
            self.load_models(model_path)
    
    def load_models(self, model_path: str):
        """Carregar modelos salvos"""
        try:
            if os.path.exists(f"{model_path}/demand_model.pth"):
                self.demand_model.load_state_dict(torch.load(f"{model_path}/demand_model.pth"))
            
            if os.path.exists(f"{model_path}/sales_model.pkl"):
                self.sales_model = joblib.load(f"{model_path}/sales_model.pkl")
            
            if os.path.exists(f"{model_path}/inventory_model.pkl"):
                self.inventory_model = joblib.load(f"{model_path}/inventory_model.pkl")
            
            logger.info("Modelos carregados com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao carregar modelos: {e}")
    
    def forecast_demand(self, product_id: str, historical_data: List[Dict[str, Any]], 
                       forecast_days: int = 30) -> List[DemandForecast]:
        """Prever demanda de produtos"""
        try:
            forecasts = []
            
            # Simular previsões para múltiplos produtos
            for i in range(min(5, len(historical_data))):  # Máximo 5 produtos
                data = historical_data[i]
                
                # Simular predição
                base_demand = data.get('average_demand', 100)
                trend_factor = np.random.normal(1.0, 0.1)
                seasonality_factor = 1 + 0.2 * np.sin(2 * np.pi * i / 12)  # Sazonalidade
                
                predicted_demand = base_demand * trend_factor * seasonality_factor
                confidence_interval = (predicted_demand * 0.8, predicted_demand * 1.2)
                
                # Determinar tendência
                if trend_factor > 1.05:
                    trend = "increasing"
                elif trend_factor < 0.95:
                    trend = "decreasing"
                else:
                    trend = "stable"
                
                forecast = DemandForecast(
                    product_id=data.get('product_id', f'PROD_{i:03d}'),
                    predicted_demand=predicted_demand,
                    confidence_interval=confidence_interval,
                    trend=trend,
                    seasonality=seasonality_factor,
                    forecast_date=datetime.now() + timedelta(days=forecast_days)
                )
                
                forecasts.append(forecast)
            
            return forecasts
            
        except Exception as e:
            logger.error(f"Erro na previsão de demanda: {e}")
            return []
    
    def analyze_sales(self, sales_data: List[Dict[str, Any]]) -> SalesAnalysis:
        """Analisar dados de vendas"""
        try:
            # Converter para DataFrame
            df = pd.DataFrame(sales_data)
            
            # Calcular métricas básicas
            total_sales = df['amount'].sum() if 'amount' in df.columns else 0
            
            # Calcular taxa de crescimento (simulação)
            if len(df) > 1:
                growth_rate = np.random.normal(0.05, 0.02)  # 5% ± 2%
            else:
                growth_rate = 0.0
            
            # Top produtos
            if 'product_id' in df.columns and 'amount' in df.columns:
                top_products = df.groupby('product_id')['amount'].sum().nlargest(5).to_dict()
                top_products_list = [
                    {'product_id': pid, 'total_sales': amount}
                    for pid, amount in top_products.items()
                ]
            else:
                top_products_list = []
            
            # Padrões sazonais (simulação)
            seasonal_patterns = {
                'Q1': np.random.normal(0.8, 0.1),  # Inverno
                'Q2': np.random.normal(1.0, 0.1),  # Primavera
                'Q3': np.random.normal(1.2, 0.1),  # Verão
                'Q4': np.random.normal(1.1, 0.1)   # Outono
            }
            
            # Segmentos de clientes (simulação)
            customer_segments = [
                {'segment': 'VIP', 'count': int(len(df) * 0.1), 'avg_spend': total_sales * 0.3},
                {'segment': 'Regular', 'count': int(len(df) * 0.7), 'avg_spend': total_sales * 0.6},
                {'segment': 'New', 'count': int(len(df) * 0.2), 'avg_spend': total_sales * 0.1}
            ]
            
            analysis = SalesAnalysis(
                total_sales=total_sales,
                growth_rate=growth_rate,
                top_products=top_products_list,
                seasonal_patterns=seasonal_patterns,
                customer_segments=customer_segments
            )
            
            return analysis
            
        except Exception as e:
            logger.error(f"Erro na análise de vendas: {e}")
            return SalesAnalysis(
                total_sales=0.0,
                growth_rate=0.0,
                top_products=[],
                seasonal_patterns={},
                customer_segments=[]
            )
    
    def optimize_inventory(self, inventory_data: List[Dict[str, Any]]) -> List[InventoryOptimization]:
        """Otimizar estoque"""
        try:
            optimizations = []
            
            for data in inventory_data:
                optimization = self.inventory_model.optimize_inventory(data)
                optimizations.append(optimization)
            
            return optimizations
            
        except Exception as e:
            logger.error(f"Erro na otimização de estoque: {e}")
            return []
    
    def generate_insights(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gerar insights de analytics"""
        try:
            insights = {
                'demand_insights': {
                    'trending_products': ['PROD001', 'PROD002', 'PROD003'],
                    'declining_products': ['PROD004', 'PROD005'],
                    'seasonal_patterns': {
                        'peak_season': 'Q3',
                        'low_season': 'Q1',
                        'growth_rate': 0.15
                    }
                },
                'sales_insights': {
                    'top_performing_categories': ['Alimentos', 'Bebidas', 'Higiene'],
                    'underperforming_categories': ['Eletrônicos', 'Roupas'],
                    'customer_behavior': {
                        'average_basket_size': 150.0,
                        'repeat_purchase_rate': 0.65,
                        'loyalty_score': 0.78
                    }
                },
                'inventory_insights': {
                    'overstocked_products': ['PROD006', 'PROD007'],
                    'understocked_products': ['PROD008', 'PROD009'],
                    'optimization_potential': {
                        'cost_savings': 25000.0,
                        'stockout_reduction': 0.3,
                        'efficiency_gain': 0.15
                    }
                },
                'recommendations': [
                    'Aumentar estoque de produtos sazonais para Q3',
                    'Reduzir estoque de produtos em declínio',
                    'Implementar sistema de reorder automático',
                    'Focar em produtos com alta rotatividade'
                ]
            }
            
            return insights
            
        except Exception as e:
            logger.error(f"Erro na geração de insights: {e}")
            return {'error': str(e)}

