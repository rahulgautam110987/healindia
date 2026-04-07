/* ============================================================
   BHARATHEALS — SHARED JAVASCRIPT  (v2026-04-07 · GSAP Premium)
   ============================================================ */
console.log('[BharatHeals] app.js v2026-04-07-gsap loaded');

(function () {
  'use strict';

  /* ----------------------------------------------------------
     0. GSAP SETUP
  ---------------------------------------------------------- */
  var hasGsap = typeof gsap !== 'undefined';
  var prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var mm;

  if (!hasGsap) {
    console.warn('[BharatHeals] GSAP not loaded — animations disabled');
    bootstrapNoGsap();
  } else {
    gsap.registerPlugin(ScrollTrigger, ScrollToPlugin);
    gsap.defaults({ ease: 'power3.out', duration: 0.8 });
    mm = gsap.matchMedia();
  }

  /* ----------------------------------------------------------
     1. NAV SCROLL
  ---------------------------------------------------------- */
  var nav = document.getElementById('mainNav');
  if (nav && hasGsap) {
    ScrollTrigger.create({
      start: 60,
      onUpdate: function (self) {
        nav.classList.toggle('scrolled', self.scroll() > 60);
      }
    });
  } else if (nav) {
    window.addEventListener('scroll', function () {
      nav.classList.toggle('scrolled', window.scrollY > 60);
    });
  }

  /* ----------------------------------------------------------
     2. MOBILE MENU
  ---------------------------------------------------------- */
  window.toggleMobile = function () {
    document.getElementById('mobileMenu').classList.toggle('active');
  };

  /* ----------------------------------------------------------
     3. HERO ENTRANCE SEQUENCE
  ---------------------------------------------------------- */
  var hero = document.querySelector('.hero');
  if (hero && hasGsap && !prefersReduced) {
    var tl = gsap.timeline({ defaults: { ease: 'power4.out' } });

    // Split hero heading words for stagger
    var h1 = hero.querySelector('h1');
    if (h1) {
      var origHTML = h1.innerHTML;
      var lines = origHTML.split(/<em>|<\/em>/);
      var rebuilt = '';
      for (var li = 0; li < lines.length; li++) {
        var isEm = li % 2 === 1;
        var words = lines[li].trim().split(/\s+/);
        for (var wi = 0; wi < words.length; wi++) {
          if (words[wi]) {
            rebuilt += (isEm ? '<em>' : '') +
              '<span class="bh-word" style="display:inline-block;opacity:0;transform:translateY(40px)">' +
              words[wi] + '</span>' +
              (isEm ? '</em>' : '') + ' ';
          }
        }
      }
      h1.innerHTML = rebuilt;
    }

    tl.set(hero, { visibility: 'visible' });

    // Nav entrance
    tl.from(nav, { y: -80, opacity: 0, duration: 0.6, ease: 'power2.out' }, 0);

    // Eyebrow
    var eyebrow = hero.querySelector('.hero-eyebrow');
    if (eyebrow) tl.from(eyebrow, { opacity: 0, x: -30, duration: 0.5 }, 0.2);

    // Words stagger
    var words = hero.querySelectorAll('.bh-word');
    if (words.length) {
      tl.to(words, {
        opacity: 1, y: 0, duration: 0.6,
        stagger: 0.06, ease: 'back.out(1.4)'
      }, 0.35);
    }

    // Subtitle
    var heroSub = hero.querySelector('.hero-sub');
    if (heroSub) tl.from(heroSub, { opacity: 0, y: 20, duration: 0.6 }, 0.7);

    // CTA buttons
    var heroActions = hero.querySelectorAll('.hero-actions > *');
    if (heroActions.length) {
      tl.from(heroActions, { opacity: 0, y: 20, stagger: 0.1, duration: 0.5 }, 0.9);
    }

    // Stat cards fly in from different directions
    var statCards = hero.querySelectorAll('.stat-card');
    if (statCards.length) {
      gsap.set(statCards, { opacity: 1, transform: 'none' });
      statCards.forEach(function (card, i) {
        card.style.opacity = '0';
        var fromX = (i % 2 === 0) ? 60 : -60;
        var fromY = (i < 2) ? -40 : 40;
        tl.from(card, {
          opacity: 0, x: fromX, y: fromY, scale: 0.85,
          duration: 0.7, ease: 'back.out(1.2)'
        }, 1.0 + i * 0.12);
      });
    }
  }

  /* ----------------------------------------------------------
     4. SCROLL-TRIGGERED SECTION REVEALS
  ---------------------------------------------------------- */
  if (hasGsap && !prefersReduced) {
    // Section headers
    gsap.utils.toArray('section, .calc-page-hero, .hosp-hero, .pj-hero').forEach(function (section) {
      var headers = section.querySelectorAll('.section-tag, .section-title, .section-lead');
      if (headers.length) {
        gsap.from(headers, {
          scrollTrigger: {
            trigger: section,
            start: 'top 85%',
            toggleActions: 'play none none none'
          },
          y: 40, opacity: 0, duration: 0.7,
          stagger: 0.12
        });
      }
    });

    // Card grids with stagger
    var gridSelectors = [
      '.specialties-grid', '.doctors-grid', '.hospital-grid',
      '.testimonials-grid', '.gallery-grid', '.logistics-grid',
      '.aus-grid', '.process-steps', '.hosp-list'
    ];
    gridSelectors.forEach(function (sel) {
      gsap.utils.toArray(sel).forEach(function (grid) {
        var children = grid.children;
        if (!children.length) return;
        gsap.from(children, {
          scrollTrigger: {
            trigger: grid,
            start: 'top 85%',
            toggleActions: 'play none none none'
          },
          y: 50, opacity: 0, scale: 0.95, rotateX: 4,
          duration: 0.65,
          stagger: { amount: 0.5, from: 'start' }
        });
      });
    });

    // Individual elements
    gsap.utils.toArray('.why-item, .faq-item, .pricing-card, .trust-bar, .consult-banner, .pj-card').forEach(function (el) {
      gsap.from(el, {
        scrollTrigger: { trigger: el, start: 'top 88%' },
        y: 30, opacity: 0, duration: 0.6
      });
    });

    // Process step connector line draw
    var processLine = document.querySelector('.process-steps::before');
    var processSection = document.querySelector('.process-steps');
    if (processSection) {
      gsap.from(processSection, {
        scrollTrigger: { trigger: processSection, start: 'top 80%' },
        '--line-scale': 0, duration: 1.2, ease: 'power2.inOut'
      });
    }
  }

  /* ----------------------------------------------------------
     5. PARALLAX EFFECTS
  ---------------------------------------------------------- */
  if (hasGsap && !prefersReduced) {
    mm.add('(min-width: 768px)', function () {
      // Hero background depth
      var heroBg = document.querySelector('.hero-bg');
      var heroPattern = document.querySelector('.hero-pattern');
      if (heroBg) {
        gsap.to(heroBg, {
          scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: 1 },
          y: 120, ease: 'none'
        });
      }
      if (heroPattern) {
        gsap.to(heroPattern, {
          scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: 1 },
          y: 60, ease: 'none'
        });
      }

      // Cost comparison parallax
      var whyVisual = document.querySelector('.why-visual');
      if (whyVisual) {
        gsap.to(whyVisual, {
          scrollTrigger: { trigger: whyVisual, start: 'top bottom', end: 'bottom top', scrub: 1 },
          y: -40, ease: 'none'
        });
      }

      // Consult banner parallax
      var consultBanner = document.querySelector('.consult-banner');
      if (consultBanner) {
        gsap.to(consultBanner.querySelector('.consult-inner'), {
          scrollTrigger: { trigger: consultBanner, start: 'top bottom', end: 'bottom top', scrub: 1 },
          y: -20, ease: 'none'
        });
      }
    });
  }

  /* ----------------------------------------------------------
     6. ANIMATED NUMBER COUNTERS (site-wide)
  ---------------------------------------------------------- */
  if (hasGsap) { // begin GSAP-dependent block

  function animateCounter(el) {
    if (el.dataset.bhAnimated) return;
    el.dataset.bhAnimated = '1';

    var target, suffix, prefix, hasDecimal, decimalPlaces, hasCommas;

    // data-target elements (hero stat cards)
    if (el.dataset.target) {
      target = parseFloat(el.dataset.target);
      suffix = el.dataset.suffix || '';
      prefix = '';
      hasDecimal = el.dataset.decimal === 'true';
      decimalPlaces = hasDecimal ? 1 : 0;
      hasCommas = target >= 1000;
    } else {
      // Parse from rendered text
      var text = el.textContent.trim();
      var match = text.match(/([\d,.]+)/);
      if (!match) return;
      var numStr = match[1].replace(/,/g, '');
      target = parseFloat(numStr);
      if (isNaN(target) || target === 0) return;
      prefix = text.substring(0, text.indexOf(match[1]));
      suffix = text.substring(text.indexOf(match[1]) + match[1].length);
      hasDecimal = numStr.indexOf('.') !== -1;
      decimalPlaces = hasDecimal ? (numStr.split('.')[1] || '').length : 0;
      hasCommas = match[1].indexOf(',') !== -1;
    }

    var proxy = { val: 0 };
    gsap.to(proxy, {
      val: target,
      duration: 1.8,
      ease: 'power2.out',
      scrollTrigger: { trigger: el, start: 'top 90%' },
      onUpdate: function () {
        var v = proxy.val;
        var formatted;
        if (hasDecimal) {
          formatted = v.toFixed(decimalPlaces);
        } else {
          formatted = Math.round(v).toString();
        }
        if (hasCommas) {
          formatted = Number(formatted).toLocaleString('en-US', {
            minimumFractionDigits: decimalPlaces,
            maximumFractionDigits: decimalPlaces
          });
        }
        el.textContent = prefix + formatted + suffix;
      }
    });
  }

  // Counter selectors — stat cards, impact numbers, hospital meta, doctor stats
  var counterSelectors = [
    '.stat-num', '.hosp-stat-item .num', '.hosp-meta-item .num',
    '.doctor-stat .num', '.pj-stat .num',
    '.impact-num', '.strip-num'
  ];
  counterSelectors.forEach(function (sel) {
    document.querySelectorAll(sel).forEach(function (el) {
      animateCounter(el);
    });
  });

  /* ----------------------------------------------------------
     7. COST BAR ANIMATION (GSAP-powered)
  ---------------------------------------------------------- */
  var costCompare = document.getElementById('costCompare');
  if (costCompare) {
    costCompare.querySelectorAll('.cost-bar-fill').forEach(function (bar) {
      var w = bar.dataset.width;
      if (w) {
        gsap.fromTo(bar, { width: '0%' }, {
          width: w + '%',
          duration: 1.2,
          ease: 'power2.out',
          scrollTrigger: { trigger: costCompare, start: 'top 75%' }
        });
      }
    });
  }

  /* ----------------------------------------------------------
     8. TESTIMONIAL CAROUSEL
  ---------------------------------------------------------- */
  var testimGrid = document.querySelector('.testimonials-grid');
  if (testimGrid) {
    var cards = Array.from(testimGrid.querySelectorAll('.testimonial-card'));
    if (cards.length > 3) {
      var currentSet = 0;
      var setsOf3 = Math.ceil(cards.length / 3);
      var autoTimer;

      // Create dot navigation
      var dotsWrap = document.createElement('div');
      dotsWrap.style.cssText = 'text-align:center;margin-top:1.5rem;display:flex;justify-content:center;gap:0.5rem;';
      for (var d = 0; d < setsOf3; d++) {
        var dot = document.createElement('button');
        dot.style.cssText = 'width:10px;height:10px;border-radius:50%;border:1.5px solid var(--gold);background:' + (d === 0 ? 'var(--gold)' : 'transparent') + ';cursor:pointer;transition:all 0.3s;padding:0;';
        dot.dataset.idx = d;
        dot.addEventListener('click', function () { goToSet(parseInt(this.dataset.idx)); });
        dotsWrap.appendChild(dot);
      }
      testimGrid.parentNode.insertBefore(dotsWrap, testimGrid.nextSibling);

      function goToSet(idx) {
        currentSet = idx;
        cards.forEach(function (c, i) {
          var inSet = Math.floor(i / 3) === idx;
          gsap.to(c, {
            opacity: inSet ? 1 : 0,
            scale: inSet ? 1 : 0.92,
            y: inSet ? 0 : 20,
            duration: 0.5,
            ease: 'power2.inOut',
            onComplete: function () {
              c.style.display = inSet ? '' : 'none';
            }
          });
          if (inSet) c.style.display = '';
        });
        dotsWrap.querySelectorAll('button').forEach(function (dt, di) {
          dt.style.background = di === idx ? 'var(--gold)' : 'transparent';
        });
      }

      function autoRotate() {
        autoTimer = setInterval(function () {
          goToSet((currentSet + 1) % setsOf3);
        }, 5000);
      }

      testimGrid.addEventListener('mouseenter', function () { clearInterval(autoTimer); });
      testimGrid.addEventListener('mouseleave', autoRotate);

      goToSet(0);
      autoRotate();
    }
  }

  /* ----------------------------------------------------------
     9. MAGNETIC HOVER ON BUTTONS
  ---------------------------------------------------------- */
  if (hasGsap && !prefersReduced) {
    mm.add('(hover: hover) and (min-width: 768px)', function () {
      document.querySelectorAll('.btn-primary, .nav-cta, .consult-btn, .cta-btn').forEach(function (btn) {
        btn.addEventListener('mousemove', function (e) {
          var rect = btn.getBoundingClientRect();
          var x = e.clientX - rect.left - rect.width / 2;
          var y = e.clientY - rect.top - rect.height / 2;
          gsap.to(btn, { x: x * 0.25, y: y * 0.25, duration: 0.3, ease: 'power2.out' });
        });
        btn.addEventListener('mouseleave', function () {
          gsap.to(btn, { x: 0, y: 0, duration: 0.5, ease: 'elastic.out(1, 0.4)' });
        });
      });

      // Cursor-tracking tilt on premium cards
      document.querySelectorAll('.specialty-card, .doctor-card, .hospital-card, .testimonial-card, .gallery-card').forEach(function (card) {
        card.addEventListener('mousemove', function (e) {
          var rect = card.getBoundingClientRect();
          var cx = e.clientX - rect.left;
          var cy = e.clientY - rect.top;
          var px = (cx / rect.width - 0.5) * 2;
          var py = (cy / rect.height - 0.5) * 2;
          gsap.to(card, {
            rotateY: px * 6, rotateX: -py * 6,
            duration: 0.4, ease: 'power2.out',
            transformPerspective: 800
          });
        });
        card.addEventListener('mouseleave', function () {
          gsap.to(card, {
            rotateY: 0, rotateX: 0, scale: 1,
            duration: 0.6, ease: 'elastic.out(1, 0.5)'
          });
        });
      });
    });
  }

  /* ----------------------------------------------------------
     10. SMOOTH SCROLL (GSAP ScrollToPlugin or native fallback)
  ---------------------------------------------------------- */
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      var href = this.getAttribute('href');
      if (href === '#') return;
      var target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        if (hasGsap) {
          gsap.to(window, {
            scrollTo: { y: target, offsetY: 80 },
            duration: 1,
            ease: 'power3.inOut'
          });
        } else {
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }
    });
  });

  /* ----------------------------------------------------------
     11. PAGE ENTRANCE (non-hero pages)
  ---------------------------------------------------------- */
  if (hasGsap && !hero && !prefersReduced) {
    var pageHero = document.querySelector('.calc-page-hero, .hosp-hero, .pj-hero');
    if (pageHero) {
      gsap.from(pageHero, { opacity: 0, y: -20, duration: 0.6, delay: 0.1 });
    }
    if (nav) {
      gsap.from(nav, { y: -60, opacity: 0, duration: 0.5 });
    }
  }

  /* ----------------------------------------------------------
     12. SCORE BAR ANIMATION (doctor pages)
  ---------------------------------------------------------- */
  document.querySelectorAll('.score-fill').forEach(function (bar) {
    var w = bar.style.width;
    if (w) {
      gsap.fromTo(bar, { width: '0%' }, {
        width: w,
        duration: 1,
        ease: 'power2.out',
        scrollTrigger: { trigger: bar, start: 'top 90%' }
      });
    }
  });

  } // end GSAP-dependent block

  /* ----------------------------------------------------------
     SHARED UTILITIES (preserved from v1)
  ---------------------------------------------------------- */

  // ===== CONSULTATION MODAL =====
  window.openConsultModal = function (treatment) {
    var modal = document.getElementById('consultModal');
    if (!modal) return;
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    if (treatment) document.getElementById('consTreatment').value = treatment;
    document.getElementById('consultForm').style.display = '';
    document.getElementById('consultSuccess').classList.remove('active');
    var btn = document.getElementById('consultSubmitBtn');
    btn.disabled = false;
    btn.textContent = 'Book My Free Consultation \u2192';
  };

  window.closeConsultModal = function () {
    var modal = document.getElementById('consultModal');
    if (modal) modal.classList.remove('active');
    document.body.style.overflow = '';
  };

  var consultModal = document.getElementById('consultModal');
  if (consultModal) {
    consultModal.addEventListener('click', function (e) {
      if (e.target === this) closeConsultModal();
    });
  }
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeConsultModal();
  });

  // ===== CONSULTATION FORM SUBMIT =====
  var consultForm = document.getElementById('consultForm');
  if (consultForm) {
    consultForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var btn = document.getElementById('consultSubmitBtn');
      btn.disabled = true;
      btn.textContent = 'Booking...';

      var fd = new FormData(this);
      var data = {};
      fd.forEach(function (v, k) { data[k] = v; });

      fetch('/api/consultations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })
        .then(function (r) { return r.json(); })
        .then(function (result) {
          if (result.success) {
            document.getElementById('consultForm').style.display = 'none';
            document.getElementById('consultSuccess').classList.add('active');
            showToast('Consultation booked successfully!', 'success');
          } else {
            showToast(result.error || 'Something went wrong.', 'error');
            btn.disabled = false;
            btn.textContent = 'Book My Free Consultation \u2192';
          }
        })
        .catch(function () {
          showToast('Network error. Please try again.', 'error');
          btn.disabled = false;
          btn.textContent = 'Book My Free Consultation \u2192';
        });
    });
  }

  // ===== CTA FORM SUBMIT =====
  var ctaForm = document.getElementById('ctaForm');
  if (ctaForm) {
    ctaForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var fd = new FormData(this);
      var data = {};
      fd.forEach(function (v, k) { data[k] = v; });
      document.querySelectorAll('[form="ctaForm"]').forEach(function (input) {
        if (input.name && input.value) data[input.name] = input.value;
      });

      fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })
        .then(function (r) { return r.json(); })
        .then(function (result) {
          if (result.success) {
            showToast(result.message, 'success');
            ctaForm.reset();
            document.querySelectorAll('[form="ctaForm"]').forEach(function (i) { i.value = ''; });
          } else {
            showToast(result.error || 'Something went wrong.', 'error');
          }
        })
        .catch(function () {
          showToast('Network error. Please try again.', 'error');
        });
    });
  }

  // ===== FAQ ACCORDION =====
  document.querySelectorAll('.faq-question').forEach(function (q) {
    q.addEventListener('click', function () {
      var item = this.closest('.faq-item');
      var wasActive = item.classList.contains('active');
      document.querySelectorAll('.faq-item').forEach(function (i) { i.classList.remove('active'); });
      if (!wasActive) item.classList.add('active');
    });
  });

  // ===== TOAST =====
  var toastTimeout;
  window.showToast = function (msg, type) {
    var toast = document.getElementById('toast');
    if (!toast) return;
    toast.textContent = msg;
    toast.className = 'toast ' + (type || 'success');
    clearTimeout(toastTimeout);
    requestAnimationFrame(function () { toast.classList.add('active'); });
    toastTimeout = setTimeout(function () { toast.classList.remove('active'); }, 4000);
  };

  // ===== AUTH STATE =====
  window.getAuthToken = function () { return localStorage.getItem('bharatheals_token'); };
  window.getAuthUser = function () { try { return JSON.parse(localStorage.getItem('bharatheals_user')); } catch(e) { return null; } };
  window.logout = function () {
    localStorage.removeItem('bharatheals_token');
    localStorage.removeItem('bharatheals_user');
    localStorage.removeItem('bharatheals_welcomed');
    window.location.href = '/';
  };

  var user = window.getAuthUser();
  if (user) {
    var firstName = user.name ? user.name.split(' ')[0] : 'User';

    document.querySelectorAll('.nav-links a[href="/login.html"]').forEach(function (link) {
      var li = link.parentElement;
      if (!li) return;
      var pill = document.createElement('div');
      pill.className = 'hi-user-pill';
      pill.style.cssText = 'display:flex;align-items:center;gap:8px;cursor:pointer;padding:5px 14px 5px 6px;border-radius:30px;background:rgba(198,163,91,0.15);border:1.5px solid rgba(198,163,91,0.4);transition:all 0.25s;';
      pill.onmouseenter = function() { this.style.background = 'rgba(198,163,91,0.3)'; };
      pill.onmouseleave = function() { this.style.background = 'rgba(198,163,91,0.15)'; };

      if (user.avatar) {
        pill.innerHTML = '<img src="' + user.avatar + '" alt="' + firstName + '" style="width:26px;height:26px;border-radius:50%;border:1.5px solid rgba(198,163,91,0.6);">' +
          '<span style="color:#fff;font-size:0.78rem;font-weight:600;letter-spacing:0.04em;">' + firstName + '</span>' +
          '<span style="font-size:10px;color:rgba(255,255,255,0.4);margin-left:2px;">\u25BE</span>';
      } else {
        var initials = (user.name || 'U').split(' ').map(function(w){return w[0];}).join('').substring(0,2).toUpperCase();
        pill.innerHTML = '<div style="width:26px;height:26px;border-radius:50%;background:linear-gradient(135deg,#c6a35b,#e8c367);display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:800;color:#0a1628;">' + initials + '</div>' +
          '<span style="color:#fff;font-size:0.78rem;font-weight:600;letter-spacing:0.04em;">' + firstName + '</span>' +
          '<span style="font-size:10px;color:rgba(255,255,255,0.4);margin-left:2px;">\u25BE</span>';
      }

      pill.setAttribute('data-logged-in', 'true');
      pill.title = 'Logged in as ' + user.email;
      pill.onclick = function(e) {
        e.preventDefault();
        e.stopPropagation();
        window.location.href = '/dashboard.html';
      };
      li.innerHTML = '';
      li.appendChild(pill);
    });

    document.querySelectorAll('.mobile-menu a[href="/login.html"]').forEach(function (link) {
      if (user.avatar) {
        link.innerHTML = '<img src="' + user.avatar + '" style="width:22px;height:22px;border-radius:50%;vertical-align:middle;margin-right:6px;border:1.5px solid rgba(198,163,91,0.6);">' +
          '<span style="vertical-align:middle;">Hi, ' + firstName + '</span>';
      } else {
        link.textContent = 'Hi, ' + firstName;
      }
      link.href = 'javascript:void(0)';
      link.setAttribute('data-logged-in', 'true');
      link.onclick = function(e) {
        e.preventDefault();
        if (confirm('Logout from BharatHeals?')) window.logout();
      };
    });

    console.log('[BharatHeals] User logged in:', user.name, user.email);
    var navEl = document.getElementById('mainNav');
    if (navEl) {
      var banner = document.createElement('div');
      banner.id = 'hi-welcome-banner';
      banner.style.cssText = 'background:linear-gradient(135deg,#c6a35b,#e8c367);color:#0a1628;text-align:center;padding:8px 16px;font-size:13px;font-weight:600;font-family:DM Sans,sans-serif;letter-spacing:0.02em;position:relative;z-index:9998;';
      var welcomeText = 'Welcome, ' + user.name + '!';
      if (user.email) welcomeText += '  |  ' + user.email;
      welcomeText += '  |  ';
      banner.innerHTML = welcomeText + '<a href="javascript:void(0)" onclick="window.logout()" style="color:#0a1628;text-decoration:underline;font-weight:700;">Logout</a>';
      navEl.parentNode.insertBefore(banner, navEl.nextSibling);
    }

    if (!localStorage.getItem('bharatheals_welcomed')) {
      localStorage.setItem('bharatheals_welcomed', '1');
      setTimeout(function() { showToast('Welcome, ' + firstName + '! You are now signed in.', 'success'); }, 400);
    }
  }

  // ===== MINI CALCULATOR =====
  var calcSelect = document.getElementById('calcTreatment');
  var calcCurrency = document.getElementById('calcCurrency');
  if (calcSelect) {
    var prices = {
      'hair-fue-2000':   { au: 12000, us: 10000, uk: 8000, india: 1200 },
      'hair-fue-3000':   { au: 16000, us: 15000, uk: 10000, india: 1500 },
      'hair-dhi-3500':   { au: 20000, us: 18000, uk: 14000, india: 2200 },
      'dental-implant':  { au: 5500, us: 5000, uk: 3000, india: 500 },
      'dental-veneer':   { au: 2000, us: 1800, uk: 1200, india: 250 },
      'dental-allon4':   { au: 25000, us: 24000, uk: 18000, india: 3500 },
      'dental-fullmouth':{ au: 35000, us: 30000, uk: 22000, india: 5000 },
      'cardiac-bypass':  { au: 80000, us: 120000, uk: 50000, india: 7000 },
      'knee-replace':    { au: 35000, us: 40000, uk: 18000, india: 5500 },
      'hip-replace':     { au: 38000, us: 40000, uk: 18000, india: 5500 },
      'ivf':             { au: 12000, us: 15000, uk: 8000, india: 2500 },
      'lasik':           { au: 4000, us: 4500, uk: 3000, india: 800 },
      'liver-transplant':{ au: 150000, us: 300000, uk: 120000, india: 30000 },
      'kidney-transplant':{ au: 80000, us: 150000, uk: 60000, india: 12000 },
    };

    var symbols = { usd: '$', gbp: '\u00A3', aud: 'A$', sar: 'SAR ', aed: 'AED ' };
    var rates = { usd: 0.65, gbp: 0.52, aud: 1, sar: 2.44, aed: 2.39 };

    function updateCalc() {
      var key = calcSelect.value;
      var curr = calcCurrency ? calcCurrency.value : 'aud';
      var sym = symbols[curr];
      var rate = rates[curr];
      var result = document.getElementById('calcResult');
      if (!key || !prices[key]) {
        if (result) result.style.display = 'none';
        return;
      }
      var p = prices[key];
      var homePrice = Math.round(p.au * rate);
      var indiaPrice = Math.round(p.india * rate);
      var savings = homePrice - indiaPrice;

      if (result) {
        result.style.display = '';
        document.getElementById('calcSavings').textContent = sym + savings.toLocaleString();
        document.getElementById('calcHome').textContent = sym + homePrice.toLocaleString();
        document.getElementById('calcIndia').textContent = sym + indiaPrice.toLocaleString();
        var pct = Math.round((savings / homePrice) * 100);
        document.getElementById('calcPct').textContent = pct + '% savings';
      }
    }

    calcSelect.addEventListener('change', updateCalc);
    if (calcCurrency) calcCurrency.addEventListener('change', updateCalc);
  }

  /* ----------------------------------------------------------
     FALLBACK (no GSAP)
  ---------------------------------------------------------- */
  function bootstrapNoGsap() {
    var nav = document.getElementById('mainNav');
    if (nav) {
      window.addEventListener('scroll', function () {
        nav.classList.toggle('scrolled', window.scrollY > 60);
      });
    }
    window.toggleMobile = function () {
      document.getElementById('mobileMenu').classList.toggle('active');
    };
    document.querySelectorAll('a[href^="#"]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        var t = document.querySelector(this.getAttribute('href'));
        if (t) { e.preventDefault(); t.scrollIntoView({ behavior: 'smooth' }); }
      });
    });
  }

})();
