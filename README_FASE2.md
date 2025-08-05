# ETP Generator - Fase 2: Editor Integrado de Documentos

## 🎯 Visão Geral

A Fase 2 do ETP Generator implementa um **Editor Integrado de Documentos** com interface React moderna, substituindo a interface Streamlit por uma solução mais robusta e profissional.

## 🏗️ Arquitetura Híbrida

### Backend Python (Preservado)
- **FastAPI**: API REST completa expondo toda funcionalidade Python
- **Integrador.py**: Lógica de negócio do assistente inteligente (800+ linhas)
- **Processamento IA**: Mantém todos os prompts especializados e análise contextual
- **RAG System**: Sistema de consulta à Lei 14.133 com memória de conversa

### Frontend React (Novo)
- **Interface Moderna**: UI/UX profissional com Ant Design
- **Editor WYSIWYG**: TinyMCE integrado para edição rica de documentos
- **Componentes Reutilizáveis**: Arquitetura modular e escalável
- **Estado Reativo**: Gerenciamento de estado com React Query

## 📁 Estrutura do Projeto

```
ETP_beta01/
├── 📄 Backend Python
│   ├── api.py                 # FastAPI - API REST completa
│   ├── integrador.py          # Lógica de negócio (preservada)
│   ├── app.py                 # Interface Streamlit (mantida)
│   └── requirements_api.txt   # Dependências do backend
│
├── 🎨 Frontend React
│   ├── package.json           # Configuração e dependências
│   ├── src/
│   │   ├── App.js            # Componente principal
│   │   ├── App.css           # Estilos globais
│   │   ├── services/
│   │   │   └── apiService.js # Camada de comunicação com API
│   │   └── components/
│   │       ├── Layout/       # Header e Sidebar
│   │       ├── Dashboard/    # Página inicial
│   │       ├── ETP/          # Formulário e Editor ETP
│   │       ├── RAG/          # Assistente Lei 14.133
│   │       └── Config/       # Configurações do sistema
│   └── start.sh              # Script de inicialização
│
└── 📚 Documentação
    ├── README_FASE2.md       # Este arquivo
    └── PLANO_FASE2_EDITOR_INTEGRADO.md
```

## 🚀 Funcionalidades Implementadas

### 1. Dashboard Inteligente
- **Status do Sistema**: Monitoramento em tempo real dos serviços
- **Estatísticas**: Contadores de ETPs criados, consultas RAG, análises IA
- **Navegação Rápida**: Acesso direto a todas as funcionalidades
- **Alertas Contextuais**: Notificações sobre configuração necessária

### 2. Formulário ETP com Assistente IA
- **11 Campos Críticos**: Cada campo com assistente inteligente integrado
- **Análise Contextual**: IA analisa relação entre campos
- **Validação TRT-2**: Conformidade com normas técnicas
- **Sugestões Inteligentes**: Melhorias automáticas de texto
- **Scores de Qualidade**: Pontuação de 0-10 para cada campo

### 3. Editor WYSIWYG Avançado
- **TinyMCE Integrado**: Editor rico com todas as funcionalidades
- **Template ETP**: Estrutura pré-definida com 17 seções TRT-2
- **Assistente IA no Editor**: Melhoria de texto selecionado
- **Exportação**: HTML, PDF e outros formatos
- **Salvamento**: Persistência local e na nuvem

### 4. Assistente RAG Lei 14.133
- **Chat Inteligente**: Interface conversacional moderna
- **Memória de Conversa**: Contexto mantido entre perguntas
- **Fontes Citadas**: Referências aos documentos consultados
- **Perguntas Sugeridas**: Guias para consultas comuns
- **Histórico Persistente**: Conversas salvas localmente

### 5. Sistema de Configurações
- **APIs Múltiplas**: Suporte OpenAI e Anthropic
- **Status em Tempo Real**: Monitoramento de conexões
- **Configuração Visual**: Interface intuitiva para setup
- **Teste de Conexão**: Validação automática das configurações

## 🛠️ Tecnologias Utilizadas

### Backend
- **FastAPI**: Framework web moderno e rápido
- **Python 3.8+**: Linguagem principal
- **LangChain**: Framework para aplicações LLM
- **OpenAI/Anthropic**: Provedores de IA
- **Uvicorn**: Servidor ASGI

### Frontend
- **React 18**: Biblioteca de interface
- **Ant Design**: Biblioteca de componentes UI
- **TinyMCE**: Editor WYSIWYG
- **React Query**: Gerenciamento de estado servidor
- **Styled Components**: CSS-in-JS
- **Axios**: Cliente HTTP

## 📦 Instalação e Configuração

