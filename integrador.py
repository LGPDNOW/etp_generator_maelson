"""
Module for generating Preliminary Technical Studies (ETP) using LangChain and AI language models.

This module provides a class for generating technical documentation and studies 
using different AI language model providers such as OpenAI and Anthropic.
"""
# etp_llm_generator.py
import re
import io
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
import os
import streamlit as st
from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import tempfile


# Carrega variáveis de ambiente do arquivo .env
load_dotenv()


class EtpLlmGenerator:
    """Gerador de Estudos Técnicos Preliminares (ETP) usando LangChain."""

    def __init__(self, provider: str = "openai"):
        """
        Inicializa o gerador de ETP com um provedor LLM específico.

        Args:
            provider (str): O provedor LLM a ser usado ('openai' ou 'anthropic')
        """
        self.provider = provider.lower()

        # Configurar o modelo LLM baseado no provedor
        if self.provider == "openai":
            api_key = os.environ.get(
                "OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY", ""))
            if not api_key:
                st.warning(
                    "Chave de API da OpenAI não configurada. Defina a variável de ambiente OPENAI_API_KEY ou configure em st.secrets.")

            self.llm = ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0.7,
                api_key=api_key,
                max_tokens=4000
            )

        elif self.provider == "anthropic":
            api_key = os.environ.get(
                "ANTHROPIC_API_KEY", st.secrets.get("ANTHROPIC_API_KEY", ""))
            if not api_key:
                st.warning(
                    "Chave de API da Anthropic não configurada. Defina a variável de ambiente ANTHROPIC_API_KEY ou configure em st.secrets.")

            self.llm = ChatAnthropic(
                model="claude-3-opus-20240229",
                temperature=0.7,
                api_key=api_key,
                max_tokens=4000
            )

        else:
            raise ValueError(
                f"Provedor LLM não suportado: {provider}. Use 'openai' ou 'anthropic'.")

        # Criar o template de prompt para o ETP
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "Você é um especialista em elaboração de documentos técnicos para contratações governamentais, "
             "especialmente Estudos Técnicos Preliminares (ETP). Seu objetivo é criar documentos claros, "
             "objetivos e em conformidade com a legislação brasileira."),
            ("user", "{prompt}")
        ])

        # Configurar a cadeia de processamento
        self.chain = (
            {"prompt": RunnablePassthrough()}
            | self.prompt_template
            | self.llm
            | StrOutputParser()
        )

    def _construct_prompt(self, dados_etp: Dict[str, Any]) -> str:
        """
        Constrói o prompt para o LLM com base nos dados do ETP.

        Args:
            dados_etp: Dicionário contendo os dados do ETP

        Returns:
            str: Prompt formatado para o LLM
        """
        # Formatar valores monetários
        valor_min = f"R$ {dados_etp['valor_minimo']:,.2f}".replace(",", "X").replace(
            ".", ",").replace("X", ".") if dados_etp['valor_minimo'] else "Não informado"
        valor_med = f"R$ {dados_etp['valor_medio']:,.2f}".replace(",", "X").replace(
            ".", ",").replace("X", ".") if dados_etp['valor_medio'] else "Não informado"
        valor_max = f"R$ {dados_etp['valor_maximo']:,.2f}".replace(",", "X").replace(
            ".", ",").replace("X", ".") if dados_etp['valor_maximo'] else "Não informado"

        # Construir o prompt
        prompt = f"""
        Elabore um Estudo Técnico Preliminar (ETP) completo e detalhado com base nas seguintes informações:
        
        # IDENTIFICAÇÃO DO PROBLEMA
        Descrição do problema: {dados_etp['descricao_problema']}
        Áreas impactadas: {', '.join(dados_etp['areas_impactadas'])}
        Stakeholders: {', '.join(dados_etp['stakeholders'])}
        
        # REQUISITOS
        Requisitos funcionais: {dados_etp['requisitos_funcionais']}
        Requisitos não funcionais: {dados_etp['requisitos_nao_funcionais']}
        
        # ANÁLISE DE MERCADO
        Soluções disponíveis: {dados_etp['solucoes_mercado']}
        Comparativo entre soluções: {dados_etp['comparativo_solucoes']}
        Estimativa de preços:
        - Valor mínimo: {valor_min}
        - Valor médio: {valor_med}
        - Valor máximo: {valor_max}
        
        # SOLUÇÃO PROPOSTA
        Solução escolhida: {dados_etp['solucao_proposta']}
        Justificativa: {dados_etp['justificativa_escolha']}
        
        # IMPLANTAÇÃO
        Estratégia de implantação: {dados_etp['estrategia_implantacao']}
        Cronograma: {dados_etp['cronograma']}
        Recursos necessários: {dados_etp['recursos_necessarios']}
        Providências: {dados_etp['providencias']}
        
        # BENEFÍCIOS
        Benefícios esperados: {dados_etp['beneficios']}
        Beneficiários: {dados_etp['beneficiarios']}
        
        # VIABILIDADE
        Declaração de viabilidade: A contratação foi declarada {dados_etp['declaracao_viabilidade']}
        
        Formate o documento de forma profissional, com numeração de seções, parágrafos bem estruturados e linguagem formal adequada para documentos governamentais. Inclua uma introdução e conclusão.
        """

        return prompt

    def generate_etp(self, dados_etp: Dict[str, Any]) -> str:
        """
        Gera o ETP usando o LLM configurado.

        Args:
            dados_etp: Dicionário contendo os dados do ETP

        Returns:
            str: Texto do ETP gerado
        """
        prompt = self._construct_prompt(dados_etp)

        try:
            # Executar a cadeia de processamento
            result = self.chain.invoke({"prompt": prompt})
            return result
        except Exception as e:
            st.error(f"Erro ao gerar o ETP: {str(e)}")
            return f"Erro na geração do documento: {str(e)}"


