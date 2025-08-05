import React from 'react';
import { Layout, Menu, Typography, Badge, Tooltip } from 'antd';
import { 
  FileTextOutlined, 
  EditOutlined, 
  QuestionCircleOutlined,
  SettingOutlined,
  HomeOutlined,
  BookOutlined,
  RobotOutlined,
  ApiOutlined,
  CheckCircleOutlined,
  ExclamationCircleOutlined
} from '@ant-design/icons';
import styled from 'styled-components';

const { Sider } = Layout;
const { Text } = Typography;

// Styled Components
const StyledSider = styled(Sider)`
  background: #001529;
  box-shadow: 2px 0 8px rgba(0,0,0,0.15);
  
  .ant-layout-sider-trigger {
    background: #002140;
    color: white;
    
    &:hover {
      background: #003a8c;
    }
  }
`;

const SiderHeader = styled.div`
  padding: 16px;
  text-align: center;
  border-bottom: 1px solid #002140;
  margin-bottom: 16px;
`;

const MenuItemWithBadge = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  
  .menu-text {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .status-indicator {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    
    &.active {
      background: #52c41a;
    }
    
    &.inactive {
      background: #fa8c16;
    }
    
    &.disabled {
      background: #d9d9d9;
    }
  }
`;

const Sidebar = ({ collapsed, selectedKey, onMenuClick, apiStatus }) => {
  const getServiceStatus = (service) => {
    if (!apiStatus) return 'disabled';
    return apiStatus[service] ? 'active' : 'inactive';
  };

  const menuItems = [
    {
      key: 'home',
      icon: <HomeOutlined />,
      label: 'Dashboard',
      title: 'Página inicial do sistema'
    },
    {
      key: 'etp-form',
      icon: <FileTextOutlined />,
      label: (
        <MenuItemWithBadge>
          <span className="menu-text">Formulário ETP</span>
          <Tooltip title={`Assistente ETP: ${getServiceStatus('assistente_etp') === 'active' ? 'Ativo' : 'Inativo'}`}>
            <div className={`status-indicator ${getServiceStatus('assistente_etp')}`} />
          </Tooltip>
        </MenuItemWithBadge>
      ),
      title: 'Criar novo ETP com assistente inteligente'
    },
    {
      key: 'etp-editor',
      icon: <EditOutlined />,
      label: (
        <MenuItemWithBadge>
          <span className="menu-text">Editor de ETP</span>
          <Tooltip title="Editor WYSIWYG para documentos">
            <div className="status-indicator active" />
          </Tooltip>
        </MenuItemWithBadge>
      ),
      title: 'Editor rico para documentos ETP'
    },
    {
      key: 'rag-assistant',
      icon: <QuestionCircleOutlined />,
      label: (
        <MenuItemWithBadge>
          <span className="menu-text">Assistente Lei 14.133</span>
          <Tooltip title={`RAG Assistant: ${getServiceStatus('rag_assistant') === 'active' ? 'Ativo' : 'Inativo'}`}>
            <div className={`status-indicator ${getServiceStatus('rag_assistant')}`} />
          </Tooltip>
        </MenuItemWithBadge>
      ),
      title: 'Consultar documentação da Lei 14.133'
    },
    {
      type: 'divider'
    },
    {
      key: 'config',
      icon: <SettingOutlined />,
      label: (
        <MenuItemWithBadge>
          <span className="menu-text">Configurações</span>
          <Tooltip title={`APIs: ${(apiStatus?.openai_api || apiStatus?.anthropic_api) ? 'Configuradas' : 'Não configuradas'}`}>
            <div className={`status-indicator ${(apiStatus?.openai_api || apiStatus?.anthropic_api) ? 'active' : 'inactive'}`} />
          </Tooltip>
        </MenuItemWithBadge>
      ),
      title: 'Configurar APIs e sistema'
    }
  ];

  const getStatusSummary = () => {
    if (!apiStatus) return { total: 0, active: 0 };
    
    const services = ['openai_api', 'anthropic_api', 'rag_assistant', 'assistente_etp'];
    const active = services.filter(service => apiStatus[service]).length;
    
    return { total: services.length, active };
  };

  const statusSummary = getStatusSummary();

  return (
    <StyledSider 
      collapsible 
      collapsed={collapsed}
      width={280}
      collapsedWidth={80}
    >
      {!collapsed && (
        <SiderHeader>
          <div style={{ marginBottom: 8 }}>
            <Text style={{ color: 'white', fontSize: '14px', fontWeight: 600 }}>
              Status do Sistema
            </Text>
          </div>
          
          <div style={{ display: 'flex', justifyContent: 'center', gap: 16 }}>
            <Tooltip title="APIs Configuradas">
              <div style={{ textAlign: 'center' }}>
                <div style={{ color: '#52c41a', fontSize: '18px' }}>
                  {(apiStatus?.openai_api || apiStatus?.anthropic_api) ? '✅' : '❌'}
                </div>
                <Text style={{ color: 'rgba(255,255,255,0.7)', fontSize: '11px' }}>
                  APIs
                </Text>
              </div>
            </Tooltip>
            
            <Tooltip title="Serviços Ativos">
              <div style={{ textAlign: 'center' }}>
                <div style={{ color: '#1890ff', fontSize: '18px' }}>
                  {statusSummary.active}/{statusSummary.total}
                </div>
                <Text style={{ color: 'rgba(255,255,255,0.7)', fontSize: '11px' }}>
                  Serviços
                </Text>
              </div>
            </Tooltip>
            
            <Tooltip title="Sistema Operacional">
              <div style={{ textAlign: 'center' }}>
                <div style={{ color: statusSummary.active > 0 ? '#52c41a' : '#fa8c16', fontSize: '18px' }}>
                  {statusSummary.active > 0 ? '🟢' : '🟡'}
                </div>
                <Text style={{ color: 'rgba(255,255,255,0.7)', fontSize: '11px' }}>
                  Status
                </Text>
              </div>
            </Tooltip>
          </div>
        </SiderHeader>
      )}

      <Menu
        theme="dark"
        mode="inline"
        selectedKeys={[selectedKey]}
        onClick={({ key }) => onMenuClick(key)}
        items={menuItems}
        style={{ borderRight: 0 }}
      />

      {/* Informações adicionais quando expandido */}
      {!collapsed && (
        <div style={{ 
          position: 'absolute', 
          bottom: 16, 
          left: 16, 
          right: 16,
          padding: 12,
          background: 'rgba(255,255,255,0.05)',
          borderRadius: 6,
          border: '1px solid rgba(255,255,255,0.1)'
        }}>
          <Text style={{ color: 'rgba(255,255,255,0.7)', fontSize: '11px' }}>
            <RobotOutlined /> ETP Generator v2.0
          </Text>
          <br />
          <Text style={{ color: 'rgba(255,255,255,0.5)', fontSize: '10px' }}>
            Sistema Integrado de Documentos
          </Text>
          
          <div style={{ marginTop: 8, display: 'flex', gap: 4 }}>
            <Tooltip title={`OpenAI: ${apiStatus?.openai_api ? 'Ativo' : 'Inativo'}`}>
              <div style={{ 
                width: 6, 
                height: 6, 
                borderRadius: '50%', 
                background: apiStatus?.openai_api ? '#52c41a' : '#d9d9d9' 
              }} />
            </Tooltip>
            
            <Tooltip title={`Anthropic: ${apiStatus?.anthropic_api ? 'Ativo' : 'Inativo'}`}>
              <div style={{ 
                width: 6, 
                height: 6, 
                borderRadius: '50%', 
                background: apiStatus?.anthropic_api ? '#52c41a' : '#d9d9d9' 
              }} />
            </Tooltip>
            
            <Tooltip title={`RAG: ${apiStatus?.rag_assistant ? 'Ativo' : 'Inativo'}`}>
              <div style={{ 
                width: 6, 
                height: 6, 
                borderRadius: '50%', 
                background: apiStatus?.rag_assistant ? '#52c41a' : '#d9d9d9' 
              }} />
            </Tooltip>
            
            <Tooltip title={`ETP IA: ${apiStatus?.assistente_etp ? 'Ativo' : 'Inativo'}`}>
              <div style={{ 
                width: 6, 
                height: 6, 
                borderRadius: '50%', 
                background: apiStatus?.assistente_etp ? '#52c41a' : '#d9d9d9' 
              }} />
            </Tooltip>
          </div>
        </div>
      )}
    </StyledSider>
  );
};

export default Sidebar;