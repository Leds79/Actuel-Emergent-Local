# -*- coding: utf-8 -*-
"""Contrôle du site publié : chaque fichier suivi par git doit être servi en ligne, à l'identique de la copie locale.

Usage : python outils/controle/en_ligne.py [adresse du site]
À lancer une minute après `git push`. Juste après une publication, le site peut répondre de façon incomplète
pendant quelques secondes : en cas d'écart, relancer avant de conclure.
"""
import hashlib
import os
import subprocess
import sys
import urllib.error
import urllib.request

ICI = os.path.dirname(os.path.abspath(__file__))
DEPOT = os.path.dirname(os.path.dirname(ICI))
SITE = "https://leds79.github.io/Actuel-Emergent-Local/"
PUBLIES = (".html", ".pdf", ".docx", ".md", ".png", ".svg", ".xml")
A_PART = ("CLAUDE.md", "SUIVI.md", "README.md", "404.html")


def lire(adresse):
    requete = urllib.request.Request(adresse, headers={"User-Agent": "controle-du-site", "Cache-Control": "no-cache"})
    try:
        with urllib.request.urlopen(requete, timeout=40) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except urllib.error.URLError as e:
        return 0, str(e.reason).encode("utf-8")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    site = (sys.argv[1] if len(sys.argv) > 1 else SITE).rstrip("/") + "/"
    suivis = subprocess.run(["git", "-c", "core.quotepath=off", "ls-files"], cwd=DEPOT, capture_output=True, check=True).stdout.decode("utf-8").split("\n")
    fichiers = [f for f in suivis if f.endswith(PUBLIES) and not f.startswith("outils/") and f not in A_PART]
    ecarts = 0
    for f in fichiers:
        with open(os.path.join(DEPOT, f), "rb") as local:
            attendu = local.read()
        code, recu = lire(site + f)
        # git peut convertir les fins de ligne d'un texte : on compare sans elles
        pareil = code == 200 and (recu == attendu or recu.replace(b"\r\n", b"\n") == attendu.replace(b"\r\n", b"\n"))
        ecarts += not pareil
        print("%s %-62s %3d  %8d octets  %s" % ("ok   " if pareil else "ÉCART", f, code, len(recu), hashlib.sha256(recu).hexdigest()[:10]))
    # une adresse de dossier sert son index.html ; une adresse inconnue sert la page d'erreur
    for dossier in [""] + sorted({f.rsplit("/", 1)[0] + "/" for f in fichiers if f.endswith("/index.html")}):
        code, recu = lire(site + dossier)
        with open(os.path.join(DEPOT, dossier, "index.html"), "rb") as local:
            pareil = code == 200 and recu.replace(b"\r\n", b"\n") == local.read().replace(b"\r\n", b"\n")
        ecarts += not pareil
        print("%s %-62s %3d" % ("ok   " if pareil else "ÉCART", dossier or "(accueil)", code))
    code, recu = lire(site + "cette-page-n-existe-pas")
    print("%s page inconnue : code %d (404 attendu), page d'erreur %s" % (
        "ok   " if code == 404 and b"Cette page n" in recu else "ÉCART", code, "servie" if b"Cette page n" in recu else "absente"))
    ecarts += not (code == 404 and b"Cette page n" in recu)
    print("SITE CONFORME : %d fichiers identiques à la copie locale" % len(fichiers) if not ecarts else "%d ÉCART(S) : relancer dans une minute avant de conclure" % ecarts)
    sys.exit(1 if ecarts else 0)


if __name__ == "__main__":
    main()
