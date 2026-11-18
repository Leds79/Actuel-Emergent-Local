# -*- coding: utf-8 -*-
"""Construit le site statique du modèle « Actuel, Émergent, Local ».

Sources : documents/*.md (exports des documents) et outils/gabarits/ (styles, scripts, planches interactives).
Sorties : index.html et pilier-N/{index,article,demonstration}.html, à la racine du dépôt.
Usage   : python outils/construire_site.py
          (nécessite le module Python « markdown » : pip install markdown)
"""
import html
import io
import os
import re
import sys
import urllib.parse

import markdown

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figures import FIGURES, VIGNETTES  # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAB = os.path.join(RACINE, "outils", "gabarits")
DOCS = os.path.join(RACINE, "documents")
AUTEUR = "Sylvain Leduc"
DOSSIER = "Formalisation du modèle « Actuel, Émergent, Local »"
LIEN_DOSSIER_PRIVE = "https://claude.ai/artifact/4ZtY3d2RwEVQGYMST5XD2r"

PILIERS = [
    dict(n=1, titre="L'ombre plus rapide que la lumière", objet="Géométrie de l'observateur", echelle="1 px = 400 000 km",
         article="L'ombre plus rapide que la lumière, vue par celui qui tient les ciseaux",
         resume="Sur un écran plat, l'ombre des ciseaux part de 524 fois la vitesse de la lumière et retombe vers c. "
                "Celui qui tient les ciseaux la voit tendre vers c/2."),
    dict(n=2, titre="On ne voit jamais la lumière passer", objet="Lumière actuelle, émergente, locale", echelle="Schémas de principe",
         article="On ne voit jamais la lumière passer",
         resume="Un faisceau qui traverse le vide est invisible de côté. La lumière ne se manifeste qu'à l'endroit "
                "et à l'instant où elle rencontre de la matière."),
    dict(n=3, titre="La pente du temps", objet="Cadence c et masse comme frein", echelle="Schémas de principe",
         article="Tomber, c'est suivre la pente du temps",
         resume="Près d'une masse, les horloges battent plus lentement. La pesanteur est la pente de ce ralentissement, "
                "multipliée par c²."),
    dict(n=4, titre="Le choix qui ne réécrit pas le passé", objet="Choix retardé de Wheeler", echelle="Schémas de principe",
         article="Le choix d'aujourd'hui ne réécrit pas le passé",
         resume="Choisir aujourd'hui comment mesurer un photon ne change rien à ce qu'il a fait. Entre « une route » "
                "et « deux routes », tous les intermédiaires existent."),
    dict(n=5, titre="Comment une réponse devient un fait", objet="Cristallisation de l'information", echelle="Schémas de principe",
         article="Comment une réponse devient un fait",
         resume="La réponse est d'abord inscrite au crayon, encore effaçable. L'environnement la recopie ensuite "
                "des milliards de fois et la grave."),
]
VUES = [("index.html", "Planche interactive"), ("article.html", "Article"), ("demonstration.html", "Démonstration")]
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
});
"""

GABARIT = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%%TITRE%%</title>
<meta name="description" content="%%DESCRIPTION%%">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Serif:ital,wght@1,400;1,500&display=swap">
%%TETE%%<style>
%%CSS%%
</style>
</head>
<body>
<div class="sheet">
<header class="cartouche">
  <div class="cc"><span class="ck">Projet</span><span class="cv"><a href="%%RACINE%%index.html">Modèle «&nbsp;Actuel, Émergent, Local&nbsp;»</a></span></div>
  <div class="cc"><span class="ck">Objet</span><span class="cv">%%OBJET%%</span></div>
  <div class="cc"><span class="ck">%%CLE3%%</span><span class="cv">%%VAL3%%</span></div>
  <div class="cc"><span class="ck">Auteur</span><span class="cv">%%AUTEUR%%</span></div>
  <div class="cc"><span class="ck">Date</span><span class="cv">%%DATE%%</span></div>
  <nav class="cc" aria-label="Sommaire et piliers"><span class="ck">%%CLENAV%%</span><span class="cv planches">%%NAV%%</span></nav>
</header>
%%ONGLETS%%<main>
%%CORPS%%
</main>
<footer>
%%PIED%%
</footer>
</div>
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


INSECABLES = (("« ", "« "), (" »", " »"), (" :", " :"), (" ;", " ;"), (" ?", " ?"), (" !", " !"), (" %", " %"))


def typo(fragment):
    """Espaces insécables de la typographie française, dans les textes seulement (pas dans les balises)."""
    def f(m):
        t = m.group(1)
        for a, b in INSECABLES:
            t = t.replace(a, b)
        return ">" + t + "<"
    return re.sub(r">([^<]+)<", f, fragment)


def date_fr(md):
    m = re.search(r"^([A-Z][a-z]{2}) (\d{1,2}), (\d{4}) ·", md, flags=re.M)
    return "%d %s %s" % (int(m.group(2)), MOIS[m.group(1)], m.group(3)) if m else ""


def figure(legende, vue):
    for debut, v, titre, svg in FIGURES:
        if legende.startswith(debut) and v in (None, vue):
            return ('<figure class="fig solo"><figcaption class="figtitle">%s</figcaption><div class="stage">%s</div></figure>'
                    % (e(titre), svg))
    return '<p class="fnote">Figure : %s. Voir la planche interactive.</p>' % e(legende)


def tableau(m):
    """Habille un tableau : sur petit écran, un tableau de texte long s'empile, un tableau large défile."""
    corps = m.group(1)
    titres = [re.sub(r"<[^>]+>", "", t).strip() for t in re.findall(r"<th[^>]*>(.*?)</th>", corps, flags=re.S)]
    cellules = re.findall(r"<td[^>]*>(.*?)</td>", corps, flags=re.S)
    classe = "data"
    if len(titres) >= 3 and any(len(re.sub(r"<[^>]+>", "", c)) > 140 for c in cellules):
        classe = "data empile"
        rang = [0]

        def etiquette(mm):
            titre = titres[rang[0] % len(titres)]
            rang[0] += 1
            return '<td data-th="%s"%s>' % (html.escape(html.unescape(titre), quote=True), mm.group(1))
        corps = re.sub(r"<td([^>]*)>", etiquette, corps)
    elif len(titres) >= 4:
        classe = "data large c%d" % len(titres)
    return '<div class="tablewrap"><table class="%s">%s</table></div>' % (classe, corps)


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
    h = typo(h)
    h = re.sub(r"<p>FIGURE(\d+)FIN</p>", lambda m: figure(figs[int(m.group(1))], vue), h)
    h = re.sub(r"<p>FORMULE(\d+)FIN</p>", lambda m: '<div class="tex">%s</div>' % html.escape(texs[int(m.group(1))]), h)
    return h


