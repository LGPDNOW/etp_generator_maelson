# Plano de Evolução: Sistema Gerador de Documentos Oficiais

## Visão Geral

Este plano detalha a evolução do sistema atual de geração de ETPs para um sistema completo de geração de documentos oficiais, com foco em qualidade técnica, flexibilidade e conformidade com padrões governamentais.

## Análise da Situação Atual

### Problemas Identificados
1. **Prompt do ETP inadequado**: Linguagem com bullets, não técnica
2. **Interface rígida**: Formulário engessado sem flexibilidade
3. **Falta de edição**: Usuário não pode alterar o documento gerado
4. **Limitação de tipos**: Apenas ETPs, sem outros documentos oficiais
5. **Ausência de templates**: Sem padronização organizacional

### Pontos Fortes Atuais
- Interface Streamlit funcional
- Integração com LLMs estabelecida
- Sistema de RAG implementado
- Geração de PDF funcionando

## Roadmap de Desenvolvimento

### FASE 1: Melhoria do Prompt e Qualidade do ETP
**Prioridade**: Alta | **Tempo Estimado**: 2-3 dias

#### 1.1 Análise de Requisitos Técnicos
- Estudar manuais de construção de ETP/ETR
- Analisar exemplos reais de ETPs aprovados
- Identificar estrutura técnica padrão
- Mapear linguagem formal necessária

#### 1.2 Reestruturação do Prompt
```
Objetivos:
- Linguagem técnica formal (sem bullets)
- Estrutura conforme normas governamentais
- Seções padronizadas e numeradas
- Fundamentação legal adequada
- Análise de viabilidade técnica e econômica
```

#### 1.3 Especificações Técnicas
- **Arquivo**: `integrador.py` - método `_construct_prompt()`
- **Estrutura do ETP**:
  1. Identificação e Contextualização
  2. Análise da Necessidade
  3. Requisitos da Contratação
  4. Estudo de Viabilidade
  5. Análise de Mercado
  6. Estratégia de Contratação
  7. Cronograma de Execução
  8. Recursos Orçamentários
  9. Gestão de Riscos
  10. Conclusão e Recomendações

### FASE 2: Editor de Documentos Integrado
**Prioridade**: Alta | **Tempo Estimado**: 3-4 dias

#### 2.1 Funcionalidades do Editor
- Editor de texto rico integrado na interface
- Capacidade de edição em tempo real
- Preview lado a lado (edição | visualização)
- Salvamento automático de alterações
- Histórico de versões

#### 2.2 Arquitetura Técnica
```python
# Componentes necessários:
- st_ace ou st_quill para editor rico
- Sistema de versionamento de documentos
- Sincronização entre editor e preview
- Validação de estrutura do documento
```

#### 2.3 Interface Proposta
```
Layout em 3 colunas:
[Formulário] | [Editor] | [Preview PDF]
    30%      |   40%    |     30%
```

### FASE 3: Expansão para Múltiplos Tipos de Documentos
**Prioridade**: Média | **Tempo Estimado**: 4-5 dias

#### 3.1 Tipos de Documentos a Implementar
1. **Ofícios**
   - Estrutura formal padronizada
   - Numeração sequencial
   - Campos específicos (destinatário, assunto, referência)

2. **Memorandos**
   - Comunicação interna
   - Formato mais direto
   - Campos de urgência e classificação

3. **Atas de Reunião**
   - Lista de participantes
   - Pauta e deliberações
   - Espaço para assinaturas

4. **Pareceres Técnicos**
   - Análise fundamentada
   - Conclusões e recomendações
   - Referências técnicas

#### 3.2 Arquitetura Modular
```python
class DocumentGenerator:
    def __init__(self, document_type):
        self.document_type = document_type
        self.template = self._load_template()
        self.prompt_builder = self._get_prompt_builder()
    
    def _load_template(self):
        # Carrega template específico do tipo
        pass
    
    def _get_prompt_builder(self):
        # Retorna builder de prompt específico
        pass
```

