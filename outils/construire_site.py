# -*- coding: utf-8 -*-
"""Construit le site statique du modèle « Actuel, Émergent, Local ».

Sources : documents/*.md (exports des documents) et outils/gabarits/ (styles, scripts, planches interactives).
Sorties : index.html, dossier.html, 404.html, favicon.svg et pilier-N/{index,article,demonstration}.html,
          à la racine du dépôt.
Usage   : python outils/construire_site.py          reconstruit les pages
          python outils/construire_site.py --pdf    refait aussi dossier-complet.pdf et apercu.png
                                                     (demande Edge ou Chrome, et une connexion Internet)
Nécessite le module Python « markdown » : pip install markdown
"""
import html
import io
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse

import markdown

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figures import FAVICON, FIGURES, ICONE  # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAB = os.path.join(RACINE, "outils", "gabarits")
DOCS = os.path.join(RACINE, "documents")
NOM = "Actuel, Émergent, Local"
AUTEUR = "Sylvain Leduc"
DOSSIER = "Formalisation du modèle « Actuel, Émergent, Local »"
LIEN_DOSSIER_PRIVE = "https://claude.ai/artifact/4ZtY3d2RwEVQGYMST5XD2r"
PDF_DOSSIER = "dossier-complet.pdf"
IMAGE_PARTAGE = "apercu.png"
SITE = "https://leds79.github.io/Actuel-Emergent-Local/"
DEPOT = "https://github.com/Leds79/Actuel-Emergent-Local"
ACCROCHE = ("Cinq intuitions sur la lumière, la gravité et la mesure, nées du suivi de projet : flux, délais, goulots "
            "d'étranglement. Chacune est traduite en équations, confrontée à la physique établie, puis corrigée là où il le faut.")
POLICES = ("https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600&family=IBM+Plex+Mono:wght@400;500"
           "&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Serif:ital,wght@1,400;1,500&display=swap")

# clef : un chiffre tiré des documents, affiché sous la vignette de la page d'accueil
PILIERS = [
    dict(n=1, titre="L'ombre plus rapide que la lumière", objet="Géométrie de l'observateur", echelle="Variable : le dessin se resserre",
         article="L'ombre plus rapide que la lumière, vue par celui qui tient les ciseaux",
         resume="Sur un écran plat à 100 millions de kilomètres, l'ombre de ciseaux fermés en une seconde part de 524 fois la vitesse "
                "de la lumière, notée c, puis retombe vers c. Celui qui tient les ciseaux la voit tendre vers c/2.",
         clef=("524 c", "vitesse de l'ombre au centre de l'écran, dans l'exemple chiffré")),
    dict(n=2, titre="On ne voit jamais la lumière passer", objet="Lumière actuelle, émergente, locale", echelle="Schémas de principe",
         article="On ne voit jamais la lumière passer",
         resume="Un faisceau qui traverse le vide est invisible de côté. La lumière ne se manifeste qu'à l'endroit "
                "et à l'instant où elle rencontre de la matière.",
         clef=("1 clic", "par photon : deux détecteurs se déclenchent ensemble bien plus rarement que ne le permettrait une onde (1986)")),
    dict(n=3, titre="La pente du temps", objet="Cadence c et masse comme frein", echelle="Schémas de principe",
         article="Tomber, c'est suivre la pente du temps",
         resume="La relativité donne un sens précis à cette intuition : tout avance dans l'espace-temps à la cadence de la "
                "lumière, et une masse ralentit les horloges autour d'elle. Tomber, c'est virer vers cette zone ralentie.",
         meta="Tout avance dans l'espace-temps à la cadence de la lumière, et une masse ralentit les horloges autour d'elle. "
              "Tomber, c'est virer vers cette zone ralentie.",
         clef=("9,81 m/s<sup>2</sup>", "la pesanteur, retrouvée en multipliant la pente du temps par c²")),
    dict(n=4, titre="Le choix d'aujourd'hui ne réécrit pas le passé", objet="Choix retardé de Wheeler", echelle="Schémas de principe",
         article="Le choix d'aujourd'hui ne réécrit pas le passé",
         resume="Choisir aujourd'hui comment mesurer un photon ne change rien au passé. Entre « une route » "
                "et « deux routes », tous les intermédiaires existent.",
         clef=("3 500 km", "au plus, parcourus par les photons quand l'expérience a été refaite avec un satellite, en 2017")),
    dict(n=5, titre="Comment une réponse devient un fait", objet="Cristallisation de l'information", echelle="Schémas de principe",
         article="Comment une réponse devient un fait",
         resume="La réponse est d'abord inscrite au crayon, encore effaçable. L'environnement la recopie ensuite "
                "des milliards de fois et la grave.",
         clef=("10 ps", "dix picosecondes : le temps que met le soleil à brouiller l'interférence d'un grain de poussière")),
]
# l'intuition de départ de chaque pilier, dans les mots de l'auteur : orthographe corrigée, rien d'ajouté, et « […] »
# là où deux de ses messages sont rapprochés. Piliers 1 à 4 : sa conversation d'origine. Pilier 5 : sa demande d'ajout
# d'un cinquième point. Les deux sont dans prive/.
INTUITIONS = {
    1: "L'observateur est celui qui ferme les ciseaux : il faut que le photon revienne du tableau. […] Je vois cela un peu comme "
       "dans un miroir face à un miroir : il y a un décalage. […] Alors, un tableau parfaitement plat.",
    2: "La lumière est comme l'eau, transparente. Je pense que c'est la définition de la lumière par le langage qui est obsolète. […] "
       "La lumière n'est pas absolue mais émergente : alors les vrais mots seraient, selon moi, actuel, émergent, local.",
    3: "Je risque de me tromper, mais selon moi, ici, tout tourne à la vitesse de la lumière. Des corps trop lourds, comme les trous "
       "noirs, ralentissent leur environnement. […] La masse qui courbe l'espace gravitationnel localement est plus lente que "
       "l'ensemble, qui tourne à la vitesse de la lumière.",
    4: "C'est bizarre de devoir rester dans ce cadre fermé de ces deux options. Je vais formuler mon intuition, cela va sembler "
       "peut-être bizarre : on parle de choix retardé ; pour moi, cela veut dire qu'il y a intention, et que ce que nous concevons, "
       "connaissons, est graduellement donné.",
    5: "La cristallisation de l'information fait suite à la quatrième hypothèse : la question est un potentiel ; actualiser, "
       "c'est cristalliser l'information.",
}

# épures : pour chaque pilier, l'instant montré quand l'animation est désactivée, et la description du dessin
EPURES = {
    1: ("3.6", "L'ombre d'une paire de ciseaux sur un tableau plat, vue de face. Elle se referme peu à peu, du centre vers la pointe, chaque point avec son propre retard ; en pointillé, ce que voit celui qui tient les ciseaux, encore plus en retard"),
    2: ("4.0", "En haut, le mot « rayon », barré : une tige rigide enfermée dans les limites de sa définition. En bas, le fait : un trajet invisible, et des éclats là où la lumière rencontre la matière"),
    3: ("6.0", "La toile de l'espace-temps tourne tout entière, avec ses galaxies. Un trou noir y creuse un puits : la toile s'étire, et tout ce qui passe près de lui ralentit et s'entasse"),
    4: ("24.0", "Un sablier : les grains tombent un à un du potentiel vers les constats, et aucun ne remonte"),
    5: ("7.0", "Un germe apparaît au centre, puis un flocon de neige en part : six bras identiques, chacun portant des rameaux de plus en plus fins. La réponse cristallise"),
}
# une phrase sous le dessin, quand l'image demande une précision pour ne pas être prise au pied de la lettre
NOTES_EPURES = {
    3: "Une image de l'auteur : la cadence est figurée par une toile qui tourne. L'espace, lui, ne tourne pas.",
}
VUES = [("index.html", 'Planche<span class="plus"> interactive</span>'), ("article.html", "Article"),
        ("demonstration.html", "Démonstration")]
