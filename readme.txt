# Gerador de Estudos Técnicos Preliminares (ETP)

Aplicação que utiliza Inteligência Artificial para gerar Estudos Técnicos Preliminares para contratações governamentais.

## Funcionalidades

- Geração de ETP usando modelos de linguagem avançados (OpenAI ou Anthropic)
- Interface amigável para inserção de dados
- Visualização e edição do documento gerado
- Exportação para PDF

## Instalação

1. Clone o repositório:
   ```
   git clone https://github.com/seu-usuario/etp-generator.git
   cd etp-generator
   ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente:
   Crie um arquivo `.env` na raiz do projeto com:
   ```
   OPENAI_API_KEY=sua_chave_api_openai
   ANTHROPIC_API_KEY=sua_chave_api_anthropic
   ```

4. Execute a aplicação:
   ```
   streamlit run app.py
   ```

## Como usar

1. Selecione o provedor de IA (OpenAI ou Anthropic)
2. Preencha os dados do ETP nos formulários
3. Clique em "Gerar ETP"
4. Visualize, edite e baixe o documento gerado

## Tecnologias utilizadas

- Python
- Streamlit
- LangChain
- OpenAI/Anthropic
- ReportLab
```

## 8. Fazer commit e push das atualizações

```bash
git add requirements.txt README.md
git commit -m "Adiciona requirements.txt e atualiza README"
git push