#### 3.3 Interface Adaptativa
- Seleção de tipo de documento na tela inicial
- Formulários dinâmicos baseados no tipo
- Campos específicos por categoria
- Validações personalizadas

### FASE 4: Sistema de Templates Organizacionais
**Prioridade**: Média | **Tempo Estimado**: 5-6 dias

#### 4.1 Funcionalidades do Sistema de Templates
- **Cadastro de Templates**: Interface para criar/editar templates
- **Campos Dinâmicos**: Brasão, dados organizacionais, assinaturas
- **Hierarquia de Templates**: Templates base + personalizações
- **Versionamento**: Controle de versões dos templates

#### 4.2 Estrutura de Dados
```python
template_structure = {
    "id": "template_001",
    "name": "ETP Padrão Prefeitura",
    "document_type": "etp",
    "organization": {
        "name": "Prefeitura Municipal de...",
        "logo_path": "/assets/brasao.png",
        "address": "...",
        "cnpj": "..."
    },
    "sections": [
        {
            "title": "1. IDENTIFICAÇÃO",
            "fields": ["orgao", "setor", "responsavel"],
            "template_text": "..."
        }
    ],
    "signatures": [
        {
            "role": "Responsável Técnico",
            "name_field": "responsavel_tecnico",
            "title_field": "cargo_responsavel"
        }
    ]
}
```

#### 4.3 Interface de Gerenciamento
- **Tela de Templates**: Lista, criar, editar, excluir
- **Editor Visual**: Drag-and-drop para campos
- **Preview em Tempo Real**: Visualização durante edição
- **Importação/Exportação**: Backup e compartilhamento

## Arquitetura Técnica Detalhada

### Estrutura de Arquivos Proposta
```
/
├── app.py (interface principal)
├── integrador.py (lógica de negócio)
├── processador_documentos.py (RAG)
├── generators/
│   ├── __init__.py
│   ├── base_generator.py
│   ├── etp_generator.py
│   ├── oficio_generator.py
│   ├── memorando_generator.py
│   └── ata_generator.py
├── templates/
│   ├── __init__.py
│   ├── template_manager.py
│   ├── template_editor.py
│   └── default_templates/
├── editors/
│   ├── __init__.py
│   ├── rich_text_editor.py
│   └── document_preview.py
└── utils/
    ├── __init__.py
    ├── document_validator.py
    └── pdf_generator.py
```

### Banco de Dados (Opcional)
Para persistência de templates e documentos:
```sql
-- Templates
CREATE TABLE templates (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255),
    document_type VARCHAR(50),
    organization_data JSON,
    template_structure JSON,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Documentos Salvos
CREATE TABLE documents (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255),
    document_type VARCHAR(50),
    template_id INTEGER,
    content TEXT,
    metadata JSON,
    created_at TIMESTAMP,
    FOREIGN KEY (template_id) REFERENCES templates(id)
);
```

## Especificações de Interface

