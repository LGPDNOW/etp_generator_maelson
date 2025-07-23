import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Book, Search, ExternalLink, Calendar, Tag } from 'lucide-react';

const LegalGuide = () => {
  const [searchTerm, setSearchTerm] = useState('');

  const legislacoes = [
    {
      id: 1,
      titulo: 'Lei 14.133/2021',
      subtitulo: 'Nova Lei de Licitações e Contratos',
      categoria: 'lei',
      ano: '2021',
      status: 'vigente',
      resumo: 'Nova lei geral de licitações e contratos administrativos que substitui as Leis 8.666/93, 10.520/02 e outras.',
      topicos: [
        'Modalidades de licitação',
        'Procedimentos licitatórios',
        'Contratos administrativos',
        'Governança e gestão de riscos'
      ],
      link: 'https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/L14133.htm'
    },
    {
      id: 2,
      titulo: 'Lei 8.666/93',
      subtitulo: 'Lei de Licitações (Revogada)',
      categoria: 'lei',
      ano: '1993',
      status: 'revogada',
      resumo: 'Antiga lei que regulamentava licitações e contratos da administração pública, revogada pela Lei 14.133/21.',
      topicos: [
        'Modalidades tradicionais',
        'Documentação de habilitação',
        'Contratos administrativos',
        'Sanções administrativas'
      ],
      link: 'https://www.planalto.gov.br/ccivil_03/leis/l8666cons.htm'
    },
    {
      id: 3,
      titulo: 'Decreto 10.024/19',
      subtitulo: 'Pregão Eletrônico',
      categoria: 'decreto',
      ano: '2019',
      status: 'vigente',
      resumo: 'Regulamenta a modalidade de pregão na forma eletrônica para aquisição de bens e contratação de serviços comuns.',
      topicos: [
        'Pregão eletrônico',
        'Sistema eletrônico de licitações',
        'Procedimentos do pregão',
        'Recursos e impugnações'
      ],
      link: 'https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2019/decreto/D10024.htm'
    },
    {
      id: 4,
      titulo: 'Lei 12.462/11',
      subtitulo: 'Regime Diferenciado de Contratações - RDC',
      categoria: 'lei',
      ano: '2011',
      status: 'vigente',
      resumo: 'Institui o Regime Diferenciado de Contratações Públicas aplicável aos Jogos Olímpicos, Copa do Mundo, obras do PAC e outras situações.',
      topicos: [
        'RDC aplicações',
        'Procedimentos diferenciados',
        'Contratação integrada',
        'Remuneração variável'
      ],
      link: 'https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/Lei/L12462.htm'
    }
  ];

  const modalidades = [
    {
      nome: 'Pregão',
      valorLimite: 'Sem limite',
      aplicacao: 'Bens e serviços comuns',
      prazoMinimo: '8 dias úteis',
      descricao: 'Modalidade para aquisição de bens e serviços comuns, independentemente do valor.'
    },
    {
      nome: 'Concorrência',
      valorLimite: 'Acima de R$ 3.300.000 (obras) / R$ 1.430.000 (outros)',
      aplicacao: 'Obras, serviços e compras de grande vulto',
      prazoMinimo: '30 dias',
      descricao: 'Modalidade para contratações de grande valor ou alta complexidade.'
    },
    {
      nome: 'Tomada de Preços',
      valorLimite: 'R$ 330.000 a R$ 3.300.000 (obras) / R$ 176.000 a R$ 1.430.000 (outros)',
      aplicacao: 'Obras, serviços e compras de médio porte',
      prazoMinimo: '15 dias',
      descricao: 'Modalidade intermediária entre convite e concorrência.'
    },
    {
      nome: 'Convite',
      valorLimite: 'Até R$ 330.000 (obras) / R$ 176.000 (outros)',
      aplicacao: 'Obras, serviços e compras de pequeno valor',
      prazoMinimo: '5 dias úteis',
      descricao: 'Modalidade para contratações de menor complexidade e valor.'
    }
  ];

  const filteredLegislacoes = legislacoes.filter(lei =>
    lei.titulo.toLowerCase().includes(searchTerm.toLowerCase()) ||
    lei.subtitulo.toLowerCase().includes(searchTerm.toLowerCase()) ||
    lei.topicos.some(topico => topico.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  const getStatusBadge = (status: string) => {
    const variants: Record<string, "default" | "secondary" | "destructive" | "outline"> = {
      vigente: 'default',
      revogada: 'destructive',
      alterada: 'secondary'
    };
    
    return (
      <Badge variant={variants[status] || 'outline'}>
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </Badge>
    );
  };

  const getCategoriaColor = (categoria: string) => {
    const colors: Record<string, string> = {
      lei: 'bg-primary',
      decreto: 'bg-secondary',
      instrucao: 'bg-accent'
    };
    return colors[categoria] || 'bg-muted';
  };

  return (
    <div className="space-y-6">
      <Card className="shadow-elegant border-0 bg-gradient-subtle">
        <CardHeader className="bg-gradient-secondary text-white rounded-t-lg">
          <CardTitle className="flex items-center gap-2">
            <Book className="h-5 w-5" />
            Guia Legal - Licitações e Contratos
          </CardTitle>
          <CardDescription className="text-white/80">
            Consulte a legislação, modalidades e orientações sobre licitações públicas
          </CardDescription>
        </CardHeader>
      </Card>

      <Tabs defaultValue="legislacao" className="space-y-6">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="legislacao">Legislação</TabsTrigger>
          <TabsTrigger value="modalidades">Modalidades</TabsTrigger>
        </TabsList>

        <TabsContent value="legislacao" className="space-y-4">
          <div className="flex gap-2">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Buscar na legislação..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-9"
              />
            </div>
          </div>

          <div className="grid gap-4">
            {filteredLegislacoes.map((lei) => (
              <Card key={lei.id} className="hover:shadow-lg transition-smooth border">
                <CardHeader className="pb-3">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <div className={`w-3 h-3 rounded-full ${getCategoriaColor(lei.categoria)}`} />
                        <CardTitle className="text-lg">{lei.titulo}</CardTitle>
                        {getStatusBadge(lei.status)}
                      </div>
                      <CardDescription className="text-base">{lei.subtitulo}</CardDescription>
                    </div>
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                      <Calendar className="h-4 w-4" />
                      {lei.ano}
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <p className="text-sm text-muted-foreground">{lei.resumo}</p>
                  
                  <div>
                    <h4 className="text-sm font-medium mb-2 flex items-center gap-2">
                      <Tag className="h-4 w-4" />
                      Tópicos principais:
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {lei.topicos.map((topico, index) => (
                        <Badge key={index} variant="outline" className="text-xs">
                          {topico}
                        </Badge>
                      ))}
                    </div>
                  </div>

                  <div className="pt-2 border-t">
                    <Button variant="outline" size="sm" asChild>
                      <a href={lei.link} target="_blank" rel="noopener noreferrer">
                        <ExternalLink className="h-4 w-4 mr-2" />
                        Ver texto completo
                      </a>
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="modalidades" className="space-y-4">
          <div className="grid gap-4">
            {modalidades.map((modalidade, index) => (
              <Card key={index} className="hover:shadow-lg transition-smooth border">
                <CardHeader>
                  <CardTitle className="text-lg text-primary">{modalidade.nome}</CardTitle>
                  <CardDescription>{modalidade.descricao}</CardDescription>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                    <div>
                      <span className="font-medium text-muted-foreground">Valor limite:</span>
                      <p className="text-foreground">{modalidade.valorLimite}</p>
                    </div>
                    <div>
                      <span className="font-medium text-muted-foreground">Aplicação:</span>
                      <p className="text-foreground">{modalidade.aplicacao}</p>
                    </div>
                    <div>
                      <span className="font-medium text-muted-foreground">Prazo mínimo:</span>
                      <p className="text-foreground">{modalidade.prazoMinimo}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default LegalGuide;