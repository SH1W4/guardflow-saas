# ❓ FAQ - QR Checkout GuardFlow

**Perguntas Frequentes Técnicas e Comerciais**  
**Versão**: 1.0 | **Data**: 20/10/2025

---

## 🏢 **PERGUNTAS COMERCIAIS**

### **💰 Modelo de Preços**

**Q: Como funciona o modelo de preços?**
A: Modelo híbrido SaaS + Taxa de Sucesso:
- **Mensalidade fixa**: Cobertura de infraestrutura e suporte
- **Taxa por transação**: 2-5% dependendo do plano
- **ROI garantido**: Se não economizar, devolvemos o investimento

**Q: Qual o investimento inicial?**
A: 
- **Setup**: R$ 15.000 (hardware + instalação)
- **Mensalidade**: R$ 2.000 - R$ 10.000 (conforme plano)
- **Taxa**: 2-5% por transação processada
- **ROI**: 100-300% em 6-12 meses

**Q: Há taxa de cancelamento?**
A: Não. Contrato mensal com 30 dias de aviso prévio. Acreditamos na qualidade do serviço para retenção.

### **📊 ROI e Benefícios**

**Q: Como vocês garantem ROI de 158% ao mês?**
A: Baseado em 3 pilares mensuráveis:
1. **Redução de custos**: -30% funcionários caixa
2. **Aumento de vendas**: +700% conversão comprovada
3. **Redução de perdas**: -85% abandono de carrinho

**Q: Em quanto tempo vejo resultados?**
A: 
- **Semana 1**: Redução de filas visível
- **Semana 2**: Aumento de conversão mensurável  
- **Mês 1**: ROI positivo comprovado
- **Mês 3**: ROI de 100%+ consolidado

**Q: E se minha loja for muito pequena?**
A: Temos plano Starter para lojas com 1.000+ transações/mês. ROI ainda é positivo devido à eficiência operacional.

### **🤝 Implementação**

**Q: Quanto tempo para implementar?**
A:
- **Análise e planejamento**: 1-2 semanas
- **Instalação técnica**: 2-3 semanas
- **Treinamento e testes**: 1-2 semanas
- **Go-live**: 4-7 semanas total

**Q: Preciso parar a operação?**
A: Não. Implementação paralela com migração gradual. Zero downtime operacional.

**Q: Funciona com meu ERP atual?**
A: Sim. Integramos com 95% dos ERPs do mercado via API REST. Casos especiais têm desenvolvimento customizado incluso.

---

## 🔧 **PERGUNTAS TÉCNICAS**

### **⚖️ Validação por Peso**

**Q: Como funciona a validação por peso?**
A: Sistema híbrido:
- **Balança no carrinho**: Peso em tempo real
- **Balança no pórtico**: Validação final
- **IA preditiva**: Aprende padrões de peso por produto
- **Tolerância adaptativa**: 5-15% conforme contexto

**Q: E produtos a granel (frutas, carnes)?**
A: 
- **Integração com balança PLU**: Peso exato na origem
- **Códigos específicos**: Cada pesagem gera SKU único
- **Validação cruzada**: Peso esperado vs. medido
- **Margem de tolerância**: Maior para produtos variáveis

**Q: Qual a precisão do sistema?**
A:
- **Detecção de fraude**: 98.5% de precisão
- **Falsos positivos**: < 5%
- **Falsos negativos**: < 2%
- **Uptime**: 99.9% garantido

### **🔐 Segurança**

**Q: Como garantem que o QR não seja falsificado?**
A: Múltiplas camadas de segurança:
- **Assinatura criptográfica**: HMAC-SHA256
- **Timestamp**: Expiração automática em 2h
- **Hash do carrinho**: Integridade dos dados
- **Chave rotativa**: Renovada a cada 24h

