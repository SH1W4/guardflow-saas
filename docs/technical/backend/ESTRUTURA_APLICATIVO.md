# GuardFlow - Estrutura do Aplicativo

## 🔍 Análise da Estrutura Atual

### **Status Atual: Landing Page Bem Estruturada**
Você já criou uma **landing page impressionante** com:
- ✅ **HTML semântico** bem organizado
- ✅ **CSS moderno** com variáveis CSS e design responsivo
- ✅ **JavaScript funcional** com navegação e demos
- ✅ **Seções completas**: Hero, Features, Demo, Tech, Roadmap, Investment
- ✅ **Design profissional** com gradientes e animações

### **Pontos Fortes da Estrutura Atual**

#### **1. HTML Estruturado (index.html)**
```html
Estrutura bem organizada:
├── Navigation (navbar responsiva)
├── Hero Section (call-to-action principal)
├── Features (6 recursos principais)
├── Demo Interativa (5 telas)
├── Technology Stack (4 categorias)
├── Roadmap (6 fases de desenvolvimento)
├── Investment (formulário de investidores)
├── Contact (informações de contato)
└── Footer (links e redes sociais)
```

#### **2. CSS Moderno (styles.css)**
```css
Características técnicas:
├── CSS Variables (--primary-green, --primary-blue, etc.)
├── Design Responsivo (media queries)
├── Gradientes modernos (linear-gradient)
├── Animações CSS (transitions, transforms)
├── Typography (Inter font family)
├── Component-based (navbar, hero, features, etc.)
└── Mobile-first approach
```

#### **3. JavaScript Funcional (main.js)**
```javascript
Funcionalidades implementadas:
├── Navigation (smooth scrolling, mobile menu)
├── Scroll Effects (parallax, fade-in)
├── Demo System (interactive demos)
├── Form Handling (investment, contact)
├── Animations (entrance effects)
└── Mobile Responsiveness
```

## 🚀 Estrutura Proposta: Aplicativo Mobile

### **Visão Geral: Do Website para App**
Agora precisamos **evoluir da landing page para o aplicativo mobile** real. Vou propor uma estrutura robusta e escalável:

```
GuardFlow-App/
├── 📱 Mobile App (React Native)
├── 🌐 Backend API (FastAPI)
├── 🗄️ Database (PostgreSQL + Redis)
├── ⛓️ Blockchain (Smart Contracts)
├── 🤖 AI Services (Computer Vision + ML)
└── ☁️ Infrastructure (Docker + AWS)
```

### **1. Estrutura do Mobile App (React Native)**

#### **Arquitetura de Pastas**
```
src/
├── components/           # Componentes reutilizáveis
│   ├── common/          # Botões, inputs, cards
│   ├── forms/           # Formulários específicos
│   ├── navigation/      # Componentes de navegação
│   └── scanner/         # Componentes do scanner
├── screens/             # Telas do aplicativo
│   ├── auth/           # Login, registro, onboarding
│   ├── shopping/       # Scanner, carrinho, checkout
│   ├── rewards/        # Tokens GST, NFTs, recompensas
│   ├── profile/        # Perfil, histórico, configurações
│   └── wallet/         # Carteira digital, pagamentos
├── services/           # Serviços e APIs
│   ├── api/           # Chamadas para backend
│   ├── auth/          # Autenticação e autorização
│   ├── blockchain/    # Interação com blockchain
│   ├── camera/        # Scanner e computer vision
│   └── storage/       # Armazenamento local
├── store/             # Gerenciamento de estado (Redux)
│   ├── slices/        # Redux Toolkit slices
│   ├── middleware/    # Middleware customizado
│   └── persist/       # Persistência de estado
├── utils/             # Utilitários e helpers
│   ├── constants/     # Constantes da aplicação
│   ├── helpers/       # Funções auxiliares
│   ├── hooks/         # Custom hooks
│   └── validators/    # Validações
├── assets/            # Recursos estáticos
│   ├── images/        # Imagens e ícones
│   ├── fonts/         # Fontes customizadas
│   └── animations/    # Animações Lottie
└── styles/            # Estilos globais
    ├── colors.js      # Paleta de cores
    ├── typography.js  # Tipografia
    └── spacing.js     # Espaçamentos
```

#### **Telas Principais do App**

##### **1. Onboarding & Auth**
```
screens/auth/
├── OnboardingScreen.js    # Introdução ao app (4 telas)
├── LoginScreen.js         # Login com email/biometria
├── RegisterScreen.js      # Cadastro de usuário
├── BiometricSetupScreen.js # Configuração biométrica
└── PermissionsScreen.js   # Solicitação de permissões
```

##### **2. Shopping Experience**
```
screens/shopping/
├── ScannerScreen.js       # Scanner principal (câmera + IA)
├── ProductScreen.js       # Detalhes do produto escaneado
├── CartScreen.js          # Carrinho de compras
├── CheckoutScreen.js      # Finalização da compra
└── ReceiptScreen.js       # Recibo e NFe tokenizada
```

