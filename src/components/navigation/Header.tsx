import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';
import { Menu, Scale, FileText, MessageCircle, Book } from 'lucide-react';

interface HeaderProps {
  activeSection: string;
  onSectionChange: (section: string) => void;
}

const Header = ({ activeSection, onSectionChange }: HeaderProps) => {
  const [isOpen, setIsOpen] = useState(false);

  const menuItems = [
    {
      id: 'chat',
      title: 'Chat IA',
      icon: MessageCircle,
      description: 'Tire dúvidas sobre licitações'
    },
    {
      id: 'etp',
      title: 'Gerador ETP',
      icon: FileText,
      description: 'Crie estudos técnicos preliminares'
    },
    {
      id: 'guia',
      title: 'Guia Legal',
      icon: Book,
      description: 'Consulte a legislação'
    }
  ];

  const handleMenuClick = (sectionId: string) => {
    onSectionChange(sectionId);
    setIsOpen(false);
  };

  return (
    <header className="bg-gradient-hero shadow-elegant sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-white/20 rounded-lg">
              <Scale className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">Licita Amiga IA</h1>
              <p className="text-white/80 text-sm">Assistente Inteligente para Servidores Públicos</p>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-2">
            {menuItems.map((item) => {
              const Icon = item.icon;
              return (
                <Button
                  key={item.id}
                  variant={activeSection === item.id ? 'secondary' : 'ghost'}
                  onClick={() => onSectionChange(item.id)}
                  className={`text-white hover:bg-white/20 ${
                    activeSection === item.id ? 'bg-white/25' : ''
                  }`}
                >
                  <Icon className="h-4 w-4 mr-2" />
                  {item.title}
                </Button>
              );
            })}
          </nav>

          {/* Mobile Navigation */}
          <Sheet open={isOpen} onOpenChange={setIsOpen}>
            <SheetTrigger asChild>
              <Button variant="ghost" size="icon" className="md:hidden text-white hover:bg-white/20">
                <Menu className="h-5 w-5" />
              </Button>
            </SheetTrigger>
            <SheetContent side="right" className="w-80">
              <div className="py-6">
                <div className="flex items-center gap-3 mb-8">
                  <div className="p-2 bg-gradient-primary rounded-lg">
                    <Scale className="h-5 w-5 text-white" />
                  </div>
                  <div>
                    <h2 className="font-semibold">Licita Amiga IA</h2>
                    <p className="text-sm text-muted-foreground">Menu de navegação</p>
                  </div>
                </div>

                <nav className="space-y-2">
                  {menuItems.map((item) => {
                    const Icon = item.icon;
                    return (
                      <Button
                        key={item.id}
                        variant={activeSection === item.id ? 'secondary' : 'ghost'}
                        onClick={() => handleMenuClick(item.id)}
                        className="w-full justify-start h-auto p-4"
                      >
                        <div className="flex items-start gap-3">
                          <Icon className="h-5 w-5 mt-0.5 shrink-0" />
                          <div className="text-left">
                            <div className="font-medium">{item.title}</div>
                            <div className="text-sm text-muted-foreground">{item.description}</div>
                          </div>
                        </div>
                      </Button>
                    );
                  })}
                </nav>
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  );
};

export default Header;