MOIS = dict(Jan="janvier", Feb="février", Mar="mars", Apr="avril", May="mai", Jun="juin", Jul="juillet", Aug="août",
            Sep="septembre", Oct="octobre", Nov="novembre", Dec="décembre")

KATEX = ('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.css" '
         'integrity="sha512-fHwaWebuwA7NSF5Qg/af4UeDx9XqUpYpOGgubo3yWu+b2IQR4UeQwbb42Ti7gVAjNtVoI/I9TEoYeu9omwcC6g==" crossorigin="anonymous">\n'
         '<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js" '
         'integrity="sha512-LQNxIMR5rXv7o+b1l8+N1EZMfhG7iFZ9HhnbJkTp4zjNr5Wvst75AqUeFDxeRUa7l5vEDyUiAip//r+EFLLCyA==" crossorigin="anonymous"></script>\n')
KATEX_JS = """
window.addEventListener('DOMContentLoaded', function () {
  if (!window.katex) return;
  $$('.tex').forEach(function (d) {
    var t = d.textContent;
    try { katex.render(t, d, { displayMode: true, throwOnError: false, strict: 'ignore' }); d.classList.add('ok'); } catch (e) { }
  });
  // À l'écran, une formule plus large que sa colonne est réduite, jusqu'à 62 % ; au-delà elle défile, et une ombre le signale.
  // À l'impression (et dans le PDF), elle est réduite pour tenir sur la ligne.
  var PAPIER = 650, CORPS = 16.94, MINI = 0.62;
  var ajuster = function () {
    $$('.tex.ok').forEach(function (d) {
      var k = d.querySelector('.katex'), h = d.querySelector('.katex-html');
      if (!k || !h) return;
      d.style.removeProperty('--zoom');
      var r = document.createRange(); r.selectNodeContents(h);
      var large = r.getBoundingClientRect().width, w = large * CORPS / (parseFloat(getComputedStyle(k).fontSize) || 19.36);
      d.dataset.w = Math.round(w);
      if (w > PAPIER) d.style.setProperty('--fit', (PAPIER / w).toFixed(3));
      var c = getComputedStyle(d), place = d.clientWidth - parseFloat(c.paddingLeft) - parseFloat(c.paddingRight) - 2;
      if (!(place > 0) || !(large > 0)) return;
      var zoom = large > place ? Math.max(MINI, place / large) : 1;
      if (zoom < 1) d.style.setProperty('--zoom', zoom.toFixed(3));
      d.classList.toggle('defile', large * zoom > place + 2);
      if (large * zoom > place + 2) d.setAttribute('tabindex', '0'); else d.removeAttribute('tabindex');
    });
  };
  var attente = 0, largeur = window.innerWidth;
  window.addEventListener('resize', function () {
    if (window.innerWidth === largeur) return;
    largeur = window.innerWidth; clearTimeout(attente); attente = setTimeout(ajuster, 160);
  });
  var pret = function () {
    ajuster();
    // le rendu des formules a déplacé le texte : on revient sur l'ancre demandée
    var cible = location.hash.length > 1 && document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (cible) cible.scrollIntoView();
  };
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(pret); else pret();
});
"""

AVIS = ('<aside class="avis"><span class="eyebrow">À savoir avant de lire</span>'
        '<p>Ce dossier examine une à une les formules de départ. Elles ont été écrites à partir des intuitions de l\'auteur, dans la '
        'demande qui a lancé ce travail. Quand le texte dit « la formule demandée », il s\'agit de l\'une d\'elles : elle est '
        'démontrée telle quelle, ou corrigée.</p>%s</aside>')
# le dossier et les autres vues ne nomment pas tout à fait les choses de la même façon
AVIS_MOTS = {
    1: '<p>Le dossier dit « tableau », « tache », « observateur » et « vitesse perçue » là où l\'article et la planche disent '
       '« écran », « ombre », « opérateur » et « vitesse vue ». Ce sont les mêmes choses.</p>',
    2: '<p>Le dossier dit « tableau » là où l\'article et la planche disent « écran » ou « mur ». C\'est le même objet.</p>',
}
AVIS_DOSSIER = ('<p>Dans les deux premiers piliers, le dossier dit « tableau », « tache », « observateur » et « vitesse perçue » là où '
                'les articles et les planches disent « écran », « ombre », « opérateur » et « vitesse vue ». Ce sont les mêmes choses.</p>')

GABARIT = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%%TITREPAGE%%</title>
<meta name="description" content="%%DESCRIPTION%%">
<link rel="canonical" href="%%ADRESSE%%">
<meta property="og:type" content="%%OGTYPE%%">
<meta property="og:site_name" content="Actuel, Émergent, Local">
<meta property="og:locale" content="fr_CA">
<meta property="og:title" content="%%TITRE%%">
<meta property="og:description" content="%%DESCRIPTION%%">
<meta property="og:url" content="%%ADRESSE%%">
<meta property="og:image" content="%%IMAGE%%">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0a2046">
<link rel="icon" href="%%RACINE%%favicon.svg" type="image/svg+xml">
<link rel="icon" href="%%RACINE%%favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="%%RACINE%%apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="%%POLICES%%">
%%TETE%%<style>
%%CSS%%
</style>
</head>
<body class="%%CLASSE%%">
<a class="saut" href="#contenu">Aller au contenu</a>
%%BARRE%%
%%ENTETE%%
<div class="pose"><div class="sheet">
<div class="cartouche">%%CARTOUCHE%%</div>
<main id="contenu" tabindex="-1">
%%CORPS%%
</main>
%%PAGINATION%%</div></div>
%%PIED%%
%%REMONTER%%<script>
%%JS%%
</script>
</body>
</html>
"""


# ---------------------------------------------------------------- outils
def lire(chemin):
    with io.open(chemin, encoding="utf-8") as f:
        return f.read()


def ecrire(relatif, texte):
    chemin = os.path.join(RACINE, relatif)
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with io.open(chemin, "w", encoding="utf-8", newline="\n") as f:
        f.write(texte)
    print("  écrit : %-34s %6d octets" % (relatif, len(texte.encode("utf-8"))))


def url(nom):
    return urllib.parse.quote(nom)


def e(texte):
    return html.escape(texte, quote=True)


INSECABLES = (("« ", "«\u00a0"), (" »", "\u00a0»"), (" :", "\u00a0:"), (" ;", "\u00a0;"), (" ?", "\u00a0?"), (" !", "\u00a0!"), (" %", "\u00a0%"))
EXPOSANTS = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺", "0123456789−+")


def nombres(t):
    """Un nombre ne se sépare ni de ses milliers, ni de son unité ; une courte égalité tient sur une ligne."""
    t = re.sub(r"(?<=\d) (?=\d{3}(?!\d))", "\u00a0", t)
    t = re.sub(r"(?<=\d) (?=[^\W\d_])", "\u00a0", t)
    t = t.replace(" × ", "\u00a0×\u00a0")
    # un symbole d'une lettre ne commence pas une ligne : « à la cadence c », « vers c/2 »
    t = re.sub(r"(?<=[^\W\d_]) (?=(?:c/2|[cxvtθτφ])(?![\w’'/-]))", "\u00a0", t)
    t = re.sub(r"(?<=\d)–(?=\d)", "\u2060–\u2060", t)
    morceaux = re.split(r" (=|≥|≤|≈|&lt;|&gt;|/|±) ", t)
    t = morceaux[0]
    for i in range(1, len(morceaux), 2):
        avant, signe, apres = morceaux[i - 1], morceaux[i], morceaux[i + 1]
        courts = len(avant.rsplit(" ", 1)[-1]) <= 12 and len(apres.split(" ", 1)[0]) <= 12
        t += ("\u00a0%s\u00a0" if courts else " %s ") % signe + apres
    return t


def typo(fragment, exposants=True):
    """Typographie des textes, pas des balises : apostrophes courbes, espaces insécables, nombres, exposants."""
    def f(m):
        t = m.group(1).replace("&#x27;", "’").replace("'", "’")
        for a, b in INSECABLES:
            t = t.replace(a, b)
        t = nombres(t)
        if exposants:
            t = re.sub("[⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]+", lambda x: "<sup>%s</sup>" % x.group(0).translate(EXPOSANTS), t)
            # le dossier écrit « t indice m » : sur le site, c'est un vrai indice
            t = re.sub(r"(?<![\w’'])([A-Za-z]) indice ([A-Za-z])(?![\w’'])", r"\1<sub>\2</sub>", t)
        return ">" + t + "<"
    return re.sub(r">([^<]+)<", f, fragment)


def typo_planche(corps):
    """Typographie d'une planche : les dessins gardent leurs exposants (pas de balise dans un texte SVG), les formules ne sont pas touchées."""
    morceaux = re.split(r'(<svg\b.*?</svg>|<div class="tex">.*?</div>)', corps, flags=re.S)
    return "".join(x if x.startswith('<div class="tex">') else typo(x, exposants=not x.startswith("<svg")) for x in morceaux)


