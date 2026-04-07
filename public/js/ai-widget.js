/* ============================================================
   BHARATHHEALS — FLOATING AI AGENT WIDGET
   Self-contained: injects its own HTML + CSS, manages state.
   Include on any page: <script src="/js/ai-widget.js"></script>
   ============================================================ */
(function () {
  'use strict';

  // ── CSS ──────────────────────────────────────────────────
  var css = `
  #hi-ai-fab{position:fixed;bottom:28px;right:28px;z-index:99999;width:64px;height:64px;border-radius:50%;background:linear-gradient(135deg,#0a1628 0%,#162a4a 100%);box-shadow:0 6px 28px rgba(10,22,40,.45),0 0 0 0 rgba(198,163,91,.4);display:flex;align-items:center;justify-content:center;cursor:pointer;transition:transform .25s,box-shadow .25s;border:2px solid rgba(198,163,91,.6);animation:hi-pulse 2.4s infinite}
  #hi-ai-fab:hover{transform:scale(1.08);box-shadow:0 8px 32px rgba(10,22,40,.55)}
  #hi-ai-fab svg{width:30px;height:30px;fill:none;stroke:#c6a35b;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;transition:transform .3s}
  #hi-ai-fab.open svg{transform:rotate(90deg) scale(.8)}
  @keyframes hi-pulse{0%,100%{box-shadow:0 6px 28px rgba(10,22,40,.45),0 0 0 0 rgba(198,163,91,.35)}50%{box-shadow:0 6px 28px rgba(10,22,40,.45),0 0 0 12px rgba(198,163,91,0)}}
  #hi-ai-badge{position:absolute;top:-2px;right:-2px;width:18px;height:18px;border-radius:50%;background:#22c55e;border:2px solid #0a1628;display:flex;align-items:center;justify-content:center}
  #hi-ai-badge span{display:block;width:6px;height:6px;border-radius:50%;background:#fff}

  #hi-ai-panel{position:fixed;bottom:104px;right:28px;z-index:99998;width:420px;max-height:calc(100vh - 140px);border-radius:20px;overflow:hidden;display:flex;flex-direction:column;background:#fff;box-shadow:0 25px 80px rgba(10,22,40,.35),0 0 0 1px rgba(0,0,0,.06);opacity:0;transform:translateY(20px) scale(.96);pointer-events:none;transition:opacity .35s cubic-bezier(.22,1,.36,1),transform .35s cubic-bezier(.22,1,.36,1)}
  #hi-ai-panel.open{opacity:1;transform:translateY(0) scale(1);pointer-events:auto}

  .hi-head{background:linear-gradient(135deg,#0a1628 0%,#162a4a 100%);padding:18px 20px;display:flex;align-items:center;gap:14px;flex-shrink:0}
  .hi-head-avatar{width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,#c6a35b,#e8c367);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:14px;color:#0a1628;flex-shrink:0;letter-spacing:.3px}
  .hi-head-info{flex:1;min-width:0}
  .hi-head-name{color:#fff;font-weight:700;font-size:15px;letter-spacing:.2px}
  .hi-head-status{color:rgba(255,255,255,.55);font-size:11.5px;display:flex;align-items:center;gap:5px;margin-top:2px}
  .hi-head-status::before{content:'';width:7px;height:7px;border-radius:50%;background:#22c55e;flex-shrink:0}
  .hi-head-close{background:none;border:none;color:rgba(255,255,255,.5);font-size:24px;cursor:pointer;padding:4px 8px;border-radius:8px;transition:color .2s,background .2s;line-height:1}
  .hi-head-close:hover{color:#fff;background:rgba(255,255,255,.1)}

  .hi-msgs{flex:1;overflow-y:auto;padding:20px 16px;display:flex;flex-direction:column;gap:12px;background:#f8f7f4;min-height:260px;max-height:calc(100vh - 340px);scroll-behavior:smooth}
  .hi-msgs::-webkit-scrollbar{width:5px}.hi-msgs::-webkit-scrollbar-track{background:transparent}.hi-msgs::-webkit-scrollbar-thumb{background:rgba(0,0,0,.12);border-radius:10px}

  .hi-msg{display:flex;gap:10px;max-width:92%;animation:hi-msgIn .35s ease}
  .hi-msg.user{margin-left:auto;flex-direction:row-reverse}
  @keyframes hi-msgIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}

  .hi-msg-ava{width:30px;height:30px;border-radius:50%;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;margin-top:2px}
  .hi-msg:not(.user) .hi-msg-ava{background:linear-gradient(135deg,#0a1628,#1e3a5f);color:#c6a35b}
  .hi-msg.user .hi-msg-ava{background:linear-gradient(135deg,#c6a35b,#e8c367);color:#0a1628}

  .hi-bubble{padding:12px 16px;border-radius:16px;font-size:13.5px;line-height:1.65;letter-spacing:.01em;word-break:break-word}
  .hi-msg:not(.user) .hi-bubble{background:#fff;color:#1a1a1a;border:1px solid rgba(0,0,0,.06);border-bottom-left-radius:4px;box-shadow:0 1px 3px rgba(0,0,0,.04)}
  .hi-msg.user .hi-bubble{background:linear-gradient(135deg,#0a1628,#162a4a);color:#fff;border-bottom-right-radius:4px}

  .hi-bubble strong{font-weight:700}.hi-bubble em{font-style:italic;color:#c6a35b}
  .hi-bubble ul,.hi-bubble ol{margin:.5em 0 .5em 1.2em;padding:0}.hi-bubble li{margin:.25em 0}
  .hi-bubble p{margin:.5em 0}.hi-bubble p:first-child{margin-top:0}.hi-bubble p:last-child{margin-bottom:0}
  .hi-bubble code{background:rgba(0,0,0,.06);padding:1px 5px;border-radius:4px;font-size:12px}
  .hi-bubble a{color:#c6a35b;text-decoration:underline}

  .hi-typing{display:flex;gap:10px;max-width:88%;animation:hi-msgIn .35s ease}
  .hi-typing .hi-bubble{display:flex;align-items:center;gap:5px;padding:14px 20px}
  .hi-dot{width:7px;height:7px;border-radius:50%;background:#aaa;animation:hi-dotBounce 1.4s infinite}
  .hi-dot:nth-child(2){animation-delay:.2s}.hi-dot:nth-child(3){animation-delay:.4s}
  @keyframes hi-dotBounce{0%,60%,100%{transform:translateY(0);opacity:.4}30%{transform:translateY(-6px);opacity:1}}

  .hi-suggestions{display:flex;flex-wrap:wrap;gap:6px;padding:0 16px 12px}
  .hi-chip{padding:7px 14px;border-radius:20px;background:#fff;border:1px solid rgba(198,163,91,.35);color:#0a1628;font-size:12px;cursor:pointer;transition:all .2s;font-weight:500;white-space:nowrap}
  .hi-chip:hover{background:linear-gradient(135deg,#c6a35b,#e8c367);color:#0a1628;border-color:transparent;transform:translateY(-1px);box-shadow:0 3px 10px rgba(198,163,91,.3)}

  .hi-plan-actions{display:flex;gap:8px;padding:0 16px 12px;flex-wrap:wrap}
  .hi-plan-btn{padding:8px 16px;border-radius:10px;border:none;font-size:12px;font-weight:600;cursor:pointer;transition:all .2s;display:flex;align-items:center;gap:6px}
  .hi-plan-btn.pdf{background:linear-gradient(135deg,#0a1628,#162a4a);color:#c6a35b}.hi-plan-btn.pdf:hover{transform:translateY(-1px);box-shadow:0 4px 12px rgba(10,22,40,.3)}
  .hi-plan-btn.book{background:linear-gradient(135deg,#c6a35b,#e8c367);color:#0a1628}.hi-plan-btn.book:hover{transform:translateY(-1px);box-shadow:0 4px 12px rgba(198,163,91,.4)}

  .hi-footer{padding:12px 16px 14px;background:#fff;border-top:1px solid rgba(0,0,0,.06);flex-shrink:0}
  .hi-input-wrap{display:flex;align-items:flex-end;gap:8px;background:#f8f7f4;border:1.5px solid rgba(0,0,0,.08);border-radius:14px;padding:6px 8px 6px 14px;transition:border-color .2s,box-shadow .2s}
  .hi-input-wrap:focus-within{border-color:rgba(198,163,91,.5);box-shadow:0 0 0 3px rgba(198,163,91,.1)}
  #hi-input{flex:1;border:none;outline:none;background:none;font-size:13.5px;color:#1a1a1a;resize:none;max-height:100px;min-height:22px;line-height:1.5;font-family:inherit;padding:4px 0}
  #hi-input::placeholder{color:#999}
  #hi-send{width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,#0a1628,#162a4a);border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:transform .15s,opacity .15s;opacity:.7}
  #hi-send:hover{transform:scale(1.06);opacity:1}
  #hi-send:disabled{opacity:.3;cursor:default;transform:none}
  #hi-send svg{width:16px;height:16px;fill:none;stroke:#c6a35b;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round}
  .hi-footer-note{text-align:center;font-size:10px;color:#bbb;margin-top:6px;letter-spacing:.2px}

  @media(max-width:480px){
    #hi-ai-panel{right:0;left:0;bottom:0;width:100%;max-height:100vh;border-radius:20px 20px 0 0}
    #hi-ai-fab{bottom:16px;right:16px;width:56px;height:56px}
    .hi-msgs{max-height:calc(100vh - 260px)}
  }
  `;

  var styleEl = document.createElement('style');
  styleEl.textContent = css;
  document.head.appendChild(styleEl);

  // ── HTML ─────────────────────────────────────────────────
  var wrapper = document.createElement('div');
  wrapper.id = 'hi-ai-root';
  wrapper.innerHTML = `
    <div id="hi-ai-fab" title="Chat with AI Agent">
      <svg viewBox="0 0 24 24"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>
      <div id="hi-ai-badge"><span></span></div>
    </div>
    <div id="hi-ai-panel">
      <div class="hi-head">
        <div class="hi-head-avatar">AI</div>
        <div class="hi-head-info">
          <div class="hi-head-name">BharatHeals AI Agent</div>
          <div class="hi-head-status">Powered by Claude AI</div>
        </div>
        <button class="hi-head-close" id="hi-close">&times;</button>
      </div>
      <div class="hi-msgs" id="hi-msgs"></div>
      <div id="hi-extras"></div>
      <div class="hi-footer">
        <div class="hi-input-wrap">
          <textarea id="hi-input" placeholder="Ask me about treatments, costs, plans..." rows="1"></textarea>
          <button id="hi-send"><svg viewBox="0 0 24 24"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg></button>
        </div>
        <div class="hi-footer-note">BharatHeals AI &middot; Responses are indicative, not medical advice</div>
      </div>
    </div>
  `;
  document.body.appendChild(wrapper);

  // ── State ────────────────────────────────────────────────
  var fab = document.getElementById('hi-ai-fab');
  var panel = document.getElementById('hi-ai-panel');
  var closeBtn = document.getElementById('hi-close');
  var msgsEl = document.getElementById('hi-msgs');
  var extrasEl = document.getElementById('hi-extras');
  var inputEl = document.getElementById('hi-input');
  var sendBtn = document.getElementById('hi-send');

  var isOpen = false;
  var isLoading = false;
  var history = [];
  var currentPlan = null;
  var greeted = false;

  // ── Toggle ───────────────────────────────────────────────
  fab.addEventListener('click', function () {
    isOpen = !isOpen;
    panel.classList.toggle('open', isOpen);
    fab.classList.toggle('open', isOpen);
    if (isOpen && !greeted) { showWelcome(); greeted = true; }
    if (isOpen) { inputEl.focus(); scrollToBottom(); }
  });
  closeBtn.addEventListener('click', function () {
    isOpen = false;
    panel.classList.remove('open');
    fab.classList.remove('open');
  });

  // ── Welcome ──────────────────────────────────────────────
  function showWelcome() {
    addBotMessage("Welcome to **BharatHeals**! I'm your AI medical tourism assistant, powered by Claude.\n\nI help patients from around the world explore treatments in India, compare costs, build personalised treatment plans, and generate downloadable PDFs.\n\n**What are you looking for today?**");
    showSuggestions([
      'Hair Transplant options',
      'Dental Implant costs',
      'Cosmetic Surgery info',
      'IVF / Fertility help',
      'Surrogacy law in India',
      'Compare all costs'
    ]);
  }

  // ── Messages ─────────────────────────────────────────────
  function addBotMessage(text) {
    var div = document.createElement('div');
    div.className = 'hi-msg';
    div.innerHTML = '<div class="hi-msg-ava">AI</div><div class="hi-bubble">' + renderMarkdown(text) + '</div>';
    msgsEl.appendChild(div);
    scrollToBottom();
  }

  function addUserMessage(text) {
    var div = document.createElement('div');
    div.className = 'hi-msg user';
    div.innerHTML = '<div class="hi-msg-ava">You</div><div class="hi-bubble">' + escapeHtml(text) + '</div>';
    msgsEl.appendChild(div);
    scrollToBottom();
  }

  function showTyping() {
    var div = document.createElement('div');
    div.className = 'hi-typing';
    div.id = 'hi-typing';
    div.innerHTML = '<div class="hi-msg-ava" style="width:30px;height:30px;border-radius:50%;background:linear-gradient(135deg,#0a1628,#1e3a5f);display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:#c6a35b;">AI</div><div class="hi-bubble"><div class="hi-dot"></div><div class="hi-dot"></div><div class="hi-dot"></div></div>';
    msgsEl.appendChild(div);
    scrollToBottom();
  }

  function hideTyping() {
    var el = document.getElementById('hi-typing');
    if (el) el.remove();
  }

  function showSuggestions(items) {
    extrasEl.innerHTML = '<div class="hi-suggestions">' + items.map(function (t) {
      return '<button class="hi-chip">' + escapeHtml(t) + '</button>';
    }).join('') + '</div>';
    extrasEl.querySelectorAll('.hi-chip').forEach(function (btn) {
      btn.addEventListener('click', function () {
        sendMessage(this.textContent);
      });
    });
  }

  function showPlanActions() {
    extrasEl.innerHTML = '<div class="hi-plan-actions">' +
      '<button class="hi-plan-btn pdf" id="hi-dl-pdf"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg> Download PDF Plan</button>' +
      '<button class="hi-plan-btn book" id="hi-book-consult"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg> Book Free Consultation</button>' +
      '</div>';
    document.getElementById('hi-dl-pdf').addEventListener('click', generatePDF);
    document.getElementById('hi-book-consult').addEventListener('click', function () {
      if (typeof window.openConsultModal === 'function') {
        window.openConsultModal(currentPlan ? currentPlan.treatment : '');
      }
    });
  }

  function clearExtras() { extrasEl.innerHTML = ''; }
  function scrollToBottom() { setTimeout(function () { msgsEl.scrollTop = msgsEl.scrollHeight; }, 60); }

  // ── Send ─────────────────────────────────────────────────
  function sendMessage(text) {
    if (!text || !text.trim() || isLoading) return;
    text = text.trim();
    clearExtras();
    addUserMessage(text);
    history.push({ role: 'user', content: text });
    inputEl.value = '';
    autoResize();
    isLoading = true;
    sendBtn.disabled = true;
    showTyping();
    streamResponse();
  }

  sendBtn.addEventListener('click', function () { sendMessage(inputEl.value); });
  inputEl.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(inputEl.value); }
  });
  inputEl.addEventListener('input', autoResize);

  function autoResize() {
    inputEl.style.height = 'auto';
    inputEl.style.height = Math.min(inputEl.scrollHeight, 100) + 'px';
  }

  // ── Streaming response ───────────────────────────────────
  function streamResponse() {
    fetch('/api/ai-agent/stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages: history }),
    }).then(function (res) {
      if (!res.ok) throw new Error('API error ' + res.status);
      return res;
    }).then(function (res) {
      hideTyping();

      var msgDiv = document.createElement('div');
      msgDiv.className = 'hi-msg';
      msgDiv.innerHTML = '<div class="hi-msg-ava">AI</div><div class="hi-bubble"></div>';
      msgsEl.appendChild(msgDiv);
      var bubbleEl = msgDiv.querySelector('.hi-bubble');

      var fullText = '';
      var reader = res.body.getReader();
      var decoder = new TextDecoder();

      function processStream() {
        reader.read().then(function (result) {
          if (result.done) { finishStream(fullText, bubbleEl); return; }
          var chunk = decoder.decode(result.value, { stream: true });
          var lines = chunk.split('\n');
          for (var i = 0; i < lines.length; i++) {
            var line = lines[i].trim();
            if (!line.startsWith('data: ')) continue;
            var payload = line.slice(6);
            if (payload === '[DONE]') { finishStream(fullText, bubbleEl); return; }
            try {
              var data = JSON.parse(payload);
              if (data.text) { fullText += data.text; bubbleEl.innerHTML = renderMarkdown(stripPlanBlock(fullText)); scrollToBottom(); }
              if (data.error) { fullText += '\n\n*Connection interrupted. Please try again.*'; }
            } catch (e) {}
          }
          processStream();
        }).catch(function (err) {
          console.error('Stream read error:', err);
          finishStream(fullText, bubbleEl);
        });
      }
      processStream();
    }).catch(function (err) {
      console.error('AI Widget fetch error:', err);
      hideTyping();
      addBotMessage("I'm sorry, I'm having trouble connecting right now. Please try again in a moment, or [book a free consultation](/plan-journey.html) with one of our human consultants.");
      isLoading = false;
      sendBtn.disabled = false;
    });
  }

  function finishStream(fullText, bubbleEl) {
    bubbleEl.innerHTML = renderMarkdown(stripPlanBlock(fullText));
    history.push({ role: 'assistant', content: fullText });

    var planMatch = fullText.match(/<<<PLAN_JSON>>>\s*([\s\S]*?)\s*<<<END_PLAN>>>/);
    if (planMatch) {
      try {
        currentPlan = JSON.parse(planMatch[1].trim());
        showPlanActions();
      } catch (e) { console.error('Plan parse error', e); }
    }

    isLoading = false;
    sendBtn.disabled = false;
    scrollToBottom();
  }

  function stripPlanBlock(text) {
    return text.replace(/<<<PLAN_JSON>>>[\s\S]*?<<<END_PLAN>>>/, '').trim();
  }

  // ── Markdown renderer ────────────────────────────────────
  function renderMarkdown(text) {
    if (!text) return '';
    return text
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>')
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.+?)\*/g, '<em>$1</em>')
      .replace(/`(.+?)`/g, '<code>$1</code>')
      .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>')
      .replace(/^### (.+)$/gm, '<strong style="font-size:14px;display:block;margin:.6em 0 .3em">$1</strong>')
      .replace(/^## (.+)$/gm, '<strong style="font-size:15px;display:block;margin:.6em 0 .3em">$1</strong>')
      .replace(/^[-•] (.+)$/gm, '<li>$1</li>')
      .replace(/^(\d+)\. (.+)$/gm, '<li>$2</li>')
      .replace(/((?:<li>.*<\/li>\n?)+)/g, '<ul>$1</ul>')
      .replace(/\n{2,}/g, '</p><p>')
      .replace(/\n/g, '<br>')
      .replace(/^/, '<p>').replace(/$/, '</p>')
      .replace(/<p><\/p>/g, '')
      .replace(/<p>(<ul>)/g, '$1')
      .replace(/(<\/ul>)<\/p>/g, '$1')
      .replace(/<p>(<strong style)/g, '$1')
      .replace(/(<\/strong>)<\/p>/g, '$1');
  }

  function escapeHtml(t) { var d = document.createElement('div'); d.textContent = t; return d.innerHTML; }

  // ── PDF generation ───────────────────────────────────────
  var JSPDF_CDNS = [
    'https://cdn.jsdelivr.net/npm/jspdf@2.5.2/dist/jspdf.umd.min.js',
    'https://unpkg.com/jspdf@2.5.2/dist/jspdf.umd.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js'
  ];

  function loadJsPDFLib() {
    if (window.jspdf) return Promise.resolve();
    var idx = 0;
    function tryNext() {
      if (idx >= JSPDF_CDNS.length) return Promise.reject(new Error('All CDN sources failed'));
      return new Promise(function (resolve, reject) {
        var s = document.createElement('script');
        s.src = JSPDF_CDNS[idx++];
        s.onload = function () { resolve(); };
        s.onerror = function () { s.remove(); tryNext().then(resolve, reject); };
        document.head.appendChild(s);
      });
    }
    return tryNext();
  }

  (function preloadJsPDF() { loadJsPDFLib().catch(function () {}); })();

  function generatePDF() {
    if (!currentPlan) return;
    var p = currentPlan;

    var authUser = null;
    try { authUser = JSON.parse(localStorage.getItem('bharatheals_user')); } catch(e) {}
    var patientName = (authUser && authUser.name) ? authUser.name : '';
    var patientEmail = (authUser && authUser.email) ? authUser.email : '';

    loadJsPDFLib().then(function () {
      var jsPDF = window.jspdf.jsPDF;
      var doc = new jsPDF({ unit: 'mm', format: 'a4' });
      var W = 210, H = 297, M = 15, cw = W - 2 * M;
      var y = 0;
      var NAVY = [10, 22, 40], GOLD = [198, 163, 91], WHITE = [255, 255, 255];
      var GRAY = [120, 120, 120], DARK = [30, 30, 30], CREAM = [248, 247, 244];
      var GREEN = [34, 139, 34], RED = [180, 50, 50], LIGHT_GOLD = [252, 248, 237];
      var BLUE_LIGHT = [235, 242, 250], GREEN_LIGHT = [235, 250, 240];
      var dateStr = new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });
      var pageNum = 0;

      function rgb(c) { doc.setTextColor(c[0], c[1], c[2]); }
      function fill(c) { doc.setFillColor(c[0], c[1], c[2]); }
      function draw(c) { doc.setDrawColor(c[0], c[1], c[2]); }

      function newPage() {
        if (pageNum > 0) { addFooter(); doc.addPage(); }
        pageNum++;
        addHeader();
        y = 22;
      }
      function checkPage(need) {
        if (y + need > H - 22) { newPage(); }
      }

      function addHeader() {
        if (pageNum <= 1) return;
        fill(NAVY); doc.rect(0, 0, W, 11, 'F');
        fill(GOLD); doc.rect(0, 11, W, 0.6, 'F');
        rgb(GOLD); doc.setFontSize(8); doc.setFont('helvetica', 'bold');
        doc.text('BharatHeals', M, 7.5);
        rgb([200,200,200]); doc.setFontSize(7); doc.setFont('helvetica', 'normal');
        var headerMid = patientName ? ('Plan for ' + patientName) : 'Your Complete Medical Tourism Guide';
        doc.text(headerMid, W / 2, 7.5, { align: 'center' });
        doc.text(dateStr, W - M, 7.5, { align: 'right' });
      }
      function addFooter() {
        fill(NAVY); doc.rect(0, H - 12, W, 12, 'F');
        fill(GOLD); doc.rect(0, H - 12, W, 0.4, 'F');
        rgb([160,160,160]); doc.setFontSize(6); doc.setFont('helvetica', 'normal');
        doc.text('This is an AI-generated indicative plan. Final costs confirmed after video consultation. BharatHeals | bharatheals.com', W / 2, H - 7, { align: 'center' });
        rgb(GOLD); doc.setFontSize(6.5); doc.setFont('helvetica', 'bold');
        doc.text('Page ' + pageNum, W - M, H - 7, { align: 'right' });
      }

      function sectionBar(title) {
        checkPage(14);
        fill(NAVY); doc.roundedRect(M, y, cw, 9, 1.5, 1.5, 'F');
        rgb(GOLD); doc.setFontSize(9.5); doc.setFont('helvetica', 'bold');
        doc.text(title.toUpperCase(), M + 5, y + 6.2);
        y += 13;
      }

      function subHeading(title) {
        checkPage(10);
        fill(LIGHT_GOLD); doc.roundedRect(M, y, cw, 7.5, 1, 1, 'F');
        draw(GOLD); doc.setLineWidth(0.3); doc.roundedRect(M, y, cw, 7.5, 1, 1, 'S');
        rgb(NAVY); doc.setFontSize(8.5); doc.setFont('helvetica', 'bold');
        doc.text(title, M + 4, y + 5.3);
        y += 11;
      }

      function kvRow(label, value, opts) {
        if (!value && value !== 0) return;
        opts = opts || {};
        checkPage(8);
        var labelW = opts.labelW || 44;
        var x = M + (opts.indent || 2);
        doc.setFontSize(opts.size || 8.5); doc.setFont('helvetica', 'bold'); rgb(GRAY);
        doc.text(label, x, y);
        doc.setFont('helvetica', 'normal'); rgb(opts.valueColor || DARK);
        var lines = doc.splitTextToSize(String(value), cw - labelW - (opts.indent || 2) - 4);
        doc.text(lines, x + labelW, y);
        y += Math.max(lines.length * 4, 5.5);
      }

      function bulletItem(text, icon, color) {
        if (!text) return;
        checkPage(7);
        rgb(color || GREEN); doc.setFontSize(8.5); doc.setFont('helvetica', 'bold');
        doc.text(icon || '\u2713', M + 3, y);
        doc.setFont('helvetica', 'normal'); rgb(DARK);
        var lines = doc.splitTextToSize(String(text), cw - 12);
        doc.text(lines, M + 10, y);
        y += lines.length * 4 + 1.5;
      }

      function infoBox(bgColor, borderColor, lines) {
        var boxH = lines.length * 5 + 8;
        checkPage(boxH + 4);
        fill(bgColor); doc.roundedRect(M, y, cw, boxH, 2, 2, 'F');
        if (borderColor) { draw(borderColor); doc.setLineWidth(0.4); doc.roundedRect(M, y, cw, boxH, 2, 2, 'S'); }
        var ty = y + 5;
        lines.forEach(function(l) {
          if (l.bold) { doc.setFont('helvetica', 'bold'); doc.setFontSize(l.size || 8.5); rgb(l.color || DARK); }
          else { doc.setFont('helvetica', 'normal'); doc.setFontSize(l.size || 8); rgb(l.color || GRAY); }
          doc.text(l.text, l.align === 'center' ? W / 2 : M + 5, ty, l.align === 'center' ? { align: 'center' } : undefined);
          ty += (l.gap || 5);
        });
        y += boxH + 4;
      }

      // ═══════════════════════════════════════════════════════
      // PAGE 1 — COVER PAGE
      // ═══════════════════════════════════════════════════════
      pageNum = 1;
      fill(NAVY); doc.rect(0, 0, W, H, 'F');
      fill(GOLD); doc.rect(0, 0, 5, H, 'F');
      doc.setGState(new doc.GState({ opacity: 0.04 }));
      fill(GOLD); doc.circle(W + 20, -20, 120, 'F'); doc.circle(-40, H + 20, 100, 'F');
      doc.setGState(new doc.GState({ opacity: 1 }));

      rgb(GOLD); doc.setFontSize(40); doc.setFont('helvetica', 'bold');
      doc.text('BharatHeals', 24, 45);
      rgb([170, 170, 170]); doc.setFontSize(11); doc.setFont('helvetica', 'normal');
      doc.text('Your Complete Medical Tourism Guide', 24, 55);
      fill(GOLD); doc.rect(24, 61, 55, 1, 'F');

      // "Prepared for" personalization
      if (patientName) {
        rgb([130,130,130]); doc.setFontSize(9); doc.setFont('helvetica', 'normal');
        doc.text('Prepared exclusively for', 24, 72);
        rgb(WHITE); doc.setFontSize(20); doc.setFont('helvetica', 'bold');
        doc.text(patientName, 24, 81);
        if (patientEmail) {
          rgb([150,150,150]); doc.setFontSize(8.5); doc.setFont('helvetica', 'normal');
          doc.text(patientEmail, 24, 87);
        }
        fill(GOLD); doc.rect(24, 91, 40, 0.6, 'F');
      }

      var coverY = patientName ? 100 : 72;

      rgb(WHITE); doc.setFontSize(24); doc.setFont('helvetica', 'bold');
      var titleLines = doc.splitTextToSize(p.treatment || 'Treatment Plan', cw - 20);
      doc.text(titleLines, 24, coverY);
      var ty = coverY + titleLines.length * 10;

      if (p.procedure) {
        rgb(GOLD); doc.setFontSize(10.5); doc.setFont('helvetica', 'normal');
        var procLines = doc.splitTextToSize(p.procedure, cw - 20);
        doc.text(procLines, 24, ty + 2);
        ty += procLines.length * 5 + 6;
      }
      ty += 6;

      var coverStats = [
        { label: 'TREATMENT COST (INDIA)', val: p.estimatedCost || '$—' },
        { label: 'HOME COUNTRY COST', val: p.homeCost || '$—' },
        { label: 'YOUR SAVINGS', val: (p.savings || '') + (p.savingsAmount ? ' (' + p.savingsAmount + ')' : '') || '—' },
        { label: 'HOSPITAL', val: (p.hospital || '') + (p.hospitalCity ? ', ' + p.hospitalCity : '') },
        { label: 'LEAD SURGEON', val: p.doctor || 'To be assigned' },
        { label: 'STAY IN INDIA', val: p.stay || '—' },
        { label: 'YOUR CONSULTANT', val: p.consultant || 'Sarah Mitchell' },
      ];
      coverStats.forEach(function(s) {
        rgb([130, 130, 130]); doc.setFontSize(7); doc.setFont('helvetica', 'normal');
        doc.text(s.label, 24, ty);
        rgb(WHITE); doc.setFontSize(11); doc.setFont('helvetica', 'bold');
        doc.text(String(s.val), 24, ty + 5);
        ty += 12;
      });

      fill(GOLD); doc.setGState(new doc.GState({ opacity: 0.15 }));
      doc.roundedRect(18, H - 45, cw + 4, 30, 2, 2, 'F');
      doc.setGState(new doc.GState({ opacity: 1 }));
      rgb([160,160,160]); doc.setFontSize(7.5); doc.setFont('helvetica', 'normal');
      var coverFooter1 = 'Generated: ' + dateStr;
      if (patientName) coverFooter1 += '  |  Exclusively for ' + patientName;
      coverFooter1 += '  |  Prices in USD';
      doc.text(coverFooter1, 24, H - 32);
      rgb(GOLD); doc.setFontSize(8); doc.setFont('helvetica', 'bold');
      doc.text('bharatheals.com  |  WhatsApp: +91 99999 99999  |  info@bharatheals.com', 24, H - 26);
      rgb([130,130,130]); doc.setFontSize(7); doc.setFont('helvetica', 'normal');
      doc.text('Book a free video consultation for a personalised, binding quote', 24, H - 21);

      // ═══════════════════════════════════════════════════════
      // PAGE 2 — TREATMENT DETAILS & COST BREAKDOWN
      // ═══════════════════════════════════════════════════════
      newPage();

      if (patientName) {
        fill(LIGHT_GOLD); doc.roundedRect(M, y, cw, 12, 2, 2, 'F');
        draw(GOLD); doc.setLineWidth(0.3); doc.roundedRect(M, y, cw, 12, 2, 2, 'S');
        rgb(GRAY); doc.setFontSize(7.5); doc.setFont('helvetica', 'normal');
        doc.text('PATIENT', M + 5, y + 5);
        rgb(NAVY); doc.setFontSize(10); doc.setFont('helvetica', 'bold');
        doc.text(patientName, M + 5, y + 10);
        if (patientEmail) {
          rgb(GRAY); doc.setFontSize(7.5); doc.setFont('helvetica', 'normal');
          doc.text(patientEmail, W - M - 5, y + 7.5, { align: 'right' });
        }
        rgb(GRAY); doc.setFontSize(7); doc.setFont('helvetica', 'normal');
        doc.text('Plan generated: ' + dateStr, W - M - 5, y + 3.5, { align: 'right' });
        y += 16;
      }

      sectionBar('Treatment & Hospital Details');
      kvRow('Treatment', p.treatment);
      if (p.procedure) kvRow('Procedure', p.procedure);
      kvRow('Hospital', (p.hospital || '') + (p.hospitalCity ? ', ' + p.hospitalCity : ''));
      if (p.hospitalAddress) kvRow('Address', p.hospitalAddress);
      if (p.hospitalAccreditation) kvRow('Accreditation', p.hospitalAccreditation);
      kvRow('Lead Surgeon', p.doctor);
      if (p.doctorCredentials) kvRow('Credentials', p.doctorCredentials);
      if (p.doctorExperience) kvRow('Experience', p.doctorExperience);
      kvRow('Duration in India', p.stay);
      kvRow('Recovery Period', p.recovery);
      kvRow('Your Consultant', p.consultant);
      if (p.consultantPhone) kvRow('Consultant Phone', p.consultantPhone);
      if (p.consultantEmail) kvRow('Consultant Email', p.consultantEmail);
      y += 3;

      sectionBar('Cost Comparison — India vs. Home Country');
      checkPage(38);
      fill(CREAM); doc.roundedRect(M, y, cw, 34, 2.5, 2.5, 'F');
      draw(GOLD); doc.setLineWidth(0.5); doc.roundedRect(M, y, cw, 34, 2.5, 2.5, 'S');
      var colW = cw / 3;
      var costLabels = ['India Cost', 'Home Country Cost', 'You Save'];
      var costVals = [p.estimatedCost || '$—', p.homeCost || '$—', (p.savingsAmount || p.savings || '—')];
      var costColors = [GREEN, RED, NAVY];
      for (var ci = 0; ci < 3; ci++) {
        var cx = M + colW * ci + colW / 2;
        doc.setFontSize(7.5); doc.setFont('helvetica', 'normal'); rgb(GRAY);
        doc.text(costLabels[ci], cx, y + 10, { align: 'center' });
        doc.setFontSize(17); doc.setFont('helvetica', 'bold'); rgb(costColors[ci]);
        doc.text(costVals[ci], cx, y + 21, { align: 'center' });
        if (ci === 2 && p.savings) {
          doc.setFontSize(9); rgb(GREEN);
          doc.text(p.savings + ' savings', cx, y + 28, { align: 'center' });
        }
      }
      y += 40;

      if (p.inclusions && p.inclusions.length) {
        sectionBar("What's Included in Your Package");
        var cols = 2;
        var items = p.inclusions;
        for (var ii = 0; ii < items.length; ii += cols) {
          checkPage(7);
          for (var cc = 0; cc < cols && ii + cc < items.length; cc++) {
            var xx = M + cc * (cw / cols) + 3;
            rgb(GREEN); doc.setFontSize(8); doc.setFont('helvetica', 'bold');
            doc.text('\u2713', xx, y);
            doc.setFont('helvetica', 'normal'); rgb(DARK);
            var itLines = doc.splitTextToSize(items[ii + cc], cw / cols - 12);
            doc.text(itLines, xx + 6, y);
          }
          y += 5.5;
        }
        y += 3;
      }

      // ═══════════════════════════════════════════════════════
      // PAGE 3 — TRAVEL & VISA GUIDE
      // ═══════════════════════════════════════════════════════
      newPage();

      sectionBar('Travel & Flight Information');
      if (p.travel) {
        var t = p.travel;
        kvRow('Flight Cost', t.flightEstimate);
        kvRow('Flight Duration', t.flightDuration);
        if (t.bestAirlines) kvRow('Recommended Airlines', t.bestAirlines);
        if (t.nearestAirport) kvRow('Nearest Airport', t.nearestAirport);
        if (t.airportDistance) kvRow('Hospital Distance', t.airportDistance);
        y += 3;

        subHeading('Visa Information — e-Medical Visa');
        kvRow('Visa Type', t.visa || 'e-Medical Visa');
        if (t.visaCost) kvRow('Cost', t.visaCost);
        if (t.visaProcessing) kvRow('Processing', t.visaProcessing);
        if (t.visaDocuments) kvRow('Documents Needed', t.visaDocuments);
        y += 3;

        subHeading('Travel Insurance');
        kvRow('Recommended', t.insurance || '$50-150 comprehensive policy');
        if (t.insuranceTip) kvRow('Tip', t.insuranceTip);
        y += 3;
      }

      // ═══════════════════════════════════════════════════════
      // ACCOMMODATION OPTIONS
      // ═══════════════════════════════════════════════════════
      sectionBar('Accommodation Options');
      if (p.accommodation && p.accommodation.length) {
        p.accommodation.forEach(function(acc) {
          checkPage(28);
          var badge = acc.type || 'Standard';
          var bColor = badge === 'Premium' ? GOLD : badge === 'Mid-Range' ? [92,122,106] : [100,140,200];
          var bgColor = badge === 'Premium' ? [255,252,243] : badge === 'Mid-Range' ? [243,250,246] : BLUE_LIGHT;

          fill(bgColor); doc.roundedRect(M, y, cw, 22, 2, 2, 'F');
          draw(bColor); doc.setLineWidth(0.5); doc.roundedRect(M, y, cw, 22, 2, 2, 'S');

          fill(bColor); doc.roundedRect(M + 3, y + 3, 26, 6, 1, 1, 'F');
          rgb(WHITE); doc.setFontSize(6.5); doc.setFont('helvetica', 'bold');
          doc.text(badge.toUpperCase(), M + 16, y + 7, { align: 'center' });

          rgb(DARK); doc.setFontSize(9); doc.setFont('helvetica', 'bold');
          doc.text(acc.name || '', M + 33, y + 7.5);

          rgb(NAVY); doc.setFontSize(10); doc.setFont('helvetica', 'bold');
          doc.text(acc.cost || '', W - M - 4, y + 7.5, { align: 'right' });

          rgb(GRAY); doc.setFontSize(7.5); doc.setFont('helvetica', 'normal');
          if (acc.totalStay) doc.text('Total stay: ' + acc.totalStay, M + 5, y + 13.5);
          if (acc.notes) { var nL = doc.splitTextToSize(acc.notes, cw - 12); doc.text(nL, M + 5, y + (acc.totalStay ? 17.5 : 13.5)); }
          if (acc.examples) { rgb(GOLD); doc.setFont('helvetica', 'bold'); doc.text('e.g. ' + acc.examples, W - M - 4, y + 18, { align: 'right' }); }

          y += 26;
        });
      }
      y += 2;

      // ═══════════════════════════════════════════════════════
      // PAGE 4 — FOOD, DAILY COSTS, TOTAL ESTIMATE
      // ═══════════════════════════════════════════════════════
      newPage();

      if (p.foodGuide) {
        sectionBar('Food & Dining Guide');
        var fg = p.foodGuide;
        kvRow('Hospital Food', fg.hospitalFood);
        kvRow('Street Food', fg.streetFood);
        kvRow('Mid-Range Dining', fg.midRange);
        kvRow('Fine Dining', fg.fineDining);
        if (fg.dietaryNote) {
          y += 1;
          infoBox(GREEN_LIGHT, [180, 220, 190], [
            { text: 'Dietary Note', bold: true, color: GREEN, size: 8 },
            { text: fg.dietaryNote, bold: false, color: DARK, size: 7.5 }
          ]);
        }
        if (fg.waterTip) kvRow('Water Tip', fg.waterTip);
        y += 3;
      }

      if (p.dailyCosts) {
        sectionBar('Daily Living Costs');
        var dc = p.dailyCosts;
        checkPage(40);
        fill(CREAM); doc.roundedRect(M, y, cw, 4, 0, 0, 'F');

        var dcItems = [
          { label: 'Food & Meals', val: dc.food },
          { label: 'Local Transport (Uber/Ola)', val: dc.localTransport },
          { label: 'SIM Card & Internet', val: dc.sim },
          { label: 'Laundry', val: dc.laundry },
          { label: 'Miscellaneous', val: dc.misc },
        ];
        dcItems.forEach(function(item, di) {
          if (!item.val) return;
          checkPage(8);
          if (di % 2 === 0) { fill([248, 248, 248]); doc.rect(M, y - 1.5, cw, 6.5, 'F'); }
          rgb(DARK); doc.setFontSize(8.5); doc.setFont('helvetica', 'normal');
          doc.text(item.label, M + 4, y + 1.5);
          rgb(NAVY); doc.setFont('helvetica', 'bold');
          doc.text(item.val, W - M - 4, y + 1.5, { align: 'right' });
          y += 6.5;
        });
        if (dc.totalDaily) {
          checkPage(10);
          fill(NAVY); doc.roundedRect(M, y, cw, 8, 1, 1, 'F');
          rgb(GOLD); doc.setFontSize(9); doc.setFont('helvetica', 'bold');
          doc.text('ESTIMATED DAILY TOTAL', M + 5, y + 5.5);
          rgb(WHITE); doc.setFontSize(10); doc.setFont('helvetica', 'bold');
          doc.text(dc.totalDaily, W - M - 5, y + 5.5, { align: 'right' });
          y += 12;
        }
        y += 4;
      }

      if (p.totalEstimate) {
        sectionBar('Total Trip Cost Estimate (All-Inclusive)');
        checkPage(70);
        var te = p.totalEstimate;
        var tiers = [
          { label: 'BUDGET', desc: 'Economy flights, 3-star stay, local food', val: te.budget, breakdown: te.budgetBreakdown, color: [100,140,200], bg: BLUE_LIGHT },
          { label: 'COMFORTABLE', desc: '4-star hotel, restaurants, Uber rides', val: te.midRange, breakdown: te.midRangeBreakdown, color: [92,122,106], bg: GREEN_LIGHT },
          { label: 'PREMIUM', desc: '5-star luxury, fine dining, private transfers', val: te.premium, breakdown: te.premiumBreakdown, color: GOLD, bg: [255,252,243] },
        ];
        tiers.forEach(function(tier) {
          if (!tier.val) return;
          var boxH = tier.breakdown ? 22 : 16;
          checkPage(boxH + 4);
          fill(tier.bg); doc.roundedRect(M, y, cw, boxH, 2, 2, 'F');
          draw(tier.color); doc.setLineWidth(0.6); doc.roundedRect(M, y, cw, boxH, 2, 2, 'S');

          fill(tier.color); doc.roundedRect(M + 4, y + 3.5, 30, 7, 1, 1, 'F');
          rgb(WHITE); doc.setFontSize(7); doc.setFont('helvetica', 'bold');
          doc.text(tier.label, M + 19, y + 8, { align: 'center' });

          rgb(DARK); doc.setFontSize(8.5); doc.setFont('helvetica', 'normal');
          doc.text(tier.desc, M + 38, y + 8);

          rgb(NAVY); doc.setFontSize(13); doc.setFont('helvetica', 'bold');
          doc.text(tier.val, W - M - 5, y + 9, { align: 'right' });

          if (tier.breakdown) {
            rgb(GRAY); doc.setFontSize(6.5); doc.setFont('helvetica', 'normal');
            var bLines = doc.splitTextToSize(tier.breakdown, cw - 12);
            doc.text(bLines, M + 5, y + 15);
          }
          y += boxH + 4;
        });
        y += 2;
      }

      // ═══════════════════════════════════════════════════════
      // PAGE 5 — CITY GUIDE & PRACTICAL INFO
      // ═══════════════════════════════════════════════════════
      if (p.cityGuide) {
        newPage();
        sectionBar('City & Practical Guide — ' + (p.cityGuide.city || p.hospitalCity || 'India'));
        var cg = p.cityGuide;
        kvRow('Weather', cg.weather);
        kvRow('Best Time to Visit', cg.bestTime);
        kvRow('Language', cg.language);
        kvRow('Currency', cg.currency);
        kvRow('Time Zone', cg.timezone);
        kvRow('Electricity', cg.electricity);
        kvRow('Safety', cg.safety);
        if (cg.emergencyNumbers) kvRow('Emergency Numbers', cg.emergencyNumbers);
        y += 4;
      }

      if (p.packingChecklist && p.packingChecklist.length) {
        sectionBar('Pre-Travel Packing Checklist');
        var cols2 = 2;
        for (var pi = 0; pi < p.packingChecklist.length; pi += cols2) {
          checkPage(7);
          for (var pc = 0; pc < cols2 && pi + pc < p.packingChecklist.length; pc++) {
            var px = M + pc * (cw / cols2) + 3;
            rgb(NAVY); doc.setFontSize(8); doc.setFont('helvetica', 'bold');
            doc.text('\u2610', px, y);
            doc.setFont('helvetica', 'normal'); rgb(DARK);
            var pkLines = doc.splitTextToSize(p.packingChecklist[pi + pc], cw / cols2 - 12);
            doc.text(pkLines, px + 6, y);
          }
          y += 5.5;
        }
        y += 4;
      }

      // ═══════════════════════════════════════════════════════
      // PAGE 6 — STEP-BY-STEP JOURNEY TIMELINE
      // ═══════════════════════════════════════════════════════
      if (p.steps && p.steps.length) {
        newPage();
        sectionBar('Your Journey — Step by Step Timeline');

        p.steps.forEach(function(step, idx) {
          checkPage(24);
          var isLast = idx === p.steps.length - 1;

          fill(NAVY); doc.circle(M + 5, y + 3, 4, 'F');
          rgb(WHITE); doc.setFontSize(8); doc.setFont('helvetica', 'bold');
          doc.text(String(idx + 1), M + 5, y + 4.2, { align: 'center' });

          if (!isLast) {
            draw([200, 200, 200]); doc.setLineWidth(0.5);
            doc.setLineDashPattern([1, 1], 0);
            doc.line(M + 5, y + 7.5, M + 5, y + 22);
            doc.setLineDashPattern([], 0);
          }

          fill(LIGHT_GOLD); doc.roundedRect(M + 14, y - 2.5, cw - 16, 6.5, 1, 1, 'F');
          rgb(GOLD); doc.setFontSize(7.5); doc.setFont('helvetica', 'bold');
          doc.text(step.phase || ('Step ' + (idx + 1)), M + 17, y + 2);

          rgb(DARK); doc.setFontSize(9.5); doc.setFont('helvetica', 'bold');
          doc.text(step.task || '', M + 14, y + 9);

          if (step.detail) {
            doc.setFont('helvetica', 'normal'); rgb(GRAY); doc.setFontSize(8);
            var dLines = doc.splitTextToSize(step.detail, cw - 18);
            doc.text(dLines, M + 14, y + 14);
            y += 14 + dLines.length * 3.8 + 4;
          } else {
            y += 16;
          }
        });
        y += 4;
      }

      // ═══════════════════════════════════════════════════════
      // OPTIONAL EXTRAS
      // ═══════════════════════════════════════════════════════
      if (p.optionalExtras && p.optionalExtras.length) {
        checkPage(20);
        sectionBar('Optional Add-Ons & Experiences');
        p.optionalExtras.forEach(function(extra) {
          checkPage(14);
          var isObj = typeof extra === 'object';
          var item = isObj ? extra.item : extra;
          var cost = isObj ? extra.cost : '';
          var desc = isObj ? extra.desc : '';

          fill(LIGHT_GOLD); doc.roundedRect(M, y, cw, desc ? 12 : 7, 1.5, 1.5, 'F');
          rgb(GOLD); doc.setFontSize(8.5); doc.setFont('helvetica', 'bold');
          doc.text('\u2605  ' + item, M + 4, y + 5);
          if (cost) { rgb(NAVY); doc.text(cost, W - M - 4, y + 5, { align: 'right' }); }
          if (desc) {
            rgb(GRAY); doc.setFontSize(7.5); doc.setFont('helvetica', 'normal');
            doc.text(desc, M + 10, y + 10);
          }
          y += (desc ? 15 : 10);
        });
        y += 3;
      }

      // ═══════════════════════════════════════════════════════
      // IMPORTANT NOTES
      // ═══════════════════════════════════════════════════════
      checkPage(50);
      sectionBar('Important Notes & Disclaimers');
      var notes = p.importantNotes || [
        'All prices are estimates in USD — final quote after video consultation with surgeon.',
        'Hospital and doctor assignment confirmed after reviewing your medical reports.',
        'e-Medical Visa: 60-day validity, triple entry — we assist with the full application.',
        'Comprehensive medical travel insurance is strongly recommended ($50-150).',
        'Companion visa available for one family member at no additional cost.',
        'Post-treatment: 12 months of free telemedicine follow-up included.',
        'If complications arise during your stay, corrective treatment is covered.',
        'We provide 24/7 emergency support throughout your stay in India.',
      ];
      notes.forEach(function(n) {
        checkPage(8);
        rgb(GRAY); doc.setFontSize(7.5); doc.setFont('helvetica', 'normal');
        var nLines = doc.splitTextToSize('\u2022  ' + n, cw - 6);
        doc.text(nLines, M + 3, y);
        y += nLines.length * 3.6 + 2;
      });
      y += 6;

      // ═══════════════════════════════════════════════════════
      // FINAL CTA
      // ═══════════════════════════════════════════════════════
      checkPage(48);
      fill(NAVY); doc.roundedRect(M, y, cw, patientName ? 42 : 36, 3, 3, 'F');
      fill(GOLD); doc.roundedRect(M + 3, y + 3, cw - 6, 0.6, 0, 0, 'F');
      var ctaTitle = patientName ? (patientName.split(' ')[0] + ', Ready to Start Your Journey?') : 'Ready to Start Your Journey?';
      rgb(GOLD); doc.setFontSize(14); doc.setFont('helvetica', 'bold');
      doc.text(ctaTitle, W / 2, y + 12, { align: 'center' });
      rgb(WHITE); doc.setFontSize(9); doc.setFont('helvetica', 'normal');
      var ctaLine1 = 'Book a free video consultation with ' + (p.consultant || 'our medical team') + '.';
      doc.text(ctaLine1, W / 2, y + 19, { align: 'center' });
      doc.text('Get a personalised, binding quote within 24 hours.', W / 2, y + 24, { align: 'center' });
      if (patientName) {
        rgb([180,180,180]); doc.setFontSize(7.5); doc.setFont('helvetica', 'normal');
        doc.text('This plan was prepared exclusively for ' + patientName + ' on ' + dateStr, W / 2, y + 30, { align: 'center' });
      }
      rgb(GOLD); doc.setFontSize(8.5); doc.setFont('helvetica', 'bold');
      var contactLine = 'bharatheals.com';
      if (p.consultantPhone) contactLine += '  |  ' + p.consultantPhone;
      contactLine += '  |  WhatsApp: +91 99999 99999';
      if (p.consultantEmail) contactLine += '  |  ' + p.consultantEmail;
      doc.text(contactLine, W / 2, y + 31, { align: 'center' });

      addFooter();

      var fileName = 'BharatHeals-' + (p.treatment || 'Plan').replace(/[^a-zA-Z0-9]/g, '-');
      if (patientName) fileName += '-' + patientName.replace(/[^a-zA-Z0-9]/g, '-');
      doc.save(fileName + '.pdf');
      if (typeof window.showToast === 'function') window.showToast('Your comprehensive treatment & travel guide has been downloaded!', 'success');
    }).catch(function (err) {
      console.error('PDF generation error:', err);
      addBotMessage("Sorry, I couldn't load the PDF library. Please check your internet connection and try again.");
    });
  }

})();
