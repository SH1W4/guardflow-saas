# 🌐 Landing Page SaaS - GuardFlow

**Página de Conversão para Geração de Leads SaaS**  
**Versão**: 1.0 | **Data**: 20/10/2025

---

## 🎯 **ESTRUTURA DA LANDING PAGE**

### **📱 HERO SECTION (Above the Fold)**

```html
<!-- HERO SECTION -->
<section class="hero-section">
  <div class="container">
    <div class="hero-content">
      <div class="hero-logo">
        <!-- Logo GuardFlow: Carrinho azul + cruz verde + arco colorido -->
        <img src="guardflow-logo.svg" alt="GuardFlow" class="logo-main">
      </div>
      
      <h1 class="hero-title">
        Transforme seu Checkout em 
        <span class="highlight">Vantagem Competitiva</span>
      </h1>
      
      <h2 class="hero-subtitle">
        A Primeira Plataforma SaaS de Checkout Inteligente 
        com IA Ética do Brasil
      </h2>
      
      <div class="hero-benefits">
        <div class="benefit">
          <span class="icon">⚡</span>
          <span class="text">90% mais rápido</span>
        </div>
        <div class="benefit">
          <span class="icon">🌱</span>
          <span class="text">ESG automático</span>
        </div>
        <div class="benefit">
          <span class="icon">🧠</span>
          <span class="text">IA personalizada</span>
        </div>
        <div class="benefit">
          <span class="icon">💰</span>
          <span class="text">ROI 200%+ ao mês</span>
        </div>
      </div>
      
      <div class="hero-cta">
        <button class="cta-primary" onclick="openDemo()">
          🎬 Ver Demo Gratuita (2 min)
        </button>
        <button class="cta-secondary" onclick="openCalculator()">
          🧮 Calcular Meu ROI
        </button>
      </div>
      
      <div class="hero-proof">
        <p class="proof-text">
          ✅ Mais de 50 supermercados já economizam R$ 2,3M/mês
          <br>
          ✅ ROI médio de 208% ao mês comprovado
          <br>
          ✅ Implementação em 4 semanas garantida
        </p>
      </div>
    </div>
    
    <div class="hero-video">
      <video autoplay muted loop>
        <source src="guardflow-demo.mp4" type="video/mp4">
      </video>
      <div class="video-overlay">
        <button class="play-button" onclick="playFullDemo()">
          ▶️ Assistir Demo Completa
        </button>
      </div>
    </div>
  </div>
</section>
```

### **🚨 PROBLEMA SECTION**

```html
<!-- PROBLEMA SECTION -->
<section class="problem-section">
  <div class="container">
    <h2 class="section-title">
      Seu Checkout Está Custando uma Fortuna
    </h2>
    
    <div class="problems-grid">
      <div class="problem-card">
        <div class="problem-icon">⏰</div>
        <h3>Filas de 8-12 Minutos</h3>
        <p>70% dos clientes abandonam o carrinho por causa das filas intermináveis</p>
        <div class="problem-cost">Custo: R$ 50K-500K/mês</div>
      </div>
      
      <div class="problem-card">
        <div class="problem-icon">👥</div>
        <h3>Custos Operacionais Altos</h3>
        <p>30-40% do staff dedicado aos caixas, com salários de R$ 3K+ cada</p>
        <div class="problem-cost">Custo: R$ 20K-200K/mês</div>
      </div>
      
      <div class="problem-card">
        <div class="problem-icon">📊</div>
        <h3>Zero Dados ESG</h3>
        <p>Compliance manual, custoso e propenso a erros e multas</p>
        <div class="problem-cost">Custo: R$ 10K-50K/mês</div>
      </div>
      
      <div class="problem-card">
        <div class="problem-icon">😤</div>
        <h3>Experiência Arcaica</h3>
        <p>NPS médio de apenas 4.2/10, clientes insatisfeitos</p>
        <div class="problem-cost">Custo: Perda de fidelização</div>
      </div>
    </div>
    
    <div class="problem-summary">
      <h3>Total Desperdiçado: R$ 80K - R$ 750K por mês</h3>
      <p>E isso é só o que você consegue medir...</p>
    </div>
  </div>
</section>
```

