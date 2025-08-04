# Plano de Implementação: Memória de Conversa para o Assistente

## Problema Identificado

O assistente está perdendo o contexto da conversa porque apenas a pergunta atual é enviada para o modelo de IA, sem o histórico das mensagens anteriores. Isso resulta em respostas descontextualizadas e perda de continuidade na conversa.

## Análise Técnica

### Estado Atual
- O histórico é armazenado em `st.session_state.messages` no `app.py`
- A classe `RagChain` no `integrador.py` só processa a pergunta atual
- O método `invoke()` da `RagChain` não recebe o histórico da conversa

### Arquitetura da Solução

```
Fluxo Atual:
Pergunta → RagChain.invoke(pergunta) → Resposta

Fluxo Proposto:
Pergunta + Histórico → RagChain.invoke_with_history(pergunta, histórico) → Resposta
```

## Especificações de Implementação

### 1. Modificações na Classe RagChain (`integrador.py`)

#### 1.1 Novo Método `invoke_with_history`
```python
def invoke_with_history(self, question: str, chat_history: list) -> str:
    """
    Invoca a cadeia de RAG com histórico de conversa.
    
    Args:
        question (str): A pergunta atual do usuário
        chat_history (list): Lista de mensagens anteriores no formato:
                           [{"role": "user", "content": "..."}, 
                            {"role": "assistant", "content": "..."}]
    
    Returns:
        str: A resposta gerada pela IA considerando o contexto
    """
```

#### 1.2 Novo Template de Prompt
O template deve incluir:
- Contexto dos documentos (RAG)
- Histórico da conversa
- Pergunta atual
- Instruções para manter continuidade

```python
template = """
Você é um assistente especialista em licitações e contratos públicos, com profundo conhecimento da Lei 14.133/2021 e de manuais de boas práticas.
Sua tarefa é fornecer orientações claras e práticas para os usuários, baseando-se no contexto fornecido e mantendo a continuidade da conversa.

Contexto dos Documentos:
{context}

Histórico da Conversa:
{chat_history}

Pergunta Atual:
{question}

Instruções:
1. **Mantenha a Continuidade:** Considere todo o histórico da conversa para fornecer respostas coerentes e contextualizadas.
2. **Seja um Orientador:** Sintetize os pontos relevantes do contexto para fornecer recomendações práticas.
3. **Fundamente sua Resposta:** Baseie suas orientações nas informações do contexto e cite fontes quando possível.
4. **Seja Prático:** Traduza a linguagem técnica para orientações aplicáveis no dia a dia.
5. **Estruture a Resposta:** Organize de forma lógica para facilitar o entendimento.
6. **Referências Contextuais:** Quando apropriado, faça referência a pontos discutidos anteriormente na conversa.
"""
```

#### 1.3 Função Auxiliar para Formatação do Histórico
```python
def _format_chat_history(self, chat_history: list) -> str:
    """
    Formata o histórico de chat para inclusão no prompt.
    
    Args:
        chat_history (list): Lista de mensagens
        
    Returns:
        str: Histórico formatado
    """
    if not chat_history:
        return "Nenhuma conversa anterior."
    
    formatted_history = []
    for message in chat_history[-6:]:  # Últimas 6 mensagens para não sobrecarregar
        role = "Usuário" if message["role"] == "user" else "Assistente"
        formatted_history.append(f"{role}: {message['content']}")
    
    return "\n".join(formatted_history)
```

### 2. Modificações no App.py

#### 2.1 Atualização da Chamada do RAG
Localização: Linha 585 aproximadamente

```python
# Código atual:
resposta = rag_chain.invoke(prompt)

# Código proposto:
resposta = rag_chain.invoke_with_history(prompt, st.session_state.messages)
```

#### 2.2 Limitação do Histórico (Opcional)
Para evitar prompts muito longos, limitar o histórico:

```python
# Manter apenas as últimas 10 mensagens (5 pares pergunta-resposta)
max_history = 10
history_to_send = st.session_state.messages[-max_history:] if len(st.session_state.messages) > max_history else st.session_state.messages
resposta = rag_chain.invoke_with_history(prompt, history_to_send)
```

### 3. Melhorias Adicionais

#### 3.1 Indicador Visual de Contexto
Adicionar um indicador na interface quando o assistente está usando contexto de conversas anteriores:

```python
if len(st.session_state.messages) > 0:
    st.info("💬 Considerando o contexto da conversa anterior...")
```

#### 3.2 Botão para Limpar Histórico
Permitir que o usuário reinicie a conversa:

```python
if st.button("🔄 Nova Conversa"):
    st.session_state.messages = []
    st.rerun()
```

#### 3.3 Resumo de Contexto
Para conversas muito longas, implementar um sistema de resumo:

```python
def _summarize_old_context(self, messages: list) -> str:
    """
    Resume mensagens antigas para manter contexto sem sobrecarregar o prompt.
    """
    # Implementar lógica de resumo usando o próprio LLM
```

## Benefícios Esperados

1. **Continuidade da Conversa:** O assistente lembrará do contexto anterior
2. **Respostas Mais Precisas:** Poderá fazer referências a informações já discutidas
3. **Experiência Melhorada:** Conversas mais naturais e fluidas
4. **Eficiência:** Usuário não precisará repetir informações

## Considerações de Performance

1. **Tamanho do Prompt:** Limitar histórico para evitar prompts muito longos
2. **Tokens:** Monitorar uso de tokens com histórico incluído
3. **Cache:** Considerar cache para conversas similares
4. **Memória:** Gerenciar adequadamente o `session_state`

## Testes Recomendados

1. **Teste de Continuidade:** Fazer uma pergunta, depois uma pergunta relacionada
2. **Teste de Contexto:** Perguntar "sobre o que estamos falando?"
3. **Teste de Referência:** Usar pronomes que referenciem mensagens anteriores
4. **Teste de Limite:** Verificar comportamento com muitas mensagens

## Cronograma de Implementação

1. **Fase 1:** Modificar classe RagChain (30 min)
2. **Fase 2:** Atualizar chamada no app.py (15 min)
3. **Fase 3:** Testes básicos (15 min)
4. **Fase 4:** Melhorias adicionais (30 min)

**Total Estimado:** 1h30min

## Arquivos a Modificar

1. `integrador.py` - Classe RagChain
2. `app.py` - Chamada do assistente
3. `plano_memoria_conversa.md` - Este documento (para referência)

## Próximos Passos

1. Implementar as modificações na classe RagChain
2. Atualizar a chamada no app.py
3. Testar a funcionalidade
4. Ajustar conforme necessário
5. Documentar as mudanças