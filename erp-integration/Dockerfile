FROM python:3.11-slim

# Definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    unixodbc \
    unixodbc-dev \
    libaio1 \
    libaio-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar Oracle Instant Client
RUN curl -o oracle-instantclient-basic-21.9.0.0.0-1.x86_64.rpm \
    https://download.oracle.com/otn_software/linux/instantclient/219000/oracle-instantclient-basic-21.9.0.0.0-1.x86_64.rpm \
    && curl -o oracle-instantclient-devel-21.9.0.0.0-1.x86_64.rpm \
    https://download.oracle.com/otn_software/linux/instantclient/219000/oracle-instantclient-devel-21.9.0.0.0-1.x86_64.rpm \
    && alien -d oracle-instantclient-basic-21.9.0.0.0-1.x86_64.rpm \
    && alien -d oracle-instantclient-devel-21.9.0.0.0-1.x86_64.rpm \
    && dpkg -i oracle-instantclient-basic_21.9.0.0.0-2_amd64.deb \
    && dpkg -i oracle-instantclient-devel_21.9.0.0.0-2_amd64.deb \
    && rm -f *.rpm *.deb

# Configurar Oracle Instant Client
ENV LD_LIBRARY_PATH=/usr/lib/oracle/21/client64/lib:$LD_LIBRARY_PATH
ENV ORACLE_HOME=/usr/lib/oracle/21/client64

# Criar diretório da aplicação
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretórios necessários
RUN mkdir -p /app/logs /app/data

# Definir permissões
RUN chmod +x /app/scripts/*.sh 2>/dev/null || true

# Expor porta
EXPOSE 8003

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8003/health || exit 1

# Comando de inicialização
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003", "--reload"]

