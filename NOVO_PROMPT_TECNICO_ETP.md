# 📝 NOVO PROMPT TÉCNICO ETP - Manual TRT-2

## 📅 Data: 04/08/2025
## 🎯 Versão: 2.0.0 - Conformidade Manual TRT-2

---

## 🔍 **ANÁLISE DO PROMPT ATUAL**

### **❌ Problemas Identificados:**

1. **Estrutura Informal**: Usa bullets e linguagem coloquial
2. **Seções Incompletas**: Faltam 10 das 17 seções obrigatórias do Manual TRT-2
3. **Não Conformidade Legal**: Não segue estrutura da Lei 14.133/2021
4. **Linguagem Inadequada**: Não usa terminologia técnica formal
5. **Ausência de Fundamentação**: Não cita base legal obrigatória

### **📋 Seções Ausentes (Manual TRT-2):**
- Histórico de Contratações Similares
- Análise de Riscos (Mapa de Riscos)
- Critérios de Sustentabilidade
- Estimativa de Quantidades
- Justificativa de Parcelamento/Agrupamento
- Previsão de Contratações Futuras
- Dependência do Contratado
- Transição Contratual
- Declaração de Adequação Orçamentária
- Aprovação da Autoridade Competente

---

## 🏗️ **NOVO PROMPT TÉCNICO BASEADO NO MANUAL TRT-2**

### **Estrutura Completa (17 Seções Obrigatórias):**

