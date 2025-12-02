// animations.js — small helpers: intersection observer + hero parallax
(function(){
    'use strict';

    // Respect reduced motion
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // IntersectionObserver for .animate-on-scroll and images
    function initObservers(){
        if(prefersReducedMotion) return;

        const ioOptions = { threshold: 0.12, rootMargin: '0px 0px -80px 0px' };

        const io = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                const el = entry.target;
                if(entry.isIntersecting){
                    // If element already animated, skip
                    if(!el.classList.contains('animated')){
                        // If parent list, compute index for stagger
                        let parent = el.parentElement;
                        let index = 0;
                        if(parent){
                            const children = Array.from(parent.querySelectorAll('.animate-on-scroll'));
                            index = children.indexOf(el);
                        }
                        el.style.setProperty('--stagger-index', index);
                        el.classList.add('animated');
                    }

                    // For images inside gallery/product, add visible
                    if(el.tagName === 'IMG') el.classList.add('visible');

                    io.unobserve(el);
                }
            });
        }, ioOptions);

        // Observe elements
        document.querySelectorAll('.animate-on-scroll').forEach(el => io.observe(el));
        // Also observe gallery/product images
        document.querySelectorAll('.gallery-item img, .product-image img').forEach(img => io.observe(img));
    }

    // Lightweight hero parallax: adjust background-position-y for .hero
    function initHeroParallax(){
        if(prefersReducedMotion) return;
        const hero = document.querySelector('.hero');
        if(!hero) return;

        let latestY = 0, ticking = false;

        function onScroll(){
            latestY = window.scrollY;
            requestTick();
        }
        function requestTick(){
            if(!ticking){
                requestAnimationFrame(update);
            }
            ticking = true;
        }
        function update(){
            const rect = hero.getBoundingClientRect();
            // only apply small effect while hero visible
            if(rect.bottom > 0){
                // compute percent scrolled within hero
                const heroHeight = Math.max(rect.height, 200);
                const scrolled = Math.min(Math.max((window.scrollY) / (heroHeight*1.5), 0), 1);
                // move background position a bit
                const pos = 50 - scrolled * 8; // from 50% to ~42%
                hero.style.backgroundPosition = `center ${pos}%`;
            }
            ticking = false;
        }

        window.addEventListener('scroll', onScroll, { passive: true });
    }

    // Initialize on DOM ready
    if(document.readyState === 'loading'){
        document.addEventListener('DOMContentLoaded', () => { initObservers(); initHeroParallax(); });
    } else {
        initObservers(); initHeroParallax();
    }
})();
