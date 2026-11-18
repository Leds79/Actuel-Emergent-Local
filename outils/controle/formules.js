// Contrôle : nombre de formules et de formules composées par KaTeX, erreurs de KaTeX, taille des toiles des dessins.
// S'emploie avec capture.py --js formules.js --budget 15000.
await new Promise(r => setTimeout(r, 2500));
window.__mesures = {
  formules: document.querySelectorAll('.tex').length,
  composees: document.querySelectorAll('.tex.ok .katex').length,
  erreursKatex: document.querySelectorAll('.katex-error').length,
  toiles: Array.from(document.querySelectorAll('canvas')).map(c => c.width + 'x' + c.height).join(' ')
};
