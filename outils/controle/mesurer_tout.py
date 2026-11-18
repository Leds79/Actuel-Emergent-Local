# -*- coding: utf-8 -*-
"""Mesure toutes les pages du site à plusieurs largeurs et signale ce qui déborde : la page, un tableau, une figure,
un élément qui dépasse le bord droit, une erreur de script. Une formule qui défile encore après réduction est comptée à part.

Usage : python outils/controle/mesurer_tout.py [largeurs] [pages]
  largeurs : par défaut 320,360,390,768,1280
  pages    : par défaut toutes ; sinon une liste séparée par des virgules, par exemple index.html,pilier-4/index.html
Compter une dizaine de secondes par mesure. Le site mesuré est la version locale : reconstruire d'abord.
"""
import json
import sys

import capture

PAGES = ["index.html", "dossier.html", "404.html"] + ["pilier-%d/%s" % (n, v) for n in range(1, 6)
                                                       for v in ("index.html", "article.html", "demonstration.html")]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    largeurs = [int(x) for x in (sys.argv[1] if len(sys.argv) > 1 else "320,360,390,768,1280").split(",")]
    pages = sys.argv[2].replace(chr(92), "/").split(",") if len(sys.argv) > 2 else PAGES
    nav = capture.navigateur()
    if not nav:
        sys.exit("Arrêt : ni Edge ni Chrome trouvés sur cette machine.")
    capture.assurer_serveur()
    anomalies = 0
    for page in pages:
        for w in largeurs:
            m = capture.mesurer(nav, page, w=w, js="debords.js", budget=12000)
            if not m or not m.get("extra"):
                anomalies += 1
                print("ÉCHEC    %-28s %5d : pas de mesure" % (page, w), flush=True)
                continue
            x = m["extra"]
            mal = m["debord"] or x["page"] or x["tableaux"] or x["figures"] or x["depasse"] or x["marqueAbregee"] or m["erreurs"]
            anomalies += bool(mal)
            print("%s %-28s %5d  hauteur %6d  formules qui défilent %2d%s" % (
                "ANOMALIE" if mal else "ok      ", page, w, m["hauteur"], len(x["formules"]),
                "  " + json.dumps(dict(x, erreurs=m["erreurs"]), ensure_ascii=False) if mal else ""), flush=True)
    print("TERMINÉ : %d anomalie(s) sur %d mesures" % (anomalies, len(pages) * len(largeurs)), flush=True)
    sys.exit(1 if anomalies else 0)


if __name__ == "__main__":
    main()
