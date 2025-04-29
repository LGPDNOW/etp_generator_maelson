# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
import base64
from io import BytesIO
import random
import os
# from etp_llm_generator import EtpLlmGenerator, format_etp_as_html, save_etp_as_pdf
from integrador import EtpLlmGenerator, format_etp_as_html, save_etp_as_pdf

# Configuração da página
st.set_page_config(
    page_title="Gerador de ETP",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1E3A8A;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        margin-bottom: 1rem;
    }
    .highlight {
        background-color: #E8F0FE;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
    }
    .success-banner {
        background-color: #D1FAE5;
        color: #065F46;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
        text-align: center;
        font-weight: bold;
    }
    .btn-primary {
        background-color: #1E3A8A;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        text-decoration: none;
        margin-right: 0.5rem;
    }
    .btn-secondary {
        background-color: #6B7280;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        text-decoration: none;
        margin-right: 0.5rem;
    }
    .btn-success {
        background-color: #10B981;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        text-decoration: none;
    }
    .pdf-view {
        border: 1px solid #dee2e6;
        border-radius: 0.5rem;
        padding: 1.5rem;
        background-color: white;
        height: 600px;
        overflow-y: auto;
    }
    .step-nav {
        display: flex;
        justify-content: space-between;
        margin-top: 2rem;
    }
    footer {
        margin-top: 3rem;
        text-align: center;
        color: #6B7280;
    }
    .loading {
        text-align: center;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Funções auxiliares


def create_download_link(val, filename):
    b64 = base64.b64encode(val.encode()).decode() if isinstance(
        val, str) else base64.b64encode(val).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}" class="btn-success">Baixar PDF</a>'


def formato_moeda(valor):
    if valor:
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return "R$ 0,00"


# Estado da sessão
if 'step' not in st.session_state:
    st.session_state.step = 1

if 'dados_etp' not in st.session_state:
    st.session_state.dados_etp = {
        'descricao_problema': '',
        'areas_impactadas': [],
        'stakeholders': [],
        'requisitos_funcionais': '',
        'requisitos_nao_funcionais': '',
        'solucoes_mercado': '',
        'comparativo_solucoes': '',
        'valor_minimo': None,
        'valor_medio': None,
        'valor_maximo': None,
        'solucao_proposta': '',
        'justificativa_escolha': '',
        'estrategia_implantacao': '',
        'cronograma': '',
        'recursos_necessarios': '',
        'beneficios': '',
        'beneficiarios': '',
        'providencias': '',
        'declaracao_viabilidade': 'viável'
    }

if 'documento_gerado' not in st.session_state:
    st.session_state.documento_gerado = None

if 'pdf_bytes' not in st.session_state:
    st.session_state.pdf_bytes = None

# Funções de navegação


def avancar_etapa():
    st.session_state.step += 1


def voltar_etapa():
    st.session_state.step -= 1


def ir_para_etapa(etapa):
    st.session_state.step = etapa


def salvar_dados(dados_novos):
    st.session_state.dados_etp.update(dados_novos)


# Layout do cabeçalho
st.markdown('<div style="display: flex; justify-content: space-between; align-items: center;">'
            '<h1 style="color: #1E3A8A;">📝 Gerador de ETP</h1>'
            '<div>'
            '<a href="#" style="margin-right: 20px; text-decoration: none; color: #1E3A8A;">Início</a>'
            '<a href="#" style="margin-right: 20px; text-decoration: none; color: #1E3A8A;">Ajuda</a>'
            '<a href="#" style="text-decoration: none; color: #1E3A8A;">Sobre</a>'
            '</div>'
            '</div>', unsafe_allow_html=True)

