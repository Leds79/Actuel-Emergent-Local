# -*- coding: utf-8 -*-
"""Figures statiques (SVG) des articles et des démonstrations, et marque du site.

Chaque figure remplace, dans les exports Markdown, la ligne « embedded content : <légende> ».
Chacune existe en deux mises en page : large pour l'ordinateur, étroite pour le téléphone (suffixe _M).
La feuille de style n'en affiche qu'une à la fois (classes « bureau » et « mobile »).
Les classes de dessin (ln, lnk, ray, geo, tb, tq, tm, f-ray…) sont définies dans gabarits/base.css.
"""

_RAY3 = (
    '<line x1="{ox}" y1="340" x2="{ax}" y2="{ay}" class="ln" style="stroke:var(--ink-2)"/>'
    '<line x1="{ax}" y1="{ay}" x2="{ex}" y2="100" class="ray"/><circle cx="{ex}" cy="100" r="4.5" class="f-ray"/>'
)
# version étroite : source en (46, 300), écran à y = 70, écran courbe de rayon 230
_RAY3_M = (
    '<line x1="46" y1="300" x2="{ax}" y2="{ay}" class="ln" style="stroke:var(--ink-2)"/>'
    '<line x1="{ax}" y1="{ay}" x2="{ex}" y2="70" class="ray"/><circle cx="{ex}" cy="70" r="4.5" class="f-ray"/>'
)
_RAYONS_M = (_RAY3_M.format(ax=107.7, ay=78.4, ex=110) + _RAY3_M.format(ax=174.0, ay=108.9, ex=200)
             + _RAY3_M.format(ax=221.1, ay=150.9, ex=316))

GEO_DOSSIER = (
    '<svg viewBox="0 0 760 404" role="img" aria-label="Sur un tableau plat, la diagonale s\'allonge quand on s\'éloigne du centre">'
    '<defs><marker id="fg-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
    '<path d="M0 0L10 5L0 10z" class="f-axis"/></marker></defs>'
    '<line x1="40" y1="100" x2="736" y2="100" class="lnk"/>'
    '<text x="736" y="84" text-anchor="end" class="tb">tableau plat</text>'
    '<path d="M140 100A240 240 0 0 1 380 340" class="ln dash"/>'
    '<text x="392" y="318" class="tq">écran sphérique : R = D partout</text>'
    '<line x1="140" y1="340" x2="140" y2="100" class="ln"/>'
    '<text x="128" y="226" text-anchor="end" class="tb">D</text>'
    '<text x="132" y="118" text-anchor="end" class="tq">centre du tableau</text>'
    + _RAY3.format(ox=140, ax=284, ay=148, ex=320)
    + _RAY3.format(ox=140, ax=342.9, ay=211.8, ex=520)
    + _RAY3.format(ox=140, ax=360.6, ay=245.5, ex=700)
    + '<text x="234" y="196" text-anchor="end" class="tb">diagonale R</text>'
    '<text x="538" y="150" text-anchor="middle" class="tb">R − D</text>'
    '<line x1="140" y1="78" x2="320" y2="78" class="ln" marker-start="url(#fg-ar)" marker-end="url(#fg-ar)"/>'
    '<text x="230" y="70" text-anchor="middle" class="tb">x</text>'
    '<path d="M140 290A50 50 0 0 1 170 300" class="ln"/><text x="161" y="283" text-anchor="middle" class="t">θ</text>'
    '<circle cx="140" cy="340" r="5" class="f-ink"/>'
    '<text x="24" y="366" class="tb">O : source et observateur</text>'
    '<text x="24" y="384" class="tq">La lumière part de O et y revient : trajet total 2R</text>'
    '</svg>'
)
GEO_DOSSIER_M = (
    '<svg viewBox="0 0 350 384" role="img" aria-label="Sur un tableau plat, la diagonale s\'allonge quand on s\'éloigne du centre">'
    '<defs><marker id="fg-arm" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
    '<path d="M0 0L10 5L0 10z" class="f-axis"/></marker></defs>'
    '<line x1="16" y1="70" x2="340" y2="70" class="lnk"/>'
    '<text x="340" y="56" text-anchor="end" class="tb">tableau plat</text>'
    '<path d="M46 70A230 230 0 0 1 276 300" class="ln dash"/>'
    '<line x1="46" y1="300" x2="46" y2="70" class="ln"/>'
    '<text x="36" y="192" text-anchor="end" class="tb">D</text>'
    + _RAYONS_M
    + '<text x="120" y="262" class="tb">diagonale R</text>'
    '<text x="282" y="126" class="tb">R − D</text>'
    '<line x1="46" y1="48" x2="110" y2="48" class="ln" marker-start="url(#fg-arm)" marker-end="url(#fg-arm)"/>'
    '<text x="78" y="40" text-anchor="middle" class="tb">x</text>'
    '<path d="M46 252A48 48 0 0 1 58.4 253.6" class="ln"/><text x="58" y="240" text-anchor="middle" class="t">θ</text>'
    '<circle cx="46" cy="300" r="5" class="f-ink"/>'
    '<text x="340" y="320" text-anchor="end" class="tq">écran sphérique : R = D partout</text>'
    '<text x="16" y="344" class="tb">O : source et observateur</text>'
    '<text x="16" y="362" class="tq">La lumière part de O et y revient :</text>'
    '<text x="16" y="378" class="tq">trajet total 2R</text>'
    '</svg>'
)

