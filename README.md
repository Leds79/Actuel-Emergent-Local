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
| 4 | Le choix d'aujourd'hui ne réécrit pas le passé | Choix retardé de Wheeler, réel « graduellement donné » |
| 5 | Comment une réponse devient un fait | Cristallisation de l'information : inscription, puis décohérence |

Chaque pilier se lit de trois façons : une **planche interactive** (figure à manipuler, formules, chiffres clés), un **article** sans équation, et une **démonstration** mathématique complète avec ses références.

## Contenu du dépôt

- `index.html` : page d'accueil (sommaire, verdict, synthèse, téléchargements).
- `pilier-1/` à `pilier-5/` : pour chaque pilier, `index.html` (planche interactive), `article.html` et `demonstration.html`.
- `dossier.html` : le dossier complet sur une seule page (cinq démonstrations, synthèse, références).
- `dossier-complet.pdf` : le même dossier en PDF, avec les formules composées.
- `apercu.png`, `favicon.svg`, `favicon-32.png`, `apple-touch-icon.png`, `404.html`, `sitemap.xml` : l'image affichée quand le lien est partagé, les icônes, la page d'erreur et le plan du site.
- `documents/` : les exports d'origine du dossier et des cinq articles, en PDF, Word et Markdown. Dans les exports du dossier, les formules sont écrites en code LaTeX ; pour le lire, préférer `dossier-complet.pdf`.
- `CLAUDE.md`, `SUIVI.md` : le guide de reprise et le suivi du projet, pour continuer le travail d'une séance à l'autre.
- `outils/` : le générateur du site (`construire_site.py`, `figures.py`, `icones.py`) et ses gabarits : la feuille de style, les scripts communs, l'animation de l'accueil (`accueil.js`), les cinq dessins animés des en-têtes (`epures.js`) et les cinq planches interactives (`p1` à `p5`). Le sous-dossier `controle/` réunit les outils de vérification : capture d'une page à la largeur d'un téléphone, recherche des débordements, comparaison du site publié avec la copie locale.

## Reconstruire le site

Les pages sont générées à partir des fichiers Markdown de `documents/` et des gabarits de `outils/gabarits/`. Il ne faut donc pas les modifier à la main.

```
pip install markdown
python outils/construire_site.py
```

Pour refaire aussi le PDF du dossier et l'image de partage, ajouter l'option `--pdf`. Elle demande Microsoft Edge ou Google Chrome, et une connexion Internet.

```
python outils/construire_site.py --pdf
```

Après la modification d'un document, remplacer son export `.md` dans `documents/` en gardant le même nom de fichier, relancer la commande, puis publier les fichiers générés.

## Statut du modèle

Une fois les corrections faites, le modèle ne contredit aucun résultat établi : il reformule des résultats connus en langage de flux et de délais. Il ne prédit rien que la relativité et la mécanique quantique standard ne prédisent déjà.
