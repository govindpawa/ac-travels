(function () {
    'use strict';

    var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // Dynamic copyright year
    var yearEl = document.getElementById('year');
    if (yearEl) yearEl.textContent = new Date().getFullYear();

    // Set min date to today on all date inputs
    var todayStr = new Date().toISOString().split('T')[0];
    document.querySelectorAll('input[type="date"]').forEach(function (el) { el.min = todayStr; });

    // Smooth scrolling + close mobile nav
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            var target = document.querySelector(this.getAttribute('href'));
            if (!target) return;
            e.preventDefault();
            var headerOffset = 70;
            var top = target.getBoundingClientRect().top + window.scrollY - headerOffset;
            window.scrollTo({ top: top, behavior: prefersReducedMotion ? 'auto' : 'smooth' });
            document.querySelector('.nav').classList.remove('active');
        });
    });

    // Back to top button visibility + header shrink/blur on scroll
    var backToTop = document.getElementById('backToTop');
    var header = document.getElementById('header');
    window.addEventListener('scroll', function () {
        if (backToTop) backToTop.classList.toggle('visible', window.scrollY > 400);
        if (header) header.classList.toggle('is-scrolled', window.scrollY > 30);
    }, { passive: true });

    // Scrollspy - highlight nav link for section in view
    var navLinks = Array.prototype.slice.call(document.querySelectorAll('.nav a[href^="#"]'));
    var sections = navLinks
        .map(function (link) { return document.querySelector(link.getAttribute('href')); })
        .filter(Boolean);

    if ('IntersectionObserver' in window && sections.length) {
        var spy = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                var link = navLinks.find(function (l) { return l.getAttribute('href') === '#' + entry.target.id; });
                if (!link) return;
                if (entry.isIntersecting) {
                    navLinks.forEach(function (l) { l.classList.remove('active-link'); });
                    link.classList.add('active-link');
                }
            });
        }, { rootMargin: '-45% 0px -50% 0px' });
        sections.forEach(function (s) { spy.observe(s); });
    }

    // Scroll-reveal animations
    var revealSelector = [
        '.section-title', '.section-subtitle',
        '.service-card', '.fleet-card', '.fleet-category',
        '.gallery-img', '.why-card', '.stats-row',
        '.about-content > *', '.contact-form', '.contact-info',
        '.quote-card'
    ].join(', ');

    var revealEls = Array.prototype.slice.call(document.querySelectorAll(revealSelector));
    revealEls.forEach(function (el) { el.classList.add('reveal'); });

    if ('IntersectionObserver' in window && !prefersReducedMotion) {
        // Assign a stagger index per parent so siblings cascade in.
        var parentCounters = new Map();
        revealEls.forEach(function (el) {
            var parent = el.parentElement;
            var count = parentCounters.get(parent) || 0;
            el.style.setProperty('--stagger', count % 8);
            parentCounters.set(parent, count + 1);
        });

        var revealObserver = new IntersectionObserver(function (entries, obs) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('in-view');
                    obs.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15, rootMargin: '0px 0px -8% 0px' });

        revealEls.forEach(function (el) { revealObserver.observe(el); });
    } else {
        revealEls.forEach(function (el) { el.classList.add('in-view'); });
    }

    // Animated stat counters
    var counters = document.querySelectorAll('.stat-number[data-count]');
    function animateCounter(el) {
        var target = parseInt(el.getAttribute('data-count'), 10) || 0;
        if (prefersReducedMotion) { el.textContent = target + '+'; return; }
        var duration = 1400;
        var start = null;
        function step(ts) {
            if (start === null) start = ts;
            var progress = Math.min((ts - start) / duration, 1);
            var eased = 1 - Math.pow(1 - progress, 3);
            el.textContent = Math.round(eased * target) + '+';
            if (progress < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
    }

    if ('IntersectionObserver' in window && counters.length) {
        var statObserver = new IntersectionObserver(function (entries, obs) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    obs.unobserve(entry.target);
                }
            });
        }, { threshold: 0.6 });
        counters.forEach(function (c) { statObserver.observe(c); });
    }

    // Card tilt removed: the Bugatti system has no decorative depth (see DESIGN.md)
    var isTouch = window.matchMedia('(hover: none)').matches;
    if (!isTouch && !prefersReducedMotion) {
        // Magnetic buttons
        document.querySelectorAll('.magnetic').forEach(function (btn) {
            btn.addEventListener('mousemove', function (e) {
                var rect = btn.getBoundingClientRect();
                var x = e.clientX - rect.left - rect.width / 2;
                var y = e.clientY - rect.top - rect.height / 2;
                btn.style.transform = 'translate(' + (x * 0.18).toFixed(1) + 'px, ' + (y * 0.35).toFixed(1) + 'px)';
            });
            btn.addEventListener('mouseleave', function () {
                btn.style.transform = '';
            });
        });
    }

    // Quick-quote trip-type tabs
    document.querySelectorAll('.quote-tab').forEach(function (tab) {
        tab.addEventListener('click', function () {
            var group = tab.closest('.quote-tabs');
            group.querySelectorAll('.quote-tab').forEach(function (t) { t.classList.remove('active'); });
            tab.classList.add('active');
            var form = group.parentElement.querySelector('.quote-form');
            if (form) form.tripType.value = tab.getAttribute('data-trip');
        });
    });

    // Quick-quote submission via WhatsApp
    window.handleQuoteSubmit = function (e) {
        e.preventDefault();
        var form = e.target;
        var tripType = form.tripType.value;
        var pickup = form.pickup.value.trim();
        var drop = form.drop.value.trim();
        var date = form.date.value;

        var text = 'Hi, I want a quote for a ride.\n\nTrip Type: ' + tripType +
            '\nPickup: ' + pickup + '\nDrop: ' + drop + '\nDate: ' + date;

        window.open('https://wa.me/919945498275?text=' + encodeURIComponent(text), '_blank');
    };

    // Form submission via WhatsApp
    window.handleSubmit = function (e) {
        e.preventDefault();
        var form = e.target;
        var name = form.name.value.trim();
        var phone = form.phone.value.trim();
        var pickup = form.pickup.value.trim();
        var drop = form.drop.value.trim();
        var date = form.date.value;
        var vehicle = form.vehicle.value;
        var message = form.message.value.trim();

        var text = 'Hi, I want to book a ride.\n\nName: ' + name + '\nPhone: ' + phone +
            '\nPickup: ' + pickup + '\nDrop: ' + drop + '\nDate: ' + date +
            '\nVehicle: ' + vehicle + '\nNote: ' + message;

        window.open('https://wa.me/919945498275?text=' + encodeURIComponent(text), '_blank');
    };
})();
