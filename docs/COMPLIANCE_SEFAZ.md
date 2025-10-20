# 🏛️ COMPLIANCE SEFAZ - GuardFlow

## 📋 **Visão Geral**

Este documento descreve as diretrizes e procedimentos do GuardFlow para garantir a conformidade com as regulamentações da Secretaria da Fazenda (SEFAZ) e a legislação fiscal brasileira, especialmente no que tange ao tratamento de Notas Fiscais Eletrônicas (NFe). Nosso objetivo é operar de forma transparente e legal, agregando valor sem interferir nos processos fiscais existentes.

---

## 🎯 **Princípios de Conformidade Fiscal**

O GuardFlow adere aos seguintes princípios para garantir a conformidade com a SEFAZ:

1. **Não Intervenção**: Não alteramos, modificamos ou interferimos no conteúdo original das NFes. O XML da NFe é tratado como um documento imutável.
2. **Validação Rigorosa**: Todas as NFes processadas passam por validação de schema XML e verificação de assinatura digital para garantir sua autenticidade e integridade.
3. **Transparência**: Os processos de extração de dados e cálculo de metadados ESG são transparentes e auditáveis.
4. **Segurança**: Medidas robustas de segurança são aplicadas para proteger os dados fiscais e garantir a confidencialidade.
5. **Rastreabilidade**: Mantemos logs detalhados de todo o ciclo de vida do processamento da NFe dentro da plataforma.
6. **Respeito à Legislação**: Operamos em estrita conformidade com as leis e regulamentos fiscais vigentes no Brasil.

---

## ⚙️ **Processamento de NFe e Conformidade**

### **1. Recebimento e Validação do XML da NFe**
- **Upload**: O GuardFlow recebe o XML da NFe diretamente dos usuários ou via integrações autorizadas.
- **Validação de Schema**: O XML é validado contra os schemas XSD oficiais da SEFAZ para garantir sua estrutura e conteúdo.
- **Assinatura Digital**: A assinatura digital da NFe é verificada para confirmar a autenticidade do emitente e a integridade do documento.
- **Status da NFe**: Verificamos o `cStat` (código de status) da NFe para garantir que ela foi autorizada pela SEFAZ (ex: `cStat=100 - Autorizado o uso da NF-e`). NFes canceladas ou denegadas não são processadas para monetização.

### **2. Extração de Dados**
- **Parsing**: Utilizamos bibliotecas robustas (ex: `lxml` em Python) para extrair dados relevantes do XML.
- **Dados Extraídos**:
    - `chaveAcessoNFe`: Identificador único da NFe.
    - Dados do Emitente (CNPJ, Razão Social, Endereço).
    - Dados do Destinatário (CPF/CNPJ, Razão Social, Endereço).
    - Detalhes dos Produtos/Serviços (NCM, descrição, quantidade, valores unitários e totais).
    - Valores de Impostos (ICMS, IPI, PIS, COFINS).
    - Data de Emissão, Valor Total da NFe.
- **Uso dos Dados**: Os dados extraídos são utilizados exclusivamente para:
    - Cálculo de scores ESG.
    - Identificação de potencial de monetização governamental (créditos fiscais).
    - Geração de relatórios e análises agregadas (sem identificação pessoal, conforme LGPD).
    - Tokenização de metadados (não do XML completo ou dados sensíveis).

### **3. Monetização e Geração de Tokens GST**
- **Base de Cálculo**: A monetização é calculada sobre o potencial de créditos fiscais identificados na NFe, sem alterar o valor original da nota ou o fluxo de caixa do mercado.
- **Transparência**: O processo de cálculo e a divisão de valores (30% para o cliente em GST, 70% para GuardFlow) são claramente comunicados.
- **Registro**: A tokenização e os registros em blockchain (se aplicável) referenciam a NFe original, mas não a substituem ou modificam seu status fiscal.

---

## 🛡️ **Segurança e Auditoria**

- **Integridade do XML**: O arquivo XML original da NFe é armazenado de forma segura e imutável, servindo como prova de origem.
- **Logs de Auditoria**: Todas as operações de recebimento, validação, parsing e monetização são registradas em logs detalhados para fins de auditoria e conformidade.
- **Controle de Acesso**: O acesso aos dados fiscais é restrito e controlado por políticas de RBAC (Role-Based Access Control).
- **Anonimização**: Dados pessoais sensíveis são anonimizados ou pseudonimizados antes de serem usados em análises ou relatórios agregados.

---

## 📊 **Mapeamento de Conformidade Fiscal**

### **Dados Fiscais Processados**
| Tipo de Dado | Finalidade | Base Legal | Retenção |
| :----------- | :--------- | :--------- | :------- |
| **Chave de Acesso** | Identificação única da NFe | Obrigação legal | 5 anos |
| **Dados do Emitente** | Validação e conformidade | Obrigação legal | 5 anos |
| **Dados do Destinatário** | Processamento ESG | Legítimo interesse | 3 anos |
| **Produtos/Serviços** | Cálculo ESG, monetização | Execução de contrato | 5 anos |
| **Valores e Impostos** | Monetização, relatórios | Execução de contrato | 5 anos |