### 1. Pré-requisitos
```bash
# Python 3.8+
python --version

# Node.js 16+
node --version

# npm ou yarn
npm --version
```

### 2. Backend (API)
```bash
# Instalar dependências Python
pip install -r requirements_api.txt

# Iniciar servidor FastAPI
python -m uvicorn api:app --reload --port 8000
```

### 3. Frontend (React)
```bash
# Navegar para o diretório frontend
cd frontend

# Instalar dependências
npm install

# Iniciar servidor de desenvolvimento
npm start
# ou usar o script personalizado
./start.sh
```

### 4. Configuração das APIs
1. Acesse http://localhost:3000
2. Vá para "Configurações"
3. Configure pelo menos uma API:
   - **OpenAI**: Obtenha em https://platform.openai.com
   - **Anthropic**: Obtenha em https://console.anthropic.com
4. Teste a conexão
5. Ative os serviços desejados

## 🎮 Como Usar

### 1. Criar um ETP
1. Acesse "Formulário ETP"
2. Preencha os campos obrigatórios
3. Use os botões 🤖 para análise IA
4. Aplique as melhorias sugeridas
5. Gere o ETP final

### 2. Editar Documentos
1. Acesse "Editor de ETP"
2. Use o template pré-definido
3. Edite com ferramentas WYSIWYG
4. Selecione texto e use assistente IA
5. Salve e exporte o documento

### 3. Consultar Lei 14.133
1. Acesse "Assistente Lei 14.133"
2. Faça perguntas sobre licitações
3. Use perguntas sugeridas
4. Consulte o histórico de conversas

## 🔧 Desenvolvimento

### Estrutura de Componentes
```
components/
├── Layout/
│   ├── Header.js          # Cabeçalho com status
│   └── Sidebar.js         # Menu lateral
├── Dashboard/
│   └── Dashboard.js       # Página inicial
├── ETP/
│   ├── EtpForm.js        # Formulário com IA
│   └── EtpEditor.js      # Editor WYSIWYG
├── RAG/
│   └── RagAssistant.js   # Chat Lei 14.133
└── Config/
    └── ConfigPage.js     # Configurações
```



### API Service Layer
```javascript
// Exemplo de uso do apiService
import { apiService } from './services/apiService';

// Gerar ETP
const etp = await apiService.gerarEtp(formData);

// Analisar campo
const analise = await apiService.analisarCampo(
  'descricao_necessidade', 
  texto, 
  contexto
);

// Consultar RAG
const resposta = await apiService.consultarRag(
  pergunta, 
  historico
);
```

## 🧪 Testes

### Backend
```bash
# Testar API diretamente
curl http://localhost:8000/status

# Testar geração ETP
curl -X POST http://localhost:8000/gerar-etp \
  -H "Content-Type: application/json" \
  -d '{"descricao_necessidade": "Teste"}'
```

### Frontend
```bash
# Executar testes
npm test

# Build de produção
npm run build
```

## 🚀 Deploy

### Backend
```bash
# Produção com Gunicorn
gunicorn api:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend
```bash
# Build otimizado
npm run build

# Servir arquivos estáticos
npx serve -s build
```

## 📈 Melhorias Futuras (Fase 3)

1. **Múltiplos Tipos de Documento**
   - Contratos
   - Termos de Referência
   - Editais

2. **Templates Organizacionais**
   - Templates personalizados
   - Biblioteca de modelos
   - Versionamento

3. **Colaboração**
   - Edição simultânea
   - Comentários
   - Aprovações

4. **Integrações**
   - Sistemas ERP
   - Assinatura digital
   - Workflow automático

## 🐛 Troubleshooting

### Problemas Comuns

**Backend não conecta:**
```bash
# Verificar se a porta está livre
lsof -i :8000

# Reinstalar dependências
pip install -r requirements_api.txt --force-reinstall
```

**Frontend não carrega:**
```bash
# Limpar cache
npm start -- --reset-cache

# Reinstalar node_modules
rm -rf node_modules package-lock.json
npm install
```

**APIs não funcionam:**
1. Verifique as chaves de API
2. Teste conexão na página de configurações
3. Consulte logs do backend

## 📞 Suporte

Para dúvidas e suporte:
1. Consulte a documentação completa
2. Verifique os logs do sistema
3. Teste as configurações de API
4. Reinicie os serviços se necessário

---

## 🎉 Conclusão

A Fase 2 transforma o ETP Generator em uma solução profissional e escalável, mantendo toda a inteligência do backend Python enquanto oferece uma interface moderna e intuitiva. O sistema está pronto para uso em produção e preparado para as evoluções da Fase 3.

**Status**: ✅ Implementação Completa
**Próxima Fase**: Múltiplos tipos de documento e templates organizacionais