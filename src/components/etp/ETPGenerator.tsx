import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Checkbox } from '@/components/ui/checkbox';
import { FileText, Download, Eye, FileDown } from 'lucide-react';
import { useToast } from '@/components/ui/use-toast';
import { PDFViewer, PDFDownloadLink } from '@react-pdf/renderer';
import ETPPDFDocument from './ETPPDFDocument';

interface ETPFormData {
  objeto: string;
  justificativa: string;
  modalidade: string;
  valorEstimado: string;
  prazoExecucao: string;
  localExecucao: string;
  especificacoesTecnicas: string;
  criterioJulgamento: string;
  documentacaoNecessaria: string[];
  observacoes: string;
}

const ETPGenerator = () => {
  const [formData, setFormData] = useState<ETPFormData>({
    objeto: '',
    justificativa: '',
    modalidade: '',
    valorEstimado: '',
    prazoExecucao: '',
    localExecucao: '',
    especificacoesTecnicas: '',
    criterioJulgamento: '',
    documentacaoNecessaria: [],
    observacoes: ''
  });
  const { toast } = useToast();

  const modalidades = [
    { value: 'pregao', label: 'Pregão (Presencial/Eletrônico)' },
    { value: 'concorrencia', label: 'Concorrência' },
    { value: 'tomada-precos', label: 'Tomada de Preços' },
    { value: 'convite', label: 'Convite' },
    { value: 'concurso', label: 'Concurso' },
    { value: 'leilao', label: 'Leilão' },
    { value: 'rdc', label: 'RDC - Regime Diferenciado de Contratações' },
    { value: 'dialogo-competitivo', label: 'Diálogo Competitivo' }
  ];

  const criteriosJulgamento = [
    { value: 'menor-preco', label: 'Menor Preço' },
    { value: 'melhor-tecnica', label: 'Melhor Técnica' },
    { value: 'tecnica-preco', label: 'Técnica e Preço' },
    { value: 'maior-lance', label: 'Maior Lance' },
    { value: 'melhor-conteudo', label: 'Melhor Conteúdo Artístico' }
  ];

  const documentacoes = [
    'Projeto Básico',
    'Projeto Executivo',
    'Orçamento Detalhado',
    'Cronograma Físico-Financeiro',
    'Memorial Descritivo',
    'Especificações Técnicas',
    'Planilha de Quantitativos',
    'Estudo de Viabilidade',
    'Licenças Ambientais',
    'Certidões e Alvarás'
  ];

  const handleInputChange = (field: keyof ETPFormData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleDocumentacaoChange = (doc: string, checked: boolean) => {
    setFormData(prev => ({
      ...prev,
      documentacaoNecessaria: checked
        ? [...prev.documentacaoNecessaria, doc]
        : prev.documentacaoNecessaria.filter(d => d !== doc)
    }));
  };

  const hasMinimumData = formData.objeto && formData.justificativa && formData.modalidade;

  const fileName = `ETP_${formData.objeto.substring(0, 20).replace(/[^a-zA-Z0-9]/g, '_')}_${new Date().toISOString().split('T')[0]}.pdf`;

  return (
    <div className="space-y-6">
      <Card className="shadow-elegant border-0 bg-gradient-subtle">
        <CardHeader className="bg-gradient-secondary text-white rounded-t-lg">
          <CardTitle className="flex items-center gap-2">
            <FileText className="h-5 w-5" />
            Gerador de ETP - Estudo Técnico Preliminar
          </CardTitle>
          <CardDescription className="text-white/80">
            Preencha as informações para gerar automaticamente seu Estudo Técnico Preliminar
          </CardDescription>
        </CardHeader>
        <CardContent className="p-6 space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <div>
                <Label htmlFor="objeto" className="text-sm font-medium">
                  Objeto da Licitação *
                </Label>
                <Textarea
                  id="objeto"
                  placeholder="Descreva o objeto da licitação (ex: Contratação de empresa para prestação de serviços de limpeza e conservação...)"
                  value={formData.objeto}
                  onChange={(e) => handleInputChange('objeto', e.target.value)}
                  className="mt-1"
                  rows={3}
                />
              </div>

              <div>
                <Label htmlFor="justificativa" className="text-sm font-medium">
                  Justificativa *
                </Label>
                <Textarea
                  id="justificativa"
                  placeholder="Justifique a necessidade da contratação..."
                  value={formData.justificativa}
                  onChange={(e) => handleInputChange('justificativa', e.target.value)}
                  className="mt-1"
                  rows={4}
                />
              </div>

              <div>
                <Label htmlFor="modalidade" className="text-sm font-medium">
                  Modalidade de Licitação *
                </Label>
                <Select value={formData.modalidade} onValueChange={(value) => handleInputChange('modalidade', value)}>
                  <SelectTrigger className="mt-1">
                    <SelectValue placeholder="Selecione a modalidade" />
                  </SelectTrigger>
                  <SelectContent>
                    {modalidades.map((modalidade) => (
                      <SelectItem key={modalidade.value} value={modalidade.value}>
                        {modalidade.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="criterio" className="text-sm font-medium">
                  Critério de Julgamento
                </Label>
                <Select value={formData.criterioJulgamento} onValueChange={(value) => handleInputChange('criterioJulgamento', value)}>
                  <SelectTrigger className="mt-1">
                    <SelectValue placeholder="Selecione o critério" />
                  </SelectTrigger>
                  <SelectContent>
                    {criteriosJulgamento.map((criterio) => (
                      <SelectItem key={criterio.value} value={criterio.value}>
                        {criterio.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="space-y-4">
              <div>
                <Label htmlFor="valor" className="text-sm font-medium">
                  Valor Estimado (R$)
                </Label>
                <Input
                  id="valor"
                  type="text"
                  placeholder="Ex: 150.000,00"
                  value={formData.valorEstimado}
                  onChange={(e) => handleInputChange('valorEstimado', e.target.value)}
                  className="mt-1"
                />
              </div>

              <div>
                <Label htmlFor="prazo" className="text-sm font-medium">
                  Prazo de Execução
                </Label>
                <Input
                  id="prazo"
                  placeholder="Ex: 12 meses"
                  value={formData.prazoExecucao}
                  onChange={(e) => handleInputChange('prazoExecucao', e.target.value)}
                  className="mt-1"
                />
              </div>

              <div>
                <Label htmlFor="local" className="text-sm font-medium">
                  Local de Execução
                </Label>
                <Input
                  id="local"
                  placeholder="Ex: Sede do órgão"
                  value={formData.localExecucao}
                  onChange={(e) => handleInputChange('localExecucao', e.target.value)}
                  className="mt-1"
                />
              </div>

              <div>
                <Label htmlFor="especificacoes" className="text-sm font-medium">
                  Especificações Técnicas
                </Label>
                <Textarea
                  id="especificacoes"
                  placeholder="Descreva as especificações técnicas necessárias..."
                  value={formData.especificacoesTecnicas}
                  onChange={(e) => handleInputChange('especificacoesTecnicas', e.target.value)}
                  className="mt-1"
                  rows={3}
                />
              </div>
            </div>
          </div>

          <div>
            <Label className="text-sm font-medium mb-3 block">
              Documentação Necessária
            </Label>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {documentacoes.map((doc) => (
                <div key={doc} className="flex items-center space-x-2">
                  <Checkbox
                    id={doc}
                    checked={formData.documentacaoNecessaria.includes(doc)}
                    onCheckedChange={(checked) => handleDocumentacaoChange(doc, checked as boolean)}
                  />
                  <Label htmlFor={doc} className="text-sm">
                    {doc}
                  </Label>
                </div>
              ))}
            </div>
          </div>

          <div>
            <Label htmlFor="observacoes" className="text-sm font-medium">
              Observações Gerais
            </Label>
            <Textarea
              id="observacoes"
              placeholder="Adicione observações relevantes para o processo licitatório..."
              value={formData.observacoes}
              onChange={(e) => handleInputChange('observacoes', e.target.value)}
              className="mt-1"
              rows={3}
            />
          </div>

          <div className="flex gap-3 pt-4">
            {hasMinimumData && (
              <PDFDownloadLink
                document={
                  <ETPPDFDocument 
                    formData={formData} 
                    modalidades={modalidades}
                    criteriosJulgamento={criteriosJulgamento}
                  />
                }
                fileName={fileName}
                className="flex-1"
              >
                {({ loading }) => (
                  <Button
                    disabled={loading}
                    variant="institutional"
                    className="w-full"
                  >
                    {loading ? (
                      <>
                        <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                        Preparando PDF...
                      </>
                    ) : (
                      <>
                        <FileDown className="h-4 w-4 mr-2" />
                        Baixar ETP (PDF)
                      </>
                    )}
                  </Button>
                )}
              </PDFDownloadLink>
            )}
          </div>
        </CardContent>
      </Card>

      {hasMinimumData && (
        <Card className="shadow-elegant border-0">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Eye className="h-5 w-5" />
              Pré-visualização do ETP em Tempo Real
            </CardTitle>
            <CardDescription>
              O documento é atualizado automaticamente conforme você preenche os campos
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[600px] border rounded-lg overflow-hidden">
              <PDFViewer 
                width="100%" 
                height="100%"
                showToolbar={false}
              >
                <ETPPDFDocument 
                  formData={formData} 
                  modalidades={modalidades}
                  criteriosJulgamento={criteriosJulgamento}
                />
              </PDFViewer>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default ETPGenerator;