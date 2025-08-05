import React, { useState } from 'react';
import {
  Form,
  Input,
  Button,
  Card,
  Space,
  Typography,
  Row,
  Col,
  message,
  Spin,
  Modal,
  Alert,
  Badge,
  Divider,
  Tooltip
} from 'antd';
import {
  RobotOutlined,
  FileTextOutlined,
  SaveOutlined,
  EyeOutlined
} from '@ant-design/icons';
import styled from 'styled-components';
import { apiService } from '../../services/apiService';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;

// Styled Components
const FormContainer = styled.div`
  .ant-form-item {
    margin-bottom: 24px;
  }
  
  .field-with-assistant {
    position: relative;
    
    .assistant-button {
      position: absolute;
      top: 0;
      right: 0;
      z-index: 10;
      border-radius: 0 6px 0 6px;
    }
  }
`;

const AssistantButton = styled(Button)`
  &.active {
    background: #52c41a;
    border-color: #52c41a;
    color: white;
    
    &:hover {
      background: #73d13d;
      border-color: #73d13d;
    }
  }
`;

const AnalysisCard = styled(Card)`
  margin-top: 16px;
  border-left: 4px solid #1890ff;
  
  &.warning {
    border-left-color: #faad14;
  }
  
  &.error {
    border-left-color: #ff4d4f;
  }
  
  &.success {
    border-left-color: #52c41a;
  }
`;

