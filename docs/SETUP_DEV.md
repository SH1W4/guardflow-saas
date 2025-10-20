# 🛠️ GUARDFLOW - SETUP DE DESENVOLVIMENTO

## 📋 Pré-requisitos
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Docker (recomendado)

## 🚀 Setup Rápido

### 1. Clone e Configuração Inicial
```bash
git clone https://github.com/SH1W4/guardflow.git
cd guardflow
```

### 2. Backend (FastAPI) - Método 1: Local
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\Activate.ps1
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Editar .env com suas configurações

uvicorn app.main:app --reload --port 8000
```

### 3. Frontend (React)
```bash
cd guardflow-web
npm install
cp .env.example .env.development
# Editar .env.development

npm start
```

### 4. Mobile (React Native)
```bash
cd mobile-app
npm install
# Android
npx react-native run-android
# iOS
npx react-native run-ios
```

### 5. SaaS (Node.js)
```bash
cd guardflow-saas
npm install
npm start
```

## 🐳 Docker (Recomendado) - Método 2: Containerizado

### Setup Completo com Docker
```bash
# Iniciar todos os serviços
docker-compose -f docker-compose.dev.yml up -d

# Verificar status
docker-compose -f docker-compose.dev.yml ps

# Logs em tempo real
docker-compose -f docker-compose.dev.yml logs -f backend
```

### Serviços Disponíveis
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Métricas**: http://localhost:8000/metrics
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001 (admin/guardflow)

## 🔧 Configuração Avançada

### Variáveis de Ambiente

#### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://guardflow:guardflow@db:5432/guardflow
REDIS_URL=redis://redis:6380

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30

# API Keys
GOOGLE_VISION_API_KEY=your-google-vision-api-key
MERCADO_PAGO_ACCESS_TOKEN=your-mercado-pago-token

# Environment
DEBUG=true
ENVIRONMENT=development
```

#### Frontend (.env.development)
```bash
REACT_APP_API_BASE_URL=http://localhost:8000
REACT_APP_ENV=development
REACT_APP_VERSION=1.0.0
```

#### Mobile (src/config/api.js)
```javascript
export const API_BASE_URL = 'http://localhost:8000';
export const API_VERSION = 'v1';
```

### Banco de Dados

#### PostgreSQL (Local)
```bash
# Criar banco
createdb guardflow

# Conectar
psql guardflow

# Executar migrations (se houver)
# psql guardflow < backend/migrations/001_initial.sql
```

#### Redis (Local)
```bash
# Iniciar Redis
redis-server

# Testar conexão
redis-cli ping
```

## 🧪 Testes

### Testes do Backend
```bash
cd backend

# Todos os testes
pytest -v

# Com cobertura
pytest --cov=app --cov-report=html

# Testes específicos
pytest tests/test_auth_cart_payment.py -v
pytest tests/test_health.py -v

# Com variáveis de ambiente
PYTHONPATH=. pytest tests/ -v
```

### Testes do Frontend
```bash
cd guardflow-web
npm test
```

### Testes do Mobile
```bash
cd mobile-app
npm test
```

### Testes E2E (Docker)
```bash
# Executar testes em container
docker-compose -f docker-compose.dev.yml exec backend pytest tests/ -v
```

## 📊 Monitoramento e Observabilidade

### Prometheus Metrics
```bash
# Acessar métricas
curl http://localhost:8000/metrics

# Verificar targets
curl http://localhost:9090/api/v1/targets
```

### Grafana Dashboards
```bash
# Acessar Grafana
open http://localhost:3001
# Login: admin / guardflow

# Importar dashboards
# - API Performance
# - Error Tracking
# - Resource Usage
```

### Health Checks
```bash
# Health check básico
curl http://localhost:8000/health

# Health check detalhado
curl http://localhost:8000/health | jq

# Status dos containers
docker-compose -f docker-compose.dev.yml ps
```

