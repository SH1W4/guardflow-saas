// GuardFlow Landing Page - Interactive JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initNavigation();
    initHeroAnimations();
    initTabSwitcher();
    initROICalculator();
    initPricingToggle();
    initContactForm();
    initChatWidget();
    initScrollAnimations();
    initDemoControls();
    
    console.log('🚀 GuardFlow Landing Page initialized!');
});

// Navigation
function initNavigation() {
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Mobile menu toggle
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
        });
    }
    
    // Close mobile menu when clicking on links
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
            navToggle.classList.remove('active');
        });
    });
    
    // Navbar scroll effect
    window.addEventListener('scroll', () => {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 100) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.boxShadow = 'none';
        }
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Hero Animations
function initHeroAnimations() {
    // Animate hero stats
    const stats = document.querySelectorAll('.stat-number');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateNumber(entry.target);
            }
        });
    });
    
    stats.forEach(stat => observer.observe(stat));
    
    // Animate dashboard metrics
    setTimeout(() => {
        const metricCards = document.querySelectorAll('.metric-card');
        metricCards.forEach((card, index) => {
            setTimeout(() => {
                card.style.animation = `slideInRight 0.6s ease-out ${index * 0.2}s both`;
            }, 1000);
        });
    }, 500);
    
    // Demo steps animation
    const demoSteps = document.querySelectorAll('.demo-step');
    let currentStep = 0;
    
    setInterval(() => {
        demoSteps.forEach(step => step.classList.remove('active'));
        demoSteps[currentStep].classList.add('active');
        currentStep = (currentStep + 1) % demoSteps.length;
    }, 2000);
}

// Animate numbers
function animateNumber(element) {
    const target = parseFloat(element.textContent);
    const duration = 2000;
    const step = target / (duration / 16);
    let current = 0;
    
    const timer = setInterval(() => {
        current += step;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        
        if (element.textContent.includes('%')) {
            element.textContent = Math.floor(current) + '%';
        } else if (element.textContent.includes('.')) {
            element.textContent = current.toFixed(1);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

// Tab Switcher
function initTabSwitcher() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');
            
            // Remove active class from all buttons and panes
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));
            
            // Add active class to clicked button and corresponding pane
            button.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });
}

// ROI Calculator
function initROICalculator() {
    const inputs = {
        monthlySales: document.getElementById('monthly-sales'),
        abandonmentRate: document.getElementById('abandonment-rate'),
        checkoutTime: document.getElementById('checkout-time'),
        employees: document.getElementById('employees')
    };
    
    const results = {
        revenueIncrease: document.getElementById('revenue-increase'),
        timeSaved: document.getElementById('time-saved'),
        costReduction: document.getElementById('cost-reduction'),
        totalROI: document.getElementById('total-roi')
    };
    
    // Calculate ROI
    function calculateROI() {
        const monthlySales = parseFloat(inputs.monthlySales.value) || 100000;
        const abandonmentRate = parseFloat(inputs.abandonmentRate.value) || 68;
        const checkoutTime = parseFloat(inputs.checkoutTime.value) || 3;
        const employees = parseFloat(inputs.employees.value) || 5;
        
        // Calculations
        const recoveredSales = monthlySales * (abandonmentRate / 100) * 0.67; // 67% recovery rate
        const timeSavedPercent = 85; // 85% time reduction
        const employeeCostSaving = employees * 3000 * 0.25; // 25% efficiency gain
        const totalROI = ((recoveredSales + employeeCostSaving) / 15000) * 100; // Assuming R$ 15k monthly cost
        
        // Update results
        if (results.revenueIncrease) {
            results.revenueIncrease.textContent = `+R$ ${(recoveredSales / 1000).toFixed(1)}k`;
        }
        if (results.timeSaved) {
            results.timeSaved.textContent = `-${timeSavedPercent}%`;
        }
        if (results.costReduction) {
            results.costReduction.textContent = `-R$ ${(employeeCostSaving / 1000).toFixed(1)}k`;
        }
        if (results.totalROI) {
            results.totalROI.textContent = `ROI: ${Math.floor(totalROI)}%`;
        }
    }
    
    // Add event listeners to inputs
    Object.values(inputs).forEach(input => {
        if (input) {
            input.addEventListener('input', calculateROI);
        }
    });
    
    // Initial calculation
    calculateROI();
}

// Pricing Toggle
function initPricingToggle() {
    const toggle = document.getElementById('pricing-toggle');
    const amounts = document.querySelectorAll('.amount');
    
    if (toggle) {
        toggle.addEventListener('change', () => {
            const isYearly = toggle.checked;
            
            amounts.forEach(amount => {
                const monthly = parseFloat(amount.getAttribute('data-monthly'));
                const yearly = parseFloat(amount.getAttribute('data-yearly'));
                
                if (isYearly) {
                    amount.textContent = yearly.toLocaleString('pt-BR');
                } else {
                    amount.textContent = monthly.toLocaleString('pt-BR');
                }
            });
        });
    }
}