def simple(texte):
    """Texte pour un attribut ou un titre de page : échappé, avec l'apostrophe courbe."""
    return e(texte).replace("&#x27;", "’")


SYMBOLES = re.compile(r"\([^()<>]{1,10}\)|(?<![\w’'/])(?:c/2|[xrctvτθφωβ])(?![\w’'/])")


def symboles(h):
    """Dans un libellé écrit en capitales, les symboles et les unités gardent leur casse."""
    return SYMBOLES.sub(lambda m: '<span class="sym">%s</span>' % m.group(0), h)


def entetes(corps):
    return re.sub(r"(<th[^>]*>)(.*?)(</th>)", lambda m: m.group(1) + symboles(m.group(2)) + m.group(3), corps, flags=re.S)


def t(texte):
    """Texte simple -> HTML échappé, avec les espaces insécables."""
    return typo(">" + e(texte) + "<")[1:-1]


def date_fr(md):
    m = re.search(r"^([A-Z][a-z]{2}) (\d{1,2}), (\d{4}) ·", md, flags=re.M)
    if not (m and m.group(1) in MOIS):
        print("  ATTENTION : ligne de date introuvable ou d'une forme inattendue dans un export (attendu : « Nov 17, 2026 · … »)")
        return ""
    return "%d %s %s" % (int(m.group(2)), MOIS[m.group(1)], m.group(3))


def sans_titre(md):
    """Retire le titre et la ligne de date d'un export Markdown."""
    md = re.sub(r"^# .*$", "", md, count=1, flags=re.M)
    return re.sub(r"^[A-Z][a-z]{2} \d{1,2}, \d{4} ·.*$", "", md, count=1, flags=re.M).strip()


def figure(legende, vue):
    for debut, v, titre, svg, etroit in FIGURES:
        if legende.startswith(debut) and v in (None, vue):
            if etroit:
                svg = svg.replace("<svg ", '<svg class="bureau" ', 1) + etroit.replace("<svg ", '<svg class="mobile" ', 1)
            return (typo('<figure class="fig solo"><figcaption class="figtitle">%s</figcaption>' % e(titre))
                    + '<div class="stage">%s</div></figure>' % typo(svg, exposants=False))
    print("  ATTENTION : figure sans dessin, remplacée par un renvoi : « %s »" % legende)
    return '<p class="fnote">Figure : %s. Voir la planche interactive.</p>' % e(legende)


def habiller(corps):
    """Classe et contenu d'un tableau. Un tableau large ou bavard devient une suite de fiches sur téléphone."""
    titres = [re.sub(r"<[^>]+>", "", x).strip() for x in re.findall(r"<th[^>]*>(.*?)</th>", corps, flags=re.S)]
    cellules = [re.sub(r"<[^>]+>", "", c) for c in re.findall(r"<td[^>]*>(.*?)</td>", corps, flags=re.S)]
    if len(titres) < 3 or (len(titres) == 3 and all(len(c) <= 22 for c in cellules)):
        return "data", corps
    rang = [0]

    def etiquette(m):
        titre = titres[rang[0] % len(titres)]
        rang[0] += 1
        return '<td data-th="%s"%s>' % (html.escape(html.unescape(titre), quote=True), m.group(1))
    return "data empile", re.sub(r"<td([^>]*)>", etiquette, corps)


def tableau(m):
    classe, corps = habiller(m.group(1))
    return '<div class="tablewrap"><table class="%s">%s</table></div>' % (classe, entetes(corps))


def tableau_planche(m):
    classe, corps = habiller(m.group(1))
    return '<table class="%s">%s</table>' % (classe, entetes(corps))


def encadres(h):
    """Les lectures mécaniques et les corrections du dossier reprennent les encadrés des planches."""
    h = re.sub(r"<p><strong>Lecture mécanique\s*\.</strong>\s*(.*?)</p>",
               r'<div class="lecture"><span class="eyebrow">Lecture mécanique</span><p>\1</p></div>', h, flags=re.S)

    def corr(m):
        nom = "Précision" if m.group(2).startswith("Précision") else "Correction"
        return '<div class="correction"><span class="eyebrow">%s</span><p>%s</p>%s</div>' % (nom, m.group(1), m.group(3) or "")
    return re.sub(r"<p>(<strong>((?:Corrections?|Précision)\b[^<]*)</strong>.*?)</p>(\s*<(ol|ul)>.*?</\4>)?", corr, h, flags=re.S)


def md_html(md, vue):
    """Markdown exporté -> HTML. Les formules et les figures passent par des marqueurs pour ne pas être altérées."""
    figs, texs = [], []

    def r_fig(m):
        figs.append(html.unescape(m.group(1)).strip())
        return "\n\nFIGURE%dFIN\n\n" % (len(figs) - 1)

    def r_tex(m):
        texs.append(m.group(1).strip())
        return "\n\nFORMULE%dFIN\n\n" % (len(texs) - 1)

    md = re.sub(r"^&#91;embedded content: (.*?)\\\]\s*$", r_fig, md, flags=re.M)
    md = re.sub(r"^```latex\s*\n(.*?)\n```\s*$", r_tex, md, flags=re.M | re.S)
    h = markdown.markdown(md, extensions=["tables"], output_format="html5")
    h = re.sub(r"<table>(.*?)</table>", tableau, h, flags=re.S)
    h = encadres(typo(h))
    h = re.sub(r"<p>FIGURE(\d+)FIN</p>", lambda m: figure(figs[int(m.group(1))], vue), h)
    h = re.sub(r"<p>FORMULE(\d+)FIN</p>", lambda m: '<div class="tex">%s</div>' % html.escape(texs[int(m.group(1))]), h)
    return h