GEO_ARTICLE = (
    '<svg viewBox="0 0 760 404" role="img" aria-label="Sur un écran plat, la diagonale s\'allonge quand on s\'éloigne du centre">'
    '<line x1="40" y1="100" x2="736" y2="100" class="lnk"/>'
    '<text x="736" y="84" text-anchor="end" class="tb">écran plat</text>'
    '<path d="M180 100A240 240 0 0 1 420 340" class="ln dash"/>'
    '<text x="432" y="318" class="tq">écran courbe : même distance partout</text>'
    '<line x1="180" y1="340" x2="180" y2="100" class="ln"/>'
    '<text x="168" y="226" text-anchor="end" class="tb">100 millions de km</text>'
    '<text x="172" y="118" text-anchor="end" class="tq">centre de l\'écran</text>'
    + _RAY3.format(ox=180, ax=313.1, ay=140.3, ex=340)
    + _RAY3.format(ox=180, ax=376.1, ay=201.6, ex=520)
    + _RAY3.format(ox=180, ax=396.4, ay=236.1, ex=680)
    + '<text x="262" y="196" text-anchor="end" class="tb">diagonale</text>'
    '<circle cx="180" cy="340" r="5" class="f-ink"/>'
    '<text x="24" y="366" class="tb">Source et opérateur</text>'
    '<text x="24" y="384" class="tq">La lumière part d\'ici et y revient : le trajet est doublé</text>'
    '</svg>'
)
GEO_ARTICLE_M = (
    '<svg viewBox="0 0 350 384" role="img" aria-label="Sur un écran plat, la diagonale s\'allonge quand on s\'éloigne du centre">'
    '<line x1="16" y1="70" x2="340" y2="70" class="lnk"/>'
    '<text x="340" y="56" text-anchor="end" class="tb">écran plat</text>'
    '<text x="16" y="56" class="tq">centre</text>'
    '<path d="M46 70A230 230 0 0 1 276 300" class="ln dash"/>'
    '<line x1="46" y1="300" x2="46" y2="70" class="ln"/>'
    '<text x="36" y="188" text-anchor="middle" class="tb" transform="rotate(-90 36 188)">100 millions de km</text>'
    + _RAYONS_M
    + '<text x="120" y="262" class="tb">diagonale</text>'
    '<circle cx="46" cy="300" r="5" class="f-ink"/>'
    '<text x="340" y="320" text-anchor="end" class="tq">écran courbe : même distance partout</text>'
    '<text x="16" y="344" class="tb">Source et opérateur</text>'
    '<text x="16" y="362" class="tq">La lumière part d\'ici et y revient :</text>'
    '<text x="16" y="378" class="tq">le trajet est doublé</text>'
    '</svg>'
)

