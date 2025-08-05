# 🚀 Guia de Início Rápido - ETP Generator

## ⚡ Instalação em 3 Passos

### 1. Executar Instalação Automática
```bash
# Tornar o script executável
chmod +x install.sh

# Executar instalação completa
./install.sh
```

### 2. Iniciar o Sistema

**Terminal 1 - Backend:**
```bash
source venv/bin/activate
python -m uvicorn api:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### 3. Configurar APIs
1. Acesse http://localhost:3000
2. Clique em "Configurações" 
3. Configure sua chave OpenAI ou Anthropic
4. Teste a conexão
5. ✅ Sistema pronto!

---

## 🔧 Solução de Problemas

### Erro de Pandas com Python 3.13
Se você estiver usando Python 3.13 e tiver erro de pandas:

```bash
# Usar Python 3.11 (recomendado)
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements_api.txt
```

### Porta em Uso
```bash
# Verificar portas ocupadas
lsof -i :3000  # Frontend
lsof -i :8000  # Backend

# Matar processo se necessário
kill -9 <PID>
```

### Dependências do Frontend
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 🎯 Funcionalidades Principais

### 📊 Dashboard
- Status em tempo real dos serviços
- Estatísticas de uso
- Navegação rápida

### 📝 Formulário ETP
- 11 campos com assistente IA
- Análise contextual automática
- Validação TRT-2
- Scores de qualidade

### ✏️ Editor WYSIWYG
- TinyMCE integrado
- Template ETP pré-definido
- Assistente IA no texto
- Exportação múltiplos formatos

### 🤖 Assistente RAG
- Chat sobre Lei 14.133
- Memória de conversa
- Fontes citadas
- Perguntas sugeridas

### ⚙️ Configurações
- APIs OpenAI/Anthropic
- Status visual
- Teste de conexão

---

## 🔑 Configuração de APIs

### OpenAI
1. Acesse https://platform.openai.com
2. Crie uma conta/faça login
3. Vá em "API Keys"
4. Crie uma nova chave
5. Cole no sistema: `sk-...`

### Anthropic
1. Acesse https://console.anthropic.com
2. Crie uma conta/faça login
3. Vá em "API Keys"
4. Crie uma nova chave
5. Cole no sistema: `sk-ant-...`

---

## 📱 URLs do Sistema

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Streamlit** (legado): http://localhost:8501

---

## 🆘 Suporte Rápido

### Logs Importantes
```bash
# Backend logs
tail -f logs/api.log

# Frontend logs
# Visíveis no terminal onde rodou npm start
```

### Comandos Úteis
```bash
# Reiniciar backend
source venv/bin/activate
python -m uvicorn api:app --reload --port 8000

# Reiniciar frontend
cd frontend
npm start

# Verificar status
curl http://localhost:8000/status
```

### Problemas Comuns

**"Erro ao conectar com backend"**
- ✅ Backend está rodando na porta 8000?
- ✅ Ambiente virtual ativado?
- ✅ Dependências instaladas?

**"Configure as APIs"**
- ✅ Chave OpenAI ou Anthropic configurada?
- ✅ Chave válida e com créditos?
- ✅ Teste de conexão passou?

**"Componente não carrega"**
- ✅ Frontend rodando na porta 3000?
- ✅ Dependências npm instaladas?
- ✅ Console do browser sem erros?

---

## 🎉 Pronto para Usar!

Após seguir este guia, você terá:
- ✅ Sistema completo funcionando
- ✅ Interface React moderna
- ✅ Assistente IA configurado
- ✅ Editor WYSIWYG ativo
- ✅ Chat RAG operacional

**Próximo passo**: Criar seu primeiro ETP! 🚀