##### **3. Rewards & Tokens**
```
screens/rewards/
├── TokensScreen.js        # Saldo GST e histórico
├── NFTsScreen.js          # Coleção de NFTs (NFe)
├── RewardsScreen.js       # Recompensas disponíveis
├── MarketplaceScreen.js   # Marketplace de NFTs
└── ESGScreen.js           # Impacto ESG pessoal
```

##### **4. Profile & Wallet**
```
screens/profile/
├── ProfileScreen.js       # Perfil do usuário
├── WalletScreen.js        # Carteira digital
├── HistoryScreen.js       # Histórico de compras
├── SettingsScreen.js      # Configurações
└── HelpScreen.js          # Central de ajuda
```

### **2. Estrutura do Backend (FastAPI)**

#### **Arquitetura de Microserviços**
```
backend/
├── api/                 # API Gateway
│   ├── auth/           # Autenticação e autorização
│   ├── users/          # Gestão de usuários
│   ├── products/       # Catálogo de produtos
│   ├── transactions/   # Transações e pagamentos
│   ├── tokens/         # Tokens GST e NFTs
│   └── analytics/      # Analytics e relatórios
├── services/           # Microserviços
│   ├── scanner/        # Computer Vision Service
│   ├── blockchain/     # Blockchain Integration
│   ├── payments/       # Payment Processing
│   ├── notifications/  # Push Notifications
│   └── esg/           # ESG Data Processing
├── models/            # Modelos de dados
│   ├── user.py        # Modelo de usuário
│   ├── product.py     # Modelo de produto
│   ├── transaction.py # Modelo de transação
│   └── token.py       # Modelo de token
├── database/          # Configuração de banco
│   ├── migrations/    # Migrações do banco
│   ├── seeds/         # Dados iniciais
│   └── connection.py  # Conexão com PostgreSQL
├── blockchain/        # Smart Contracts
│   ├── contracts/     # Contratos Solidity
│   ├── migrations/    # Deploy scripts
│   └── abi/          # ABIs dos contratos
└── utils/            # Utilitários
    ├── security.py    # Funções de segurança
    ├── validators.py  # Validações
    └── helpers.py     # Funções auxiliares
```

### **3. Estrutura de Dados**

#### **Banco de Dados Principal (PostgreSQL)**
```sql
-- Usuários
users (
    id UUID PRIMARY KEY,
    email VARCHAR UNIQUE,
    name VARCHAR,
    phone VARCHAR,
    wallet_address VARCHAR,
    gst_balance DECIMAL,
    created_at TIMESTAMP
);

-- Produtos
products (
    id UUID PRIMARY KEY,
    barcode VARCHAR UNIQUE,
    name VARCHAR,
    brand VARCHAR,
    price DECIMAL,
    esg_score INTEGER,
    created_at TIMESTAMP
);

-- Transações
transactions (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    total_amount DECIMAL,
    gst_earned INTEGER,
    nfe_hash VARCHAR,
    nft_token_id VARCHAR,
    created_at TIMESTAMP
);

-- NFTs (NFe Tokenizada)
nfts (
    id UUID PRIMARY KEY,
    transaction_id UUID REFERENCES transactions(id),
    token_id VARCHAR UNIQUE,
    metadata_uri VARCHAR,
    esg_data JSONB,
    created_at TIMESTAMP
);
```

#### **Cache e Sessões (Redis)**
```
Redis Structure:
├── user_sessions:{user_id}     # Sessões de usuário
├── product_cache:{barcode}     # Cache de produtos
├── gst_balance:{user_id}       # Saldo GST em tempo real
├── scanner_results:{session}   # Resultados do scanner
└── rate_limits:{user_id}       # Rate limiting
```

### **4. Componentes Principais do App**

#### **Scanner Component (Core)**
```javascript
// components/scanner/CameraScanner.js
import { Camera } from 'react-native-vision-camera';
import { runOnJS, runOnUI } from 'react-native-reanimated';

const CameraScanner = ({ onProductDetected }) => {
  // IA para reconhecimento de produtos
  const processFrame = useCallback((frame) => {
    'worklet';
    
    // Computer Vision processing
    const products = detectProducts(frame);
    
    if (products.length > 0) {
      runOnJS(onProductDetected)(products[0]);
    }
  }, [onProductDetected]);

  return (
    <Camera
      style={styles.camera}
      device={device}
      isActive={true}
      frameProcessor={processFrame}
      frameProcessorFps={5}
    />
  );
};
```