EVENTAIL = (
    '<svg viewBox="0 0 760 330" role="img" aria-label="Chaque impact vient de la source, aucun ne vient de son voisin">'
    '<defs><marker id="fe-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
    '<path d="M0 0L10 5L0 10z" class="f-ink3"/></marker>'
    '<marker id="fe-b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
    '<path d="M0 0L10 5L0 10z" style="fill:var(--critical)"/></marker></defs>'
    '<line x1="380" y1="14" x2="380" y2="316" class="gr"/>'
    '<text x="194" y="34" text-anchor="middle" class="tb">Ce qui se passe</text>'
    '<line x1="44" y1="84" x2="344" y2="84" class="lnk"/><text x="344" y="70" text-anchor="end" class="tq">écran</text>'
    '<g class="ln" style="stroke:var(--ink-3)">'
    '<path d="M190.3 246.9L107.3 90.2" marker-end="url(#fe-a)"/><path d="M194 246V91" marker-end="url(#fe-a)"/>'
    '<path d="M197.7 246.9L280.7 90.2" marker-end="url(#fe-a)"/></g>'
    '<circle cx="104" cy="84" r="5" class="f-ray"/><circle cx="194" cy="84" r="5" class="f-ray"/><circle cx="284" cy="84" r="5" class="f-ray"/>'
    '<text x="104" y="70" text-anchor="middle" class="tb">A</text><text x="194" y="70" text-anchor="middle" class="tb">B</text>'
    '<text x="284" y="70" text-anchor="middle" class="tb">C</text>'
    '<circle cx="194" cy="254" r="5" class="f-ink"/><text x="194" y="276" text-anchor="middle" class="tq">source</text>'
    '<text x="194" y="302" text-anchor="middle" class="tq">trois envois séparés depuis la source</text>'
    '<text x="566" y="34" text-anchor="middle" class="tb">Ce qu\'on croit voir</text>'
    '<line x1="416" y1="84" x2="716" y2="84" class="lnk"/><text x="716" y="70" text-anchor="end" class="tq">écran</text>'
    '<g style="fill:none;stroke:var(--critical);stroke-width:1.5;stroke-dasharray:5 4">'
    '<path d="M478 96Q521 136 560 98" marker-end="url(#fe-b)"/><path d="M568 96Q611 136 650 98" marker-end="url(#fe-b)"/></g>'
    '<circle cx="476" cy="84" r="5" class="f-ray"/><circle cx="566" cy="84" r="5" class="f-ray"/><circle cx="656" cy="84" r="5" class="f-ray"/>'
    '<text x="476" y="70" text-anchor="middle" class="tb">A</text><text x="566" y="70" text-anchor="middle" class="tb">B</text>'
    '<text x="656" y="70" text-anchor="middle" class="tb">C</text>'
    '<text x="566" y="168" text-anchor="middle" class="tq">une tache qui glisserait de A vers B puis C</text>'
    '<text x="566" y="188" text-anchor="middle" class="tb">ce lien n\'existe pas</text>'
    '</svg>'
)
# version étroite : les deux schémas l'un sous l'autre
EVENTAIL_M = (
    '<svg viewBox="0 0 350 470" role="img" aria-label="Chaque impact vient de la source, aucun ne vient de son voisin">'
    '<defs><marker id="fe-am" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
    '<path d="M0 0L10 5L0 10z" class="f-ink3"/></marker>'
    '<marker id="fe-bm" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
    '<path d="M0 0L10 5L0 10z" style="fill:var(--critical)"/></marker></defs>'
    '<text x="16" y="24" class="tb">1. Ce qui se passe</text>'
    '<line x1="24" y1="78" x2="326" y2="78" class="lnk"/><text x="326" y="64" text-anchor="end" class="tq">écran</text>'
    '<g class="ln" style="stroke:var(--ink-3)">'
    '<path d="M171.3 222.9L87.4 84.2" marker-end="url(#fe-am)"/><path d="M175 222V85" marker-end="url(#fe-am)"/>'
    '<path d="M178.7 222.9L262.6 84.2" marker-end="url(#fe-am)"/></g>'
    '<circle cx="84" cy="78" r="5" class="f-ray"/><circle cx="175" cy="78" r="5" class="f-ray"/><circle cx="266" cy="78" r="5" class="f-ray"/>'
    '<text x="84" y="64" text-anchor="middle" class="tb">A</text><text x="175" y="64" text-anchor="middle" class="tb">B</text>'
    '<text x="266" y="64" text-anchor="middle" class="tb">C</text>'
    '<circle cx="175" cy="230" r="5" class="f-ink"/><text x="175" y="252" text-anchor="middle" class="tq">source</text>'
    '<text x="175" y="276" text-anchor="middle" class="tq">trois envois séparés depuis la source</text>'
    '<line x1="16" y1="298" x2="334" y2="298" class="gr"/>'
    '<text x="16" y="328" class="tb">2. Ce qu\'on croit voir</text>'
    '<line x1="24" y1="382" x2="326" y2="382" class="lnk"/><text x="326" y="368" text-anchor="end" class="tq">écran</text>'
    '<g style="fill:none;stroke:var(--critical);stroke-width:1.5;stroke-dasharray:5 4">'
    '<path d="M86 394Q129 432 169 396" marker-end="url(#fe-bm)"/><path d="M177 394Q220 432 260 396" marker-end="url(#fe-bm)"/></g>'
    '<circle cx="84" cy="382" r="5" class="f-ray"/><circle cx="175" cy="382" r="5" class="f-ray"/><circle cx="266" cy="382" r="5" class="f-ray"/>'
    '<text x="84" y="368" text-anchor="middle" class="tb">A</text><text x="175" y="368" text-anchor="middle" class="tb">B</text>'
    '<text x="266" y="368" text-anchor="middle" class="tb">C</text>'
    '<text x="175" y="444" text-anchor="middle" class="tq">une tache qui glisserait de A vers B puis C</text>'
    '<text x="175" y="462" text-anchor="middle" class="tb">ce lien n\'existe pas</text>'
    '</svg>'
)

