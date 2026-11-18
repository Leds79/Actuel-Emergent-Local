// Accueil : un écran de détection s'expose photon par photon.
// Chaque point arrive en un lieu et à un instant ; les bandes n'apparaissent qu'avec le nombre.
(function () {
  const plaque = $('.plaque');
  if (!plaque) return;
  const A = $('#expo-a'), B = $('#expo-b'), sortie = $('#expo-n'), bouton = $('#expo-re');
  const a = A.getContext('2d'), b = B.getContext('2d');
  const MAX = 16000, FIXE = reduceMotion || location.hash === '#fixe';
  const pts = new Float32Array(2 * MAX);
  let n = 0, W = 1, H = 1, dpr = 1, raf = 0, visible = true, queue = 0, hasard = mulberry(20261117);

  // deux chemins qui interfèrent : neuf franges sous une enveloppe, comme derrière deux fentes
  const intensite = u => {
    const e = u === 0 ? 1 : Math.sin(Math.PI * u) / (Math.PI * u), c = Math.cos(4.5 * Math.PI * u);
    return c * c * e * e;
  };
  const tirer = () => {
    let u;
    do { u = 2 * hasard() - 1; } while (hasard() > intensite(u));
    pts[2 * n] = u; pts[2 * n + 1] = hasard(); n++;
  };
  const X = u => (0.5 + 0.47 * u) * W, Y = v => (0.13 + 0.74 * v) * H;
  const point = (c, i, r, alpha) => {
    c.globalAlpha = alpha; c.beginPath(); c.arc(X(pts[2 * i]), Y(pts[2 * i + 1]), r, 0, 6.2832); c.fill();
  };
  const compter = () => { sortie.textContent = frNum(n); };
  const tailler = () => {
    const r = plaque.getBoundingClientRect();
    dpr = Math.min(2, window.devicePixelRatio || 1);
    W = Math.max(1, Math.round(r.width * dpr)); H = Math.max(1, Math.round(r.height * dpr));
    A.width = B.width = W; A.height = B.height = H;
    a.fillStyle = b.fillStyle = css('--photon') || '#ffefc4';
    a.globalCompositeOperation = 'lighter';
    for (let i = 0; i < n; i++) point(a, i, 0.85 * dpr, 0.5);
  };
  const pas = () => {
    raf = 0;
    if (!visible) return;
    // les éclats des dernières arrivées s'éteignent
    b.globalCompositeOperation = 'destination-out'; b.globalAlpha = 0.16; b.fillRect(0, 0, W, H);
    b.globalCompositeOperation = 'source-over';
    if (n < MAX) {
      // d'abord un par un, puis de plus en plus vite
      const k = Math.min(MAX - n, Math.max(1, Math.round(n / 90)), 44);
      for (let j = 0; j < k; j++) { tirer(); point(a, n - 1, 0.85 * dpr, 0.5); point(b, n - 1, 2.6 * dpr, 0.9); }
      compter();
      queue = 40;
    } else queue--;
    if (n < MAX || queue > 0) raf = requestAnimationFrame(pas);
  };
  const lancer = () => { if (!raf && !FIXE && (n < MAX || queue > 0)) raf = requestAnimationFrame(pas); };
  const remplir = () => { while (n < MAX) tirer(); };

  if (FIXE) remplir();
  tailler(); compter();
  if ('ResizeObserver' in window) {
    let attente = 0;
    new ResizeObserver(() => { cancelAnimationFrame(attente); attente = requestAnimationFrame(tailler); }).observe(plaque);
  }
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(es => { visible = es[0].isIntersecting; if (visible) lancer(); }).observe(plaque);
  }
  bouton.addEventListener('click', () => {
    n = 0; queue = 0; hasard = mulberry((Date.now() & 0xfffffff) || 1);
    if (FIXE) remplir();
    tailler(); compter(); lancer();
  });
  lancer();
})();
