# Actuel, Émergent, Local

Cinq intuitions sur la lumière, la gravité et la mesure, nées du suivi de projet (flux, délais, goulots d'étranglement). Chacune est traduite en équations, confrontée à la physique établie, puis corrigée là où il le faut.

Par Sylvain Leduc.

**Site : https://leds79.github.io/Actuel-Emergent-Local/**

## Les cinq piliers

| Pilier | Titre | Sujet |
| --- | --- | --- |
| 1 | L'ombre plus rapide que la lumière | Géométrie de l'observateur : écran plat, aller-retour du photon, limites c et c/2 |
| 2 | On ne voit jamais la lumière passer | Lumière actuelle, émergente, locale : causalité et détection |
| 3 | La pente du temps | Cadence c, masse comme frein, gravité comme réfraction |
| 4 | Le choix qui ne réécrit pas le passé | Choix retardé de Wheeler, réel « graduellement donné » |
| 5 | Comment une réponse devient un fait | Cristallisation de l'information : inscription, puis décohérence |

Chaque pilier se lit de trois façons : une **planche interactive** (figure à manipuler, formules, chiffres clés), un **article** sans équation, et une **démonstration** mathématique complète avec ses références.

## Contenu du dépôt

- `index.html` : page d'accueil (sommaire, verdict, synthèse, téléchargements).
- `pilier-1/` à `pilier-5/` : pour chaque pilier, `index.html` (planche interactive), `article.html` et `demonstration.html`.
- `dossier.html` : le dossier complet sur une seule page (cinq démonstrations, synthèse, références).
- `dossier-complet.pdf` : le même dossier en PDF, avec les formules composées.
- `documents/` : les exports d'origine du dossier et des cinq articles, en PDF, Word et Markdown. Dans les exports du dossier, les formules sont écrites en code LaTeX ; pour le lire, préférer `dossier-complet.pdf`.
- `outils/` : le générateur du site et ses gabarits.

## Reconstruire le site

Les pages sont générées à partir des fichiers Markdown de `documents/` et des gabarits de `outils/gabarits/`. Il ne faut donc pas les modifier à la main.

```
pip install markdown
python outils/construire_site.py
```

Pour refaire aussi le PDF du dossier, ajouter l'option `--pdf`. Elle demande Microsoft Edge ou Google Chrome, et une connexion Internet.

```
python outils/construire_site.py --pdf
```

Après la modification d'un document, remplacer son export `.md` dans `documents/`, relancer la commande, puis publier les fichiers générés.

## Statut du modèle

Une fois les corrections faites, le modèle ne contredit aucun résultat établi : il reformule des résultats connus en langage de flux et de délais. Il ne prédit rien que la relativité et la mécanique quantique standard ne prédisent déjà.
