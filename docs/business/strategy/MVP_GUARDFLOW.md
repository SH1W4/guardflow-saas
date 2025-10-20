# GuardFlow MVP - "Agiliza aí" em 90 Dias

## 🎯 Visão Geral do MVP

### **Objetivo:**
Criar um **MVP funcional** do GuardFlow em **90 dias** para validar com supermercados parceiros e demonstrar superioridade competitiva.

### **Slogan MVP:**
**"GuardFlow - Agiliza aí suas compras!"**

### **Core Features (Mínimo Viável):**
- ✅ **Scanner de produtos** via câmera do celular
- ✅ **Checkout inteligente** com carrinho virtual
- ✅ **Pagamento PIX** integrado
- ✅ **Interface "Agiliza aí"** brasileira e intuitiva
- ✅ **Integração GuardPass** (simulada para MVP)
- ✅ **Dashboard supermercado** básico

## 🏗️ Arquitetura Técnica MVP

### **Stack Tecnológico Escolhido:**
```
Frontend Mobile:
├── React Native 0.72+ (cross-platform)
├── TypeScript (type safety)
├── Expo (desenvolvimento ágil)
├── React Navigation (navegação)
└── Redux Toolkit (estado global)

Backend API:
├── FastAPI (Python 3.11+)
├── PostgreSQL (banco principal)
├── Redis (cache/sessions)
├── Docker (containerização)
└── AWS/Railway (deploy rápido)

Computer Vision:
├── Google Vision API (reconhecimento produtos)
├── OpenCV (processamento imagem)
├── TensorFlow Lite (IA mobile)
└── Barcode scanning nativo

Pagamentos:
├── PIX via Mercado Pago API
├── Simulador GuardPass Pay
├── Webhook notifications
└── Reconciliação automática

Infraestrutura:
├── AWS EC2/RDS (produção)
├── Railway (desenvolvimento)
├── GitHub Actions (CI/CD)
└── Sentry (monitoramento)
```

### **Diagrama de Arquitetura:**
```
[App Mobile GuardFlow] 
       ↕ (HTTPS/REST)
[Load Balancer]
       ↕
[FastAPI Backend]
   ↕        ↕        ↕
[PostgreSQL] [Redis] [Google Vision API]
   ↕
[Mercado Pago API] ← PIX
   ↕
[GuardPass Simulator] ← Auth/ESG
```

## 📱 App Mobile - GuardFlow

### **Estrutura de Telas:**
```
GuardFlow App Structure:
├── 🔐 Login/Auth
│   ├── SplashScreen
│   ├── LoginScreen (GuardPass)
│   └── OnboardingScreen
├── 🏠 Home/Scanner
│   ├── ScannerScreen (principal)
│   ├── ProductListScreen
│   └── CartScreen
├── 💳 Checkout
│   ├── CheckoutScreen
│   ├── PaymentScreen
│   └── SuccessScreen
├── 👤 Profile
│   ├── ProfileScreen
│   ├── HistoryScreen
│   └── SettingsScreen
└── 🏪 Supermarket
    ├── StoreSelectScreen
    └── StoreInfoScreen
```

### **Fluxo Principal (Happy Path):**
```
1. 🔐 Login com GuardPass
   "Agiliza aí! Entre com sua conta"

2. 🏪 Selecionar Supermercado
   "Qual supermercado vamos agilizar hoje?"

3. 📱 Ativar Scanner
   "Aponte a câmera e agilize suas compras!"

4. 🛒 Escanear Produtos
   "Produto reconhecido! Agilizou mais um!"

5. 💳 Checkout Rápido
   "Agilizando seu pagamento via PIX..."

6. ✅ Compra Finalizada
   "Agilizou! Pode sair sem fila!"
```

## 🖥️ Backend API - FastAPI