### **✨ SOLUÇÃO SECTION**

```html
<!-- SOLUÇÃO SECTION -->
<section class="solution-section">
  <div class="container">
    <h2 class="section-title">
      GuardFlow: Checkout Inteligente em 3 Passos
    </h2>
    
    <div class="solution-steps">
      <div class="step">
        <div class="step-number">1</div>
        <div class="step-content">
          <h3>🧠 Personalização Inteligente</h3>
          <p>IA SEVE detecta preferências na entrada e oferece recomendações ESG personalizadas, sem coletar dados pessoais</p>
          <div class="step-benefit">Resultado: +15% conversão</div>
        </div>
        <div class="step-visual">
          <img src="step1-personalization.gif" alt="Personalização SEVE">
        </div>
      </div>
      
      <div class="step">
        <div class="step-number">2</div>
        <div class="step-content">
          <h3>📱 Checkout Zero Atrito</h3>
          <p>Cliente escaneia produtos pelo app/web, sistema valida por peso e gera QR assinado criptograficamente</p>
          <div class="step-benefit">Resultado: 8min → 30seg</div>
        </div>
        <div class="step-visual">
          <img src="step2-checkout.gif" alt="QR Checkout">
        </div>
      </div>
      
      <div class="step">
        <div class="step-number">3</div>
        <div class="step-content">
          <h3>🚪 Saída Automática</h3>
          <p>Pórtico valida QR automaticamente e libera cliente sem intervenção humana</p>
          <div class="step-benefit">Resultado: -85% abandono</div>
        </div>
        <div class="step-visual">
          <img src="step3-exit.gif" alt="Saída Automática">
        </div>
      </div>
    </div>
    
    <div class="solution-cta">
      <button class="cta-primary" onclick="requestDemo()">
        🎯 Quero Ver Isso Funcionando
      </button>
    </div>
  </div>
</section>
```

### **💰 ROI SECTION**

```html
<!-- ROI SECTION -->
<section class="roi-section">
  <div class="container">
    <h2 class="section-title">
      ROI Comprovado: Clientes Economizam Milhões
    </h2>
    
    <div class="roi-calculator">
      <h3>Calcule Sua Economia Agora:</h3>
      
      <div class="calculator-inputs">
        <div class="input-group">
          <label>Número de lojas:</label>
          <input type="number" id="stores" value="3" onchange="calculateROI()">
        </div>
        <div class="input-group">
          <label>Transações/mês por loja:</label>
          <input type="number" id="transactions" value="5000" onchange="calculateROI()">
        </div>
        <div class="input-group">
          <label>Ticket médio (R$):</label>
          <input type="number" id="ticket" value="65" onchange="calculateROI()">
        </div>
        <div class="input-group">
          <label>Funcionários caixa por loja:</label>
          <input type="number" id="cashiers" value="8" onchange="calculateROI()">
        </div>
      </div>
      
      <div class="calculator-results">
        <div class="result-card current-costs">
          <h4>💸 Custos Atuais (Mensal)</h4>
          <div class="cost-item">
            <span>Salários caixas:</span>
            <span id="salary-costs">R$ 72.000</span>
          </div>
          <div class="cost-item">
            <span>Perdas abandono:</span>
            <span id="abandonment-costs">R$ 682.500</span>
          </div>
          <div class="cost-item">
            <span>Ineficiência:</span>
            <span id="inefficiency-costs">R$ 21.600</span>
          </div>
          <div class="total-current">
            <strong>Total: <span id="total-current">R$ 776.100</span></strong>
          </div>
        </div>
        
        <div class="result-card guardflow-investment">
          <h4>💰 Investimento GuardFlow</h4>
          <div class="cost-item">
            <span>Plano Professional:</span>
            <span>R$ 24.000</span>
          </div>
          <div class="cost-item">
            <span>Taxa sucesso (3.5%):</span>
            <span id="success-fee">R$ 34.125</span>
          </div>
          <div class="total-investment">
            <strong>Total: <span id="total-investment">R$ 58.125</span></strong>
          </div>
        </div>
        
        <div class="result-card roi-results">
          <h4>💎 Retorno Mensal</h4>
          <div class="benefit-item">
            <span>Redução funcionários:</span>
            <span id="staff-savings">R$ 43.200</span>
          </div>
          <div class="benefit-item">
            <span>Redução abandono:</span>
            <span id="abandonment-savings">R$ 580.125</span>
          </div>
          <div class="benefit-item">
            <span>Aumento conversão:</span>
            <span id="conversion-increase">R$ 146.250</span>
          </div>
          <div class="total-benefits">
            <strong>Total: <span id="total-benefits">R$ 769.575</span></strong>
          </div>
          
          <div class="roi-final">
            <div class="roi-metric">
              <span>ROI Líquido:</span>
              <span id="net-roi" class="highlight">R$ 711.450/mês</span>
            </div>
            <div class="roi-metric">
              <span>ROI %:</span>
              <span id="roi-percentage" class="highlight">1.224% ao mês</span>
            </div>
            <div class="roi-metric">
              <span>Payback:</span>
              <span id="payback" class="highlight">2.4 semanas</span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="roi-cta">
        <button class="cta-primary" onclick="requestProposal()">
          📊 Quero Proposta Personalizada
        </button>
      </div>
    </div>
  </div>
</section>
```

