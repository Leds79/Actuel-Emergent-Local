// Contrôle : ce qui déborde sur la page (page entière, tableaux, figures, formules, élément qui dépasse le bord droit).
// S'emploie avec capture.py --js debords.js, ou par mesurer_tout.py.
await new Promise(r => setTimeout(r, 1500));
const larg = document.documentElement.clientWidth;
const defile = sel => Array.from(document.querySelectorAll(sel)).filter(e => e.getClientRects().length && e.scrollWidth > e.clientWidth + 2)
  .map(e => (e.className || e.tagName) + ' ' + e.scrollWidth + '>' + e.clientWidth);
const depasse = Array.from(document.querySelectorAll('body *')).filter(e => {
  if (!e.getClientRects().length) return false;
  const r = e.getBoundingClientRect();
  if (r.width === 0 || r.right <= larg + 1) return false;
  for (let p = e.parentElement; p; p = p.parentElement) {
    const o = getComputedStyle(p).overflowX;
    if (o === 'auto' || o === 'scroll' || o === 'hidden') return false;
  }
  return true;
}).slice(0, 8).map(e => e.tagName + '.' + (e.className && e.className.baseVal !== undefined ? e.className.baseVal : e.className) + ' ' + Math.round(e.getBoundingClientRect().right));
window.__mesures = {
  page: document.documentElement.scrollWidth - larg,
  tableaux: defile('.tablewrap'), figures: defile('.stage'), formules: defile('.tex'),
  depasse: depasse,
  fiches: getComputedStyle(document.querySelector('table.empile') || document.body).display,
  // le nom du site, dans la barre du haut, s'abrège quand la place manque : cela ne doit pas arriver avec les polices du site
  marqueAbregee: (m => !!m && m.getClientRects().length > 0 && m.scrollWidth > m.clientWidth + 1)(document.querySelector('.marque span'))
};
