import React, { useState, useRef, useEffect } from 'react';
import { Editor } from '@tinymce/tinymce-react';
import {
  Card,
  Button,
  Space,
  Typography,
  Row,
  Col,
  message,
  Modal,
  Input,
  Select
} from 'antd';
import {
  SaveOutlined,
  EyeOutlined,
  DownloadOutlined,
  FileTextOutlined,
  CheckCircleOutlined
} from '@ant-design/icons';
import styled from 'styled-components';
import { apiService } from '../../services/apiService';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;

// Styled Components
const EditorContainer = styled.div`
  .tox-tinymce {
    border-radius: 8px;
    border: 1px solid #d9d9d9;
  }
  
  .tox-toolbar {
    background: #fafafa;
  }
`;

const PreviewContainer = styled.div`
  background: white;
  padding: 24px;
  border-radius: 8px;
  border: 1px solid #d9d9d9;
  min-height: 500px;
  
  h1, h2, h3, h4, h5, h6 {
    color: #1890ff;
    margin-top: 24px;
    margin-bottom: 16px;
  }
  
  p {
    margin-bottom: 16px;
    line-height: 1.6;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0;
    
    th, td {
      border: 1px solid #d9d9d9;
      padding: 8px 12px;
      text-align: left;
    }
    
    th {
      background: #fafafa;
      font-weight: 600;
    }
  }
`;

const ActionBar = styled.div`
  background: #fafafa;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 16px;
  border: 1px solid #d9d9d9;
`;