### **🏆 CASES DE SUCESSO**

```html
<!-- CASES SECTION -->
<section class="cases-section">
  <div class="container">
    <h2 class="section-title">
      Cases Reais: Resultados Comprovados
    </h2>
    
    <div class="cases-grid">
      <div class="case-card">
        <div class="case-header">
          <h3>Supermercado ABC - São Paulo</h3>
          <div class="case-profile">2 lojas • 8K transações/mês</div>
        </div>
        <div class="case-results">
          <div class="metric">
            <span class="metric-value">-88%</span>
            <span class="metric-label">Tempo checkout</span>
          </div>
          <div class="metric">
            <span class="metric-value">+420%</span>
            <span class="metric-label">Conversão</span>
          </div>
          <div class="metric">
            <span class="metric-value">234%</span>
            <span class="metric-label">ROI mensal</span>
          </div>
          <div class="metric">
            <span class="metric-value">9.4/10</span>
            <span class="metric-label">NPS</span>
          </div>
        </div>
        <div class="case-quote">
          "O GuardFlow transformou nossa operação. Nossos clientes adoram e nossa equipe é 40% mais produtiva."
        </div>
        <div class="case-author">— João Silva, Gerente</div>
      </div>
      
      <div class="case-card">
        <div class="case-header">
          <h3>Farmácia XYZ - Rio de Janeiro</h3>
          <div class="case-profile">1 loja • 3K transações/mês</div>
        </div>
        <div class="case-results">
          <div class="metric">
            <span class="metric-value">100%</span>
            <span class="metric-label">Compliance ESG</span>
          </div>
          <div class="metric">
            <span class="metric-value">+65%</span>
            <span class="metric-label">Velocidade</span>
          </div>
          <div class="metric">
            <span class="metric-value">0</span>
            <span class="metric-label">Vendas irregulares</span>
          </div>
          <div class="metric">
            <span class="metric-value">9.1/10</span>
            <span class="metric-label">Satisfação</span>
          </div>
        </div>
        <div class="case-quote">
          "Compliance ESG automático nos poupou R$ 15K/mês em consultoria. O sistema se paga sozinho."
        </div>
        <div class="case-author">— Maria Santos, Proprietária</div>
      </div>
      
      <div class="case-card">
        <div class="case-header">
          <h3>Eletrônicos 123 - Belo Horizonte</h3>
          <div class="case-profile">1 loja • 2K transações/mês</div>
        </div>
        <div class="case-results">
          <div class="metric">
            <span class="metric-value">0</span>
            <span class="metric-label">Perdas por furto</span>
          </div>
          <div class="metric">
            <span class="metric-value">+70%</span>
            <span class="metric-label">Eficiência</span>
          </div>
          <div class="metric">
            <span class="metric-value">+15%</span>
            <span class="metric-label">Ticket médio</span>
          </div>
          <div class="metric">
            <span class="metric-value">9.5/10</span>
            <span class="metric-label">NPS</span>
          </div>
        </div>
        <div class="case-quote">
          "Segurança total com experiência incrível. Nossos clientes recomendam a loja pela tecnologia."
        </div>
        <div class="case-author">— Carlos Lima, Dono</div>
      </div>
    </div>
  </div>
</section>
```

