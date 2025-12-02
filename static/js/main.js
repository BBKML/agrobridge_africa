/**
 * AgroBridge Africa - JavaScript Optimisé
 * Performance et accessibilité améliorées
 */

// ============================================
// UTILITAIRES
// ============================================

// Debounce optimisé
const debounce = (func, wait = 10) => {
    let timeout;
    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
};

// Throttle pour événements fréquents
const throttle = (func, limit = 100) => {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
};

// ============================================
// 1. LOADING SCREEN - Optimisé
// ============================================

window.addEventListener('load', () => {
    const loader = document.querySelector('.loading-overlay');
    if (loader) {
        // Utiliser requestAnimationFrame pour smooth animation
        requestAnimationFrame(() => {
            loader.style.opacity = '0';
            setTimeout(() => loader.remove(), 500);
        });
    }
});

// ============================================
// 2. HEADER SCROLL - Throttled
// ============================================

const header = document.querySelector('header');
let lastScroll = 0;

const handleScroll = throttle(() => {
    const currentScroll = window.pageYOffset;
    
    // Toggle classe scrolled
    header.classList.toggle('scrolled', currentScroll > 50);
    
    // Auto-hide header (optionnel)
    // if (currentScroll > lastScroll && currentScroll > 200) {
    //     header.style.transform = 'translateY(-100%)';
    // } else {
    //     header.style.transform = 'translateY(0)';
    // }
    
    lastScroll = currentScroll;
}, 100);

window.addEventListener('scroll', handleScroll, { passive: true });

// ============================================
// 3. INTERSECTION OBSERVER - Performant
// ============================================

// Configuration optimale
const observerConfig = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

// Observer unique pour tous les éléments
const animationObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            // Ajouter classe avec délai cascade
            const delay = entry.target.dataset.delay || 0;
            
            setTimeout(() => {
                entry.target.classList.add('animated');
            }, delay);
            
            // Arrêter d'observer après animation
            animationObserver.unobserve(entry.target);
        }
    });
}, observerConfig);

// Initialiser au chargement DOM
document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll(`
        .feature-card,
        .service-card,
        .product-card,
        .pillar-card,
        .contact-info-card,
        .process-step,
        .benefit-item,
        .value-item,
        .faq-item,
        .spec-card
    `);
    
    animatedElements.forEach((el, index) => {
        el.classList.add('animate-on-scroll');
        
        // Calculer délai pour effet cascade dans grilles
        const parent = el.parentElement;
        if (parent.classList.contains('features-grid') ||
            parent.classList.contains('services-grid') ||
            parent.classList.contains('products-grid')) {
            el.dataset.delay = index * 100; // 100ms entre chaque
        }
        
        animationObserver.observe(el);
    });
});

// ============================================
// 4. MOBILE MENU - Amélioré
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    const body = document.body;
    
    if (!menuToggle || !navLinks) return;
    
    // Toggle menu
    menuToggle.addEventListener('click', () => {
        const isOpen = navLinks.classList.toggle('active');
        menuToggle.classList.toggle('active');
        body.classList.toggle('menu-open');
        
        // Accessibility
        menuToggle.setAttribute('aria-expanded', isOpen);
        menuToggle.innerHTML = isOpen ? '✕' : '☰';
        
        // Bloquer scroll quand menu ouvert
        body.style.overflow = isOpen ? 'hidden' : '';
    });
    
    // Fermer au clic sur un lien
    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
            menuToggle.classList.remove('active');
            body.classList.remove('menu-open');
            body.style.overflow = '';
            menuToggle.setAttribute('aria-expanded', 'false');
            menuToggle.innerHTML = '☰';
        });
    });
    
    // Fermer avec Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && navLinks.classList.contains('active')) {
            navLinks.classList.remove('active');
            menuToggle.classList.remove('active');
            body.classList.remove('menu-open');
            body.style.overflow = '';
            menuToggle.focus();
        }
    });
});

// ============================================
// 5. SMOOTH SCROLL
// ============================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href === '#') return;
        
        e.preventDefault();
        const target = document.querySelector(href);
        
        if (target) {
            const offsetTop = target.offsetTop - 70; // Header height
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// ============================================
// 6. COUNTER ANIMATION - Optimisé
// ============================================

const animateCounter = (element, target, duration = 2000) => {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;
    
    const updateCounter = () => {
        current += increment;
        if (current < target) {
            element.textContent = Math.floor(current);
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target;
        }
    };
    
    requestAnimationFrame(updateCounter);
};

// Observer pour compteurs
const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting && !entry.target.dataset.animated) {
            entry.target.dataset.animated = 'true';
            const target = parseInt(entry.target.dataset.count);
            if (!isNaN(target)) {
                animateCounter(entry.target, target);
            }
            counterObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-count]').forEach(counter => {
        counterObserver.observe(counter);
    });
});

