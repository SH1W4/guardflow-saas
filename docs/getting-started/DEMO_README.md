# 🚀 GuardFlow Demo - Sistema de Checkout Inteligente

## 📋 Visão Geral

O **GuardFlow** é um sistema de checkout inteligente que revoluciona a experiência de compras em supermercados. Este demo apresenta todas as funcionalidades principais do sistema.

## ✨ Funcionalidades Demonstradas

### 🛒 **Sistema de Carrinho Inteligente**
- Escaneamento de produtos (simulado)
- Gerenciamento de quantidade
- Cálculo automático de totais
- Persistência local dos dados

### 💳 **Múltiplas Formas de Pagamento**
- **PIX** - Pagamento instantâneo
- **Cartão** - Crédito ou débito
- **GuardPass** - Sistema proprietário GuardDrive
- **GST Tokens** - Tokens de sustentabilidade ESG

### 🌱 **Integração ESG**
- Tokens de sustentabilidade
- Impacto ambiental positivo
- Sistema de recompensas
- **Conversão de notas fiscais em ativos ESG**
- **Marketplace de ativos ESG**

### 💰 **Sistema de Monetização**
- **Conversão de notas fiscais em dinheiro** (95% do valor)
- **Taxa GuardFlow** (5% do valor convertido)
- **Conversão em ativos ESG** (sem taxa)
- **Venda de ativos ESG** no marketplace
- **Histórico completo** de conversões

### 🛡️ **Segurança GuardDrive**
- Sistema de autenticação
- Proteção de dados
- Integração com blockchain

## 🚀 Como Executar o Demo

### Opção 1: Docker (Recomendado)

```bash
# 1. Navegar para o diretório do projeto
cd GuardFlow

# 2. Executar o script de inicialização
.\start-demo.ps1

# 3. Acessar http://localhost:3000
```

### Opção 2: Manual

```bash
# Backend (Terminal 1)
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000

# Frontend (Terminal 2)
cd guardflow-demo
npm install
npm start
```

## 🌐 Acessos

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentação API**: http://localhost:8000/docs
- **Banco de Dados**: localhost:5432 (PostgreSQL)
- **Cache**: localhost:6379 (Redis)

## 📱 Como Usar o Demo

### 1. **Página Inicial**
- Visão geral do sistema
- Ações rápidas
- Estatísticas do usuário

### 2. **Escanear Produtos**
- Clique em "Escanear Produto" para simular escaneamento
- Use os códigos de teste fornecidos
- Produtos são adicionados automaticamente ao carrinho

### 3. **Carrinho de Compras**
- Visualize todos os produtos
- Ajuste quantidades
- Remova itens
- Veja o total calculado

### 4. **Finalizar Pagamento**
- Escolha a forma de pagamento
- Veja informações sobre GuardPass e GST Tokens
- Simule o processamento do pagamento

### 5. **Perfil do Usuário**
- Faça login como demo (automático)
- Acesse configurações
- Veja estatísticas

### 6. **Monetização**
- Converta notas fiscais em dinheiro
- Converta em ativos ESG
- Venda ativos ESG no marketplace
- Acompanhe histórico de conversões

## 🧪 Códigos de Teste

Use estes códigos para testar o escaneamento:

| Código | Produto | Preço |
|--------|---------|-------|
| 1234567890123 | Coca-Cola 350ml | R$ 3,50 |
| 9876543210987 | Pão de Açúcar 500g | R$ 4,20 |
| 5555555555555 | Leite Integral 1L | R$ 5,90 |
| 1111111111111 | Arroz 5kg | R$ 12,90 |
| 2222222222222 | Feijão 1kg | R$ 8,50 |

## 🏗️ Arquitetura

### **Backend (FastAPI)**
- API REST completa
- Autenticação JWT
- Integração com PostgreSQL
- Cache Redis
- Documentação automática

### **Frontend (React + TypeScript)**
- Interface responsiva
- Context API para estado
- Roteamento com React Router
- Simulação de câmera

### **Banco de Dados**
- PostgreSQL para dados persistentes
- Redis para cache e sessões
- Migrações automáticas

## 🔧 Configurações

### **Variáveis de Ambiente**
```env
# Backend
DATABASE_URL=postgresql://guardflow:guardflow123@db:5432/guardflow
REDIS_URL=redis://redis:6379
ENVIRONMENT=production
DEBUG=false

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

### **Portas Utilizadas**
- 3000: Frontend React
- 8000: Backend FastAPI
- 5432: PostgreSQL
- 6379: Redis
- 80: Nginx (opcional)

## 📊 Métricas do Demo

- **5 páginas** principais implementadas
- **4 formas** de pagamento
- **5 produtos** de teste
- **100% responsivo** para mobile e desktop
- **Tempo de carregamento** < 3 segundos

## 🎯 Próximos Passos

1. **Integração com GuardDrive SDK**
2. **Câmera real** para escaneamento
3. **Notificações push**
4. **Histórico de compras**
5. **Sistema de avaliações**

## 🆘 Solução de Problemas

### **Docker não inicia**
```bash
# Verificar se Docker Desktop está rodando
docker --version

# Limpar containers antigos
docker-compose down
docker system prune -f
```

### **Porta já em uso**
```bash
# Verificar processos usando as portas
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# Parar processos se necessário
taskkill /PID <PID> /F
```

### **Frontend não carrega**
```bash
# Reinstalar dependências
cd guardflow-demo
rm -rf node_modules package-lock.json
npm install
npm start
```

## 📞 Suporte

Para dúvidas ou problemas:
- **Email**: suporte@guardflow.app
- **Documentação**: http://localhost:8000/docs
- **Logs**: `docker-compose logs -f`

---

**GuardFlow** - Agiliza aí suas compras! 🚀
