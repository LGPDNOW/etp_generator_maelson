import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Row, 
  Col, 
  Statistic, 
  Typography, 
  Space, 
  Button, 
  Alert,
  List,
  Tag,
  Progress,
  Divider
} from 'antd';
import { 
  FileTextOutlined, 
  RobotOutlined, 
  QuestionCircleOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  ApiOutlined,
  TrophyOutlined,
  RocketOutlined
} from '@ant-design/icons';
import styled from 'styled-components';

const { Title, Text, Paragraph } = Typography;

// Styled Components
const DashboardContainer = styled.div`
  .dashboard-card {
    transition: all 0.3s;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
  }
  
  .feature-card {
    text-align: center;
    padding: 24px;
    
    .feature-icon {
      font-size: 48px;
      margin-bottom: 16px;
      display: block;
    }
  }
  
  .status-overview {
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    border: 1px solid #bae6fd;
  }
`;

const WelcomeSection = styled.div`
  background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%);
  color: white;
  padding: 32px;
  border-radius: 12px;
  margin-bottom: 24px;
  text-align: center;
  
  .welcome-title {
    color: white;
    margin-bottom: 8px;
  }
  
  .welcome-subtitle {
    color: rgba(255, 255, 255, 0.8);
    font-size: 16px;
  }
`;

