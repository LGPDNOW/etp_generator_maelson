import React, { useState, useRef, useEffect } from 'react';
import {
  Card,
  Input,
  Button,
  Space,
  Typography,
  List,
  Avatar,
  Spin,
  message,
  Row,
  Col,
  Tag,
  Divider,
  Alert,
  Empty,
  Tooltip
} from 'antd';
import {
  SendOutlined,
  UserOutlined,
  RobotOutlined,
  BookOutlined,
  ClockCircleOutlined,
  ClearOutlined,
  QuestionCircleOutlined
} from '@ant-design/icons';
import styled from 'styled-components';
import ReactMarkdown from 'react-markdown';
import { apiService } from '../../services/apiService';

const { Title, Text } = Typography;
const { TextArea } = Input;

// Styled Components
const ChatContainer = styled.div`
  height: 600px;
  display: flex;
  flex-direction: column;
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: #fafafa;
  border-radius: 8px;
  margin-bottom: 16px;
  
  &::-webkit-scrollbar {
    width: 6px;
  }
  
  &::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 3px;
  }
  
  &::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 3px;
  }
`;

const MessageBubble = styled.div`
  margin-bottom: 16px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  
  &.user {
    flex-direction: row-reverse;
    
    .message-content {
      background: #1890ff;
      color: white;
      border-radius: 18px 18px 4px 18px;
    }
  }
  
  &.assistant {
    .message-content {
      background: white;
      border: 1px solid #d9d9d9;
      border-radius: 18px 18px 18px 4px;
    }
  }
  
  .message-content {
    max-width: 70%;
    padding: 12px 16px;
    word-wrap: break-word;
  }
  
  .message-meta {
    font-size: 12px;
    color: #8c8c8c;
    margin-top: 4px;
  }
`;

const InputContainer = styled.div`
  display: flex;
  gap: 8px;
  align-items: flex-end;
`;

const SuggestedQuestions = styled.div`
  margin-bottom: 16px;
  
  .question-tag {
    margin: 4px;
    cursor: pointer;
    transition: all 0.3s;
    
    &:hover {
      transform: translateY(-1px);
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
  }
`;

