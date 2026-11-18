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
from figures import FAVICON, FIGURES, ICONE, VIGNETTES  # noqa: E402

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
    dict(n=1, titre="L'ombre plus rapide que la lumière", objet="Géométrie de l'observateur", echelle="1 px = 400 000 km",
         article="L'ombre plus rapide que la lumière, vue par celui qui tient les ciseaux",
         resume="Sur un écran plat, l'ombre des ciseaux part de 524 fois la vitesse de la lumière et retombe vers c. "
                "Celui qui tient les ciseaux la voit tendre vers c/2.",
         clef=("524 c", "vitesse de l'ombre au centre de l'écran, dans l'exemple chiffré")),
    dict(n=2, titre="On ne voit jamais la lumière passer", objet="Lumière actuelle, émergente, locale", echelle="Schémas de principe",
         article="On ne voit jamais la lumière passer",
         resume="Un faisceau qui traverse le vide est invisible de côté. La lumière ne se manifeste qu'à l'endroit "
                "et à l'instant où elle rencontre de la matière.",
         clef=("1 clic", "par photon : deux détecteurs ne se déclenchent pratiquement jamais ensemble (1986)")),
    dict(n=3, titre="La pente du temps", objet="Cadence c et masse comme frein", echelle="Schémas de principe",
         article="Tomber, c'est suivre la pente du temps",
         resume="Près d'une masse, les horloges battent plus lentement. La pesanteur est la pente de ce ralentissement, "
                "multipliée par c².",
         clef=("9,81 m/s<sup>2</sup>", "la pesanteur, retrouvée en multipliant la pente du temps par c²")),
    dict(n=4, titre="Le choix qui ne réécrit pas le passé", objet="Choix retardé de Wheeler", echelle="Schémas de principe",
         article="Le choix d'aujourd'hui ne réécrit pas le passé",
         resume="Choisir aujourd'hui comment mesurer un photon ne change rien à ce qu'il a fait. Entre « une route » "
                "et « deux routes », tous les intermédiaires existent.",
         clef=("3 500 km", "portée de l'expérience du choix retardé réalisée par satellite (2017)")),
    dict(n=5, titre="Comment une réponse devient un fait", objet="Cristallisation de l'information", echelle="Schémas de principe",
         article="Comment une réponse devient un fait",
         resume="La réponse est d'abord inscrite au crayon, encore effaçable. L'environnement la recopie ensuite "
                "des milliards de fois et la grave.",
         clef=("10 ps", "dix picosecondes pour éteindre l'interférence d'un grain de poussière au soleil (calcul de 1985)")),
]
VUES = [("index.html", 'Planche<span class="plus"> interactive</span>'), ("article.html", "Article"),
        ("demonstration.html", "Démonstration")]
MOIS = dict(Jan="janvier", Feb="février", Mar="mars", Apr="avril", May="mai", Jun="juin", Jul="juillet", Aug="août",
            Sep="septembre", Oct="octobre", Nov="novembre", Dec="décembre")

KATEX = ('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.css">\n'
         '<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>\n')
KATEX_JS = """
window.addEventListener('DOMContentLoaded', function () {
  if (!window.katex) return;
  $$('.tex').forEach(function (d) {
    var t = d.textContent;
    try { katex.render(t, d, { displayMode: true, throwOnError: false, strict: 'ignore' }); d.classList.add('ok'); } catch (e) { }
  });
  // À l'impression (et dans le PDF), une formule plus large que la page est réduite pour tenir sur la ligne.
  var PAPIER = 650, CORPS = 16.94;
  var ajuster = function () {
    $$('.tex.ok').forEach(function (d) {
      var k = d.querySelector('.katex'), h = d.querySelector('.katex-html');
      if (!k || !h) return;
      var r = document.createRange(); r.selectNodeContents(h);
      var w = r.getBoundingClientRect().width * CORPS / (parseFloat(getComputedStyle(k).fontSize) || 19.36);
      d.dataset.w = Math.round(w);
      if (w > PAPIER) d.style.setProperty('--fit', (PAPIER / w).toFixed(3));
    });
  };
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(ajuster); else ajuster();
});
"""