### **Estrutura da API:**
```
guardflow-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── config.py               # Configurações
│   ├── database.py             # DB connection
│   ├── models/                 # SQLAlchemy models
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── cart.py
│   │   ├── transaction.py
│   │   └── store.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── cart.py
│   │   └── transaction.py
│   ├── api/                    # Endpoints
│   │   ├── auth.py             # Autenticação
│   │   ├── scanner.py          # Scanner/Vision
│   │   ├── cart.py             # Carrinho
│   │   ├── payment.py          # Pagamentos
│   │   └── store.py            # Supermercado
│   ├── services/               # Business logic
│   │   ├── vision_service.py   # Google Vision
│   │   ├── payment_service.py  # PIX/Pagamentos
│   │   ├── guardpass_service.py # GuardPass sim
│   │   └── notification_service.py
│   └── utils/                  # Utilities
│       ├── security.py
│       ├── helpers.py
│       └── constants.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

### **Endpoints Principais:**
```
Authentication:
├── POST /auth/login            # Login GuardPass
├── POST /auth/refresh          # Refresh token
└── GET  /auth/me              # User info

Scanner/Products:
├── POST /scanner/scan          # Escanear produto
├── GET  /products/{barcode}    # Info produto
├── GET  /products/search       # Buscar produtos
└── POST /products/feedback     # Feedback reconhecimento

Shopping Cart:
├── GET  /cart                  # Ver carrinho
├── POST /cart/add             # Adicionar item
├── PUT  /cart/update          # Atualizar quantidade
└── DELETE /cart/remove        # Remover item

Payment:
├── POST /payment/create        # Criar pagamento PIX
├── GET  /payment/{id}/status   # Status pagamento
├── POST /payment/webhook       # Webhook Mercado Pago
└── GET  /payment/history       # Histórico

Store Management:
├── GET  /stores                # Listar lojas
├── GET  /stores/{id}          # Info loja
├── POST /stores/{id}/checkin   # Check-in na loja
└── GET  /stores/{id}/products  # Produtos da loja
```

## 🗄️ Banco de Dados

### **Schema PostgreSQL:**
```sql
-- Usuários (integração GuardPass)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guardpass_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Supermercados
CREATE TABLE stores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(2) NOT NULL,
    zipcode VARCHAR(10) NOT NULL,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Produtos
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    barcode VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    brand VARCHAR(100),
    category VARCHAR(100),
    price DECIMAL(10,2),
    image_url TEXT,
    esg_score INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Carrinho de compras