PENTE = (
    '<svg viewBox="0 0 760 300" role="img" aria-label="Le côté lent avance moins : la trajectoire vire vers la masse">'
    '<defs><marker id="fp-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
    '<path d="M0 0L10 5L0 10z" class="f-ray"/></marker></defs>'
    '<line x1="44" y1="48" x2="44" y2="222" class="ln"/>'
    '<text x="24" y="38" class="tq">temps plus rapide</text><text x="24" y="240" class="tq">temps plus lent</text>'
    '<rect x="24" y="254" width="712" height="28" class="box" style="fill:var(--grid)"/>'
    '<text x="380" y="273" text-anchor="middle" class="tb">masse : planète ou étoile</text>'
    '<path d="M200 66Q470 66 680 186" class="ray" marker-end="url(#fp-a)"/>'
    '<text x="700" y="210" text-anchor="end" class="tq">trajectoire</text>'
    '<g class="lnk" style="stroke:var(--ink-2)"><line x1="200" y1="31" x2="200" y2="101"/>'
    '<line x1="387.5" y1="46.2" x2="375.8" y2="115.2"/><line x1="560.7" y1="92" x2="536.5" y2="157.6"/></g>'
    '<text x="200" y="20" text-anchor="middle" class="tq">front d\'onde</text>'
    '<text x="574" y="86" class="tq">le haut avance plus vite</text>'
    '<text x="524" y="178" text-anchor="end" class="tq">le bas avance moins vite</text>'
    '</svg>'
)
PENTE_M = (
    '<svg viewBox="0 0 350 292" role="img" aria-label="Le côté lent avance moins : la trajectoire vire vers la masse">'
    '<defs><marker id="fp-am" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
    '<path d="M0 0L10 5L0 10z" class="f-ray"/></marker></defs>'
    '<line x1="22" y1="34" x2="22" y2="214" class="ln"/>'
    '<text x="14" y="22" class="tq">temps plus rapide</text><text x="14" y="232" class="tq">temps plus lent</text>'
    '<rect x="14" y="246" width="322" height="28" class="box" style="fill:var(--grid)"/>'
    '<text x="175" y="265" text-anchor="middle" class="tb">masse : planète ou étoile</text>'
    '<path d="M92 76Q220 76 322 182" class="ray" marker-end="url(#fp-am)"/>'
    '<g class="lnk" style="stroke:var(--ink-2)"><line x1="92" y1="42" x2="92" y2="110"/>'
    '<line x1="228.7" y1="72.5" x2="199.3" y2="133.7"/><line x1="314.6" y1="126.2" x2="269.7" y2="177.3"/></g>'
    '<text x="100" y="56" class="tq">front d\'onde</text>'
    '<text x="340" y="52" text-anchor="end" class="tq">le haut avance plus vite</text>'
    '<text x="258" y="206" text-anchor="end" class="tq">le bas avance moins vite</text>'
    '<text x="340" y="222" text-anchor="end" class="tq">trajectoire</text>'
    '</svg>'
)

