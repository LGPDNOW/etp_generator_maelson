import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Form, 
  Input, 
  Button, 
  Space, 
  Typography, 
  Row, 
  Col, 
  message,
  Alert,
  Divider,
  Switch,
  Select,
  Tooltip,
  Badge,
  Spin
} from 'antd';
import { 
  SettingOutlined, 
  SaveOutlined, 
  ReloadOutlined,
  CheckCircleOutlined,
  ExclamationCircleOutlined,
  EyeInvisibleOutlined,
  EyeTwoTone,
  ApiOutlined,
  RobotOutlined,
  BookOutlined
} from '@ant-design/icons';
import styled from 'styled-components';
import { apiService } from '../../services/apiService';

const { Title, Text, Paragraph } = Typography;
const { Password } = Input;
const { Option } = Select;

// Styled Components
const ConfigContainer = styled.div`
  .config-section {
    margin-bottom: 24px;
  }
  
  .status-indicator {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    
    &.active {
      background: #f6ffed;
      color: #52c41a;
      border: 1px solid #b7eb8f;
    }
    
    &.inactive {
      background: #fff2e8;
      color: #fa8c16;
      border: 1px solid #ffd591;
    }
    
    &.error {
      background: #fff1f0;
      color: #ff4d4f;
      border: 1px solid #ffccc7;
    }
  }
`;

const ServiceCard = styled(Card)`
  .ant-card-head {
    background: #fafafa;
  }
  
  &.service-active {
    border-color: #52c41a;
    box-shadow: 0 2px 8px rgba(82, 196, 26, 0.15);
  }
  
  &.service-inactive {
    border-color: #fa8c16;
  }
  
  &.service-error {
    border-color: #ff4d4f;
  }
`;