```python
def _construct_prompt_tecnico_trt2(self, dados_etp: Dict[str, Any]) -> str:
    """Constrói prompt técnico conforme Manual TRT-2 e Lei 14.133/2021."""
    
    # Formatar valores monetários
    valor_min = f"R$ {dados_etp['valor_minimo']:,.2f}".replace(",", "X").replace(
        ".", ",").replace("X", ".") if dados_etp['valor_minimo'] else "Não informado"
    valor_med = f"R$ {dados_etp['valor_medio']:,.2f}".replace(",", "X").replace(
        ".", ",").replace("X", ".") if dados_etp['valor_medio'] else "Não informado"
    valor_max = f"R$ {dados_etp['valor_maximo']:,.2f}".replace(",", "X").replace(
        ".", ",").replace("X", ".") if dados_etp['valor_maximo'] else "Não informado"

    prompt_tecnico = f"""
    Elabore um Estudo Técnico Preliminar (ETP) em conformidade com o Manual de Compras e Licitações do TRT-2 e a Lei 14.133/2021.

    IMPORTANTE: O documento deve seguir RIGOROSAMENTE a estrutura técnica formal de documentos governamentais, com linguagem jurídico-administrativa adequada e fundamentação legal completa.

    ## DADOS FORNECIDOS PELO USUÁRIO:

    **IDENTIFICAÇÃO DA NECESSIDADE:**
    - Descrição do problema: {dados_etp['descricao_problema']}
    - Áreas organizacionais impactadas: {', '.join(dados_etp['areas_impactadas'])}
    - Partes interessadas (stakeholders): {', '.join(dados_etp['stakeholders'])}

    **REQUISITOS TÉCNICOS:**
    - Requisitos funcionais: {dados_etp['requisitos_funcionais']}
    - Requisitos não funcionais: {dados_etp['requisitos_nao_funcionais']}

    **ANÁLISE DE MERCADO REALIZADA:**
    - Soluções identificadas no mercado: {dados_etp['solucoes_mercado']}
    - Análise comparativa: {dados_etp['comparativo_solucoes']}
    - Faixa de preços pesquisada: Mínimo {valor_min}, Médio {valor_med}, Máximo {valor_max}

    **SOLUÇÃO TÉCNICA PROPOSTA:**
    - Descrição da solução escolhida: {dados_etp['solucao_proposta']}
    - Fundamentação da escolha: {dados_etp['justificativa_escolha']}

    **ESTRATÉGIA DE IMPLEMENTAÇÃO:**
    - Metodologia de implantação: {dados_etp['estrategia_implantacao']}
    - Cronograma previsto: {dados_etp['cronograma']}
    - Recursos organizacionais necessários: {dados_etp['recursos_necessarios']}
    - Providências preparatórias: {dados_etp['providencias']}

    **ANÁLISE DE BENEFÍCIOS:**
    - Benefícios esperados: {dados_etp['beneficios']}
    - Beneficiários identificados: {dados_etp['beneficiarios']}

    **CONCLUSÃO TÉCNICA:**
    - Declaração de viabilidade: A contratação foi avaliada como {dados_etp['declaracao_viabilidade']}

    ## ESTRUTURA OBRIGATÓRIA DO ETP (Manual TRT-2):

    Elabore o documento seguindo EXATAMENTE esta estrutura numerada:

    **1. DESCRIÇÃO DA NECESSIDADE**
    - Contextualização do problema ou oportunidade identificada
    - Análise de conformidade com Decreto 9.507/2018 (execução direta vs. terceirização)
    - Justificativa técnica para a contratação
    - Identificação de terceirização lícita/ilícita quando aplicável

    **2. HISTÓRICO DE CONTRATAÇÕES SIMILARES**
    - Levantamento de contratações anteriores relacionadas
    - Lições aprendidas de contratos similares
    - Análise de relatórios de gestão contratuais anteriores
    - Identificação de oportunidades de melhoria

    **3. SOLUÇÕES EXISTENTES NO MERCADO**
    - Pesquisa abrangente de alternativas disponíveis
    - Análise comparativa técnica e econômica
    - Consideração de execução direta pelo órgão
    - Vantagens e desvantagens de cada alternativa

    **4. LEVANTAMENTO E ANÁLISE DE RISCOS**
    - Elaboração de Mapa de Riscos obrigatório
    - Identificação de riscos de planejamento, seleção e execução
    - Análise de probabilidade e impacto
    - Medidas de mitigação propostas

    **5. CRITÉRIOS DE SUSTENTABILIDADE**
    - Conformidade com Guia de Contratações Sustentáveis
    - Identificação de impactos ambientais
    - Medidas mitigadoras específicas
    - Requisitos de eficiência energética e logística reversa

    **6. ESTIMATIVA DO VALOR DA CONTRATAÇÃO**
    - Metodologia de pesquisa conforme art. 23 da Lei 14.133/2021
    - Fontes consultadas (Painel de Preços, SICAF, mercado)
    - Custos totais considerados (aquisição + acessórios + ciclo de vida)
    - Memórias de cálculo detalhadas

    **7. DEFINIÇÃO DO OBJETO**
    - Descrição técnica precisa e completa
    - Especificações técnicas detalhadas
    - Alinhamento com necessidade identificada
    - Possibilidade de desdobramento em múltiplos Termos de Referência

    **8. JUSTIFICATIVA DE ESCOLHA DA SOLUÇÃO**
    - Fundamentação técnica, operacional e financeira
    - Demonstração de vantajosidade para a Administração
    - Comparação com alternativas analisadas
    - Alinhamento com interesse público

    **9. PREVISÃO DE CONTRATAÇÕES FUTURAS (PCA)**
    - Inserção no Plano de Contratações Anuais
    - Cronograma de contratações relacionadas
    - Interdependências com outras aquisições
    - Planejamento plurianual quando aplicável

    **10. ESTIMATIVA DE QUANTIDADES**
    - Memórias de cálculo fundamentadas
    - Análise de histórico de consumo
    - Consideração de economia de escala
    - Previsões de demanda futura

    **11. JUSTIFICATIVAS PARA PARCELAMENTO, AGRUPAMENTO E SUBCONTRATAÇÃO**
    - Análise de viabilidade técnica e econômica
    - Conformidade com Súmula 247 do TCU
    - Justificativa para divisibilidade ou indivisibilidade do objeto
    - Considerações sobre economia de escala

    **12. DEPENDÊNCIA DO CONTRATADO**
    - Análise de dependência tecnológica
    - Medidas para evitar aprisionamento tecnológico
    - Estratégias de migração e portabilidade
    - Garantias de continuidade dos serviços

    **13. TRANSIÇÃO CONTRATUAL**
    - Planejamento da transição entre contratos
    - Período de sobreposição necessário
    - Transferência de conhecimento e documentação
    - Continuidade dos serviços essenciais

    **14. ESTRATÉGIA DE IMPLANTAÇÃO**
    - Metodologia de implementação detalhada
    - Cronograma executivo com marcos principais
    - Recursos humanos e materiais necessários
    - Plano de gestão de mudanças

    **15. BENEFÍCIOS ESPERADOS**
    - Benefícios quantitativos e qualitativos
    - Indicadores de desempenho propostos
    - Beneficiários diretos e indiretos
    - Retorno sobre investimento esperado

    **16. DECLARAÇÃO DE ADEQUAÇÃO ORÇAMENTÁRIA**
    - Confirmação de disponibilidade orçamentária
    - Fonte de recursos identificada
    - Compatibilidade com planejamento orçamentário
    - Impacto nas metas fiscais

    **17. APROVAÇÃO DA AUTORIDADE COMPETENTE**
    - Identificação da autoridade competente
    - Fundamentação da competência decisória
    - Espaço para assinatura e data
    - Referência aos autos do processo administrativo

    ## DIRETRIZES DE ELABORAÇÃO:

    1. **LINGUAGEM TÉCNICA FORMAL**: Utilize terminologia jurídico-administrativa adequada
    2. **FUNDAMENTAÇÃO LEGAL**: Cite base legal pertinente (Lei 14.133/2021, decretos, instruções normativas)
    3. **ESTRUTURAÇÃO PROFISSIONAL**: Numeração sequencial, parágrafos bem estruturados
    4. **COMPLETUDE TÉCNICA**: Todas as 17 seções devem ser desenvolvidas adequadamente
    5. **CONFORMIDADE NORMATIVA**: Aderência total ao Manual TRT-2 e legislação vigente
    6. **OBJETIVIDADE**: Linguagem clara, precisa e objetiva
    7. **FUNDAMENTAÇÃO**: Todas as afirmações devem ser tecnicamente fundamentadas

    ## OBSERVAÇÕES IMPORTANTES:

    - O documento deve ter entre 8-15 páginas quando impresso
    - Cada seção deve ter desenvolvimento adequado (não apenas tópicos)
    - Incluir referências normativas pertinentes
    - Manter coerência técnica entre todas as seções
    - Adequar linguagem ao padrão de documentos oficiais do Poder Judiciário

    Elabore o ETP completo seguindo rigorosamente esta estrutura e diretrizes.
    """
    
    return prompt_tecnico
```

