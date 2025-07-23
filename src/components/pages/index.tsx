import { useState } from 'react';
import Header from '@/components/navigation/Header';
import ChatInterface from '@/components/chat/ChatInterface';
import ETPGenerator from '@/components/etp/ETPGenerator';
import LegalGuide from '@/components/guide/LegalGuide';

const Index = () => {
  const [activeSection, setActiveSection] = useState('chat');

  const renderContent = () => {
    switch (activeSection) {
      case 'chat':
        return <ChatInterface />;
      case 'etp':
        return <ETPGenerator />;
      case 'guia':
        return <LegalGuide />;
      default:
        return <ChatInterface />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-subtle">
      <Header activeSection={activeSection} onSectionChange={setActiveSection} />
      <main className="container mx-auto px-4 py-8">
        {renderContent()}
      </main>
    </div>
  );
};

export default Index;