def chapeau(h):
    """Sépare le premier paragraphe, qui monte dans l'en-tête, du reste du texte."""
    m = re.match(r"\s*<p>(.*?)</p>\s*", h, flags=re.S)
    return (m.group(1), h[m.end():]) if m else ("", h)


def bouton(href, texte, classe="btn"):
    return '<a class="%s" href="%s">%s <span aria-hidden="true">→</span></a>' % (classe, href, t(texte))


def intuition(n):
    """L'intuition de départ du pilier, citée en tête de ses pages."""
    return typo('<blockquote class="intuition"><span class="eyebrow">L\'intuition de départ</span><p>« %s »</p>'
                '<footer>%s</footer></blockquote>' % (e(INTUITIONS[n]), AUTEUR))


def plaque(n, classe="plaque"):
    """La plaque d'un pilier : une toile où epures.js trace son dessin animé."""
    fige, description = EPURES[n]
    return '<div class="%s"><canvas data-epure="%d" data-fige="%s" role="img" aria-label="%s"></canvas></div>' % (
        classe, n, fige, e(description))


def entete(repere, titre, texte="", suite="", onglets="", dessin=""):
    """En-tête de page : le plan bleu, avec repères, titre, chapeau, puis boutons ou onglets."""
    bloc = '<p class="repere">%s</p>\n<h1>%s</h1>\n%s%s' % (
        "".join("<span>%s</span>" % symboles(t(r)) for r in repere), titre, ('<p class="chapeau">%s</p>\n' % texte) if texte else "", suite)
    if dessin:
        bloc = '<div class="tete"><div>\n%s</div>\n<figure class="epure">%s</figure></div>\n' % (bloc, dessin)
    return '<header class="plan"><div class="dedans%s">\n%s%s</div></header>' % (" onglets" if onglets else "", bloc, onglets)


def entete_pilier(p, vue):
    """En-tête d'un pilier, le même sur ses trois vues : son titre, puis l'intuition de l'auteur, dans ses mots."""
    onglets = '<nav class="vues" aria-label="Trois façons de lire ce pilier">%s</nav>\n' % "".join(
        '<a href="%s"%s>%s</a>' % (f, ' aria-current="page"' if f == vue else "", nom) for f, nom in VUES)
    note = NOTES_EPURES.get(p["n"])
    dessin = plaque(p["n"]) + ("<figcaption>%s</figcaption>" % t(note) if note else "")
    return entete(["Pilier %d / 5" % p["n"], p["objet"]], t(p["titre"]), suite=intuition(p["n"]) + "\n", onglets=onglets, dessin=dessin)


def amorce(etiquette, texte, titre="", pilier=""):
    """Ouvre la feuille : le nom de la vue, le titre du document s'il diffère de celui du pilier, puis son chapeau."""
    h = '<span class="eyebrow">%s</span>' % etiquette
    if titre and titre != pilier:
        h += '<h2 class="doc-titre">%s</h2>' % t(titre)
    return '<div class="amorce">%s<p class="lead">%s</p></div>' % (h, texte)


def rail(h):
    """Pose une ancre sur chaque intertitre ; renvoie le sommaire latéral (grand écran), le sommaire repliable (petit écran) et le texte."""
    liens = []

    def ancre(m):
        ident = re.search(r'id="([^"]+)"', m.group(1)).group(1) if m.group(1) else "s%d" % (len(liens) + 1)
        liens.append('<li><a href="#%s">%s</a></li>' % (ident, re.sub(r"</?a\b[^>]*>", "", m.group(2))))
        return '<h2 id="%s">%s</h2>' % (ident, m.group(2))
    h = re.sub(r'<h2( id="[^"]+")?>(.*?)</h2>', ancre, h, flags=re.S)
    if len(liens) < 2:
        return "", "", h
    nav = '<nav class="rail" aria-label="Dans cette page"><span class="eyebrow">Dans cette page</span><ol>%s</ol></nav>\n' % "".join(liens)
    plie = '<details class="sommaire" id="sommaire"><summary>Dans cette page</summary><ol>%s</ol></details>\n' % "".join(liens)
    return nav, plie, h


def references(refs):
    """Lit la liste des références du dossier : (pilier, année, auteurs, titre)."""
    sortie, pilier = [], 0
    for ligne in refs.split("\n"):
        m = re.match(r"\*\*Pilier (\d)\*\*", ligne)
        if m:
            pilier = int(m.group(1))
            continue
        m = re.match(r"- (.+?) \((\d{4})[a-z]?\)\.\s*(.*)", ligne)
        if not (m and pilier):
            if ligne.startswith("- "):
                print("  note : référence sans année, absente de la frise : %s" % ligne[2:70])
            continue
        noms = [x for x in m.group(1).split(", ") if not re.match(r"^(?:[^\W\d_]\.[- ]?)+$|^et al\.$", x)]
        auteurs = noms[0] + " et al." if ("et al." in m.group(1) or len(noms) > 2) else " et ".join(noms)
        titre = (re.match(r"\[([^\]]+)\]", m.group(3)) or re.match(r"«\s*(.+?)\s*»", m.group(3))
                 or re.match(r"(.+?)\.(?:\s|$)", m.group(3)))
        sortie.append((pilier, int(m.group(2)), auteurs, titre.group(1).strip() if titre else ""))
    return sortie


def frise(refs):
    """Frise des travaux cités : un rang par pilier, un point par référence, placé à son année.
    Deux mises en page du même dessin : large pour l'ordinateur, étroite pour le téléphone."""
    donnees = references(refs)
    if not donnees:
        sys.exit("Arrêt : aucune référence lue dans la section « Références » du dossier.")
    an_min, an_max = min(d[1] for d in donnees), max(d[1] for d in donnees)
    a0, a1 = an_min // 20 * 20, (an_max // 5 + 2) * 5

    def dessin(etroit):
        large, gx, dx, ecart = (360, 16, 328, 13) if etroit else (1000, 250, 732, 12)

        def X(an):
            return gx + dx * (an - a0) / float(a1 - a0)
        y, corps = 20, []
        for p in PILIERS:
            niveaux, points = [], []
            for (_, an, auteurs, titre) in sorted(d for d in donnees if d[0] == p["n"]):
                x = X(an)
                niv = next((k for k, dernier in enumerate(niveaux) if x - dernier >= ecart), len(niveaux))
                if niv == len(niveaux):
                    niveaux.append(x)
                else:
                    niveaux[niv] = x
                points.append((x, niv, an, auteurs, titre))
            # la hauteur du rang suit l'empilement : aucun point ne touche le rang du dessus
            fond = y + (34 + ecart * max(len(niveaux), 2) if etroit else max(56, 24 + ecart * len(niveaux)))
            base = fond - 15
            corps.append('<line x1="16" y1="%d" x2="%d" y2="%d" class="ln"/>' % (fond, large - 16, fond))
            if etroit:
                corps.append('<text x="16" y="%d"><tspan class="tb">Pilier %d</tspan><tspan class="tq" dx="8">%s</tspan></text>'
                             % (y + 15, p["n"], e(p["objet"])))
            else:
                corps.append('<text x="16" y="%d" class="tb">Pilier %d</text><text x="16" y="%d" class="tq">%s</text>'
                             % (base - 13, p["n"], base + 4, e(p["objet"])))
            for i, (x, niv, an, auteurs, titre) in enumerate(points):
                yy = base - ecart * niv
                nom = "%s (%d)" % (auteurs, an)
                corps.append('<g class="ref" tabindex="0" role="img" aria-label="%s. %s" data-t="%s" data-s="%s">'
                             '<circle class="touche" cx="%.1f" cy="%.1f" r="14"/><circle class="pt" cx="%.1f" cy="%.1f" r="%s"/></g>'
                             % (e(nom), e(titre), e(nom), e(titre), x, yy, x, yy, "5.5" if etroit else "5"))
                if i == 0 and not etroit:
                    # le plus ancien du rang est nommé : à gauche du point s'il y a la place, sinon au-dessus
                    if x - 10 - 6.4 * len("%s, %d" % (auteurs, an)) > gx - 8:
                        corps.append('<text x="%.1f" y="%.1f" text-anchor="end" class="tq">%s, %d</text>' % (x - 10, yy + 4, e(auteurs), an))
                    else:
                        corps.append('<text x="%.1f" y="%.1f" class="tq">%s, %d</text>' % (x - 4, yy - 13, e(auteurs), an))
            y = fond
        grille = "".join('<line x1="%.1f" y1="20" x2="%.1f" y2="%d" class="gr"/><text x="%.1f" y="%d" text-anchor="middle" class="tm">%d</text>'
                         % (X(an), X(an), y, X(an), y + 19, an) for an in range(a0, a1, 40 if etroit else 20))
        return ('<svg class="%s" viewBox="0 0 %d %d" role="group" aria-label="Frise de %d travaux cités, de %d à %d, répartis par pilier">%s%s</svg>'
                % ("frise mobile" if etroit else "wide frise bureau", large, y + 30, len(donnees), an_min, an_max, grille, "".join(corps)))
    return typo(dessin(False), exposants=False) + typo(dessin(True), exposants=False), len(donnees), an_min, an_max


