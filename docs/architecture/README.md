# 🔗 **ARQUITETURA DE INTEGRAÇÃO GUARDFLOW ↔ ECOSYSTEM-DEGOV**

## 📋 **VISÃO GERAL**

Este diretório contém toda a documentação e configurações para a integração entre o **GuardFlow** (sistema de processamento NFe ESG) e o **Ecosystem-Degov** (ecossistema de tokenização ESG).

### **🎯 Objetivo da Integração**
Criar um **ecossistema ESG completo** que combina:
- **GuardFlow**: Processamento de NFe ESG (B2B)
- **Ecosystem-Degov**: Tokenização ESG (DeFi)
- **Integração**: Monetização de dados ESG via tokens

---

## 📁 **ESTRUTURA DOS ARQUIVOS**

```
docs/architecture/
├── README.md                           # Este arquivo
├── INTEGRACAO_GUARDFLOW_ECOSYSTEM_DEGOV.md  # Documentação completa
├── integration-config.yaml             # Configuração YAML
├── integration.env.example             # Variáveis de ambiente
├── docker-compose.integration.yml     # Docker Compose
└── diagrams/                          # Diagramas de arquitetura
    ├── integration-flow.mermaid
    ├── data-flow.mermaid
    └── deployment.mermaid
```

---

## 🚀 **INÍCIO RÁPIDO**

### **1. Configuração do Ambiente**

```bash
# 1. Copiar arquivo de configuração
cp docs/architecture/integration.env.example backend/.env.integration

# 2. Ajustar variáveis de ambiente
# Editar backend/.env.integration com suas configurações

# 3. Iniciar serviços
docker-compose -f docs/architecture/docker-compose.integration.yml up -d
```

### **2. Verificar Integração**

```bash
# Verificar status dos serviços
curl http://localhost:8000/health
curl http://localhost:8080/health

# Verificar status da integração
curl http://localhost:8000/api/v1/ecosystem-integration/integration-status
```

### **3. Testar Tokenização**

```bash
# Exemplo de tokenização de NFe
curl -X POST http://localhost:8000/api/v1/ecosystem-integration/tokenize-nfe \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_token" \
  -d '{
    "nfe_id": "12345678901234567890123456789012345678901234",
    "chave_acesso": "35240114200166000187550010000000071234567890",
    "valor_total": 1500.00,
    "ncm_codes": ["84000000", "01000000"],
    "emitente": {
      "cnpj": "14200166000187",
      "razao_social": "Empresa Exemplo LTDA"
    },
    "destinatario": {
      "cnpj_cpf": "12345678000195",
      "razao_social": "Cliente Exemplo LTDA"
    }
  }'
```

---

## 🔧 **CONFIGURAÇÃO DETALHADA**

### **📋 Variáveis de Ambiente**

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `ECOSYSTEM_DEGOV_API_URL` | URL do Ecosystem-Degov | `http://localhost:8080` |
| `ECOSYSTEM_DEGOV_API_KEY` | Chave de API | `sk_guardflow_1234567890abcdef` |
| `INTEGRATION_ENABLED` | Habilitar integração | `true` |
| `INTEGRATION_TIMEOUT` | Timeout das requisições | `30` |
| `INTEGRATION_RETRY_ATTEMPTS` | Tentativas de retry | `3` |

### **🗄️ Banco de Dados**

