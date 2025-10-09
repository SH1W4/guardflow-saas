#!/bin/bash

# GuardFlow AI Services - Setup Script
# Script de configuração e inicialização do SaaS de IA

set -e

echo "🚀 Iniciando configuração do GuardFlow AI Services..."

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
    exit 1
}

# Verificar dependências
check_dependencies() {
    log "Verificando dependências..."
    
    # Verificar Docker
    if ! command -v docker &> /dev/null; then
        error "Docker não encontrado. Instale o Docker primeiro."
    fi
    
    # Verificar Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose não encontrado. Instale o Docker Compose primeiro."
    fi
    
    # Verificar Python
    if ! command -v python3 &> /dev/null; then
        error "Python 3 não encontrado. Instale o Python 3 primeiro."
    fi
    
    success "Todas as dependências encontradas"
}

# Criar diretórios necessários
create_directories() {
    log "Criando diretórios necessários..."
    
    mkdir -p models
    mkdir -p logs
    mkdir -p data
    mkdir -p monitoring/grafana/dashboards
    mkdir -p monitoring/grafana/datasources
    mkdir -p nginx/ssl
    
    success "Diretórios criados"
}

# Configurar variáveis de ambiente
setup_environment() {
    log "Configurando variáveis de ambiente..."
    
    if [ ! -f .env ]; then
        cat > .env << EOF
# GuardFlow AI Services - Environment Variables

# Application
ENVIRONMENT=development
DEBUG=true
SECRET_KEY=your-secret-key-change-this-in-production

# Database
DATABASE_URL=postgresql://guardflow:guardflow123@localhost:5432/guardflow_ai

# Redis
REDIS_URL=redis://localhost:6379

# External APIs (opcional)
GOOGLE_VISION_API_KEY=your-google-vision-api-key
OPENAI_API_KEY=your-openai-api-key
HUGGINGFACE_API_KEY=your-huggingface-api-key

# AI Models
MODEL_PATH=./models
MODEL_CACHE_TTL=3600
MODEL_BATCH_SIZE=32
MODEL_MAX_WORKERS=4

# Performance
MAX_CONCURRENT_REQUESTS=100
REQUEST_TIMEOUT=30
MODEL_LOAD_TIMEOUT=60

# Security
JWT_ALGORITHM=HS256
PASSWORD_MIN_LENGTH=8

# Monitoring
SENTRY_DSN=your-sentry-dsn
PROMETHEUS_ENABLED=true

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
EOF
        success "Arquivo .env criado"
    else
        warning "Arquivo .env já existe"
    fi
}

# Baixar modelos pré-treinados
download_models() {
    log "Baixando modelos pré-treinados..."
    
    # Criar script de download de modelos
    cat > scripts/download_models.py << 'EOF'
#!/usr/bin/env python3
"""
Script para baixar modelos pré-treinados
"""

import os
import requests
import zipfile
from pathlib import Path

def download_model(url, filename, extract_to):
    """Baixa e extrai um modelo"""
    print(f"Baixando {filename}...")
    
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print(f"Extraindo {filename}...")
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    
    os.remove(filename)
    print(f"✅ {filename} baixado e extraído com sucesso")

def main():
    """Função principal"""
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # Lista de modelos para baixar
    models = [
        {
            "name": "product_recognition",
            "url": "https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5s.pt",
            "filename": "yolov5s.pt"
        },
        {
            "name": "sentiment_analysis",
            "url": "https://huggingface.co/bert-base-multilingual-uncased/resolve/main/pytorch_model.bin",
            "filename": "bert-base-multilingual-uncased.bin"
        }
    ]
    
    for model in models:
        try:
            download_model(
                model["url"],
                model["filename"],
                models_dir / model["name"]
            )
        except Exception as e:
            print(f"❌ Erro ao baixar {model['name']}: {e}")
    
    print("🎉 Todos os modelos baixados com sucesso!")

if __name__ == "__main__":
    main()
EOF
    
    # Executar script de download
    python3 scripts/download_models.py
    
    success "Modelos baixados"
}