def page(relatif, titre, description, objet, cle3, val3, date, corps, pied, js, pilier=None, vue=None, tete=""):
    racine = "../" if pilier else ""
    fichier = vue or "index.html"
    nav = ['<a class="som" href="%sindex.html"%s>Sommaire</a>' % (racine, "" if pilier else ' aria-current="page"')]
    for p in PILIERS:
        nav.append('<a href="%spilier-%d/%s"%s title="%s">%d</a>' % (
            racine, p["n"], fichier, ' aria-current="page"' if pilier and p["n"] == pilier["n"] else "", e(p["titre"]), p["n"]))
    onglets = ""
    if pilier:
        onglets = '<nav class="vues" aria-label="Trois façons de lire ce pilier">%s</nav>\n' % "".join(
            '<a href="%s"%s>%s</a>' % (f, ' aria-current="page"' if f == vue else "", nom) for f, nom in VUES)
    doc = (GABARIT.replace("%%TITRE%%", e(titre)).replace("%%DESCRIPTION%%", e(description))
           .replace("%%TETE%%", tete).replace("%%RACINE%%", racine).replace("%%OBJET%%", e(objet))
           .replace("%%CLE3%%", e(cle3)).replace("%%VAL3%%", e(val3)).replace("%%AUTEUR%%", AUTEUR).replace("%%DATE%%", e(date))
           .replace("%%CLENAV%%", "Pilier %d / 5" % pilier["n"] if pilier else "Piliers")
           .replace("%%NAV%%", "".join(nav)).replace("%%ONGLETS%%", onglets).replace("%%PIED%%", pied)
           .replace("%%CSS%%", lire(os.path.join(GAB, "base.css"))).replace("%%JS%%", js).replace("%%CORPS%%", corps))
    ecrire(relatif, doc)