#### **Token Management**
```javascript
// services/blockchain/tokenService.js
class TokenService {
  async earnGSTTokens(userId, amount, reason) {
    // Mint GST tokens para o usuário
    const transaction = await this.gstContract.mint(
      userWallet, 
      amount,
      { reason, timestamp: Date.now() }
    );
    
    return transaction;
  }

  async createNFT(transactionData) {
    // Criar NFT da NFe
    const metadata = {
      name: `NFe #${transactionData.id}`,
      description: 'Nota Fiscal Eletrônica Tokenizada',
      image: transactionData.qrCode,
      attributes: [
        { trait_type: 'ESG Score', value: transactionData.esgScore },
        { trait_type: 'Store', value: transactionData.store },
        { trait_type: 'Total', value: transactionData.total }
      ]
    };

    const nft = await this.nftContract.mint(
      userWallet,
      metadata
    );

    return nft;
  }
}
```

#### **ESG Calculation Engine**
```javascript
// services/esg/esgCalculator.js
class ESGCalculator {
  calculateProductESG(product) {
    const scores = {
      environmental: this.calculateEnvironmental(product),
      social: this.calculateSocial(product),
      governance: this.calculateGovernance(product)
    };

    return {
      total: (scores.environmental + scores.social + scores.governance) / 3,
      breakdown: scores,
      gstReward: this.calculateGSTReward(scores.total)
    };
  }

  calculateEnvironmental(product) {
    let score = 50; // Base score
    
    // Produto orgânico
    if (product.isOrganic) score += 20;
    
    // Embalagem sustentável
    if (product.sustainablePackaging) score += 15;
    
    // Produção local
    if (product.isLocal) score += 10;
    
    // Carbon footprint baixo
    if (product.lowCarbon) score += 5;
    
    return Math.min(score, 100);
  }

  calculateGSTReward(esgScore) {
    // Quanto maior o ESG score, mais GST tokens
    return Math.floor(esgScore / 10); // 10 ESG = 1 GST
  }
}
```

### **5. Fluxo de Uso do App**

#### **Jornada do Usuário**
```
1. Onboarding
   ├── Apresentação do app (4 telas)
   ├── Cadastro/Login
   ├── Configuração biométrica
   └── Permissões (câmera, localização)

2. Shopping
   ├── Abrir scanner
   ├── Escanear produto (IA identifica)
   ├── Ver detalhes + ESG score
   ├── Adicionar ao carrinho
   ├── Continuar escaneando
   └── Finalizar compra

3. Checkout
   ├── Revisar carrinho
   ├── Escolher pagamento
   ├── Confirmar compra
   ├── Processar pagamento
   ├── Gerar NFe
   ├── Tokenizar NFe (criar NFT)
   ├── Distribuir GST tokens
   └── Mostrar recibo

4. Rewards
   ├── Ver saldo GST
   ├── Ver coleção NFTs
   ├── Trocar GST por desconto
   ├── Vender NFTs no marketplace
   └── Ver impacto ESG
```

### **6. Tecnologias e Ferramentas**

#### **Frontend Mobile**
```javascript
{
  "dependencies": {
    "react-native": "0.72+",
    "react-navigation": "^6.0",
    "@reduxjs/toolkit": "^1.9",
    "react-native-vision-camera": "^3.0",
    "react-native-biometrics": "^3.0",
    "react-native-reanimated": "^3.0",
    "react-native-gesture-handler": "^2.0",
    "react-native-vector-icons": "^9.0",
    "react-native-async-storage": "^1.19",
    "react-native-keychain": "^8.0",
    "web3": "^4.0",
    "@walletconnect/react-native": "^2.0"
  }
}
```

#### **Backend API**
```python
# requirements.txt
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
alembic==1.13.0
psycopg2-binary==2.9.9
redis==5.0.1
celery==5.3.4
web3==6.11.3
opencv-python==4.8.1
tensorflow==2.14.0
pydantic==2.5.0
python-jose==3.3.0
passlib==1.7.4
boto3==1.34.0
```

#### **Infrastructure**
```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
      
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: guardflow
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      
  redis:
    image: redis:7
    ports:
      - "6379:6379"
      
  blockchain:
    image: ethereum/client-go:latest
    ports:
      - "8545:8545"
```

## 🎯 Próximos Passos

### **Fase 1: Setup do Projeto (Esta Semana)**
1. **Configurar ambiente React Native**
2. **Criar estrutura de pastas**
3. **Implementar navegação básica**
4. **Configurar Redux store**

### **Fase 2: Core Features (Próximas 2 semanas)**
1. **Implementar scanner com IA**
2. **Criar sistema de autenticação**
3. **Desenvolver carrinho de compras**
4. **Integrar sistema de pagamentos**

### **Fase 3: Blockchain Integration (Próximas 4 semanas)**
1. **Implementar smart contracts**
2. **Criar sistema de tokens GST**
3. **Desenvolver NFTs de NFe**
4. **Integrar carteira digital**

### **Fase 4: Advanced Features (Próximas 8 semanas)**
1. **Marketplace de NFTs**
2. **Sistema de recompensas**
3. **Analytics ESG**
4. **Otimizações de performance**

---

*Estrutura do Aplicativo GuardFlow - Sistema de Economia Urbana Tokenizada*



