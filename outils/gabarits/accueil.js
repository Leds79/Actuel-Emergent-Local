// Accueil : un écran de détection s'expose photon par photon.
// Chaque point arrive en un lieu et à un instant ; les franges n'apparaissent qu'avec le nombre.
// Si l'on apprend par où passe chaque photon, les franges disparaissent.
(function () {
  const plaque = $('.plaque.expo-ecran');
  if (!plaque) return;
  const A = $('#expo-a'), B = $('#expo-b'), sortie = $('#expo-n'), bouton = $('#expo-re');
  const libre = $('#expo-libre'), connue = $('#expo-route'), legende = $('#expo-txt');
  const a = A.getContext('2d'), b = B.getContext('2d');
  const MAX = 16000, FIXE = reduceMotion || /^#fi[xg]e/.test(location.hash);
  const pts = new Float32Array(2 * MAX);
  let n = 0, W = 1, H = 1, dpr = 1, raf = 0, visible = true, queue = 0, route = false, dernier = 0, hasard = mulberry(20261117);
  const TEXTES = [
    'Chaque point est l’arrivée d’un photon : un lieu, un instant. Aucun ne dessine les franges, ces bandes qui n’apparaissent qu’avec le nombre.',
    'Un détecteur signale maintenant par où passe chaque photon. Les arrivées restent des points, mais les franges ont disparu : il ne reste qu’une tache.'
  ];

  // deux chemins qui interfèrent : neuf franges sous une enveloppe. Route connue : l'enveloppe seule.
  const intensite = u => {
    const e = u === 0 ? 1 : Math.sin(Math.PI * u) / (Math.PI * u);
    if (route) return e * e;
    const c = Math.cos(4.5 * Math.PI * u);
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
  const pas = ts => {
    raf = 0;
    if (!visible) { dernier = 0; return; }
    // la cadence suit le temps écoulé, pas le nombre d'images : même durée sur un écran à 60 ou à 120 images par seconde
    const rythme = dernier ? clamp((ts - dernier) / 16.7, 0.4, 3) : 1;
    dernier = ts;
    // les éclats des dernières arrivées s'éteignent
    b.globalCompositeOperation = 'destination-out'; b.globalAlpha = 0.16; b.fillRect(0, 0, W, H);
    b.globalCompositeOperation = 'source-over';
    if (n < MAX) {
      // d'abord un par un, puis de plus en plus vite
      const k = Math.min(MAX - n, Math.max(1, Math.round(rythme * Math.min(44, n / 90))));
      for (let j = 0; j < k; j++) { tirer(); point(a, n - 1, 0.85 * dpr, 0.5); point(b, n - 1, 2.6 * dpr, 0.9); }
      compter();
      queue = 40;
    } else queue--;
    if (n < MAX || queue > 0) raf = requestAnimationFrame(pas); else dernier = 0;
  };
  const lancer = () => { if (!raf && !FIXE && (n < MAX || queue > 0)) raf = requestAnimationFrame(pas); };
  const remplir = () => { while (n < MAX) tirer(); };
  const recommencer = () => {
    n = 0; queue = 0; hasard = mulberry((Date.now() & 0xfffffff) || 1);
    if (FIXE) remplir();
    tailler(); compter(); lancer();
  };
  const choisir = connu => {
    route = connu;
    if (libre) libre.setAttribute('aria-pressed', connu ? 'false' : 'true');
    if (connue) connue.setAttribute('aria-pressed', connu ? 'true' : 'false');
    if (legende) legende.textContent = TEXTES[connu ? 1 : 0];
    recommencer();
  };

  if (FIXE) remplir();
  tailler(); compter();
  if ('ResizeObserver' in window) {
    let attente = 0;
    new ResizeObserver(() => { cancelAnimationFrame(attente); attente = requestAnimationFrame(tailler); }).observe(plaque);
  }
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(es => { visible = es[es.length - 1].isIntersecting; if (visible) lancer(); }).observe(plaque);
  }
  if (bouton) bouton.addEventListener('click', recommencer);
  if (libre) libre.addEventListener('click', () => choisir(false));
  if (connue) connue.addEventListener('click', () => choisir(true));
  lancer();
})();

// Frise des travaux : une bulle nomme la référence survolée, touchée ou atteinte au clavier.
// La frise existe en deux mises en page (large et étroite) ; une seule est affichée à la fois.
$$('.frise').forEach(frise => {
  const fig = frise.closest('.fig'), bulle = $('.bulle', fig), refs = $$('.ref', frise);
  const montrer = g => {
    bulle.textContent = '';
    const titre = document.createElement('b'); titre.textContent = g.dataset.t;
    bulle.appendChild(titre); bulle.appendChild(document.createTextNode(g.dataset.s));
    bulle.style.left = bulle.style.top = '0';              // remise à zéro avant la mesure : sa largeur ne dépend plus de l'ancienne position
    bulle.hidden = false;
    const r = $('.pt', g).getBoundingClientRect(), f = fig.getBoundingClientRect();
    const x = clamp(r.left + r.width / 2 - f.left - bulle.offsetWidth / 2, 6, Math.max(6, f.width - bulle.offsetWidth - 6));
    let y = r.top - f.top - bulle.offsetHeight - 10;
    if (y < 4) y = r.bottom - f.top + 10;
    bulle.style.left = x + 'px'; bulle.style.top = y + 'px';
  };
  const cacher = () => { bulle.hidden = true; };
  refs.forEach((g, i) => {
    // au clavier : un seul arrêt de tabulation, puis les flèches passent d'un point au suivant
    g.setAttribute('tabindex', i ? '-1' : '0');
    g.addEventListener('keydown', e => {
      const d = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? 1 : e.key === 'ArrowLeft' || e.key === 'ArrowUp' ? -1 : 0;
      if (d && refs[i + d]) { e.preventDefault(); refs[i + d].focus(); }
      if (e.key === 'Escape') cacher();
    });
    g.addEventListener('pointerenter', () => montrer(g));
    g.addEventListener('pointerleave', e => { if (e.pointerType === 'mouse') cacher(); });
    g.addEventListener('focus', () => montrer(g));
    g.addEventListener('blur', cacher);
    g.addEventListener('click', () => montrer(g));
  });
  const scene = $('.stage', fig);
  if (scene) scene.addEventListener('scroll', cacher, { passive: true });
  document.addEventListener('pointerdown', e => { if (!e.target.closest || !e.target.closest('.frise .ref')) cacher(); });
});
