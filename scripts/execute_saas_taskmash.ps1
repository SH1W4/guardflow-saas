# TaskMash Executor - GuardFlow SaaS Super Escopo
# Executa o plano de desenvolvimento completo do SaaS

Write-Host "🚀 TASKMASH EXECUTOR - GUARDFLOW SAAS SUPER ESCOPO" -ForegroundColor Green
Write-Host ""

# Verificar se Python está instalado
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python não encontrado. Instale Python 3.8+ primeiro." -ForegroundColor Red
    exit 1
}

# Verificar se arquivo TaskMash existe
$taskmashFile = "taskmash_saas_super_escopo.json"
if (-not (Test-Path $taskmashFile)) {
    Write-Host "❌ Arquivo TaskMash não encontrado: $taskmashFile" -ForegroundColor Red
    Write-Host "💡 Certifique-se de que o arquivo existe no diretório atual." -ForegroundColor Yellow
    exit 1
}

# Verificar se script Python existe
$pythonScript = "scripts/execute_saas_taskmash.py"
if (-not (Test-Path $pythonScript)) {
    Write-Host "❌ Script Python não encontrado: $pythonScript" -ForegroundColor Red
    Write-Host "💡 Certifique-se de que o script existe no diretório scripts/." -ForegroundColor Yellow
    exit 1
}

# Executar TaskMash
Write-Host "🚀 Iniciando execução do TaskMash Super Escopo..." -ForegroundColor Green
Write-Host ""

try {
    python $pythonScript
    Write-Host ""
    Write-Host "✅ TaskMash executado com sucesso!" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro ao executar TaskMash: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🎯 Próximos passos:" -ForegroundColor Cyan
Write-Host "1. Revisar relatório de progresso" -ForegroundColor White
Write-Host "2. Implementar tarefas pendentes" -ForegroundColor White
Write-Host "3. Configurar ambiente de desenvolvimento" -ForegroundColor White
Write-Host "4. Iniciar desenvolvimento das APIs Backend" -ForegroundColor White
Write-Host ""
Write-Host "🚀 GuardFlow SaaS Super Escopo em execução!" -ForegroundColor Green