**Q: E se alguém trocar produtos no carrinho?**
A: Sistema detecta via:
- **Validação de peso**: Divergência aciona alerta
- **Câmeras IA**: Detecção de movimento suspeito
- **Padrões comportamentais**: Anomalias no GuardPass
- **Auditoria amostral**: 3-7% das transações

**Q: Dados dos clientes ficam seguros?**
A: Conformidade total:
- **LGPD**: Dados pseudonimizados
- **Criptografia**: AES-256 em repouso e trânsito
- **Auditoria**: Logs imutáveis no blockchain
- **Consentimento**: Opt-in explícito para benefícios

### **📱 Tecnologia**

**Q: Preciso de app específico?**
A: Flexibilidade total:
- **App nativo**: iOS/Android otimizado
- **Web app**: Funciona em qualquer navegador
- **QR de entrada**: Cliente escaneia para acessar
- **Offline**: Funciona sem internet (sincroniza depois)

**Q: Funciona em lojas sem Wi-Fi bom?**
A: Sim:
- **Modo offline**: Dados locais sincronizados depois
- **4G/5G**: Backup automático via celular
- **Edge computing**: Processamento local
- **Sincronização inteligente**: Apenas dados essenciais

**Q: Integra com câmeras existentes?**
A: Sim:
- **ONVIF**: Padrão universal de câmeras IP
- **Análise em tempo real**: Detecção de anomalias
- **Privacy by design**: Apenas metadados, não imagens
- **Retrofit**: Aproveitamos infraestrutura existente

---

## 🌱 **ESG E SUSTENTABILIDADE**

**Q: Como o ESG é calculado?**
A: Engine proprietário que analisa:
- **Código NCM**: Base de dados ESG por produto
- **Cadeia de suprimentos**: Origem e transporte
- **Impacto ambiental**: Pegada de carbono
- **Responsabilidade social**: Práticas trabalhistas

**Q: Clientes veem o score ESG?**
A: Sim, de forma gamificada:
- **Score visual**: 0-10 com cores intuitivas
- **Sugestões**: Produtos mais sustentáveis
- **Recompensas**: Pontos por compras ESG
- **Impacto**: "Você salvou X árvores hoje"

**Q: Como isso ajuda minha loja?**
A: Múltiplos benefícios:
- **Diferenciação**: Primeira loja ESG da região
- **Compliance**: Relatórios automáticos para certificações
- **Marketing**: Cases de sustentabilidade
- **Fidelização**: Clientes conscientes são mais fiéis

---

## 🛡️ **GUARDPASS**

**Q: O que é o GuardPass?**
A: Sistema de reputação e confiança:
- **Perfil de risco**: Baseado em histórico
- **Tiers**: Basic, Premium, Enterprise
- **Benefícios**: Menos fricção para usuários confiáveis
- **Segurança**: Mais validação para novos usuários

**Q: Como alguém vira Premium?**
A: Critérios automáticos:
- **Transações**: 50+ sem incidentes
- **KYC**: Documentos verificados
- **Comportamento**: Padrões normais de compra
- **Tempo**: 3+ meses de uso regular

**Q: E se não tiver GuardPass?**
A: Funciona normalmente:
- **Usuário anônimo**: Validação padrão
- **Criação automática**: Perfil criado na primeira compra
- **Evolução gradual**: Melhora com uso
- **Sem obrigatoriedade**: Sempre opcional

---

## 🚀 **IMPLEMENTAÇÃO E SUPORTE**

### **🛠️ Requisitos Técnicos**

**Q: Que hardware preciso comprar?**
A: Mínimo necessário:
- **Balança**: Integrada ao carrinho ou pórtico (fornecemos)
- **Tablet/smartphone**: Para demonstração (cliente pode usar próprio)
- **Wi-Fi**: 10 Mbps estável
- **Energia**: 220V para balança

**Q: Minha equipe precisa de treinamento?**
A: Treinamento incluído:
- **Gerentes**: 4h (estratégia e métricas)
- **Operadores**: 2h (uso diário)
- **TI**: 8h (integração e troubleshooting)
- **Material**: Vídeos, manuais, certificação

