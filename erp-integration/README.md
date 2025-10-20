# 🔗 GuardFlow ERP Integration

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-20+-2496ed.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 **VISÃO GERAL**

**GuardFlow ERP Integration** é um sistema completo de integração com sistemas ERP (SAP, Oracle, Microsoft Dynamics, TOTVS) que permite sincronização de dados em tempo real e em lote, autenticação segura e mapeamento inteligente de dados.

### 🏷️ **Linguagens e Tecnologias**
- **Backend**: Python 3.11+, FastAPI, SQLAlchemy, Pydantic
- **Database**: PostgreSQL, Redis
- **ERP Connectors**: SAP RFC, Oracle OCI, Dynamics API, TOTVS API
- **Authentication**: OAuth2, JWT, Basic Auth, API Keys
- **DevOps**: Docker, Kubernetes, Nginx, Prometheus, Grafana

## 🎯 **PROPOSTA DE VALOR**

- **🔗 Integração Universal**: Suporte a SAP, Oracle, Dynamics, TOTVS
- **⚡ Sincronização Inteligente**: Tempo real e em lote
- **🔐 Autenticação Segura**: Múltiplos métodos de autenticação
- **📊 Mapeamento de Dados**: Conversão automática entre formatos
- **📈 Monitoramento**: Métricas e dashboards em tempo real
- **🔄 Sincronização Automática**: Agendamento e execução automática
- **🛡️ Segurança**: Criptografia e validação de dados
- **📱 API RESTful**: Integração simples e documentada

## 🚀 **QUICK START**

### **Pré-requisitos**
- Docker & Docker Compose
- Git
- 4GB RAM disponível
- 10GB espaço em disco

### **Instalação Rápida**

```bash
# Clone o repositório
git clone https://github.com/SH1W4/guardflow-saas.git
cd guardflow-saas/erp-integration

# Executar setup automático
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### **Instalação Manual**

```bash
# 1. Construir e iniciar containers
docker-compose up -d

# 2. Verificar status
docker-compose ps

# 3. Ver logs
docker-compose logs -f erp-integration
```

## 📦 **COMPONENTES**

### **ERP Connectors**
- **SAP Connector**: Integração via RFC
- **Oracle Connector**: Integração via OCI
- **Dynamics Connector**: Integração via REST API
- **TOTVS Connector**: Integração via API nativa

### **Data Synchronization**
- **Real-time Sync**: Sincronização em tempo real
- **Batch Sync**: Sincronização em lote
- **Scheduled Sync**: Sincronização agendada
- **Manual Sync**: Sincronização manual

### **Authentication System**
- **Basic Auth**: Autenticação básica
- **OAuth2**: Fluxo OAuth2 completo
- **JWT**: Tokens JWT seguros
- **API Keys**: Chaves de API

### **Data Mapping**
- **Product Mapping**: Mapeamento de produtos
- **Customer Mapping**: Mapeamento de clientes
- **Inventory Mapping**: Mapeamento de estoque
- **Order Mapping**: Mapeamento de pedidos

## 🔧 **CONFIGURAÇÃO**

### **Variáveis de Ambiente**

```bash
# Database
DATABASE_URL=postgresql://postgres:password@postgres:5432/guardflow_erp
REDIS_URL=redis://redis:6379/0

# ERP Configurations
SAP_HOST=sap-server.example.com
SAP_PORT=8000
SAP_USERNAME=admin
SAP_PASSWORD=admin123

ORACLE_HOST=oracle-server.example.com
ORACLE_PORT=1521
ORACLE_USERNAME=admin
ORACLE_PASSWORD=admin123

DYNAMICS_HOST=dynamics-server.example.com
DYNAMICS_API_KEY=your-api-key

TOTVS_HOST=totvs-server.example.com
TOTVS_PORT=8080
TOTVS_USERNAME=admin
TOTVS_PASSWORD=admin123

# Security
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=8

# Monitoring
PROMETHEUS_ENABLED=true
GRAFANA_ENABLED=true
```

## 📊 **FUNCIONALIDADES**

### **1. Conectar ao ERP**
```python
from guardflow_erp import ERPIntegration

# Configurar ERP
erp_config = {
    "erp_type": "sap",
    "host": "sap-server.example.com",
    "port": 8000,
    "username": "admin",
    "password": "admin123"
}

# Conectar
erp = ERPIntegration(erp_config)
await erp.connect()
```

### **2. Sincronizar Dados**
```python
# Sincronização completa
sync_result = await erp.sync_all_data(
    store_id="STORE001",
    sync_type="batch",
    data_types=["products", "inventory", "customers", "orders"]
)

# Sincronização específica
products = await erp.sync_products(store_id="STORE001")
inventory = await erp.sync_inventory(store_id="STORE001")
customers = await erp.sync_customers()
orders = await erp.sync_orders()
```

### **3. Obter Dados**
```python
# Obter produtos
products = await erp.get_products(filters={"category": "Alimentos"})

# Obter estoque
inventory = await erp.get_inventory(store_id="STORE001")

# Obter clientes
customers = await erp.get_customers(filters={"city": "São Paulo"})

# Obter pedidos
orders = await erp.get_orders(filters={"status": "Completed"})
```

### **4. Agendar Sincronização**
```python
# Agendar sincronização automática
await erp.schedule_sync(
    store_id="STORE001",
    interval_minutes=60,
    data_types=["products", "inventory"]
)

