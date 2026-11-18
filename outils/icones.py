# -*- coding: utf-8 -*-
"""Produit les icônes PNG du site à partir du dessin de la marque (une source, trois rayons, un écran plat).

Safari n'affiche pas les icônes SVG : il lui faut un PNG, et une icône de 180 px pour l'écran d'accueil d'un iPhone.
Usage : python outils/icones.py        (nécessite le module Pillow ; à relancer seulement si la marque change)
"""
import os

from PIL import Image, ImageDraw

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAN, ENCRE, PHOTON = (15, 44, 86), (243, 246, 251), (255, 239, 196)


def icone(taille, marge=0.0):
    """Dessine la marque sur une grille de 32 unités, huit fois trop grande, puis la réduit pour lisser les traits."""
    k = 8
    n = taille * k
    u = n * (1 - 2 * marge) / 32.0
    d = n * marge
    im = Image.new("RGB", (n, n), PLAN)
    g = ImageDraw.Draw(im)

    def p(x, y):
        return (d + x * u, d + y * u)
    for x in (7.5, 16, 24.5):
        g.line([p(16, 25), p(x, 8.5)], fill=PHOTON, width=max(1, int(round(2 * u))))
    g.line([p(5, 8.5), p(27, 8.5)], fill=ENCRE, width=max(1, int(round(2.6 * u))))
    cx, cy = p(16, 25)
    r = 2.8 * u
    g.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ENCRE)
    return im.resize((taille, taille), Image.LANCZOS)


if __name__ == "__main__":
    icone(32).save(os.path.join(RACINE, "favicon-32.png"))
    icone(180, marge=0.12).save(os.path.join(RACINE, "apple-touch-icon.png"))
    print("icônes écrites : favicon-32.png, apple-touch-icon.png")