### Tela Principal Redesenhada
```
┌─────────────────────────────────────────────────────────┐
│ 📝 Gerador de Documentos Oficiais                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐        │
│ │     ETP     │ │   Ofício    │ │  Memorando  │        │
│ │   📋 Criar  │ │   📄 Criar  │ │   📝 Criar  │        │
│ └─────────────┘ └─────────────┘ └─────────────┘        │
│                                                         │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐        │
│ │     Ata     │ │   Parecer   │ │  Templates  │        │
│ │   📊 Criar  │ │   ⚖️ Criar   │ │   ⚙️ Gerenciar │      │
│ └─────────────┘ └─────────────┘ └─────────────┘        │
│                                                         │
│ 📂 Documentos Recentes                                  │
│ • ETP - Sistema de Impressão (ontem)                    │
│ • Ofício 001/2024 - Solicitação (2 dias atrás)         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Tela de Edição Integrada
```
┌─────────────────────────────────────────────────────────┐
│ 📋 Editando: ETP - Sistema de Impressão                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ ┌─────────────┐ ┌─────────────────┐ ┌─────────────────┐ │
│ │ Formulário  │ │     Editor      │ │    Preview      │ │
│ │             │ │                 │ │                 │ │
│ │ Problema:   │ │ 1. IDENTIFICAÇÃO│ │ [PDF Preview]   │ │
│ │ [________]  │ │                 │ │                 │ │
│ │             │ │ Este Estudo     │ │                 │ │
│ │ Valor:      │ │ Técnico Prelim- │ │                 │ │
│ │ [________]  │ │ inar tem por    │ │                 │ │
│ │             │ │ objetivo...     │ │                 │ │
│ │ [Gerar IA]  │ │                 │ │                 │ │
│ │             │ │ [Editor Rico]   │ │                 │ │
│ └─────────────┘ └─────────────────┘ └─────────────────┘ │
│                                                         │
│ [Salvar] [Baixar PDF] [Compartilhar] [Nova Versão]     │
└─────────────────────────────────────────────────────────┘
```

## Cronograma de Implementação

### Sprint 1 (Semana 1): Melhoria do Prompt ETP
- [ ] Análise de manuais e exemplos reais
- [ ] Reestruturação completa do prompt
- [ ] Testes de qualidade do output
- [ ] Ajustes baseados em feedback

### Sprint 2 (Semana 2): Editor Integrado
- [ ] Implementação do editor de texto rico
- [ ] Interface de edição lado a lado
- [ ] Sistema de preview em tempo real
- [ ] Salvamento e versionamento

### Sprint 3 (Semana 3): Múltiplos Documentos
- [ ] Arquitetura modular para tipos de documento
- [ ] Implementação de Ofícios
- [ ] Interface adaptativa por tipo
- [ ] Testes de integração

### Sprint 4 (Semana 4): Sistema de Templates
- [ ] Estrutura de dados para templates
- [ ] Interface de gerenciamento
- [ ] Editor visual de templates
- [ ] Integração com geração de documentos

### Sprint 5 (Semana 5): Polimento e Testes
- [ ] Testes de usuário
- [ ] Correções e ajustes
- [ ] Documentação
- [ ] Deploy e treinamento

## Métricas de Sucesso

### Qualidade dos Documentos
- Conformidade com padrões técnicos: >95%
- Aprovação em revisões jurídicas: >90%
- Redução de tempo de elaboração: >60%

### Usabilidade
- Tempo de aprendizado: <30 minutos
- Taxa de adoção: >80%
- Satisfação do usuário: >4.5/5

### Técnicas
- Tempo de geração: <30 segundos
- Disponibilidade: >99%
- Suporte a múltiplos usuários simultâneos

## Riscos e Mitigações

### Riscos Técnicos
- **Complexidade do editor**: Usar bibliotecas testadas (Quill, TinyMCE)
- **Performance com múltiplos tipos**: Arquitetura modular e lazy loading
- **Integração com LLMs**: Fallbacks e tratamento de erros

### Riscos de Negócio
- **Resistência à mudança**: Treinamento e migração gradual
- **Qualidade dos prompts**: Testes extensivos e iteração
- **Conformidade legal**: Revisão jurídica contínua

## Recursos Necessários

### Desenvolvimento
- 1 Desenvolvedor Python/Streamlit (tempo integral)
- 1 Especialista em UX/UI (meio período)
- 1 Consultor jurídico (consultoria)

### Infraestrutura
- Servidor para aplicação
- Banco de dados (opcional)
- Armazenamento para templates e documentos
- Backup e versionamento

## Conclusão

Este plano estruturado permitirá a evolução gradual do sistema atual para uma solução completa de geração de documentos oficiais, mantendo a qualidade técnica e a conformidade com padrões governamentais.

A implementação em fases permite validação contínua e ajustes baseados no feedback dos usuários, garantindo que o produto final atenda às necessidades reais da organização.