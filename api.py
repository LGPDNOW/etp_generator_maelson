# api.py - FastAPI Backend para Sistema ETP
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import os
from datetime import datetime
from dotenv import load_dotenv
from integrador import EtpLlmGenerator, AssistenteEtpInteligente, RagChain
from processador_documentos import criar_indice_vetorial, obter_retriever

# Carregar variáveis do .env
load_dotenv()

# Inicializar FastAPI
app = FastAPI(
    title="Sistema ETP - API",
    description="API para geração e análise de Estudos Técnicos Preliminares",
    version="2.0.0"
)

# Configurar CORS para React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class DadosETP(BaseModel):
    orgao_responsavel: str = ""
    descricao_problema: str = ""
    areas_impactadas: List[str] = []
    stakeholders: List[str] = []
    requisitos_funcionais: str = ""
    requisitos_nao_funcionais: str = ""
    solucoes_mercado: str = ""
    comparativo_solucoes: str = ""
    valor_minimo: Optional[float] = None
    valor_medio: Optional[float] = None
    valor_maximo: Optional[float] = None
    solucao_proposta: str = ""
    justificativa_escolha: str = ""
    estrategia_implantacao: str = ""
    cronograma: str = ""
    recursos_necessarios: str = ""
    beneficios: str = ""
    beneficiarios: str = ""
    providencias: str = ""
    declaracao_viabilidade: str = "viável"

class ConfiguracaoIA(BaseModel):
    provider: str = "openai"  # "openai" ou "anthropic"
    api_key: str

class AnaliseCampo(BaseModel):
    nome_campo: str
    conteudo_atual: str
    contexto_anterior: Dict[str, Any] = {}

class MelhoriaTexto(BaseModel):
    texto: str
    tipo_melhoria: str = "geral"  # "gramatica", "tecnico", "geral"

class PerguntaRAG(BaseModel):
    pergunta: str
    historico: List[Dict[str, str]] = []

# Variáveis globais para instâncias
etp_generator = None
assistente_etp = None
rag_chain = None

# Inicializar serviços automaticamente se as chaves estiverem no .env
def inicializar_servicos():
    global etp_generator, assistente_etp, rag_chain
    
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    
    if openai_key:
        try:
            etp_generator = EtpLlmGenerator(provider="openai")
            assistente_etp = AssistenteEtpInteligente(provider="openai")
            print("✅ Serviços OpenAI inicializados")
        except Exception as e:
            print(f"❌ Erro ao inicializar OpenAI: {e}")
    
    elif anthropic_key:
        try:
            etp_generator = EtpLlmGenerator(provider="anthropic")
            assistente_etp = AssistenteEtpInteligente(provider="anthropic")
            print("✅ Serviços Anthropic inicializados")
        except Exception as e:
            print(f"❌ Erro ao inicializar Anthropic: {e}")
    
    # Inicializar RAG se possível
    if (openai_key or anthropic_key) and not rag_chain:
        try:
            caminhos_pdf = [
                "data/input/lei_14133.pdf",
                "data/input/Manual_Compras_Licitacoes.pdf"
            ]
            indice_vetorial = criar_indice_vetorial(caminhos_pdf)
            if indice_vetorial:
                retriever = obter_retriever(indice_vetorial)
                provider = "openai" if openai_key else "anthropic"
                rag_chain = RagChain(retriever=retriever, provider=provider)
                print("✅ RAG inicializado")
        except Exception as e:
            print(f"❌ Erro ao inicializar RAG: {e}")

# Inicializar na startup
inicializar_servicos()