const RagAssistant = ({ apiStatus }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Perguntas sugeridas
  const suggestedQuestions = [
    "O que é um Estudo Técnico Preliminar?",
    "Quais são os requisitos para licitação?",
    "Como calcular o valor estimado da contratação?",
    "Quais critérios de sustentabilidade devo considerar?",
    "O que deve conter a análise de riscos?",
    "Como justificar o parcelamento do objeto?",
    "Quais são as modalidades de licitação?",
    "O que é o Plano de Contratações Anuais?"
  ];

  // Scroll automático para última mensagem
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Carregar histórico do localStorage
  useEffect(() => {
    const savedHistory = localStorage.getItem('rag_chat_history');
    if (savedHistory) {
      try {
        setMessages(JSON.parse(savedHistory));
      } catch (error) {
        console.error('Erro ao carregar histórico:', error);
      }
    }
  }, []);

  // Salvar histórico no localStorage
  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem('rag_chat_history', JSON.stringify(messages));
    }
  }, [messages]);

  const handleSendMessage = async (question = null) => {
    const messageText = question || inputValue.trim();
    
    if (!messageText) {
      message.warning('Digite uma pergunta');
      return;
    }

    if (!apiStatus.rag_assistant) {
      message.error('Configure o assistente RAG primeiro');
      return;
    }

    // Adicionar mensagem do usuário
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: messageText,
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setLoading(true);

    try {
      // Preparar histórico para contexto
      const chatHistory = messages.map(msg => ({
        role: msg.type === 'user' ? 'human' : 'assistant',
        content: msg.content
      }));

      const response = await apiService.consultarRag(messageText, chatHistory);

      if (response.status === 'success') {
        const assistantMessage = {
          id: Date.now() + 1,
          type: 'assistant',
          content: response.resposta,
          sources: response.fontes || [],
          timestamp: new Date().toLocaleTimeString()
        };

        setMessages(prev => [...prev, assistantMessage]);
      }
    } catch (error) {
      message.error(`Erro na consulta: ${error.message}`);
      
      // Adicionar mensagem de erro
      const errorMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: 'Desculpe, ocorreu um erro ao processar sua pergunta. Tente novamente.',
        timestamp: new Date().toLocaleTimeString(),
        isError: true
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleClearChat = () => {
    setMessages([]);
    localStorage.removeItem('rag_chat_history');
    message.success('Conversa limpa!');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const renderMessage = (msg) => (
    <MessageBubble key={msg.id} className={msg.type}>
      <Avatar
        icon={msg.type === 'user' ? <UserOutlined /> : <RobotOutlined />}
        style={{
          backgroundColor: msg.type === 'user' ? '#1890ff' : '#52c41a',
          flexShrink: 0
        }}
      />
      
      <div className="message-content">
        <div>
          {msg.type === 'assistant' ? (
            <ReactMarkdown
              components={{
                h1: ({children}) => <h3 style={{color: '#1890ff', marginBottom: '8px'}}>{children}</h3>,
                h2: ({children}) => <h4 style={{color: '#1890ff', marginBottom: '6px'}}>{children}</h4>,
                h3: ({children}) => <h5 style={{color: '#1890ff', marginBottom: '4px'}}>{children}</h5>,
                p: ({children}) => <p style={{marginBottom: '8px', lineHeight: '1.5'}}>{children}</p>,
                ul: ({children}) => <ul style={{marginLeft: '16px', marginBottom: '8px'}}>{children}</ul>,
                ol: ({children}) => <ol style={{marginLeft: '16px', marginBottom: '8px'}}>{children}</ol>,
                li: ({children}) => <li style={{marginBottom: '4px'}}>{children}</li>,
                strong: ({children}) => <strong style={{color: '#262626'}}>{children}</strong>,
                em: ({children}) => <em style={{color: '#595959'}}>{children}</em>
              }}
            >
              {msg.content}
            </ReactMarkdown>
          ) : (
            msg.content
          )}
        </div>
        
        {msg.sources && msg.sources.length > 0 && (
          <div style={{ marginTop: 8 }}>
            <Divider style={{ margin: '8px 0' }} />
            <Text type="secondary" style={{ fontSize: '12px' }}>
              <BookOutlined /> Fontes consultadas:
            </Text>
            {msg.sources.map((source, index) => (
              <Tag key={index} size="small" style={{ margin: '2px' }}>
                {source}
              </Tag>
            ))}
          </div>
        )}
        
        <div className="message-meta">
          <ClockCircleOutlined /> {msg.timestamp}
        </div>
      </div>
    </MessageBubble>
  );

  return (
    <div>
      <Title level={2}>
        <QuestionCircleOutlined /> Assistente Lei 14.133
      </Title>
      
      <Alert
        message="Assistente RAG Ativo"
        description="Faça perguntas sobre a Lei 14.133/2021 e obtenha respostas baseadas na documentação oficial."
        type="info"
        showIcon
        style={{ marginBottom: 16 }}
      />

      <Card>
        <ChatContainer>
          {messages.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '40px 0' }}>
              <Empty
                image={Empty.PRESENTED_IMAGE_SIMPLE}
                description="Nenhuma conversa ainda"
              >
                <Text type="secondary">
                  Comece fazendo uma pergunta sobre a Lei 14.133/2021
                </Text>
              </Empty>
              
              <SuggestedQuestions>
                <Title level={4}>Perguntas Sugeridas:</Title>
                {suggestedQuestions.map((question, index) => (
                  <Tag
                    key={index}
                    className="question-tag"
                    color="blue"
                    onClick={() => handleSendMessage(question)}
                  >
                    {question}
                  </Tag>
                ))}
              </SuggestedQuestions>
            </div>
          ) : (
            <MessagesContainer>
              {messages.map(renderMessage)}
              {loading && (
                <MessageBubble className="assistant">
                  <Avatar 
                    icon={<RobotOutlined />}
                    style={{ backgroundColor: '#52c41a' }}
                  />
                  <div className="message-content">
                    <Spin size="small" /> Pensando...
                  </div>
                </MessageBubble>
              )}
              <div ref={messagesEndRef} />
            </MessagesContainer>
          )}

          <Row gutter={[8, 8]} style={{ marginBottom: 16 }}>
            <Col flex="auto">
              <InputContainer>
                <TextArea
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Digite sua pergunta sobre a Lei 14.133..."
                  autoSize={{ minRows: 1, maxRows: 4 }}
                  disabled={loading}
                />
                
                <Button
                  type="primary"
                  icon={<SendOutlined />}
                  onClick={() => handleSendMessage()}
                  loading={loading}
                  disabled={!inputValue.trim()}
                >
                  Enviar
                </Button>
              </InputContainer>
            </Col>
          </Row>

          {messages.length > 0 && (
            <Row justify="space-between" align="middle">
              <Col>
                <Text type="secondary">
                  {messages.length} mensagens na conversa
                </Text>
              </Col>
              
              <Col>
                <Space>
                  <Tooltip title="Limpar conversa">
                    <Button
                      icon={<ClearOutlined />}
                      onClick={handleClearChat}
                      size="small"
                    >
                      Limpar
                    </Button>
                  </Tooltip>
                </Space>
              </Col>
            </Row>
          )}
        </ChatContainer>
      </Card>

      {messages.length === 0 && (
        <Card style={{ marginTop: 16 }} title="💡 Dicas de Uso">
          <List
            size="small"
            dataSource={[
              "Faça perguntas específicas sobre procedimentos licitatórios",
              "Consulte sobre requisitos técnicos para documentos",
              "Peça esclarecimentos sobre artigos específicos da lei",
              "Use o histórico da conversa para perguntas contextuais"
            ]}
            renderItem={(item, index) => (
              <List.Item>
                <Text>
                  <strong>{index + 1}.</strong> {item}
                </Text>
              </List.Item>
            )}
          />
        </Card>
      )}
    </div>
  );
};

export default RagAssistant;