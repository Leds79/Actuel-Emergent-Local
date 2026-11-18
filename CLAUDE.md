# Projet « Actuel, Émergent, Local »

Guide de reprise. Claude lit ce fichier au début de chaque session ouverte dans ce dossier.
Il décrit ce qui change peu : le projet, ses règles, son organisation.
L'avancement, les décisions en attente et la suite sont dans `SUIVI.md`, à lire juste après.

## Le projet

Sylvain Leduc a formulé cinq intuitions sur la lumière, la gravité et la mesure, à partir de ses réflexes de suivi de projet.
Ce dépôt contient leur mise en équations (le dossier), cinq articles de vulgarisation, cinq planches interactives,
et le site qui réunit le tout : https://leds79.github.io/Actuel-Emergent-Local/

| Pilier | Intuition de départ | Ce que la physique précise ou corrige |
| --- | --- | --- |
| 1 | L'observateur tient les ciseaux : le photon doit revenir. Sur un tableau plat, la diagonale s'allonge, comme entre deux miroirs face à face. | c/2 est un plancher dans l'exemple chiffré ; un plafond seulement pour un balayage lent. |
| 2 | La lumière est transparente en chemin. Elle est actuelle, émergente, locale. Le langage qui la décrit est obsolète. | En transit elle porte de l'énergie : « potentiel » ne veut pas dire « rien ». |
| 3 | Tout tourne à la vitesse de la lumière ; les corps lourds ralentissent leur environnement. | Sur place rien ne ralentit ; un facteur 2 sépare la lumière de la matière lente. |
| 4 | Refus du cadre « une route ou deux ». Qui dit choix dit intention ; le réel est graduellement donné. | Le choix n'exige pas d'intention consciente ; les lectures participatives sont des interprétations. |
| 5 | La question est un potentiel ; actualiser, c'est cristalliser l'information. | Inscrire (réversible) et cristalliser (irréversible en pratique) sont deux temps distincts. |

Verdict d'ensemble, à ne jamais gonfler : le modèle est une relecture cohérente de résultats connus.
Il ne prédit rien que la relativité et la mécanique quantique standard ne prédisent déjà.

## Règles de travail

1. **Langue.** Français, tutoiement, phrases courtes. Les commandes destinées à l'auteur sont en PowerShell.
2. **Son idée d'abord.** Tout texte sur un pilier commence par l'intuition de l'auteur, avec ses mots, puis dit ce que la physique en confirme ou en corrige. Ses formulations sont dans `INTUITIONS` (`outils/construire_site.py`) et, en entier, dans `prive/conversation-d-origine.md`. Garder ses images : goulot d'étranglement, délais en série, boucle de retour vers l'observateur, zone rapide et zone ralentie, « tout tourne à la vitesse de la lumière ».
3. **Exactitude.** Citer l'idée, puis poser la nuance. Ne pas affirmer plus que le dossier. Toute référence est contrôlée sur sa source avant d'être citée. Présentation humble.
4. **Présentation.** Le site doit être frappant, attrayant et professionnel, sans perdre son identité : plan bleu de chantier, feuille de dessin, cartouche. Les images des dessins animés viennent de l'auteur (voir plus bas) : les conserver.
5. **Vérifier comme un visiteur.** Avant de dire qu'un travail est fini : largeur de téléphone (390 px), bas de chaque type de page, mode sombre, fichiers proposés au téléchargement réellement ouverts. Dire ce qui a été vérifié et ce qui ne l'a pas été.
6. **Vie privée.** Le dépôt est public. Ne rien y mettre de personnel. Le dossier `prive/` n'est jamais publié.
7. **Mémoire du projet.** À la fin de chaque séance, mettre à jour `SUIVI.md` ; modifier ce guide seulement si une règle ou l'organisation change.

## D'où vient le contenu

Chaîne : documents Claude (source de vérité) → exports dans `documents/` → pages générées.