### **🛡️ DIFERENCIAL COMPETITIVO**

```html
<!-- DIFERENCIAL SECTION -->
<section class="competitive-section">
  <div class="container">
    <h2 class="section-title">
      Por Que GuardFlow é Único no Mercado
    </h2>
    
    <div class="comparison-table">
      <table>
        <thead>
          <tr>
            <th>Aspecto</th>
            <th class="guardflow">GuardFlow</th>
            <th>Amazon Go</th>
            <th>Self-Checkout</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Personalização</td>
            <td class="guardflow">✅ IA ética</td>
            <td>❌ Invasiva</td>
            <td>❌ Inexistente</td>
          </tr>
          <tr>
            <td>ESG</td>
            <td class="guardflow">✅ Nativo</td>
            <td>❌ Add-on</td>
            <td>❌ Manual</td>
          </tr>
          <tr>
            <td>Implementação</td>
            <td class="guardflow">✅ 4 semanas</td>
            <td>❌ 6+ meses</td>
            <td>✅ 2 semanas</td>
          </tr>
          <tr>
            <td>Custo</td>
            <td class="guardflow">✅ R$ 26K/mês</td>
            <td>❌ R$ 500K+</td>
            <td>✅ R$ 50K setup</td>
          </tr>
          <tr>
            <td>ROI</td>
            <td class="guardflow">✅ 208%/mês</td>
            <td>❌ 24 meses</td>
            <td>❌ Negativo</td>
          </tr>
          <tr>
            <td>Segurança</td>
            <td class="guardflow">✅ Militar</td>
            <td>✅ Alta</td>
            <td>❌ Básica</td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div class="unique-advantages">
      <div class="advantage">
        <div class="advantage-icon">🥇</div>
        <h3>Primeiro Mover</h3>
        <p>Única solução com IA ética no Brasil. 3 anos de desenvolvimento, 15 patentes depositadas.</p>
      </div>
      <div class="advantage">
        <div class="advantage-icon">🧠</div>
        <h3>Tecnologia Proprietária</h3>
        <p>SEVE personalização, QR assinado, ESG Engine automático, thresholds adaptativos.</p>
      </div>
      <div class="advantage">
        <div class="advantage-icon">🔒</div>
        <h3>Defensibilidade</h3>
        <p>Patentes, dados proprietários, integração profunda, barreira de entrada R$ 50M+.</p>
      </div>
    </div>
  </div>
</section>
```

### **💎 OFERTA ESPECIAL**

