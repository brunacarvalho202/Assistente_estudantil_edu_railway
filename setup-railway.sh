#!/bin/bash
# setup-railway.sh - Script de setup automático para Railway

set -e

echo "========================================"
echo "🚀 Setup Automático - Railway + Docker Hub"
echo "========================================"
echo ""

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para exibir sucesso
success() {
    echo -e "${GREEN}✓${NC} $1"
}

# Função para exibir erro
error() {
    echo -e "${RED}✗${NC} $1"
}

# Função para exibir aviso
warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Verificar pré-requisitos
echo "Verificando pré-requisitos..."
echo ""

# Git
if command -v git &> /dev/null; then
    success "Git instalado"
else
    error "Git não encontrado. Por favor, instale git: https://git-scm.com"
    exit 1
fi

# Node.js/npm (para Railway CLI)
if command -v npm &> /dev/null; then
    success "NPM instalado"
else
    warning "NPM não encontrado. Você precisará instalar Railway CLI manualmente com: npm install -g @railway/cli"
fi

# Docker (opcional)
if command -v docker &> /dev/null; then
    success "Docker instalado"
else
    warning "Docker não encontrado. Você poderá testar localmente depois de instalar Docker"
fi

echo ""
echo "========================================"
echo "📋 Configuração de Credenciais"
echo "========================================"
echo ""

# Docker Hub
read -p "Docker Hub Username: " DOCKERHUB_USERNAME
read -s -p "Docker Hub Token (será ocultado): " DOCKERHUB_TOKEN
echo ""

# Railway Token
read -s -p "Railway Token (será ocultado): " RAILWAY_TOKEN
echo ""

# Gemini API Key
read -s -p "Gemini API Key (será ocultado): " GEMINI_API_KEY
echo ""

echo ""
echo "========================================"
echo "🔐 Configurando Secrets do GitHub"
echo "========================================"
echo ""

# Verificar se gh CLI está instalado
if command -v gh &> /dev/null; then
    warning "Você pode usar GitHub CLI para adicionar secrets automaticamente:"
    echo ""
    echo "gh secret set DOCKERHUB_USERNAME -b\"$DOCKERHUB_USERNAME\""
    echo "gh secret set DOCKERHUB_TOKEN -b\"$DOCKERHUB_TOKEN\""
    echo "gh secret set RAILWAY_TOKEN -b\"$RAILWAY_TOKEN\""
else
    warning "GitHub CLI (gh) não instalado. Adicione os secrets manualmente:"
    echo ""
    echo "1. Acesse: https://github.com/seu-usuario/EDU_ASSISTANT_AI/settings/secrets/actions"
    echo "2. Clique em 'New repository secret'"
    echo "3. Adicione:"
    echo ""
    echo "   Secret: DOCKERHUB_USERNAME"
    echo "   Value: $DOCKERHUB_USERNAME"
    echo ""
    echo "   Secret: DOCKERHUB_TOKEN"
    echo "   Value: (seu token)"
    echo ""
    echo "   Secret: RAILWAY_TOKEN"
    echo "   Value: (seu token)"
fi

echo ""
echo "========================================"
echo "🚂 Criando Projeto no Railway"
echo "========================================"
echo ""

# Instalar Railway CLI
if ! command -v railway &> /dev/null; then
    echo "Instalando Railway CLI..."
    npm install -g @railway/cli
    success "Railway CLI instalado"
else
    success "Railway CLI já instalado"
fi

echo ""
echo "Faça login no Railway:"
railway login --token "$RAILWAY_TOKEN"
success "Login no Railway realizado"

echo ""
echo "========================================"
echo "⚙️  Configuração Local"
echo "========================================"
echo ""

# Criar .env.local
if [ ! -f .env.local ]; then
    cat > .env.local << EOF
ENV=local
GEMINI_API_KEY=$GEMINI_API_KEY
LLM_PROVIDER=gemini
MODEL_NAME=models/gemini-1.5-flash-001
EOF
    success ".env.local criado"
else
    warning ".env.local já existe, não foi sobrescrito"
fi

echo ""
echo "========================================"
echo "🐳 Teste Local com Docker (Opcional)"
echo "========================================"
echo ""

read -p "Deseja testar a aplicação localmente com Docker? (s/n) " -n 1 -r TEST_LOCAL
echo ""

if [[ $TEST_LOCAL =~ ^[Ss]$ ]]; then
    if command -v docker &> /dev/null; then
        echo "Construindo imagem Docker..."
        docker build -t edu-assistant-ai:latest .
        success "Imagem construída"
        
        echo ""
        echo "Iniciando container..."
        docker run -it --rm \
            -p 8000:8000 \
            -p 8501:8501 \
            -e GEMINI_API_KEY="$GEMINI_API_KEY" \
            -e ENV=development \
            edu-assistant-ai:latest
    else
        error "Docker não está instalado. Pule este passo."
    fi
fi

echo ""
echo "========================================"
echo "📍 Próximos Passos"
echo "========================================"
echo ""
echo "1. Configure variáveis de ambiente no Railway:"
echo "   https://railway.app/dashboard"
echo ""
echo "2. Faça um push para master para disparar o workflow:"
echo "   git add ."
echo "   git commit -m 'Migração para Railway'"
echo "   git push origin master"
echo ""
echo "3. Monitore o deployment:"
echo "   https://github.com/seu-usuario/EDU_ASSISTANT_AI/actions"
echo ""
echo "4. Acesse sua aplicação após deploy:"
echo "   https://seu-dominio-railway.railway.app/docs"
echo ""
echo "========================================"
success "Setup concluído!"
echo "========================================"