#### **Tabelas de Integração**
```sql
-- Logs de integração
CREATE TABLE esg_integration_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nfe_id VARCHAR(44) NOT NULL,
    chave_acesso VARCHAR(44) NOT NULL,
    esg_score_overall DECIMAL(5,2) NOT NULL,
    valor_total DECIMAL(15,2) NOT NULL,
    transaction_id VARCHAR(100),
    tokens_generated JSONB,
    integration_status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Transações de tokens
CREATE TABLE token_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nfe_id VARCHAR(44) NOT NULL,
    transaction_hash VARCHAR(66),
    token_type VARCHAR(20) NOT NULL,
    amount DECIMAL(18,8) NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## 🔄 **FLUXOS DE INTEGRAÇÃO**

### **📈 Fluxo Principal: NFe → ESG Score → Tokens**

1. **Upload NFe** → GuardFlow processa XML
2. **Cálculo ESG** → ESG Engine calcula scores
3. **Envio para Tokenização** → Ecosystem-Degov recebe dados
4. **Trinity AI Agent** → Processa e otimiza
5. **Geração de Tokens** → Smart contracts criam tokens
6. **Retorno de Resultado** → GuardFlow recebe confirmação

### **🔄 Fluxos Secundários**

#### **Sincronização de Dados**
- **Intervalo**: A cada 5 minutos
- **Método**: Message Queue (Redis)
- **Dados**: Logs, status, transações

#### **Monitoramento**
- **Métricas**: Prometheus
- **Dashboards**: Grafana
- **Alertas**: Slack/Email

---

## 🛡️ **SEGURANÇA E COMPLIANCE**

### **🔐 Autenticação**
- **API Keys**: Rotação automática a cada 30 dias
- **Webhooks**: Verificação de assinatura HMAC
- **Rate Limiting**: 100 req/min por cliente

### **📋 Compliance**
- **LGPD**: Anonimização de dados pessoais
- **SEFAZ**: Não interferência na NFe original
- **Blockchain**: Logs imutáveis de transações

---

## 📊 **MONITORAMENTO**

### **🔍 Métricas Importantes**

#### **GuardFlow**
- `integration_requests_total`: Total de requisições
- `integration_success_rate`: Taxa de sucesso
- `integration_latency_seconds`: Latência média

#### **Ecosystem-Degov**
- `tokens_generated_total`: Total de tokens
- `nft_minted_total`: Total de NFTs
- `blockchain_transactions_total`: Transações blockchain

### **📈 Dashboards**

#### **Dashboard de Integração**
- **URL**: http://localhost:3001/d/integration
- **Métricas**: Taxa de sucesso, latência, volume
- **Alertas**: Falhas, timeouts, erros

---

## 🚨 **TROUBLESHOOTING**

### **❌ Problemas Comuns**

#### **1. Timeout de Integração**
```bash
# Verificar conectividade
curl -v http://ecosystem-degov:8080/health

# Ajustar timeout
export INTEGRATION_TIMEOUT=60
```

#### **2. Falha na Tokenização**
```bash
# Verificar logs
docker logs guardflow
docker logs ecosystem-degov

# Verificar status da blockchain
curl http://localhost:8080/api/v1/blockchain/status
```

#### **3. Sincronização de Dados**
```bash
# Forçar sincronização
curl -X POST http://localhost:8000/api/v1/ecosystem-integration/sync-data
```

### **🔧 Comandos Úteis**

```bash
# Verificar status dos serviços
docker-compose -f docs/architecture/docker-compose.integration.yml ps

# Ver logs em tempo real
docker-compose -f docs/architecture/docker-compose.integration.yml logs -f

# Reiniciar serviços
docker-compose -f docs/architecture/docker-compose.integration.yml restart

# Limpar volumes
docker-compose -f docs/architecture/docker-compose.integration.yml down -v
```

---

## 📚 **DOCUMENTAÇÃO ADICIONAL**

### **🔗 Links Úteis**
- [Documentação Completa](./INTEGRACAO_GUARDFLOW_ECOSYSTEM_DEGOV.md)
- [Configuração YAML](./integration-config.yaml)
- [Docker Compose](./docker-compose.integration.yml)
- [Variáveis de Ambiente](./integration.env.example)

### **📖 Documentação Técnica**
- [GuardFlow API](../api/README.md)
- [Ecosystem-Degov API](../../ecosystem-degov/docs/api/README.md)
- [Trinity AI Agent](../../ecosystem-degov/docs/trinity/README.md)
- [Blockchain Integration](./blockchain/README.md)

---

## 🤝 **SUPORTE**

### **📞 Contato**
- **Email**: integration@guardflow.com
- **Slack**: #integration-support
- **GitHub**: [Issues](https://github.com/guardflow/integration/issues)

### **📋 Checklist de Manutenção**

#### **Diário**
- [ ] Verificar status dos serviços
- [ ] Verificar métricas de integração
- [ ] Verificar logs de erro

#### **Semanal**
- [ ] Análise de performance
- [ ] Backup de dados
- [ ] Atualização de dependências

#### **Mensal**
- [ ] Auditoria de segurança
- [ ] Análise de custos
- [ ] Planejamento de melhorias

---

*Última atualização: 16 de Outubro de 2025*
*Versão: 1.0.0*
*Autor: GuardFlow Development Team*