# Configurações do LLM
with st.sidebar:
    st.header("Configurações da IA")
    llm_provider = st.selectbox(
        "Provedor de IA:",
        options=["OpenAI", "Anthropic/Claude"],
        index=0
    )

    if llm_provider == "OpenAI":
        openai_api_key = st.text_input(
            "OpenAI API Key:", type="password", value=os.environ.get("OPENAI_API_KEY", ""))
        if openai_api_key:
            os.environ["OPENAI_API_KEY"] = openai_api_key
    else:
        anthropic_api_key = st.text_input(
            "Anthropic API Key:", type="password", value=os.environ.get("ANTHROPIC_API_KEY", ""))
        if anthropic_api_key:
            os.environ["ANTHROPIC_API_KEY"] = anthropic_api_key

# Página inicial
if st.session_state.step == 1:
    st.markdown('<div class="highlight">'
                '<h2>Simplifique a elaboração de Estudos Técnicos Preliminares</h2>'
                '<p>Esta ferramenta auxilia na criação automatizada de ETPs, economizando tempo e garantindo '
                'a conformidade com as normativas vigentes.</p>'
                '</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="card">'
                    '<h3>✨ Intuitivo</h3>'
                    '<p>Interface amigável que guia você por todas as etapas necessárias.</p>'
                    '</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">'
                    '<h3>⚡ Rápido</h3>'
                    '<p>Gere documentos completos em minutos, não dias.</p>'
                    '</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card">'
                    '<h3>🤖 IA Integrada</h3>'
                    '<p>Utiliza tecnologia de IA avançada para criar documentos com aparência profissional.</p>'
                    '</div>', unsafe_allow_html=True)

    # st.markdown('<div style="text-align: center; margin-top: 2rem;">'
    #            '<button onclick="parent.streamlit.setComponentValue(\'iniciar\')" '
    #            'style="background-color: #1E3A8A; color: white; padding: 10px 20px; '
    #            'border: none; border-radius: 5px; font-size: 16px; cursor: pointer;">'
    #            # 'Iniciar novo ETP</button>'
    #            '</div>', unsafe_allow_html=True)

    if st.button("Iniciar novo ETP"):
        avancar_etapa()