// Contact Form
function initContactForm() {
    const form = document.getElementById('contact-form');
    
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(form);
            const data = Object.fromEntries(formData);
            
            // Show loading state
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enviando...';
            submitBtn.disabled = true;
            
            try {
                // Simulate form submission
                await new Promise(resolve => setTimeout(resolve, 2000));
                
                // Show success message
                showNotification('Mensagem enviada com sucesso! Entraremos em contato em breve.', 'success');
                form.reset();
                
                // Track conversion
                gtag('event', 'form_submit', {
                    event_category: 'Contact',
                    event_label: 'Landing Page Form'
                });
                
            } catch (error) {
                showNotification('Erro ao enviar mensagem. Tente novamente.', 'error');
            } finally {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }
        });
    }
}

// Chat Widget
function initChatWidget() {
    const chatButton = document.getElementById('chat-button');
    const chatPopup = document.getElementById('chat-popup');
    const chatClose = document.getElementById('chat-close');
    const chatOptions = document.querySelectorAll('.chat-option');
    
    if (chatButton && chatPopup) {
        chatButton.addEventListener('click', () => {
            chatPopup.classList.toggle('active');
        });
    }
    
    if (chatClose) {
        chatClose.addEventListener('click', () => {
            chatPopup.classList.remove('active');
        });
    }
    
    chatOptions.forEach(option => {
        option.addEventListener('click', () => {
            const action = option.textContent.trim();
            
            switch (action) {
                case 'Agendar Demo':
                    window.location.href = '#contact';
                    break;
                case 'Ver Preços':
                    window.location.href = '#pricing';
                    break;
                case 'Suporte Técnico':
                    window.open('https://github.com/SH1W4/guardflow-saas/issues', '_blank');
                    break;
            }
            
            chatPopup.classList.remove('active');
        });
    });
    
    // Close chat when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('#chat-widget')) {
            chatPopup.classList.remove('active');
        }
    });
}

// Scroll Animations
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('.benefit-card, .feature-item, .testimonial-card, .problem-item');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in-up');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    animatedElements.forEach(element => {
        observer.observe(element);
    });
    
    // Parallax effect for hero background
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const heroBackground = document.querySelector('.hero-background');
        
        if (heroBackground) {
            heroBackground.style.transform = `translateY(${scrolled * 0.5}px)`;
        }
    });
}

// Demo Controls
function initDemoControls() {
    const demoBtns = document.querySelectorAll('.demo-btn');
    const demoIframe = document.querySelector('.demo-iframe iframe');
    
    demoBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const demoType = btn.getAttribute('data-demo');
            
            // Remove active class from all buttons
            demoBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Update iframe src based on demo type
            if (demoIframe) {
                const baseUrl = 'https://guardflow-demo.vercel.app';
                let newUrl = baseUrl;
                
                switch (demoType) {
                    case 'scanner':
                        newUrl += '/scanner';
                        break;
                    case 'checkout':
                        newUrl += '/checkout';
                        break;
                    case 'esg':
                        newUrl += '/esg';
                        break;
                    case 'analytics':
                        newUrl += '/analytics';
                        break;
                }
                
                demoIframe.src = newUrl;
            }
        });
    });
}

// Utility Functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        </div>
        <button class="notification-close">&times;</button>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        padding: 16px 20px;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        z-index: 10000;
        max-width: 400px;
        animation: slideInRight 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 5000);
    
    // Close button
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.addEventListener('click', () => {
        notification.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    });
}

// Performance Monitoring
function initPerformanceMonitoring() {
    // Track page load time
    window.addEventListener('load', () => {
        const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
        
        if (typeof gtag !== 'undefined') {
            gtag('event', 'page_load_time', {
                event_category: 'Performance',
                value: Math.round(loadTime)
            });
        }
        
        console.log(`Page loaded in ${loadTime}ms`);
    });
    
    // Track scroll depth
    let maxScroll = 0;
    window.addEventListener('scroll', () => {
        const scrollPercent = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
        
        if (scrollPercent > maxScroll) {
            maxScroll = scrollPercent;
            
            // Track milestones
            if ([25, 50, 75, 100].includes(scrollPercent)) {
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'scroll_depth', {
                        event_category: 'Engagement',
                        value: scrollPercent
                    });
                }
            }
        }
    });
}

// Initialize performance monitoring
initPerformanceMonitoring();

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100px);
        }
    }
    
    .notification-content {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .notification-close {
        position: absolute;
        top: 8px;
        right: 12px;
        background: none;
        border: none;
        color: white;
        font-size: 18px;
        cursor: pointer;
        opacity: 0.8;
    }
    
    .notification-close:hover {
        opacity: 1;
    }
    
    .demo-btn.active {
        background: var(--primary) !important;
        color: white !important;
    }
`;
document.head.appendChild(style);

// Export functions for external use
window.GuardFlow = {
    showNotification,
    calculateROI: initROICalculator,
    initDemo: initDemoControls
};
