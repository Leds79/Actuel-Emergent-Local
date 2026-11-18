// Épures : un dessin animé par pilier, tracé au trait sur le plan bleu.
// Chaque dessin ne dépend que du temps : on peut l'arrêter sur n'importe quelle image.
(function () {
  const toiles = $$('canvas[data-epure]');
  if (!toiles.length) return;
  const ENCRE = '#f3f6fb', PALE = 'rgba(205,225,255,.62)', TRAIT = 'rgba(205,225,255,.3)', PHOTON = '#ffefc4', TOUR = 6.2832;

  const trait = (g, x1, y1, x2, y2, couleur, ep, tirets) => {
    g.save(); g.strokeStyle = couleur; g.lineWidth = ep; if (tirets) g.setLineDash(tirets);
    g.beginPath(); g.moveTo(x1, y1); g.lineTo(x2, y2); g.stroke(); g.restore();
  };
  const disque = (g, x, y, r, couleur, alpha) => {
    g.save(); g.globalAlpha *= alpha == null ? 1 : alpha; g.fillStyle = couleur; g.beginPath(); g.arc(x, y, r, 0, TOUR); g.fill(); g.restore();
  };
  const anneau = (g, x, y, r, couleur, ep) => {
    g.save(); g.strokeStyle = couleur; g.lineWidth = ep; g.beginPath(); g.arc(x, y, r, 0, TOUR); g.stroke(); g.restore();
  };
  const mot = (g, texte, x, y, u, cote, couleur) => {
    g.save(); g.font = '500 ' + (10 * u) + 'px "IBM Plex Mono", ui-monospace, Consolas, monospace';
    if ('letterSpacing' in g) g.letterSpacing = (1.1 * u) + 'px';
    g.textAlign = cote || 'left'; g.textBaseline = 'middle'; g.fillStyle = couleur || PALE; g.fillText(texte, x, y); g.restore();
  };

  // Pilier 1. Une source balaie un écran plat. Chaque photon file droit à la vitesse c :
  // ensemble ils dessinent une spirale, et la tache n'est que l'endroit où elle touche l'écran.
  const balayage = (g, W, H, t, u, petit) => {
    const T = 5.6, tt = t % T, ox = 0.14 * W, oy = 0.84 * H, sy = 0.22 * H, D = oy - sy;
    const om = 1.2, c = D * om / 2, thMax = 1.03, tau1 = thMax / om;   // Dω/c = 2 : la visée court deux fois plus vite que la lumière
    trait(g, 0.05 * W, sy, 0.96 * W, sy, ENCRE, 1.8 * u);
    trait(g, ox, oy, ox, sy, TRAIT, u);
    g.save(); g.strokeStyle = TRAIT; g.lineWidth = u; g.setLineDash([4 * u, 5 * u]);
    g.beginPath(); g.arc(ox, oy, D, -TOUR / 4, -TOUR / 4 + 1.15); g.stroke(); g.restore();
    if (tt < tau1) {
      const xa = ox + D * Math.tan(om * tt);
      trait(g, ox, oy, xa, sy, TRAIT, u, [3 * u, 5 * u]); anneau(g, xa, sy, 4.5 * u, PALE, 1.3 * u);
      if (!petit) mot(g, 'VISÉE', xa, sy - 13 * u, u, 'center');
    }
    let tache = null, k = 0;
    for (let tau = 0; tau <= tau1 && tau <= tt; tau += 0.016, k++) {
      const th = om * tau, R = D / Math.cos(th), r = c * (tt - tau), sx = Math.sin(th), cy = -Math.cos(th);
      if (r < R) {
        if (k % 9 === 0) trait(g, ox, oy, ox + r * sx, oy + r * cy, 'rgba(255,239,196,.13)', u);
        disque(g, ox + r * sx, oy + r * cy, 1.6 * u, PHOTON, 0.95);
      } else {
        const xi = ox + D * Math.tan(th), age = (r - R) / c;
        disque(g, xi, sy, 1.3 * u, PHOTON, 0.4);
        if (age < 0.45) { disque(g, xi, sy, (2.5 + 6 * age / 0.45) * u, PHOTON, 0.55 * (1 - age / 0.45)); tache = xi; }
      }
    }
    disque(g, ox, oy, 4.5 * u, ENCRE);
    if (!petit) {
      mot(g, 'SOURCE', ox + 11 * u, oy + 2 * u, u);
      if (tt >= tau1) mot(g, 'ÉCRAN PLAT', 0.96 * W, sy - 13 * u, u, 'right');
      if (tache != null) mot(g, 'TACHE', tache, sy + 15 * u, u, 'center', PHOTON);
    }
  };

  // Pilier 2. Le faisceau traverse la pièce sans se montrer. Seul un grain de poussière qui le croise
  // s'allume, et c'est lui que l'œil voit.
  const poussiere = (g, W, H, t, u, petit) => {
    const by = 0.4 * H, lx = 0.13 * W, mx = 0.9 * W, ex = 0.52 * W, ey = 0.85 * H, hasard = mulberry(7);
    g.save(); g.strokeStyle = ENCRE; g.lineWidth = 1.5 * u; g.strokeRect(lx - 30 * u, by - 9 * u, 30 * u, 18 * u); g.restore();
    trait(g, mx, 0.14 * H, mx, 0.66 * H, ENCRE, 1.8 * u);
    trait(g, lx, by, mx, by, 'rgba(205,225,255,.16)', u, [2 * u, 7 * u]);
    trait(g, mx, by, ex, ey, 'rgba(255,239,196,.4)', u);
    disque(g, mx, by, 8 * u, PHOTON, 0.25); disque(g, mx, by, 3.6 * u, PHOTON);
    for (let k = 0; k < 34; k++) {
      const x0 = lx + (mx - lx) * (0.05 + 0.9 * hasard()), y0 = (0.14 + 0.52 * hasard()) * H, A = (0.05 + 0.1 * hasard()) * H;
      const Tk = 5 + 6 * hasard(), ph = TOUR * hasard();
      const y = y0 + A * Math.sin(TOUR * t / Tk + ph), x = x0 + 6 * u * Math.sin(TOUR * t / (1.7 * Tk) + ph), d = Math.abs(y - by);
      if (d < 5 * u) {
        const f = 1 - d / (5 * u);
        trait(g, x, y, ex, ey, 'rgba(255,239,196,' + (0.55 * f).toFixed(3) + ')', u);
        disque(g, x, y, 7 * u, PHOTON, 0.25 * f); disque(g, x, y, 2.3 * u, PHOTON);
      } else disque(g, x, y, 1.3 * u, PALE, 0.55);
    }
    g.save(); g.strokeStyle = ENCRE; g.lineWidth = 1.5 * u; g.beginPath(); g.ellipse(ex, ey, 14 * u, 7 * u, 0, 0, TOUR); g.stroke(); g.restore();
    disque(g, ex, ey, 3.4 * u, ENCRE);
    if (!petit) {
      mot(g, 'LASER', lx - 30 * u, by - 20 * u, u);
      mot(g, 'MUR', mx, 0.1 * H, u, 'center');
      mot(g, 'ŒIL, PLACÉ DE CÔTÉ', ex, ey + 19 * u, u, 'center');
    }
  };

  // Pilier 3. Près de la masse, l'horloge bat moins vite. Le bas de chaque front d'onde avance moins :
  // le front pivote et la trajectoire vire vers le temps lent.
  const horloge = (g, x, y, r, tours, u) => {
    anneau(g, x, y, r, ENCRE, 1.5 * u);
    for (let i = 0; i < 12; i++) {
      const a = i * TOUR / 12, c = Math.cos(a), s = Math.sin(a);
      trait(g, x + (r - 4 * u) * c, y + (r - 4 * u) * s, x + (r - 1.2 * u) * c, y + (r - 1.2 * u) * s, TRAIT, u);
    }
    const a = tours * TOUR - TOUR / 4;
    trait(g, x, y, x + 0.72 * r * Math.cos(a), y + 0.72 * r * Math.sin(a), PHOTON, 2 * u); disque(g, x, y, 2.3 * u, ENCRE);
  };
  const pente = (g, W, H, t, u, petit) => {
    g.save(); g.beginPath(); g.arc(0.5 * W, 0.9 * H + 2.2 * W, 2.2 * W, 0, TOUR);
    g.fillStyle = 'rgba(205,225,255,.1)'; g.fill(); g.strokeStyle = ENCRE; g.lineWidth = 1.8 * u; g.stroke(); g.restore();
    horloge(g, 0.13 * W, 0.24 * H, 24 * u, t / 3.2, u);
    horloge(g, 0.13 * W, 0.66 * H, 24 * u, 0.55 * t / 3.2, u);
    const x0 = 0.31 * W, L = 0.6 * W, y0 = 0.27 * H, A = 0.47 * H, Y = s => y0 + A * s * s, incl = s => Math.atan(2 * A * s / L);
    g.save(); g.strokeStyle = TRAIT; g.lineWidth = u; g.setLineDash([4 * u, 5 * u]); g.beginPath();
    for (let i = 0; i <= 40; i++) { const s = i / 40; if (i) g.lineTo(x0 + L * s, Y(s)); else g.moveTo(x0, Y(0)); }
    g.stroke(); g.restore();
    for (let j = 0; j < 6; j++) {
      const s = (t * 0.17 + j / 6) % 1, a = incl(s), nx = -Math.sin(a), ny = Math.cos(a), x = x0 + L * s, y = Y(s), d = 17 * u;
      g.save(); g.globalAlpha = Math.sin(Math.PI * s); trait(g, x - nx * d, y - ny * d, x + nx * d, y + ny * d, PHOTON, 2 * u); g.restore();
    }
    const a1 = incl(1), fx = x0 + L, fy = Y(1), fl = 10 * u;
    g.save(); g.fillStyle = PALE; g.beginPath(); g.moveTo(fx + fl * Math.cos(a1), fy + fl * Math.sin(a1));
    g.lineTo(fx - fl * 0.5 * Math.cos(a1 - 0.9), fy - fl * 0.5 * Math.sin(a1 - 0.9));
    g.lineTo(fx - fl * 0.5 * Math.cos(a1 + 0.9), fy - fl * 0.5 * Math.sin(a1 + 0.9)); g.closePath(); g.fill(); g.restore();
    if (!petit) {
      mot(g, 'LOIN : TEMPS RAPIDE', 0.045 * W, 0.24 * H - 38 * u, u);
      mot(g, 'PRÈS : TEMPS LENT', 0.045 * W, 0.66 * H + 38 * u, u);
      mot(g, 'MASSE', 0.5 * W, 0.955 * H, u, 'center');
    }
  };

  // Pilier 4. Le photon contourne la galaxie par deux routes à la fois. Au dernier moment, on place ou non
  // une lame : sans elle on apprend la route, avec elle on lit le décalage entre les deux routes.
  const choix = (g, W, H, t, u, petit) => {
    const T = 5.2, k = Math.floor(t / T), tt = t - k * T, lame = k % 2 === 1;
    const S = [0.09 * W, 0.5 * H], M = [0.68 * W, 0.5 * H], P1 = [0.38 * W, 0.02 * H], P2 = [0.38 * W, 0.98 * H];
    const D1 = [0.89 * W, 0.164 * H], D2 = [0.89 * W, 0.836 * H];
    const sur = (P, s) => [(1 - s) * (1 - s) * S[0] + 2 * (1 - s) * s * P[0] + s * s * M[0], (1 - s) * (1 - s) * S[1] + 2 * (1 - s) * s * P[1] + s * s * M[1]];
    [P1, P2].forEach(P => {
      g.save(); g.strokeStyle = TRAIT; g.lineWidth = u; g.setLineDash([4 * u, 5 * u]);
      g.beginPath(); g.moveTo(S[0], S[1]); g.quadraticCurveTo(P[0], P[1], M[0], M[1]); g.stroke(); g.restore();
    });
    trait(g, M[0], M[1], D1[0], D1[1], TRAIT, u, [4 * u, 5 * u]); trait(g, M[0], M[1], D2[0], D2[1], TRAIT, u, [4 * u, 5 * u]);
    g.save(); g.translate(0.38 * W, 0.5 * H); g.rotate(-0.35); g.beginPath(); g.ellipse(0, 0, 30 * u, 13 * u, 0, 0, TOUR);
    g.fillStyle = 'rgba(205,225,255,.12)'; g.fill(); g.strokeStyle = PALE; g.lineWidth = 1.3 * u; g.stroke(); g.restore();
    disque(g, S[0], S[1], 4.5 * u, ENCRE);
    [D1, D2].forEach(D => { g.save(); g.strokeStyle = ENCRE; g.lineWidth = 1.5 * u; g.strokeRect(D[0] - 6 * u, D[1] - 6 * u, 12 * u, 12 * u); g.restore(); });
    const decide = tt > 2.0;
    if (decide && lame) trait(g, M[0] - 19 * u, M[1], M[0] + 19 * u, M[1], ENCRE, 2.6 * u);
    else trait(g, M[0] - 19 * u, M[1], M[0] + 19 * u, M[1], TRAIT, 1.2 * u, [3 * u, 4 * u]);
    const but = lame ? D1 : (mulberry(7 * k + 3)() < 0.5 ? D1 : D2);
    if (tt < 3) {
      [P1, P2].forEach(P => { for (let i = 0; i < 8; i++) { const s = tt / 3 - i * 0.017; if (s > 0) { const q = sur(P, s); disque(g, q[0], q[1], (2.7 - i * 0.26) * u, PHOTON, 0.8 - i * 0.09); } } });
    } else if (tt < 3.5) {
      const s = (tt - 3) / 0.5; disque(g, M[0] + (but[0] - M[0]) * s, M[1] + (but[1] - M[1]) * s, 2.7 * u, PHOTON, 0.9);
    } else {
      const a = Math.max(0, 1 - (tt - 3.5) / 1.5);
      disque(g, but[0], but[1], (7 + 12 * (1 - a)) * u, PHOTON, 0.5 * a); disque(g, but[0], but[1], 4.2 * u, PHOTON);
    }
    if (!petit) {
      mot(g, 'SOURCE', S[0] - 8 * u, S[1] + 17 * u, u);
      mot(g, 'GALAXIE', 0.38 * W, 0.5 * H + 30 * u, u, 'center');
      mot(g, decide ? (lame ? 'LAME EN PLACE' : 'SANS LAME') : 'CHOIX À VENIR', M[0], M[1] - 16 * u, u, 'center', decide ? PHOTON : PALE);
      if (tt >= 3.5) mot(g, lame ? 'LES DEUX ROUTES INTERFÈRENT' : 'UNE ROUTE, AU HASARD', 0.5 * W, 0.95 * H, u, 'center', PHOTON);
    }
  };

  // Pilier 5. La réponse est d'abord inscrite au crayon. Puis l'environnement l'emporte en copies,
  // de plus en plus nombreuses : elle devient un fait.
  const cristal = (g, W, H, t, u, petit) => {
    const T = 7.5, tt = t % T, cx = 0.5 * W, cy = 0.5 * H, a = 26 * u, hasard = mulberry(11);
    const n = tt < 2.8 ? 0 : Math.min(420, Math.floor(Math.pow(2, (tt - 2.8) * 2.6)));
    g.save(); g.fillStyle = PHOTON;
    for (let j = 0; j < n; j++) {
      const dir = TOUR * hasard(), v = (0.14 + 0.2 * hasard()) * W, tj = 2.8 + Math.log2(j + 1) / 2.6, d = a + v * (tt - tj);
      const al = clamp(1 - d / (0.6 * W), 0, 1);
      if (al > 0) { g.globalAlpha = 0.85 * al; g.fillRect(cx + d * Math.cos(dir) - 1.6 * u, cy + d * Math.sin(dir) - 1.6 * u, 3.2 * u, 3.2 * u); }
    }
    g.restore();
    const fait = clamp((tt - 2.8) / 2.2, 0, 1);
    g.save(); g.lineWidth = 1.8 * u; g.strokeStyle = ENCRE;
    g.globalAlpha = 1 - fait; g.setLineDash([5 * u, 5 * u]); g.strokeRect(cx - a, cy - a, 2 * a, 2 * a);
    g.globalAlpha = fait; g.setLineDash([]); g.lineWidth = 2.4 * u; g.strokeRect(cx - a, cy - a, 2 * a, 2 * a); g.restore();
    if (tt < 1.4) {
      g.save(); g.font = '500 ' + (30 * u) + 'px "IBM Plex Mono", Consolas, monospace'; g.textAlign = 'center'; g.textBaseline = 'middle';
      g.fillStyle = PALE; g.fillText('?', cx, cy + 1.5 * u); g.restore();
    } else {
      g.save(); g.globalAlpha = tt < 2.8 ? 0.45 : 0.45 + 0.55 * fait; g.strokeStyle = PHOTON; g.lineWidth = 3.4 * u; g.lineJoin = 'round';
      g.beginPath(); g.moveTo(cx - 11 * u, cy + 1 * u); g.lineTo(cx - 3 * u, cy + 9 * u); g.lineTo(cx + 12 * u, cy - 9 * u); g.stroke(); g.restore();
    }
    if (!petit) {
      mot(g, tt < 1.4 ? 'QUESTION' : tt < 2.8 ? 'INSCRIPTION : ENCORE EFFAÇABLE' : 'CRISTALLISATION', cx, cy - a - 17 * u, u, 'center', tt < 2.8 ? PALE : PHOTON);
      if (tt >= 2.8) mot(g, 'COPIES DANS L’ENVIRONNEMENT : ' + frNum(n), cx, 0.94 * H, u, 'center');
    }
  };

  const DESSINS = { 1: balayage, 2: poussiere, 3: pente, 4: choix, 5: cristal };
  const fiches = toiles.map(c => ({ c: c, g: c.getContext('2d'), dessin: DESSINS[c.dataset.epure], t: 0, vu: false, W: 1, H: 1, u: 1, petit: false }))
    .filter(f => f.dessin);
  const tailler = f => {
    const r = f.c.getBoundingClientRect(), dpr = Math.min(2, window.devicePixelRatio || 1);
    f.W = Math.max(1, Math.round(r.width * dpr)); f.H = Math.max(1, Math.round(r.height * dpr));
    f.c.width = f.W; f.c.height = f.H; f.u = f.W / 400; f.petit = r.width < 330;
  };
  const peindre = f => {
    if (f.W < 8) return;
    f.g.setTransform(1, 0, 0, 1, 0, 0); f.g.clearRect(0, 0, f.W, f.H); f.g.globalAlpha = 1; f.g.lineCap = 'round';
    f.dessin(f.g, f.W, f.H, f.t, f.u, f.petit);
  };
  const fige = /^#fige=([0-9.]+)/.exec(location.hash), ARRET = reduceMotion || !!fige;
  let raf = 0, avant = 0;
  const boucle = maintenant => {
    const dt = Math.min(0.05, Math.max(0, (maintenant - avant) / 1000)); avant = maintenant;
    let encore = false;
    fiches.forEach(f => { if (f.vu) { f.t += dt; peindre(f); encore = true; } });
    raf = encore ? requestAnimationFrame(boucle) : 0;
  };
  const lancer = () => { if (!raf && !ARRET) { avant = performance.now(); raf = requestAnimationFrame(boucle); } };
  fiches.forEach(f => { f.t = fige ? parseFloat(fige[1]) || 0 : (ARRET ? parseFloat(f.c.dataset.fige) || 3 : 0); tailler(f); peindre(f); });
  if ('ResizeObserver' in window) {
    const ro = new ResizeObserver(es => es.forEach(e => { const f = fiches.find(x => x.c === e.target); if (f) { tailler(f); peindre(f); } }));
    fiches.forEach(f => ro.observe(f.c));
  }
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => { es.forEach(e => { const f = fiches.find(x => x.c === e.target); if (f) f.vu = e.isIntersecting; }); lancer(); });
    fiches.forEach(f => io.observe(f.c));
  } else { fiches.forEach(f => { f.vu = true; }); lancer(); }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => { if (ARRET) fiches.forEach(peindre); });
})();