# Obter sincronizações agendadas
scheduled = await erp.get_scheduled_syncs()
```

## 🔌 **API REFERENCE**

### **Endpoints Principais**

#### **Conectar ao ERP**
```http
POST /api/v1/erp/connect
Content-Type: application/json

{
  "erp_type": "sap",
  "host": "sap-server.example.com",
  "port": 8000,
  "username": "admin",
  "password": "admin123"
}
```

#### **Sincronizar Dados**
```http
POST /api/v1/erp/sync
Content-Type: application/json

{
  "erp_config": {
    "erp_type": "sap",
    "host": "sap-server.example.com",
    "port": 8000,
    "username": "admin",
    "password": "admin123"
  },
  "store_id": "STORE001",
  "sync_type": "batch",
  "data_types": ["products", "inventory", "customers", "orders"]
}
```

#### **Obter Status do Job**
```http
GET /api/v1/erp/sync/jobs/{job_id}
```

#### **Obter Produtos**
```http
GET /api/v1/erp/products
```

#### **Obter Estoque**
```http
GET /api/v1/erp/inventory/{store_id}
```

#### **Health Check**
```http
GET /api/v1/erp/health
```

## 🧪 **TESTES**

### **Executar Testes**
```bash
# Testes unitários
python -m pytest tests/unit/

# Testes de integração
python -m pytest tests/integration/

# Testes de performance
python -m pytest tests/performance/

# Testes com cobertura
python -m pytest --cov=app tests/
```

### **Testes de Conectividade**
```bash
# Testar conexão SAP
python tests/test_sap_connection.py

# Testar conexão Oracle
python tests/test_oracle_connection.py

# Testar conexão Dynamics
python tests/test_dynamics_connection.py

# Testar conexão TOTVS
python tests/test_totvs_connection.py
```

## 📈 **MONITORAMENTO**

### **Métricas Disponíveis**
- **Performance**: Tempo de resposta, throughput
- **Sincronização**: Jobs executados, sucessos, falhas
- **Conectividade**: Status das conexões ERP
- **Dados**: Registros processados, mapeados, validados

### **Dashboards**
- **Grafana**: http://localhost:3001 (admin/admin)
- **Prometheus**: http://localhost:9090
- **Métricas da API**: http://localhost:8003/metrics

### **Alertas**
- **Falha de Conexão**: ERP inacessível
- **Sincronização Falhada**: Jobs com erro
- **Performance Degradada**: Tempo de resposta alto
- **Dados Inconsistentes**: Validação falhou

## 🛣️ **ROADMAP**

### **Phase 1: Core Integration (✅ Completed)**
- [x] Conectores ERP (SAP, Oracle, Dynamics, TOTVS)
- [x] Sistema de autenticação
- [x] Mapeamento de dados
- [x] Sincronização básica
- [x] API RESTful

### **Phase 2: Advanced Features (🔄 In Progress)**
- [ ] Sincronização em tempo real
- [ ] Transformação de dados avançada
- [ ] Validação de dados inteligente
- [ ] Retry automático
- [ ] Compressão de dados

### **Phase 3: Enterprise Features (📋 Planned)**
- [ ] Suporte a mais ERPs
- [ ] Clustering e alta disponibilidade
- [ ] Backup e recuperação
- [ ] Auditoria completa
- [ ] Compliance e segurança

## 💰 **BUSINESS MODEL**

### **Revenue Sources**
1. **Licenciamento**: Por ERP conectado
2. **Sincronização**: Por volume de dados
3. **Suporte**: Suporte técnico premium
4. **Customização**: Desenvolvimentos específicos

### **Pricing Tiers**
- **Starter**: 1 ERP, 1K registros/mês
- **Professional**: 3 ERPs, 10K registros/mês
- **Enterprise**: Ilimitado, suporte 24/7

## 🤝 **CONTRIBUIÇÃO**

### **Como Contribuir**
1. Fork o repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

### **Padrões de Código**
- **Python**: PEP 8, Black, Flake8
- **TypeScript**: ESLint, Prettier
- **Documentação**: Markdown, OpenAPI
- **Testes**: Pytest, Coverage

## 📄 **LICENÇA**

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 **SUPORTE**

### **Documentação**
- **API Docs**: http://localhost:8003/docs
- **ReDoc**: http://localhost:8003/redoc
- **Health Check**: http://localhost:8003/health

### **Comunidade**
- **GitHub Issues**: https://github.com/SH1W4/guardflow-saas/issues
- **Email**: erp-support@guardflow.com
- **Slack**: https://guardflow.slack.com

### **Suporte Técnico**
- **Documentação**: [docs.guardflow.com/erp](https://docs.guardflow.com/erp)
- **FAQ**: [docs.guardflow.com/erp/faq](https://docs.guardflow.com/erp/faq)
- **Troubleshooting**: [docs.guardflow.com/erp/troubleshooting](https://docs.guardflow.com/erp/troubleshooting)

---

**GuardFlow ERP Integration** - Conectando ERPs ao futuro! 🚀

**Versão**: 1.0.0  
**Status**: 🚧 **EM DESENVOLVIMENTO**  
**Próxima versão**: v1.1.0 (Janeiro 2025)