const ConfigPage = ({ apiStatus, onStatusUpdate }) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [testingConnection, setTestingConnection] = useState(false);
  const [config, setConfig] = useState({
    openai_api_key: '',
    anthropic_api_key: '',
    provider_preference: 'openai',
    rag_enabled: true,
    assistente_etp_enabled: true,
    max_tokens: 4000,
    temperature: 0.7
  });

  // Carregar configurações ao montar o componente
  useEffect(() => {
    loadConfig();
  }, []);

  const loadConfig = async () => {
    try {
      const response = await apiService.obterConfig();
      if (response.status === 'success') {
        setConfig(response.config);
        form.setFieldsValue(response.config);
      }
    } catch (error) {
      console.error('Erro ao carregar configurações:', error);
    }
  };

  const handleSave = async (values) => {
    setLoading(true);
    try {
      const response = await apiService.salvarConfig(values);
      
      if (response.status === 'success') {
        setConfig(values);
        message.success('Configurações salvas com sucesso!');
        
        // Atualizar status dos serviços
        if (onStatusUpdate) {
          onStatusUpdate();
        }
      }
    } catch (error) {
      message.error(`Erro ao salvar configurações: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleTestConnection = async () => {
    setTestingConnection(true);
    try {
      const values = form.getFieldsValue();
      const response = await apiService.testarConexao(values);
      
      if (response.status === 'success') {
        message.success('Conexão testada com sucesso!');
        
        // Atualizar status
        if (onStatusUpdate) {
          onStatusUpdate();
        }
      }
    } catch (error) {
      message.error(`Erro no teste de conexão: ${error.message}`);
    } finally {
      setTestingConnection(false);
    }
  };

  const getServiceStatus = (service) => {
    if (!apiStatus) return 'inactive';
    
    switch (service) {
      case 'openai':
        return apiStatus.openai_api ? 'active' : 'inactive';
      case 'anthropic':
        return apiStatus.anthropic_api ? 'active' : 'inactive';
      case 'rag':
        return apiStatus.rag_assistant ? 'active' : 'inactive';
      case 'etp':
        return apiStatus.assistente_etp ? 'active' : 'inactive';
      default:
        return 'inactive';
    }
  };

  const renderStatusBadge = (service) => {
    const status = getServiceStatus(service);
    const statusConfig = {
      active: { color: 'success', text: 'Ativo', icon: <CheckCircleOutlined /> },
      inactive: { color: 'warning', text: 'Inativo', icon: <ExclamationCircleOutlined /> },
      error: { color: 'error', text: 'Erro', icon: <ExclamationCircleOutlined /> }
    };
    
    const config = statusConfig[status];
    return (
      <Badge 
        status={config.color} 
        text={
          <span className={`status-indicator ${status}`}>
            {config.icon} {config.text}
          </span>
        }
      />
    );
  };

  return (
    <ConfigContainer>
      <Title level={2}>
        <SettingOutlined /> Configurações do Sistema
      </Title>
      
      <Alert
        message="Configuração de APIs"
        description="Configure as chaves de API para ativar os serviços de IA. Todas as informações são armazenadas de forma segura."
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />

      <Form
        form={form}
        layout="vertical"
        onFinish={handleSave}
        initialValues={config}
        size="large"
      >
        <Row gutter={[24, 24]}>
          {/* Configurações OpenAI */}
          <Col span={12}>
            <ServiceCard 
              className={`service-${getServiceStatus('openai')}`}
              title={
                <Space>
                  <ApiOutlined />
                  OpenAI API
                  {renderStatusBadge('openai')}
                </Space>
              }
              size="small"
            >
              <Form.Item
                name="openai_api_key"
                label="Chave da API OpenAI"
                rules={[
                  { required: true, message: 'Chave da API é obrigatória' },
                  { min: 20, message: 'Chave deve ter pelo menos 20 caracteres' }
                ]}
              >
                <Password
                  placeholder="sk-..."
                  iconRender={(visible) => (visible ? <EyeTwoTone /> : <EyeInvisibleOutlined />)}
                />
              </Form.Item>
              
              <Text type="secondary" style={{ fontSize: '12px' }}>
                Usado para geração de ETP e análise de campos
              </Text>
            </ServiceCard>
          </Col>

          {/* Configurações Anthropic */}
          <Col span={12}>
            <ServiceCard 
              className={`service-${getServiceStatus('anthropic')}`}
              title={
                <Space>
                  <RobotOutlined />
                  Anthropic API
                  {renderStatusBadge('anthropic')}
                </Space>
              }
              size="small"
            >
              <Form.Item
                name="anthropic_api_key"
                label="Chave da API Anthropic"
                rules={[
                  { min: 20, message: 'Chave deve ter pelo menos 20 caracteres' }
                ]}
              >
                <Password
                  placeholder="sk-ant-..."
                  iconRender={(visible) => (visible ? <EyeTwoTone /> : <EyeInvisibleOutlined />)}
                />
              </Form.Item>
              
              <Text type="secondary" style={{ fontSize: '12px' }}>
                Alternativa para geração de conteúdo
              </Text>
            </ServiceCard>
          </Col>

          {/* Configurações de Serviços */}
          <Col span={24}>
            <Card title="Configurações de Serviços" size="small">
              <Row gutter={[24, 16]}>
                <Col span={8}>
                  <Form.Item
                    name="provider_preference"
                    label="Provedor Preferido"
                  >
                    <Select>
                      <Option value="openai">OpenAI (GPT)</Option>
                      <Option value="anthropic">Anthropic (Claude)</Option>
                    </Select>
                  </Form.Item>
                </Col>

                <Col span={8}>
                  <Form.Item
                    name="max_tokens"
                    label="Máximo de Tokens"
                  >
                    <Input type="number" min={1000} max={8000} />
                  </Form.Item>
                </Col>

                <Col span={8}>
                  <Form.Item
                    name="temperature"
                    label="Temperatura (Criatividade)"
                  >
                    <Input type="number" min={0} max={1} step={0.1} />
                  </Form.Item>
                </Col>
              </Row>

              <Row gutter={[24, 16]}>
                <Col span={12}>
                  <Form.Item
                    name="rag_enabled"
                    label="Assistente RAG (Lei 14.133)"
                    valuePropName="checked"
                  >
                    <Switch 
                      checkedChildren="Ativo" 
                      unCheckedChildren="Inativo"
                    />
                  </Form.Item>
                  {renderStatusBadge('rag')}
                </Col>

                <Col span={12}>
                  <Form.Item
                    name="assistente_etp_enabled"
                    label="Assistente ETP Inteligente"
                    valuePropName="checked"
                  >
                    <Switch 
                      checkedChildren="Ativo" 
                      unCheckedChildren="Inativo"
                    />
                  </Form.Item>
                  {renderStatusBadge('etp')}
                </Col>
              </Row>
            </Card>
          </Col>

          {/* Status Geral do Sistema */}
          <Col span={24}>
            <Card title="Status do Sistema" size="small">
              <Row gutter={[16, 16]}>
                <Col span={6}>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '24px', marginBottom: '8px' }}>
                      {apiStatus?.openai_api ? '✅' : '❌'}
                    </div>
                    <Text>OpenAI API</Text>
                  </div>
                </Col>

                <Col span={6}>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '24px', marginBottom: '8px' }}>
                      {apiStatus?.anthropic_api ? '✅' : '❌'}
                    </div>
                    <Text>Anthropic API</Text>
                  </div>
                </Col>

                <Col span={6}>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '24px', marginBottom: '8px' }}>
                      {apiStatus?.rag_assistant ? '✅' : '❌'}
                    </div>
                    <Text>RAG Assistant</Text>
                  </div>
                </Col>

                <Col span={6}>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '24px', marginBottom: '8px' }}>
                      {apiStatus?.assistente_etp ? '✅' : '❌'}
                    </div>
                    <Text>ETP Assistant</Text>
                  </div>
                </Col>
              </Row>
            </Card>
          </Col>
        </Row>

        <Divider />

        <Row justify="center">
          <Col>
            <Space size="large">
              <Button
                type="primary"
                htmlType="submit"
                icon={<SaveOutlined />}
                loading={loading}
                size="large"
              >
                Salvar Configurações
              </Button>
              
              <Button
                icon={<ReloadOutlined />}
                onClick={handleTestConnection}
                loading={testingConnection}
                size="large"
              >
                Testar Conexão
              </Button>
              
              <Button
                icon={<ReloadOutlined />}
                onClick={loadConfig}
                size="large"
              >
                Recarregar
              </Button>
            </Space>
          </Col>
        </Row>
      </Form>

      <Card style={{ marginTop: 24 }} title="💡 Dicas de Configuração" size="small">
        <Row gutter={[16, 16]}>
          <Col span={12}>
            <Paragraph>
              <Text strong>OpenAI API:</Text>
              <br />
              • Obtenha sua chave em: platform.openai.com
              <br />
              • Necessária para geração de ETP
              <br />
              • Suporta modelos GPT-3.5 e GPT-4
            </Paragraph>
          </Col>
          
          <Col span={12}>
            <Paragraph>
              <Text strong>Anthropic API:</Text>
              <br />
              • Obtenha sua chave em: console.anthropic.com
              <br />
              • Alternativa ao OpenAI
              <br />
              • Suporta modelos Claude
            </Paragraph>
          </Col>
        </Row>
      </Card>
    </ConfigContainer>
  );
};

export default ConfigPage;