COMPROMIS = (
    '<svg class="fit adapte" viewBox="150 40 460 310" role="img" aria-label="Plus on peut connaître la route, moins les franges sont nettes" style="max-width:560px;margin:0 auto">'
    '<defs><marker id="fc-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
    '<path d="M0 0L10 5L0 10z" class="f-axis"/></marker></defs>'
    '<path d="M250 300H494" class="ln" marker-end="url(#fc-a)"/><path d="M250 300V56" class="ln" marker-end="url(#fc-a)"/>'
    '<path d="M250 80A220 220 0 0 1 470 300" class="geo"/>'
    '<circle cx="250" cy="80" r="5.5" class="f-ray ring"/><circle cx="405.6" cy="144.4" r="5.5" class="f-ray ring"/>'
    '<circle cx="470" cy="300" r="5.5" class="f-ray ring"/>'
    '<text x="264" y="72" class="tb">tout onde</text><text x="420" y="138" class="tb">un peu des deux</text>'
    '<text x="486" y="286" class="tb">tout particule</text>'
    '<text x="238" y="180" text-anchor="end" class="tq">contraste</text><text x="238" y="196" text-anchor="end" class="tq">des franges</text>'
    '<text x="238" y="84" text-anchor="end" class="tm">maximal</text><text x="238" y="296" text-anchor="end" class="tm">nul</text>'
    '<text x="262" y="318" class="tm">aucune</text><text x="470" y="318" text-anchor="middle" class="tm">totale</text>'
    '<text x="360" y="340" text-anchor="middle" class="tq">information disponible sur la route</text>'
    '</svg>'
)


def _trois_temps(q, i, c, f1, f2):
    return (
        '<svg viewBox="0 0 728 210" role="img" aria-label="Tant qu\'elle n\'est pas cristallisée, la réponse reste effaçable">'
        '<defs><marker id="ft-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        '<path d="M0 0L10 5L0 10z" class="f-ink3"/></marker></defs>'
        '<g class="ln" style="stroke:var(--ink-3)"><path d="M224 82H262" marker-end="url(#ft-a)"/><path d="M464 82H502" marker-end="url(#ft-a)"/>'
        '<path d="M364 118V156H124V120" marker-end="url(#ft-a)"/></g>'
        '<rect x="24" y="46" width="200" height="72" class="box"/><text x="124" y="70" text-anchor="middle" class="tb">Question</text>'
        '<text x="124" y="88" text-anchor="middle" class="tq">%s</text><text x="124" y="104" text-anchor="middle" class="tq">%s</text>'
        '<rect x="264" y="46" width="200" height="72" class="box"/><text x="364" y="70" text-anchor="middle" class="tb">Inscription</text>'
        '<text x="364" y="88" text-anchor="middle" class="tq">%s</text><text x="364" y="104" text-anchor="middle" class="tq">%s</text>'
        '<rect x="504" y="46" width="200" height="72" class="box on"/><text x="604" y="70" text-anchor="middle" class="tb">Cristallisation</text>'
        '<text x="604" y="88" text-anchor="middle" class="tq">%s</text><text x="604" y="104" text-anchor="middle" class="tq">%s</text>'
        '<text x="244" y="36" text-anchor="middle" class="tm">%s</text><text x="484" y="36" text-anchor="middle" class="tm">%s</text>'
        '<text x="244" y="176" text-anchor="middle" class="tq">gomme quantique : la réponse s\'efface</text>'
        '<text x="604" y="146" text-anchor="middle" class="tq">retour impossible en pratique</text>'
        '</svg>'
    ) % (q[0], q[1], i[0], i[1], c[0], c[1], f1, f2)


