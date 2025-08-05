#!/bin/bash

# Script de instalação ETP Generator - Python 3.11
# Instalação otimizada e testada

echo "🚀 ETP Generator - Instalação Completa"
echo "====================================="

# Verificar se Python 3.11 está disponível
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
    echo "✅ Python 3.11 encontrado"
elif command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+')
    if [[ "$PYTHON_VERSION" == "3.11" ]]; then
        PYTHON_CMD="python3"
        echo "✅ Python 3.11 encontrado (python3)"
    else
        echo "⚠️  Python 3.11 não encontrado. Versão atual: $PYTHON_VERSION"
        echo "   Continuando com a versão disponível..."
        PYTHON_CMD="python3"
    fi
else
    echo "❌ Python não encontrado. Instale Python 3.11 primeiro."
    exit 1
fi

# Verificar se Node.js está instalado
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✅ Node.js encontrado: $NODE_VERSION"
else
    echo "❌ Node.js não encontrado. Instale Node.js primeiro."
    echo "   Download: https://nodejs.org/"
    exit 1
fi

echo ""
echo "📦 INSTALAÇÃO DO BACKEND"
echo "========================"

# Criar ambiente virtual com Python 3.11
if [ ! -d "venv" ]; then
    echo "🔧 Criando ambiente virtual com Python 3.11..."
    $PYTHON_CMD -m venv venv
    echo "✅ Ambiente virtual criado"
else
    echo "✅ Ambiente virtual já existe"
fi

# Ativar ambiente virtual
echo "🔄 Ativando ambiente virtual..."
source venv/bin/activate

# Verificar versão do Python no venv
VENV_PYTHON_VERSION=$(python --version 2>&1)
echo "✅ Python no venv: $VENV_PYTHON_VERSION"

# Atualizar pip
echo "⬆️  Atualizando pip..."
pip install --upgrade pip

# Instalar dependências do backend
echo "📦 Instalando dependências do backend..."
pip install -r requirements_api.txt

# Verificar instalação crítica
echo "🔍 Verificando instalação do backend..."
python -c "
import sys
print(f'✅ Python: {sys.version}')

try:
    import pandas as pd
    print(f'✅ Pandas: {pd.__version__}')
except ImportError as e:
    print(f'❌ Pandas: {e}')

try:
    import fastapi
    print(f'✅ FastAPI: {fastapi.__version__}')
except ImportError as e:
    print(f'❌ FastAPI: {e}')

try:
    import langchain
    print(f'✅ LangChain: {langchain.__version__}')
except ImportError as e:
    print(f'❌ LangChain: {e}')

try:
    import streamlit
    print(f'✅ Streamlit: {streamlit.__version__}')
except ImportError as e:
    print(f'❌ Streamlit: {e}')
"

echo ""
echo "🎨 INSTALAÇÃO DO FRONTEND"
echo "========================="

# Navegar para o diretório frontend
cd frontend

# Verificar se package.json existe
if [ ! -f "package.json" ]; then
    echo "❌ package.json não encontrado no diretório frontend"
    exit 1
fi

# Instalar dependências do frontend
echo "📦 Instalando dependências do frontend..."
npm install

# Verificar se a instalação foi bem-sucedida
if [ $? -eq 0 ]; then
    echo "✅ Dependências do frontend instaladas com sucesso"
else
    echo "❌ Erro na instalação das dependências do frontend"
    exit 1
fi

# Voltar ao diretório raiz
cd ..

echo ""
echo "🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!"
echo "===================================="
echo ""
echo "🚀 Para iniciar o sistema:"
echo ""
echo "1️⃣  BACKEND (Terminal 1):"
echo "   source venv/bin/activate"
echo "   python -m uvicorn api:app --reload --port 8000"
echo ""
echo "2️⃣  FRONTEND (Terminal 2):"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "3️⃣  ACESSO:"
echo "   • Frontend: http://localhost:3000"
echo "   • Backend:  http://localhost:8000"
echo "   • Docs API: http://localhost:8000/docs"
echo ""
echo "⚙️  CONFIGURAÇÃO:"
echo "   1. Acesse http://localhost:3000"
echo "   2. Vá em 'Configurações'"
echo "   3. Configure sua chave OpenAI ou Anthropic"
echo "   4. Teste a conexão"
echo "   5. Sistema pronto para uso!"
echo ""
echo "📚 FUNCIONALIDADES:"
echo "   • Dashboard com status do sistema"
echo "   • Formulário ETP com assistente IA"
echo "   • Editor WYSIWYG com TinyMCE"
echo "   • Assistente RAG para Lei 14.133"
echo "   • Sistema de configurações"
echo ""
echo "🆘 SUPORTE:"
echo "   • Verifique os logs se houver problemas"
echo "   • Certifique-se de que as portas 3000 e 8000 estão livres"
echo "   • Configure pelo menos uma API (OpenAI ou Anthropic)"