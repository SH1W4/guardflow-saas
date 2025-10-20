# 🚀 GUARDFLOW - GUIA DE OPERAÇÃO DO REPOSITÓRIO

## 📋 Visão Geral
Este guia fornece instruções completas para operar o repositório GuardFlow em diferentes ambientes.

## 🏗️ Estrutura do Projeto
```
GuardFlow/
├── backend/              # Backend FastAPI com segurança OAuth2/JWT
├── guardflow-saas/       # SaaS Completo  
├── guardflow-sdk/        # SDK Unificado
├── guardflow-web/         # Interface Web (React)
├── mobile-app/           # App Móvel (React Native)
├── analytics/            # Serviço de Analytics
├── docsync/             # Sincronização de Docs
├── examples/             # Exemplos e Demos
├── docs/                # Documentação consolidada
├── infrastructure/      # Infraestrutura Docker
├── scripts/             # Scripts de automação
├── .github/workflows/   # CI/CD workflows
└── docker-compose.dev.yml # Stack de desenvolvimento
```

## 🔧 Comandos Essenciais

### Desenvolvimento Local
```bash
# Backend (FastAPI)
cd backend
python -m venv venv
venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Frontend (React)
cd guardflow-web
npm install
npm start

# Mobile (React Native)
cd mobile-app
npm install
npx react-native run-android
# ou
npx react-native run-ios

# SaaS (React)
cd guardflow-saas
npm install
npm start
```

### Docker (Recomendado)
```bash
# Desenvolvimento completo
docker-compose -f docker-compose.dev.yml up -d

# Verificar serviços
docker-compose -f docker-compose.dev.yml ps

# Logs
docker-compose -f docker-compose.dev.yml logs -f backend

# Parar serviços
docker-compose -f docker-compose.dev.yml down
```

### Testes
```bash
# Backend (com cobertura)
cd backend
pytest -v --cov=app --cov-report=html

# Testes específicos
pytest tests/test_auth_cart_payment.py -v
pytest tests/test_health.py -v

# Frontend
cd guardflow-web
npm test

# Mobile
cd mobile-app
npm test
```

## 📊 Monitoramento e Observabilidade

### Serviços Disponíveis
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Métricas**: http://localhost:8000/metrics
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001 (admin/guardflow)

### Health Checks
```bash
# Health check básico
curl http://localhost:8000/health

# Métricas Prometheus
curl http://localhost:8000/metrics

# Status dos containers
docker-compose -f docker-compose.dev.yml ps
```

## 🔐 Segurança

### Configurações Implementadas
- **OAuth2/JWT**: Autenticação segura com tokens
- **RBAC**: Controle de acesso baseado em roles
- **Rate Limiting**: Proteção contra abuso
- **CORS**: Configuração de origens confiáveis
- **Trusted Hosts**: Validação de hosts

### Variáveis de Ambiente
```bash
# Backend (.env)
DATABASE_URL=postgresql://guardflow:guardflow@db:5432/guardflow
REDIS_URL=redis://redis:6380
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
```

### Rotação de Segredos
- **Tokens JWT**: Configurável via `JWT_EXPIRE_MINUTES`
- **Rate Limiting**: 100 req/min por IP (configurável)
- **CORS**: Domínios específicos configurados

## 🚀 Deploy e CI/CD

### Workflows GitHub Actions
- **CI**: Linting (ruff) + Testes (pytest) na push/PR
- **Staging**: Deploy automático na branch `develop`
- **Produção**: Deploy automático na branch `main`

### Comandos de Deploy
```bash
# Verificar status
git status
git branch

# Deploy para staging
git checkout develop
git pull origin develop
git push origin develop

# Deploy para produção
git checkout main
git merge develop
git push origin main
```

### Rollback
```bash
# Identificar commit anterior
git log --oneline

# Rollback
git revert <commit-hash>
git push origin <branch>
```

## 📈 Métricas e Logs

### Prometheus Metrics
- **Request Duration**: Tempo de resposta das APIs
- **Request Count**: Número de requisições
- **Error Rate**: Taxa de erros
- **Active Connections**: Conexões ativas

### Grafana Dashboards
- **API Performance**: Métricas de performance
- **Error Tracking**: Rastreamento de erros
- **Resource Usage**: Uso de recursos
- **Business Metrics**: Métricas de negócio

### Logs Estruturados
```bash
# Logs do backend
docker-compose -f docker-compose.dev.yml logs -f backend

# Logs específicos
docker-compose -f docker-compose.dev.yml logs backend | grep ERROR
```

## 🛠️ Troubleshooting

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
```

## 📞 Suporte e Contatos

### Canais de Suporte
- **Issues**: [GitHub Issues](https://github.com/SH1W4/guardflow/issues)
- **Documentação**: `/docs` directory
- **Email**: support@guardflow.com
- **Discord**: [GuardFlow Community](https://discord.gg/guardflow)

### Documentação Adicional
- **[SETUP_DEV.md](SETUP_DEV.md)** - Setup de desenvolvimento
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
```

---

<div align="center">
🚀 **GuardFlow** - Sistema de Checkout Inteligente<br/>
Operação e Monitoramento Profissional
</div>