# Etapa 2: Identificação do Problema
elif st.session_state.step == 2:
    st.markdown('<h2 class="sub-header">Etapa 1: Identificação do Problema</h2>',
                unsafe_allow_html=True)

    descricao = st.text_area("Descrição do problema ou necessidade:",
                             value=st.session_state.dados_etp['descricao_problema'],
                             height=150,
                             help="Descreva o problema ou necessidade que motiva esta contratação")

    areas_opcoes = ["TI", "RH", "Financeiro", "Administrativo",
                    "Jurídico", "Operacional", "Comercial", "Marketing", "Outro"]
    areas = st.multiselect("Áreas impactadas:",
                           options=areas_opcoes,
                           default=st.session_state.dados_etp['areas_impactadas'],
                           help="Selecione as áreas da organização afetadas por este problema")

    stakeholders = st.multiselect("Stakeholders envolvidos:",
                                  options=["Diretoria", "Gerência", "Servidores",
                                           "Cidadãos", "Fornecedores", "Outros órgãos"],
                                  default=st.session_state.dados_etp['stakeholders'],
                                  help="Selecione as partes interessadas nesta contratação")

    requisitos_func = st.text_area("Requisitos funcionais desejados:",
                                   value=st.session_state.dados_etp['requisitos_funcionais'],
                                   height=100,
                                   help="Liste os principais requisitos funcionais que a solução deve atender")

    requisitos_nao_func = st.text_area("Requisitos não funcionais:",
                                       value=st.session_state.dados_etp['requisitos_nao_funcionais'],
                                       height=100,
                                       help="Liste requisitos não funcionais como desempenho, segurança, conformidade etc.")

    st.markdown('<div class="step-nav">'
                # '<button class="btn-secondary" onclick="window.history.back()">Voltar</button>'
                # '<button class="btn-primary" id="avancar">Avançar</button>'
                '</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Voltar", key="btn_voltar_3"):
            voltar_etapa()
    with col2:
        if st.button("Avançar", key="btn_avancar_2"):
            dados = {
                'descricao_problema': descricao,
                'areas_impactadas': areas,
                'stakeholders': stakeholders,
                'requisitos_funcionais': requisitos_func,
                'requisitos_nao_funcionais': requisitos_nao_func
            }
            salvar_dados(dados)
            avancar_etapa()

# Etapa 3: Análise de Mercado
elif st.session_state.step == 3:
    st.markdown('<h2 class="sub-header">Etapa 2: Análise de Mercado</h2>',
                unsafe_allow_html=True)

    solucoes = st.text_area("Soluções disponíveis no mercado:",
                            value=st.session_state.dados_etp['solucoes_mercado'],
                            height=150,
                            help="Descreva as principais soluções disponíveis no mercado para atender esta necessidade")

    comparativo = st.text_area("Comparativo entre as soluções:",
                               value=st.session_state.dados_etp['comparativo_solucoes'],
                               height=150,
                               help="Compare as soluções em termos de funcionalidades, preço, suporte etc.")

    col1, col2, col3 = st.columns(3)

    with col1:
        valor_min = st.number_input("Valor mínimo estimado (R$):",
                                    value=st.session_state.dados_etp[
                                        'valor_minimo'] if st.session_state.dados_etp['valor_minimo'] else 0.0,
                                    min_value=0.0,
                                    step=1000.0,
                                    format="%.2f")

    with col2:
        valor_med = st.number_input("Valor médio estimado (R$):",
                                    value=st.session_state.dados_etp[
                                        'valor_medio'] if st.session_state.dados_etp['valor_medio'] else 0.0,
                                    min_value=0.0,
                                    step=1000.0,
                                    format="%.2f")

    with col3:
        valor_max = st.number_input("Valor máximo estimado (R$):",
                                    value=st.session_state.dados_etp[
                                        'valor_maximo'] if st.session_state.dados_etp['valor_maximo'] else 0.0,
                                    min_value=0.0,
                                    step=1000.0,
                                    format="%.2f")

    solucao_prop = st.text_area("Solução proposta:",
                                value=st.session_state.dados_etp['solucao_proposta'],
                                height=100,
                                help="Descreva a solução que você propõe para atender a necessidade identificada")

    justificativa = st.text_area("Justificativa da escolha:",
                                 value=st.session_state.dados_etp['justificativa_escolha'],
                                 height=100,
                                 help="Justifique por que a solução proposta é a mais adequada")

    st.markdown('<div class="step-nav">'
                # '<button class="btn-secondary" id="voltar">Voltar</button>'
                # '<button class="btn-primary" id="avancar">Avançar</button>'
                '</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Voltar", key="btn_voltar_3"):
            voltar_etapa()
    with col2:
        if st.button("Avançar", key="btn_avancar_3"):
            dados = {
                'solucoes_mercado': solucoes,
                'comparativo_solucoes': comparativo,
                'valor_minimo': valor_min,
                'valor_medio': valor_med,
                'valor_maximo': valor_max,
                'solucao_proposta': solucao_prop,
                'justificativa_escolha': justificativa
            }
            salvar_dados(dados)
            avancar_etapa()

# Etapa 4: Implantação
elif st.session_state.step == 4:
    st.markdown('<h2 class="sub-header">Etapa 3: Implantação</h2>',
                unsafe_allow_html=True)

    estrategia = st.text_area("Estratégia de implantação:",
                              value=st.session_state.dados_etp['estrategia_implantacao'],
                              height=150,
                              help="Descreva como será feita a implantação da solução")

    cronograma = st.text_area("Cronograma estimado:",
                              value=st.session_state.dados_etp['cronograma'],
                              height=100,
                              help="Apresente um cronograma estimado para a implantação")

    # Continuação do arquivo app.py (Etapa 4: Implantação - continuação)

    recursos = st.text_area("Recursos necessários:",
                            value=st.session_state.dados_etp['recursos_necessarios'],
                            height=100,
                            help="Liste os recursos humanos, materiais e tecnológicos necessários")

    providencias = st.text_area("Providências necessárias:",
                                value=st.session_state.dados_etp['providencias'],
                                height=100,
                                help="Descreva as providências a serem tomadas antes e durante a implantação")

    st.markdown('<div class="step-nav">'
                # '<button class="btn-secondary" id="voltar">Voltar</button>'
                # '<button class="btn-primary" id="avancar">Avançar</button>'
                '</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Voltar", key="btn_voltar_4"):
            voltar_etapa()
    with col2:
        if st.button("Avançar", key="btn_avancar_4"):
            dados = {
                'estrategia_implantacao': estrategia,
                'cronograma': cronograma,
                'recursos_necessarios': recursos,
                'providencias': providencias
            }
            salvar_dados(dados)
            avancar_etapa()

# Etapa 5: Benefícios e Valor
elif st.session_state.step == 5:
    st.markdown('<h2 class="sub-header">Etapa 4: Benefícios e Valor</h2>',
                unsafe_allow_html=True)

    beneficios = st.text_area("Benefícios esperados:",
                              value=st.session_state.dados_etp['beneficios'],
                              height=150,
                              help="Descreva os benefícios esperados com a implantação da solução")

    beneficiarios = st.text_area("Beneficiários:",
                                 value=st.session_state.dados_etp['beneficiarios'],
                                 height=100,
                                 help="Liste quem serão os beneficiários diretos e indiretos da solução")

    viabilidade = st.radio("Declaração de viabilidade:",
                           options=["viável", "inviável"],
                           index=0 if st.session_state.dados_etp['declaracao_viabilidade'] == "viável" else 1,
                           help="Declare se a contratação é viável ou inviável com base no estudo realizado")

    st.markdown('<div class="step-nav">'
                # '<button class="btn-secondary" id="voltar">Voltar</button>'
                # '<button class="btn-primary" id="avancar">Avançar</button>'
                '</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Voltar", key="btn_voltar_5"):
            voltar_etapa()
    with col2:
        if st.button("Finalizar e Gerar ETP", key="btn_finalizar"):
            dados = {
                'beneficios': beneficios,
                'beneficiarios': beneficiarios,
                'declaracao_viabilidade': viabilidade
            }
            salvar_dados(dados)

            # Exibir spinner enquanto gera o documento com o LLM
            with st.spinner('Gerando documento ETP com IA. Esta operação pode levar alguns segundos...'):
                try:
                    # Inicializar o gerador de ETP com o provedor escolhido
                    provider = "openai" if llm_provider == "OpenAI" else "anthropic"
                    etp_generator = EtpLlmGenerator(provider=provider)

                    # Gerar o ETP com o modelo LLM
                    st.session_state.documento_gerado = etp_generator.generate_etp(
                        st.session_state.dados_etp)

                    # Formatar como HTML para melhor visualização e gerar PDF
                    etp_html = format_etp_as_html(
                        st.session_state.documento_gerado)
                    st.session_state.pdf_bytes = save_etp_as_pdf(etp_html)

                except Exception as e:
                    st.error(f"Erro ao gerar o documento: {str(e)}")
                    st.session_state.documento_gerado = "Ocorreu um erro ao gerar o documento. Verifique as configurações da API e tente novamente."

            avancar_etapa()

# Etapa 6: Visualização do documento gerado
elif st.session_state.step == 6:
    st.markdown('<div class="success-banner">'
                '<h2>✅ Documento ETP gerado com sucesso!</h2>'
                '</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([4, 6])

    with col1:
        st.markdown('<h3>Resumo das Informações</h3>', unsafe_allow_html=True)

        st.markdown('<div class="card">'
                    f'<h4>Problema</h4>'
                    f'<p>{st.session_state.dados_etp["descricao_problema"][:150]}...</p>'
                    f'<p><strong>Áreas afetadas:</strong> {", ".join(st.session_state.dados_etp["areas_impactadas"])}</p>'
                    f'<p><strong>Stakeholders:</strong> {", ".join(st.session_state.dados_etp["stakeholders"])}</p>'
                    '</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">'
                    f'<h4>Análise de Mercado</h4>'
                    f'<p><strong>Valor estimado:</strong> {formato_moeda(st.session_state.dados_etp["valor_medio"])}</p>'
                    f'<p><strong>Solução escolhida:</strong> {st.session_state.dados_etp["solucao_proposta"][:150]}...</p>'
                    '</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">'
                    f'<h4>Implantação</h4>'
                    f'<p>{st.session_state.dados_etp["estrategia_implantacao"][:150]}...</p>'
                    '</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">'
                    f'<h4>Benefícios</h4>'
                    f'<p>{st.session_state.dados_etp["beneficios"][:150]}...</p>'
                    f'<p><strong>Beneficiários:</strong> {st.session_state.dados_etp["beneficiarios"]}</p>'
                    f'<p><strong>Declaração:</strong> A contratação foi declarada {st.session_state.dados_etp["declaracao_viabilidade"]}</p>'
                    '</div>', unsafe_allow_html=True)

        # Botões de ação
        col_edit, col_download = st.columns(2)

        with col_edit:
            if st.button("Editar informações"):
                ir_para_etapa(2)

        with col_download:
            if st.session_state.pdf_bytes:
                # Botão para download do PDF
                pdf_download_link = create_download_link(
                    st.session_state.pdf_bytes, "ETP_gerado.pdf")
                st.markdown(pdf_download_link, unsafe_allow_html=True)
            else:
                if st.button("Gerar PDF"):
                    with st.spinner('Gerando PDF...'):
                        try:
                            etp_html = format_etp_as_html(
                                st.session_state.documento_gerado)
                            st.session_state.pdf_bytes = save_etp_as_pdf(
                                etp_html)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro ao gerar PDF: {str(e)}")

    with col2:
        st.markdown('<h3>Documento ETP Gerado pela IA</h3>',
                    unsafe_allow_html=True)

        if st.session_state.documento_gerado:
            # Criar um container estilizado para o documento
            st.markdown("""
            <style>
            .pdf-container {
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
                background-color: white;
                height: 600px;
                overflow-y: auto;
                margin-bottom: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            </style>
            """, unsafe_allow_html=True)

            # Exibir o documento dentro do container estilizado
            st.markdown(f'<div class="pdf-container">{st.session_state.documento_gerado}</div>',
                        unsafe_allow_html=True)

            # Adicionar botões para download ou outras ações abaixo do visualizador
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("Editar Documento"):
                    st.session_state.editing_mode = True
            with col_btn2:
                if st.button("Baixar PDF"):
                    with st.spinner('Gerando PDF...'):
                        try:
                            etp_html = format_etp_as_html(
                                st.session_state.documento_gerado)
                            st.session_state.pdf_bytes = save_etp_as_pdf(
                                etp_html)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro ao gerar PDF: {str(e)}")
        else:
            st.warning(
                "Nenhum documento gerado. Retorne às etapas anteriores e tente novamente.")

    # st.markdown('<div style="margin-top: 2rem; text-align: center;">'
      #          '<button class="btn-secondary" id="nova_geracao">Gerar novo ETP</button>'
       #         '</div>', unsafe_allow_html=True)

    if st.button("Gerar novo ETP"):
        st.session_state.step = 1
        st.session_state.dados_etp = {
            'descricao_problema': '',
            'areas_impactadas': [],
            'stakeholders': [],
            'requisitos_funcionais': '',
            'requisitos_nao_funcionais': '',
            'solucoes_mercado': '',
            'comparativo_solucoes': '',
            'valor_minimo': None,
            'valor_medio': None,
            'valor_maximo': None,
            'solucao_proposta': '',
            'justificativa_escolha': '',
            'estrategia_implantacao': '',
            'cronograma': '',
            'recursos_necessarios': '',
            'beneficios': '',
            'beneficiarios': '',
            'providencias': '',
            'declaracao_viabilidade': 'viável'
        }
        st.session_state.documento_gerado = None
        st.session_state.pdf_bytes = None

# Rodapé
st.markdown('<footer>'
            '<p>©Bravonix 2025 Gerador de ETP | Desenvolvido com Streamlit e IA</p>'
            '</footer>', unsafe_allow_html=True)
