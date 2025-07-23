# processador_documentos.py
import os
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configura a chave da API da OpenAI
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

@st.cache_resource
def criar_indice_vetorial(caminhos_pdf: list[str]):
    """
    Cria um índice vetorial a partir de uma lista de arquivos PDF.

    Esta função carrega múltiplos documentos PDF, os combina, divide o texto
    em chunks, gera embeddings para cada chunk e os armazena em um índice FAISS.
    O resultado é cacheado para evitar reprocessamento.

    Args:
        caminhos_pdf (list[str]): Uma lista de caminhos para os arquivos PDF.

    Returns:
        FAISS: O índice vetorial pronto para busca.
    """
    todos_documentos = []
    for caminho_pdf in caminhos_pdf:
        if not os.path.exists(caminho_pdf):
            st.warning(f"Arquivo PDF não encontrado em: {caminho_pdf}. Pulando.")
            continue
        try:
            loader = PyPDFLoader(caminho_pdf)
            documentos = loader.load()
            todos_documentos.extend(documentos)
        except Exception as e:
            st.error(f"Erro ao carregar o arquivo {caminho_pdf}: {e}")

    if not todos_documentos:
        st.error("Nenhum documento PDF pôde ser carregado. Verifique os arquivos.")
        return None

    try:
        # 2. Dividir o texto em chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_documents(todos_documentos)

        # 3. Gerar embeddings e criar o índice FAISS
        embeddings = OpenAIEmbeddings()
        indice_vetorial = FAISS.from_documents(chunks, embeddings)

        st.success("Índice vetorial da base de conhecimento criado com sucesso!")
        return indice_vetorial

    except Exception as e:
        st.error(f"Erro ao processar os PDFs e criar o índice: {e}")
        return None

def obter_retriever(indice_vetorial):
    """
    Cria um retriever a partir de um índice vetorial.

    Args:
        indice_vetorial (FAISS): O índice vetorial.

    Returns:
        retriever: Um objeto retriever configurado para busca.
    """

    if indice_vetorial:
        return indice_vetorial.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5} # Retorna os 5 chunks mais relevantes
        )
    return None