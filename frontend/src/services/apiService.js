import axios from 'axios';

// Configuração base do Axios
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para tratamento de erros
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error);
    
    if (error.response) {
      // Erro do servidor
      throw new Error(error.response.data.detail || 'Erro no servidor');
    } else if (error.request) {
      // Erro de rede
      throw new Error('Erro de conexão com o servidor');
    } else {
      // Erro de configuração
      throw new Error('Erro na requisição');
    }
  }
);

export const apiService = {
  // ===== CONFIGURAÇÃO =====
  
  /**
   * Verifica o status dos serviços
   */
  async getStatus() {
    return await apiClient.get('/api/status');
  },

  async verificarStatus() {
    return await apiClient.get('/api/status');
  },

  /**
   * Configura o provedor de IA
   */
  async configurarIA(provider, apiKey) {
    return await apiClient.post('/api/configurar-ia', {
      provider,
      api_key: apiKey
    });
  },

  /**
   * Configura o sistema RAG
   */
  async configurarRAG(caminhosPdf = null, provider = 'openai') {
    return await apiClient.post('/api/configurar-rag', {
      caminhos_pdf: caminhosPdf,
      provider
    });
  },

  // ===== ETP =====

  /**
   * Gera um ETP completo
   */
  async gerarETP(dadosEtp) {
    return await apiClient.post('/api/gerar-etp', dadosEtp);
  },

  /**
   * Valida a consistência geral do ETP
   */
  async validarConsistencia(dadosEtp) {
    return await apiClient.post('/api/validar-consistencia', dadosEtp);
  },

  // ===== ASSISTENTE INTELIGENTE =====

  /**
   * Analisa um campo específico
   */
  async analisarCampo(nomeCampo, conteudoAtual, contextoAnterior = {}) {
    return await apiClient.post('/api/analisar-campo', {
      nome_campo: nomeCampo,
      conteudo_atual: conteudoAtual,
      contexto_anterior: contextoAnterior
    });
  },

  /**
   * Melhora um texto
   */
  async melhorarTexto(texto, tipoMelhoria = 'geral') {
    return await apiClient.post('/api/melhorar-texto', {
      texto,
      tipo_melhoria: tipoMelhoria
    });
  },

  /**
   * Gera exemplo para um campo
   */
  async gerarExemplo(nomeCampo, contextoAnterior = {}) {
    return await apiClient.post('/api/gerar-exemplo', {
      nome_campo: nomeCampo,
      contexto_anterior: contextoAnterior
    });
  },

  /**
   * Obtém lista de campos críticos
   */
  async getCamposCriticos() {
    return await apiClient.get('/api/campos-criticos');
  },

  /**
   * Obtém mapeamento de seções TRT-2
   */
  async getSecoesTRT2() {
    return await apiClient.get('/api/secoes-trt2');
  },

  // ===== RAG (Lei 14.133) =====

  /**
   * Faz uma pergunta ao sistema RAG
   */
  async perguntarRAG(pergunta, historico = []) {
    return await apiClient.post('/api/perguntar-rag', {
      pergunta,
      historico
    });
  },

  async consultarRag(pergunta, historico = []) {
    return await apiClient.post('/api/perguntar-rag', {
      pergunta,
      historico
    });
  },

  // ===== UTILITÁRIOS =====

  /**
   * Health check da API
   */
  async healthCheck() {
    return await apiClient.get('/');
  },

  // Configurações
  async obterConfig() {
    return await apiClient.get('/config');
  },

  async salvarConfig(config) {
    return await apiClient.post('/config', config);
  },

  async testarConexao(config) {
    return await apiClient.post('/testar-conexao', config);
  }
};

// Hooks personalizados para React Query
export const apiHooks = {
  // Status da API
  useApiStatus: () => ({
    queryKey: ['api-status'],
    queryFn: apiService.getStatus,
    refetchInterval: 30000, // Refetch a cada 30 segundos
  }),

  // Campos críticos
  useCamposCriticos: () => ({
    queryKey: ['campos-criticos'],
    queryFn: apiService.getCamposCriticos,
    staleTime: 5 * 60 * 1000, // 5 minutos
  }),

  // Seções TRT-2
  useSecoesTRT2: () => ({
    queryKey: ['secoes-trt2'],
    queryFn: apiService.getSecoesTRT2,
    staleTime: 5 * 60 * 1000, // 5 minutos
  }),
};

// Tipos de melhoria de texto disponíveis
export const TIPOS_MELHORIA = {
  GRAMATICA: 'gramatica',
  TECNICO: 'tecnico',
  GERAL: 'geral'
};

// Provedores de IA disponíveis
export const PROVEDORES_IA = {
  OPENAI: 'openai',
  ANTHROPIC: 'anthropic'
};

// Status de qualidade do assistente
export const STATUS_QUALIDADE = {
  EXCELENTE: 'excelente',
  BOA: 'boa',
  REGULAR: 'regular',
  PRECISA_MELHORAR: 'precisa_melhorar',
  ERRO: 'erro'
};

// Cores para status de qualidade
export const CORES_QUALIDADE = {
  [STATUS_QUALIDADE.EXCELENTE]: '#52c41a',
  [STATUS_QUALIDADE.BOA]: '#faad14',
  [STATUS_QUALIDADE.REGULAR]: '#fa8c16',
  [STATUS_QUALIDADE.PRECISA_MELHORAR]: '#f5222d',
  [STATUS_QUALIDADE.ERRO]: '#ff4d4f'
};

// Ícones para status de qualidade
export const ICONES_QUALIDADE = {
  [STATUS_QUALIDADE.EXCELENTE]: '🟢',
  [STATUS_QUALIDADE.BOA]: '🟡',
  [STATUS_QUALIDADE.REGULAR]: '🟠',
  [STATUS_QUALIDADE.PRECISA_MELHORAR]: '🔴',
  [STATUS_QUALIDADE.ERRO]: '❌'
};

export default apiService;