def pagination(p, vue):
    n = p["n"]
    if n > 1:
        q = PILIERS[n - 2]
        avant = '<a href="../pilier-%d/%s"><span class="num">← Pilier %d</span><b>%s</b></a>' % (q["n"], vue, q["n"], t(q["titre"]))
    else:
        avant = '<a href="../index.html"><span class="num">← Accueil</span><b>Les cinq piliers</b></a>'
    if n < len(PILIERS):
        q = PILIERS[n]
        apres = '<a href="../pilier-%d/%s"><span class="num">Pilier %d →</span><b>%s</b></a>' % (q["n"], vue, q["n"], t(q["titre"]))
    else:
        apres = '<a href="../dossier.html"><span class="num">Pour finir →</span><b>Le dossier complet</b></a>'
    return '<nav class="pagination" aria-label="Pilier précédent et pilier suivant">%s%s</nav>\n' % (avant, apres)


def page(relatif, titre, description, haut, corps, js, cart, classe, pilier=None, vue=None, tete="", accueil=False, bas="", racine=None):
    """Assemble une page : barre, en-tête, feuille (cartouche, corps, pagination), pied."""
    if racine is None:
        racine = "../" if pilier else ""
    fichier = vue or "index.html"
    nav = "".join('<a href="%spilier-%d/%s"%s title="%s" aria-label="Pilier %d : %s">%d</a>' % (
        racine, p["n"], fichier, ' aria-current="page"' if pilier and p["n"] == pilier["n"] else "", simple(p["titre"]), p["n"],
        simple(p["titre"]), p["n"]) for p in PILIERS)
    barre = ('<div class="barre"><div class="dedans">\n<a class="marque" href="%sindex.html" aria-label="Accueil : %s"%s>%s<span>%s</span></a>\n'
             '<nav aria-label="Piliers et dossier"><span class="lib">Piliers</span>%s<a class="dos" href="%sdossier.html"%s>Dossier</a></nav>\n'
             '</div></div>' % (racine, NOM, ' aria-current="page"' if accueil else "", ICONE, NOM, nav, racine,
                               ' aria-current="page"' if relatif == "dossier.html" else ""))
    liens = ['<a href="%sindex.html">Accueil</a>' % racine, '<a href="%sdossier.html">Dossier complet</a>' % racine,
             '<a href="%s%s">Dossier en PDF</a>' % (racine, PDF_DOSSIER)]
    if pilier:
        liens.append('<a href="../documents/%s.pdf">Article en PDF</a>' % url(pilier["article"]))
    liens.append('<a href="%s">Code source</a>' % DEPOT)
    pied = typo('<footer class="pied"><div class="dedans">\n<p class="sig">%s<span>%s · un modèle de %s</span></p>\n'
                '<nav aria-label="Liens de bas de page">%s</nav>\n</div></footer>' % ("ICONEICI", NOM, AUTEUR, "".join(liens))).replace("ICONEICI", ICONE)
    cartouche = typo("".join('<div class="cc"><span class="ck">%s</span><span class="cv">%s</span></div>' % (e(k), e(v)) for k, v in cart))
    remonter = ('<a class="remonter" href="#sommaire" hidden><span aria-hidden="true">↑</span> Sommaire</a>\n'
                if 'id="sommaire"' in corps else "")
    adresse = SITE + (relatif[:-len("index.html")] if relatif.endswith("index.html") else relatif)
    doc = (GABARIT.replace("%%TITREPAGE%%", simple(titre if accueil else "%s · %s" % (titre, NOM))).replace("%%TITRE%%", simple(titre))
           .replace("%%DESCRIPTION%%", simple(description)).replace("%%REMONTER%%", remonter).replace("%%ADRESSE%%", adresse).replace("%%IMAGE%%", SITE + IMAGE_PARTAGE)
           .replace("%%OGTYPE%%", "website" if accueil else "article").replace("%%RACINE%%", racine).replace("%%POLICES%%", POLICES)
           .replace("%%TETE%%", tete).replace("%%CLASSE%%", classe).replace("%%BARRE%%", barre).replace("%%ENTETE%%", haut)
           .replace("%%CARTOUCHE%%", cartouche).replace("%%PAGINATION%%", bas).replace("%%PIED%%", pied)
           .replace("%%CSS%%", lire(os.path.join(GAB, "base.css"))).replace("%%JS%%", js).replace("%%CORPS%%", corps))
    ecrire(relatif, doc)


def cart(objet, cle3, val3, date):
    return [("Projet", "Modèle « %s »" % NOM), ("Objet", objet), (cle3, val3), ("Auteur", AUTEUR), ("Date", date)]


