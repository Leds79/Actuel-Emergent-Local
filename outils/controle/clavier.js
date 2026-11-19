// Contrôle : ordre de tabulation, liens doublons hors du parcours, dessins décrits, liste des piliers (clic, Échap, toucher ailleurs).
// S'emploie avec capture.py --js clavier.js.
const visibles = e => e.getClientRects().length > 0 && getComputedStyle(e).visibility !== 'hidden';
const tabulables = Array.from(document.querySelectorAll('a[href],button,input,select,textarea,summary,[tabindex]'))
  .filter(e => visibles(e) && e.tabIndex >= 0 && !e.disabled);
const nom = e => (e.getAttribute('aria-label') || e.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40);
const cacheParent = e => { for (let p = e; p; p = p.parentElement) if (p.getAttribute && p.getAttribute('aria-hidden') === 'true') return true; return false; };
const menu = document.querySelector('.barre .menu'), resume = menu.querySelector('summary');
const etats = [];
resume.click(); await new Promise(r => setTimeout(r, 50)); etats.push('clic : ' + menu.open);
document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true })); etats.push('Échap : ' + menu.open + ', foyer sur ' + document.activeElement.tagName);
resume.click(); await new Promise(r => setTimeout(r, 50));
document.querySelector('main').dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })); etats.push('toucher ailleurs : ' + menu.open);
resume.click(); await new Promise(r => setTimeout(r, 50));
menu.querySelector('li a').dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })); etats.push('toucher un lien de la liste : ' + menu.open);
// sortie au clavier : la liste reste ouverte tant que le foyer y circule, et se ferme quand il passe à un élément placé après elle
menu.open = true; await new Promise(r => setTimeout(r, 50));
const dernier = Array.from(menu.querySelectorAll('li a')).pop();
dernier.dispatchEvent(new FocusEvent('focusout', { bubbles: true, relatedTarget: menu.querySelector('li a') })); etats.push('foyer qui reste dans la liste : ' + menu.open);
dernier.dispatchEvent(new FocusEvent('focusout', { bubbles: true, relatedTarget: document.querySelector('.barre nav>a.dos') })); etats.push('foyer qui sort de la liste : ' + menu.open);
menu.open = false;
window.__mesures = {
  ordre: tabulables.slice(0, 16).map(e => e.tagName.toLowerCase() + ':' + nom(e)),
  nbTabulables: tabulables.length,
  voiles: Array.from(document.querySelectorAll('.voile')).map(a => a.getAttribute('tabindex') + '/' + a.getAttribute('aria-hidden') + '/' + a.getAttribute('href') + '/' + Math.round(a.getBoundingClientRect().width) + 'x' + Math.round(a.getBoundingClientRect().height)),
  voilesTabulables: tabulables.filter(e => e.classList.contains('voile')).length,
  dessins: Array.from(document.querySelectorAll('canvas[role=img]')).map(c => (cacheParent(c) ? 'MASQUÉ ' : 'décrit ') + (c.getAttribute('aria-label') || '').slice(0, 30)),
  masquesFocalisables: Array.from(document.querySelectorAll('[aria-hidden="true"]')).filter(h => (h.matches('a[href],button,input') ? [h] : []).concat(Array.from(h.querySelectorAll('a[href],button,input,[tabindex]'))).some(e => e.tabIndex >= 0)).length,
  menu: etats,
  liensSansNom: Array.from(document.querySelectorAll('a[href]')).filter(a => !cacheParent(a) && !nom(a)).length
};