---

## 🔄 **COMPARAÇÃO: PROMPT ATUAL vs. NOVO PROMPT**

| Aspecto | **Prompt Atual** | **Novo Prompt Técnico** |
|---------|------------------|-------------------------|
| **Estrutura** | ❌ 6 seções informais | ✅ 17 seções obrigatórias |
| **Linguagem** | ❌ Coloquial com bullets | ✅ Técnica formal |
| **Base Legal** | ❌ Não menciona | ✅ Lei 14.133/2021 + Manual TRT-2 |
| **Completude** | ❌ Básico | ✅ Completo e detalhado |
| **Conformidade** | ❌ Não conforme | ✅ Totalmente conforme |
| **Tamanho** | ❌ ~2-3 páginas | ✅ 8-15 páginas |
| **Qualidade** | ❌ Amadora | ✅ Profissional |

---

## 📊 **MELHORIAS IMPLEMENTADAS**

### **✅ Estrutura Técnica Completa:**
- **17 seções obrigatórias** conforme Manual TRT-2
- **Numeração sequencial** profissional
- **Desenvolvimento adequado** de cada seção
- **Coerência técnica** entre seções

### **✅ Linguagem Jurídico-Administrativa:**
- **Terminologia técnica** adequada
- **Padrão formal** de documentos oficiais
- **Objetividade** e precisão
- **Conformidade** com padrões do Poder Judiciário

### **✅ Fundamentação Legal Robusta:**
- **Lei 14.133/2021** como base principal
- **Manual TRT-2** como referência técnica
- **Decreto 9.507/2018** para análise de terceirização
- **Súmula 247 TCU** para parcelamento

### **✅ Completude Técnica:**
- **Mapa de Riscos** obrigatório
- **Critérios de Sustentabilidade** detalhados
- **Análise de Dependência** tecnológica
- **Transição Contratual** planejada

---

## 🎯 **IMPACTO ESPERADO**

### **Para a Qualidade dos ETPs:**
- ✅ **Conformidade Total**: Aderência ao Manual TRT-2
- ✅ **Robustez Técnica**: Documentos profissionais
- ✅ **Redução de Questionamentos**: Menos problemas com órgãos de controle
- ✅ **Padronização**: Consistência entre documentos

### **Para os Usuários:**
- ✅ **Orientação Clara**: Estrutura bem definida
- ✅ **Aprendizado**: Conhecimento das normas técnicas
- ✅ **Eficiência**: Processo mais organizado
- ✅ **Confiança**: Documentos tecnicamente superiores

---

## 🔧 **IMPLEMENTAÇÃO**

### **Localização no Código:**
- **Arquivo**: [`integrador.py`](integrador.py:813-865)
- **Método**: `_construct_prompt()` → `_construct_prompt_tecnico_trt2()`
- **Classe**: `EtpLlmGenerator`

### **Próximos Passos:**
1. **Substituir prompt atual** pelo novo prompt técnico
2. **Testar geração** com dados reais
3. **Validar conformidade** com Manual TRT-2
4. **Ajustar** baseado em feedback
5. **Integrar** com assistente inteligente

---

## ✅ **STATUS**

**NOVO PROMPT TÉCNICO: ESPECIFICADO E PRONTO PARA IMPLEMENTAÇÃO** 🎉

O novo prompt técnico está completamente especificado e alinhado com as normas do Manual TRT-2 e Lei 14.133/2021. A implementação resultará em ETPs tecnicamente superiores e totalmente conformes.