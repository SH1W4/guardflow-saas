"""
Data Mapping - Mapeamento de dados entre diferentes sistemas ERP
Padronização de dados para integração com GuardFlow SaaS
"""

from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)

class ERPType(Enum):
    """Tipos de ERP suportados"""
    SAP = "sap"
    ORACLE = "oracle"
    DYNAMICS = "dynamics"
    TOTVS = "totvs"

class DataMapper:
    """Mapeador de dados entre ERPs e formato padrão GuardFlow"""
    
    def __init__(self, source_erp: ERPType, target_erp: ERPType = None):
        self.source_erp = source_erp
        self.target_erp = target_erp
        self.mapping_rules = self._load_mapping_rules()
    
    def _load_mapping_rules(self) -> Dict[str, Dict[str, str]]:
        """Carregar regras de mapeamento"""
        return {
            "products": {
                "sap": {
                    "id": "material_id",
                    "name": "description",
                    "category": "category",
                    "price": "price",
                    "unit": "unit",
                    "sustainable": "sustainable",
                    "carbon_footprint": "carbon_footprint"
                },
                "oracle": {
                    "id": "item_id",
                    "name": "description",
                    "category": "category",
                    "price": "price",
                    "unit": "unit",
                    "sustainable": "sustainable",
                    "carbon_footprint": "carbon_footprint"
                },
                "dynamics": {
                    "id": "product_id",
                    "name": "name",
                    "category": "category",
                    "price": "price",
                    "unit": "unit",
                    "sustainable": "sustainable",
                    "carbon_footprint": "carbon_footprint"
                },
                "totvs": {
                    "id": "codigo",
                    "name": "descricao",
                    "category": "categoria",
                    "price": "preco",
                    "unit": "unidade",
                    "sustainable": "sustentavel",
                    "carbon_footprint": "pegada_carbono"
                }
            },
            "customers": {
                "sap": {
                    "id": "customer_id",
                    "name": "name",
                    "email": "email",
                    "phone": "phone",
                    "address": "address",
                    "city": "city",
                    "state": "state",
                    "postal_code": "postal_code"
                },
                "oracle": {
                    "id": "customer_id",
                    "name": "name",
                    "email": "email",
                    "phone": "phone",
                    "address": "address",
                    "city": "city",
                    "state": "state",
                    "postal_code": "postal_code"
                },
                "dynamics": {
                    "id": "customer_id",
                    "name": "name",
                    "email": "email",
                    "phone": "phone",
                    "address": "address",
                    "city": "city",
                    "state": "state",
                    "postal_code": "postal_code"
                },
                "totvs": {
                    "id": "cliente_id",
                    "name": "nome",
                    "email": "email",
                    "phone": "telefone",
                    "address": "endereco",
                    "city": "cidade",
                    "state": "estado",
                    "postal_code": "cep"
                }
            },
            "inventory": {
                "sap": {
                    "product_id": "material_id",
                    "store_id": "store_id",
                    "quantity": "quantity",
                    "reserved": "reserved",
                    "available": "available",
                    "location": "location"
                },
                "oracle": {
                    "product_id": "item_id",
                    "store_id": "store_id",
                    "quantity": "quantity",
                    "reserved": "reserved",
                    "available": "available",
                    "location": "location"
                },
                "dynamics": {
                    "product_id": "product_id",
                    "store_id": "store_id",
                    "quantity": "quantity",
                    "reserved": "reserved",
                    "available": "available",
                    "location": "location"
                },
                "totvs": {
                    "product_id": "codigo",
                    "store_id": "loja_id",
                    "quantity": "quantidade",
                    "reserved": "reservado",
                    "available": "disponivel",
                    "location": "localizacao"
                }
            },
            "orders": {
                "sap": {
                    "id": "order_id",
                    "customer_id": "customer_id",
                    "order_date": "order_date",
                    "total_amount": "total_amount",
                    "status": "status",
                    "items": "items"
                },
                "oracle": {
                    "id": "order_id",
                    "customer_id": "customer_id",
                    "order_date": "order_date",
                    "total_amount": "total_amount",
                    "status": "status",
                    "items": "items"
                },
                "dynamics": {
                    "id": "order_id",
                    "customer_id": "customer_id",
                    "order_date": "order_date",
                    "total_amount": "total_amount",
                    "status": "status",
                    "items": "items"
                },
                "totvs": {
                    "id": "pedido_id",
                    "customer_id": "cliente_id",
                    "order_date": "data_pedido",
                    "total_amount": "valor_total",
                    "status": "status",
                    "items": "itens"
                }
            }
        }
    
    def map_products(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Mapear produtos para formato padrão"""
        mapped_products = []
        
        for product in products:
            try:
                mapped_product = self._map_single_product(product)
                mapped_products.append(mapped_product)
            except Exception as e:
                logger.error(f"Erro ao mapear produto: {e}")
                continue
        
        return mapped_products
    
    def _map_single_product(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Mapear um único produto"""
        mapping = self.mapping_rules["products"][self.source_erp.value]
        
        mapped_product = {
            "id": product.get(mapping["id"]),
            "name": product.get(mapping["name"]),
            "category": product.get(mapping["category"]),
            "price": float(product.get(mapping["price"], 0)),
            "unit": product.get(mapping["unit"]),
            "sustainable": bool(product.get(mapping["sustainable"], False)),
            "carbon_footprint": float(product.get(mapping["carbon_footprint"], 0)),
            "source_erp": self.source_erp.value,
            "mapped_at": datetime.now().isoformat()
        }
        
        return mapped_product
    
    def map_customers(self, customers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Mapear clientes para formato padrão"""
        mapped_customers = []
        
        for customer in customers:
            try:
                mapped_customer = self._map_single_customer(customer)
                mapped_customers.append(mapped_customer)
            except Exception as e:
                logger.error(f"Erro ao mapear cliente: {e}")
                continue
        
        return mapped_customers
    
    def _map_single_customer(self, customer: Dict[str, Any]) -> Dict[str, Any]:
        """Mapear um único cliente"""
        mapping = self.mapping_rules["customers"][self.source_erp.value]
        
        mapped_customer = {
            "id": customer.get(mapping["id"]),
            "name": customer.get(mapping["name"]),
            "email": customer.get(mapping["email"]),
            "phone": customer.get(mapping["phone"]),
            "address": customer.get(mapping["address"]),
            "city": customer.get(mapping["city"]),
            "state": customer.get(mapping["state"]),
            "postal_code": customer.get(mapping["postal_code"]),
            "source_erp": self.source_erp.value,
            "mapped_at": datetime.now().isoformat()
        }
        
        return mapped_customer
    
    def map_inventory(self, inventory: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Mapear estoque para formato padrão"""
        mapped_inventory = []
        
        for item in inventory:
            try:
                mapped_item = self._map_single_inventory_item(item)
                mapped_inventory.append(mapped_item)
            except Exception as e:
                logger.error(f"Erro ao mapear item de estoque: {e}")
                continue
        
        return mapped_inventory
    
    def _map_single_inventory_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Mapear um único item de estoque"""
        mapping = self.mapping_rules["inventory"][self.source_erp.value]
        
        mapped_item = {
            "product_id": item.get(mapping["product_id"]),
            "store_id": item.get(mapping["store_id"]),
            "quantity": int(item.get(mapping["quantity"], 0)),
            "reserved": int(item.get(mapping["reserved"], 0)),
            "available": int(item.get(mapping["available"], 0)),
            "location": item.get(mapping["location"]),
            "source_erp": self.source_erp.value,
            "mapped_at": datetime.now().isoformat()
        }
        
        return mapped_item
    
    def map_orders(self, orders: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Mapear pedidos para formato padrão"""
        mapped_orders = []
        
        for order in orders:
            try:
                mapped_order = self._map_single_order(order)
                mapped_orders.append(mapped_order)
            except Exception as e:
                logger.error(f"Erro ao mapear pedido: {e}")
                continue
        
        return mapped_orders
    
    def _map_single_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Mapear um único pedido"""
        mapping = self.mapping_rules["orders"][self.source_erp.value]
        
        mapped_order = {
            "id": order.get(mapping["id"]),
            "customer_id": order.get(mapping["customer_id"]),
            "order_date": order.get(mapping["order_date"]),
            "total_amount": float(order.get(mapping["total_amount"], 0)),
            "status": order.get(mapping["status"]),
            "items": order.get(mapping["items"], []),
            "source_erp": self.source_erp.value,
            "mapped_at": datetime.now().isoformat()
        }
        
        return mapped_order
    
    def reverse_map_products(self, products: List[Dict[str, Any]], target_erp: ERPType) -> List[Dict[str, Any]]:
        """Mapear produtos do formato padrão para ERP específico"""
        reverse_mapped_products = []
        
        for product in products:
            try:
                reverse_mapped_product = self._reverse_map_single_product(product, target_erp)
                reverse_mapped_products.append(reverse_mapped_product)
            except Exception as e:
                logger.error(f"Erro ao mapear produto reverso: {e}")
                continue
        
        return reverse_mapped_products
    
    def _reverse_map_single_product(self, product: Dict[str, Any], target_erp: ERPType) -> Dict[str, Any]:
        """Mapear um único produto do formato padrão para ERP específico"""
        mapping = self.mapping_rules["products"][target_erp.value]
        
        # Criar mapeamento reverso
        reverse_mapping = {v: k for k, v in mapping.items()}
        
        reverse_mapped_product = {}
        for standard_field, erp_field in reverse_mapping.items():
            if standard_field in product:
                reverse_mapped_product[erp_field] = product[standard_field]
        
        return reverse_mapped_product

class DataValidator:
    """Validador de dados mapeados"""
    
    @staticmethod
    def validate_product(product: Dict[str, Any]) -> bool:
        """Validar produto mapeado"""
        required_fields = ["id", "name", "price", "unit"]
        
        for field in required_fields:
            if field not in product or product[field] is None:
                logger.error(f"Campo obrigatório ausente: {field}")
                return False
        
        if product["price"] < 0:
            logger.error("Preço não pode ser negativo")
            return False
        
        return True
    
    @staticmethod
    def validate_customer(customer: Dict[str, Any]) -> bool:
        """Validar cliente mapeado"""
        required_fields = ["id", "name", "email"]
        
        for field in required_fields:
            if field not in customer or customer[field] is None:
                logger.error(f"Campo obrigatório ausente: {field}")
                return False
        
        # Validar email
        if "@" not in customer["email"]:
            logger.error("Email inválido")
            return False
        
        return True
    
    @staticmethod
    def validate_inventory_item(item: Dict[str, Any]) -> bool:
        """Validar item de estoque mapeado"""
        required_fields = ["product_id", "store_id", "quantity"]
        
        for field in required_fields:
            if field not in item or item[field] is None:
                logger.error(f"Campo obrigatório ausente: {field}")
                return False
        
        if item["quantity"] < 0:
            logger.error("Quantidade não pode ser negativa")
            return False
        
        return True
    
    @staticmethod
    def validate_order(order: Dict[str, Any]) -> bool:
        """Validar pedido mapeado"""
        required_fields = ["id", "customer_id", "total_amount"]
        
        for field in required_fields:
            if field not in order or order[field] is None:
                logger.error(f"Campo obrigatório ausente: {field}")
                return False
        
        if order["total_amount"] < 0:
            logger.error("Valor total não pode ser negativo")
            return False
        
        return True

class DataTransformer:
    """Transformador de dados para diferentes formatos"""
    
    @staticmethod
    def to_esg_format(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transformar dados para formato ESG"""
        esg_data = []
        
        for item in data:
            esg_item = {
                "id": item.get("id"),
                "name": item.get("name"),
                "sustainable": item.get("sustainable", False),
                "carbon_footprint": item.get("carbon_footprint", 0),
                "esg_score": DataTransformer._calculate_esg_score(item),
                "environmental_impact": DataTransformer._calculate_environmental_impact(item)
            }
            esg_data.append(esg_item)
        
        return esg_data
    
    @staticmethod
    def _calculate_esg_score(item: Dict[str, Any]) -> float:
        """Calcular score ESG"""
        base_score = 50.0
        
        if item.get("sustainable", False):
            base_score += 30.0
        
        carbon_footprint = item.get("carbon_footprint", 0)
        if carbon_footprint < 0.5:
            base_score += 20.0
        elif carbon_footprint < 1.0:
            base_score += 10.0
        
        return min(base_score, 100.0)
    
    @staticmethod
    def _calculate_environmental_impact(item: Dict[str, Any]) -> Dict[str, Any]:
        """Calcular impacto ambiental"""
        carbon_footprint = item.get("carbon_footprint", 0)
        
        return {
            "carbon_kg": carbon_footprint,
            "water_usage_l": carbon_footprint * 10,  # Estimativa
            "waste_kg": carbon_footprint * 0.1,  # Estimativa
            "renewable_energy": item.get("sustainable", False)
        }