AVIS = ('<aside class="avis"><span class="eyebrow">À savoir avant de lire</span>'
        '<p>Ce dossier examine une à une les formules que l\'auteur proposait à partir de ses intuitions. Quand le texte dit '
        '« la formule demandée », il s\'agit de l\'une de ces formules de départ : elle est démontrée telle quelle, ou corrigée.</p>'
        '%s</aside>')
AVIS_MOT = '<p>Le dossier dit « tableau » là où les articles et les planches disent « écran ». C\'est le même objet.</p>'

GABARIT = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="%%POLICES%%">
%%TETE%%<style>
%%CSS%%
</style>
</head>
<body class="%%CLASSE%%">
%%BARRE%%
%%ENTETE%%
<div class="pose"><div class="sheet">
<div class="cartouche">%%CARTOUCHE%%</div>
<main>
%%CORPS%%
</main>
%%PAGINATION%%</div></div>
%%PIED%%
<script>
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


def typo(fragment):
    """Espaces insécables de la typographie française, dans les textes seulement (pas dans les balises)."""
    def f(m):
        t = m.group(1)
        for a, b in INSECABLES:
            t = t.replace(a, b)
        return ">" + t + "<"
    return re.sub(r">([^<]+)<", f, fragment)


def t(texte):
    """Texte simple -> HTML échappé, avec les espaces insécables."""
    return typo(">" + e(texte) + "<")[1:-1]


def date_fr(md):
    m = re.search(r"^([A-Z][a-z]{2}) (\d{1,2}), (\d{4}) ·", md, flags=re.M)
    return "%d %s %s" % (int(m.group(2)), MOIS[m.group(1)], m.group(3)) if m else ""


def sans_titre(md):
    """Retire le titre et la ligne de date d'un export Markdown."""
    md = re.sub(r"^# .*$", "", md, count=1, flags=re.M)
    return re.sub(r"^[A-Z][a-z]{2} \d{1,2}, \d{4} ·.*$", "", md, count=1, flags=re.M).strip()


def figure(legende, vue):
    for debut, v, titre, svg in FIGURES:
        if legende.startswith(debut) and v in (None, vue):
            return ('<figure class="fig solo"><figcaption class="figtitle">%s</figcaption><div class="stage">%s</div></figure>'
                    % (e(titre), svg))
    return '<p class="fnote">Figure : %s. Voir la planche interactive.</p>' % e(legende)


def habiller(corps):
    """Classe et contenu d'un tableau. Un tableau large ou bavard devient une suite de fiches sur téléphone."""
    titres = [re.sub(r"<[^>]+>", "", x).strip() for x in re.findall(r"<th[^>]*>(.*?)</th>", corps, flags=re.S)]
    cellules = [re.sub(r"<[^>]+>", "", c) for c in re.findall(r"<td[^>]*>(.*?)</td>", corps, flags=re.S)]
    if len(titres) < 3 or (len(titres) == 3 and all(len(c) <= 40 for c in cellules)):
        return "data", corps
    rang = [0]

    def etiquette(m):
        titre = titres[rang[0] % len(titres)]
        rang[0] += 1
        return '<td data-th="%s"%s>' % (html.escape(html.unescape(titre), quote=True), m.group(1))
    return "data empile", re.sub(r"<td([^>]*)>", etiquette, corps)


def tableau(m):
    classe, corps = habiller(m.group(1))
    return '<div class="tablewrap"><table class="%s">%s</table></div>' % (classe, corps)


def tableau_planche(m):
    classe, corps = habiller(m.group(1))
    return '<table class="%s">%s</table>' % (classe, corps)