# ---------------------------------------------------------------- productions qui demandent un navigateur
def navigateur():
    candidats = [shutil.which(n) for n in ("msedge", "chrome", "google-chrome", "chromium")] + [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
    return next((c for c in candidats if c and os.path.exists(c)), None)


def imprimer(nav, sortie, source, *options):
    """Lance le navigateur sans interface ; vrai si le fichier de sortie a bien été (ré)écrit."""
    avant = os.path.getmtime(sortie) if os.path.exists(sortie) else 0
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as profil:
        subprocess.run([nav, "--headless=new", "--disable-gpu", "--no-first-run", "--hide-scrollbars",
                        "--user-data-dir=" + profil, "--virtual-time-budget=25000"] + list(options) + [source],
                       capture_output=True, timeout=600)
    return os.path.exists(sortie) and os.path.getmtime(sortie) > avant


def pdf_dossier(nav):
    """Imprime dossier.html en PDF, pour obtenir un dossier aux formules composées."""
    sortie = os.path.join(RACINE, PDF_DOSSIER)
    ok = imprimer(nav, sortie, pathlib.Path(os.path.join(RACINE, "dossier.html")).as_uri(),
                  "--no-pdf-header-footer", "--print-to-pdf=" + sortie)
    print("  écrit : %-34s %6d octets" % (PDF_DOSSIER, os.path.getsize(sortie)) if ok else "  PDF non produit : l'impression a échoué")


def image_partage(nav, css, js):
    """Image de 1200 × 630 affichée quand le lien du site est partagé."""
    carte = """<!doctype html><html lang="fr"><head><meta charset="utf-8">
<link rel="stylesheet" href="%s">
<style>
%s
html,body{margin:0;width:1200px;height:630px;overflow:hidden}
.plan{width:1200px;height:630px}
.plan .dedans{max-width:none;padding:56px 62px 0}
.hero{grid-template-columns:1.08fr .92fr;gap:54px}
.accueil h1{font-size:124px;line-height:.98}
.repere{font-size:16px}
.chapeau{font-size:25px;line-height:1.42;max-width:none}
.plaque{aspect-ratio:1/1}
.pl-t,.pl-n{font-size:13px}
</style></head><body>
<header class="plan accueil"><div class="dedans hero">
<div><p class="repere"><span>Modèle de %s</span><span>Cinq piliers</span></p>
<h1><span>Actuel,</span><span>Émergent,</span><span>Local</span></h1>
<p class="chapeau">Cinq intuitions sur la lumière, la gravité et la mesure, mises en équations et confrontées à la physique établie.</p></div>
<figure class="expo"><div class="plaque expo-ecran"><canvas id="expo-a"></canvas><canvas id="expo-b"></canvas>
<span class="pl-t">Écran de détection</span><span class="pl-n">Photons détectés<b id="expo-n">0</b></span></div>
<button id="expo-re" hidden></button></figure>
</div></header>
<script>
%s
</script></body></html>""" % (POLICES, css, AUTEUR, js)
    sortie = os.path.join(RACINE, IMAGE_PARTAGE)
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
        source = os.path.join(d, "carte.html")
        with io.open(source, "w", encoding="utf-8") as f:
            f.write(carte)
        ok = imprimer(nav, sortie, pathlib.Path(source).as_uri() + "#fixe", "--window-size=1200,630", "--screenshot=" + sortie)
    print("  écrit : %-34s %6d octets" % (IMAGE_PARTAGE, os.path.getsize(sortie)) if ok else "  image de partage non produite")


# ---------------------------------------------------------------- construction
def main():
    css = lire(os.path.join(GAB, "base.css"))
    base_js = lire(os.path.join(GAB, "base.js"))
    accueil_js = lire(os.path.join(GAB, "accueil.js"))
    commun_js = base_js + "\n" + lire(os.path.join(GAB, "epures.js"))
    dossier = lire(os.path.join(DOCS, DOSSIER + ".md"))
    date = date_fr(dossier)
    morceaux = re.split(r"^## (.+)$", dossier, flags=re.M)
    intro = sans_titre(morceaux[0])
    sections = {morceaux[i].strip(): morceaux[i + 1] for i in range(1, len(morceaux), 2)}
    attendues = ["Pilier %d " % p["n"] for p in PILIERS] + ["Synthèse", "Références"]
    absentes = [a.strip() for a in attendues if not any(k.startswith(a) for k in sections)]
    if absentes:
        sys.exit("Arrêt : sections introuvables dans le dossier (titres « ## … ») : " + ", ".join(absentes))
    if any("—" not in k for k in sections if k.startswith("Pilier ")):
        sys.exit("Arrêt : un titre de pilier du dossier n'a plus la forme « Pilier N — titre ».")
    refs = sections.get("Références", "")
    print("Site « %s » — sources du %s" % (NOM, date))
    ecrire("favicon.svg", FAVICON)

    for p in PILIERS:
        n, dos = p["n"], "pilier-%d/" % p["n"]
        meta = p.get("meta", p["resume"])

        # 1. planche interactive : son chapeau ouvre la feuille, ses formules sont composées comme celles du dossier
        corps, script = lire(os.path.join(GAB, "p%d.frag.html" % n)).split("<!--SCRIPT-->")
        m = re.match(r'\s*<div class="head">\s*<h1>(.*?)</h1>\s*<p class="lead">(.*?)</p>\s*</div>', corps, flags=re.S)
        chapo = typo(">" + m.group(2) + "<")[1:-1]
        corps = re.sub(r'<table class="data">(.*?)</table>', tableau_planche, typo_planche(corps[m.end():]), flags=re.S)
        corps = (amorce("Planche interactive", chapo) + "\n" + corps.strip() + '\n<p class="suite">%s%s</p>'
                 % (bouton("article.html", "Lire l'article", "btn encre"), bouton("demonstration.html", "Lire la démonstration")))
        page(dos + "index.html", p["titre"], meta, entete_pilier(p, "index.html"), corps,
             commun_js + "\n" + script.strip() + KATEX_JS, cart(p["objet"], "Échelle", p["echelle"], date), "p-planche",
             pilier=p, vue="index.html", tete=KATEX, bas=pagination(p, "index.html"))

        # 2. article de vulgarisation
        art = lire(os.path.join(DOCS, p["article"] + ".md"))
        titre_art = re.search(r"^# (.+)$", art, flags=re.M).group(1).strip()
        date_art = date_fr(art) or date
        texte, reste = chapeau(md_html(sans_titre(art).replace(LIEN_DOSSIER_PRIVE, "demonstration.html"), "article"))
        sommaire, plie, reste = rail(reste)
        corps = ('<div class="avec-rail">%s<article class="prose">\n%s\n%s%s\n<p class="suite">%s%s</p>\n</article></div>'
                 % (sommaire, amorce("Article de vulgarisation", texte, titre_art, p["titre"]), plie, reste,
                    bouton("index.html", "Manipuler la planche interactive", "btn encre"), bouton("demonstration.html", "Lire la démonstration")))
        page(dos + "article.html", titre_art, meta, entete_pilier(p, "article.html"), corps, commun_js,
             cart(p["objet"], "Vue", "Article de vulgarisation", date_art), "p-article",
             pilier=p, vue="article.html", bas=pagination(p, "article.html"))

        # 3. démonstration mathématique : la section du dossier, puis ses références
        cle = next(k for k in sections if k.startswith("Pilier %d " % n))
        titre_demo = cle.split("—", 1)[1].strip()
        demo = sections[cle].replace("\n### ", "\n## ")
        m = re.search(r"\*\*Pilier %d\*\*\s*\n\n((?:- .*(?:\n|$))+)" % n, refs)
        if m:
            demo += "\n\n## Références\n\n" + m.group(1)
        texte, reste = chapeau(md_html(demo.strip(), "demonstration"))
        avis = typo(AVIS % AVIS_MOTS.get(n, ""))
        sommaire, plie, reste = rail(reste)
        corps = ('<div class="avec-rail">%s<article class="prose">\n%s\n%s\n%s%s\n<p class="suite">%s%s</p>\n</article></div>'
                 % (sommaire, amorce("Démonstration mathématique", texte, titre_demo, p["titre"]), avis, plie, reste,
                    bouton("index.html", "Manipuler la planche interactive", "btn encre"), bouton("article.html", "Lire l'article")))
        page(dos + "demonstration.html", titre_demo, meta, entete_pilier(p, "demonstration.html"),
             corps, commun_js + KATEX_JS, cart(p["objet"], "Vue", "Démonstration mathématique", date), "p-demo",
             pilier=p, vue="demonstration.html", tete=KATEX, bas=pagination(p, "demonstration.html"))

    # 4. page d'accueil
    planches = []
    for p in PILIERS:
        planches.append(typo(
            '<article class="plk"><div class="no"><span class="num">Pilier</span><b>%02d</b></div>'
            '<div class="plt"><span class="eyebrow">%s</span><h3><a href="pilier-%d/index.html">%s</a></h3>'
            '<p class="mot">« %s »</p><p>%s</p>'
            '<p class="acces">%s<a class="btn fin" href="pilier-%d/article.html">Article</a>'
            '<a class="btn fin" href="pilier-%d/demonstration.html">Démonstration</a></p></div>'
            '<div class="vis"><a href="pilier-%d/index.html" tabindex="-1" aria-hidden="true">%s</a><p class="clef"><b>%s</b><span>%s</span></p></div></article>'
            % (p["n"], symboles(e(p["objet"])), p["n"], e(p["titre"]), e(INTUITIONS[p["n"]]), e(p["resume"]),
               bouton("pilier-%d/index.html" % p["n"], "Planche interactive", "btn encre"), p["n"], p["n"], p["n"],
               plaque(p["n"], "plaque mini"), p["clef"][0], e(p["clef"][1]))))
    dessin_frise, nb_refs, an_debut, an_fin = frise(refs)
    docs = [("Dossier mathématique complet", "dossier.html", PDF_DOSSIER, DOSSIER)] + [
        ("Article du pilier %d — %s" % (p["n"], p["article"]), "pilier-%d/article.html" % p["n"],
         "documents/%s.pdf" % url(p["article"]), p["article"]) for p in PILIERS]
    rangs = "".join(
        '<li><span>%s</span><span class="liens"><a href="%s">Lire en ligne</a><a href="%s">PDF</a><a href="documents/%s.docx">Word</a>'
        '<a href="documents/%s.md">Markdown</a></span></li>' % (t(nom), web, pdf, url(f), url(f)) for nom, web, pdf, f in docs)
    haut = ('<header class="plan accueil"><div class="dedans hero">\n<div>\n<p class="repere"><span>Modèle de %s</span><span>Cinq piliers</span></p>\n'
            '<h1><span>Actuel,</span> <span>Émergent,</span> <span>Local</span></h1>\n<p class="chapeau">%s</p>\n'
            '<p class="actions">%s%s</p>\n</div>\n'
            '<figure class="expo">\n<div class="plaque expo-ecran" role="img" aria-label="Des impacts de photons s\'accumulent sur un écran et dessinent peu à peu des franges">'
            '<canvas id="expo-a"></canvas><canvas id="expo-b"></canvas>'
            '<span class="pl-t">Écran de détection</span><span class="pl-n">Photons détectés<b id="expo-n">0</b></span></div>\n'
            '<figcaption><p id="expo-txt">Chaque point est l\'arrivée d\'un photon : un lieu, un instant. Aucun ne dessine les franges, '
            'ces bandes qui n\'apparaissent qu\'avec le nombre.</p>\n'
            '<div class="choix" role="group" aria-labelledby="expo-lib"><span class="lib" id="expo-lib">Ce que l\'on sait du trajet de chaque photon</span>'
            '<span class="duo"><button class="jeton" id="expo-libre" type="button" aria-pressed="true">Route inconnue</button>'
            '<button class="jeton" id="expo-route" type="button" aria-pressed="false">Route connue</button></span>'
            '<button class="lien" id="expo-re" type="button">Recommencer</button></div></figcaption>\n'
            '</figure>\n</div></header>'
            % (AUTEUR, t(ACCROCHE), bouton("pilier-1/index.html", "Commencer par le pilier 1", "btn plein"),
               bouton("dossier.html", "Lire le dossier complet")))
    haut = typo(haut)
    corps = typo("""<section aria-labelledby="h-liste">
  <span class="eyebrow">Liste des planches</span>
  <h2 id="h-liste">Les cinq piliers</h2>
  <p>Chaque pilier se lit de trois façons : une planche interactive à manipuler, un article sans équation, et une démonstration complète avec ses références.</p>
  <div class="planches">
%s
  </div>
</section>

<section aria-labelledby="h-fil">
  <span class="eyebrow">Le fil commun</span>
  <h2 id="h-fil">Une même grille de lecture, venue du suivi de projet</h2>
  <p>Tout est parti d'une objection à une phrase qu'on répète souvent : « l'ombre va plus vite que la lumière ». Pour la mettre à l'épreuve, l'auteur a appliqué ses réflexes de suivi de projet. Les cinq piliers posent les trois mêmes questions.</p>
  <dl class="defs">
    <div><dt>Où est l'observateur ?</dt><dd>Celui qui déclenche l'action doit attendre que l'information lui revienne. La boucle de retour fait partie du phénomène.</dd></div>
    <div><dt>Quel chemin, réellement ?</dt><dd>Chaque signal parcourt une vraie distance, à une cadence limitée. Les délais s'additionnent, et le plus long fixe le rythme.</dd></div>
    <div><dt>En transit, ou arrivé ?</dt><dd>Tant qu'un signal voyage, rien n'est encore constaté. Un fait naît à l'endroit et à l'instant où il rencontre la matière.</dd></div>
  </dl>
  <p>De là viennent les trois mots du modèle : actuel, émergent, local. Rien n'y agit à distance ; chaque événement se produit quelque part, à un moment donné.</p>
</section>

<section aria-labelledby="h-verdict">
  <span class="eyebrow">Verdict</span>
  <h2 id="h-verdict">Ce que les équations confirment, et ce qu'elles corrigent</h2>
  <div class="verdict">
    <p>Le dossier part des formules de la demande qui a lancé ce travail, écrites à partir des intuitions de l'auteur. Il démontre ou corrige une à une ces « formules demandées ».</p>
%s
  </div>
</section>

<section aria-labelledby="h-frise">
  <span class="eyebrow">Sources</span>
  <h2 id="h-frise">Un siècle de travaux derrière les cinq piliers</h2>
  <p>Le dossier s'appuie sur NBREFS travaux publiés entre ANDEBUT et ANFINAUTRESREFS. Chaque point est l'un de ces travaux : survolez-le ou touchez-le pour savoir lequel.</p>
  <figure class="fig solo"><div class="stage">DESSINFRISE</div><div class="bulle" hidden></div></figure>
  <p class="fnote">La liste complète, avec un lien vers chaque source, se trouve dans les <a href="dossier.html#references">références du dossier</a>.</p>
</section>

<section aria-labelledby="h-synth">
  <span class="eyebrow">Synthèse</span>
  <h2 id="h-synth">Intuitions, équations, théorèmes et corrections</h2>
  <div class="prose large">
%s
  </div>
</section>

<section aria-labelledby="h-docs">
  <span class="eyebrow">Documents</span>
  <h2 id="h-docs">Tout lire, tout télécharger</h2>
  <p>Le <a href="dossier.html">dossier complet</a> réunit sur une seule page les cinq démonstrations, la synthèse et les références.</p>
  <ul class="docs">%s</ul>
  <p class="fnote">Le PDF du dossier est produit à partir de ce site : les formules y sont composées. Dans ses versions Word et Markdown, elles restent écrites en code LaTeX.</p>
</section>

<section aria-labelledby="h-apropos">
  <span class="eyebrow">À propos</span>
  <h2 id="h-apropos">Comment ce site a été fait</h2>
  <p>Les intuitions sont celles de Sylvain Leduc, qui fait du suivi de projet et s'intéresse à la cosmologie. Leur mise en équations, les articles et ce site ont été réalisés à sa demande avec l'aide d'une intelligence artificielle, Claude, d'Anthropic. Les calculs ont été vérifiés numériquement et les références contrôlées une à une ; les exceptions sont signalées dans le dossier.</p>
</section>""") % ("\n".join(planches), md_html(intro, "accueil"), md_html(sections.get("Synthèse", "").strip(), "accueil"), rangs)
    sans_annee = len(re.findall(r"^- ", refs, flags=re.M)) - nb_refs
    autres = {0: "", 1: ", plus une page technique sans date"}.get(sans_annee, ", plus %d sources sans date" % sans_annee)
    corps = (corps.replace("NBREFS", str(nb_refs)).replace("ANDEBUT", str(an_debut)).replace("ANFINAUTRESREFS", str(an_fin) + autres)
             .replace("DESSINFRISE", dessin_frise))
    page("index.html", NOM,
         "Cinq intuitions sur la lumière, la gravité et la mesure, traduites en équations et confrontées à la physique établie.",
         haut, corps, commun_js + "\n" + accueil_js, cart("Page de garde", "Contenu", "5 planches · 5 articles · 5 démonstrations", date),
         "p-accueil", accueil=True)

    # 5. dossier complet sur une seule page ; il sert aussi à produire le PDF aux formules composées
    texte, h = chapeau(md_html(sans_titre(dossier), "demonstration"))
    sommaire = []

    def ancre(m):
        titre = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        mm = re.match(r"Pilier\s+(\d)", titre)
        ident = "pilier-%s" % mm.group(1) if mm else {"Synthèse": "synthese", "Références": "references"}.get(
            titre, "partie-%d" % (len(sommaire) + 1))
        sommaire.append('<li><a href="#%s">%s</a></li>' % (ident, m.group(1)))
        return '<h2 id="%s">%s</h2>' % (ident, m.group(1))
    h = re.sub(r"<h2>(.*?)</h2>", ancre, h, flags=re.S)
    table = '<nav class="toc" id="sommaire" aria-label="Sommaire du dossier"><span class="eyebrow">Sommaire</span><ol>%s</ol></nav>' % "".join(sommaire)
    h = h.replace('<h2 id="pilier-1">', table + '\n<h2 id="pilier-1">', 1)
    lateral, _, h = rail(h)
    h = re.sub(r'(<h2 id="pilier-(\d)">.*?</h2>)', lambda m: m.group(1) + "\n" + intuition(int(m.group(2))), h, flags=re.S)
    corps = '<div class="avec-rail">%s<article class="prose dossier">\n%s\n%s\n</article></div>' % (lateral, typo(AVIS % AVIS_DOSSIER), h)
    bilan = "".join('<p><b>%d</b><span>%s</span></p>' % (n, mot) for n, mot in (
        (len(PILIERS), "démonstrations"), (h.count('class="tex"'), "formules"), (len(re.findall(r"^- ", refs, flags=re.M)), "références")))
    haut = entete(["Dossier complet", "Cinq démonstrations, synthèse, références"], t(DOSSIER), texte,
                  suite='<p class="actions">%s</p>\n' % bouton(PDF_DOSSIER, "Télécharger le PDF", "btn plein"),
                  dessin='<div class="bilan" role="group" aria-label="Le dossier en chiffres">%s</div>' % bilan)
    page("dossier.html", DOSSIER, "Les cinq démonstrations du modèle, la synthèse et les références, sur une seule page.",
         haut, corps, base_js + KATEX_JS, cart("Les cinq piliers", "Vue", "Dossier complet", date), "p-dossier", tete=KATEX)

    # 6. page d'erreur : ses liens partent de la racine du site, où que se trouve l'adresse fautive
    rs = urllib.parse.urlparse(SITE).path
    liste = "".join(
        '<li><span>Pilier %d — %s</span><span class="liens"><a href="%spilier-%d/index.html">Planche</a><a href="%spilier-%d/article.html">Article</a>'
        '<a href="%spilier-%d/demonstration.html">Démonstration</a></span></li>'
        % (p["n"], e(p["titre"]), rs, p["n"], rs, p["n"], rs, p["n"]) for p in PILIERS)
    liste += '<li><span>Le dossier complet</span><span class="liens"><a href="%sdossier.html">Lire en ligne</a><a href="%s%s">PDF</a></span></li>' % (rs, rs, PDF_DOSSIER)
    corps = typo('<section><span class="eyebrow">Par où continuer</span><h2>Les cinq piliers et le dossier</h2>\n<ul class="docs">%s</ul></section>' % liste)
    haut = entete(["Erreur 404"], t("Cette page n'existe pas"), t("L'adresse a peut-être changé. Les cinq piliers, eux, n'ont pas bougé."),
                  suite='<p class="actions">%s</p>\n' % bouton(rs + "index.html", "Revenir à l'accueil", "btn plein"))
    page("404.html", "Page introuvable", "Cette page n'existe pas.", haut, corps, base_js,
         cart("Page introuvable", "Vue", "Erreur 404", date), "p-404", tete='<meta name="robots" content="noindex">\n', racine=rs)

    # 7. plan du site, pour les moteurs de recherche
    adresses = ["", "dossier.html"] + ["pilier-%d/%s" % (p["n"], v) for p in PILIERS for v in ("", "article.html", "demonstration.html")]
    ecrire("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n'
           % "".join("  <url><loc>%s%s</loc></url>\n" % (SITE, a) for a in adresses))

    if "--pdf" in sys.argv:
        nav = navigateur()
        if nav:
            pdf_dossier(nav)
            image_partage(nav, css, base_js + "\n" + accueil_js)
        else:
            print("  PDF et image de partage non produits : ni Edge ni Chrome trouvés sur cette machine")
    verifier_liens()


def verifier_liens():
    """Chaque lien interne doit pointer vers un fichier présent, et chaque ancre vers un identifiant de la page visée."""
    manquants, pages = 0, {}

    def idents(chemin):
        if chemin not in pages:
            pages[chemin] = set(re.findall(r'\bid="([^"]+)"', lire(chemin)))
        return pages[chemin]
    for dossier, _, fichiers in os.walk(RACINE):
        relatif = os.path.relpath(dossier, RACINE).replace(os.sep, "/")
        if relatif.split("/")[0] in (".git", "outils", "prive", "documents"):
            continue
        for f in fichiers:
            if not f.endswith(".html"):
                continue
            ici = os.path.join(dossier, f)
            for cible in re.findall(r'href="([^"]+)"', lire(ici)):
                if re.match(r"^(https?:|mailto:|/)", cible):
                    continue
                fichier, _, ancre = html.unescape(cible).partition("#")
                chemin = os.path.normpath(os.path.join(dossier, urllib.parse.unquote(fichier))) if fichier else ici
                if not os.path.exists(chemin):
                    manquants += 1
                    print("  LIEN CASSÉ dans %s : %s" % (os.path.relpath(ici, RACINE), cible))
                elif ancre and ancre != "top" and chemin.endswith(".html") and ancre not in idents(chemin):
                    manquants += 1
                    print("  ANCRE INCONNUE dans %s : %s" % (os.path.relpath(ici, RACINE), cible))
    print("Liens internes :", "tous valides" if not manquants else "%d cassés" % manquants)


if __name__ == "__main__":
    main()
