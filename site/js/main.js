(() => {
  document.documentElement.classList.replace('no-js', 'js');

  // menu
  const burger = document.querySelector('.burger');
  const nav = document.getElementById('nav');
  burger.addEventListener('click', () => {
    const open = burger.getAttribute('aria-expanded') !== 'true';
    burger.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
    document.body.style.overflow = open ? 'hidden' : '';
  });
  nav.querySelectorAll('a').forEach(a => a.addEventListener('click', () => { if (nav.classList.contains('is-open')) burger.click(); }));

  // reveal
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px' });
  document.querySelectorAll('.rv').forEach(el => io.observe(el));

  // filters + sort
  const list = document.querySelector('#homes .cards');
  if (list) {
    const cards = [...list.children];
    let area = 'all';
    document.querySelectorAll('.seg button').forEach(b => b.addEventListener('click', () => {
      document.querySelectorAll('.seg button').forEach(x => x.classList.toggle('on', x === b));
      area = b.dataset.v;
      cards.forEach(c => c.classList.toggle('hide', area !== 'all' && c.dataset.area !== area));
    }));
    const sel = document.querySelector('[data-sort]');
    sel.addEventListener('change', () => {
      const dir = sel.value === 'asc' ? 1 : -1;
      cards.sort((a, b) => (a.dataset.price - b.dataset.price) * dir).forEach(c => list.appendChild(c));
    });
  }

  // ---- currencies: live daily rates (ECB via Frankfurter), cached for 24 h ----
  const CUR = {
    EUR: { sym: '€', name: 'euros', locale: 'en-IE' },
    GBP: { sym: '£', name: 'pounds', locale: 'en-GB' },
    USD: { sym: '$', name: 'dollars', locale: 'en-US' },
  };
  const store = {
    get(k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* storage blocked: fine */ } },
  };
  const guess = () => {
    const l = (navigator.language || '').toLowerCase();
    if (l === 'en-gb' || l.endsWith('-gb')) return 'GBP';
    if (l === 'en-us' || l.endsWith('-us')) return 'USD';
    return 'EUR';
  };
  let cur = store.get('iga-cur') || guess();
  if (!CUR[cur]) cur = 'EUR';
  const fb = window.FX_FALLBACK || { date: '', EUR: 0.0056, GBP: 0.0048, USD: 0.0063 };
  let fx = { date: fb.date, rates: { EUR: fb.EUR, GBP: fb.GBP, USD: fb.USD }, live: false };

  const money = (yenV) => {
    const c = CUR[cur], v = yenV * fx.rates[cur];
    const r = v >= 1000 ? Math.round(v / 100) * 100 : Math.round(v / 10) * 10;
    return c.sym + r.toLocaleString(c.locale);
  };
  const fmtDate = d => { try { return new Date(d + 'T12:00:00Z').toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' }); } catch (e) { return d; } };
  const render = () => {
    document.querySelectorAll('.fx').forEach(el => { el.textContent = '≈ ' + money(+el.dataset.yen); });
    document.querySelectorAll('[data-fx-name]').forEach(el => { el.textContent = CUR[cur].name; });
    const per = Math.round(1 / fx.rates[cur]);
    document.querySelectorAll('[data-fx-note]').forEach(el => {
      el.textContent = `Approximate ${CUR[cur].name}: ${CUR[cur].sym}1 = ¥${per} (European Central Bank reference rate, ${fmtDate(fx.date)}${fx.live ? '' : ' — offline estimate'}). Rates are checked once a day; the price you pay is in yen.`;
    });
    document.querySelectorAll('[data-cur]').forEach(s => { s.value = cur; });
  };
  document.querySelectorAll('[data-cur]').forEach(s => s.addEventListener('change', () => { cur = s.value; store.set('iga-cur', cur); render(); }));

  const DAY = 24 * 60 * 60 * 1000;
  const cached = store.get('iga-fx');
  if (cached && cached.rates && Date.now() - cached.fetched < DAY) {
    fx = { date: cached.date, rates: cached.rates, live: true };
  } else {
    fetch('https://api.frankfurter.dev/v1/latest?base=JPY&symbols=USD,EUR,GBP')
      .then(r => r.ok ? r.json() : Promise.reject(r.status))
      .then(j => {
        if (!j.rates || !j.rates.EUR) return;
        fx = { date: j.date, rates: { EUR: j.rates.EUR, GBP: j.rates.GBP, USD: j.rates.USD }, live: true };
        store.set('iga-fx', { date: j.date, rates: fx.rates, fetched: Date.now() });
        render();
      })
      .catch(() => { /* keep fallback rates */ });
  }
  render();

  // fee calculator
  const calc = document.querySelector('.calc');
  if (calc) {
    const fee = +calc.dataset.fee;
    const yen = v => '¥' + Math.round(v).toLocaleString('en-GB');
    const out = k => calc.querySelector(`[data-o="${k}"]`);
    const input = calc.querySelector('input');
    const upd = () => {
      const p = +input.value, f = p * fee;
      out('price').textContent = yen(p); out('fee').textContent = yen(f); out('total').textContent = yen(p + f);
      const row = out('eur'); const span = row && row.querySelector('.fx'); if (span) { span.dataset.yen = p + f; span.textContent = '≈ ' + money(p + f); }
    };
    input.addEventListener('input', upd); upd();
  }

  // gallery
  const main = document.querySelector('.g-main img');
  document.querySelectorAll('.g-thumbs button').forEach(b => b.addEventListener('click', () => {
    main.src = b.dataset.src;
    document.querySelectorAll('.g-thumbs button').forEach(x => x.classList.toggle('on', x === b));
  }));
})();