def encadres(h):
    """Les lectures mécaniques et les corrections du dossier reprennent les encadrés des planches."""
    h = re.sub(r"<p><strong>Lecture mécanique\s*\.</strong>\s*(.*?)</p>",
               r'<div class="lecture"><span class="eyebrow">Lecture mécanique</span><p>\1</p></div>', h, flags=re.S)

    def corr(m):
        nom = "Précision" if m.group(2).startswith("Précision") else "Correction"
        return '<div class="correction"><span class="eyebrow">%s</span><p>%s</p></div>' % (nom, m.group(1))
    return re.sub(r"<p>(<strong>((?:Corrections?|Précision)\b[^<]*)</strong>.*?)</p>", corr, h, flags=re.S)


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
    return '<a class="%s" href="%s">%s <span aria-hidden="true">→</span></a>' % (classe, href, texte)


def entete(repere, titre, texte="", suite="", onglets=""):
    """En-tête de page : le plan bleu, avec repères, titre, chapeau, puis boutons ou onglets."""
    return ('<header class="plan"><div class="dedans%s">\n<p class="repere">%s</p>\n<h1>%s</h1>\n%s%s%s</div></header>' % (
        " onglets" if onglets else "", "".join("<span>%s</span>" % t(r) for r in repere), titre,
        ('<p class="chapeau">%s</p>\n' % texte) if texte else "", suite, onglets))


def entete_pilier(p, vue, titre, texte):
    onglets = '<nav class="vues" aria-label="Trois façons de lire ce pilier">%s</nav>\n' % "".join(
        '<a href="%s"%s>%s</a>' % (f, ' aria-current="page"' if f == vue else "", nom) for f, nom in VUES)
    return entete(["Pilier %d / 5" % p["n"], p["objet"]], titre, texte, onglets=onglets)


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


