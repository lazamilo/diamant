(() => {
  const d = document, root = d.documentElement, body = d.body;
  root.classList.remove('no-js');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduced) root.classList.add('reduced');
  const hasG = typeof gsap !== 'undefined';
  if (hasG && typeof ScrollTrigger !== 'undefined') gsap.registerPlugin(ScrollTrigger);
  const $ = (s, c = d) => c.querySelector(s), $$ = (s, c = d) => [...c.querySelectorAll(s)];

  /* ---------- smooth scroll ---------- */
  let lenis = null;
  if (!reduced && typeof Lenis !== 'undefined') {
    lenis = new Lenis({ lerp: 0.1, smoothWheel: true });
    if (hasG) { lenis.on('scroll', ScrollTrigger.update); gsap.ticker.add(t => lenis.raf(t * 1000)); gsap.ticker.lagSmoothing(0); }
    else { const raf = t => { lenis.raf(t); requestAnimationFrame(raf); }; requestAnimationFrame(raf); }
  }
  const lock = on => { if (lenis) on ? lenis.stop() : lenis.start(); body.style.overflow = on ? 'hidden' : ''; };
  $$('a[href^="#"]').forEach(a => a.addEventListener('click', e => {
    const t = $(a.getAttribute('href')); if (!t) return; e.preventDefault();
    lenis ? lenis.scrollTo(t, { offset: -90 }) : t.scrollIntoView({ behavior: 'smooth' });
  }));

  /* ---------- nav ---------- */
  const nav = $('.nav');
  const light = nav && nav.classList.contains('is-light');
  let lastY = 0;
  const onScroll = () => {
    const y = scrollY;
    nav.classList.toggle('is-solid', y > 40);
    const hide = y > lastY && y > 500 && !body.classList.contains('mega-open');
    nav.classList.toggle('is-hidden', hide);
    const mbar = $('.mbar'); if (mbar) mbar.style.transform = (y < 300 && !light) ? 'translateY(140%)' : '';
    lastY = y;
  };
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* mega menu */
  const mega = $('.mega'), megaBtn = $('[data-mega]');
  let megaT;
  const openMega = on => { body.classList.toggle('mega-open', on); mega && mega.classList.toggle('is-open', on); megaBtn && megaBtn.setAttribute('aria-expanded', on); };
  if (megaBtn && mega) {
    megaBtn.addEventListener('click', () => openMega(!mega.classList.contains('is-open')));
    megaBtn.addEventListener('mouseenter', () => { clearTimeout(megaT); openMega(true); });
    mega.addEventListener('mouseenter', () => clearTimeout(megaT));
    [megaBtn, mega].forEach(el => el.addEventListener('mouseleave', () => { megaT = setTimeout(() => openMega(false), 250); }));
  }
  /* mobile menu */
  const burger = $('.burger');
  burger && burger.addEventListener('click', () => { const on = !body.classList.contains('menu-open'); body.classList.toggle('menu-open', on); burger.setAttribute('aria-expanded', on); lock(on); });
  /* drawer */
  const openDrawer = on => { body.classList.toggle('drawer-open', on); lock(on); body.classList.remove('menu-open'); if (on) setTimeout(() => { const i = $('.drawer input'); i && i.focus({ preventScroll: true }); }, 500); };
  $$('[data-book]').forEach(b => b.addEventListener('click', e => { e.preventDefault(); openMega(false); openDrawer(true); }));
  $$('.drawer__close, .scrim').forEach(b => b.addEventListener('click', () => { openDrawer(false); openMega(false); }));
  addEventListener('keydown', e => { if (e.key === 'Escape') { openDrawer(false); openMega(false); } });

  /* forms (demo) */
  $$('form.form').forEach(f => f.addEventListener('submit', e => { e.preventDefault(); if (!f.reportValidity()) return; f.classList.add('is-sent'); }));

  /* ---------- loader + hero ---------- */
  const loader = $('.loader');
  const heroIn = () => {
    if (!hasG || reduced) return;
    const F = (sel, vars) => { const t = $$(sel); t.length && gsap.from(t, vars); };
    F('.hero h1 .line>span', { yPercent: 110, duration: 1.3, ease: 'expo.out', stagger: .09 });
    F('.hero__side > *', { y: 30, opacity: 0, duration: 1.1, ease: 'expo.out', stagger: .08, delay: .35 });
    F('.phero .crumbs, .phero .lead, .phero .btn', { y: 30, opacity: 0, duration: 1.1, ease: 'expo.out', stagger: .08, delay: .25 });
    F('.phero h1 .line>span', { yPercent: 110, duration: 1.2, ease: 'expo.out', stagger: .08 });
  };
  const firstVisit = !sessionStorage.getItem('dmt');
  if (loader && hasG && !reduced && firstVisit) {
    try { sessionStorage.setItem('dmt', 1); } catch (e) {}
    lock(true);
    const tl = gsap.timeline({ onComplete: () => { root.classList.add('loaded'); lock(false); } });
    tl.to('.loader__mark img', { clipPath: 'polygon(50% 0%,100% 100%,0% 100%)', duration: .7, ease: 'expo.out' })
      .to('.loader__mark img', { clipPath: 'polygon(0% 0%,100% 0%,100% 100%,0% 100%)', duration: .7, ease: 'expo.inOut' })
      .to('.loader__bar span', { scaleX: 1, duration: 1.2, ease: 'power2.inOut' }, 0)
      .to('.loader__mark', { scale: .9, opacity: 0, duration: .5, ease: 'power2.in' }, '+=.1')
      .to('.loader__bar', { opacity: 0, duration: .3 }, '<')
      .to(loader, { clipPath: 'polygon(0 0,100% 0,100% 0,0 0)', duration: 1, ease: 'expo.inOut' }, '-=.15')
      .add(heroIn, '-=.55');
    loader.style.clipPath = 'polygon(0 0,100% 0,100% 100%,0 100%)';
  } else { root.classList.add('loaded'); heroIn(); }

  /* hero slideshow */
  const slides = $$('.hero__media img'), dots = $$('.hero__dots i b');
  if (slides.length) {
    let i = 0; const dur = 6;
    const show = n => {
      slides.forEach((s, k) => s.classList.toggle('is-on', k === n));
      if (hasG && !reduced) {
        gsap.fromTo(slides[n], { scale: 1.12 }, { scale: 1, duration: dur + 1.6, ease: 'none' });
        dots.forEach((b, k) => gsap.set(b, { scaleX: k < n ? 1 : 0 }));
        dots[n] && gsap.fromTo(dots[n], { scaleX: 0 }, { scaleX: 1, duration: dur, ease: 'none' });
      } else slides[n].style.transform = 'none';
    };
    show(0);
    if (slides.length > 1) setInterval(() => { i = (i + 1) % slides.length; show(i); }, dur * 1000);
    if (hasG && !reduced) gsap.to('.hero__media', { yPercent: 18, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
  }

  if (!hasG || reduced) { $$('.rv').forEach(e => e.style.opacity = 1); return; }

  /* ---------- reveals ---------- */
  $$('.rv').forEach(el => gsap.to(el, { opacity: 1, y: 0, duration: 1.2, ease: 'expo.out', scrollTrigger: { trigger: el, start: 'top 88%' } }));
  $$('[data-split]').forEach(el => {
    const spans = $$('.line>span', el);
    gsap.from(spans, { yPercent: 110, duration: 1.2, ease: 'expo.out', stagger: .08, scrollTrigger: { trigger: el, start: 'top 85%' } });
  });
  $$('[data-par] img').forEach(img => gsap.fromTo(img, { yPercent: -8 }, { yPercent: 8, ease: 'none', scrollTrigger: { trigger: img.parentElement, start: 'top bottom', end: 'bottom top', scrub: true } }));

  /* statement word fill */
  const big = $('.statement .big');
  if (big) {
    const words = big.textContent.trim().split(/\s+/);
    big.innerHTML = words.map(w => `<span class="w">${w}</span>`).join(' ');
    const ws = $$('.w', big);
    ScrollTrigger.create({ trigger: big, start: 'top 80%', end: 'bottom 45%', scrub: true,
      onUpdate: s => { const n = Math.round(s.progress * ws.length); ws.forEach((w, k) => w.classList.toggle('on', k < n)); } });
  }
  /* counters */
  $$('[data-count]').forEach(el => {
    const to = +el.dataset.count, fmt = n => n.toLocaleString('sl-SI');
    const o = { v: 0 };
    gsap.to(o, { v: to, duration: 2, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 90%' }, onUpdate: () => el.firstChild.nodeValue = fmt(Math.round(o.v)) });
  });

  /* services tabs + floating image */
  $$('.tabs button').forEach(b => b.addEventListener('click', () => {
    $$('.tabs button').forEach(x => x.classList.toggle('is-on', x === b));
    $$('.svc-list').forEach(l => l.hidden = l.dataset.list !== b.dataset.tab);
    const vis = $(`.svc-list[data-list="${b.dataset.tab}"]`);
    gsap.from($$('li', vis), { y: 30, opacity: 0, duration: .8, ease: 'expo.out', stagger: .04 });
    ScrollTrigger.refresh();
  }));
  const fl = $('.float-img');
  if (fl && matchMedia('(hover:hover)').matches) {
    const fi = $('img', fl);
    const xTo = gsap.quickTo(fl, 'x', { duration: .6, ease: 'power3' }), yTo = gsap.quickTo(fl, 'y', { duration: .6, ease: 'power3' });
    $$('.svc-list a').forEach(a => {
      a.addEventListener('mouseenter', () => { fi.src = a.dataset.img; fl.classList.add('on'); });
      a.addEventListener('mouseleave', () => fl.classList.remove('on'));
    });
    addEventListener('mousemove', e => { xTo(e.clientX + 40); yTo(e.clientY); });
  }

  /* all-on-4 story */
  const steps = $$('.step'), figs = $$('.story__stage figure');
  if (steps.length) {
    const act = n => { steps.forEach((s, k) => s.classList.toggle('on', k === n)); figs.forEach((f, k) => f.classList.toggle('on', k === n)); };
    act(0);
    steps.forEach((s, k) => ScrollTrigger.create({ trigger: s, start: 'top 60%', end: 'bottom 60%', onToggle: st => st.isActive && act(k) }));
  }

  /* before/after */
  $$('.ba').forEach(ba => {
    const set = x => { const r = ba.getBoundingClientRect(); const p = Math.min(100, Math.max(0, (x - r.left) / r.width * 100)); ba.style.setProperty('--p', p + '%'); };
    let down = false;
    ba.addEventListener('pointerdown', e => { down = true; ba.setPointerCapture(e.pointerId); set(e.clientX); });
    ba.addEventListener('pointermove', e => down && set(e.clientX));
    ba.addEventListener('pointerup', () => down = false);
    const o = { p: 85 };
    gsap.to(o, { p: 50, duration: 1.6, ease: 'expo.inOut', scrollTrigger: { trigger: ba, start: 'top 75%' }, onUpdate: () => ba.style.setProperty('--p', o.p + '%') });
  });

  /* bento */
  gsap.utils.toArray('.tile').forEach((t, k) => gsap.from(t, { y: 60, opacity: 0, duration: 1.2, ease: 'expo.out', delay: (k % 3) * .08, scrollTrigger: { trigger: t, start: 'top 92%' } }));

  /* team horizontal */
  const track = $('.team__track');
  if (track) {
    const mm = gsap.matchMedia();
    mm.add('(min-width: 861px)', () => {
      const dist = () => track.scrollWidth - innerWidth;
      gsap.to(track, { x: () => -dist(), ease: 'none', scrollTrigger: { trigger: '.team', start: 'top top', end: () => '+=' + dist(), pin: true, scrub: 1, invalidateOnRefresh: true,
        onUpdate: s => gsap.set('.team__bar span', { scaleX: s.progress }) } });
    });
    mm.add('(max-width: 860px)', () => { track.style.overflowX = 'auto'; track.style.scrollSnapType = 'x mandatory'; $$('.member', track).forEach(m => m.style.scrollSnapAlign = 'start'); });
  }

  /* quotes */
  const qs = $$('.q'), qc = $('.q-count');
  if (qs.length) {
    let qi = 0, qt;
    const showQ = n => { qi = (n + qs.length) % qs.length; qs.forEach((q, k) => q.classList.toggle('on', k === qi)); if (qc) qc.textContent = `${qi + 1} / ${qs.length}`;
      gsap.fromTo($('blockquote', qs[qi]), { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: .9, ease: 'expo.out' }); clearInterval(qt); qt = setInterval(() => showQ(qi + 1), 9000); };
    showQ(0);
    $('[data-q="prev"]') && $('[data-q="prev"]').addEventListener('click', () => showQ(qi - 1));
    $('[data-q="next"]') && $('[data-q="next"]').addEventListener('click', () => showQ(qi + 1));
  }

  /* band number */
  const bn = $('.band__num');
  bn && gsap.from(bn, { xPercent: -30, opacity: 0, duration: 1.4, ease: 'expo.out', scrollTrigger: { trigger: bn, start: 'top 85%' } });

  /* price nav active */
  const pn = $$('.price-nav a');
  pn.forEach(a => { const t = $(a.getAttribute('href')); t && ScrollTrigger.create({ trigger: t, start: 'top 50%', end: 'bottom 50%', onToggle: s => s.isActive && pn.forEach(x => x.classList.toggle('on', x === a)) }); });

  addEventListener('load', () => ScrollTrigger.refresh());
})();
