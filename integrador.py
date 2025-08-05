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
from datetime import datetime


# Carrega variáveis de ambiente do arquivo .env
load_dotenv()


class AssistenteEtpInteligente:
    """
    Assistente inteligente para análise contextual de campos do ETP.
    
    Fornece validação de consistência, completude e qualidade dos campos
    baseado no contexto dos campos anteriores e nas normas técnicas.
    """
    
    def __init__(self, provider: str = "openai"):
        """
        Inicializa o assistente com um provedor LLM específico.
        
        Args:
            provider (str): O provedor LLM a ser usado ('openai' ou 'anthropic')
        """
        self.provider = provider.lower()
        self.llm = self._get_llm()
        
        # Definir os prompts especializados para cada campo
        self.prompts_especializados = self._definir_prompts_especializados()
        
        # Mapeamento dos campos críticos
        self.campos_criticos = [
            "descricao_necessidade",
            "historico",
            "solucoes_mercado",
            "dependencia_contratado",
            "transicao_contratual",
            "criterios_sustentabilidade",
            "estimativa_valor",
            "analise_riscos",
            "definicao_objeto",
            "justificativa_escolha",
            "previsao_pca",
            "estimativa_quantidades",
            "justificativa_parcelamento"
        ]
    
    def _get_llm(self):
        """Configura e retorna o modelo LLM com base no provedor."""
        if self.provider == "openai":
            api_key = os.environ.get("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY"))
            if not api_key:
                st.warning("Chave de API da OpenAI não configurada.")
                return None
            return ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key=api_key, max_tokens=2000)

        elif self.provider == "anthropic":
            api_key = os.environ.get("ANTHROPIC_API_KEY", st.secrets.get("ANTHROPIC_API_KEY"))
            if not api_key:
                st.warning("Chave de API da Anthropic não configurada.")
                return None
            return ChatAnthropic(model="claude-3-opus-20240229", temperature=0.3, api_key=api_key, max_tokens=2000)
        
        else:
            raise ValueError(f"Provedor LLM não suportado: {self.provider}.")
    
    def _definir_prompts_especializados(self) -> Dict[str, str]:
        """Define os prompts especializados para cada campo crítico."""
        return {
            "descricao_necessidade": """
            Você é um especialista em elaboração de ETPs conforme a Lei 14.133/2021 e Manual TRT-2.
            
            Analise a DESCRIÇÃO DA NECESSIDADE considerando:
            
            CRITÉRIOS OBRIGATÓRIOS:
            1. Clareza do problema identificado
            2. Conformidade com Decreto 9.507/2018 (análise de execução direta)
            3. Justificativa para terceirização (se aplicável)
            4. Identificação de terceirização lícita/ilícita
            5. Linguagem técnica formal adequada
            
            CONTEXTO ANTERIOR: {contexto_anterior}
            CONTEÚDO ATUAL: {conteudo_atual}
            
            Forneça feedback estruturado:
            - ✅ PONTOS POSITIVOS
            - ⚠️ PONTOS DE ATENÇÃO
            - 📝 SUGESTÕES DE MELHORIA
            - 💡 EXEMPLO MELHORADO (se necessário)
            """,
            
            "historico": """
            Você é um especialista em elaboração de ETPs conforme a Lei 14.133/2021 e Manual TRT-2.
            
            Analise o HISTÓRICO considerando:
            
            CRITÉRIOS OBRIGATÓRIOS:
            1. Consistência com contratações anteriores mencionadas
            2. Lições aprendidas identificadas e documentadas
            3. Oportunidades de melhoria específicas
            4. Análise de relatórios de gestão anteriores
            5. Boletins de Avaliação de Desempenho referenciados
            
            CONTEXTO ANTERIOR: {contexto_anterior}
            CONTEÚDO ATUAL: {conteudo_atual}
            
            Forneça feedback estruturado:
            - ✅ PONTOS POSITIVOS
            - ⚠️ PONTOS DE ATENÇÃO
            - 📝 SUGESTÕES DE MELHORIA
            - 💡 EXEMPLO MELHORADO (se necessário)
            """,
            
            "solucoes_mercado": """
            Você é um especialista em elaboração de ETPs conforme a Lei 14.133/2021 e Manual TRT-2.
            
            Analise as SOLUÇÕES EXISTENTES NO MERCADO considerando:
            
            CRITÉRIOS OBRIGATÓRIOS:
            1. Completude da pesquisa de mercado
            2. Análise comparativa adequada entre alternativas
            3. Vantagens e desvantagens bem fundamentadas
            4. Consideração de execução direta pelo órgão
            5. Justificativa técnica/econômica da escolha
            
            CONTEXTO ANTERIOR: {contexto_anterior}
            CONTEÚDO ATUAL: {conteudo_atual}
            
            Forneça feedback estruturado:
            - ✅ PONTOS POSITIVOS
            - ⚠️ PONTOS DE ATENÇÃO
            - 📝 SUGESTÕES DE MELHORIA
            - 💡 EXEMPLO MELHORADO (se necessário)
            """,
            
            "analise_riscos": """
            Você é um especialista em elaboração de ETPs conforme a Lei 14.133/2021 e Manual TRT-2.
            
            Analise o LEVANTAMENTO E ANÁLISE DE RISCOS considerando:
            
            CRITÉRIOS OBRIGATÓRIOS:
            1. Mapa de Riscos obrigatório elaborado
            2. Identificação adequada de riscos (planejamento, seleção, execução)
            3. Medidas de mitigação propostas
            4. Análise de probabilidade e impacto
            5. Conformidade com metodologia institucional
            
            CONTEXTO ANTERIOR: {contexto_anterior}
            CONTEÚDO ATUAL: {conteudo_atual}
            
            Forneça feedback estruturado:
            - ✅ PONTOS POSITIVOS
            - ⚠️ PONTOS DE ATENÇÃO
            - 📝 SUGESTÕES DE MELHORIA
            - 💡 EXEMPLO MELHORADO (se necessário)
            """,
            
            "criterios_sustentabilidade": """
            Você é um especialista em elaboração de ETPs conforme a Lei 14.133/2021 e Manual TRT-2.
            
            Analise os CRITÉRIOS DE SUSTENTABILIDADE considerando:
            
            CRITÉRIOS OBRIGATÓRIOS:
            1. Conformidade com Guia de Contratações Sustentáveis
            2. Impactos ambientais identificados
            3. Medidas mitigadoras específicas
            4. Requisitos de baixo consumo de energia
            5. Logística reversa para desfazimento
            
            CONTEXTO ANTERIOR: {contexto_anterior}
            CONTEÚDO ATUAL: {conteudo_atual}
            
            Forneça feedback estruturado:
            - ✅ PONTOS POSITIVOS
            - ⚠️ PONTOS DE ATENÇÃO
            - 📝 SUGESTÕES DE MELHORIA
            - 💡 EXEMPLO MELHORADO (se necessário)
            """,
            
            "estimativa_valor": """
            Você é um especialista em elaboração de ETPs conforme a Lei 14.133/2021 e Manual TRT-2.
            
            Analise a ESTIMATIVA DO VALOR DA CONTRATAÇÃO considerando:
            
            CRITÉRIOS OBRIGATÓRIOS:
            1. Metodologia de pesquisa de preços conforme art. 23 Lei 14.133/2021
            2. Custos totais considerados (aquisição + acessórios + ciclo de vida)
            3. Análise comparativa entre soluções
            4. Memórias de cálculo apresentadas
            5. Fontes de pesquisa adequadas (Painel de Preços, SICAF, etc.)
            
            CONTEXTO ANTERIOR: {contexto_anterior}
            CONTEÚDO ATUAL: {conteudo_atual}
            
            Forneça feedback estruturado:
            - ✅ PONTOS POSITIVOS
            - ⚠️ PONTOS DE ATENÇÃO
            - 📝 SUGESTÕES DE MELHORIA
            - 💡 EXEMPLO MELHORADO (se necessário)
            """,
            
            "definicao_objeto": """
            Você é um especialista em elaboração de ETPs conforme a Lei 14.133/2021 e Manual TRT-2.
            
            Analise a DEFINIÇÃO DO OBJETO considerando:
            
            CRITÉRIOS OBRIGATÓRIOS:
            1. Clareza e precisão da descrição
            2. Alinhamento com necessidade identificada
            3. Especificações técnicas adequadas
            4. Conformidade com análise de mercado realizada
            5. Possibilidade de originar múltiplos TRs
            
            CONTEXTO ANTERIOR: {contexto_anterior}
            CONTEÚDO ATUAL: {conteudo_atual}
            
            Forneça feedback estruturado:
            - ✅ PONTOS POSITIVOS
            - ⚠️ PONTOS DE ATENÇÃO
            - 📝 SUGESTÕES DE MELHORIA
            - 💡 EXEMPLO MELHORADO (se necessário)
            """,
            
            "justificativa_escolha": """
            Você é um especialista em elaboração de ETPs conforme a Lei 14.133/2021 e Manual TRT-2.
            
            Analise a JUSTIFICATIVA DE ESCOLHA DA SOLUÇÃO considerando:
            
            CRITÉRIOS OBRIGATÓRIOS:
            1. Fundamentação técnica, operacional e financeira
            2. Comparação adequada com alternativas
            3. Alinhamento com interesse público
            4. Vantajosidade demonstrada
            5. Motivação clara das decisões
            
            CONTEXTO ANTERIOR: {contexto_anterior}
            CONTEÚDO ATUAL: {conteudo_atual}
            
            Forneça feedback estruturado:
            - ✅ PONTOS POSITIVOS
            - ⚠️ PONTOS DE ATENÇÃO
            - 📝 SUGESTÕES DE MELHORIA
            - 💡 EXEMPLO MELHORADO (se necessário)
            """,
            
            "estimativa_quantidades": """
            Você é um especialista em elaboração de ETPs conforme a Lei 14.133/2021 e Manual TRT-2.
            
            Analise a ESTIMATIVA DE QUANTIDADES considerando:
            
            CRITÉRIOS OBRIGATÓRIOS:
            1. Memórias de cálculo apresentadas
            2. Consideração de economia de escala
            3. Interdependências com outras contratações
            4. Histórico de consumo analisado
            5. Previsões futuras fundamentadas
            
            CONTEXTO ANTERIOR: {contexto_anterior}
            CONTEÚDO ATUAL: {conteudo_atual}
            
            Forneça feedback estruturado:
            - ✅ PONTOS POSITIVOS
            - ⚠️ PONTOS DE ATENÇÃO
            - 📝 SUGESTÕES DE MELHORIA
            - 💡 EXEMPLO MELHORADO (se necessário)
            """,
            
            "justificativa_parcelamento": """
            Você é um especialista em elaboração de ETPs conforme a Lei 14.133/2021 e Manual TRT-2.
            
            Analise as JUSTIFICATIVAS PARA PARCELAMENTO, AGRUPAMENTO E SUBCONTRATAÇÃO considerando:
            
            CRITÉRIOS OBRIGATÓRIOS:
            1. Análise de viabilidade técnica e econômica
            2. Conformidade com Súmula 247 do TCU
            3. Justificativas adequadas para decisões
            4. Consideração de economia de escala
            5. Avaliação de divisibilidade do objeto
            
            CONTEXTO ANTERIOR: {contexto_anterior}
            CONTEÚDO ATUAL: {conteudo_atual}
            
            Forneça feedback estruturado:
            - ✅ PONTOS POSITIVOS
            - ⚠️ PONTOS DE ATENÇÃO
            - 📝 SUGESTÕES DE MELHORIA
            - 💡 EXEMPLO MELHORADO (se necessário)
            """
        }
    
    def analisar_campo(self, nome_campo: str, conteudo_atual: str, contexto_anterior: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analisa um campo específico considerando o contexto anterior.
        
        Args:
            nome_campo (str): Nome do campo sendo analisado
            conteudo_atual (str): Conteúdo atual do campo
            contexto_anterior (Dict): Contexto dos campos anteriores
            
        Returns:
            Dict: Análise estruturada com feedback e sugestões
        """
        if not self.llm:
            return {
                "erro": "LLM não inicializado. Verifique as chaves de API.",
                "feedback": "",
                "sugestoes": [],
                "qualidade": "erro"
            }
        
        # Verificar se o campo tem prompt especializado
        if nome_campo not in self.prompts_especializados:
            return self._analise_generica(nome_campo, conteudo_atual, contexto_anterior)
        
        # Formatar contexto anterior
        contexto_formatado = self._formatar_contexto(contexto_anterior)
        
        # Obter prompt especializado
        prompt_template = self.prompts_especializados[nome_campo]
        
        # Criar prompt final
        prompt_final = prompt_template.format(
            contexto_anterior=contexto_formatado,
            conteudo_atual=conteudo_atual
        )
        
        try:
            # Criar template de chat
            chat_template = ChatPromptTemplate.from_messages([
                ("system", "Você é um especialista em elaboração de documentos técnicos governamentais, "
                          "especialmente ETPs conforme Lei 14.133/2021 e Manual TRT-2."),
                ("user", prompt_final)
            ])
            
            # Criar cadeia de processamento
            chain = chat_template | self.llm | StrOutputParser()
            
            # Executar análise
            resultado = chain.invoke({})
            
            # Processar resultado
            return self._processar_resultado_analise(resultado, nome_campo)
            
        except Exception as e:
            st.error(f"Erro na análise do campo {nome_campo}: {str(e)}")
            return {
                "erro": f"Erro na análise: {str(e)}",
                "feedback": "",
                "sugestoes": [],
                "qualidade": "erro"
            }
    
    def _formatar_contexto(self, contexto: Dict[str, Any]) -> str:
        """Formata o contexto anterior para inclusão no prompt."""
        if not contexto:
            return "Nenhum contexto anterior disponível."
        
        contexto_formatado = []
        for campo, valor in contexto.items():
            if valor and str(valor).strip():
                contexto_formatado.append(f"**{campo.upper()}**: {str(valor)[:200]}...")
        
        return "\n".join(contexto_formatado) if contexto_formatado else "Nenhum contexto anterior disponível."
    
    def _analise_generica(self, nome_campo: str, conteudo_atual: str, contexto_anterior: Dict[str, Any]) -> Dict[str, Any]:
        """Realiza análise genérica para campos sem prompt especializado."""
        prompt_generico = f"""
        Analise o campo "{nome_campo}" de um ETP considerando:
        
        1. Clareza e objetividade do conteúdo
        2. Adequação à linguagem técnica formal
        3. Completude das informações
        4. Consistência com contexto anterior
        
        CONTEXTO ANTERIOR: {self._formatar_contexto(contexto_anterior)}
        CONTEÚDO ATUAL: {conteudo_atual}
        
        Forneça feedback estruturado com sugestões de melhoria.
        """
        
        try:
            chat_template = ChatPromptTemplate.from_messages([
                ("system", "Você é um especialista em documentos técnicos governamentais."),
                ("user", prompt_generico)
            ])
            
            chain = chat_template | self.llm | StrOutputParser()
            resultado = chain.invoke({})
            
            return self._processar_resultado_analise(resultado, nome_campo)
            
        except Exception as e:
            return {
                "erro": f"Erro na análise genérica: {str(e)}",
                "feedback": "",
                "sugestoes": [],
                "qualidade": "erro"
            }
    
    def _processar_resultado_analise(self, resultado: str, nome_campo: str) -> Dict[str, Any]:
        """Processa o resultado da análise e estrutura a resposta."""
        # Extrair seções do resultado
        pontos_positivos = self._extrair_secao(resultado, "✅ PONTOS POSITIVOS", "⚠️")
        pontos_atencao = self._extrair_secao(resultado, "⚠️ PONTOS DE ATENÇÃO", "📝")
        sugestoes = self._extrair_secao(resultado, "📝 SUGESTÕES DE MELHORIA", "💡")
        exemplo = self._extrair_secao(resultado, "💡 EXEMPLO MELHORADO", "")
        
        # Determinar qualidade geral
        qualidade = self._determinar_qualidade(pontos_atencao, sugestoes)
        
        return {
            "campo": nome_campo,
            "feedback": resultado,
            "pontos_positivos": pontos_positivos,
            "pontos_atencao": pontos_atencao,
            "sugestoes": sugestoes,
            "exemplo_melhorado": exemplo,
            "qualidade": qualidade,
            "timestamp": datetime.now().isoformat()
        }
    
    def _extrair_secao(self, texto: str, inicio: str, fim: str) -> str:
        """Extrai uma seção específica do texto de análise."""
        try:
            start_idx = texto.find(inicio)
            if start_idx == -1:
                return ""
            
            start_idx += len(inicio)
            
            if fim:
                end_idx = texto.find(fim, start_idx)
                if end_idx == -1:
                    return texto[start_idx:].strip()
                return texto[start_idx:end_idx].strip()
            else:
                return texto[start_idx:].strip()
                
        except Exception:
            return ""
    
    def _determinar_qualidade(self, pontos_atencao: str, sugestoes: str) -> str:
        """Determina a qualidade geral baseada nos pontos de atenção e sugestões."""
        if not pontos_atencao and not sugestoes:
            return "excelente"
        elif len(pontos_atencao) < 100 and len(sugestoes) < 200:
            return "boa"
        elif len(pontos_atencao) < 300 and len(sugestoes) < 500:
            return "regular"
        else:
            return "precisa_melhorar"
    
    def validar_consistencia_geral(self, dados_etp: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida a consistência geral entre todos os campos do ETP.
        
        Args:
            dados_etp (Dict): Todos os dados do ETP preenchidos
            
        Returns:
            Dict: Análise de consistência geral
        """
        if not self.llm:
            return {"erro": "LLM não inicializado"}
        
        prompt_consistencia = f"""
        Analise a consistência geral entre todos os campos deste ETP:
        
        DADOS DO ETP:
        {self._formatar_dados_completos(dados_etp)}
        
        Verifique:
        1. Consistência entre problema identificado e solução proposta
        2. Alinhamento entre histórico e necessidade atual
        3. Coerência entre análise de mercado e escolha da solução
        4. Adequação entre riscos identificados e medidas propostas
        5. Conformidade geral com Lei 14.133/2021
        
        Forneça análise estruturada com:
        - Inconsistências identificadas
        - Recomendações de ajustes
        - Avaliação geral de qualidade
        """
        
        try:
            chat_template = ChatPromptTemplate.from_messages([
                ("system", "Você é um especialista em ETPs e Lei 14.133/2021."),
                ("user", prompt_consistencia)
            ])
            
            chain = chat_template | self.llm | StrOutputParser()
            resultado = chain.invoke({})
            
            return {
                "analise_geral": resultado,
                "timestamp": datetime.now().isoformat(),
                "status": "concluida"
            }
            
        except Exception as e:
            return {
                "erro": f"Erro na validação geral: {str(e)}",
                "status": "erro"
            }
    
    def _formatar_dados_completos(self, dados_etp: Dict[str, Any]) -> str:
        """Formata todos os dados do ETP para análise geral."""
        dados_formatados = []
        
        for campo, valor in dados_etp.items():
            if valor and str(valor).strip():
                # Limitar tamanho para não sobrecarregar o prompt
                valor_limitado = str(valor)[:300] + "..." if len(str(valor)) > 300 else str(valor)
                dados_formatados.append(f"**{campo.upper()}**: {valor_limitado}")
        
        return "\n\n".join(dados_formatados)
    
    def melhorar_texto(self, texto: str, tipo_melhoria: str = "geral") -> Dict[str, Any]:
        """
        Melhora um texto específico com foco em qualidade técnica.
        
        Args:
            texto (str): Texto a ser melhorado
            tipo_melhoria (str): Tipo de melhoria ('gramatica', 'tecnico', 'geral')
            
        Returns:
            Dict: Texto melhorado e explicação das mudanças
        """
        if not self.llm:
            return {"erro": "LLM não inicializado"}
        
        prompts_melhoria = {
            "gramatica": """
            Corrija apenas os erros gramaticais e de ortografia do texto abaixo,
            mantendo o conteúdo técnico inalterado:
            
            TEXTO ORIGINAL:
            {texto}
            
            Forneça:
            1. TEXTO CORRIGIDO
            2. PRINCIPAIS CORREÇÕES REALIZADAS
            """,
            
            "tecnico": """
            Melhore a linguagem técnica do texto abaixo para adequá-lo aos padrões
            de documentos governamentais conforme Lei 14.133/2021:
            
            TEXTO ORIGINAL:
            {texto}
            
            Forneça:
            1. TEXTO MELHORADO (linguagem técnica formal)
            2. PRINCIPAIS MELHORIAS REALIZADAS
            """,
            
            "geral": """
            Melhore o texto abaixo considerando:
            - Correção gramatical
            - Linguagem técnica formal adequada
            - Clareza e objetividade
            - Estruturação de parágrafos
            
            TEXTO ORIGINAL:
            {texto}
            
            Forneça:
            1. TEXTO MELHORADO
            2. PRINCIPAIS MELHORIAS REALIZADAS
            """
        }
        
        prompt_escolhido = prompts_melhoria.get(tipo_melhoria, prompts_melhoria["geral"])
        
        try:
            chat_template = ChatPromptTemplate.from_messages([
                ("system", "Você é um especialista em redação técnica para documentos governamentais."),
                ("user", prompt_escolhido.format(texto=texto))
            ])
            
            chain = chat_template | self.llm | StrOutputParser()
            resultado = chain.invoke({})
            
            # Processar resultado
            partes = resultado.split("2. PRINCIPAIS")
            texto_melhorado = partes[0].replace("1. TEXTO MELHORADO", "").replace("1. TEXTO CORRIGIDO", "").strip()
            melhorias = partes[1] if len(partes) > 1 else "Melhorias aplicadas."
            
            return {
                "texto_original": texto,
                "texto_melhorado": texto_melhorado,
                "melhorias_realizadas": melhorias,
                "tipo_melhoria": tipo_melhoria,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "erro": f"Erro na melhoria do texto: {str(e)}",
                "texto_original": texto
            }
    
    def gerar_exemplo_campo(self, nome_campo: str, contexto_anterior: Dict[str, Any]) -> str:
        """
        Gera um exemplo de preenchimento para um campo específico.
        
        Args:
            nome_campo (str): Nome do campo
            contexto_anterior (Dict): Contexto dos campos anteriores
            
        Returns:
            str: Exemplo de preenchimento
        """
        if not self.llm:
            return "Erro: LLM não inicializado."
        
        contexto_formatado = self._formatar_contexto(contexto_anterior)
        
        prompt_exemplo = f"""
        Gere um exemplo de preenchimento para o campo "{nome_campo}" de um ETP,
        considerando o contexto anterior e as normas da Lei 14.133/2021.
        
        CONTEXTO ANTERIOR:
        {contexto_formatado}
        
        CAMPO A PREENCHER: {nome_campo}
        
        Forneça um exemplo prático, técnico e bem estruturado que sirva como
        referência para o usuário.
        """
        
        try:
            chat_template = ChatPromptTemplate.from_messages([
                ("system", "Você é um especialista em ETPs e Lei 14.133/2021."),
                ("user", prompt_exemplo)
            ])
            
            chain = chat_template | self.llm | StrOutputParser()
            return chain.invoke({})
            
        except Exception as e:
            return f"Erro ao gerar exemplo: {str(e)}"
    
    def _mapear_campo_para_secao_trt2(self, nome_campo: str) -> Dict[str, str]:
        """Mapeia campos do formulário para seções do Manual TRT-2."""
        mapeamento = {
            "descricao_problema": {
                "secao_trt2": "1. DESCRIÇÃO DA NECESSIDADE",
                "prompt_especializado": "descricao_necessidade",
                "criterios_obrigatorios": [
                    "Conformidade com Decreto 9.507/2018",
                    "Justificativa para terceirização",
                    "Identificação de terceirização lícita/ilícita",
                    "Linguagem técnica formal"
                ]
            },
            "solucoes_mercado": {
                "secao_trt2": "3. SOLUÇÕES EXISTENTES NO MERCADO",
                "prompt_especializado": "solucoes_mercado",
                "criterios_obrigatorios": [
                    "Pesquisa abrangente de alternativas",
                    "Análise comparativa técnica e econômica",
                    "Consideração de execução direta",
                    "Vantagens e desvantagens fundamentadas"
                ]
            },
            "solucao_proposta": {
                "secao_trt2": "7. DEFINIÇÃO DO OBJETO",
                "prompt_especializado": "definicao_objeto",
                "criterios_obrigatorios": [
                    "Descrição técnica precisa",
                    "Especificações detalhadas",
                    "Alinhamento com necessidade",
                    "Possibilidade de múltiplos TRs"
                ]
            },
            "justificativa_escolha": {
                "secao_trt2": "8. JUSTIFICATIVA DE ESCOLHA DA SOLUÇÃO",
                "prompt_especializado": "justificativa_escolha",
                "criterios_obrigatorios": [
                    "Fundamentação técnica/operacional/financeira",
                    "Demonstração de vantajosidade",
                    "Comparação com alternativas",
                    "Alinhamento com interesse público"
                ]
            },
            "estrategia_implantacao": {
                "secao_trt2": "14. ESTRATÉGIA DE IMPLANTAÇÃO",
                "prompt_especializado": "generico",
                "criterios_obrigatorios": [
                    "Metodologia de implementação detalhada",
                    "Cronograma executivo com marcos",
                    "Recursos humanos e materiais",
                    "Plano de gestão de mudanças"
                ]
            },
            "beneficios": {
                "secao_trt2": "15. BENEFÍCIOS ESPERADOS",
                "prompt_especializado": "generico",
                "criterios_obrigatorios": [
                    "Benefícios quantitativos e qualitativos",
                    "Indicadores de desempenho",
                    "Beneficiários diretos e indiretos",
                    "Retorno sobre investimento"
                ]
            }
        }
        
        return mapeamento.get(nome_campo, {
            "secao_trt2": "Seção Genérica",
            "prompt_especializado": "generico",
            "criterios_obrigatorios": ["Análise geral de qualidade"]
        })
    
    def analisar_campo_com_contexto_trt2(self, nome_campo: str, conteudo_atual: str,
                                        contexto_anterior: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analisa campo considerando contexto TRT-2 e integração com novo prompt.
        """
        # Obter mapeamento para seção TRT-2
        mapeamento = self._mapear_campo_para_secao_trt2(nome_campo)
        
        # Análise normal do campo
        resultado = self.analisar_campo(nome_campo, conteudo_atual, contexto_anterior)
        
        # Adicionar contexto TRT-2
        if "erro" not in resultado:
            resultado["secao_trt2"] = mapeamento["secao_trt2"]
            resultado["criterios_obrigatorios"] = mapeamento["criterios_obrigatorios"]
            resultado["conformidade_manual"] = self._avaliar_conformidade_manual(
                conteudo_atual, mapeamento["criterios_obrigatorios"]
            )
        
        return resultado
    
    def _avaliar_conformidade_manual(self, conteudo: str, criterios: list) -> bool:
        """
        Avalia se o conteúdo está conforme com os critérios do Manual TRT-2.
        """
        if not conteudo or len(conteudo.strip()) < 50:
            return False
        
        # Verificações básicas de conformidade
        conformidade_basica = [
            len(conteudo.strip()) >= 100,  # Conteúdo mínimo
            not any(palavra in conteudo.lower() for palavra in ['bullet', '•', '-']),  # Sem bullets
            any(palavra in conteudo.lower() for palavra in ['técnico', 'análise', 'conformidade']),  # Linguagem técnica
        ]
        
        return sum(conformidade_basica) >= 2  # Pelo menos 2 de 3 critérios
    
    def validar_alinhamento_prompt_tecnico(self, dados_etp: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida se os dados estão alinhados com a estrutura do novo prompt técnico.
        """
        validacoes = []
        
        # Verificar campos obrigatórios para cada seção TRT-2
        secoes_obrigatorias = {
            "1. DESCRIÇÃO DA NECESSIDADE": dados_etp.get('descricao_problema'),
            "3. SOLUÇÕES EXISTENTES NO MERCADO": dados_etp.get('solucoes_mercado'),
            "7. DEFINIÇÃO DO OBJETO": dados_etp.get('solucao_proposta'),
            "8. JUSTIFICATIVA DE ESCOLHA": dados_etp.get('justificativa_escolha'),
            "14. ESTRATÉGIA DE IMPLANTAÇÃO": dados_etp.get('estrategia_implantacao'),
            "15. BENEFÍCIOS ESPERADOS": dados_etp.get('beneficios')
        }
        
        for secao, conteudo in secoes_obrigatorias.items():
            if not conteudo or not conteudo.strip():
                validacoes.append(f"⚠️ Seção '{secao}' não preenchida adequadamente")
            elif len(conteudo.strip()) < 50:
                validacoes.append(f"⚠️ Seção '{secao}' precisa de mais detalhamento")
        
        # Verificar coerência entre seções
        coerencia = self._verificar_coerencia_secoes(dados_etp)
        validacoes.extend(coerencia)
        
        return {
            "validacoes": validacoes,
            "status": "aprovado" if len(validacoes) == 0 else "requer_ajustes",
            "conformidade_trt2": len(validacoes) == 0,
            "timestamp": datetime.now().isoformat()
        }
    
    def _verificar_coerencia_secoes(self, dados_etp: Dict[str, Any]) -> list:
        """
        Verifica coerência entre as seções do ETP.
        """
        inconsistencias = []
        
        # Verificar se solução proposta está alinhada com problema identificado
        problema = dados_etp.get('descricao_problema', '').lower()
        solucao = dados_etp.get('solucao_proposta', '').lower()
        
        if problema and solucao:
            # Verificação básica de alinhamento (pode ser melhorada com NLP)
            palavras_problema = set(problema.split())
            palavras_solucao = set(solucao.split())
            intersecao = len(palavras_problema.intersection(palavras_solucao))
            
            if intersecao < 3:  # Muito pouca sobreposição
                inconsistencias.append("⚠️ Solução proposta pode não estar alinhada com problema identificado")
        
        # Verificar se justificativa está coerente com análise de mercado
        mercado = dados_etp.get('solucoes_mercado', '').lower()
        justificativa = dados_etp.get('justificativa_escolha', '').lower()
        
        if mercado and justificativa:
            if 'comparativo' in mercado and 'vantagem' not in justificativa:
                inconsistencias.append("⚠️ Justificativa deveria mencionar vantagens identificadas na análise de mercado")
        
        return inconsistencias


# Funções auxiliares para integração com Streamlit
def criar_assistente_etp(provider: str = "openai") -> AssistenteEtpInteligente:
    """Cria uma instância do assistente ETP."""
    return AssistenteEtpInteligente(provider=provider)


def exibir_feedback_campo(feedback_resultado: Dict[str, Any]) -> None:
    """
    Exibe o feedback de um campo no Streamlit de forma estruturada.
    
    Args:
        feedback_resultado (Dict): Resultado da análise do campo
    """
    if "erro" in feedback_resultado:
        st.error(f"❌ {feedback_resultado['erro']}")
        return
    
    # Indicador de qualidade
    qualidade = feedback_resultado.get("qualidade", "regular")
    cores_qualidade = {
        "excelente": "🟢",
        "boa": "🟡",
        "regular": "🟠",
        "precisa_melhorar": "🔴",
        "erro": "❌"
    }
    
    st.markdown(f"### {cores_qualidade.get(qualidade, '🟡')} Análise do Campo")
    
    # Pontos positivos
    if feedback_resultado.get("pontos_positivos"):
        with st.expander("✅ Pontos Positivos", expanded=True):
            st.markdown(feedback_resultado["pontos_positivos"])
    
    # Pontos de atenção
    if feedback_resultado.get("pontos_atencao"):
        with st.expander("⚠️ Pontos de Atenção", expanded=True):
            st.warning(feedback_resultado["pontos_atencao"])
    
    # Sugestões de melhoria
    if feedback_resultado.get("sugestoes"):
        with st.expander("📝 Sugestões de Melhoria", expanded=True):
            st.info(feedback_resultado["sugestoes"])
    
    # Exemplo melhorado
    if feedback_resultado.get("exemplo_melhorado"):
        with st.expander("💡 Exemplo Melhorado", expanded=False):
            st.code(feedback_resultado["exemplo_melhorado"], language="text")


def criar_botao_ajuda_campo(nome_campo: str, conteudo_atual: str, contexto_anterior: Dict[str, Any],
                           assistente: AssistenteEtpInteligente) -> None:
    """
    Cria um botão de ajuda para um campo específico.
    
    Args:
        nome_campo (str): Nome do campo
        conteudo_atual (str): Conteúdo atual do campo
        contexto_anterior (Dict): Contexto dos campos anteriores
        assistente (AssistenteEtpInteligente): Instância do assistente
    """
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button(f"🤖 Analisar {nome_campo}", key=f"analisar_{nome_campo}"):
            if conteudo_atual.strip():
                with st.spinner("Analisando campo..."):
                    resultado = assistente.analisar_campo(nome_campo, conteudo_atual, contexto_anterior)
                    exibir_feedback_campo(resultado)
            else:
                st.warning("⚠️ Preencha o campo antes de solicitar análise.")
    
    with col2:
        if st.button(f"📝 Melhorar Texto", key=f"melhorar_{nome_campo}"):
            if conteudo_atual.strip():
                with st.spinner("Melhorando texto..."):
                    resultado = assistente.melhorar_texto(conteudo_atual, "geral")
                    if "erro" not in resultado:
                        st.success("✅ Texto melhorado!")
                        st.markdown("**Texto Melhorado:**")
                        st.text_area("Texto melhorado", value=resultado["texto_melhorado"],
                                   key=f"melhorado_{nome_campo}", height=150, label_visibility="collapsed")
                        st.markdown("**Melhorias Realizadas:**")
                        st.info(resultado["melhorias_realizadas"])
                    else:
                        st.error(resultado["erro"])
            else:
                st.warning("⚠️ Preencha o campo antes de solicitar melhoria.")
    
    with col3:
        if st.button(f"💡 Ver Exemplo", key=f"exemplo_{nome_campo}"):
            with st.spinner("Gerando exemplo..."):
                exemplo = assistente.gerar_exemplo_campo(nome_campo, contexto_anterior)
                st.markdown("**Exemplo de Preenchimento:**")
                st.text_area("Exemplo de preenchimento", value=exemplo, key=f"exemplo_texto_{nome_campo}", height=150, label_visibility="collapsed")


def criar_botao_ajuda_campo_trt2(assistente: AssistenteEtpInteligente, nome_campo: str,
                                conteudo_atual: str, contexto_anterior: Dict[str, Any],
                                feedback_key: str) -> Dict[str, Any]:
    """
    Cria botões de ajuda para um campo específico com integração TRT-2.
    
    Args:
        assistente (AssistenteEtpInteligente): Instância do assistente
        nome_campo (str): Nome do campo
        conteudo_atual (str): Conteúdo atual do campo
        contexto_anterior (Dict): Contexto dos campos anteriores
        feedback_key (str): Chave para armazenar feedback
        
    Returns:
        Dict: Resultado da análise se executada
    """
    col1, col2, col3 = st.columns([1, 1, 1])
    
    feedback_resultado = None
    
    with col1:
        if st.button(f"🤖 Analisar", key=f"analisar_trt2_{feedback_key}"):
            if conteudo_atual.strip():
                with st.spinner("Analisando campo com contexto TRT-2..."):
                    # Usar método integrado com TRT-2
                    feedback_resultado = assistente.analisar_campo_com_contexto_trt2(
                        nome_campo, conteudo_atual, contexto_anterior
                    )
                    return feedback_resultado
            else:
                st.warning("⚠️ Preencha o campo antes de solicitar análise.")
    
    with col2:
        if st.button(f"📝 Melhorar", key=f"melhorar_trt2_{feedback_key}"):
            if conteudo_atual.strip():
                with st.spinner("Melhorando texto..."):
                    resultado = assistente.melhorar_texto(conteudo_atual, "tecnico")
                    if "erro" not in resultado:
                        st.success("✅ Texto melhorado!")
                        st.markdown("**Texto Melhorado:**")
                        st.text_area("Texto melhorado TRT-2", value=resultado["texto_melhorado"],
                                   key=f"melhorado_trt2_{feedback_key}", height=150, label_visibility="collapsed")
                        st.markdown("**Melhorias Realizadas:**")
                        st.info(resultado["melhorias_realizadas"])
                    else:
                        st.error(resultado["erro"])
            else:
                st.warning("⚠️ Preencha o campo antes de solicitar melhoria.")
    
    with col3:
        if st.button(f"💡 Exemplo", key=f"exemplo_trt2_{feedback_key}"):
            with st.spinner("Gerando exemplo..."):
                exemplo = assistente.gerar_exemplo_campo(nome_campo, contexto_anterior)
                st.markdown("**Exemplo de Preenchimento:**")
                st.text_area("Exemplo TRT-2", value=exemplo, key=f"exemplo_texto_trt2_{feedback_key}", height=150, label_visibility="collapsed")
    
    return feedback_resultado


def exibir_feedback_campo_trt2(feedback_resultado: Dict[str, Any]) -> None:
    """
    Exibe feedback de campo com informações do Manual TRT-2.
    """
    if "erro" in feedback_resultado:
        st.error(f"❌ {feedback_resultado['erro']}")
        return
    
    # Indicador de qualidade + conformidade TRT-2
    qualidade = feedback_resultado.get("qualidade", "regular")
    conformidade = feedback_resultado.get("conformidade_manual", False)
    
    cores_qualidade = {
        "excelente": "🟢",
        "boa": "🟡",
        "regular": "🟠",
        "precisa_melhorar": "🔴",
        "erro": "❌"
    }
    
    # Título com indicadores
    titulo = f"### {cores_qualidade.get(qualidade, '🟡')} Análise do Campo"
    if conformidade:
        titulo += " ✅ Conforme TRT-2"
    else:
        titulo += " ⚠️ Requer Adequação TRT-2"
    
    st.markdown(titulo)
    
    # Seção TRT-2 correspondente
    if feedback_resultado.get("secao_trt2"):
        st.info(f"📋 **Seção Manual TRT-2:** {feedback_resultado['secao_trt2']}")
    
    # Critérios obrigatórios
    if feedback_resultado.get("criterios_obrigatorios"):
        with st.expander("📋 Critérios Obrigatórios (Manual TRT-2)", expanded=False):
            for criterio in feedback_resultado["criterios_obrigatorios"]:
                st.markdown(f"• {criterio}")
    
    # Pontos positivos
    if feedback_resultado.get("pontos_positivos"):
        with st.expander("✅ Pontos Positivos", expanded=True):
            st.markdown(feedback_resultado["pontos_positivos"])
    
    # Pontos de atenção
    if feedback_resultado.get("pontos_atencao"):
        with st.expander("⚠️ Pontos de Atenção", expanded=True):
            st.warning(feedback_resultado["pontos_atencao"])
    
    # Sugestões de melhoria
    if feedback_resultado.get("sugestoes"):
        with st.expander("📝 Sugestões de Melhoria", expanded=True):
            st.info(feedback_resultado["sugestoes"])
    
    # Exemplo melhorado
    if feedback_resultado.get("exemplo_melhorado"):
        with st.expander("💡 Exemplo Melhorado", expanded=False):
            st.code(feedback_resultado["exemplo_melhorado"], language="text")


def criar_validacao_completa_trt2(dados_etp: Dict[str, Any], assistente: AssistenteEtpInteligente) -> None:
    """
    Cria interface para validação completa contra Manual TRT-2.
    """
    st.markdown("---")
    st.markdown("### 🏛️ Validação Manual TRT-2")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📋 Validar Conformidade TRT-2", help="Verifica conformidade com todas as seções obrigatórias"):
            with st.spinner("Validando conformidade com Manual TRT-2..."):
                validacao = assistente.validar_alinhamento_prompt_tecnico(dados_etp)
                
                if validacao["status"] == "aprovado":
                    st.success("✅ ETP conforme com Manual TRT-2!")
                else:
                    st.warning("⚠️ ETP requer ajustes para conformidade:")
                    for validacao_item in validacao["validacoes"]:
                        st.markdown(f"• {validacao_item}")
    
    with col2:
        if st.button("🔍 Análise Detalhada TRT-2", help="Análise detalhada de cada seção"):
            st.info("Funcionalidade em desenvolvimento - análise seção por seção")


class EtpLlmGenerator:
    """Gerador de Estudos Técnicos Preliminares (ETP) usando LangChain."""

    def __init__(self, provider: str = "openai"):
        """
        Inicializa o gerador de ETP com um provedor LLM específico.

        Args:
            provider (str): O provedor LLM a ser usado ('openai' ou 'anthropic')
        """
        self.provider = provider.lower()
        self.llm = self._get_llm()

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

    def _get_llm(self):
        """Configura e retorna o modelo LLM com base no provedor."""
        if self.provider == "openai":
            api_key = os.environ.get("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY"))
            if not api_key:
                st.warning("Chave de API da OpenAI não configurada.")
                return None
            return ChatOpenAI(model="gpt-4o-mini", temperature=0.7, api_key=api_key, max_tokens=8000)

        elif self.provider == "anthropic":
            api_key = os.environ.get("ANTHROPIC_API_KEY", st.secrets.get("ANTHROPIC_API_KEY"))
            if not api_key:
                st.warning("Chave de API da Anthropic não configurada.")
                return None
            return ChatAnthropic(model="claude-3-opus-20240229", temperature=0.7, api_key=api_key, max_tokens=8000)

        else:
            raise ValueError(f"Provedor LLM não suportado: {self.provider}.")

    def _construct_prompt(self, dados_etp: Dict[str, Any]) -> str:
        """Constrói prompt técnico conforme Manual TRT-2 e Lei 14.133/2021."""
        return self._construct_prompt_tecnico_trt2(dados_etp)
    
    def _construct_prompt_tecnico_trt2(self, dados_etp: Dict[str, Any]) -> str:
        """Constrói prompt técnico conforme Manual TRT-2 e Lei 14.133/2021."""
        
        # Formatar valores monetários
        valor_min = f"R$ {dados_etp['valor_minimo']:,.2f}".replace(",", "X").replace(
            ".", ",").replace("X", ".") if dados_etp['valor_minimo'] else "Não informado"
        valor_med = f"R$ {dados_etp['valor_medio']:,.2f}".replace(",", "X").replace(
            ".", ",").replace("X", ".") if dados_etp['valor_medio'] else "Não informado"
        valor_max = f"R$ {dados_etp['valor_maximo']:,.2f}".replace(",", "X").replace(
            ".", ",").replace("X", ".") if dados_etp['valor_maximo'] else "Não informado"

        orgao_responsavel = dados_etp.get('orgao_responsavel', 'Órgão Público')
        
        prompt_tecnico = f"""
Elabore um Estudo Técnico Preliminar (ETP) em conformidade com a Lei 14.133/2021 e melhores práticas de contratações públicas.

IMPORTANTE: O documento deve seguir RIGOROSAMENTE a estrutura técnica formal de documentos governamentais, com linguagem jurídico-administrativa adequada e fundamentação legal completa.

## DADOS FORNECIDOS PELO USUÁRIO:

**ÓRGÃO RESPONSÁVEL:**
- {orgao_responsavel}

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

    def generate_etp(self, dados_etp: Dict[str, Any]) -> str:
        """Gera o ETP usando o LLM configurado com geração modular."""
        if not self.llm:
            return "Erro: LLM não inicializado. Verifique as chaves de API."
        
        try:
            # Usar geração modular para garantir completude
            result = self.generate_etp_modular(dados_etp)
            return result
        except Exception as e:
            st.error(f"Erro ao gerar o ETP: {str(e)}")
            return f"Erro na geração do documento: {str(e)}"
    
    def generate_etp_modular(self, dados_etp: Dict[str, Any]) -> str:
        """Gera ETP em etapas para evitar truncamento."""
        
        # Dividir as 17 seções em 3 grupos
        grupos_secoes = [
            [1, 2, 3, 4, 5, 6],      # Seções 1-6
            [7, 8, 9, 10, 11, 12],   # Seções 7-12
            [13, 14, 15, 16, 17]     # Seções 13-17 (inclui cronograma)
        ]
        
        documento_completo = []
        
        for i, grupo in enumerate(grupos_secoes):
            st.info(f"Gerando seções {grupo[0]}-{grupo[-1]}...")
            prompt_grupo = self._construct_prompt_grupo(dados_etp, grupo)
            resultado_grupo = self.chain.invoke({"prompt": prompt_grupo})
            documento_completo.append(resultado_grupo)
        
        # Juntar documento completo
        documento_final = "\n\n".join(documento_completo)
        
        # Validar completude
        validacao = self._validar_completude_etp(documento_final)
        if not validacao["completo"]:
            st.warning(f"⚠️ Algumas seções podem estar incompletas: {', '.join(validacao['secoes_ausentes'])}")
            st.info(f"📊 Completude: {validacao['percentual_completude']:.1f}%")
        else:
            st.success("✅ Todas as 17 seções foram geradas com sucesso!")
        
        return documento_final
    
    def _construct_prompt_grupo(self, dados_etp: Dict[str, Any], secoes: list) -> str:
        """Constrói prompt para um grupo específico de seções."""
        
        # Formatar valores monetários
        valor_min = f"R$ {dados_etp['valor_minimo']:,.2f}".replace(",", "X").replace(
            ".", ",").replace("X", ".") if dados_etp['valor_minimo'] else "Não informado"
        valor_med = f"R$ {dados_etp['valor_medio']:,.2f}".replace(",", "X").replace(
            ".", ",").replace("X", ".") if dados_etp['valor_medio'] else "Não informado"
        valor_max = f"R$ {dados_etp['valor_maximo']:,.2f}".replace(",", "X").replace(
            ".", ",").replace("X", ".") if dados_etp['valor_maximo'] else "Não informado"

        orgao_responsavel = dados_etp.get('orgao_responsavel', 'Órgão Público')
        
        # Definir seções por grupo
        secoes_definicoes = {
            1: "**1. DESCRIÇÃO DA NECESSIDADE**\n- Contextualização do problema ou oportunidade identificada\n- Análise de conformidade com Decreto 9.507/2018 (execução direta vs. terceirização)\n- Justificativa técnica para a contratação\n- Identificação de terceirização lícita/ilícita quando aplicável",
            2: "**2. HISTÓRICO DE CONTRATAÇÕES SIMILARES**\n- Levantamento de contratações anteriores relacionadas\n- Lições aprendidas de contratos similares\n- Análise de relatórios de gestão contratuais anteriores\n- Identificação de oportunidades de melhoria",
            3: "**3. SOLUÇÕES EXISTENTES NO MERCADO**\n- Pesquisa abrangente de alternativas disponíveis\n- Análise comparativa técnica e econômica\n- Consideração de execução direta pelo órgão\n- Vantagens e desvantagens de cada alternativa",
            4: "**4. LEVANTAMENTO E ANÁLISE DE RISCOS**\n- Elaboração de Mapa de Riscos obrigatório\n- Identificação de riscos de planejamento, seleção e execução\n- Análise de probabilidade e impacto\n- Medidas de mitigação propostas",
            5: "**5. CRITÉRIOS DE SUSTENTABILIDADE**\n- Conformidade com Guia de Contratações Sustentáveis\n- Identificação de impactos ambientais\n- Medidas mitigadoras específicas\n- Requisitos de eficiência energética e logística reversa",
            6: "**6. ESTIMATIVA DO VALOR DA CONTRATAÇÃO**\n- Metodologia de pesquisa conforme art. 23 da Lei 14.133/2021\n- Fontes consultadas (Painel de Preços, SICAF, mercado)\n- Custos totais considerados (aquisição + acessórios + ciclo de vida)\n- Memórias de cálculo detalhadas",
            7: "**7. DEFINIÇÃO DO OBJETO**\n- Descrição técnica precisa e completa\n- Especificações técnicas detalhadas\n- Alinhamento com necessidade identificada\n- Possibilidade de desdobramento em múltiplos Termos de Referência",
            8: "**8. JUSTIFICATIVA DE ESCOLHA DA SOLUÇÃO**\n- Fundamentação técnica, operacional e financeira\n- Demonstração de vantajosidade para a Administração\n- Comparação com alternativas analisadas\n- Alinhamento com interesse público",
            9: "**9. PREVISÃO DE CONTRATAÇÕES FUTURAS (PCA)**\n- Inserção no Plano de Contratações Anuais\n- Cronograma de contratações relacionadas\n- Interdependências com outras aquisições\n- Planejamento plurianual quando aplicável",
            10: "**10. ESTIMATIVA DE QUANTIDADES**\n- Memórias de cálculo fundamentadas\n- Análise de histórico de consumo\n- Consideração de economia de escala\n- Previsões de demanda futura",
            11: "**11. JUSTIFICATIVAS PARA PARCELAMENTO, AGRUPAMENTO E SUBCONTRATAÇÃO**\n- Análise de viabilidade técnica e econômica\n- Conformidade com Súmula 247 do TCU\n- Justificativa para divisibilidade ou indivisibilidade do objeto\n- Considerações sobre economia de escala",
            12: "**12. DEPENDÊNCIA DO CONTRATADO**\n- Análise de dependência tecnológica\n- Medidas para evitar aprisionamento tecnológico\n- Estratégias de migração e portabilidade\n- Garantias de continuidade dos serviços",
            13: "**13. TRANSIÇÃO CONTRATUAL**\n- Planejamento da transição entre contratos\n- Período de sobreposição necessário\n- Transferência de conhecimento e documentação\n- Continuidade dos serviços essenciais",
            14: "**14. ESTRATÉGIA DE IMPLANTAÇÃO**\n- Metodologia de implementação detalhada\n- Cronograma executivo com marcos principais\n- Recursos humanos e materiais necessários\n- Plano de gestão de mudanças",
            15: "**15. BENEFÍCIOS ESPERADOS**\n- Benefícios quantitativos e qualitativos\n- Indicadores de desempenho propostos\n- Beneficiários diretos e indiretos\n- Retorno sobre investimento esperado",
            16: "**16. DECLARAÇÃO DE ADEQUAÇÃO ORÇAMENTÁRIA**\n- Confirmação de disponibilidade orçamentária\n- Fonte de recursos identificada\n- Compatibilidade com planejamento orçamentário\n- Impacto nas metas fiscais",
            17: "**17. APROVAÇÃO DA AUTORIDADE COMPETENTE**\n- Identificação da autoridade competente\n- Fundamentação da competência decisória\n- Espaço para assinatura e data\n- Referência aos autos do processo administrativo"
        }
        
        # Construir seções para este grupo
        secoes_grupo = []
        for secao_num in secoes:
            secoes_grupo.append(secoes_definicoes[secao_num])
        
        secoes_texto = "\n\n".join(secoes_grupo)
        
        prompt_grupo = f"""
Elabore as seções {secoes[0]} a {secoes[-1]} de um Estudo Técnico Preliminar (ETP) em conformidade com a Lei 14.133/2021.

IMPORTANTE: Desenvolva COMPLETAMENTE cada seção solicitada com conteúdo técnico adequado e linguagem jurídico-administrativa formal.

## DADOS FORNECIDOS PELO USUÁRIO:

**ÓRGÃO RESPONSÁVEL:** {orgao_responsavel}

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

## SEÇÕES A DESENVOLVER:

{secoes_texto}

## DIRETRIZES:

1. **LINGUAGEM TÉCNICA FORMAL**: Utilize terminologia jurídico-administrativa adequada
2. **FUNDAMENTAÇÃO LEGAL**: Cite base legal pertinente (Lei 14.133/2021, decretos, instruções normativas)
3. **ESTRUTURAÇÃO PROFISSIONAL**: Numeração sequencial, parágrafos bem estruturados
4. **COMPLETUDE TÉCNICA**: Cada seção deve ser desenvolvida adequadamente (não apenas tópicos)
5. **CONFORMIDADE NORMATIVA**: Aderência total ao Manual TRT-2 e legislação vigente

IMPORTANTE: Para a seção 14 (ESTRATÉGIA DE IMPLANTAÇÃO), inclua OBRIGATORIAMENTE o cronograma detalhado baseado nas informações fornecidas pelo usuário.

Desenvolva APENAS as seções solicitadas ({secoes[0]} a {secoes[-1]}) com conteúdo completo e técnico.
        """
        
        return prompt_grupo
    
    def _validar_completude_etp(self, documento_gerado: str) -> Dict[str, Any]:
        """Valida se todas as seções foram geradas."""
        
        secoes_obrigatorias = [
            "1. DESCRIÇÃO DA NECESSIDADE",
            "2. HISTÓRICO DE CONTRATAÇÕES",
            "3. SOLUÇÕES EXISTENTES NO MERCADO",
            "4. LEVANTAMENTO E ANÁLISE DE RISCOS",
            "5. CRITÉRIOS DE SUSTENTABILIDADE",
            "6. ESTIMATIVA DO VALOR",
            "7. DEFINIÇÃO DO OBJETO",
            "8. JUSTIFICATIVA DE ESCOLHA",
            "9. PREVISÃO DE CONTRATAÇÕES FUTURAS",
            "10. ESTIMATIVA DE QUANTIDADES",
            "11. JUSTIFICATIVAS PARA PARCELAMENTO",
            "12. DEPENDÊNCIA DO CONTRATADO",
            "13. TRANSIÇÃO CONTRATUAL",
            "14. ESTRATÉGIA DE IMPLANTAÇÃO",  # ← Cronograma aqui
            "15. BENEFÍCIOS ESPERADOS",
            "16. DECLARAÇÃO DE ADEQUAÇÃO ORÇAMENTÁRIA",
            "17. APROVAÇÃO DA AUTORIDADE COMPETENTE"
        ]
        
        secoes_ausentes = []
        for secao in secoes_obrigatorias:
            # Verificar se a seção está presente (busca flexível)
            secao_numero = secao.split('.')[0]
            if not any(f"{secao_numero}." in linha for linha in documento_gerado.split('\n')):
                secoes_ausentes.append(secao)
        
        return {
            "completo": len(secoes_ausentes) == 0,
            "secoes_ausentes": secoes_ausentes,
            "percentual_completude": ((17 - len(secoes_ausentes)) / 17) * 100,
            "total_secoes": 17,
            "secoes_encontradas": 17 - len(secoes_ausentes)
        }


class RagChain:
    """Cadeia de RAG para responder perguntas sobre a Lei 14.133."""

    def __init__(self, retriever, provider: str = "openai"):
        """
        Inicializa a cadeia de RAG.

        Args:
            retriever: O retriever configurado para buscar documentos.
            provider (str): O provedor LLM a ser usado.
        """
        self.retriever = retriever
        self.provider = provider.lower()
        self.llm = self._get_llm()
        self.chain = self._create_rag_chain()

    def _get_llm(self):
        """Configura e retorna o modelo LLM com base no provedor."""
        # Reutiliza a lógica da classe EtpLlmGenerator
        generator = EtpLlmGenerator(provider=self.provider)
        return generator.llm

    def _create_rag_chain(self):
        """Cria a cadeia de RAG completa."""
        if not self.llm:
            return None

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
        1.  **Mantenha a Continuidade:** Considere todo o histórico da conversa para fornecer respostas coerentes e contextualizadas.
        2.  **Seja um Orientador:** Sintetize os pontos relevantes do contexto para fornecer recomendações práticas.
        3.  **Fundamente sua Resposta:** Baseie suas orientações nas informações do contexto e cite fontes quando possível.
        4.  **Seja Prático:** Traduza a linguagem técnica para orientações aplicáveis no dia a dia.
        5.  **Estruture a Resposta:** Organize de forma lógica para facilitar o entendimento.
        6.  **Referências Contextuais:** Quando apropriado, faça referência a pontos discutidos anteriormente na conversa.
        """
        
        prompt = ChatPromptTemplate.from_template(template)

        rag_chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        return rag_chain

    def _format_chat_history(self, chat_history: list) -> str:
        """
        Formata o histórico de chat para inclusão no prompt.
        
        Args:
            chat_history (list): Lista de mensagens no formato:
                               [{"role": "user", "content": "..."},
                                {"role": "assistant", "content": "..."}]
            
        Returns:
            str: Histórico formatado
        """
        if not chat_history:
            return "Nenhuma conversa anterior."
        
        # Pegar apenas as últimas 6 mensagens para não sobrecarregar o prompt
        recent_history = chat_history[-6:] if len(chat_history) > 6 else chat_history
        
        formatted_history = []
        for message in recent_history:
            role = "Usuário" if message["role"] == "user" else "Assistente"
            content = message["content"][:200] + "..." if len(message["content"]) > 200 else message["content"]
            formatted_history.append(f"{role}: {content}")
        
        return "\n".join(formatted_history)

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
        if not self.chain:
            return "Erro: A cadeia de RAG não foi inicializada corretamente. Verifique as configurações da API."
        
        # Formatar o histórico da conversa
        formatted_history = self._format_chat_history(chat_history)
        
        # Criar uma nova cadeia que inclui o histórico
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
        1.  **Mantenha a Continuidade:** Considere todo o histórico da conversa para fornecer respostas coerentes e contextualizadas.
        2.  **Seja um Orientador:** Sintetize os pontos relevantes do contexto para fornecer recomendações práticas.
        3.  **Fundamente sua Resposta:** Baseie suas orientações nas informações do contexto e cite fontes quando possível.
        4.  **Seja Prático:** Traduza a linguagem técnica para orientações aplicáveis no dia a dia.
        5.  **Estruture a Resposta:** Organize de forma lógica para facilitar o entendimento.
        6.  **Referências Contextuais:** Quando apropriado, faça referência a pontos discutidos anteriormente na conversa.
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        
        chain_with_history = (
            {"context": self.retriever, "chat_history": lambda x: formatted_history, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        return chain_with_history.invoke(question)

    def invoke(self, question: str) -> str:
        """
        Invoca a cadeia de RAG para obter uma resposta (sem histórico).

        Args:
            question (str): A pergunta do usuário.

        Returns:
            str: A resposta gerada pela IA.
        """
        if not self.chain:
            return "Erro: A cadeia de RAG não foi inicializada corretamente. Verifique as configurações da API."
        
        return self.chain.invoke(question)


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