const Dashboard = ({ apiStatus, onNavigate }) => {
  const [stats, setStats] = useState({
    etpsCreated: 0,
    ragQueries: 0,
    assistantUsage: 0
  });

  // Carregar estatísticas do localStorage
  useEffect(() => {
    const savedStats = localStorage.getItem('dashboard_stats');
    if (savedStats) {
      try {
        setStats(JSON.parse(savedStats));
      } catch (error) {
        console.error('Erro ao carregar estatísticas:', error);
      }
    }
  }, []);

  const getSystemHealth = () => {
    if (!apiStatus) return 0;
    
    const services = ['openai_api', 'anthropic_api', 'rag_assistant', 'assistente_etp'];
    const activeServices = services.filter(service => apiStatus[service]).length;
    
    return Math.round((activeServices / services.length) * 100);
  };

  const getRecentActivity = () => {
    // Simular atividade recente (em um sistema real, isso viria da API)
    return [
      { action: 'ETP gerado', time: '2 horas atrás', type: 'success' },
      { action: 'Consulta RAG realizada', time: '3 horas atrás', type: 'info' },
      { action: 'Campo analisado pelo assistente', time: '5 horas atrás', type: 'processing' },
      { action: 'Configuração atualizada', time: '1 dia atrás', type: 'default' }
    ];
  };

  const features = [
    {
      key: 'etp-form',
      title: 'Formulário ETP',
      description: 'Crie ETPs com assistente inteligente',
      icon: '📝',
      status: apiStatus?.assistente_etp ? 'active' : 'inactive',
      action: () => onNavigate('etp-form')
    },
    {
      key: 'etp-editor',
      title: 'Editor Rico',
      description: 'Editor WYSIWYG para documentos',
      icon: '✏️',
      status: 'active',
      action: () => onNavigate('etp-editor')
    },
    {
      key: 'rag-assistant',
      title: 'Assistente Lei 14.133',
      description: 'Consulte a documentação oficial',
      icon: '🤖',
      status: apiStatus?.rag_assistant ? 'active' : 'inactive',
      action: () => onNavigate('rag-assistant')
    },
    {
      key: 'config',
      title: 'Configurações',
      description: 'Configure APIs e sistema',
      icon: '⚙️',
      status: 'active',
      action: () => onNavigate('config')
    }
  ];

  return (
    <DashboardContainer>
      <WelcomeSection>
        <Title level={2} className="welcome-title">
          🎯 Bem-vindo ao ETP Generator
        </Title>
        <Text className="welcome-subtitle">
          Sistema Integrado de Geração de Documentos com Inteligência Artificial
        </Text>
      </WelcomeSection>

      {/* Status do Sistema */}
      <Card className="dashboard-card status-overview" style={{ marginBottom: 24 }}>
        <Row gutter={[24, 24]} align="middle">
          <Col span={6}>
            <Statistic
              title="Saúde do Sistema"
              value={getSystemHealth()}
              suffix="%"
              valueStyle={{ color: getSystemHealth() > 75 ? '#3f8600' : '#cf1322' }}
              prefix={<TrophyOutlined />}
            />
            <Progress 
              percent={getSystemHealth()} 
              size="small" 
              status={getSystemHealth() > 75 ? 'success' : 'exception'}
              showInfo={false}
            />
          </Col>
          
          <Col span={6}>
            <Statistic
              title="ETPs Criados"
              value={stats.etpsCreated}
              prefix={<FileTextOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Col>
          
          <Col span={6}>
            <Statistic
              title="Consultas RAG"
              value={stats.ragQueries}
              prefix={<QuestionCircleOutlined />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Col>
          
          <Col span={6}>
            <Statistic
              title="Análises IA"
              value={stats.assistantUsage}
              prefix={<RobotOutlined />}
              valueStyle={{ color: '#722ed1' }}
            />
          </Col>
        </Row>
      </Card>

      <Row gutter={[24, 24]}>
        {/* Funcionalidades Principais */}
        <Col span={16}>
          <Card title="🚀 Funcionalidades Principais" className="dashboard-card">
            <Row gutter={[16, 16]}>
              {features.map(feature => (
                <Col span={12} key={feature.key}>
                  <Card 
                    size="small" 
                    className="feature-card"
                    hoverable
                    onClick={feature.action}
                    style={{ 
                      border: feature.status === 'active' ? '2px solid #52c41a' : '1px solid #d9d9d9',
                      opacity: feature.status === 'active' ? 1 : 0.7
                    }}
                  >
                    <div className="feature-icon">{feature.icon}</div>
                    <Title level={5} style={{ margin: '8px 0' }}>
                      {feature.title}
                    </Title>
                    <Text type="secondary">{feature.description}</Text>
                    <div style={{ marginTop: 12 }}>
                      <Tag color={feature.status === 'active' ? 'success' : 'warning'}>
                        {feature.status === 'active' ? 'Disponível' : 'Configure APIs'}
                      </Tag>
                    </div>
                  </Card>
                </Col>
              ))}
            </Row>
          </Card>
        </Col>

        {/* Atividade Recente */}
        <Col span={8}>
          <Card title="📊 Atividade Recente" className="dashboard-card">
            <List
              size="small"
              dataSource={getRecentActivity()}
              renderItem={item => (
                <List.Item>
                  <Space>
                    <CheckCircleOutlined 
                      style={{ 
                        color: item.type === 'success' ? '#52c41a' : 
                               item.type === 'info' ? '#1890ff' : '#8c8c8c' 
                      }} 
                    />
                    <div>
                      <Text>{item.action}</Text>
                      <br />
                      <Text type="secondary" style={{ fontSize: '12px' }}>
                        <ClockCircleOutlined /> {item.time}
                      </Text>
                    </div>
                  </Space>
                </List.Item>
              )}
            />
          </Card>
        </Col>
      </Row>

      {/* Status dos Serviços */}
      <Row gutter={[24, 24]} style={{ marginTop: 24 }}>
        <Col span={24}>
          <Card title="🔧 Status dos Serviços" className="dashboard-card">
            <Row gutter={[16, 16]}>
              <Col span={6}>
                <Card size="small" style={{ textAlign: 'center' }}>
                  <ApiOutlined style={{ fontSize: '24px', color: apiStatus?.openai_api ? '#52c41a' : '#8c8c8c' }} />
                  <div style={{ marginTop: 8 }}>
                    <Text strong>OpenAI API</Text>
                    <br />
                    <Tag color={apiStatus?.openai_api ? 'success' : 'default'}>
                      {apiStatus?.openai_api ? 'Ativo' : 'Inativo'}
                    </Tag>
                  </div>
                </Card>
              </Col>
              
              <Col span={6}>
                <Card size="small" style={{ textAlign: 'center' }}>
                  <RobotOutlined style={{ fontSize: '24px', color: apiStatus?.anthropic_api ? '#52c41a' : '#8c8c8c' }} />
                  <div style={{ marginTop: 8 }}>
                    <Text strong>Anthropic API</Text>
                    <br />
                    <Tag color={apiStatus?.anthropic_api ? 'success' : 'default'}>
                      {apiStatus?.anthropic_api ? 'Ativo' : 'Inativo'}
                    </Tag>
                  </div>
                </Card>
              </Col>
              
              <Col span={6}>
                <Card size="small" style={{ textAlign: 'center' }}>
                  <QuestionCircleOutlined style={{ fontSize: '24px', color: apiStatus?.rag_assistant ? '#52c41a' : '#8c8c8c' }} />
                  <div style={{ marginTop: 8 }}>
                    <Text strong>RAG Assistant</Text>
                    <br />
                    <Tag color={apiStatus?.rag_assistant ? 'success' : 'default'}>
                      {apiStatus?.rag_assistant ? 'Ativo' : 'Inativo'}
                    </Tag>
                  </div>
                </Card>
              </Col>
              
              <Col span={6}>
                <Card size="small" style={{ textAlign: 'center' }}>
                  <FileTextOutlined style={{ fontSize: '24px', color: apiStatus?.assistente_etp ? '#52c41a' : '#8c8c8c' }} />
                  <div style={{ marginTop: 8 }}>
                    <Text strong>ETP Assistant</Text>
                    <br />
                    <Tag color={apiStatus?.assistente_etp ? 'success' : 'default'}>
                      {apiStatus?.assistente_etp ? 'Ativo' : 'Inativo'}
                    </Tag>
                  </div>
                </Card>
              </Col>
            </Row>
          </Card>
        </Col>
      </Row>

      {/* Alertas e Dicas */}
      {(!apiStatus?.openai_api && !apiStatus?.anthropic_api) && (
        <Alert
          message="⚠️ Configure as APIs"
          description="Para usar todas as funcionalidades, configure pelo menos uma API (OpenAI ou Anthropic) na página de configurações."
          type="warning"
          showIcon
          style={{ marginTop: 24 }}
          action={
            <Button size="small" onClick={() => onNavigate('config')}>
              Configurar Agora
            </Button>
          }
        />
      )}
    </DashboardContainer>
  );
};

export default Dashboard;