# Configurar banco de dados
setup_database() {
    log "Configurando banco de dados..."
    
    # Criar script de inicialização do banco
    cat > init.sql << 'EOF'
-- GuardFlow AI Services - Database Initialization

-- Criar extensões
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Criar schema para IA
CREATE SCHEMA IF NOT EXISTS ai;

-- Tabela de modelos
CREATE TABLE IF NOT EXISTS ai.models (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL UNIQUE,
    version VARCHAR(50) NOT NULL,
    type VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'inactive',
    accuracy DECIMAL(5,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de predições
CREATE TABLE IF NOT EXISTS ai.predictions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    model_id UUID REFERENCES ai.models(id),
    input_data JSONB,
    output_data JSONB,
    confidence DECIMAL(5,4),
    processing_time INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de métricas
CREATE TABLE IF NOT EXISTS ai.metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    model_id UUID REFERENCES ai.models(id),
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(10,4) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_predictions_model_id ON ai.predictions(model_id);
CREATE INDEX IF NOT EXISTS idx_predictions_created_at ON ai.predictions(created_at);
CREATE INDEX IF NOT EXISTS idx_metrics_model_id ON ai.metrics(model_id);
CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON ai.metrics(timestamp);

-- Inserir modelos padrão
INSERT INTO ai.models (name, version, type, status) VALUES
('product_recognition', '1.0.0', 'vision', 'active'),
('sentiment_analysis', '1.0.0', 'nlp', 'active'),
('demand_forecasting', '1.0.0', 'analytics', 'active'),
('recommendation', '1.0.0', 'recommendation', 'active')
ON CONFLICT (name) DO NOTHING;

-- Criar usuário para aplicação
CREATE USER IF NOT EXISTS guardflow WITH PASSWORD 'guardflow123';
GRANT ALL PRIVILEGES ON DATABASE guardflow_ai TO guardflow;
GRANT ALL PRIVILEGES ON SCHEMA ai TO guardflow;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA ai TO guardflow;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA ai TO guardflow;
EOF
    
    success "Script de inicialização do banco criado"
}

# Configurar monitoramento
setup_monitoring() {
    log "Configurando monitoramento..."
    
    # Configuração do Prometheus
    cat > monitoring/prometheus.yml << 'EOF'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "rules/*.yml"

scrape_configs:
  - job_name: 'guardflow-ai'
    static_configs:
      - targets: ['ai-services:8000']
    metrics_path: '/metrics'
    scrape_interval: 5s

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:5432']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
EOF
    
    # Configuração do Grafana
    cat > monitoring/grafana/datasources/prometheus.yml << 'EOF'
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
EOF
    
    success "Monitoramento configurado"
}

# Configurar Nginx
setup_nginx() {
    log "Configurando Nginx..."
    
    cat > nginx/nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream ai_services {
        server ai-services:8000;
    }

    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://ai_services;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /health {
            proxy_pass http://ai_services/health;
        }
    }
}
EOF
    
    success "Nginx configurado"
}

# Inicializar serviços
start_services() {
    log "Iniciando serviços..."
    
    # Parar serviços existentes
    docker-compose down 2>/dev/null || true
    
    # Construir e iniciar serviços
    docker-compose up --build -d
    
    success "Serviços iniciados"
}

# Verificar status dos serviços
check_services() {
    log "Verificando status dos serviços..."
    
    # Aguardar serviços iniciarem
    sleep 10
    
    # Verificar AI Services
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        success "AI Services está rodando"
    else
        error "AI Services não está respondendo"
    fi
    
    # Verificar PostgreSQL
    if docker-compose exec postgres pg_isready -U guardflow -d guardflow_ai > /dev/null 2>&1; then
        success "PostgreSQL está rodando"
    else
        error "PostgreSQL não está respondendo"
    fi
    
    # Verificar Redis
    if docker-compose exec redis redis-cli ping > /dev/null 2>&1; then
        success "Redis está rodando"
    else
        error "Redis não está respondendo"
    fi
}

# Função principal
main() {
    log "🚀 Iniciando configuração do GuardFlow AI Services..."
    
    check_dependencies
    create_directories
    setup_environment
    download_models
    setup_database
    setup_monitoring
    setup_nginx
    start_services
    check_services
    
    success "🎉 GuardFlow AI Services configurado com sucesso!"
    
    echo ""
    echo "📋 Informações dos serviços:"
    echo "  🌐 AI Services: http://localhost:8000"
    echo "  📊 Prometheus: http://localhost:9090"
    echo "  📈 Grafana: http://localhost:3000 (admin/admin123)"
    echo "  🗄️  PostgreSQL: localhost:5432"
    echo "  🔴 Redis: localhost:6379"
    echo ""
    echo "📚 Documentação da API: http://localhost:8000/docs"
    echo "🔍 Health Check: http://localhost:8000/health"
    echo ""
    echo "Para parar os serviços: docker-compose down"
    echo "Para ver logs: docker-compose logs -f"
}

# Executar função principal
main "$@"
