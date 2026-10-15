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

  // fee calculator
  const calc = document.querySelector('.calc');
  if (calc) {
    const rate = +calc.dataset.rate, fee = +calc.dataset.fee;
    const yen = v => '¥' + Math.round(v).toLocaleString('en-GB');
    const eur = v => '€' + (Math.round(v / rate / 100) * 100).toLocaleString('en-GB');
    const out = k => calc.querySelector(`[data-o="${k}"]`);
    const input = calc.querySelector('input');
    const upd = () => { const p = +input.value, f = p * fee; out('price').textContent = yen(p); out('fee').textContent = yen(f); out('total').textContent = yen(p + f); out('eur').textContent = eur(p + f); };
    input.addEventListener('input', upd); upd();
  }

  // gallery
  const main = document.querySelector('.g-main img');
  document.querySelectorAll('.g-thumbs button').forEach(b => b.addEventListener('click', () => {
    main.src = b.dataset.src;
    document.querySelectorAll('.g-thumbs button').forEach(x => x.classList.toggle('on', x === b));
  }));
})();
