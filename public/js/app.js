/* ============================================================
   BHARATHHEALS — SHARED JAVASCRIPT  (v2026-04-05)
   ============================================================ */
console.log('[BharatHeals] app.js v2026-04-05 loaded');

(function () {
  'use strict';

  // ===== NAV SCROLL =====
  var nav = document.getElementById('mainNav');
  if (nav) {
    window.addEventListener('scroll', function () {
      nav.classList.toggle('scrolled', window.scrollY > 60);
    });
  }

  // ===== MOBILE MENU =====
  window.toggleMobile = function () {
    document.getElementById('mobileMenu').classList.toggle('active');
  };

  // ===== INTERSECTION OBSERVER =====
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });

  document.querySelectorAll('.stat-card, .animate-on-scroll').forEach(function (el, i) {
    el.style.animationDelay = (i * 0.12) + 's';
    observer.observe(el);
  });

  // ===== COUNTER ANIMATION =====
  function animateCounters() {
    document.querySelectorAll('.stat-num[data-target]').forEach(function (el) {
      if (el.dataset.animated) return;
      el.dataset.animated = 'true';
      var target = parseFloat(el.dataset.target);
      var suffix = el.dataset.suffix || '';
      var isDecimal = el.dataset.decimal === 'true';
      var duration = 1500;
      var start = performance.now();

      function update(now) {
        var progress = Math.min((now - start) / duration, 1);
        var eased = 1 - Math.pow(1 - progress, 3);
        var current = target * eased;
        el.textContent = isDecimal ? current.toFixed(1) + suffix : Math.round(current) + suffix;
        if (progress < 1) requestAnimationFrame(update);
      }
      requestAnimationFrame(update);
    });
  }

  var heroVisual = document.querySelector('.hero-visual');
  if (heroVisual) {
    var counterObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { animateCounters(); counterObs.unobserve(entry.target); }
      });
    }, { threshold: 0.3 });
    counterObs.observe(heroVisual);
  }

  // ===== COST BAR ANIMATION =====
  var costCompare = document.getElementById('costCompare');
  if (costCompare) {
    var barObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.querySelectorAll('.cost-bar-fill').forEach(function (bar) {
            bar.style.width = bar.dataset.width + '%';
          });
          barObs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.2 });
    barObs.observe(costCompare);
  }

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

    // Replace "Account" link in desktop nav with user profile pill
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

    // Replace "Account" link in mobile menu
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

    // Welcome banner below nav
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

    // Welcome toast on first load after login
    if (!localStorage.getItem('bharatheals_welcomed')) {
      localStorage.setItem('bharatheals_welcomed', '1');
      setTimeout(function() { showToast('Welcome, ' + firstName + '! You are now signed in.', 'success'); }, 400);
    }
  }

  // ===== SCROLL REVEAL (luxury animations) =====
  var luxRevealObs = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('lux-in-view');
        luxRevealObs.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('.lux-reveal-up, .lux-reveal-left, .lux-reveal-right, .lux-reveal-scale').forEach(function (el) {
    luxRevealObs.observe(el);
  });

  document.querySelectorAll('.section-tag, .section-title, .section-lead').forEach(function (el) {
    if (!el.classList.contains('lux-reveal-up')) {
      el.classList.add('lux-reveal-up');
      luxRevealObs.observe(el);
    }
  });

  // ===== SMOOTH SCROLL =====
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      var href = this.getAttribute('href');
      if (href === '#') return;
      var target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

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

})();