def _trois_temps_m(q, i, c, f1, f2):
    """Version étroite : les trois temps se lisent de haut en bas, la flèche de retour remonte sur le côté."""
    return (
        '<svg viewBox="0 0 350 372" role="img" aria-label="Tant qu\'elle n\'est pas cristallisée, la réponse reste effaçable">'
        '<defs><marker id="ft-am" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        '<path d="M0 0L10 5L0 10z" class="f-ink3"/></marker></defs>'
        '<g class="ln" style="stroke:var(--ink-3)"><path d="M131 84V128" marker-end="url(#ft-am)"/><path d="M131 202V246" marker-end="url(#ft-am)"/>'
        '<path d="M246 166H300V48H250" marker-end="url(#ft-am)"/></g>'
        '<rect x="16" y="14" width="230" height="70" class="box"/><text x="131" y="38" text-anchor="middle" class="tb">Question</text>'
        '<text x="131" y="56" text-anchor="middle" class="tq">%s</text><text x="131" y="72" text-anchor="middle" class="tq">%s</text>'
        '<rect x="16" y="132" width="230" height="70" class="box"/><text x="131" y="156" text-anchor="middle" class="tb">Inscription</text>'
        '<text x="131" y="174" text-anchor="middle" class="tq">%s</text><text x="131" y="190" text-anchor="middle" class="tq">%s</text>'
        '<rect x="16" y="250" width="230" height="70" class="box on"/><text x="131" y="274" text-anchor="middle" class="tb">Cristallisation</text>'
        '<text x="131" y="292" text-anchor="middle" class="tq">%s</text><text x="131" y="308" text-anchor="middle" class="tq">%s</text>'
        '<text x="140" y="111" class="tm">%s</text><text x="140" y="229" class="tm">%s</text>'
        '<text x="318" y="107" text-anchor="middle" class="tq" transform="rotate(-90 318 107)">gomme quantique</text>'
        '<text x="131" y="346" text-anchor="middle" class="tq">retour impossible en pratique</text>'
        '</svg>'
    ) % (q[0], q[1], i[0], i[1], c[0], c[1], f1, f2)


_ARTICLE5 = (("des réponses possibles", "valeur : 1 bit au plus"), ("au crayon", "encore effaçable"),
             ("gravée en copies multiples", "définitive en pratique"), "détecteur", "environnement")
_DOSSIER5 = (("potentiel de réponses", "valeur : H bits"), ("corrélation quantique", "2 bits, réversible"),
             ("1 bit classique, recopié", "figé par l'environnement"), "interaction locale", "décohérence")
TROIS_TEMPS_ARTICLE, TROIS_TEMPS_ARTICLE_M = _trois_temps(*_ARTICLE5), _trois_temps_m(*_ARTICLE5)
TROIS_TEMPS_DOSSIER, TROIS_TEMPS_DOSSIER_M = _trois_temps(*_DOSSIER5), _trois_temps_m(*_DOSSIER5)

# (début de la légende exportée, vue ou None, titre affiché, dessin large, dessin étroit ou None)
FIGURES = [
    ("géométrie du tableau plat", None, "Sur un tableau plat, la diagonale s'allonge quand on s'éloigne du centre", GEO_DOSSIER, GEO_DOSSIER_M),
    ("géométrie de l'écran plat", None, "Sur un écran plat, la diagonale s'allonge quand on s'éloigne du centre", GEO_ARTICLE, GEO_ARTICLE_M),
    ("éventail depuis la source", None, "Chaque impact vient de la source, aucun ne vient de son voisin", EVENTAIL, EVENTAIL_M),
    ("trajectoire courbée par la pente du temps", None, "Le côté lent avance moins : la trajectoire vire vers la masse", PENTE, PENTE_M),
    ("compromis entre information de route", None, "Plus on peut connaître la route, moins les franges sont nettes", COMPROMIS, None),
    ("trois temps de la mesure", "article", "Tant qu'elle n'est pas cristallisée, la réponse reste effaçable",
     TROIS_TEMPS_ARTICLE, TROIS_TEMPS_ARTICLE_M),
    ("trois temps de la mesure", "demonstration", "Tant qu'elle n'est pas cristallisée, la réponse reste effaçable",
     TROIS_TEMPS_DOSSIER, TROIS_TEMPS_DOSSIER_M),
]

# marque du site : une source, trois rayons, un écran plat (le point de départ du modèle)
ICONE = ('<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M2.5 5h19" fill="none" stroke="currentColor" stroke-width="2"/>'
         '<path d="M12 20L5 5M12 20V5M12 20L19 5" fill="none" stroke="#ffefc4" stroke-width="1.5" stroke-linecap="round"/>'
         '<circle cx="12" cy="20" r="2.2" fill="currentColor"/></svg>')
FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" fill="#0f2c56"/>'
           '<path d="M5 8.5h22" fill="none" stroke="#f3f6fb" stroke-width="2.6"/>'
           '<path d="M16 25L7.5 8.5M16 25V8.5M16 25L24.5 8.5" fill="none" stroke="#ffefc4" stroke-width="2" stroke-linecap="round"/>'
           '<circle cx="16" cy="25" r="2.8" fill="#f3f6fb"/></svg>\n')