const EtpForm = ({ apiStatus, onGenerate }) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [assistantLoading, setAssistantLoading] = useState(false);
  const [activeAssistant, setActiveAssistant] = useState(null);
  const [analysisResults, setAnalysisResults] = useState({});
  const [assistantModalVisible, setAssistantModalVisible] = useState(false);
  const [currentFieldAnalysis, setCurrentFieldAnalysis] = useState(null);

  // Campos críticos que possuem assistente IA
  const criticalFields = [
    {
      name: 'descricao_necessidade',
      label: 'Descrição da Necessidade',
      required: true,
      assistantType: 'descricao_necessidade'
    },
    {
      name: 'historico_contratacoes',
      label: 'Histórico de Contratações Similares',
      required: true,
      assistantType: 'historico_contratacoes'
    },
    {
      name: 'solucoes_mercado',
      label: 'Soluções Existentes no Mercado',
      required: true,
      assistantType: 'solucoes_mercado'
    },
    {
      name: 'analise_riscos',
      label: 'Levantamento e Análise de Riscos',
      required: true,
      assistantType: 'analise_riscos'
    },
    {
      name: 'criterios_sustentabilidade',
      label: 'Critérios de Sustentabilidade',
      required: true,
      assistantType: 'criterios_sustentabilidade'
    },
    {
      name: 'estimativa_valor',
      label: 'Estimativa do Valor da Contratação',
      required: true,
      assistantType: 'estimativa_valor'
    },
    {
      name: 'definicao_objeto',
      label: 'Definição do Objeto',
      required: true,
      assistantType: 'definicao_objeto'
    },
    {
      name: 'justificativa_escolha',
      label: 'Justificativa de Escolha da Solução',
      required: true,
      assistantType: 'justificativa_escolha'
    },
    {
      name: 'previsao_contratacoes',
      label: 'Previsão de Contratações Futuras (PCA)',
      required: true,
      assistantType: 'previsao_contratacoes'
    },
    {
      name: 'estimativa_quantidades',
      label: 'Estimativa de Quantidades',
      required: true,
      assistantType: 'estimativa_quantidades'
    },
    {
      name: 'justificativas_parcelamento',
      label: 'Justificativas para Parcelamento, Agrupamento e Subcontratação',
      required: true,
      assistantType: 'justificativas_parcelamento'
    }
  ];

  const handleAssistantClick = async (field) => {
    if (!apiStatus.assistente_etp) {
      message.error('Configure o assistente IA primeiro');
      return;
    }

    const fieldValue = form.getFieldValue(field.name);
    if (!fieldValue || fieldValue.trim().length < 10) {
      message.warning('Digite pelo menos 10 caracteres no campo para usar o assistente');
      return;
    }

    setAssistantLoading(true);
    setActiveAssistant(field.name);

    try {
      // Obter todos os valores do formulário para contexto
      const allValues = form.getFieldsValue();
      
      const response = await apiService.analisarCampo(
        field.assistantType,
        fieldValue,
        allValues
      );

      if (response.status === 'success') {
        setAnalysisResults(prev => ({
          ...prev,
          [field.name]: response.analise
        }));
        
        setCurrentFieldAnalysis({
          field: field,
          analysis: response.analise
        });
        
        setAssistantModalVisible(true);
        
        message.success('Análise concluída!');
      }
    } catch (error) {
      message.error(`Erro na análise: ${error.message}`);
    } finally {
      setAssistantLoading(false);
      setActiveAssistant(null);
    }
  };

  const handleApplyImprovement = () => {
    if (currentFieldAnalysis && currentFieldAnalysis.analysis.sugestao_melhoria) {
      form.setFieldValue(
        currentFieldAnalysis.field.name, 
        currentFieldAnalysis.analysis.sugestao_melhoria
      );
      message.success('Melhoria aplicada ao campo!');
      setAssistantModalVisible(false);
    }
  };

  const handleSubmit = async (values) => {
    setLoading(true);
    try {
      const response = await apiService.gerarEtp(values);
      
      if (response.status === 'success') {
        message.success('ETP gerado com sucesso!');
        if (onGenerate) {
          onGenerate(response.etp);
        }
      }
    } catch (error) {
      message.error(`Erro ao gerar ETP: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const getAnalysisStatus = (fieldName) => {
    const analysis = analysisResults[fieldName];
    if (!analysis) return null;
    
    if (analysis.score >= 8) return 'success';
    if (analysis.score >= 6) return 'warning';
    return 'error';
  };

  const renderFieldWithAssistant = (field) => {
    const analysis = analysisResults[field.name];
    const status = getAnalysisStatus(field.name);
    const isLoading = assistantLoading && activeAssistant === field.name;

    return (
      <Form.Item
        key={field.name}
        name={field.name}
        label={
          <Space>
            {field.label}
            {field.required && <Text type="danger">*</Text>}
            {status && (
              <Badge 
                status={status} 
                text={`Score: ${analysis.score}/10`}
              />
            )}
          </Space>
        }
        rules={[
          { required: field.required, message: `${field.label} é obrigatório` },
          { min: 10, message: 'Mínimo de 10 caracteres' }
        ]}
      >
        <div className="field-with-assistant">
          <TextArea
            rows={4}
            placeholder={`Digite ${field.label.toLowerCase()}...`}
          />
          
          <Tooltip title="Assistente IA - Analisar campo">
            <AssistantButton
              className={`assistant-button ${status ? 'active' : ''}`}
              icon={isLoading ? <Spin size="small" /> : <RobotOutlined />}
              size="small"
              loading={isLoading}
              onClick={() => handleAssistantClick(field)}
              type={status === 'success' ? 'primary' : 'default'}
            />
          </Tooltip>
        </div>
      </Form.Item>
    );
  };

  return (
    <FormContainer>
      <Title level={2}>
        <FileTextOutlined /> Formulário ETP
      </Title>
      
      <Alert
        message="Assistente IA Integrado"
        description="Use os botões 🤖 em cada campo para obter análise e sugestões de melhoria baseadas nas normas técnicas do TRT-2."
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />

      <Form
        form={form}
        layout="vertical"
        onFinish={handleSubmit}
        size="large"
      >
        <Row gutter={[24, 0]}>
          <Col span={24}>
            {criticalFields.map(field => renderFieldWithAssistant(field))}
          </Col>
        </Row>

        <Divider />

        <Row justify="center">
          <Col>
            <Space size="large">
              <Button
                type="primary"
                htmlType="submit"
                icon={<FileTextOutlined />}
                loading={loading}
                size="large"
              >
                Gerar ETP
              </Button>
              
              <Button
                icon={<SaveOutlined />}
                onClick={() => {
                  const values = form.getFieldsValue();
                  localStorage.setItem('etp_draft', JSON.stringify(values));
                  message.success('Rascunho salvo!');
                }}
              >
                Salvar Rascunho
              </Button>
              
              <Button
                icon={<EyeOutlined />}
                onClick={() => {
                  const draft = localStorage.getItem('etp_draft');
                  if (draft) {
                    form.setFieldsValue(JSON.parse(draft));
                    message.success('Rascunho carregado!');
                  } else {
                    message.info('Nenhum rascunho encontrado');
                  }
                }}
              >
                Carregar Rascunho
              </Button>
            </Space>
          </Col>
        </Row>
      </Form>

      {/* Modal de Análise do Assistente */}
      <Modal
        title={
          <Space>
            <RobotOutlined />
            Análise do Assistente IA
            {currentFieldAnalysis && (
              <Badge 
                status={getAnalysisStatus(currentFieldAnalysis.field.name)} 
                text={`Score: ${currentFieldAnalysis.analysis.score}/10`}
              />
            )}
          </Space>
        }
        open={assistantModalVisible}
        onCancel={() => setAssistantModalVisible(false)}
        width={800}
        footer={[
          <Button key="close" onClick={() => setAssistantModalVisible(false)}>
            Fechar
          </Button>,
          currentFieldAnalysis?.analysis.sugestao_melhoria && (
            <Button 
              key="apply" 
              type="primary" 
              onClick={handleApplyImprovement}
            >
              Aplicar Melhoria
            </Button>
          )
        ]}
      >
        {currentFieldAnalysis && (
          <Space direction="vertical" style={{ width: '100%' }}>
            <AnalysisCard 
              size="small" 
              title="📊 Pontuação"
              className={getAnalysisStatus(currentFieldAnalysis.field.name)}
            >
              <Text strong>Score: {currentFieldAnalysis.analysis.score}/10</Text>
              <br />
              <Text>{currentFieldAnalysis.analysis.justificativa_score}</Text>
            </AnalysisCard>

            {currentFieldAnalysis.analysis.problemas_identificados?.length > 0 && (
              <AnalysisCard size="small" title="⚠️ Problemas Identificados" className="warning">
                <ul>
                  {currentFieldAnalysis.analysis.problemas_identificados.map((problema, index) => (
                    <li key={index}>{problema}</li>
                  ))}
                </ul>
              </AnalysisCard>
            )}

            {currentFieldAnalysis.analysis.sugestoes_melhoria?.length > 0 && (
              <AnalysisCard size="small" title="💡 Sugestões de Melhoria" className="success">
                <ul>
                  {currentFieldAnalysis.analysis.sugestoes_melhoria.map((sugestao, index) => (
                    <li key={index}>{sugestao}</li>
                  ))}
                </ul>
              </AnalysisCard>
            )}

            {currentFieldAnalysis.analysis.sugestao_melhoria && (
              <AnalysisCard size="small" title="✨ Texto Melhorado" className="success">
                <Paragraph copyable>
                  {currentFieldAnalysis.analysis.sugestao_melhoria}
                </Paragraph>
              </AnalysisCard>
            )}

            {currentFieldAnalysis.analysis.conformidade_trt2 && (
              <AnalysisCard size="small" title="📋 Conformidade TRT-2">
                <Text>
                  <strong>Status:</strong> {currentFieldAnalysis.analysis.conformidade_trt2.status}
                </Text>
                <br />
                <Text>{currentFieldAnalysis.analysis.conformidade_trt2.observacoes}</Text>
              </AnalysisCard>
            )}
          </Space>
        )}
      </Modal>
    </FormContainer>
  );
};

export default EtpForm;