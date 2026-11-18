'use strict';
window.addEventListener('error', function (e) {
  var b = document.createElement('div');
  b.className = 'err';
  b.textContent = 'Erreur de script : ' + (e.message || e) + (e.lineno ? ' (ligne ' + e.lineno + ')' : '');
  document.body.appendChild(b);
});
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
// durée en secondes -> texte lisible
const duree = s => {
  if (s < 1e-12) return sig(s * 1e15) + ' fs';
  if (s < 1e-9) return sig(s * 1e12) + ' ps';
  if (s < 1e-6) return sig(s * 1e9) + ' ns';
  if (s < 1e-3) return sig(s * 1e6) + ' µs';
  if (s < 1) return sig(s * 1e3) + ' ms';
  if (s < 60) return sig(s) + ' s';
  if (s < 3600) { const m = Math.floor(s / 60); return m + ' min ' + Math.round(s - 60 * m) + ' s'; }
  if (s < 86400) { const tm = Math.round(s / 60), h = Math.floor(tm / 60); return h + ' h ' + (tm - 60 * h) + ' min'; }
  if (s < 31557600) return sig(s / 86400) + ' jours';
  if (s < 31557600e6) return sig(s / 31557600) + ' ans';
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
const typo = s => s.replace(/ ([:;?!»])/g, ' $1').replace(/« /g, '« ');
new MutationObserver(ms => ms.forEach(m => {
  const t = m.target;
  if (t.nodeType === 1 && t.classList.contains('state')) { const f = typo(t.textContent); if (f !== t.textContent) t.textContent = f; }
})).observe(document.documentElement, { childList: true, subtree: true });
// boutons à bascule exclusive
const pressOnly = (group, btn) => $$(group).forEach(b => b.setAttribute('aria-pressed', b === btn ? 'true' : 'false'));
// une figure plus large que l'écran défile : on le signale au lecteur
const marquerDefilement = () => $$('.stage').forEach(s => s.classList.toggle('defile', s.scrollWidth > s.clientWidth + 4));
window.addEventListener('load', marquerDefilement);
window.addEventListener('resize', marquerDefilement);