**Q: E se der problema?**
A: Suporte completo:
- **24/7**: Para clientes Enterprise
- **Horário comercial**: Para outros planos
- **SLA**: 4h para crítico, 24h para normal
- **Escalação**: Acesso direto ao time técnico

### **📈 Métricas e Analytics**

**Q: Que relatórios vocês fornecem?**
A: Dashboard completo:
- **Operacionais**: Tempo, conversão, abandono
- **Financeiros**: ROI, economia, receita adicional
- **ESG**: Impacto ambiental, sustentabilidade
- **Comportamentais**: Padrões de compra, satisfação

**Q: Posso integrar com meu BI?**
A: Sim:
- **API de dados**: Acesso programático
- **Webhooks**: Eventos em tempo real
- **Exportação**: CSV, JSON, XML
- **Conectores**: Power BI, Tableau, Qlik

**Q: Dados ficam na minha empresa?**
A: Flexibilidade total:
- **Cloud**: Nossos servidores (padrão)
- **On-premise**: Seus servidores (Enterprise)
- **Híbrido**: Dados sensíveis local, analytics cloud
- **Backup**: Sempre disponível para download

---

## 🎯 **CASOS ESPECÍFICOS**

### **🏪 Supermercados**

**Q: Funciona com produtos de padaria?**
A: Sim:
- **Peso variável**: Tolerância maior (±20%)
- **Códigos PLU**: Integração com balança
- **Validação visual**: IA reconhece tipos de pão
- **Fallback**: Validação manual se necessário

**Q: E com promoções/descontos?**
A: Totalmente integrado:
- **Cupons digitais**: Aplicados automaticamente
- **Promoções por quantidade**: "Leve 3, pague 2"
- **Desconto progressivo**: Quanto mais compra, mais desconta
- **Cashback**: Pontos ou dinheiro de volta

### **💊 Farmácias**

**Q: Como lidam com medicamentos controlados?**
A: Compliance total:
- **Receita obrigatória**: Sistema bloqueia sem validação
- **Farmacêutico**: Aprovação manual necessária
- **Rastreabilidade**: Blockchain para auditoria
- **Relatórios**: Automáticos para vigilância sanitária

**Q: Funciona com genéricos/similares?**
A: Sim:
- **Sugestão automática**: Genérico mais barato
- **Comparação**: Preço e eficácia lado a lado
- **Escolha do cliente**: Decisão final sempre dele
- **Transparência**: Diferenças claras

### **📱 Eletrônicos**

**Q: Como validam produtos de alto valor?**
A: Segurança reforçada:
- **Dupla validação**: Peso + código de barras
- **Lacres eletrônicos**: RFID ou NFC
- **Câmeras direcionadas**: Foco na área de eletrônicos
- **Threshold menor**: Mais rigoroso para detecção

**Q: E garantias/assistência técnica?**
A: Integração completa:
- **Registro automático**: Garantia ativada na compra
- **QR da garantia**: Acesso fácil aos termos
- **Histórico**: Todas as compras do cliente
- **Suporte**: Canal direto para assistência

---

## 📞 **PRÓXIMOS PASSOS**

### **Ainda tem dúvidas?**

**🎯 Fale com nossos especialistas:**
- **Comercial**: vendas@guardflow.com
- **Técnico**: suporte@guardflow.com  
- **C-Level**: ceo@guardflow.com
- **WhatsApp**: +55 11 99999-9999

**📅 Agende uma conversa:**
- **Demo técnica**: 30 min
- **Reunião comercial**: 45 min
- **Apresentação C-Level**: 60 min
- **Piloto gratuito**: 30 dias

**👉 [AGENDAR AGORA](https://calendly.com/guardflow-vendas)**

---

**"Toda grande transformação começa com uma pergunta. Todas as suas foram respondidas. Agora é hora de agir."** 🚀✨