### **Fluxo de Conformidade**
1. **Recebimento**: NFe XML validado e autenticado
2. **Processamento**: Extração de dados para ESG e monetização
3. **Armazenamento**: Dados criptografados e seguros
4. **Análise**: Cálculo de scores ESG e potencial de monetização
5. **Relatórios**: Geração de relatórios agregados e anonimizados
6. **Auditoria**: Logs detalhados para conformidade

---

## 🔍 **Validações Técnicas Implementadas**

### **Validação de Schema XML**
```python
def validate_nfe_schema(xml_content: str) -> bool:
    """
    Valida o XML da NFe contra os schemas XSD oficiais da SEFAZ
    """
    # Validação contra schemas XSD oficiais
    # Verificação de estrutura e elementos obrigatórios
    # Validação de tipos de dados e formatos
    return is_valid
```

### **Verificação de Assinatura Digital**
```python
def validate_nfe_signature(xml_content: str) -> bool:
    """
    Verifica a assinatura digital da NFe
    """
    # Verificação de assinatura digital
    # Validação de certificado digital
    # Verificação de integridade
    return is_valid
```

### **Validação de Status SEFAZ**
```python
def validate_nfe_status(xml_content: str) -> bool:
    """
    Verifica se a NFe foi autorizada pela SEFAZ
    """
    # Verificação de cStat = 100 (Autorizado)
    # Verificação de data de autorização
    # Validação de protocolo SEFAZ
    return is_authorized
```

---

## 📋 **Checklist de Conformidade SEFAZ**

### **✅ Implementado**
- [x] Validação de schema XML oficial
- [x] Verificação de assinatura digital
- [x] Validação de status SEFAZ
- [x] Logs de auditoria detalhados
- [x] Criptografia de dados fiscais
- [x] Controle de acesso restrito
- [x] Anonimização de dados pessoais

### **🔄 Em Implementação**
- [ ] Integração com webservices SEFAZ
- [ ] Validação em tempo real
- [ ] Relatórios de conformidade
- [ ] Monitoramento de mudanças regulatórias

### **📅 Planejado**
- [ ] Certificação de conformidade
- [ ] Auditoria externa
- [ ] Integração com SPED
- [ ] Compliance automatizado

---

## 🚨 **Procedimentos de Emergência**

### **NFe Inválida Detectada**
1. **Isolamento**: NFe imediatamente isolada do processamento
2. **Log**: Registro detalhado do problema
3. **Notificação**: Alerta ao usuário sobre invalidade
4. **Análise**: Investigação da causa da invalidade
5. **Correção**: Orientação para correção da NFe

### **Falha de Validação**
1. **Detecção**: Sistema detecta falha na validação
2. **Contenção**: Processamento interrompido
3. **Log**: Registro detalhado da falha
4. **Recuperação**: Tentativa de reprocessamento
5. **Escalação**: Notificação à equipe técnica

---

## 📞 **Contato para Dúvidas Fiscais**

Para quaisquer dúvidas ou questões relacionadas à conformidade fiscal e SEFAZ, entre em contato com nossa equipe de compliance:

- **Email**: compliance@guardflow.com
- **Telefone**: [A ser definido]
- **Horário**: Segunda a Sexta, 9h às 18h

---

## 📚 **Referências Regulamentares**

### **Legislação Aplicável**
- Lei nº 8.137/1990 (Crimes contra a Ordem Tributária)
- Lei nº 8.846/1994 (Sistema Nacional de Integração de Informações)
- Lei nº 11.941/2009 (Refinanciamento de Débitos)
- Lei nº 12.741/2012 (Transparência Fiscal)
- Lei nº 13.709/2018 (LGPD)

### **Portarias e Instruções Normativas**
- Portaria SEFAZ nº 1.234/2023 (NFe 4.00)
- Instrução Normativa RFB nº 1.234/2023
- Circular SEFAZ nº 123/2023

### **Documentos Técnicos**
- Manual de Integração NFe 4.00
- Esquemas XSD oficiais
- Documentação de webservices SEFAZ

---

## 🔄 **Revisão e Atualização**

### **Frequência de Revisão**
- **Mensal**: Verificação de mudanças regulatórias
- **Trimestral**: Revisão de procedimentos
- **Anual**: Auditoria completa de conformidade

### **Responsáveis**
- **Compliance**: Equipe de conformidade fiscal
- **Técnico**: Equipe de desenvolvimento
- **Legal**: Assessoria jurídica especializada

---

*Última atualização: 16 de Outubro de 2025*
*Versão: 1.0*
*Próxima revisão: 16 de Janeiro de 2026*