```html
<!-- OFERTA SECTION -->
<section class="offer-section">
  <div class="container">
    <div class="offer-badge">🔥 OFERTA LIMITADA</div>
    
    <h2 class="section-title">
      Pacote Piloto GuardFlow SaaS
    </h2>
    <p class="offer-subtitle">Apenas para os primeiros 10 clientes</p>
    
    <div class="offer-content">
      <div class="offer-included">
        <h3>✅ O Que Está Incluído:</h3>
        <ul>
          <li>Setup completo GRATUITO (valor R$ 15K)</li>
          <li>30 dias de teste SEM CUSTO</li>
          <li>Treinamento equipe INCLUSO</li>
          <li>Suporte dedicado 24/7</li>
          <li>Garantia ROI ou dinheiro de volta</li>
          <li>Upgrade gratuito para Professional</li>
        </ul>
      </div>
      
      <div class="offer-bonus">
        <h3>🎁 Bônus Exclusivos:</h3>
        <ul>
          <li>Consultoria ESG (R$ 10K valor)</li>
          <li>Dashboard personalizado</li>
          <li>Success Manager dedicado</li>
          <li>Certificado "Loja do Futuro"</li>
        </ul>
      </div>
      
      <div class="offer-investment">
        <h3>💰 Investimento:</h3>
        <div class="pricing-timeline">
          <div class="price-period">
            <span class="period">Mês 1:</span>
            <span class="price">GRATUITO</span>
            <span class="note">(teste)</span>
          </div>
          <div class="price-period">
            <span class="period">Mês 2-6:</span>
            <span class="price">R$ 2.000/mês</span>
            <span class="note">(Starter)</span>
          </div>
          <div class="price-period">
            <span class="period">Mês 7+:</span>
            <span class="price">R$ 8.000/mês</span>
            <span class="note">(Professional)</span>
          </div>
        </div>
        <div class="roi-guarantee">
          <strong>ROI garantido ou reembolso integral</strong>
        </div>
      </div>
    </div>
    
    <div class="offer-urgency">
      <div class="urgency-timer">
        <h4>⏰ Oferta válida até:</h4>
        <div class="countdown" id="countdown">
          <span id="days">15</span> dias
          <span id="hours">23</span> horas
          <span id="minutes">45</span> min
        </div>
      </div>
      <div class="urgency-reasons">
        <p>🎄 <strong>Black Friday chegando</strong> - Implemente antes do pico</p>
        <p>💰 <strong>Orçamentos 2026</strong> - Reserve agora</p>
        <p>🏃‍♂️ <strong>Apenas 10 vagas</strong> - 7 já preenchidas</p>
      </div>
    </div>
    
    <div class="offer-cta">
      <button class="cta-primary mega" onclick="requestOffer()">
        🚀 Quero Garantir Minha Vaga Agora
      </button>
      <p class="cta-note">Sem compromisso • Setup gratuito • ROI garantido</p>
    </div>
  </div>
</section>
```

### **📞 CALL TO ACTION FINAL**

```html
<!-- CTA FINAL SECTION -->
<section class="final-cta-section">
  <div class="container">
    <h2 class="section-title">
      Pronto para Transformar seu Checkout?
    </h2>
    
    <div class="cta-options">
      <div class="cta-option">
        <div class="cta-icon">🎬</div>
        <h3>Ver Demo Gratuita</h3>
        <p>Assista como funciona em 2 minutos</p>
        <button class="cta-button" onclick="requestDemo()">
          Assistir Agora
        </button>
      </div>
      
      <div class="cta-option">
        <div class="cta-icon">🧮</div>
        <h3>Calcular Meu ROI</h3>
        <p>Descubra quanto você vai economizar</p>
        <button class="cta-button" onclick="openCalculator()">
          Calcular ROI
        </button>
      </div>
      
      <div class="cta-option">
        <div class="cta-icon">📞</div>
        <h3>Falar com Especialista</h3>
        <p>Consultoria gratuita personalizada</p>
        <button class="cta-button" onclick="requestCall()">
          Agendar Ligação
        </button>
      </div>
    </div>
    
    <div class="contact-info">
      <h3>Ou entre em contato diretamente:</h3>
      <div class="contact-methods">
        <div class="contact-method">
          <span class="icon">📧</span>
          <span>vendas@guardflow.com</span>
        </div>
        <div class="contact-method">
          <span class="icon">📱</span>
          <span>+55 11 99999-9999</span>
        </div>
        <div class="contact-method">
          <span class="icon">🌐</span>
          <span>guardflow.com/saas</span>
        </div>
      </div>
    </div>
    
    <div class="final-guarantee">
      <h4>🛡️ Garantias:</h4>
      <ul>
        <li>✅ ROI positivo em 90 dias ou reembolso</li>
        <li>✅ Uptime 99.5% garantido por SLA</li>
        <li>✅ Suporte 24/7 durante implementação</li>
        <li>✅ Success Manager dedicado por 6 meses</li>
      </ul>
    </div>
  </div>
</section>
```

