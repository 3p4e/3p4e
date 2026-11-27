// BIG DOGMA chat avatar (owner, 2026-11-27): a chat on bigdogma.tech and the company pages. The avatar is the animated BD logo; on
// request it switches to a human digital host. "BD" (AI, DeepSeek) answers and collects leads; every chat is mirrored to the owner's
// Telegram, and a team member can answer from there (their replies appear here). Talks to /api/chat on the page's own host.
// Self-contained: its CSS is injected here; the logo shape comes from window.DOGMA_FXMARK (logo_fx/mark_data.js, on every page).
(function () {
  if (window.BDChat) return;
  const API = '/api/chat', ME = (document.currentScript && document.currentScript.src) || 'https://bigdogma.tech/chat.js';
  const BASE = new URL('.', ME).href, HUMAN = { poster: BASE + 'media/avatar/host.jpg', idle: BASE + 'media/avatar/host_idle.mp4', talk: BASE + 'media/avatar/host_talk.mp4' };
  const CO = (window.BD_CHAT && window.BD_CHAT.company) || '';
  const T = {
    mk: ['Како можам да помогнам?', 'Здраво! Јас сум BD, AI асистентот на BIG DOGMA. Како можам да ви помогнам?', 'Повеќе сакате човечко лице? Можам да се префрлам на дигитален аватар.', 'Дигитален аватар', 'Назад на логото', 'Колку чини?', 'Колку чини еден AI филм?', 'Пилот-филм', 'Како функционира пилот-филмот?', 'Разговор со човек', 'Сакам да разговарам со човек од тимот.', 'Напишете порака…', 'Испрати', 'AI асистент · тимот се вклучува преку Telegram', 'AI асистент (DeepSeek). Разговорите ги чита и тимот на BIG DOGMA. Не споделувајте чувствителни податоци.', 'BD пишува…', 'Член на тимот се приклучи во разговорот.', 'Пораката не помина. Обидете се повторно или пишете ни на inf.unit@bigdogma.tech.', 'Разговор со BIG DOGMA', 'Затвори', 'Дигитален домаќин'],
    en: ['How can I help you?', "Hi! I'm BD, the AI assistant of BIG DOGMA. How can I be of service?", 'Would you prefer a human face? I can switch to a digital avatar.', 'Digital avatar', 'Back to the logo', 'Prices', 'How much does an AI film cost?', 'Pilot film', 'How does the pilot film work?', 'Talk to a person', "I'd like to talk to a person from the team.", 'Type a message…', 'Send', 'AI assistant · the team joins via Telegram', "AI assistant (DeepSeek). The BIG DOGMA team also reads these chats. Please don't share sensitive data.", 'BD is typing…', 'A team member joined the chat.', 'Message not sent. Please try again or write to inf.unit@bigdogma.tech.', 'Chat with BIG DOGMA', 'Close', 'Digital host'],
    sq: ["Si mund t'ju ndihmoj?", "Përshëndetje! Unë jam BD, asistenti AI i BIG DOGMA. Si mund t'ju ndihmoj?", 'Preferoni një fytyrë njerëzore? Mund të kaloj te një avatar dixhital.', 'Avatar dixhital', 'Kthehu te logoja', 'Çmimet', 'Sa kushton një film AI?', 'Film pilot', 'Si funksionon filmi pilot?', 'Fol me një person', 'Dua të flas me një person nga ekipi.', 'Shkruani një mesazh…', 'Dërgo', 'Asistent AI · ekipi bashkohet përmes Telegram', 'Asistent AI (DeepSeek). Bisedat i lexon edhe ekipi i BIG DOGMA. Mos ndani të dhëna të ndjeshme.', 'BD po shkruan…', 'Një anëtar i ekipit iu bashkua bisedës.', 'Mesazhi nuk u dërgua. Provoni përsëri ose na shkruani në inf.unit@bigdogma.tech.', 'Bisedë me BIG DOGMA', 'Mbyll', 'Pritës dixhital'],
    sr: ['Kako mogu da pomognem?', 'Zdravo! Ja sam BD, AI asistent studija BIG DOGMA. Kako mogu da vam pomognem?', 'Više volite ljudsko lice? Mogu da se prebacim na digitalni avatar.', 'Digitalni avatar', 'Nazad na logo', 'Cene', 'Koliko košta jedan AI film?', 'Pilot film', 'Kako funkcioniše pilot film?', 'Razgovor sa čovekom', 'Želim da razgovaram sa nekim iz tima.', 'Napišite poruku…', 'Pošalji', 'AI asistent · tim se uključuje preko Telegrama', 'AI asistent (DeepSeek). Razgovore čita i tim BIG DOGMA. Ne delite osetljive podatke.', 'BD piše…', 'Član tima se uključio u razgovor.', 'Poruka nije poslata. Pokušajte ponovo ili pišite na inf.unit@bigdogma.tech.', 'Razgovor sa BIG DOGMA', 'Zatvori', 'Digitalni domaćin'],
    hr: ['Kako mogu pomoći?', 'Bok! Ja sam BD, AI asistent studija BIG DOGMA. Kako vam mogu pomoći?', 'Više volite ljudsko lice? Mogu se prebaciti na digitalni avatar.', 'Digitalni avatar', 'Natrag na logo', 'Cijene', 'Koliko košta jedan AI film?', 'Pilot film', 'Kako funkcionira pilot film?', 'Razgovor s osobom', 'Želim razgovarati s nekim iz tima.', 'Napišite poruku…', 'Pošalji', 'AI asistent · tim se uključuje putem Telegrama', 'AI asistent (DeepSeek). Razgovore čita i tim BIG DOGMA. Ne dijelite osjetljive podatke.', 'BD piše…', 'Član tima pridružio se razgovoru.', 'Poruka nije poslana. Pokušajte ponovno ili pišite na inf.unit@bigdogma.tech.', 'Razgovor s BIG DOGMA', 'Zatvori', 'Digitalni domaćin'],
    sl: ['Kako vam lahko pomagam?', 'Pozdravljeni! Sem BD, AI asistent studia BIG DOGMA. Kako vam lahko pomagam?', 'Vam je ljubši človeški obraz? Lahko preklopim na digitalni avatar.', 'Digitalni avatar', 'Nazaj na logotip', 'Cene', 'Koliko stane en AI film?', 'Pilotni film', 'Kako poteka pilotni film?', 'Pogovor z osebo', 'Rad bi govoril z nekom iz ekipe.', 'Napišite sporočilo…', 'Pošlji', 'AI asistent · ekipa se pridruži prek Telegrama', 'AI asistent (DeepSeek). Pogovore bere tudi ekipa BIG DOGMA. Ne delite občutljivih podatkov.', 'BD piše…', 'Član ekipe se je pridružil pogovoru.', 'Sporočilo ni bilo poslano. Poskusite znova ali pišite na inf.unit@bigdogma.tech.', 'Pogovor z BIG DOGMA', 'Zapri', 'Digitalni gostitelj'],
    bg: ['С какво мога да помогна?', 'Здравейте! Аз съм BD, AI асистентът на BIG DOGMA. С какво мога да ви помогна?', 'Предпочитате човешко лице? Мога да превключа на дигитален аватар.', 'Дигитален аватар', 'Обратно към логото', 'Цени', 'Колко струва един AI филм?', 'Пилотен филм', 'Как работи пилотният филм?', 'Разговор с човек', 'Искам да говоря с човек от екипа.', 'Напишете съобщение…', 'Изпрати', 'AI асистент · екипът се включва през Telegram', 'AI асистент (DeepSeek). Разговорите се четат и от екипа на BIG DOGMA. Не споделяйте чувствителни данни.', 'BD пише…', 'Член на екипа се включи в разговора.', 'Съобщението не беше изпратено. Опитайте отново или ни пишете на inf.unit@bigdogma.tech.', 'Разговор с BIG DOGMA', 'Затвори', 'Дигитален домакин'],
    zh: ['有什么可以帮您？', '您好！我是 BD，BIG DOGMA 的 AI 助手。有什么可以为您效劳？', '更喜欢真人形象吗？我可以切换到数字人形象。', '数字人形象', '返回标志', '价格', '一部 AI 影片多少钱？', '试点影片', '试点影片是怎么做的？', '联系真人', '我想和团队成员交谈。', '输入消息…', '发送', 'AI 助手 · 团队可通过 Telegram 加入', 'AI 助手（DeepSeek）。BIG DOGMA 团队也会阅读这些对话。请勿分享敏感信息。', 'BD 正在输入…', '团队成员已加入对话。', '消息未发送。请重试或发邮件至 inf.unit@bigdogma.tech。', '与 BIG DOGMA 对话', '关闭', '数字主持人']
  };
  const K = ['teaser', 'g1', 'g2', 'toHuman', 'toLogo', 'cPrice', 'qPrice', 'cPilot', 'qPilot', 'cHuman', 'qHuman', 'ph', 'send', 'status', 'privacy', 'typing', 'joined', 'err', 'open', 'close', 'hostName'];
  const lang = () => { const l = (document.documentElement.lang || 'en').slice(0, 2); return T[l] ? l : 'en'; };
  const t = k => T[lang()][K.indexOf(k)];
  const store = { get(k) { try { return JSON.parse(localStorage.getItem('bdchat.' + k)); } catch (e) { return null; } },
                  set(k, v) { try { localStorage.setItem('bdchat.' + k, JSON.stringify(v)); } catch (e) {} } };
  const css = `
#bdc-l{position:fixed;right:18px;bottom:18px;z-index:2147483000;width:64px;height:64px;border-radius:50%;border:1px solid rgba(242,193,78,.55);background:radial-gradient(circle at 50% 40%,#1b1810,#07070a 70%);box-shadow:0 8px 28px rgba(0,0,0,.55),0 0 0 0 rgba(242,193,78,.35);cursor:pointer;display:grid;place-items:center;padding:0;animation:bdc-ring 3.2s ease-in-out infinite}
#bdc-l svg{width:40px;height:33px;overflow:visible;filter:drop-shadow(0 0 6px rgba(242,193,78,.45))}
#bdc-l .bdc-n{position:absolute;top:-2px;right:-2px;min-width:18px;height:18px;border-radius:9px;background:#e5484d;color:#fff;font:700 11px/18px system-ui;text-align:center;padding:0 4px}
@keyframes bdc-ring{0%,100%{box-shadow:0 8px 28px rgba(0,0,0,.55),0 0 0 0 rgba(242,193,78,.32)}50%{box-shadow:0 8px 28px rgba(0,0,0,.55),0 0 0 9px rgba(242,193,78,0)}}
.bdc-mark .bdc-sh{animation:bdc-sh 3.6s linear infinite}@keyframes bdc-sh{from{transform:translateX(-120%)}to{transform:translateX(120%)}}
.bdc-mark{animation:bdc-br 4s ease-in-out infinite;transform-origin:50% 50%}@keyframes bdc-br{0%,100%{transform:scale(1)}50%{transform:scale(1.045)}}
.bdc-talk .bdc-mark{animation:bdc-tk .42s ease-in-out infinite alternate}@keyframes bdc-tk{from{transform:scale(.97);filter:brightness(1)}to{transform:scale(1.06);filter:brightness(1.35)}}
#bdc-tz{position:fixed;right:92px;bottom:30px;z-index:2147483000;max-width:230px;background:#141418;color:#f4efe2;border:1px solid rgba(242,193,78,.4);border-radius:14px 14px 4px 14px;padding:10px 30px 10px 13px;font:500 14px/1.35 system-ui,sans-serif;box-shadow:0 10px 30px rgba(0,0,0,.5);cursor:pointer;animation:bdc-in .35s ease-out}
#bdc-tz button{position:absolute;top:4px;right:6px;background:none;border:0;color:#999;font-size:16px;cursor:pointer}
@keyframes bdc-in{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
#bdc-p{position:fixed;right:18px;bottom:94px;z-index:2147483001;width:370px;max-width:calc(100vw - 24px);height:560px;max-height:calc(100vh - 120px);display:flex;flex-direction:column;background:#0d0d10;color:#efe9dc;border:1px solid rgba(242,193,78,.35);border-radius:18px;box-shadow:0 24px 60px rgba(0,0,0,.65);overflow:hidden;font:15px/1.45 system-ui,-apple-system,Segoe UI,sans-serif;animation:bdc-in .25s ease-out}
#bdc-p[hidden]{display:none}
.bdc-h{display:flex;align-items:center;gap:10px;padding:10px 12px;border-bottom:1px solid rgba(255,255,255,.07);background:linear-gradient(180deg,#16140f,#0d0d10)}
.bdc-av{width:46px;height:46px;border-radius:50%;flex:none;display:grid;place-items:center;background:#060608;border:1px solid rgba(242,193,78,.45);overflow:hidden;position:relative}
.bdc-av svg{width:32px;height:27px;overflow:visible}.bdc-av video,.bdc-av img{width:100%;height:100%;object-fit:cover;position:absolute;inset:0}
.bdc-hum .bdc-av{width:84px;height:84px;border-radius:16px}
.bdc-t{flex:1;min-width:0}.bdc-t b{display:block;font:700 15px/1.2 system-ui;letter-spacing:.02em;color:#f2c14e}.bdc-t span{display:block;font-size:12px;color:#a39c8c;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bdc-x{background:none;border:0;color:#bbb;font-size:22px;line-height:1;cursor:pointer;padding:4px 6px}
.bdc-m{flex:1;overflow-y:auto;padding:14px 12px 6px;display:flex;flex-direction:column;gap:8px;scroll-behavior:smooth}
.bdc-b{max-width:86%;padding:9px 12px;border-radius:14px;white-space:pre-wrap;word-wrap:break-word}
.bdc-b.ai,.bdc-b.sys{align-self:flex-start;background:#1a1a20;border:1px solid rgba(255,255,255,.06);border-bottom-left-radius:4px}
.bdc-b.human{align-self:flex-start;background:#22200f;border:1px solid rgba(242,193,78,.4);border-bottom-left-radius:4px}
.bdc-b.user{align-self:flex-end;background:#f2c14e;color:#121212;border-bottom-right-radius:4px}
.bdc-b.note{align-self:center;background:none;color:#a39c8c;font-size:12px;padding:2px}
.bdc-c{display:flex;flex-wrap:wrap;gap:6px;padding:2px 0 4px}
.bdc-c button{background:none;border:1px solid rgba(242,193,78,.5);color:#f2c14e;border-radius:999px;padding:6px 11px;font:600 13px system-ui;cursor:pointer}
.bdc-c button:hover{background:rgba(242,193,78,.12)}
.bdc-dots span{display:inline-block;width:6px;height:6px;margin:0 2px;border-radius:50%;background:#a39c8c;animation:bdc-d 1s infinite}.bdc-dots span:nth-child(2){animation-delay:.15s}.bdc-dots span:nth-child(3){animation-delay:.3s}
@keyframes bdc-d{0%,80%,100%{opacity:.25}40%{opacity:1}}
.bdc-f{display:flex;gap:8px;padding:10px 12px 6px;border-top:1px solid rgba(255,255,255,.07)}
.bdc-f textarea{flex:1;resize:none;height:42px;max-height:110px;background:#16161b;color:#f4efe2;border:1px solid rgba(255,255,255,.12);border-radius:12px;padding:10px 12px;font:15px/1.35 system-ui}
.bdc-f textarea:focus{outline:2px solid rgba(242,193,78,.6);outline-offset:0}
.bdc-f button{background:#f2c14e;color:#111;border:0;border-radius:12px;padding:0 14px;font:700 14px system-ui;cursor:pointer}
.bdc-pv{padding:0 12px 9px;font-size:11px;color:#7d776b;line-height:1.35}
@media (max-width:560px){#bdc-p{right:0;left:0;bottom:0;width:100%;max-width:none;height:min(86vh,640px);max-height:none;border-radius:18px 18px 0 0}#bdc-l{right:14px;bottom:14px}#bdc-tz{right:86px;bottom:24px}}
@media (prefers-reduced-motion:reduce){#bdc-l,.bdc-mark,.bdc-mark .bdc-sh{animation:none!important}}`;
  let st, launcher, panel, list, input, avatar, teaserEl, sid = store.get('sid'), last = store.get('last') || 0, log = store.get('log') || [], mode = store.get('mode') || 'logo';
  let pollT = 0, busy = false, unread = 0;
  const el = (tag, attrs, html) => { const e = document.createElement(tag); if (attrs) for (const k in attrs) e.setAttribute(k, attrs[k]); if (html != null) e.innerHTML = html; return e; };
  function markSVG() {
    const M = window.DOGMA_FXMARK, vb = M ? M.viewBox.join(' ') : '0 0 100 82', id = 'g' + Math.random().toString(36).slice(2, 7);
    const shape = M ? `<path d="${M.d}"/>` : '<path d="M0 0L0 40L45 20Z M0 42L0 82L45 62Z M48 2L48 80L100 41Z"/>';
    return `<svg viewBox="${vb}" aria-hidden="true"><defs><linearGradient id="${id}a" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f7d980"/><stop offset=".55" stop-color="#f2c14e"/><stop offset="1" stop-color="#a87a22"/></linearGradient>
      <linearGradient id="${id}s" x1="0" x2="1"><stop offset=".35" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".75"/><stop offset=".65" stop-color="#fff" stop-opacity="0"/></linearGradient>
      <clipPath id="${id}c">${shape}</clipPath></defs><g class="bdc-mark"><g fill="url(#${id}a)">${shape}</g>
      <g clip-path="url(#${id}c)"><rect class="bdc-sh" x="0" y="0" width="100%" height="100%" fill="url(#${id}s)"/></g></g></svg>`;
  }
  function setAvatar() {
    panel.classList.toggle('bdc-hum', mode === 'human');
    avatar.innerHTML = mode === 'human'
      ? `<img src="${HUMAN.poster}" alt=""><video muted playsinline loop autoplay preload="auto" poster="${HUMAN.poster}" src="${HUMAN.idle}"></video>` : markSVG();
    $('.bdc-t b').textContent = mode === 'human' ? 'BD · ' + t('hostName') : 'BD · BIG DOGMA';
  }
  const $ = s => panel.querySelector(s);
  function talking(on) {
    panel.classList.toggle('bdc-talk', on); launcher.classList.toggle('bdc-talk', on);
    const v = avatar.querySelector('video'); if (v && mode === 'human') { const want = on ? HUMAN.talk : HUMAN.idle; if (v.getAttribute('src') !== want) { v.src = want; v.play().catch(() => {}); } }
  }
  function bubble(role, text, save) {
    const b = el('div', { class: 'bdc-b ' + role }); b.textContent = text; list.appendChild(b); list.scrollTop = list.scrollHeight;
    if (save) { log.push([role, text]); log = log.slice(-60); store.set('log', log); }
    return b;
  }
  function chips(items) {
    const c = el('div', { class: 'bdc-c' });
    items.forEach(([label, fn]) => { const b = el('button', { type: 'button' }); b.textContent = label; b.onclick = () => { c.remove(); fn(); }; c.appendChild(b); });
    list.appendChild(c); list.scrollTop = list.scrollHeight;
  }
  function greet() {
    bubble('ai', t('g1')); bubble('ai', t('g2'));
    chips([[t('toHuman'), () => { switchMode('human'); }], [t('cPrice'), () => send(t('qPrice'))], [t('cPilot'), () => send(t('qPilot'))], [t('cHuman'), () => send(t('qHuman'))]]);
  }
  function switchMode(m) { mode = m; store.set('mode', m); setAvatar(); $('.bdc-sw').textContent = mode === 'human' ? t('toLogo') : t('toHuman'); }
  async function send(text) {
    text = (text || '').trim(); if (!text || busy) return; busy = true; bubble('user', text, true); input.value = '';
    const dots = el('div', { class: 'bdc-b ai bdc-dots', 'aria-label': t('typing') }, '<span></span><span></span><span></span>'); list.appendChild(dots); list.scrollTop = list.scrollHeight; talking(true);
    try {
      const r = await fetch(API + '/msg', { method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sid, text, lang: lang(), page: location.href, company: CO }) });
      const d = await r.json(); if (!r.ok) throw new Error(d.err || r.status);
      sid = d.sid; store.set('sid', sid); dots.remove();
      (d.msgs || []).forEach(m => { bubble(m.role, m.text, true); last = Math.max(last, m.id); }); store.set('last', last);
      if (d.human) bubble('note', t('joined'));
      schedule(4000);
    } catch (e) { dots.remove(); bubble('note', t('err')); }
    busy = false; talking(false);
  }
  async function poll() {
    if (!sid) return;
    try {
      const r = await fetch(`${API}/poll?sid=${encodeURIComponent(sid)}&after=${last}`); if (!r.ok) return;
      const d = await r.json(); let got = 0;
      (d.msgs || []).forEach(m => { if (m.id <= last) return; last = m.id; got++; if (m.role === 'human' && !log.some(x => x[0] === 'note' && x[1] === t('joined'))) bubble('note', t('joined'), true); bubble(m.role, m.text, true); });
      store.set('last', last);
      if (got && panel.hidden) { unread += got; badge(); }
    } catch (e) {}
  }
  function schedule(ms) { clearTimeout(pollT); if (!sid) return; pollT = setTimeout(async () => { await poll(); schedule(panel.hidden ? 20000 : 4000); }, ms); }
  function badge() { let n = launcher.querySelector('.bdc-n'); if (!unread) { if (n) n.remove(); return; } if (!n) { n = el('span', { class: 'bdc-n' }); launcher.appendChild(n); } n.textContent = unread; }
  function open() {
    if (teaserEl) { teaserEl.remove(); teaserEl = null; }
    panel.hidden = false; launcher.setAttribute('aria-expanded', 'true'); unread = 0; badge(); store.set('seen', 1);
    if (!list.childElementCount) { if (log.length) log.forEach(([r, x]) => bubble(r, x)); else greet(); }
    setTimeout(() => input.focus(), 50); schedule(500);
  }
  function close() { panel.hidden = true; launcher.setAttribute('aria-expanded', 'false'); launcher.focus(); schedule(20000); }
  function build() {
    st = el('style'); st.textContent = css; document.head.appendChild(st);
    launcher = el('button', { id: 'bdc-l', type: 'button', 'aria-label': t('open'), 'aria-expanded': 'false', 'aria-controls': 'bdc-p' }, markSVG());
    panel = el('div', { id: 'bdc-p', role: 'dialog', 'aria-label': t('open'), hidden: '' });
    panel.innerHTML = `<div class="bdc-h"><div class="bdc-av"></div><div class="bdc-t"><b></b><span>${t('status')}</span></div>
      <button type="button" class="bdc-c bdc-sw" style="padding:0;border:0"></button><button type="button" class="bdc-x" aria-label="${t('close')}">×</button></div>
      <div class="bdc-m" aria-live="polite"></div>
      <form class="bdc-f"><textarea rows="1" maxlength="1000" placeholder="${t('ph')}" aria-label="${t('ph')}"></textarea><button type="submit">${t('send')}</button></form>
      <div class="bdc-pv">${t('privacy')}</div>`;
    document.body.appendChild(launcher); document.body.appendChild(panel);
    list = $('.bdc-m'); input = $('textarea'); avatar = $('.bdc-av');
    const sw = $('.bdc-sw'); sw.className = 'bdc-sw'; sw.style.cssText = 'background:none;border:1px solid rgba(242,193,78,.5);color:#f2c14e;border-radius:999px;padding:5px 10px;font:600 12px system-ui;cursor:pointer;white-space:nowrap';
    sw.textContent = mode === 'human' ? t('toLogo') : t('toHuman'); sw.onclick = () => switchMode(mode === 'human' ? 'logo' : 'human');
    setAvatar();
    launcher.onclick = () => (panel.hidden ? open() : close()); $('.bdc-x').onclick = close;
    panel.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
    $('form').onsubmit = e => { e.preventDefault(); send(input.value); };
    input.addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(input.value); } });
    // the logo greets once per visit, a few seconds in ("how can I be of service?")
    if (!store.get('seen') && !sessionStorage.getItem('bdc-tz')) setTimeout(() => {
      if (!panel.hidden || teaserEl) return; try { sessionStorage.setItem('bdc-tz', '1'); } catch (e) {}
      teaserEl = el('div', { id: 'bdc-tz', role: 'status' }); teaserEl.textContent = t('teaser');
      const x = el('button', { type: 'button', 'aria-label': t('close') }, '×'); x.onclick = e => { e.stopPropagation(); teaserEl.remove(); teaserEl = null; };
      teaserEl.appendChild(x); teaserEl.onclick = open; document.body.appendChild(teaserEl);
    }, 9000);
    if (sid) schedule(3000);
  }
  // after the page's own splash (company pages lock the body until it ends)
  // shown only once the service can answer (AI key set or the owner's Telegram linked); ?bdchat=1 forces it for testing
  const go = () => { if (!document.body) return setTimeout(go, 200);
    fetch(API + '/ok').then(r => r.json()).then(d => { if (d.ai || d.telegram || /[?&]bdchat=1/.test(location.search)) build(); }).catch(() => {}); };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', go); else go();
  window.BDChat = { open: () => open(), close: () => close() };
})();
