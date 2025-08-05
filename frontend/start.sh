#!/bin/bash

# Script de inicialização do frontend React
# ETP Generator - Fase 2

echo "🚀 Iniciando ETP Generator Frontend..."
echo "=================================="

# Verificar se o Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado. Por favor, instale o Node.js primeiro."
    exit 1
fi

# Verificar se o npm está instalado
if ! command -v npm &> /dev/null; then
    echo "❌ npm não encontrado. Por favor, instale o npm primeiro."
    exit 1
fi

echo "✅ Node.js versão: $(node --version)"
echo "✅ npm versão: $(npm --version)"
echo ""

# Verificar se as dependências estão instaladas
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependências..."
    npm install
    
    if [ $? -ne 0 ]; then
        echo "❌ Erro ao instalar dependências."
        exit 1
    fi
    
    echo "✅ Dependências instaladas com sucesso!"
    echo ""
fi

# Verificar se o backend está rodando
echo "🔍 Verificando conexão com o backend..."
if curl -s http://localhost:8000/status > /dev/null; then
    echo "✅ Backend está rodando na porta 8000"
else
    echo "⚠️  Backend não está rodando na porta 8000"
    echo "   Para iniciar o backend, execute:"
    echo "   cd .. && python -m uvicorn api:app --reload --port 8000"
    echo ""
fi

# Verificar se a porta 3000 está disponível
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Porta 3000 já está em uso"
    echo "   O React tentará usar uma porta alternativa"
    echo ""
fi

echo "🎯 Iniciando servidor de desenvolvimento..."
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo ""
echo "📝 Funcionalidades disponíveis:"
echo "   • Dashboard com status do sistema"
echo "   • Formulário ETP com assistente IA"
echo "   • Editor WYSIWYG com TinyMCE"
echo "   • Assistente RAG para Lei 14.133"
echo "   • Página de configurações"
echo ""
echo "⚡ Para parar o servidor, pressione Ctrl+C"
echo "=================================="
echo ""

# Iniciar o servidor de desenvolvimento
npm start