---

## 📱 **JAVASCRIPT INTERATIVO**

```javascript
// ROI Calculator
function calculateROI() {
  const stores = parseInt(document.getElementById('stores').value) || 0;
  const transactions = parseInt(document.getElementById('transactions').value) || 0;
  const ticket = parseFloat(document.getElementById('ticket').value) || 0;
  const cashiers = parseInt(document.getElementById('cashiers').value) || 0;
  
  // Cálculos
  const monthlySalaries = stores * cashiers * 3000;
  const monthlyRevenue = stores * transactions * ticket;
  const abandonmentLoss = monthlyRevenue * 0.70;
  const inefficiencyCost = monthlySalaries * 0.30;
  const totalCurrentCosts = monthlySalaries + abandonmentLoss + inefficiencyCost;
  
  const saasPrice = stores <= 1 ? 2000 : stores <= 5 ? 8000 : 25000;
  const successFee = monthlyRevenue * 0.035;
  const totalInvestment = saasPrice + successFee;
  
  const staffSavings = monthlySalaries * 0.60;
  const abandonmentSavings = abandonmentLoss * 0.85;
  const conversionIncrease = monthlyRevenue * 0.15;
  const totalBenefits = staffSavings + abandonmentSavings + conversionIncrease;
  
  const netROI = totalBenefits - totalInvestment;
  const roiPercentage = ((netROI / totalInvestment) * 100).toFixed(0);
  const paybackWeeks = (totalInvestment / (totalBenefits / 4.33)).toFixed(1);
  
  // Update UI
  document.getElementById('salary-costs').textContent = `R$ ${monthlySalaries.toLocaleString()}`;
  document.getElementById('abandonment-costs').textContent = `R$ ${abandonmentLoss.toLocaleString()}`;
  document.getElementById('inefficiency-costs').textContent = `R$ ${inefficiencyCost.toLocaleString()}`;
  document.getElementById('total-current').textContent = `R$ ${totalCurrentCosts.toLocaleString()}`;
  
  document.getElementById('success-fee').textContent = `R$ ${successFee.toLocaleString()}`;
  document.getElementById('total-investment').textContent = `R$ ${totalInvestment.toLocaleString()}`;
  
  document.getElementById('staff-savings').textContent = `R$ ${staffSavings.toLocaleString()}`;
  document.getElementById('abandonment-savings').textContent = `R$ ${abandonmentSavings.toLocaleString()}`;
  document.getElementById('conversion-increase').textContent = `R$ ${conversionIncrease.toLocaleString()}`;
  document.getElementById('total-benefits').textContent = `R$ ${totalBenefits.toLocaleString()}`;
  
  document.getElementById('net-roi').textContent = `R$ ${netROI.toLocaleString()}/mês`;
  document.getElementById('roi-percentage').textContent = `${roiPercentage}% ao mês`;
  document.getElementById('payback').textContent = `${paybackWeeks} semanas`;
}

// Countdown Timer
function updateCountdown() {
  const endDate = new Date('2025-11-30T23:59:59').getTime();
  const now = new Date().getTime();
  const distance = endDate - now;
  
  const days = Math.floor(distance / (1000 * 60 * 60 * 24));
  const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  
  document.getElementById('days').textContent = days;
  document.getElementById('hours').textContent = hours;
  document.getElementById('minutes').textContent = minutes;
}

// CTA Actions
function requestDemo() {
  // Track event
  gtag('event', 'demo_request', {
    'event_category': 'engagement',
    'event_label': 'landing_page'
  });
  
  // Open demo modal or redirect
  window.open('https://calendly.com/guardflow-demo', '_blank');
}

function openCalculator() {
  document.querySelector('.roi-section').scrollIntoView({ behavior: 'smooth' });
}

function requestProposal() {
  // Collect calculator data
  const data = {
    stores: document.getElementById('stores').value,
    transactions: document.getElementById('transactions').value,
    ticket: document.getElementById('ticket').value,
    cashiers: document.getElementById('cashiers').value,
    roi: document.getElementById('roi-percentage').textContent
  };
  
  // Send to CRM
  fetch('/api/lead', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  
  // Redirect to proposal form
  window.location.href = '/proposta?' + new URLSearchParams(data);
}

function requestOffer() {
  // Track high-intent action
  gtag('event', 'offer_request', {
    'event_category': 'conversion',
    'event_label': 'special_offer'
  });
  
  // Open contact form
  window.open('/contato?offer=piloto', '_blank');
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
  calculateROI();
  setInterval(updateCountdown, 60000); // Update every minute
  updateCountdown();
});
```

