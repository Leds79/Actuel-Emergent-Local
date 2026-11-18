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

  // Pilier 1. L'ombre des ciseaux sur le tableau plat, vue de face. À la source, les ciseaux se ferment d'un coup.
  // Sur le tableau, l'ombre se referme comme une fermeture éclair : chaque point répond avec le retard de sa diagonale.
  // En pointillé, ce que voit celui qui tient les ciseaux : la lumière doit encore revenir, le retard est doublé.
  const ciseaux = (g, W, H, t, u, petit) => {
    const UN = 1.25, T = 7.9, tt = (t / UN) % T;                     // unité de temps : le trajet de la source au centre du tableau
    const x0 = 0.215 * W, cy = 0.4 * W, ech = 0.24 * W, RMAX = 3.12, A0 = 0.235, TC = 0.3, DEP = 0.5, OMBRE = '#04102a';
    const ouvert = tau => clamp(1 - tau / TC, 0, 1);
    const ecart = (rho, trajets) => rho * Math.tan(A0 * ouvert(tt - DEP - trajets * Math.hypot(1, rho))) * ech;
    // le tableau
    g.save(); g.fillStyle = 'rgba(205,225,255,.1)'; g.fillRect(0.03 * W, 0.1 * H, 0.94 * W, 0.8 * H);
    g.strokeStyle = TRAIT; g.lineWidth = u; g.strokeRect(0.03 * W, 0.1 * H, 0.94 * W, 0.8 * H); g.restore();
    // l'ombre des ciseaux, telle qu'elle est sur le tableau à cet instant
    // les branches et leurs anneaux : chaque branche prolonge la lame du côté opposé, elles se croisent au pivot
    const ecartBranches = 1.5 * A0 * ouvert(tt - DEP - 1);
    [-1, 1].forEach(cote => {
      const b = Math.PI + cote * (0.3 + ecartBranches), ca = Math.cos(b), sa = Math.sin(b), nx = -sa, ny = ca;
      const bx = x0 + 27 * u * ca, by = cy + 27 * u * sa, ax = x0 + 40 * u * ca, ay = cy + 40 * u * sa;
      g.beginPath(); g.moveTo(x0 + 3.6 * u * nx, cy + 3.6 * u * ny); g.lineTo(bx + 2.4 * u * nx, by + 2.4 * u * ny);
      g.lineTo(bx - 2.4 * u * nx, by - 2.4 * u * ny); g.lineTo(x0 - 3.6 * u * nx, cy - 3.6 * u * ny); g.closePath();
      g.fillStyle = OMBRE; g.fill(); g.strokeStyle = ENCRE; g.lineWidth = u; g.stroke();
      g.beginPath(); g.ellipse(ax, ay, 15 * u, 9.5 * u, b, 0, TOUR); g.ellipse(ax, ay, 9.5 * u, 5 * u, b, 0, TOUR);
      g.fillStyle = OMBRE; g.fill('evenodd');
      g.beginPath(); g.ellipse(ax, ay, 15 * u, 9.5 * u, b, 0, TOUR); g.stroke();
      g.beginPath(); g.ellipse(ax, ay, 9.5 * u, 5 * u, b, 0, TOUR); g.stroke();
    });
    // les lames : un tranchant droit, un dos courbe, une pointe
    [-1, 1].forEach(cote => {
      g.beginPath();
      for (let i = 0; i <= 62; i++) { const rho = RMAX * i / 62; g[i ? 'lineTo' : 'moveTo'](x0 + rho * ech, cy + cote * ecart(rho, 1)); }
      for (let i = 62; i >= 0; i--) {
        const q = i / 62, rho = RMAX * q, dos = 10.5 * (1 - Math.pow(q, 1.7)) * (0.72 + 0.28 * Math.sin(Math.PI * Math.min(1, 1.6 * q))) * u;
        g.lineTo(x0 + rho * ech, cy + cote * (ecart(rho, 1) + dos));
      }
      g.closePath(); g.fillStyle = OMBRE; g.fill(); g.strokeStyle = ENCRE; g.lineWidth = u; g.stroke();
    });
    // la vis du pivot
    disque(g, x0, cy, 4.2 * u, OMBRE); anneau(g, x0, cy, 4.2 * u, ENCRE, u); disque(g, x0, cy, 1.4 * u, ENCRE);
    // ce que voit celui qui tient les ciseaux : la même ombre, avec le retard du retour en plus
    [-1, 1].forEach(cote => {
      g.save(); g.strokeStyle = PALE; g.lineWidth = 1.3 * u; g.setLineDash([4 * u, 4 * u]); g.beginPath();
      for (let i = 0; i <= 62; i++) { const rho = RMAX * i / 62; g[i ? 'lineTo' : 'moveTo'](x0 + rho * ech, cy + cote * ecart(rho, 2)); }
      g.stroke(); g.restore();
    });
    // les deux points de fermeture : sur le tableau, et dans l'œil de l'opérateur
    const a1 = tt - DEP - TC, a2 = a1 / 2;
    const r1 = a1 > 1 ? Math.sqrt(a1 * a1 - 1) : -1, r2 = a2 > 1 ? Math.sqrt(a2 * a2 - 1) : -1;
    if (r1 >= 0 && r1 <= RMAX) { disque(g, x0 + r1 * ech, cy, 7 * u, PHOTON, 0.3); disque(g, x0 + r1 * ech, cy, 3 * u, PHOTON); }
    if (r2 >= 0 && r2 <= RMAX) anneau(g, x0 + r2 * ech, cy, 5 * u, PALE, 1.5 * u);
    // à la source : les ciseaux eux-mêmes, fermés presque tout de suite
    const b = 0.5 * ouvert(tt - DEP), sx = 0.105 * W, sy = 0.205 * H;
    [-1, 1].forEach(cote => {
      const hx = sx - 9 * u * Math.cos(b + 0.25), hy = sy - cote * 9 * u * Math.sin(b + 0.25);
      trait(g, hx, hy, sx + 19 * u * Math.cos(b), sy + cote * 19 * u * Math.sin(b), PHOTON, 1.8 * u);
      anneau(g, hx - 3.2 * u, hy - cote * 1.5 * u, 3.4 * u, PHOTON, 1.5 * u);
    });
    if (!petit) {
      mot(g, tt < DEP ? 'À LA SOURCE : OUVERTS' : 'À LA SOURCE : DÉJÀ FERMÉS', 0.03 * W, 0.045 * H, u, 'left', PHOTON);
      mot(g, 'TABLEAU PLAT, VU DE FACE', 0.97 * W, 0.045 * H, u, 'right');
      // légende, dans le coin laissé libre par les lames
      const lx = 0.06 * W, l1 = 0.8 * H, l2 = 0.855 * H;
      disque(g, lx + 4 * u, l1, 3 * u, PHOTON); mot(g, 'OÙ L’OMBRE SE FERME, SUR LE TABLEAU', lx + 16 * u, l1, u, 'left', PHOTON);
      anneau(g, lx + 4 * u, l2, 4 * u, PALE, 1.4 * u); mot(g, 'CE QUE VOIT CELUI QUI TIENT LES CISEAUX', lx + 16 * u, l2, u);
      mot(g, 'RETARD : LA DIAGONALE, PUIS LE RETOUR', 0.5 * W, 0.955 * H, u, 'center');
    }
  };

  // Pilier 2. Le mot et le fait. Le mot « rayon » trace une tige rigide entre la source et le mur, enfermée dans les
  // limites de sa définition. Le fait est autre : rien ne se voit en chemin, la lumière ne se montre qu'où elle rencontre la matière.
  const langage = (g, W, H, t, u, petit) => {
    const lx = 0.17 * W, mx = 0.9 * W, y1 = 0.25 * H, y2 = 0.64 * H, ex = 0.53 * W, ey = 0.92 * H, hasard = mulberry(7);
    // en haut, le mot : une tige pleine, immobile, bien délimitée
    g.save(); g.strokeStyle = PALE; g.lineWidth = 1.2 * u; g.setLineDash([4 * u, 4 * u]);
    g.strokeRect(lx - 42 * u, y1 - 27 * u, mx - lx + 56 * u, 50 * u); g.restore();
    g.save(); g.strokeStyle = ENCRE; g.lineWidth = 1.5 * u; g.strokeRect(lx - 30 * u, y1 + 2 * u, 30 * u, 16 * u); g.restore();
    trait(g, lx, y1 + 10 * u, mx, y1 + 10 * u, ENCRE, 3.4 * u);
    trait(g, mx, y1 - 6 * u, mx, y1 + 20 * u, ENCRE, 1.8 * u);
    g.save(); g.font = '600 ' + (13 * u) + 'px "IBM Plex Mono", ui-monospace, Consolas, monospace';
    if ('letterSpacing' in g) g.letterSpacing = (2 * u) + 'px';
    g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillStyle = ENCRE; g.fillText('« RAYON »', (lx + mx) / 2, y1 - 11 * u);
    const large = g.measureText('« RAYON »').width + 14 * u, cycle = t % 9, avance = clamp((cycle - 2) / 0.8, 0, 1) * (cycle > 8.2 ? (9 - cycle) / 0.8 : 1);
    g.restore();
    if (avance > 0) trait(g, (lx + mx) / 2 - large / 2, y1 - 11 * u, (lx + mx) / 2 - large / 2 + large * avance, y1 - 11 * u, PHOTON, 2.2 * u);
    // en bas, le fait : un trajet qu'on ne voit pas, et des éclats là où la lumière rencontre la matière
    g.save(); g.strokeStyle = ENCRE; g.lineWidth = 1.5 * u; g.strokeRect(lx - 30 * u, y2 - 8 * u, 30 * u, 16 * u); g.restore();
    trait(g, mx, y2 - 30 * u, mx, y2 + 30 * u, ENCRE, 1.8 * u);
    trait(g, lx, y2, mx, y2, 'rgba(205,225,255,.16)', u, [2 * u, 7 * u]);
    trait(g, mx, y2, ex, ey, 'rgba(255,239,196,.4)', u);
    disque(g, mx, y2, 8 * u, PHOTON, 0.25); disque(g, mx, y2, 3.6 * u, PHOTON);
    for (let k = 0; k < 30; k++) {
      const x0 = lx + (mx - lx) * (0.05 + 0.9 * hasard()), y0 = y2 + (hasard() - 0.5) * 0.3 * H, A = (0.04 + 0.08 * hasard()) * H;
      const Tk = 5 + 6 * hasard(), ph = TOUR * hasard();
      const y = y0 + A * Math.sin(TOUR * t / Tk + ph), x = x0 + 6 * u * Math.sin(TOUR * t / (1.7 * Tk) + ph), d = Math.abs(y - y2);
      if (d < 5 * u) {
        const f = 1 - d / (5 * u);
        trait(g, x, y, ex, ey, 'rgba(255,239,196,' + (0.55 * f).toFixed(3) + ')', u);
        disque(g, x, y, 7 * u, PHOTON, 0.25 * f); disque(g, x, y, 2.3 * u, PHOTON);
      } else disque(g, x, y, 1.3 * u, PALE, 0.55);
    }
    g.save(); g.strokeStyle = ENCRE; g.lineWidth = 1.5 * u; g.beginPath(); g.ellipse(ex, ey, 13 * u, 6.5 * u, 0, 0, TOUR); g.stroke(); g.restore();
    disque(g, ex, ey, 3.2 * u, ENCRE);
    if (!petit) {
      mot(g, 'LE MOT, PLUS ANCIEN QUE LES DÉCOUVERTES', lx - 42 * u, y1 - 38 * u, u);
      mot(g, 'CE QU’ON A DÉCOUVERT : ACTUEL, ÉMERGENT, LOCAL', lx - 42 * u, y2 - 0.21 * H, u, 'left', PHOTON);
    }
  };

  // Pilier 3. La toile de l'espace-temps tourne, tout entière, à la même cadence : ses battements et ses galaxies filent
  // partout à la vitesse c. Un trou noir y creuse un puits : la toile s'étire, et tout ce qui passe près de lui ralentit.
  const TOILE = (() => {
    const HX = 0.42, HY = 0.3, R0 = 0.2, V = 0.2, anneaux = [];
    const frein = d => Math.max(0.04, d * d / (d * d + 0.05));        // 1 au loin, presque 0 au bord du trou noir
    for (let i = 1; i <= 5; i++) {
      const R = 0.2 * i, temps = [0];
      for (let k = 1; k <= 240; k++) {
        const psi = TOUR * (k - 0.5) / 240, d = Math.hypot(R * Math.cos(psi) - HX, R * Math.sin(psi) - HY);
        temps.push(temps[k - 1] + (TOUR / 240) * R / (V * frein(d)));
      }
      anneaux.push({ R: R, temps: temps, total: temps[240], grains: Math.round(13 * R) + 1 });
    }
    return { HX: HX, HY: HY, R0: R0, V: V, anneaux: anneaux,
      galaxies: [[1, 0.05, 0.5], [2, 0.38, -0.4], [3, 0.7, 0.2], [4, 0.2, 1.1], [4, 0.62, -0.7], [3, 0.12, 0.9], [2, 0.85, 0.3]] };
  })();
  const toile = (g, W, H, t, u, petit) => {
    const S = TOILE;
    // la toile vue en perspective : le trou noir y creuse un puits, les mailles s'étirent vers le bas
    const P = (X, Y) => {
      const d2 = (X - S.HX) * (X - S.HX) + (Y - S.HY) * (Y - S.HY);
      return [(0.5 + 0.44 * X) * W, (0.32 + 0.2 * Y + 0.235 / (1 + d2 / (S.R0 * S.R0))) * W];
    };
    // angle atteint sur un anneau après une durée donnée : régulier au loin, freiné près du trou noir
    const angle = (A, duree) => {
      const tau = ((duree % A.total) + A.total) % A.total;
      let a = 0, b = 240;
      while (b - a > 1) { const m = (a + b) >> 1; if (A.temps[m] <= tau) a = m; else b = m; }
      return TOUR * (a + (tau - A.temps[a]) / (A.temps[b] - A.temps[a])) / 240;
    };
    g.save(); g.strokeStyle = TRAIT; g.lineWidth = u;
    S.anneaux.forEach(A => {
      g.beginPath();
      for (let i = 0; i <= 72; i++) { const a = TOUR * i / 72, p = P(A.R * Math.cos(a), A.R * Math.sin(a)); if (i) g.lineTo(p[0], p[1]); else g.moveTo(p[0], p[1]); }
      g.stroke();
    });
    // les rayons de la toile tournent : c'est tout l'ensemble qui est en mouvement
    for (let k = 0; k < 16; k++) {
      const a = S.V * t + TOUR * k / 16;
      g.beginPath();
      for (let i = 0; i <= 24; i++) { const r = 0.05 + 0.95 * i / 24, p = P(r * Math.cos(a), r * Math.sin(a)); if (i) g.lineTo(p[0], p[1]); else g.moveTo(p[0], p[1]); }
      g.stroke();
    }
    g.restore();
    // les battements : la même vitesse partout, sauf près du trou noir, où ils ralentissent et s'entassent
    S.anneaux.forEach(A => {
      for (let k = 0; k < A.grains; k++) {
        const psi = angle(A, t + k * A.total / A.grains), X = A.R * Math.cos(psi), Y = A.R * Math.sin(psi);
        if (Math.hypot(X - S.HX, Y - S.HY) < 0.06) continue;
        const p = P(X, Y); disque(g, p[0], p[1], 1.6 * u, PHOTON, 0.9);
      }
    });
    // les galaxies, emportées par la toile
    S.galaxies.forEach(G => {
      const A = S.anneaux[G[0]], psi = angle(A, t + G[1] * A.total), p = P(A.R * Math.cos(psi), A.R * Math.sin(psi));
      g.save(); g.translate(p[0], p[1]); g.rotate(G[2]); g.beginPath(); g.ellipse(0, 0, 11 * u, 4.2 * u, 0, 0, TOUR);
      g.fillStyle = 'rgba(205,225,255,.18)'; g.fill(); g.strokeStyle = PALE; g.lineWidth = 1.1 * u; g.stroke(); g.restore();
      disque(g, p[0], p[1], 1.9 * u, ENCRE);
    });
    const c = P(S.HX, S.HY);
    g.save(); g.beginPath(); g.ellipse(c[0], c[1] - 3 * u, 17 * u, 7 * u, 0, 0, TOUR); g.fillStyle = '#04102a'; g.fill();
    g.strokeStyle = PHOTON; g.lineWidth = 1.8 * u; g.stroke(); g.restore();
    if (!petit) {
      mot(g, 'TOUT L’ENSEMBLE TOURNE À LA CADENCE c', 0.045 * W, 0.075 * H, u);
      mot(g, 'LE TROU NOIR ÉTIRE LA TOILE ET LA RALENTIT', 0.5 * W, 0.95 * H, u, 'center', PHOTON);
    }
  };

  // Pilier 4. Le sablier de la connaissance. Ce qui peut être su tombe grain à grain, ici et maintenant.
  // Chaque grain tombé est un constat ; aucun ne remonte : le choix d'aujourd'hui ne réécrit pas le passé.
  const SABLIER = (() => {
    const h = mulberry(1978), N = 150, DX = 0.0135, DY = 0.0117, A = 0.19, NW = 0.011, YT = 0.085, YN = 0.375, YB = 0.665;
    const demi = y => NW + (A - NW) * Math.pow(Math.sin(Math.min(1, Math.abs(y - YN) / (YB - YN)) * Math.PI / 2), 0.85);
    const haut = [], bas = [], tas = {};
    for (let r = 0; haut.length < 2 * N; r++) {
      const y = YN - 0.03 - r * DY, m = demi(y) - 0.011, dec = r % 2 ? DX / 2 : 0;
      for (let x = -Math.floor((m + dec) / DX) * DX + dec; x <= m + 1e-6 && haut.length < 2 * N; x += DX) haut.push(x, y);
    }
    for (let i = 0; i < N; i++) {
      let b = Math.round((h() + h() + h() - 1.5) * 2.4);
      for (let e = 0; e < 40; e++) {
        const ici = tas[b] || 0, g = tas[b - 1] || 0, d = tas[b + 1] || 0;
        if (g <= ici - 2 && (g <= d || d > ici - 2)) b--; else if (d <= ici - 2) b++; else break;
      }
      const n = tas[b] || 0; tas[b] = n + 1;
      bas.push(b * DX + (n % 2 ? DX / 2 : 0), YB - 0.011 - n * DY);
    }
    return { N: N, A: A, YT: YT, YN: YN, YB: YB, demi: demi, haut: haut, bas: bas };
  })();
  const sablier = (g, W, H, t, u, petit) => {
    const S = SABLIER, T = 55, tt = t % T, PAS = 0.42, CHUTE = 1.2, DEJA = 36, fondu = tt > T - 0.8 ? (T - tt) / 0.8 : 1;
    g.save(); g.globalAlpha = fondu;
    g.save(); g.strokeStyle = ENCRE; g.lineWidth = 1.6 * u;
    [-1, 1].forEach(c => {
      g.beginPath();
      for (let i = 0; i <= 64; i++) { const y = S.YT + (S.YB - S.YT) * i / 64, x = (0.5 + c * S.demi(y)) * W; if (i) g.lineTo(x, y * W); else g.moveTo(x, y * W); }
      g.stroke();
    });
    g.restore();
    trait(g, (0.5 - S.A - 0.025) * W, S.YT * W, (0.5 + S.A + 0.025) * W, S.YT * W, ENCRE, 2.4 * u);
    trait(g, (0.5 - S.A - 0.025) * W, S.YB * W, (0.5 + S.A + 0.025) * W, S.YB * W, ENCRE, 2.4 * u);
    const partis = DEJA + clamp(Math.floor((tt - 0.6) / PAS) + 1, 0, S.N - DEJA);
    // en haut, ce qui n'est pas encore constaté : des grains pâles
    g.fillStyle = PALE; g.globalAlpha = 0.5 * fondu;
    for (let j = 0; j < S.N - partis; j++) { g.beginPath(); g.arc((0.5 + S.haut[2 * j]) * W, S.haut[2 * j + 1] * W, 1.7 * u, 0, TOUR); g.fill(); }
    // en bas, les constats ; et le grain qui tombe, ici et maintenant
    g.fillStyle = PHOTON;
    let poses = 0;
    for (let i = 0; i < partis; i++) {
      const p = i < DEJA ? 1 : (tt - 0.6 - (i - DEJA) * PAS) / CHUTE, x1 = S.bas[2 * i], y1 = S.bas[2 * i + 1];
      if (p >= 1) { g.globalAlpha = 0.95 * fondu; g.beginPath(); g.arc((0.5 + x1) * W, y1 * W, 1.9 * u, 0, TOUR); g.fill(); poses++; }
      else {
        const q = Math.pow(p, 1.7), x = (0.5 + x1 * q) * W, y = (S.YN + (y1 - S.YN) * q) * W;
        g.globalAlpha = 0.28 * fondu; g.beginPath(); g.arc(x, y, 6.5 * u, 0, TOUR); g.fill();
        g.globalAlpha = fondu; g.beginPath(); g.arc(x, y, 2.4 * u, 0, TOUR); g.fill();
      }
    }
    if (!petit) {
      g.globalAlpha = fondu;
      mot(g, 'POTENTIEL', (0.5 - S.A - 0.04) * W, 0.2 * W, u, 'right');
      trait(g, 0.515 * W, S.YN * W, 0.555 * W, S.YN * W, TRAIT, u);
      mot(g, 'ICI, MAINTENANT', 0.565 * W, S.YN * W, u);
      mot(g, 'CONSTATS : ' + poses, (0.5 + S.A + 0.04) * W, 0.59 * W, u, 'left', PHOTON);
      mot(g, 'AUCUN GRAIN NE REMONTE', 0.5 * W, 0.712 * W, u, 'center');
    }
    g.restore();
  };

  // Pilier 5. La réponse est d'abord un germe, tracé au crayon. Puis elle cristallise en flocon de neige :
  // six bras identiques, chaque rameau en porte de plus petits, de proche en proche, et rien ne revient en arrière.
  const GIVRE = (() => {
    const niveaux = [[], [], [], []], V = 0.105, LONG = 0.33, PAS = [9, 5, 3, 2];
    let total = 0, fin = 0;
    const branche = (x, y, ang, len, t0, prof) => {
      if (len < 0.011) return;
      const n = PAS[prof], pas = len / n, ca = Math.cos(ang), sa = Math.sin(ang);
      let t = t0;
      for (let k = 0; k < n; k++) {
        const x2 = x + pas * ca, y2 = y + pas * sa, d = pas / V;
        niveaux[prof].push(x, y, x2, y2, t, d); total++;
        x = x2; y = y2; t += d; if (t > fin) fin = t;
        if (prof < 3 && k < n - 1) {
          // sur un bras, les rameaux s'allongent puis raccourcissent : c'est ce qui dessine l'étoile à six branches
          const q = (k + 1) / n, l = prof === 0 ? Math.min(0.92 * q * len, 0.62 * (1 - q) * len) : 0.5 * len * Math.pow(1 - q, 0.8);
          branche(x, y, ang + 1.0472, l, t, prof + 1); branche(x, y, ang - 1.0472, l, t, prof + 1);
        }
      }
    };
    for (let i = 0; i < 6; i++) branche(0.5, 0.375, i * 1.0472, LONG, 0, 0);
    return { niveaux: niveaux, total: total, fin: fin };
  })();
  const cristal = (g, W, H, t, u, petit) => {
    const T = GIVRE.fin + 7, tt = t % T, cx = 0.5 * W, cy = 0.375 * W, tg = tt - 2.6;
    const fondu = tt > T - 0.8 ? (T - tt) / 0.8 : 1;
    const hexagone = r => { g.beginPath(); for (let i = 0; i < 6; i++) { const a = i * 1.0472 + 0.5236; g[i ? 'lineTo' : 'moveTo'](cx + r * Math.cos(a), cy + r * Math.sin(a)); } g.closePath(); };
    let n = 0;
    g.save(); g.globalAlpha = fondu;
    if (tg > 0) {
      const EP = [2.3, 1.6, 1.15, 0.85], AL = [1, 0.94, 0.84, 0.72], pointes = [];
      for (let p = 0; p < GIVRE.niveaux.length; p++) {
        const s = GIVRE.niveaux[p];
        g.beginPath();
        for (let i = 0; i < s.length; i += 6) {
          if (tg <= s[i + 4]) continue;
          const f = Math.min(1, (tg - s[i + 4]) / s[i + 5]), x = s[i] + (s[i + 2] - s[i]) * f, y = s[i + 1] + (s[i + 3] - s[i + 1]) * f;
          g.moveTo(s[i] * W, s[i + 1] * W); g.lineTo(x * W, y * W);
          if (f >= 1) n++; else if (pointes.length < 320) pointes.push(x * W, y * W);
        }
        g.strokeStyle = ENCRE; g.lineWidth = EP[p] * u; g.globalAlpha = AL[p] * fondu; g.stroke();
      }
      // les pointes qui poussent : c'est là, et à cet instant, que la réponse se recopie
      g.fillStyle = PHOTON; g.globalAlpha = 0.9 * fondu;
      for (let i = 0; i < pointes.length; i += 2) { g.beginPath(); g.arc(pointes[i], pointes[i + 1], 1.5 * u, 0, TOUR); g.fill(); }
    }
    g.restore();
    // le germe : un point d'interrogation, puis une réponse au crayon, puis le cœur du cristal
    g.save(); g.globalAlpha = fondu;
    if (tt < 1.2) {
      g.font = '500 ' + (26 * u) + 'px "IBM Plex Mono", Consolas, monospace'; g.textAlign = 'center'; g.textBaseline = 'middle';
      g.fillStyle = PALE; g.fillText('?', cx, cy + 1.5 * u);
    } else if (tg <= 0) {
      g.strokeStyle = PHOTON; g.lineWidth = 1.5 * u; g.setLineDash([3 * u, 3 * u]); g.globalAlpha = 0.75 * fondu; hexagone(9 * u); g.stroke();
    } else {
      g.fillStyle = PHOTON; hexagone(5.5 * u); g.fill();
    }
    g.restore();
    if (!petit) {
      const etiquette = (texte, y, couleur) => {
        g.save(); g.font = '500 ' + (10 * u) + 'px "IBM Plex Mono", ui-monospace, Consolas, monospace';
        if ('letterSpacing' in g) g.letterSpacing = (1.1 * u) + 'px';
        const l = g.measureText(texte).width + 16 * u;
        g.globalAlpha = 0.86 * fondu; g.fillStyle = '#0a2046'; g.fillRect(0.5 * W - l / 2, y - 10 * u, l, 20 * u); g.restore();
        g.save(); g.globalAlpha = fondu; mot(g, texte, 0.5 * W, y, u, 'center', couleur); g.restore();
      };
      etiquette(tt < 1.2 ? 'QUESTION' : tg <= 0 ? 'INSCRIPTION : ENCORE EFFAÇABLE' : 'CRISTALLISATION', 0.075 * H, tg > 0 ? PHOTON : PALE);
      if (tg > 0) etiquette('COPIES DANS L’ENVIRONNEMENT : ' + frNum(n), 0.93 * H, PALE);
    }
  };

  const DESSINS = { 1: ciseaux, 2: langage, 3: toile, 4: sablier, 5: cristal };
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
