# 🐳 **STATUS DO DOCKER - GuardFlow**

## 📊 **Status Atual (15/10/2025)**

### **❌ Docker Desktop: NÃO RODANDO**
- **Serviço**: `com.docker.service` - Status: Stopped
- **Erro**: Cannot open 'com.docker.service' service
- **Causa**: Docker Desktop não está iniciado

### **✅ Docker CLI: INSTALADO**
- **Versão**: Docker version 28.1.1, build 4eba377
- **Plugins**: 15 plugins disponíveis
- **Context**: desktop-linux

---

## 🔧 **SOLUÇÕES PARA INICIAR DOCKER**

### **Opção 1: Iniciar Docker Desktop Manualmente**
1. **Pressione `Windows + R`**
2. **Digite**: `"C:\Program Files\Docker\Docker\Docker Desktop.exe"`
3. **Pressione Enter**
4. **Aguarde** o Docker Desktop inicializar (ícone na bandeja do sistema)

### **Opção 2: Via Menu Iniciar**
1. **Clique no Menu Iniciar**
2. **Procure por "Docker Desktop"**
3. **Clique para abrir**
4. **Aguarde** a inicialização completa

### **Opção 3: Via PowerShell (como Administrador)**
```powershell
# Abrir PowerShell como Administrador
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
```

---

## 🚀 **APÓS INICIAR O DOCKER**

### **1. Verificar se está funcionando:**
```bash
docker ps
```

### **2. Iniciar os containers do GuardFlow:**
```bash
# Navegar para o diretório do projeto
cd C:\Users\João\Desktop\PROJETOS\02_ORGANIZATIONS\GuardFlow

# Usar o docker-compose de desenvolvimento
docker-compose -f config/development/docker-compose.dev.yml up -d
```

### **3. Verificar containers rodando:**
```bash
docker ps
```

### **4. Acessar os serviços:**
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001 (admin/guardflow)

---

## 📋 **SERVIÇOS CONFIGURADOS**

### **Backend (FastAPI)**
- **Porta**: 8000
- **Build**: ./backend
- **Dependências**: db, redis

### **PostgreSQL**
- **Porta**: 5432 (interno)
- **Database**: guardflow
- **User**: guardflow
- **Password**: guardflow

### **Redis**
- **Porta**: 6380 (externa)
- **Cache e sessões**

### **Prometheus**
- **Porta**: 9090
- **Métricas do sistema**

### **Grafana**
- **Porta**: 3001
- **Dashboard**: admin/guardflow

---

## 🛠️ **TROUBLESHOOTING**

### **Se Docker Desktop não iniciar:**
1. **Reiniciar o computador**
2. **Verificar se a virtualização está habilitada no BIOS**
3. **Verificar se o WSL2 está instalado e atualizado**
4. **Reinstalar Docker Desktop se necessário**

### **Se containers não iniciarem:**
1. **Verificar se as portas estão livres**
2. **Verificar logs**: `docker-compose logs`
3. **Rebuild**: `docker-compose build --no-cache`

---

## 📝 **PRÓXIMOS PASSOS**

1. **Iniciar Docker Desktop** (manual)
2. **Executar**: `docker-compose -f config/development/docker-compose.dev.yml up -d`
3. **Verificar**: `docker ps`
4. **Testar**: `curl http://localhost:8000/health`

---

*Última atualização: 15 de Outubro de 2025*