---

## 🎨 **CSS STYLING HIGHLIGHTS**

```css
/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 80px 0;
  min-height: 100vh;
  display: flex;
  align-items: center;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.highlight {
  color: #00ff88;
  text-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
}

.hero-benefits {
  display: flex;
  gap: 2rem;
  margin: 2rem 0;
  flex-wrap: wrap;
}

.benefit {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  padding: 0.5rem 1rem;
  border-radius: 25px;
  backdrop-filter: blur(10px);
}

/* CTA Buttons */
.cta-primary {
  background: linear-gradient(45deg, #00ff88, #00cc6a);
  color: white;
  border: none;
  padding: 1rem 2rem;
  font-size: 1.2rem;
  font-weight: 600;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 10px 30px rgba(0, 255, 136, 0.3);
}

.cta-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 40px rgba(0, 255, 136, 0.4);
}

.cta-primary.mega {
  font-size: 1.5rem;
  padding: 1.5rem 3rem;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { box-shadow: 0 10px 30px rgba(0, 255, 136, 0.3); }
  50% { box-shadow: 0 15px 50px rgba(0, 255, 136, 0.6); }
  100% { box-shadow: 0 10px 30px rgba(0, 255, 136, 0.3); }
}

/* ROI Calculator */
.roi-calculator {
  background: white;
  border-radius: 20px;
  padding: 3rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  margin: 2rem 0;
}

.calculator-results {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
}

.result-card {
  padding: 2rem;
  border-radius: 15px;
  border: 2px solid #f0f0f0;
}

.current-costs {
  border-color: #ff6b6b;
  background: linear-gradient(135deg, #fff5f5, #ffe0e0);
}

.guardflow-investment {
  border-color: #4ecdc4;
  background: linear-gradient(135deg, #f0fffe, #e0f7f5);
}

.roi-results {
  border-color: #00ff88;
  background: linear-gradient(135deg, #f0fff8, #e0ffed);
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-benefits {
    justify-content: center;
  }
  
  .calculator-inputs {
    grid-template-columns: 1fr;
  }
  
  .cases-grid {
    grid-template-columns: 1fr;
  }
}
```

---

## 📊 **MÉTRICAS DE CONVERSÃO**

### **🎯 KPIs da Landing Page**
- **Taxa de conversão**: 15-25% (industry: 2-5%)
- **Tempo na página**: 3-5 minutos
- **Bounce rate**: <30%
- **Demo requests**: 5-10% dos visitantes
- **ROI calculator usage**: 40-60%
- **Offer requests**: 2-5% dos visitantes

### **📈 A/B Tests Sugeridos**
1. **Headlines**: "Transforme" vs "Revolucione" vs "Automatize"
2. **CTAs**: "Ver Demo" vs "Assistir Demo" vs "Demo Gratuita"
3. **Cores**: Verde vs Azul vs Roxo para CTAs
4. **Urgência**: Com vs sem countdown timer
5. **Prova social**: Cases vs depoimentos vs números

### **🔍 Tracking Events**
```javascript
// Google Analytics 4 Events
gtag('event', 'page_view', {
  'page_title': 'GuardFlow SaaS Landing Page',
  'page_location': window.location.href
});

gtag('event', 'scroll', {
  'event_category': 'engagement',
  'event_label': 'hero_section'
});

gtag('event', 'calculator_use', {
  'event_category': 'engagement',
  'event_label': 'roi_calculator'
});
```

**A landing page SaaS está pronta para converter visitantes em leads qualificados! 🌐💰**
