'use strict';
// en développement seulement : une erreur de script s'affiche à l'écran au lieu de passer inaperçue
if (location.protocol === 'file:' || /^(localhost|127\.0\.0\.1)$/.test(location.hostname)) {
  window.addEventListener('error', function (e) {
    var b = document.createElement('div');
    b.className = 'err';
    b.textContent = 'Erreur de script : ' + (e.message || e) + (e.lineno ? ' (ligne ' + e.lineno + ')' : '');
    document.body.appendChild(b);
  });
}
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
const NS = 'http://www.w3.org/2000/svg';
const set = (e, attrs) => { for (const k in attrs) e.setAttribute(k, attrs[k]); return e; };
const el = (tag, attrs, txt) => { const e = document.createElementNS(NS, tag); set(e, attrs || {}); if (txt != null) e.textContent = txt; return e; };
const clamp = (x, a, b) => Math.min(b, Math.max(a, x));
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const css = name => getComputedStyle(document.documentElement).getPropertyValue(name).trim();

// nombres à la française
const frNum = (x, d = 0) => x.toLocaleString('fr-FR', { minimumFractionDigits: d, maximumFractionDigits: d });
const sig = (x, n = 3) => {
  if (!isFinite(x)) return '—';
  if (x === 0) return '0';
  x = Number(x.toPrecision(n));                           // on arrondit d'abord : 99,96 s'écrit 100, pas 100,0
  const e = Math.floor(Math.log10(Math.abs(x)));
  const d = clamp(n - 1 - e, 0, 12);
  return x.toLocaleString('fr-FR', { minimumFractionDigits: d, maximumFractionDigits: d });
};
const SUP = { '-': '⁻', '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹' };
const sup = n => String(n).split('').map(ch => SUP[ch] || ch).join('');
const sci = (x, n = 2) => {
  if (x === 0) return '0';
  let e = Math.floor(Math.log10(Math.abs(x)));
  let m = x / Math.pow(10, e);
  if (Number(m.toFixed(n - 1)) >= 10) { m /= 10; e += 1; }
  return m.toLocaleString('fr-FR', { minimumFractionDigits: n - 1, maximumFractionDigits: n - 1 }) + ' × 10' + sup(e);
};
// grand nombre en toutes lettres : 236 000, 720 millions, 250 milliards
const grand = x => x < 1e6 ? frNum(Number(x.toPrecision(3)))
  : x < 1e9 ? sig(x / 1e6) + (x < 1.995e6 ? ' million' : ' millions')
    : sig(x / 1e9) + (x < 1.995e9 ? ' milliard' : ' milliards');
// durée en secondes -> texte lisible
const duree = s => {
  if (s < 1e-12) return sig(s * 1e15) + ' fs';
  if (s < 1e-9) return sig(s * 1e12) + ' ps';
  if (s < 1e-6) return sig(s * 1e9) + ' ns';
  if (s < 1e-3) return sig(s * 1e6) + ' µs';
  if (s < 1) return sig(s * 1e3) + ' ms';
  if (s < 59.95) return sig(s) + ' s';
  if (s < 3599.5) { const t = Math.round(s), m = Math.floor(t / 60); return m + ' min ' + (t - 60 * m) + ' s'; }
  if (s < 86370) { const tm = Math.round(s / 60), h = Math.floor(tm / 60); return h + ' h ' + (tm - 60 * h) + ' min'; }
  if (s < 31557600) { const j = s / 86400; return sig(j) + (j < 1.995 ? ' jour' : ' jours'); }
  if (s < 31557600e6) { const a = s / 31557600; return sig(a) + (a < 1.995 ? ' an' : ' ans'); }
  return sig(s / 31557600e6) + ' millions d’années';
};
// générateur pseudo-aléatoire reproductible
const mulberry = seed => () => {
  let t = seed += 0x6D2B79F5;
  t = Math.imul(t ^ (t >>> 15), t | 1);
  t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
};
// espaces insécables dans les textes écrits par le script
const typo = s => s.replace(/ ([:;?!»%])/g, ' $1').replace(/« /g, '« ').replace(/(\d) (?=[a-zA-Zµé])/g, '$1 ');
new MutationObserver(ms => ms.forEach(m => {
  const t = m.target;
  if (t.nodeType === 1 && t.classList.contains('state')) { const f = typo(t.textContent); if (f !== t.textContent) t.textContent = f; }
})).observe(document.documentElement, { childList: true, subtree: true });
// boutons à bascule exclusive
const pressOnly = (group, btn) => $$(group).forEach(b => b.setAttribute('aria-pressed', b === btn ? 'true' : 'false'));
// une figure plus large que l'écran défile : on le signale au lecteur, et le clavier peut y entrer
const marquerDefilement = () => $$('.stage').forEach(s => {
  const oui = s.scrollWidth > s.clientWidth + 4;
  s.classList.toggle('defile', oui);
  if (oui) s.setAttribute('tabindex', '0'); else s.removeAttribute('tabindex');
});
window.addEventListener('load', marquerDefilement);
window.addEventListener('resize', marquerDefilement);
// liste des piliers, dans la barre du haut : elle se referme quand on touche ailleurs, quand le clavier en sort, avec Échap,
// ou quand on revient sur la page
(() => {
  const menu = $('.barre .menu');
  if (!menu) return;
  document.addEventListener('pointerdown', e => { if (menu.open && !menu.contains(e.target)) menu.open = false; });
  menu.addEventListener('focusout', e => { if (e.relatedTarget && !menu.contains(e.relatedTarget)) menu.open = false; });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && menu.open) { menu.open = false; $('summary', menu).focus(); }
  });
  window.addEventListener('pageshow', () => { menu.open = false; });
})();
// rail de lecture : la section en cours est marquée pendant le défilement
(() => {
  const liens = $$('.rail a');
  if (!liens.length) return;
  const cibles = liens.map(a => document.getElementById(a.getAttribute('href').slice(1))).filter(Boolean);
  if (!cibles.length) return;
  const marquer = () => {
    let courant = cibles[0];
    cibles.forEach(c => { if (c.getBoundingClientRect().top < 130) courant = c; });
    liens.forEach(a => a.setAttribute('aria-current', a.getAttribute('href') === '#' + courant.id ? 'true' : 'false'));
  };
  let attente = 0;
  window.addEventListener('scroll', () => { if (!attente) attente = requestAnimationFrame(() => { attente = 0; marquer(); }); }, { passive: true });
  marquer();
})();
// pages longues sur petit écran : un bouton ramène au sommaire, qui se replie quand on y choisit une section
(() => {
  const bouton = $('.remonter'), plie = $('details.sommaire');
  if (!bouton) return;
  const voir = () => { bouton.hidden = window.scrollY < 1200; };
  window.addEventListener('scroll', voir, { passive: true });
  voir();
  if (!plie) return;
  bouton.addEventListener('click', () => { plie.open = true; });
  $$('a', plie).forEach(a => a.addEventListener('click', () => { plie.open = false; }));
})();
