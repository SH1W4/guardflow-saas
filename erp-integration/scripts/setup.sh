#!/bin/bash

# GuardFlow ERP Integration Setup Script
# Script para configurar e inicializar a integração ERP

set -e

echo "🚀 Iniciando setup da GuardFlow ERP Integration..."

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verificar se Docker está instalado
check_docker() {
    log "Verificando Docker..."
    if ! command -v docker &> /dev/null; then
        error "Docker não está instalado. Por favor, instale o Docker primeiro."
        exit 1
    fi
    success "Docker encontrado"
}

# Verificar se Docker Compose está instalado
check_docker_compose() {
    log "Verificando Docker Compose..."
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose não está instalado. Por favor, instale o Docker Compose primeiro."
        exit 1
    fi
    success "Docker Compose encontrado"
}

# Criar diretórios necessários
create_directories() {
    log "Criando diretórios necessários..."
    mkdir -p logs
    mkdir -p data
    mkdir -p ssl
    mkdir -p grafana/dashboards
    mkdir -p grafana/datasources
    success "Diretórios criados"
}

# Criar arquivo de configuração do Nginx
create_nginx_config() {
    log "Criando configuração do Nginx..."
    cat > nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream erp_integration {
        server erp-integration:8003;
    }

    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://erp_integration;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /health {
            proxy_pass http://erp_integration/health;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
EOF
    success "Configuração do Nginx criada"
}

# Criar arquivo de configuração do Prometheus
create_prometheus_config() {
    log "Criando configuração do Prometheus..."
    cat > prometheus.yml << 'EOF'
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'erp-integration'
    static_configs:
      - targets: ['erp-integration:8003']
    metrics_path: '/metrics'
    scrape_interval: 5s

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:5432']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
EOF
    success "Configuração do Prometheus criada"
}

# Criar arquivo de inicialização do banco
create_init_sql() {
    log "Criando script de inicialização do banco..."
    cat > init.sql << 'EOF'
-- GuardFlow ERP Integration Database Initialization

-- Criar extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabela de configurações ERP
CREATE TABLE IF NOT EXISTS erp_configurations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    erp_type VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    host VARCHAR(255) NOT NULL,
    port INTEGER NOT NULL,
    username VARCHAR(100),
    password VARCHAR(255),
    database VARCHAR(100),
    additional_config JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de sessões de autenticação
CREATE TABLE IF NOT EXISTS auth_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(255) UNIQUE NOT NULL,
    erp_type VARCHAR(50) NOT NULL,
    auth_method VARCHAR(50) NOT NULL,
    user_info JSONB,
    permissions TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de jobs de sincronização
CREATE TABLE IF NOT EXISTS sync_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id VARCHAR(255) UNIQUE NOT NULL,
    erp_type VARCHAR(50) NOT NULL,
    sync_type VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    records_processed INTEGER DEFAULT 0,
    records_success INTEGER DEFAULT 0,
    records_failed INTEGER DEFAULT 0,
    error_message TEXT
);

-- Tabela de dados sincronizados
CREATE TABLE IF NOT EXISTS synced_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id VARCHAR(255) NOT NULL,
    data_type VARCHAR(50) NOT NULL,
    source_id VARCHAR(255) NOT NULL,
    data JSONB NOT NULL,
    mapped_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES sync_jobs(job_id)
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_erp_configurations_type ON erp_configurations(erp_type);
CREATE INDEX IF NOT EXISTS idx_erp_configurations_active ON erp_configurations(is_active);
CREATE INDEX IF NOT EXISTS idx_auth_sessions_session_id ON auth_sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_auth_sessions_expires_at ON auth_sessions(expires_at);
CREATE INDEX IF NOT EXISTS idx_sync_jobs_status ON sync_jobs(status);
CREATE INDEX IF NOT EXISTS idx_sync_jobs_erp_type ON sync_jobs(erp_type);
CREATE INDEX IF NOT EXISTS idx_synced_data_job_id ON synced_data(job_id);
CREATE INDEX IF NOT EXISTS idx_synced_data_data_type ON synced_data(data_type);

