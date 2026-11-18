# -*- coding: utf-8 -*-
"""Regarde une page du site comme un visiteur : capture ou mesures, à la largeur voulue (390 px par défaut).

Le navigateur sans interface ne descend pas sous 500 px de large : la page est chargée dans un cadre de la largeur demandée.

Usage : python outils/controle/capture.py <page> [sortie.png] [options]
  <page>       chemin dans le site : index.html, pilier-3/article.html, dossier.html…
  --w 390      largeur du cadre, en pixels
  --y 0 --h 0  tranche à capturer (h = 0 : toute la page ; au-delà de 16 000 px de haut, utiliser --tranche)
  --bas 1500   seulement les 1 500 derniers pixels de la page
  --tranche 3000   découpe la page en images de cette hauteur (sortie-1.png, sortie-2.png…)
  --theme dark     mode sombre
  --js debords.js  script de ce dossier exécuté dans la page avant la capture ; ce qu'il range dans window.__mesures est affiché
  --fige 4.5       instant auquel les dessins animés sont arrêtés
Sans fichier de sortie, seules les mesures sont affichées : hauteur, débordement de la page, erreurs de script.
La page regardée est celle du dépôt, servie par serveur.py (lancé au besoin) : reconstruire le site avant de contrôler.
Pour le site publié, en_ligne.py vérifie que chaque fichier servi est identique à la copie locale.
"""
import argparse
import atexit
import html
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.parse

ICI = os.path.dirname(os.path.abspath(__file__))
LOCAL = "http://127.0.0.1:8765"


def navigateur():
    candidats = [shutil.which(n) for n in ("msedge", "chrome", "google-chrome", "chromium")] + [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
    return next((c for c in candidats if c and os.path.exists(c)), None)


def assurer_serveur():
    """Lance serveur.py s'il ne tourne pas ; il s'arrête avec ce programme."""
    port = int(LOCAL.rsplit(":", 1)[1])

    def ouvert():
        with socket.socket() as s:
            s.settimeout(0.5)
            return s.connect_ex(("127.0.0.1", port)) == 0
    if ouvert():
        return
    service = subprocess.Popen([sys.executable, os.path.join(ICI, "serveur.py"), str(port)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    atexit.register(service.terminate)
    for _ in range(40):
        if ouvert():
            return
        time.sleep(0.25)
    sys.exit("Arrêt : le serveur local ne démarre pas.")


def lancer(nav, url, *options, budget=9000):
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as profil:
        r = subprocess.run([nav, "--headless=new", "--disable-gpu", "--no-first-run", "--hide-scrollbars",
                            "--user-data-dir=" + profil, "--virtual-time-budget=%d" % budget] + list(options) + [url],
                           capture_output=True, timeout=300)
    return r.stdout.decode("utf-8", "replace")


def adresse(page, w=390, y=0, h=0, theme="", js="", fige="4.5", attente=0):
    """Adresse du cadre qui charge la page."""
    page = page.replace(chr(92), "/")
    if fige and "#" not in page:
        page += "#fige=%s" % fige
    q = dict(u="/" + page.lstrip("/"), w=w, y=y, h=h)
    for cle, valeur in (("theme", theme), ("js", js), ("attente", attente)):
        if valeur:
            q[cle] = valeur
    return LOCAL + "/__o/cadre.html?" + urllib.parse.urlencode(q)


def mesurer(nav, page, essais=3, budget=9000, **options):
    """Mesures d'une page : hauteur, débordement, erreurs de script, et ce que le script --js a rangé dans window.__mesures."""
    for _ in range(essais):
        dom = lancer(nav, adresse(page, **options), "--dump-dom", "--window-size=%d,900" % max(options.get("w", 390), 520), budget=budget)
        m = re.search(r'<pre id="mesures"[^>]*>(.+?)</pre>', dom, flags=re.S)
        if m:
            return json.loads(html.unescape(m.group(1)))
    return None


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(allow_abbrev=False, description="Capture ou mesure une page du site à une largeur donnée.")
    p.add_argument("page")
    p.add_argument("sortie", nargs="?", default="")
    p.add_argument("--w", type=int, default=390)
    p.add_argument("--y", type=int, default=0)
    p.add_argument("--h", type=int, default=0)
    p.add_argument("--bas", type=int, default=0)
    p.add_argument("--tranche", type=int, default=0)
    p.add_argument("--theme", default="")
    p.add_argument("--js", default="")
    p.add_argument("--fige", default="4.5")
    p.add_argument("--attente", type=int, default=0)
    p.add_argument("--budget", type=int, default=9000)
    a = p.parse_args()
    nav = navigateur()
    if not nav:
        sys.exit("Arrêt : ni Edge ni Chrome trouvés sur cette machine.")
    assurer_serveur()
    options = dict(w=a.w, theme=a.theme, js=a.js, fige=a.fige, attente=a.attente)
    mes = mesurer(nav, a.page, budget=a.budget, **options)
    if mes is None:
        sys.exit("ÉCHEC : aucune mesure pour %s (page absente ?)" % a.page)
    print(json.dumps(mes, ensure_ascii=False))
    if not a.sortie:
        return
    from PIL import Image
    sortie, haut = os.path.abspath(a.sortie), mes["hauteur"]
    if a.bas:
        a.y, a.h = max(0, haut - a.bas), min(a.bas, haut)
    tranches = [(y, min(a.tranche, haut - y)) for y in range(0, haut, a.tranche)] if a.tranche else [(a.y, a.h or haut - a.y)]
    for i, (y, h) in enumerate(tranches):
        fichier = sortie if len(tranches) == 1 else re.sub(r"\.png$", "-%d.png" % (i + 1), sortie)
        lancer(nav, adresse(a.page, y=y, h=h, **options), "--screenshot=" + fichier,
               "--window-size=%d,%d" % (max(a.w, 520), h), budget=a.budget)
        if not os.path.exists(fichier):
            print("ÉCHEC : image non produite :", fichier)
            continue
        image = Image.open(fichier)
        image.crop((0, 0, min(a.w, image.width), min(h, image.height))).save(fichier)
        print("écrit :", fichier)


if __name__ == "__main__":
    main()