## 🔍 Debugging

### Logs do Backend
```bash
# Logs em tempo real
docker-compose -f docker-compose.dev.yml logs -f backend

# Logs específicos
docker-compose -f docker-compose.dev.yml logs backend | grep ERROR

# Logs locais (se rodando sem Docker)
tail -f backend/logs/app.log
```

### Logs do Frontend
```bash
# Debug mode
cd guardflow-web
npm start -- --debug

# Logs do Metro
npx react-native log-android
npx react-native log-ios
```

### Debugging de Banco de Dados
```bash
# Conectar ao PostgreSQL
docker-compose -f docker-compose.dev.yml exec db psql -U guardflow -d guardflow

# Verificar tabelas
\dt

# Verificar conexões
SELECT * FROM pg_stat_activity;
```

### Debugging de Redis
```bash
# Conectar ao Redis
docker-compose -f docker-compose.dev.yml exec redis redis-cli

# Verificar chaves
KEYS *

# Monitorar comandos
MONITOR
```

## 🚨 Troubleshooting

### Problemas Comuns

#### Backend não inicia
```bash
# Verificar logs
docker-compose -f docker-compose.dev.yml logs backend

# Verificar variáveis de ambiente
docker-compose -f docker-compose.dev.yml exec backend env

# Reiniciar serviço
docker-compose -f docker-compose.dev.yml restart backend
```

#### Banco de dados não conecta
```bash
# Verificar status do PostgreSQL
docker-compose -f docker-compose.dev.yml ps db

# Verificar logs do banco
docker-compose -f docker-compose.dev.yml logs db

# Testar conexão
docker-compose -f docker-compose.dev.yml exec backend python -c "from app.database import engine; print('DB OK')"
```

#### Redis não conecta
```bash
# Verificar status do Redis
docker-compose -f docker-compose.dev.yml ps redis

# Testar conexão Redis
docker-compose -f docker-compose.dev.yml exec backend python -c "import redis; r = redis.Redis(host='redis', port=6379); print('Redis OK')"
```

#### Porta ocupada
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

#### Dependências
```bash
# Python
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall

# Node.js
npm install --force
npm cache clean --force
```

### Comandos de Diagnóstico
```bash
# Status geral
docker-compose -f docker-compose.dev.yml ps

# Uso de recursos
docker stats

# Logs em tempo real
docker-compose -f docker-compose.dev.yml logs -f

# Health check manual
curl -f http://localhost:8000/health || echo "Backend down"

# Verificar conectividade
curl -f http://localhost:8000/health && echo "Backend OK"
curl -f http://localhost:9090 && echo "Prometheus OK"
curl -f http://localhost:3001 && echo "Grafana OK"
```

## 📞 Suporte

### Canais de Suporte
- **Issues**: [GitHub Issues](https://github.com/SH1W4/guardflow/issues)
- **Documentação**: `/docs` directory
- **Email**: dev@guardflow.com
- **Discord**: [GuardFlow Community](https://discord.gg/guardflow)

### Documentação Adicional
- **[OPERACAO_REPO.md](OPERACAO_REPO.md)** - Guia de operação
- **[README.md](../README.md)** - Visão geral do projeto
- **[API Docs](http://localhost:8000/docs)** - Documentação da API

### Comandos de Emergência
```bash
# Status completo
docker-compose -f docker-compose.dev.yml ps && curl -f http://localhost:8000/health

# Restart completo
docker-compose -f docker-compose.dev.yml down && docker-compose -f docker-compose.dev.yml up -d

# Backup de dados
docker-compose -f docker-compose.dev.yml exec db pg_dump -U guardflow guardflow > backup.sql

# Limpeza completa
docker-compose -f docker-compose.dev.yml down -v
docker system prune -f
```

---

<div align="center">
🛠️ **GuardFlow** - Setup de Desenvolvimento<br/>
Ambiente Profissional e Produtivo
</div>