// ============================================
// 7. FORM ENHANCEMENT
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            // Animation label flottant
            input.addEventListener('focus', () => {
                input.parentElement.classList.add('focused');
            });
            
            input.addEventListener('blur', () => {
                if (!input.value) {
                    input.parentElement.classList.remove('focused');
                }
            });
            
            // Validation temps réel
            input.addEventListener('input', debounce(() => {
                if (input.validity.valid) {
                    input.classList.remove('invalid');
                    input.classList.add('valid');
                } else {
                    input.classList.remove('valid');
                    if (input.value) {
                        input.classList.add('invalid');
                    }
                }
            }, 300));
        });
        
        // Submit avec loading
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                submitBtn.innerHTML = '<span class="spinner"></span> Envoi...';
                submitBtn.disabled = true;
            }
        });
    });
});

// ============================================
// 8. MESSAGES AUTO-HIDE
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    const messages = document.querySelectorAll('.alert');
    
    messages.forEach(message => {
        // Bouton fermeture
        const closeBtn = document.createElement('button');
        closeBtn.innerHTML = '×';
        closeBtn.className = 'message-close';
        closeBtn.setAttribute('aria-label', 'Fermer le message');
        closeBtn.style.cssText = `
            position: absolute;
            top: 50%;
            right: 1rem;
            transform: translateY(-50%);
            background: none;
            border: none;
            color: inherit;
            font-size: 1.5rem;
            cursor: pointer;
            width: 30px;
            height: 30px;
        `;
        
        message.style.position = 'relative';
        message.appendChild(closeBtn);
        
        const hideMessage = () => {
            message.classList.add('hiding');
            setTimeout(() => message.remove(), 300);
        };
        
        closeBtn.addEventListener('click', hideMessage);
        
        // Auto-hide après 5s
        setTimeout(hideMessage, 5000);
    });
});

// ============================================
// 9. 3D TILT EFFECT - Optimisé avec RAF
// ============================================

if (window.matchMedia('(hover: hover)').matches && window.innerWidth > 768) {
    document.addEventListener('DOMContentLoaded', () => {
        const cards = document.querySelectorAll('.service-card, .product-card, .feature-card');
        
        cards.forEach(card => {
            let rafId = null;
            
            card.addEventListener('mousemove', (e) => {
                if (rafId) return; // Éviter trop d'appels
                
                rafId = requestAnimationFrame(() => {
                    const rect = card.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;
                    
                    const centerX = rect.width / 2;
                    const centerY = rect.height / 2;
                    
                    const rotateX = ((y - centerY) / centerY) * 5; // Réduit à 5deg max
                    const rotateY = ((centerX - x) / centerX) * 5;
                    
                    card.style.transform = `
                        perspective(1000px) 
                        rotateX(${rotateX}deg) 
                        rotateY(${rotateY}deg) 
                        scale3d(1.02, 1.02, 1.02)
                    `;
                    
                    rafId = null;
                });
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
            });
        });
    });
}