def format_etp_as_html(etp_text: str) -> str:
    """
    Formata o texto do ETP como HTML para melhor visualização.

    Args:
        etp_text: Texto do ETP gerado

    Returns:
        str: HTML formatado
    """
    # Substituir quebras de linha por tags <br>
    html_content = etp_text.replace('\n', '<br>')

    # Adicionar estilos CSS
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Estudo Técnico Preliminar</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 40px;
                color: #333;
            }}
            h1, h2, h3, h4 {{
                color: #1E3A8A;
            }}
            h1 {{
                text-align: center;
                margin-bottom: 30px;
            }}
            h2 {{
                border-bottom: 1px solid #ddd;
                padding-bottom: 10px;
                margin-top: 30px;
            }}
            .header {{
                text-align: center;
                margin-bottom: 40px;
            }}
            .footer {{
                margin-top: 50px;
                text-align: center;
                font-size: 0.9em;
                color: #666;
            }}
            .section {{
                margin-bottom: 20px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            table, th, td {{
                border: 1px solid #ddd;
            }}
            th, td {{
                padding: 12px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>ESTUDO TÉCNICO PRELIMINAR</h1>
            <p>Documento gerado em {st.session_state.get('data_geracao', 'Data não disponível')}</p>
        </div>
        
        <div class="content">
            {html_content}
        </div>
        
        <div class="footer">
            <p>Documento gerado automaticamente - Gerador de ETP</p>
        </div>
    </body>
    </html>
    """

    return html


def save_etp_as_pdf(html_content: str) -> bytes:
    """
    Converte o conteúdo do ETP em um arquivo PDF usando ReportLab.

    Args:
        html_content: Conteúdo HTML do ETP

    Returns:
        bytes: Conteúdo do PDF em bytes
    """
    try:
        # Criar um buffer para o PDF
        buffer = io.BytesIO()

        # Configurar o documento PDF
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        # Estilos
        styles = getSampleStyleSheet()

        # Modificar estilos existentes em vez de adicionar novos com o mesmo nome
        title_style = styles['Title']
        title_style.fontSize = 16
        title_style.alignment = TA_CENTER
        title_style.spaceAfter = 20

        # Adicionar estilos personalizados com nomes únicos
        styles.add(ParagraphStyle(
            name='Normal_Justify',
            parent=styles['Normal'],
            alignment=TA_JUSTIFY,
            fontSize=10,
            leading=14
        ))

        # Modificar estilos existentes
        heading2_style = styles['Heading2']
        heading2_style.fontSize = 14
        heading2_style.spaceAfter = 10
        heading2_style.spaceBefore = 15

        heading3_style = styles['Heading3']
        heading3_style.fontSize = 12
        heading3_style.spaceAfter = 8
        heading3_style.spaceBefore = 12

        # Remover tags HTML básicas
        content = html_content.replace('<!DOCTYPE html>', '')
        content = re.sub(r'<html>.*?<body>', '', content, flags=re.DOTALL)
        content = content.replace('</body></html>', '')

        # Extrair o conteúdo do HTML
        # Remover estilos e scripts
        content = re.sub(r'<style>.*?</style>', '', content, flags=re.DOTALL)
        content = re.sub(r'<script>.*?</script>', '', content, flags=re.DOTALL)

        # Substituir <br> por quebras de linha
        content = content.replace('<br>', '\n')

        # Remover outras tags HTML
        content = re.sub(r'<[^>]*>', '', content)

        # Dividir o conteúdo em linhas
        lines = content.split('\n')

        # Elementos do documento
        elements = []

        # Adicionar título
        elements.append(
            Paragraph("ESTUDO TÉCNICO PRELIMINAR", styles['Title']))

        # Adicionar data
        data_geracao = st.session_state.get(
            'data_geracao', 'Data não disponível')
        elements.append(
            Paragraph(f"Documento gerado em {data_geracao}", styles['Normal']))
        elements.append(Spacer(1, 0.5*inch))

        # Processar o conteúdo
        current_text = ""

        for line in lines:
            line = line.strip()
            if not line:
                if current_text:
                    elements.append(
                        Paragraph(current_text, styles['Normal_Justify']))
                    current_text = ""
                elements.append(Spacer(1, 0.1*inch))
            elif line.startswith('# '):
                if current_text:
                    elements.append(
                        Paragraph(current_text, styles['Normal_Justify']))
                    current_text = ""
                elements.append(Paragraph(line[2:], styles['Heading1']))
            elif line.startswith('## '):
                if current_text:
                    elements.append(
                        Paragraph(current_text, styles['Normal_Justify']))
                    current_text = ""
                elements.append(Paragraph(line[3:], styles['Heading2']))
            elif line.startswith('### '):
                if current_text:
                    elements.append(
                        Paragraph(current_text, styles['Normal_Justify']))
                    current_text = ""
                elements.append(Paragraph(line[4:], styles['Heading3']))
            elif re.match(r'^#{1,6}\s+', line):
                # Captura qualquer cabeçalho com 1-6 hashtags
                if current_text:
                    elements.append(
                        Paragraph(current_text, styles['Normal_Justify']))
                    current_text = ""
                header_level = len(re.match(r'^(#+)\s+', line).group(1))
                header_text = line[header_level+1:]
                if header_level <= 3:
                    elements.append(
                        Paragraph(header_text, styles[f'Heading{header_level}']))
                else:
                    # Para níveis de cabeçalho acima de 3, use Heading3 com tamanho menor
                    elements.append(Paragraph(header_text, styles['Heading3']))
            else:
                if current_text:
                    current_text += " " + line
                else:
                    current_text = line

        # Adicionar o último parágrafo
        if current_text:
            elements.append(Paragraph(current_text, styles['Normal_Justify']))

        # Adicionar rodapé
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph("Documento gerado automaticamente - Gerador de ETP",
                                  styles['Normal']))

        # Construir o PDF
        doc.build(elements)

        # Obter o conteúdo do buffer
        pdf_bytes = buffer.getvalue()
        buffer.close()

        return pdf_bytes

    except Exception as e:
        st.error(f"Erro ao gerar PDF: {str(e)}")
        return None