const EtpEditor = ({ apiStatus }) => {
  const editorRef = useRef(null);
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [previewMode, setPreviewMode] = useState(false);
  const [saveModalVisible, setSaveModalVisible] = useState(false);
  const [documentTitle, setDocumentTitle] = useState('');
  const [assistantModalVisible, setAssistantModalVisible] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const [improvementType, setImprovementType] = useState('geral');

  // Template inicial do ETP
  const etpTemplate = `
    <h1 style="text-align: center;">ESTUDO TÉCNICO PRELIMINAR (ETP)</h1>
    
    <h2>1. DESCRIÇÃO DA NECESSIDADE</h2>
    <p>Descreva aqui a contextualização do problema ou oportunidade identificada...</p>
    
    <h2>2. HISTÓRICO DE CONTRATAÇÕES SIMILARES</h2>
    <p>Levantamento de contratações anteriores relacionadas...</p>
    
    <h2>3. SOLUÇÕES EXISTENTES NO MERCADO</h2>
    <p>Pesquisa abrangente de alternativas disponíveis...</p>
    
    <h2>4. LEVANTAMENTO E ANÁLISE DE RISCOS</h2>
    <p>Elaboração de Mapa de Riscos obrigatório...</p>
    
    <h2>5. CRITÉRIOS DE SUSTENTABILIDADE</h2>
    <p>Conformidade com Guia de Contratações Sustentáveis...</p>
    
    <h2>6. ESTIMATIVA DO VALOR DA CONTRATAÇÃO</h2>
    <p>Metodologia de pesquisa conforme art. 23 da Lei 14.133/2021...</p>
    
    <h2>7. DEFINIÇÃO DO OBJETO</h2>
    <p>Descrição técnica precisa e completa...</p>
    
    <h2>8. JUSTIFICATIVA DE ESCOLHA DA SOLUÇÃO</h2>
    <p>Fundamentação técnica, operacional e financeira...</p>
    
    <h2>9. PREVISÃO DE CONTRATAÇÕES FUTURAS (PCA)</h2>
    <p>Inserção no Plano de Contratações Anuais...</p>
    
    <h2>10. ESTIMATIVA DE QUANTIDADES</h2>
    <p>Memórias de cálculo fundamentadas...</p>
    
    <h2>11. JUSTIFICATIVAS PARA PARCELAMENTO, AGRUPAMENTO E SUBCONTRATAÇÃO</h2>
    <p>Análise de viabilidade técnica e econômica...</p>
    
    <h2>12. DEPENDÊNCIA DO CONTRATADO</h2>
    <p>Análise de dependência tecnológica...</p>
    
    <h2>13. TRANSIÇÃO CONTRATUAL</h2>
    <p>Planejamento da transição entre contratos...</p>
    
    <h2>14. ESTRATÉGIA DE IMPLANTAÇÃO</h2>
    <p>Metodologia de implementação detalhada...</p>
    
    <h2>15. BENEFÍCIOS ESPERADOS</h2>
    <p>Benefícios quantitativos e qualitativos...</p>
    
    <h2>16. DECLARAÇÃO DE ADEQUAÇÃO ORÇAMENTÁRIA</h2>
    <p>Confirmação de disponibilidade orçamentária...</p>
    
    <h2>17. APROVAÇÃO DA AUTORIDADE COMPETENTE</h2>
    <p>Identificação da autoridade competente...</p>
    
    <br/>
    <p><strong>Data:</strong> ___/___/______</p>
    <p><strong>Responsável:</strong> _________________________</p>
    <p><strong>Assinatura:</strong> _________________________</p>
  `;

  // Inicializar com template
  useEffect(() => {
    if (!content) {
      setContent(etpTemplate);
    }
  }, [content, etpTemplate]);

  // Configuração do TinyMCE
  const editorConfig = {
    apiKey: process.env.REACT_APP_TINYMCE_API_KEY,
    height: 600,
    menubar: true,
    plugins: [
      'advlist', 'autolink', 'lists', 'link', 'image', 'charmap', 'preview',
      'anchor', 'searchreplace', 'visualblocks', 'code', 'fullscreen',
      'insertdatetime', 'media', 'table', 'help', 'wordcount', 'save',
      'print', 'pagebreak', 'nonbreaking', 'template', 'paste'
    ],
    toolbar: [
      'undo redo | blocks | bold italic underline strikethrough | alignleft aligncenter alignright alignjustify',
      'bullist numlist outdent indent | removeformat | help',
      'link image media table | insertdatetime | preview print save',
      'searchreplace | visualblocks fullscreen | pagebreak nonbreaking'
    ].join(' | '),
    content_style: `
      body { 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
        font-size: 14px; 
        line-height: 1.6;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
      }
      h1, h2, h3, h4, h5, h6 { 
        color: #1890ff; 
        margin-top: 24px; 
        margin-bottom: 16px; 
      }
      h1 { font-size: 24px; }
      h2 { font-size: 20px; }
      h3 { font-size: 18px; }
      p { margin-bottom: 16px; }
      table { 
        border-collapse: collapse; 
        width: 100%; 
        margin: 16px 0; 
      }
      table th, table td { 
        border: 1px solid #d9d9d9; 
        padding: 8px 12px; 
        text-align: left; 
      }
      table th { 
        background-color: #fafafa; 
        font-weight: 600; 
      }
    `,
    language: 'pt_BR',
    branding: false,
    resize: false,
    paste_data_images: true,
    automatic_uploads: false,
    setup: (editor) => {
      // Adicionar botão personalizado para assistente IA
      editor.ui.registry.addButton('aiassistant', {
        text: '🤖 IA',
        tooltip: 'Assistente de IA',
        onAction: () => {
          const selection = editor.selection.getContent({ format: 'text' });
          if (selection) {
            setSelectedText(selection);
            setAssistantModalVisible(true);
          } else {
            message.warning('Selecione um texto para usar o assistente IA');
          }
        }
      });
      
      // Adicionar o botão à toolbar
      editor.ui.registry.addButton('customtoolbar', {
        text: '',
        onAction: () => {}
      });
    }
  };

  const handleEditorChange = (newContent) => {
    setContent(newContent);
  };

  const handleSave = () => {
    if (!documentTitle.trim()) {
      message.error('Digite um título para o documento');
      return;
    }
    
    // Aqui você implementaria a lógica de salvamento
    // Por exemplo, salvar no localStorage ou enviar para API
    localStorage.setItem(`etp_${Date.now()}`, JSON.stringify({
      title: documentTitle,
      content: content,
      createdAt: new Date().toISOString()
    }));
    
    message.success('Documento salvo com sucesso!');
    setSaveModalVisible(false);
    setDocumentTitle('');
  };

  const handleExport = (format) => {
    const element = document.createElement('a');
    const file = new Blob([content], { type: 'text/html' });
    element.href = URL.createObjectURL(file);
    element.download = `ETP_${new Date().toISOString().split('T')[0]}.${format}`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  const handleImproveText = async () => {
    if (!selectedText.trim()) {
      message.error('Nenhum texto selecionado');
      return;
    }

    if (!apiStatus.assistente_etp) {
      message.error('Configure o assistente IA primeiro');
      return;
    }

    setLoading(true);
    try {
      const response = await apiService.melhorarTexto(selectedText, improvementType);
      
      if (response.status === 'success') {
        const improvedText = response.melhoria.texto_melhorado;
        
        // Substituir o texto selecionado no editor
        if (editorRef.current) {
          editorRef.current.selection.setContent(improvedText);
        }
        
        message.success('Texto melhorado com sucesso!');
        setAssistantModalVisible(false);
      }
    } catch (error) {
      message.error(`Erro ao melhorar texto: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const togglePreview = () => {
    setPreviewMode(!previewMode);
  };

  return (
    <div>
      <Title level={2}>
        <FileTextOutlined /> Editor de ETP
      </Title>
      
      <ActionBar>
        <Row justify="space-between" align="middle">
          <Col>
            <Space>
              <Button 
                type="primary" 
                icon={<SaveOutlined />}
                onClick={() => setSaveModalVisible(true)}
              >
                Salvar
              </Button>
              
              <Button 
                icon={<EyeOutlined />}
                onClick={togglePreview}
              >
                {previewMode ? 'Editar' : 'Visualizar'}
              </Button>
              
              <Button 
                icon={<DownloadOutlined />}
                onClick={() => handleExport('html')}
              >
                Exportar HTML
              </Button>
            </Space>
          </Col>
          
          <Col>
            <Space>
              <Text type="secondary">
                {apiStatus.assistente_etp ? (
                  <><CheckCircleOutlined style={{ color: '#52c41a' }} /> IA Ativa</>
                ) : (
                  <>⚠️ IA Inativa</>
                )}
              </Text>
            </Space>
          </Col>
        </Row>
      </ActionBar>

      <Card>
        {previewMode ? (
          <PreviewContainer 
            dangerouslySetInnerHTML={{ __html: content }}
          />
        ) : (
          <EditorContainer>
            <Editor
              ref={editorRef}
              value={content}
              init={editorConfig}
              onEditorChange={handleEditorChange}
            />
          </EditorContainer>
        )}
      </Card>

      {/* Modal de Salvamento */}
      <Modal
        title="Salvar Documento"
        open={saveModalVisible}
        onOk={handleSave}
        onCancel={() => setSaveModalVisible(false)}
        okText="Salvar"
        cancelText="Cancelar"
      >
        <Input
          placeholder="Digite o título do documento"
          value={documentTitle}
          onChange={(e) => setDocumentTitle(e.target.value)}
          prefix={<FileTextOutlined />}
        />
      </Modal>

      {/* Modal do Assistente IA */}
      <Modal
        title="🤖 Assistente de IA"
        open={assistantModalVisible}
        onOk={handleImproveText}
        onCancel={() => setAssistantModalVisible(false)}
        okText="Melhorar Texto"
        cancelText="Cancelar"
        confirmLoading={loading}
        width={600}
      >
        <Space direction="vertical" style={{ width: '100%' }}>
          <div>
            <Text strong>Texto Selecionado:</Text>
            <TextArea
              value={selectedText}
              onChange={(e) => setSelectedText(e.target.value)}
              rows={4}
              placeholder="Texto a ser melhorado..."
            />
          </div>
          
          <div>
            <Text strong>Tipo de Melhoria:</Text>
            <Select
              value={improvementType}
              onChange={setImprovementType}
              style={{ width: '100%' }}
            >
              <Option value="geral">Melhoria Geral</Option>
              <Option value="gramatica">Correção Gramatical</Option>
              <Option value="tecnico">Linguagem Técnica</Option>
            </Select>
          </div>
        </Space>
      </Modal>
    </div>
  );
};

export default EtpEditor;