// ============================================
// 10. SCROLL TO TOP BUTTON
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    const scrollTopBtn = document.createElement('button');
    scrollTopBtn.innerHTML = '↑';
    scrollTopBtn.className = 'scroll-to-top';
    scrollTopBtn.setAttribute('aria-label', 'Retour en haut');
    scrollTopBtn.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, var(--primary-green), var(--light-green));
        color: white;
        border: none;
        border-radius: 50%;
        font-size: 1.5rem;
        cursor: pointer;
        z-index: 1000;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    `;
    
    document.body.appendChild(scrollTopBtn);
    
    // Toggle visibility
    const toggleButton = throttle(() => {
        if (window.pageYOffset > 300) {
            scrollTopBtn.classList.add('visible');
        } else {
            scrollTopBtn.classList.remove('visible');
        }
    }, 100);
    
    window.addEventListener('scroll', toggleButton, { passive: true });
    
    // Scroll to top
    scrollTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
});

// ============================================
// 11. LAZY LOADING IMAGES
// ============================================

if ('IntersectionObserver' in window) {
    document.addEventListener('DOMContentLoaded', () => {
        const images = document.querySelectorAll('img[data-src]');
        
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    img.classList.add('loaded');
                    imageObserver.unobserve(img);
                }
            });
        }, { rootMargin: '50px' });
        
        images.forEach(img => imageObserver.observe(img));
    });
}

// ============================================
// 12. PARALLAX - Optimisé avec RAF
// ============================================

if (window.matchMedia('(prefers-reduced-motion: no-preference)').matches) {
    let rafId = null;
    const parallaxElements = document.querySelectorAll('.parallax-section');
    
    if (parallaxElements.length > 0) {
        const handleParallax = () => {
            const scrolled = window.pageYOffset;
            
            parallaxElements.forEach(element => {
                const speed = parseFloat(element.dataset.speed) || 0.5;
                element.style.transform = `translate3d(0, ${scrolled * speed}px, 0)`;
            });
        };
        
        window.addEventListener('scroll', () => {
            if (!rafId) {
                rafId = requestAnimationFrame(() => {
                    handleParallax();
                    rafId = null;
                });
            }
        }, { passive: true });
    }
}

// ============================================
// 13. CUSTOM CURSOR - Desktop uniquement
// ============================================

if (window.matchMedia('(hover: hover) and (min-width: 1024px)').matches) {
    const cursor = document.createElement('div');
    cursor.className = 'custom-cursor';
    document.body.appendChild(cursor);
    
    let cursorX = 0, cursorY = 0;
    let cursorVisible = false;
    
    document.addEventListener('mousemove', (e) => {
        cursorX = e.clientX;
        cursorY = e.clientY;
        
        if (!cursorVisible) {
            cursor.style.opacity = '1';
            cursorVisible = true;
        }
        
        requestAnimationFrame(() => {
            cursor.style.left = cursorX + 'px';
            cursor.style.top = cursorY + 'px';
        });
    });
    
    // Hover sur éléments cliquables
    const clickables = document.querySelectorAll('a, button, [role="button"]');
    clickables.forEach(el => {
        el.addEventListener('mouseenter', () => cursor.classList.add('hover'));
        el.addEventListener('mouseleave', () => cursor.classList.remove('hover'));
    });
}

// ============================================
// 14. PREFETCH - Chargement anticipé
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    // Prefetch pages au hover des liens
    const links = document.querySelectorAll('a[href^="/"]');
    
    links.forEach(link => {
        link.addEventListener('mouseenter', function() {
            const href = this.getAttribute('href');
            if (href && !document.querySelector(`link[rel="prefetch"][href="${href}"]`)) {
                const prefetch = document.createElement('link');
                prefetch.rel = 'prefetch';
                prefetch.href = href;
                document.head.appendChild(prefetch);
            }
        }, { once: true });
    });
});

// ============================================
// 15. FOCUS TRAP - Accessibilité
// ============================================

const trapFocus = (element) => {
    const focusableElements = element.querySelectorAll(
        'a[href], button, textarea, input, select, [tabindex]:not([tabindex="-1"])'
    );
    const firstFocusable = focusableElements[0];
    const lastFocusable = focusableElements[focusableElements.length - 1];
    
    element.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
            if (e.shiftKey && document.activeElement === firstFocusable) {
                e.preventDefault();
                lastFocusable.focus();
            } else if (!e.shiftKey && document.activeElement === lastFocusable) {
                e.preventDefault();
                firstFocusable.focus();
            }
        }
    });
};

// Appliquer au menu mobile
document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelector('.nav-links');
    if (navLinks) {
        trapFocus(navLinks);
    }
});

// ============================================
// 16. PERFORMANCE MONITORING (Dev only)
// ============================================

if (window.location.hostname === 'localhost') {
    window.addEventListener('load', () => {
        setTimeout(() => {
            const perfData = performance.getEntriesByType('navigation')[0];
            console.log('🚀 Performance:', {
                'DOM Load': Math.round(perfData.domContentLoadedEventEnd - perfData.fetchStart) + 'ms',
                'Page Load': Math.round(perfData.loadEventEnd - perfData.fetchStart) + 'ms',
                'FCP': 'Use Lighthouse for this metric'
            });
        }, 0);
    });
}

// ============================================
// 17. CONSOLE SIGNATURE
// ============================================

console.log(
    '%c🌍 AgroBridge Africa',
    'color: #b8914f; font-size: 24px; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.2)'
);
console.log(
    '%cConnecting Africa\'s finest harvests to the world',
    'color: #2d5f3f; font-size: 14px;'
);

// ============================================
// SERVICE WORKER (Progressive Web App)
// ============================================

if ('serviceWorker' in navigator && window.location.protocol === 'https:') {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(reg => console.log('✅ Service Worker registered'))
            .catch(err => console.log('❌ SW registration failed:', err));
    });
}