def pied_pilier(p):
    return ('  <span>Pilier %d sur 5 · %s</span>\n'
            '  <a href="../documents/%s.pdf">Article en PDF</a>\n'
            '  <a href="../documents/%s.pdf">Dossier complet en PDF</a>\n'
            '  <a href="../index.html">Sommaire</a>' % (p["n"], e(p["objet"]), url(p["article"]), url(DOSSIER)))


# ---------------------------------------------------------------- construction
def main():
    base_js = lire(os.path.join(GAB, "base.js"))
    dossier = lire(os.path.join(DOCS, DOSSIER + ".md"))
    date = date_fr(dossier)
    morceaux = re.split(r"^## (.+)$", dossier, flags=re.M)
    intro = re.sub(r"^# .*$", "", morceaux[0], count=1, flags=re.M)
    intro = re.sub(r"^[A-Z][a-z]{2} \d{1,2}, \d{4} ·.*$", "", intro, count=1, flags=re.M).strip()
    sections = {morceaux[i].strip(): morceaux[i + 1] for i in range(1, len(morceaux), 2)}
    refs = sections.get("Références", "")
    print("Site « Actuel, Émergent, Local » — sources du", date)

    for p in PILIERS:
        n, dos = p["n"], "pilier-%d/" % p["n"]

        # 1. planche interactive
        corps, script = lire(os.path.join(GAB, "p%d.frag.html" % n)).split("<!--SCRIPT-->")
        for a, b in (("« ", "«&nbsp;"), (" »", "&nbsp;»"), (" :", "&nbsp;:"), (" ;", "&nbsp;;"), (" ?", "&nbsp;?"), (" !", "&nbsp;!")):
            corps = corps.replace(a, b)
        page(dos + "index.html", p["titre"], p["resume"], p["objet"], "Échelle", p["echelle"], date, corps.strip(),
             pied_pilier(p), base_js + "\n" + script.strip(), pilier=p, vue="index.html")

        # 2. article de vulgarisation
        art = lire(os.path.join(DOCS, p["article"] + ".md"))
        titre_art = re.search(r"^# (.+)$", art, flags=re.M).group(1).strip()
        date_art = date_fr(art) or date
        art = re.sub(r"^# .*$", "", art, count=1, flags=re.M)
        art = re.sub(r"^[A-Z][a-z]{2} \d{1,2}, \d{4} ·.*$", "", art, count=1, flags=re.M)
        art = art.replace(LIEN_DOSSIER_PRIVE, "demonstration.html")
        corps = ('<article class="prose">\n<div class="head"><span class="eyebrow">Article · pilier %d</span><h1>%s</h1></div>\n%s\n'
                 '<p class="suite"><a href="index.html">Manipuler la planche interactive</a> · '
                 '<a href="demonstration.html">Lire la démonstration</a></p>\n</article>'
                 % (n, typo(">" + e(titre_art) + "<")[1:-1], md_html(art.strip(), "article")))
        page(dos + "article.html", titre_art, p["resume"], p["objet"], "Vue", "Article de vulgarisation", date_art, corps,
             pied_pilier(p), base_js, pilier=p, vue="article.html")

        # 3. démonstration mathématique : la section du dossier, puis ses références
        cle = next(k for k in sections if k.startswith("Pilier %d " % n))
        titre_demo = cle.split("—", 1)[1].strip()
        demo = sections[cle].replace("\n### ", "\n## ")
        m = re.search(r"\*\*Pilier %d\*\*\s*\n\n((?:- .*(?:\n|$))+)" % n, refs)
        if m:
            demo += "\n\n## Références\n\n" + m.group(1)
        corps = ('<article class="prose">\n<div class="head"><span class="eyebrow">Démonstration · pilier %d</span><h1>%s</h1></div>\n%s\n'
                 '<p class="suite"><a href="index.html">Manipuler la planche interactive</a> · '
                 '<a href="article.html">Lire l\'article</a></p>\n</article>'
                 % (n, typo(">" + e(titre_demo) + "<")[1:-1], md_html(demo.strip(), "demonstration")))
        page(dos + "demonstration.html", "Pilier %d — %s" % (n, titre_demo), p["resume"], p["objet"], "Vue",
             "Démonstration mathématique", date, corps, pied_pilier(p), base_js + KATEX_JS, pilier=p, vue="demonstration.html", tete=KATEX)

    # 4. page d'accueil
    lignes = []
    for p in PILIERS:
        lignes.append(
            '<article class="pl">%s<div class="plt"><span class="num">Pilier %d · %s</span>'
            '<h3><a href="pilier-%d/index.html">%s</a></h3><p>%s</p></div>'
            '<div class="liens"><a href="pilier-%d/index.html">Planche interactive</a><a href="pilier-%d/article.html">Article</a>'
            '<a href="pilier-%d/demonstration.html">Démonstration</a></div></article>'
            % (VIGNETTES[p["n"]], p["n"], e(p["objet"]), p["n"], e(p["titre"]), e(p["resume"]), p["n"], p["n"], p["n"]))
    docs = [("Dossier mathématique complet", DOSSIER)] + [("Article du pilier %d — %s" % (p["n"], p["article"]), p["article"]) for p in PILIERS]
    rangs = "".join(
        '<tr><td>%s</td><td><a href="documents/%s.pdf">PDF</a></td><td><a href="documents/%s.docx">Word</a></td>'
        '<td><a href="documents/%s.md">Markdown</a></td></tr>' % (e(nom), url(f), url(f), url(f)) for nom, f in docs)
    corps = typo("""<div class="head">
  <h1>Actuel, Émergent, Local</h1>
  <p class="lead">Cinq intuitions sur la lumière, la gravité et la mesure, nées du suivi de projet : flux, délais, goulots d'étranglement. Chacune est traduite en équations, confrontée à la physique établie, puis corrigée là où il le faut.</p>
</div>

<section aria-labelledby="h-lire">
  <span class="eyebrow">Mode d'emploi</span>
  <h2 id="h-lire">Trois façons de lire chaque pilier</h2>
  <dl class="defs">
    <div><dt>Planche interactive</dt><dd>Une figure à manipuler, les formules clés, les chiffres et les corrections.</dd></div>
    <div><dt>Article</dt><dd>Le récit sans équation, pour qui découvre le sujet.</dd></div>
    <div><dt>Démonstration</dt><dd>Toutes les étapes du calcul, les conditions de validité et les références.</dd></div>
  </dl>
</section>

<section aria-labelledby="h-liste">
  <span class="eyebrow">Liste des planches</span>
  <h2 id="h-liste">Les cinq piliers</h2>
  <div class="liste">
%s
  </div>
</section>

<section aria-labelledby="h-verdict">
  <span class="eyebrow">Verdict</span>
  <h2 id="h-verdict">Ce que les équations confirment, et ce qu'elles corrigent</h2>
  <div class="prose">
%s
  </div>
</section>

<section aria-labelledby="h-synth">
  <span class="eyebrow">Synthèse</span>
  <h2 id="h-synth">Intuitions, équations, théorèmes et corrections</h2>
  <div class="prose">
%s
  </div>
</section>

<section aria-labelledby="h-docs">
  <span class="eyebrow">Documents</span>
  <h2 id="h-docs">Tout télécharger</h2>
  <div class="tablewrap"><table class="data">
    <thead><tr><th>Document</th><th colspan="3">Formats</th></tr></thead>
    <tbody>%s</tbody>
  </table></div>
</section>""") % ("\n".join(lignes), md_html(intro, "accueil"), md_html(sections.get("Synthèse", "").strip(), "accueil"), rangs)
    pied = ('  <span>Modèle « Actuel, Émergent, Local » · %s</span>\n  <a href="documents/%s.pdf">Dossier complet en PDF</a>' % (AUTEUR, url(DOSSIER)))
    page("index.html", "Actuel, Émergent, Local",
         "Cinq intuitions sur la lumière, la gravité et la mesure, traduites en équations et confrontées à la physique établie.",
         "Page de garde", "Contenu", "5 planches · 5 articles · 5 démonstrations", date, corps, pied, base_js)
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
                if re.match(r"^(https?:|mailto:)", cible):
                    continue
                chemin = os.path.normpath(os.path.join(dossier, urllib.parse.unquote(cible)))
                if not os.path.exists(chemin):
                    manquants += 1
                    print("  LIEN CASSÉ dans %s : %s" % (os.path.relpath(os.path.join(dossier, f), RACINE), cible))
    print("Liens internes :", "tous valides" if not manquants else "%d cassés" % manquants)


if __name__ == "__main__":
    main()
