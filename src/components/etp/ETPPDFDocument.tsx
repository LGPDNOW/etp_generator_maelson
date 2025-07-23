import { Document, Page, Text, View, StyleSheet, Font } from '@react-pdf/renderer';

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

interface ETPPDFDocumentProps {
  formData: ETPFormData;
  modalidades: Array<{ value: string; label: string }>;
  criteriosJulgamento: Array<{ value: string; label: string }>;
}

const styles = StyleSheet.create({
  page: {
    flexDirection: 'column',
    backgroundColor: '#ffffff',
    padding: 30,
    fontSize: 12,
    fontFamily: 'Helvetica',
  },
  header: {
    textAlign: 'center',
    marginBottom: 30,
    paddingBottom: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#000000',
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 12,
    color: '#666666',
  },
  section: {
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    marginBottom: 8,
    color: '#1a472a',
  },
  content: {
    fontSize: 11,
    lineHeight: 1.5,
    textAlign: 'justify',
  },
  listItem: {
    fontSize: 11,
    marginBottom: 3,
    paddingLeft: 10,
  },
  footer: {
    position: 'absolute',
    bottom: 30,
    left: 30,
    right: 30,
    textAlign: 'center',
    fontSize: 10,
    color: '#666666',
    borderTopWidth: 1,
    borderTopColor: '#cccccc',
    paddingTop: 10,
  },
  signature: {
    marginTop: 40,
    textAlign: 'center',
  },
  signatureLine: {
    borderBottomWidth: 1,
    borderBottomColor: '#000000',
    width: 200,
    marginHorizontal: 'auto',
    marginBottom: 5,
  },
  placeholder: {
    color: '#999999',
    fontStyle: 'italic',
  },
});

const ETPPDFDocument: React.FC<ETPPDFDocumentProps> = ({ 
  formData, 
  modalidades, 
  criteriosJulgamento 
}) => {
  const getModalidadeLabel = (value: string) => {
    return modalidades.find(m => m.value === value)?.label || value;
  };

  const getCriterioLabel = (value: string) => {
    return criteriosJulgamento.find(c => c.value === value)?.label || value;
  };

  const currentDate = new Date().toLocaleDateString('pt-BR');

  return (
    <Document>
      <Page size="A4" style={styles.page}>
        <View style={styles.header}>
          <Text style={styles.title}>ESTUDO TÉCNICO PRELIMINAR (ETP)</Text>
          <Text style={styles.subtitle}>
            Documento gerado pela Licita Amiga IA em {currentDate}
          </Text>
        </View>

        {formData.objeto && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>1. OBJETO</Text>
            <Text style={styles.content}>{formData.objeto}</Text>
          </View>
        )}

        {formData.justificativa && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>2. JUSTIFICATIVA</Text>
            <Text style={styles.content}>{formData.justificativa}</Text>
          </View>
        )}

        {formData.modalidade && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>3. MODALIDADE DE LICITAÇÃO</Text>
            <Text style={styles.content}>{getModalidadeLabel(formData.modalidade)}</Text>
          </View>
        )}

        {formData.valorEstimado && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>4. VALOR ESTIMADO</Text>
            <Text style={styles.content}>R$ {formData.valorEstimado}</Text>
          </View>
        )}

        {formData.prazoExecucao && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>5. PRAZO DE EXECUÇÃO</Text>
            <Text style={styles.content}>{formData.prazoExecucao}</Text>
          </View>
        )}

        {formData.localExecucao && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>6. LOCAL DE EXECUÇÃO</Text>
            <Text style={styles.content}>{formData.localExecucao}</Text>
          </View>
        )}

        {formData.especificacoesTecnicas && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>7. ESPECIFICAÇÕES TÉCNICAS</Text>
            <Text style={styles.content}>{formData.especificacoesTecnicas}</Text>
          </View>
        )}

        {formData.criterioJulgamento && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>8. CRITÉRIO DE JULGAMENTO</Text>
            <Text style={styles.content}>{getCriterioLabel(formData.criterioJulgamento)}</Text>
          </View>
        )}

        {formData.documentacaoNecessaria.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>9. DOCUMENTAÇÃO NECESSÁRIA</Text>
            {formData.documentacaoNecessaria.map((doc, index) => (
              <Text key={index} style={styles.listItem}>• {doc}</Text>
            ))}
          </View>
        )}

        {formData.observacoes && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>10. OBSERVAÇÕES GERAIS</Text>
            <Text style={styles.content}>{formData.observacoes}</Text>
          </View>
        )}

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>11. RESPONSÁVEL TÉCNICO</Text>
          <Text style={[styles.content, styles.placeholder]}>
            Nome: [A ser preenchido]
          </Text>
          <Text style={[styles.content, styles.placeholder]}>
            Cargo: [A ser preenchido]
          </Text>
          <Text style={[styles.content, styles.placeholder]}>
            Matrícula: [A ser preenchido]
          </Text>
        </View>

        <View style={styles.signature}>
          <Text style={styles.content}>Data: {currentDate}</Text>
          <View style={styles.signatureLine} />
          <Text style={styles.content}>Assinatura do Responsável</Text>
        </View>

        <View style={styles.footer}>
          <Text>
            Este documento foi gerado automaticamente pela Licita Amiga IA
          </Text>
          <Text>
            Verifique todas as informações antes da utilização oficial
          </Text>
        </View>
      </Page>
    </Document>
  );
};

export default ETPPDFDocument;