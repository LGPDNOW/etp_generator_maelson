import React from 'react';
import { Layout, Typography, Space, Badge, Button, Tooltip } from 'antd';
import { 
  SettingOutlined, 
  ApiOutlined,
  CheckCircleOutlined,
  ExclamationCircleOutlined,
  GithubOutlined,
  InfoCircleOutlined
} from '@ant-design/icons';
import styled from 'styled-components';

const { Header: AntHeader } = Layout;
const { Title, Text } = Typography;

// Styled Components
const StyledHeader = styled(AntHeader)`
  background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%);
  padding: 0 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  position: sticky;
  top: 0;
  z-index: 1000;
`;

const HeaderContent = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
`;

const Logo = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  
  .logo-icon {
    width: 32px;
    height: 32px;
    background: white;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    color: #1890ff;
  }
  
  .logo-text {
    color: white;
    margin: 0;
    font-weight: 600;
    font-size: 20px;
  }
  
  .logo-subtitle {
    color: rgba(255, 255, 255, 0.8);
    font-size: 12px;
    margin-left: 8px;
  }
`;

const StatusIndicators = styled.div`
  display: flex;
  align-items: center;
  gap: 16px;
`;

const StatusBadge = styled.div`
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: white;
  font-size: 12px;
  
  &.active {
    background: rgba(82, 196, 26, 0.2);
    border: 1px solid rgba(82, 196, 26, 0.3);
  }
  
  &.inactive {
    background: rgba(250, 140, 22, 0.2);
    border: 1px solid rgba(250, 140, 22, 0.3);
  }
`;

const ActionButtons = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
`;

const Header = ({ apiStatus, onConfigClick }) => {
  const getOverallStatus = () => {
    if (!apiStatus) return 'loading';
    
    const hasActiveApi = apiStatus.openai_api || apiStatus.anthropic_api;
    const hasActiveServices = apiStatus.rag_assistant || apiStatus.assistente_etp;
    
    if (hasActiveApi && hasActiveServices) return 'active';
    if (hasActiveApi) return 'partial';
    return 'inactive';
  };

  const getStatusText = () => {
    const status = getOverallStatus();
    switch (status) {
      case 'active':
        return 'Sistema Ativo';
      case 'partial':
        return 'Parcialmente Ativo';
      case 'inactive':
        return 'Sistema Inativo';
      default:
        return 'Carregando...';
    }
  };

  const getStatusIcon = () => {
    const status = getOverallStatus();
    switch (status) {
      case 'active':
        return <CheckCircleOutlined style={{ color: '#52c41a' }} />;
      case 'partial':
      case 'inactive':
        return <ExclamationCircleOutlined style={{ color: '#fa8c16' }} />;
      default:
        return <ApiOutlined />;
    }
  };

  const renderServiceStatus = (service, label) => {
    const isActive = apiStatus?.[service];
    return (
      <Tooltip title={`${label}: ${isActive ? 'Ativo' : 'Inativo'}`}>
        <StatusBadge className={isActive ? 'active' : 'inactive'}>
          {isActive ? <CheckCircleOutlined /> : <ExclamationCircleOutlined />}
          {label}
        </StatusBadge>
      </Tooltip>
    );
  };

  return (
    <StyledHeader>
      <HeaderContent>
        <Logo>
          <div className="logo-icon">
            📄
          </div>
          <div>
            <Title level={4} className="logo-text">
              ETP Generator
            </Title>
            <Text className="logo-subtitle">
              Sistema Integrado de Documentos
            </Text>
          </div>
        </Logo>

        <StatusIndicators>
          {/* Status dos Serviços */}
          {renderServiceStatus('openai_api', 'OpenAI')}
          {renderServiceStatus('anthropic_api', 'Anthropic')}
          {renderServiceStatus('rag_assistant', 'RAG')}
          {renderServiceStatus('assistente_etp', 'ETP IA')}
          
          {/* Status Geral */}
          <Tooltip title={getStatusText()}>
            <StatusBadge className={getOverallStatus()}>
              {getStatusIcon()}
              {getStatusText()}
            </StatusBadge>
          </Tooltip>
        </StatusIndicators>

        <ActionButtons>
          <Tooltip title="Configurações do Sistema">
            <Button
              type="text"
              icon={<SettingOutlined />}
              onClick={onConfigClick}
              style={{ color: 'white' }}
            />
          </Tooltip>
          
          <Tooltip title="Sobre o Sistema">
            <Button
              type="text"
              icon={<InfoCircleOutlined />}
              style={{ color: 'white' }}
              onClick={() => {
                // Aqui você pode abrir um modal com informações sobre o sistema
                console.log('Abrir modal de informações');
              }}
            />
          </Tooltip>
          
          <Tooltip title="Código no GitHub">
            <Button
              type="text"
              icon={<GithubOutlined />}
              style={{ color: 'white' }}
              onClick={() => {
                window.open('https://github.com/seu-usuario/etp-generator', '_blank');
              }}
            />
          </Tooltip>
        </ActionButtons>
      </HeaderContent>
    </StyledHeader>
  );
};

export default Header;