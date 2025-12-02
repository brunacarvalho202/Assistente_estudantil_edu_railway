# setup-railway.ps1 - Script de setup automático para Railway (Windows)
# Execute: powershell -ExecutionPolicy Bypass -File setup-railway.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 Setup Automático - Railway + Docker Hub" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Funções auxiliares
function Success($message) {
    Write-Host "✓ $message" -ForegroundColor Green
}

function Error($message) {
    Write-Host "✗ $message" -ForegroundColor Red
}

function Warning($message) {
    Write-Host "⚠ $message" -ForegroundColor Yellow
}

# Verificar pré-requisitos
Write-Host "Verificando pré-requisitos..." -ForegroundColor Cyan
Write-Host ""

# Git
$gitCheck = (Get-Command git -ErrorAction SilentlyContinue) -ne $null
if ($gitCheck) {
    Success "Git instalado"
} else {
    Error "Git não encontrado. Baixe em: https://git-scm.com"
    exit 1
}

# Node.js/npm
$npmCheck = (Get-Command npm -ErrorAction SilentlyContinue) -ne $null
if ($npmCheck) {
    Success "NPM instalado"
} else {
    Warning "NPM não encontrado. Instale Node.js de: https://nodejs.org"
}

# Docker
$dockerCheck = (Get-Command docker -ErrorAction SilentlyContinue) -ne $null
if ($dockerCheck) {
    Success "Docker instalado"
} else {
    Warning "Docker não encontrado. Você poderá testar após instalar Docker"
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "📋 Configuração de Credenciais" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Docker Hub
$DOCKERHUB_USERNAME = Read-Host "Docker Hub Username"
$DOCKERHUB_TOKEN = Read-Host "Docker Hub Token" -AsSecureString
$DOCKERHUB_TOKEN_PLAIN = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToCoTaskMemAlloc($DOCKERHUB_TOKEN))

# Railway Token
$RAILWAY_TOKEN = Read-Host "Railway Token" -AsSecureString
$RAILWAY_TOKEN_PLAIN = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToCoTaskMemAlloc($RAILWAY_TOKEN))

# Gemini API Key
$GEMINI_API_KEY = Read-Host "Gemini API Key" -AsSecureString
$GEMINI_API_KEY_PLAIN = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToCoTaskMemAlloc($GEMINI_API_KEY))

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🔐 Configurando Secrets do GitHub" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar GitHub CLI
$ghCheck = (Get-Command gh -ErrorAction SilentlyContinue) -ne $null
if ($ghCheck) {
    Warning "Você pode usar GitHub CLI para adicionar secrets automaticamente:"
    Write-Host ""
    Write-Host "gh secret set DOCKERHUB_USERNAME --body ""$DOCKERHUB_USERNAME"""
    Write-Host "gh secret set DOCKERHUB_TOKEN --body ""$DOCKERHUB_TOKEN_PLAIN"""
    Write-Host "gh secret set RAILWAY_TOKEN --body ""$RAILWAY_TOKEN_PLAIN"""
} else {
    Warning "GitHub CLI (gh) não instalado. Adicione os secrets manualmente:"
    Write-Host ""
    Write-Host "1. Acesse: https://github.com/seu-usuario/EDU_ASSISTANT_AI/settings/secrets/actions"
    Write-Host "2. Clique em 'New repository secret'"
    Write-Host "3. Adicione:"
    Write-Host ""
    Write-Host "   Secret: DOCKERHUB_USERNAME"
    Write-Host "   Value: $DOCKERHUB_USERNAME"
    Write-Host ""
    Write-Host "   Secret: DOCKERHUB_TOKEN"
    Write-Host "   Value: (seu token)"
    Write-Host ""
    Write-Host "   Secret: RAILWAY_TOKEN"
    Write-Host "   Value: (seu token)"
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚂 Criando Projeto no Railway" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Instalar Railway CLI
$railwayCheck = (Get-Command railway -ErrorAction SilentlyContinue) -ne $null
if (-not $railwayCheck) {
    Write-Host "Instalando Railway CLI..."
    npm install -g @railway/cli
    Success "Railway CLI instalado"
} else {
    Success "Railway CLI já instalado"
}

Write-Host ""
Write-Host "Faça login no Railway:"
railway login --token "$RAILWAY_TOKEN_PLAIN"
Success "Login no Railway realizado"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "⚙️  Configuração Local" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Criar .env.local
$envLocalPath = ".env.local"
if (-not (Test-Path $envLocalPath)) {
    @"
ENV=local
GEMINI_API_KEY=$GEMINI_API_KEY_PLAIN
LLM_PROVIDER=gemini
MODEL_NAME=models/gemini-1.5-flash-001
"@ | Out-File -FilePath $envLocalPath -Encoding UTF8
    Success ".env.local criado"
} else {
    Warning ".env.local já existe, não foi sobrescrito"
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🐳 Teste Local com Docker (Opcional)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$testLocal = Read-Host "Deseja testar a aplicação localmente com Docker? (s/n)"

if ($testLocal -eq "s" -or $testLocal -eq "S") {
    if ($dockerCheck) {
        Write-Host "Construindo imagem Docker..."
        docker build -t edu-assistant-ai:latest .
        Success "Imagem construída"
        
        Write-Host ""
        Write-Host "Iniciando container..."
        docker run -it --rm `
            -p 8000:8000 `
            -p 8501:8501 `
            -e GEMINI_API_KEY="$GEMINI_API_KEY_PLAIN" `
            -e ENV=development `
            edu-assistant-ai:latest
    } else {
        Error "Docker não está instalado. Pule este passo."
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "📍 Próximos Passos" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Configure variáveis de ambiente no Railway:"
Write-Host "   https://railway.app/dashboard"
Write-Host ""
Write-Host "2. Faça um push para master para disparar o workflow:"
Write-Host "   git add ."
Write-Host "   git commit -m 'Migração para Railway'"
Write-Host "   git push origin master"
Write-Host ""
Write-Host "3. Monitore o deployment:"
Write-Host "   https://github.com/seu-usuario/EDU_ASSISTANT_AI/actions"
Write-Host ""
Write-Host "4. Acesse sua aplicação após deploy:"
Write-Host "   https://seu-dominio-railway.railway.app/docs"
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Success "Setup concluído!"
Write-Host "========================================" -ForegroundColor Cyan