-- Inserir configurações padrão
INSERT INTO erp_configurations (erp_type, name, host, port, username, password, database, additional_config) VALUES
('sap', 'SAP Development', 'sap-dev.example.com', 8000, 'admin', 'admin123', 'SAP_DEV', '{"rfc_destination": "SAP_DEV"}'),
('oracle', 'Oracle Development', 'oracle-dev.example.com', 1521, 'admin', 'admin123', 'ORACLE_DEV', '{"service_name": "ORACLE_DEV"}'),
('dynamics', 'Dynamics Development', 'dynamics-dev.example.com', 443, 'admin', 'admin123', 'DYNAMICS_DEV', '{"api_version": "v1.0"}'),
('totvs', 'TOTVS Development', 'totvs-dev.example.com', 8080, 'admin', 'admin123', 'TOTVS_DEV', '{"environment": "development"}')
ON CONFLICT DO NOTHING;

-- Função para atualizar timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers para atualizar timestamp
CREATE TRIGGER update_erp_configurations_updated_at BEFORE UPDATE ON erp_configurations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_synced_data_updated_at BEFORE UPDATE ON synced_data FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
EOF
    success "Script de inicialização do banco criado"
}

# Construir e iniciar containers
build_and_start() {
    log "Construindo e iniciando containers..."
    
    # Parar containers existentes
    docker-compose down 2>/dev/null || true
    
    # Construir imagens
    docker-compose build --no-cache
    
    # Iniciar containers
    docker-compose up -d
    
    success "Containers iniciados"
}

# Verificar status dos serviços
check_services() {
    log "Verificando status dos serviços..."
    
    # Aguardar serviços ficarem prontos
    sleep 10
    
    # Verificar ERP Integration
    if curl -f http://localhost:8003/health > /dev/null 2>&1; then
        success "ERP Integration está rodando"
    else
        warning "ERP Integration pode não estar pronto ainda"
    fi
    
    # Verificar PostgreSQL
    if docker-compose exec postgres pg_isready -U postgres > /dev/null 2>&1; then
        success "PostgreSQL está rodando"
    else
        warning "PostgreSQL pode não estar pronto ainda"
    fi
    
    # Verificar Redis
    if docker-compose exec redis redis-cli ping > /dev/null 2>&1; then
        success "Redis está rodando"
    else
        warning "Redis pode não estar pronto ainda"
    fi
}

# Mostrar informações de acesso
show_access_info() {
    log "Informações de acesso:"
    echo ""
    echo "🌐 Serviços disponíveis:"
    echo "  • ERP Integration API: http://localhost:8003"
    echo "  • API Documentation: http://localhost:8003/docs"
    echo "  • ReDoc Documentation: http://localhost:8003/redoc"
    echo "  • Health Check: http://localhost:8003/health"
    echo "  • Status: http://localhost:8003/status"
    echo "  • Metrics: http://localhost:8003/metrics"
    echo ""
    echo "📊 Monitoramento:"
    echo "  • Prometheus: http://localhost:9090"
    echo "  • Grafana: http://localhost:3001 (admin/admin)"
    echo ""
    echo "🗄️  Bancos de dados:"
    echo "  • PostgreSQL: localhost:5433 (postgres/password)"
    echo "  • Redis: localhost:6380"
    echo ""
    echo "📝 Logs:"
    echo "  • docker-compose logs -f erp-integration"
    echo "  • docker-compose logs -f postgres"
    echo "  • docker-compose logs -f redis"
    echo ""
}

# Função principal
main() {
    echo "🛠️  GuardFlow ERP Integration Setup"
    echo "=================================="
    echo ""
    
    check_docker
    check_docker_compose
    create_directories
    create_nginx_config
    create_prometheus_config
    create_init_sql
    build_and_start
    check_services
    show_access_info
    
    echo ""
    success "Setup concluído com sucesso! 🎉"
    echo ""
    echo "Para parar os serviços: docker-compose down"
    echo "Para ver logs: docker-compose logs -f"
    echo "Para reiniciar: docker-compose restart"
}

# Executar função principal
main "$@"