| Document | Lien (privé, seul l'auteur peut l'ouvrir) |
| --- | --- |
| Dossier de formalisation | https://claude.ai/artifact/4ZtY3d2RwEVQGYMST5XD2r |
| Article 1 | https://claude.ai/artifact/S9XeQq59ncjWbsqAb2BPQP |
| Article 2 | https://claude.ai/artifact/YEjHcNgNhtbPRzWdHrZUJ4 |
| Article 3 | https://claude.ai/artifact/Vm6NgupaPcoyx4RZMwAHwt |
| Article 4 | https://claude.ai/artifact/78b9FAVZcR9yRU4oXTfpyx |
| Article 5 | https://claude.ai/artifact/RcmHSTG2bYS2WtFscNFwJG |

Pour changer un texte :

1. Modifier le document Claude avec le connecteur Claude Docs (recherche et remplacement par citation exacte, ou remplacement d'un bloc).
2. Refaire les trois exports dans `documents/` : appliquer la même modification au `.md` ; pour le `.pdf` et le `.docx`, utiliser l'outil `export` du connecteur, dont le résultat (base64) est enregistré dans un fichier qu'un script Python décode.
3. Reconstruire le site, contrôler, publier.

Les exports PDF et Word du **dossier** affichent les formules en code LaTeX brut. La version lisible est `dossier-complet.pdf`, produite par le générateur.

## Organisation du dépôt

- `index.html`, `dossier.html`, `404.html`, `pilier-N/{index,article,demonstration}.html` : pages **générées**, à ne jamais modifier à la main.
- `documents/` : exports des six documents (Markdown, PDF, Word).
- `outils/construire_site.py` : le générateur. `outils/figures.py` : figures statiques des articles, marque du site.
- `outils/gabarits/base.css`, `base.js` : style et script communs. `accueil.js` : écran de détection et frise de l'accueil. `epures.js` : les cinq dessins animés. `pN.frag.html` : les cinq planches interactives.
- `dossier-complet.pdf`, `apercu.png` : produits avec l'option `--pdf`.
- `prive/` : hors dépôt. Contient la conversation d'origine de l'auteur.

Les cinq dessins animés (`epures.js`), dont les images ont été choisies par l'auteur :

1. l'ombre des ciseaux sur le tableau, vue de face, qui se referme avec un décalage ; en pointillé, ce que voit celui qui tient les ciseaux ;
2. le mot « rayon », barré dans les limites de sa définition, au-dessus du fait ;
3. la toile de l'espace-temps, ses galaxies, et le trou noir qui l'étire et la ralentit ;
4. le sablier de la connaissance : les grains tombent un à un, aucun ne remonte ;
5. le flocon de neige fractal qui pousse à partir d'un germe.

Chaque dessin est une fonction du temps seul. Ajouter `#fige=4.5` à l'adresse d'une page arrête tous les dessins sur cet instant, ce qui permet de les capturer.

## Construire, contrôler, publier

```powershell
cd C:\Users\ThinkPad\Downloads\Philo
python outils\construire_site.py          # pages seulement
python outils\construire_site.py --pdf    # refait aussi dossier-complet.pdf et apercu.png (Edge ou Chrome, Internet)
git add -A
git commit -m "Message"
git push
```

Le générateur vérifie les liens internes. Le site se met à jour environ une minute après `git push`.

Le dépôt appartient au compte GitHub `Leds79`. Avant de pousser, vérifier le compte actif avec `gh auth status` ; au besoin, `gh auth switch --user Leds79`. L'identité git de ce dossier est réglée localement sur l'adresse `noreply` de ce compte.

## Pièges déjà rencontrés

- Dans l'outil Bash, un script passé en ligne perd un niveau de barres obliques inverses : écrire les scripts dans un fichier.
- KaTeX refuse `\vec{r}\,'` ; écrire `\vec{r}^{\,\prime}`.
- Le navigateur sans interface ne descend pas sous 500 px de large : pour 390 px, charger la page dans un cadre de cette largeur.
- En temps virtuel, `requestAnimationFrame` ne tourne presque pas : pour tester une animation, le remplacer par une minuterie dans une copie de la page.
- Juste après une publication, le site peut répondre de façon incomplète pendant quelques secondes : relancer le contrôle avant de conclure.