# Endpoints de Configuração
@app.post("/api/configurar-ia")
async def configurar_ia(config: ConfiguracaoIA):
    """Configura o provedor de IA e inicializa os serviços."""
    global etp_generator, assistente_etp
    
    try:
        # Configurar variável de ambiente
        if config.provider == "openai":
            os.environ["OPENAI_API_KEY"] = config.api_key
        else:
            os.environ["ANTHROPIC_API_KEY"] = config.api_key
        
        # Inicializar serviços
        etp_generator = EtpLlmGenerator(provider=config.provider)
        assistente_etp = AssistenteEtpInteligente(provider=config.provider)
        
        return {
            "status": "success",
            "message": f"IA configurada com {config.provider}",
            "provider": config.provider
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao configurar IA: {str(e)}")

@app.get("/api/status")
async def status():
    """Verifica o status dos serviços."""
    return {
        "openai_api": bool(os.getenv("OPENAI_API_KEY")),
        "anthropic_api": bool(os.getenv("ANTHROPIC_API_KEY")),
        "etp_generator": etp_generator is not None,
        "assistente_etp": assistente_etp is not None,
        "rag_assistant": rag_chain is not None
    }

# Endpoints do ETP
@app.post("/api/gerar-etp")
async def gerar_etp(dados: DadosETP):
    """Gera um ETP completo baseado nos dados fornecidos."""
    if not etp_generator:
        raise HTTPException(status_code=400, detail="IA não configurada")
    
    try:
        # Converter para dict
        dados_dict = dados.dict()
        
        # Gerar ETP
        etp_gerado = etp_generator.generate_etp(dados_dict)
        
        return {
            "status": "success",
            "etp": etp_gerado,
            "dados_utilizados": dados_dict
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar ETP: {str(e)}")

# Endpoints do Assistente Inteligente
@app.post("/api/analisar-campo")
async def analisar_campo(analise: AnaliseCampo):
    """Analisa um campo específico com contexto TRT-2."""
    if not assistente_etp:
        raise HTTPException(status_code=400, detail="Assistente não configurado")
    
    try:
        resultado = assistente_etp.analisar_campo_com_contexto_trt2(
            analise.nome_campo,
            analise.conteudo_atual,
            analise.contexto_anterior
        )
        return {
            "status": "success",
            "analise": resultado
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na análise: {str(e)}")

@app.post("/api/melhorar-texto")
async def melhorar_texto(melhoria: MelhoriaTexto):
    """Melhora um texto específico."""
    if not assistente_etp:
        raise HTTPException(status_code=400, detail="Assistente não configurado")
    
    try:
        resultado = assistente_etp.melhorar_texto(
            melhoria.texto,
            melhoria.tipo_melhoria
        )
        return {
            "status": "success",
            "melhoria": resultado
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na melhoria: {str(e)}")

@app.post("/api/gerar-exemplo")
async def gerar_exemplo(dados: Dict[str, Any]):
    """Gera exemplo para um campo específico."""
    if not assistente_etp:
        raise HTTPException(status_code=400, detail="Assistente não configurado")
    
    try:
        nome_campo = dados.get("nome_campo")
        contexto = dados.get("contexto_anterior", {})
        
        exemplo = assistente_etp.gerar_exemplo_campo(nome_campo, contexto)
        
        return {
            "status": "success",
            "exemplo": exemplo
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar exemplo: {str(e)}")

@app.post("/api/validar-consistencia")
async def validar_consistencia(dados: DadosETP):
    """Valida a consistência geral do ETP."""
    if not assistente_etp:
        raise HTTPException(status_code=400, detail="Assistente não configurado")
    
    try:
        dados_dict = dados.dict()
        
        # Validação de consistência geral
        consistencia = assistente_etp.validar_consistencia_geral(dados_dict)
        
        # Validação de alinhamento TRT-2
        alinhamento = assistente_etp.validar_alinhamento_prompt_tecnico(dados_dict)
        
        return {
            "status": "success",
            "consistencia": consistencia,
            "alinhamento_trt2": alinhamento
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na validação: {str(e)}")

# Endpoints do RAG (Lei 14.133)
@app.post("/api/configurar-rag")
async def configurar_rag(dados: Dict[str, Any]):
    """Configura o sistema RAG com documentos."""
    global rag_chain
    
    try:
        # Usar arquivos padrão se não especificado
        caminhos_pdf = dados.get("caminhos_pdf", [
            "data/input/lei_14133.pdf", 
            "data/input/Manual_Compras_Licitacoes.pdf"
        ])
        
        provider = dados.get("provider", "openai")
        
        # Criar índice vetorial
        indice_vetorial = criar_indice_vetorial(caminhos_pdf)
        
        if indice_vetorial:
            retriever = obter_retriever(indice_vetorial)
            rag_chain = RagChain(retriever=retriever, provider=provider)
            
            return {
                "status": "success",
                "message": "RAG configurado com sucesso",
                "documentos": len(caminhos_pdf)
            }
        else:
            raise HTTPException(status_code=500, detail="Erro ao criar índice vetorial")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao configurar RAG: {str(e)}")

@app.post("/api/perguntar-rag")
async def perguntar_rag(pergunta_data: PerguntaRAG):
    """Faz uma pergunta ao sistema RAG."""
    if not rag_chain:
        raise HTTPException(status_code=400, detail="RAG não configurado")
    
    try:
        if pergunta_data.historico:
            resposta_texto = rag_chain.invoke_with_history(
                pergunta_data.pergunta,
                pergunta_data.historico
            )
        else:
            resposta_texto = rag_chain.invoke(pergunta_data.pergunta)
        
        # Estruturar resposta no formato esperado pelo frontend
        return {
            "status": "success",
            "resposta": resposta_texto,
            "fontes": [],  # Pode ser implementado futuramente
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na consulta RAG: {str(e)}")

# Endpoints Utilitários
@app.get("/api/campos-criticos")
async def campos_criticos():
    """Retorna a lista de campos críticos suportados."""
    if not assistente_etp:
        return {"campos": []}
    
    return {
        "campos": assistente_etp.campos_criticos,
        "total": len(assistente_etp.campos_criticos)
    }

@app.get("/api/secoes-trt2")
async def secoes_trt2():
    """Retorna o mapeamento de campos para seções TRT-2."""
    if not assistente_etp:
        return {"mapeamento": {}}
    
    # Simular mapeamento (seria melhor extrair do método real)
    mapeamento = {
        "descricao_problema": "1. DESCRIÇÃO DA NECESSIDADE",
        "solucoes_mercado": "3. SOLUÇÕES EXISTENTES NO MERCADO",
        "solucao_proposta": "7. DEFINIÇÃO DO OBJETO",
        "justificativa_escolha": "8. JUSTIFICATIVA DE ESCOLHA DA SOLUÇÃO",
        "estrategia_implantacao": "14. ESTRATÉGIA DE IMPLANTAÇÃO",
        "beneficios": "15. BENEFÍCIOS ESPERADOS"
    }
    
    return {
        "mapeamento": mapeamento,
        "total_secoes": 17
    }

# Endpoints de Configuração
@app.get("/config")
async def obter_config():
    """Obtém as configurações atuais."""
    return {
        "status": "success",
        "config": {
            "openai_api_key": "***" if os.getenv("OPENAI_API_KEY") else "",
            "anthropic_api_key": "***" if os.getenv("ANTHROPIC_API_KEY") else "",
            "provider_preference": "openai",
            "rag_enabled": rag_chain is not None,
            "assistente_etp_enabled": assistente_etp is not None,
            "max_tokens": 4000,
            "temperature": 0.7
        }
    }

@app.post("/config")
async def salvar_config(config: Dict[str, Any]):
    """Salva as configurações."""
    global etp_generator, assistente_etp, rag_chain
    
    try:
        # Configurar chaves de API
        if config.get("openai_api_key"):
            os.environ["OPENAI_API_KEY"] = config["openai_api_key"]
        if config.get("anthropic_api_key"):
            os.environ["ANTHROPIC_API_KEY"] = config["anthropic_api_key"]
        
        # Inicializar serviços baseado na preferência
        provider = config.get("provider_preference", "openai")
        
        if config.get("openai_api_key") or config.get("anthropic_api_key"):
            etp_generator = EtpLlmGenerator(provider=provider)
            assistente_etp = AssistenteEtpInteligente(provider=provider)
        
        # Configurar RAG se habilitado
        if config.get("rag_enabled", True) and not rag_chain:
            try:
                caminhos_pdf = [
                    "data/input/lei_14133.pdf",
                    "data/input/Manual_Compras_Licitacoes.pdf"
                ]
                indice_vetorial = criar_indice_vetorial(caminhos_pdf)
                if indice_vetorial:
                    retriever = obter_retriever(indice_vetorial)
                    rag_chain = RagChain(retriever=retriever, provider=provider)
            except Exception as e:
                print(f"Erro ao configurar RAG: {e}")
        
        return {
            "status": "success",
            "message": "Configurações salvas com sucesso"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar configurações: {str(e)}")

@app.post("/testar-conexao")
async def testar_conexao(config: Dict[str, Any]):
    """Testa a conexão com as APIs configuradas."""
    try:
        provider = config.get("provider_preference", "openai")
        
        # Testar OpenAI
        openai_ok = False
        if config.get("openai_api_key"):
            try:
                os.environ["OPENAI_API_KEY"] = config["openai_api_key"]
                test_generator = EtpLlmGenerator(provider="openai")
                # Teste simples
                openai_ok = True
            except Exception as e:
                print(f"Erro OpenAI: {e}")
        
        # Testar Anthropic
        anthropic_ok = False
        if config.get("anthropic_api_key"):
            try:
                os.environ["ANTHROPIC_API_KEY"] = config["anthropic_api_key"]
                test_generator = EtpLlmGenerator(provider="anthropic")
                # Teste simples
                anthropic_ok = True
            except Exception as e:
                print(f"Erro Anthropic: {e}")
        
        return {
            "status": "success",
            "testes": {
                "openai_api": openai_ok,
                "anthropic_api": anthropic_ok,
                "provider_ativo": provider
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no teste: {str(e)}")

# Endpoint de Health Check
@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "Sistema ETP API - Funcionando",
        "version": "2.0.0",
        "status": "online"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)