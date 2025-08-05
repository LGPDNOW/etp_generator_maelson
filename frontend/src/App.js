import React, { useState, useEffect } from 'react';
import { ConfigProvider, Layout, message, Spin } from 'antd';
import ptBR from 'antd/locale/pt_BR';
import { QueryClient, QueryClientProvider } from 'react-query';
import styled from 'styled-components';

// Componentes
import Header from './components/Layout/Header';
import Sidebar from './components/Layout/Sidebar';
import Dashboard from './components/Dashboard/Dashboard';
import EtpForm from './components/ETP/EtpForm';
import EtpEditor from './components/ETP/EtpEditor';
import RagAssistant from './components/RAG/RagAssistant';
import ConfigPage from './components/Config/ConfigPage';

// Serviços
import { apiService } from './services/apiService';

// Estilos
import './App.css';

const { Content } = Layout;

// Styled Components
const AppContainer = styled.div`
  min-height: 100vh;
  background: #f0f2f5;
`;

const LoadingContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  flex-direction: column;
  gap: 16px;
  background: #f0f2f5;
`;

const ContentContainer = styled(Content)`
  padding: 24px;
  margin: 0;
  min-height: calc(100vh - 64px);
  background: #f0f2f5;
`;

const MainLayout = styled(Layout)`
  min-height: 100vh;
`;

// Query Client para React Query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function App() {
  const [loading, setLoading] = useState(true);
  const [apiStatus, setApiStatus] = useState(null);
  const [collapsed, setCollapsed] = useState(false);
  const [currentPage, setCurrentPage] = useState('home');

  // Verificar status da API ao carregar
  useEffect(() => {
    checkApiStatus();
  }, []);

  const checkApiStatus = async () => {
    try {
      const response = await apiService.verificarStatus();
      setApiStatus(response);
      
      // Verificar se pelo menos uma API está configurada
      if (!response.openai_api && !response.anthropic_api) {
        message.warning('Configure pelo menos uma API (OpenAI ou Anthropic) para usar todas as funcionalidades');
      }
    } catch (error) {
      console.error('Erro ao verificar status da API:', error);
      message.error('Erro ao conectar com o backend. Verifique se a API está rodando na porta 8000.');
      
      // Definir status padrão em caso de erro
      setApiStatus({
        openai_api: false,
        anthropic_api: false,
        rag_assistant: false,
        assistente_etp: false
      });
    } finally {
      setLoading(false);
    }
  };

  const handleMenuClick = (key) => {
    setCurrentPage(key);
  };

  const handleConfigClick = () => {
    setCurrentPage('config');
  };

  const handleStatusUpdate = () => {
    checkApiStatus();
  };

  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'home':
        return (
          <Dashboard 
            apiStatus={apiStatus} 
            onNavigate={handleMenuClick}
          />
        );
      case 'etp-form':
        return (
          <EtpForm 
            apiStatus={apiStatus}
            onGenerate={(etp) => {
              console.log('ETP gerado:', etp);
              message.success('ETP gerado com sucesso!');
              
              // Atualizar estatísticas
              const stats = JSON.parse(localStorage.getItem('dashboard_stats') || '{"etpsCreated": 0, "ragQueries": 0, "assistantUsage": 0}');
              stats.etpsCreated += 1;
              localStorage.setItem('dashboard_stats', JSON.stringify(stats));
            }}
          />
        );
      case 'etp-editor':
        return <EtpEditor apiStatus={apiStatus} />;
      case 'rag-assistant':
        return <RagAssistant apiStatus={apiStatus} />;
      case 'config':
        return (
          <ConfigPage 
            apiStatus={apiStatus} 
            onStatusUpdate={handleStatusUpdate}
          />
        );
      default:
        return (
          <Dashboard 
            apiStatus={apiStatus} 
            onNavigate={handleMenuClick}
          />
        );
    }
  };

  if (loading) {
    return (
      <LoadingContainer>
        <Spin size="large" />
        <div style={{ marginTop: 16, fontSize: '16px', color: '#666' }}>
          Carregando ETP Generator...
        </div>
        <div style={{ fontSize: '12px', color: '#999' }}>
          Verificando conexão com o backend
        </div>
      </LoadingContainer>
    );
  }

  return (
    <QueryClientProvider client={queryClient}>
      <ConfigProvider locale={ptBR}>
        <AppContainer>
          <MainLayout>
            <Header 
              apiStatus={apiStatus} 
              onConfigClick={handleConfigClick}
            />
            
            <Layout>
              <Sidebar
                collapsed={collapsed}
                selectedKey={currentPage}
                onMenuClick={handleMenuClick}
                apiStatus={apiStatus}
              />
              
              <ContentContainer>
                {renderCurrentPage()}
              </ContentContainer>
            </Layout>
          </MainLayout>
        </AppContainer>
      </ConfigProvider>
    </QueryClientProvider>
  );
}

export default App;