CREATE TABLE carts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    store_id UUID REFERENCES stores(id),
    status VARCHAR(20) DEFAULT 'active',
    total_amount DECIMAL(10,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Itens do carrinho
CREATE TABLE cart_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cart_id UUID REFERENCES carts(id),
    product_id UUID REFERENCES products(id),
    quantity INTEGER NOT NULL DEFAULT 1,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Transações/Pagamentos
CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cart_id UUID REFERENCES carts(id),
    user_id UUID REFERENCES users(id),
    store_id UUID REFERENCES stores(id),
    amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    payment_id VARCHAR(255), -- ID do Mercado Pago
    status VARCHAR(20) DEFAULT 'pending',
    pix_qr_code TEXT,
    pix_code TEXT,
    paid_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Produtos escaneados (analytics)
CREATE TABLE scan_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    store_id UUID REFERENCES stores(id),
    product_id UUID REFERENCES products(id),
    confidence_score FLOAT,
    scan_duration INTEGER, -- milliseconds
    successful BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔍 Computer Vision - Scanner

### **Integração Google Vision API:**
```python
# services/vision_service.py
import io
import base64
from google.cloud import vision
from typing import Optional, Dict, Any

class VisionService:
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()
    
    async def scan_product(self, image_base64: str) -> Dict[str, Any]:
        """
        Escanear produto via Google Vision API
        """
        try:
            # Decodificar imagem
            image_data = base64.b64decode(image_base64)
            image = vision.Image(content=image_data)
            
            # Detectar texto (para códigos de barras)
            text_response = self.client.text_detection(image=image)
            texts = text_response.text_annotations
            
            # Detectar objetos
            object_response = self.client.object_localization(image=image)
            objects = object_response.localized_object_annotations
            
            # Processar resultados
            barcode = self._extract_barcode(texts)
            product_info = self._identify_product(objects, texts)
            
            return {
                'barcode': barcode,
                'product_name': product_info.get('name'),
                'confidence': product_info.get('confidence', 0),
                'category': product_info.get('category'),
                'success': barcode is not None
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'success': False,
                'confidence': 0
            }
    
    def _extract_barcode(self, texts) -> Optional[str]:
        """Extrair código de barras do texto detectado"""
        for text in texts:
            # Regex para códigos de barras brasileiros
            if self._is_valid_barcode(text.description):
                return text.description
        return None
    
    def _identify_product(self, objects, texts) -> Dict[str, Any]:
        """Identificar produto baseado em objetos e texto"""
        # Lógica de identificação de produto
        # Por enquanto, retorna mock data
        return {
            'name': 'Produto Identificado',
            'confidence': 0.85,
            'category': 'Alimentício'
        }
```

### **Scanner Mobile (React Native):**
```typescript
// components/Scanner/ProductScanner.tsx
import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, Alert } from 'react-native';
import { Camera, useCameraDevices } from 'react-native-vision-camera';
import { useDispatch } from 'react-redux';
import { scanProduct } from '../store/slices/cartSlice';

export const ProductScanner: React.FC = () => {
  const [hasPermission, setHasPermission] = useState(false);
  const [isScanning, setIsScanning] = useState(false);
  const devices = useCameraDevices();
  const device = devices.back;
  const dispatch = useDispatch();

  useEffect(() => {
    checkCameraPermission();
  }, []);

  const checkCameraPermission = async () => {
    const status = await Camera.getCameraPermissionStatus();
    if (status === 'granted') {
      setHasPermission(true);
    } else {
      const permission = await Camera.requestCameraPermission();
      setHasPermission(permission === 'granted');
    }
  };

  const handleScan = async (frame: any) => {
    if (isScanning) return;
    
    setIsScanning(true);
    
    try {
      // Capturar frame e converter para base64
      const imageBase64 = await captureFrame(frame);
      
      // Enviar para API
      const result = await dispatch(scanProduct(imageBase64)).unwrap();
      
      if (result.success) {
        Alert.alert(
          'Produto Agilizado! 🚀',
          `${result.product_name} adicionado ao carrinho`,
          [{ text: 'Agiliza aí!', style: 'default' }]
        );
      } else {
        Alert.alert(
          'Ops! 😅',
          'Não conseguimos agilizar esse produto. Tenta de novo?'
        );
      }
    } catch (error) {
      Alert.alert('Erro', 'Algo deu errado. Vamos agilizar isso!');
    } finally {
      setIsScanning(false);
    }
  };

  if (!device || !hasPermission) {
    return (
      <View style={styles.container}>
        <Text style={styles.message}>
          Precisamos da câmera para agilizar suas compras! 📱
        </Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Camera
        style={StyleSheet.absoluteFill}
        device={device}
        isActive={true}
        onFrameProcessorPerformanceSuggestionAvailable={handleScan}
      />
      
      <View style={styles.overlay}>
        <View style={styles.scanArea}>
          <Text style={styles.instruction}>
            Aponte para o produto e agilize! 🎯
          </Text>
        </View>
        
        {isScanning && (
          <View style={styles.loading}>
            <Text style={styles.loadingText}>
              Agilizando... ⚡
            </Text>
          </View>
        )}
      </View>
    </View>
  );
};
```

## 💳 Sistema de Pagamentos

### **Integração Mercado Pago (PIX):**
```python
# services/payment_service.py
import mercadopago
from typing import Dict, Any
from app.config import settings

class PaymentService:
    def __init__(self):
        self.mp = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
    
    async def create_pix_payment(
        self, 
        amount: float, 
        user_email: str,
        description: str = "Compra GuardFlow"
    ) -> Dict[str, Any]:
        """
        Criar pagamento PIX via Mercado Pago
        """
        payment_data = {
            "transaction_amount": amount,
            "description": f"GuardFlow - {description}",
            "payment_method_id": "pix",
            "payer": {
                "email": user_email
            },
            "notification_url": f"{settings.API_BASE_URL}/payment/webhook"
        }
        
        try:
            result = self.mp.payment().create(payment_data)
            payment = result["response"]
            
            return {
                "payment_id": payment["id"],
                "qr_code": payment["point_of_interaction"]["transaction_data"]["qr_code"],
                "qr_code_base64": payment["point_of_interaction"]["transaction_data"]["qr_code_base64"],
                "ticket_url": payment["point_of_interaction"]["transaction_data"]["ticket_url"],
                "status": payment["status"],
                "success": True
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "success": False
            }
    
    async def check_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """
        Verificar status do pagamento
        """
        try:
            result = self.mp.payment().get(payment_id)
            payment = result["response"]
            
            return {
                "payment_id": payment_id,
                "status": payment["status"],
                "status_detail": payment["status_detail"],
                "amount": payment["transaction_amount"],
                "success": True
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "success": False
            }
```

## 🎨 Interface "Agiliza aí"

### **Design System GuardFlow:**
```typescript
// styles/theme.ts
export const GuardFlowTheme = {
  colors: {
    primary: '#007BFF',      // Azul GuardPass
    secondary: '#00C851',    // Verde Agilidade
    accent: '#FF6B35',       // Laranja Energia
    neutral: '#6C757D',      // Cinza Moderno
    background: '#F8F9FA',
    surface: '#FFFFFF',
    error: '#DC3545',
    success: '#28A745',
    warning: '#FFC107'
  },
  
  typography: {
    h1: {
      fontFamily: 'Inter-Bold',
      fontSize: 28,
      color: '#007BFF'
    },
    h2: {
      fontFamily: 'Inter-SemiBold',
      fontSize: 24,
      color: '#333333'
    },
    slogan: {
      fontFamily: 'Inter-SemiBoldItalic',
      fontSize: 18,
      color: '#FF6B35'
    },
    body: {
      fontFamily: 'Inter-Regular',
      fontSize: 16,
      color: '#333333'
    }
  },
  
  spacing: {
    xs: 4,
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32
  },
  
  borderRadius: {
    sm: 4,
    md: 8,
    lg: 12,
    xl: 16
  }
};

// Componentes com linguagem "Agiliza aí"
export const GuardFlowMessages = {
  welcome: "Agiliza aí! Bem-vindo ao GuardFlow! 🚀",
  scanning: "Aponte e agilize suas compras! 🎯",
  productAdded: "Agilizou! Produto adicionado! ⚡",
  checkout: "Vamos agilizar seu pagamento! 💳",
  success: "Agilizou! Compra finalizada! ✅",
  error: "Ops! Vamos agilizar isso juntos! 😅",
  loading: "Agilizando... ⏱️"
};
```

## 🚀 Cronograma de Desenvolvimento (90 Dias)

### **Sprint 1 (Dias 1-30): Fundação**
```
Semana 1-2: Setup e Infraestrutura
├── ✅ Configurar repositórios Git
├── ✅ Setup ambiente desenvolvimento
├── ✅ Configurar CI/CD pipeline
├── ✅ Criar banco de dados
└── ✅ Deploy inicial (staging)

Semana 3-4: Backend Core
├── ✅ API FastAPI básica
├── ✅ Autenticação JWT
├── ✅ CRUD básico (users, products, stores)
├── ✅ Integração Mercado Pago
└── ✅ Testes unitários básicos
```

### **Sprint 2 (Dias 31-60): Features Core**
```
Semana 5-6: Scanner e Vision
├── ✅ Integração Google Vision API
├── ✅ Endpoint /scanner/scan
├── ✅ Banco de produtos mock
├── ✅ Lógica de reconhecimento
└── ✅ Feedback de confiança

Semana 7-8: App Mobile Base
├── ✅ Setup React Native/Expo
├── ✅ Navegação principal
├── ✅ Telas de login/onboarding
├── ✅ Scanner com câmera
└── ✅ Integração com API
```

### **Sprint 3 (Dias 61-90): Finalização e Testes**
```
Semana 9-10: Checkout e Pagamentos
├── ✅ Carrinho de compras
├── ✅ Checkout flow completo
├── ✅ Pagamento PIX
├── ✅ Confirmação de pagamento
└── ✅ Histórico de compras

Semana 11-12: Polish e Deploy
├── ✅ Interface "Agiliza aí" completa
├── ✅ Testes end-to-end
├── ✅ Performance optimization
├── ✅ Deploy produção
└── ✅ Documentação final
```

## 📊 Métricas de Sucesso MVP

### **KPIs Técnicos:**
```
Performance:
├── Scanner: <2s para reconhecer produto
├── Checkout: <30s do scan ao pagamento
├── API: <500ms response time
├── App: <3s cold start
└── Uptime: >99% disponibilidade

Qualidade:
├── Reconhecimento produtos: >80% accuracy
├── Falsos positivos: <5%
├── Crashes: <1% das sessões
├── Testes: >90% coverage
└── Security: Zero vulnerabilidades críticas
```

### **KPIs de Negócio:**
```
Validação:
├── 3 supermercados parceiros
├── 100 usuários beta testers
├── 1000 produtos escaneados
├── 100 transações completadas
└── NPS >8.0 dos usuários

Agilidade (vs checkout tradicional):
├── 50% redução tempo checkout
├── 80% satisfação usuários
├── 90% taxa conversão scan→compra
├── <1% taxa abandono carrinho
└── 95% pagamentos PIX bem-sucedidos
```

## 🎯 Próximos Passos Imediatos

### **Esta Semana:**
1. **Setup repositórios** e ambiente dev
2. **Configurar infraestrutura** AWS/Railway
3. **Criar banco** PostgreSQL inicial
4. **Começar backend** FastAPI básico
5. **Setup mobile** React Native/Expo

### **Próximas 2 Semanas:**
1. **API funcional** com endpoints principais
2. **Scanner básico** funcionando
3. **App mobile** com navegação
4. **Integração pagamentos** PIX
5. **Primeiro teste** end-to-end

### **Primeiro Mês:**
1. **MVP funcional** completo
2. **Testes** com supermercado piloto
3. **Feedback** e iterações
4. **Preparação** para escala
5. **Documentação** para parceiros

## 🏆 Resultado Esperado

### **MVP Entregue (90 dias):**
- ✅ **App mobile** nativo iOS/Android
- ✅ **Scanner** reconhecendo produtos brasileiros
- ✅ **Checkout** completo com PIX
- ✅ **Interface** "Agiliza aí" brasileira
- ✅ **Backend** escalável e seguro
- ✅ **Dashboard** para supermercados
- ✅ **Integração** GuardPass simulada
- ✅ **Documentação** completa

### **Validação Mercado:**
- ✅ **3 supermercados** testando
- ✅ **100 usuários** ativos
- ✅ **1000 compras** agilizadas
- ✅ **Feedback positivo** >8.0 NPS
- ✅ **Métricas** comprovando agilidade

**Resultado:** MVP que **comprova viabilidade** e permite **escalar rapidamente** para os 50 supermercados meta! 🚀

---

*GuardFlow MVP - Agiliza aí em 90 dias! 🇧🇷⚡*