def page(relatif, titre, description, haut, corps, js, cart, classe, pilier=None, vue=None, tete="", accueil=False, bas=""):
    """Assemble une page : barre, en-tête, feuille (cartouche, corps, pagination), pied."""
    racine = "../" if pilier else ""
    fichier = vue or "index.html"
    nav = "".join('<a href="%spilier-%d/%s"%s title="%s">%d</a>' % (
        racine, p["n"], fichier, ' aria-current="page"' if pilier and p["n"] == pilier["n"] else "", e(p["titre"]), p["n"])
        for p in PILIERS)
    barre = ('<div class="barre"><div class="dedans">\n<a class="marque" href="%sindex.html" aria-label="Accueil : %s"%s>%s<span>%s</span></a>\n'
             '<nav aria-label="Piliers et dossier"><span class="lib">Piliers</span>%s<a class="dos" href="%sdossier.html"%s>Dossier</a></nav>\n'
             '</div></div>' % (racine, NOM, ' aria-current="page"' if accueil else "", ICONE, NOM, nav, racine,
                               ' aria-current="page"' if relatif == "dossier.html" else ""))
    liens = ['<a href="%sindex.html">Accueil</a>' % racine, '<a href="%sdossier.html">Dossier complet</a>' % racine,
             '<a href="%s%s">Dossier en PDF</a>' % (racine, PDF_DOSSIER)]
    if pilier:
        liens.append('<a href="../documents/%s.pdf">Article en PDF</a>' % url(pilier["article"]))
    liens.append('<a href="%s">Code source</a>' % DEPOT)
    pied = ('<footer class="pied"><div class="dedans">\n<p class="sig">%s<span>%s · un modèle de %s</span></p>\n'
            '<nav aria-label="Liens de bas de page">%s</nav>\n</div></footer>' % (ICONE, NOM, AUTEUR, "".join(liens)))
    cartouche = typo("".join('<div class="cc"><span class="ck">%s</span><span class="cv">%s</span></div>' % (e(k), e(v)) for k, v in cart))
    adresse = SITE + (relatif[:-len("index.html")] if relatif.endswith("index.html") else relatif)
    doc = (GABARIT.replace("%%TITREPAGE%%", e(titre if accueil else "%s · %s" % (titre, NOM))).replace("%%TITRE%%", e(titre))
           .replace("%%DESCRIPTION%%", e(description)).replace("%%ADRESSE%%", adresse).replace("%%IMAGE%%", SITE + IMAGE_PARTAGE)
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
.accueil h1{font-size:136px}
.repere{font-size:16px}
.chapeau{font-size:25px;line-height:1.42;max-width:none}
.plaque{aspect-ratio:1/1}
.pl-t,.pl-n{font-size:13px}
</style></head><body>
<header class="plan accueil"><div class="dedans hero">
<div><p class="repere"><span>Modèle de %s</span><span>Cinq piliers</span></p>
<h1><span>Actuel,</span><span>Émergent,</span><span>Local</span></h1>
<p class="chapeau">Cinq intuitions sur la lumière, la gravité et la mesure, mises en équations et confrontées à la physique établie.</p></div>
<figure class="expo"><div class="plaque"><canvas id="expo-a"></canvas><canvas id="expo-b"></canvas>
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
    dossier = lire(os.path.join(DOCS, DOSSIER + ".md"))
    date = date_fr(dossier)
    morceaux = re.split(r"^## (.+)$", dossier, flags=re.M)
    intro = sans_titre(morceaux[0])
    sections = {morceaux[i].strip(): morceaux[i + 1] for i in range(1, len(morceaux), 2)}
    refs = sections.get("Références", "")
    print("Site « %s » — sources du %s" % (NOM, date))
    ecrire("favicon.svg", FAVICON)

    for p in PILIERS:
        n, dos = p["n"], "pilier-%d/" % p["n"]
        suite = pagination(p, "index.html")

        # 1. planche interactive : le titre et le chapeau du gabarit montent dans l'en-tête
        corps, script = lire(os.path.join(GAB, "p%d.frag.html" % n)).split("<!--SCRIPT-->")
        for a, b in (("« ", "«&nbsp;"), (" »", "&nbsp;»"), (" :", "&nbsp;:"), (" ;", "&nbsp;;"), (" ?", "&nbsp;?"), (" !", "&nbsp;!")):
            corps = corps.replace(a, b)
        m = re.match(r'\s*<div class="head">\s*<h1>(.*?)</h1>\s*<p class="lead">(.*?)</p>\s*</div>', corps, flags=re.S)
        corps = re.sub(r'<table class="data">(.*?)</table>', tableau_planche, corps[m.end():], flags=re.S)
        page(dos + "index.html", p["titre"], p["resume"], entete_pilier(p, "index.html", m.group(1), m.group(2)), corps.strip(),
             base_js + "\n" + script.strip(), cart(p["objet"], "Échelle", p["echelle"], date), "p-planche",
             pilier=p, vue="index.html", bas=suite)

        # 2. article de vulgarisation
        art = lire(os.path.join(DOCS, p["article"] + ".md"))
        titre_art = re.search(r"^# (.+)$", art, flags=re.M).group(1).strip()
        date_art = date_fr(art) or date
        texte, reste = chapeau(md_html(sans_titre(art).replace(LIEN_DOSSIER_PRIVE, "demonstration.html"), "article"))
        corps = ('<article class="prose">\n%s\n<p class="suite">%s%s</p>\n</article>'
                 % (reste, bouton("index.html", "Manipuler la planche interactive", "btn encre"),
                    bouton("demonstration.html", "Lire la démonstration")))
        page(dos + "article.html", titre_art, p["resume"], entete_pilier(p, "article.html", t(titre_art), texte), corps, base_js,
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
        avis = typo(AVIS % (AVIS_MOT if "tableau plat" in demo else ""))
        corps = ('<article class="prose">\n%s\n%s\n<p class="suite">%s%s</p>\n</article>'
                 % (avis, reste, bouton("index.html", "Manipuler la planche interactive", "btn encre"),
                    bouton("article.html", "Lire l'article")))
        page(dos + "demonstration.html", titre_demo, p["resume"], entete_pilier(p, "demonstration.html", t(titre_demo), texte),
             corps, base_js + KATEX_JS, cart(p["objet"], "Vue", "Démonstration mathématique", date), "p-demo",
             pilier=p, vue="demonstration.html", tete=KATEX, bas=pagination(p, "demonstration.html"))

    # 4. page d'accueil
    planches = []
    for p in PILIERS:
        planches.append(typo(
            '<article class="plk"><div class="no"><span class="num">Pilier</span><b>%02d</b></div>'
            '<div class="plt"><span class="eyebrow">%s</span><h3><a href="pilier-%d/index.html">%s</a></h3><p>%s</p>'
            '<p class="acces">%s<a href="pilier-%d/article.html">Article</a><a href="pilier-%d/demonstration.html">Démonstration</a></p></div>'
            '<div class="vis"><div class="cadre">%s</div><p class="clef"><b>%s</b><span>%s</span></p></div></article>'
            % (p["n"], e(p["objet"]), p["n"], e(p["titre"]), e(p["resume"]),
               bouton("pilier-%d/index.html" % p["n"], "Planche interactive", "btn encre"), p["n"], p["n"],
               VIGNETTES[p["n"]], p["clef"][0], e(p["clef"][1]))))
    docs = [("Dossier mathématique complet", "dossier.html", PDF_DOSSIER, DOSSIER)] + [
        ("Article du pilier %d — %s" % (p["n"], p["article"]), "pilier-%d/article.html" % p["n"],
         "documents/%s.pdf" % url(p["article"]), p["article"]) for p in PILIERS]
    rangs = "".join(
        '<tr><td>%s</td><td><a href="%s">Lire</a></td><td><a href="%s">PDF</a></td><td><a href="documents/%s.docx">Word</a></td>'
        '<td><a href="documents/%s.md">Markdown</a></td></tr>' % (e(nom), web, pdf, url(f), url(f)) for nom, web, pdf, f in docs)
    haut = ('<header class="plan accueil"><div class="dedans hero">\n<div>\n<p class="repere"><span>Modèle de %s</span><span>Cinq piliers</span></p>\n'
            '<h1><span>Actuel,</span> <span>Émergent,</span> <span>Local</span></h1>\n<p class="chapeau">%s</p>\n'
            '<p class="actions">%s%s</p>\n</div>\n'
            '<figure class="expo">\n<div class="plaque" role="img" aria-label="Des impacts de photons s\'accumulent sur un écran et dessinent peu à peu des bandes">'
            '<canvas id="expo-a"></canvas><canvas id="expo-b"></canvas>'
            '<span class="pl-t">Écran de détection</span><span class="pl-n">Photons détectés<b id="expo-n">0</b></span></div>\n'
            '<figcaption>Chaque point est l\'arrivée d\'un photon : un lieu, un instant. Aucun ne dessine les bandes. '
            'Elles n\'apparaissent qu\'avec le nombre. <button class="lien" id="expo-re" type="button">Recommencer</button></figcaption>\n'
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

<section aria-labelledby="h-verdict">
  <span class="eyebrow">Verdict</span>
  <h2 id="h-verdict">Ce que les équations confirment, et ce qu'elles corrigent</h2>
  <div class="verdict">
    <p>Le dossier part des formules que l'auteur proposait à partir de ses intuitions. Il les démontre ou les corrige une à une.</p>
%s
  </div>
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
  <div class="tablewrap"><table class="data">
    <thead><tr><th>Document</th><th>En ligne</th><th colspan="3">À télécharger</th></tr></thead>
    <tbody>%s</tbody>
  </table></div>
  <p class="fnote">Le PDF du dossier est produit à partir de ce site : les formules y sont composées. Dans ses versions Word et Markdown, elles restent écrites en code LaTeX.</p>
</section>""") % ("\n".join(planches), md_html(intro, "accueil"), md_html(sections.get("Synthèse", "").strip(), "accueil"), rangs)
    page("index.html", NOM,
         "Cinq intuitions sur la lumière, la gravité et la mesure, traduites en équations et confrontées à la physique établie.",
         haut, corps, base_js + "\n" + accueil_js, cart("Page de garde", "Contenu", "5 planches · 5 articles · 5 démonstrations", date),
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
    table = '<nav class="toc" aria-label="Sommaire du dossier"><span class="eyebrow">Sommaire</span><ol>%s</ol></nav>' % "".join(sommaire)
    h = h.replace('<h2 id="pilier-1">', table + '\n<h2 id="pilier-1">', 1)
    corps = '<article class="prose dossier">\n%s\n%s\n</article>' % (typo(AVIS % AVIS_MOT), h)
    haut = entete(["Dossier complet", "Cinq démonstrations, synthèse, références"], t(DOSSIER), texte,
                  suite='<p class="actions">%s</p>\n' % bouton(PDF_DOSSIER, "Télécharger le PDF", "btn plein"))
    page("dossier.html", DOSSIER, "Les cinq démonstrations du modèle, la synthèse et les références, sur une seule page.",
         haut, corps, base_js + KATEX_JS, cart("Les cinq piliers", "Vue", "Dossier complet", date), "p-dossier", tete=KATEX)

    # 6. page d'erreur : les liens partent de la racine du site, où que se trouve l'adresse fautive
    liste = "".join('<li><a href="pilier-%d/index.html">Pilier %d — %s</a></li>' % (p["n"], p["n"], t(p["titre"])) for p in PILIERS)
    corps = ('<section><span class="eyebrow">Par où continuer</span><h2>Les cinq piliers</h2>\n<div class="prose large"><ul>%s'
             '<li><a href="dossier.html">Le dossier complet</a></li></ul></div></section>' % liste)
    haut = entete(["Erreur 404"], "Cette page n'existe pas", "L'adresse a peut-être changé. Les cinq piliers, eux, n'ont pas bougé.",
                  suite='<p class="actions">%s</p>\n' % bouton("index.html", "Revenir à l'accueil", "btn plein"))
    page("404.html", "Page introuvable", "Cette page n'existe pas.", haut, corps, base_js,
         cart("Page introuvable", "Vue", "Erreur 404", date), "p-404",
         tete='<base href="%s">\n<meta name="robots" content="noindex">\n' % urllib.parse.urlparse(SITE).path)

    if "--pdf" in sys.argv:
        nav = navigateur()
        if nav:
            pdf_dossier(nav)
            image_partage(nav, css, base_js + "\n" + accueil_js)
        else:
            print("  PDF et image de partage non produits : ni Edge ni Chrome trouvés sur cette machine")
    verifier_liens()


def verifier_liens():
    """Chaque lien interne doit pointer vers un fichier présent."""
    manquants = 0
    for dossier, _, fichiers in os.walk(RACINE):
        if any(x in dossier for x in (".git", "outils")):
            continue
        for f in fichiers:
            if not f.endswith(".html"):
                continue
            src = lire(os.path.join(dossier, f))
            for cible in re.findall(r'href="([^"#]+)"', src):
                if re.match(r"^(https?:|mailto:|/)", cible):
                    continue
                chemin = os.path.normpath(os.path.join(dossier, urllib.parse.unquote(cible)))
                if not os.path.exists(chemin):
                    manquants += 1
                    print("  LIEN CASSÉ dans %s : %s" % (os.path.relpath(os.path.join(dossier, f), RACINE), cible))
    print("Liens internes :", "tous valides" if not manquants else "%d cassés" % manquants)


if __name__ == "__main__":
    main()
