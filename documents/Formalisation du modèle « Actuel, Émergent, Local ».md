# Formalisation du modèle « Actuel, Émergent, Local »

Nov 17, 2026 · @Sylvain Leduc

Les cinq piliers se traduisent en équations de la physique établie, et la plupart des formules demandées se démontrent telles quelles. Cinq points sont corrigés ou précisés au passage. Ils concernent le sens de la limite c/2, la formule de Glauber, le facteur 2 de la réfraction gravitationnelle, le théorème de non-communication et les deux temps de la cristallisation.

Le modèle est une relecture cohérente de résultats connus, abordés par un autre chemin : celui du suivi de projet. Il ne prédit rien que la relativité et la mécanique quantique standard ne prédisent déjà.

## Pilier 1 — La géométrie de l'observateur et le tableau plat

L'intuition est exacte : sur un tableau plat, la diagonale qui s'allonge ramène la vitesse de la tache vers c, et le trajet retour ramène la vitesse perçue vers c/2. Un seul mot est à corriger. Avec les chiffres choisis, c/2 n'est pas un plafond mais un plancher, approché par le haut.

### 1.1 Géométrie et notations

La source et l'observateur sont au même point O. Le tableau est un plan perpendiculaire à l'axe de visée, à la distance D = 10⁸ km. Un point du tableau est repéré par sa distance latérale x au centre, là où tombe l'ombre du pivot.

```latex
R(x) = \sqrt{D^2 + x^2}, \qquad \tan\theta = \frac{x}{D}, \qquad \sin\theta = \frac{x}{R}, \qquad \cos\theta = \frac{D}{R}
```

- R(x) est la diagonale : la distance réelle que la lumière parcourt de O jusqu'au point x.
- θ est l'angle entre l'axe et cette diagonale.
- τ est l'instant d'émission à la source, et ω la vitesse angulaire à laquelle la direction de l'ombre balaie le tableau.

La fermeture des ciseaux fait tourner la direction visée à vitesse angulaire constante :

```latex
\theta(\tau) = \omega\tau, \qquad x(\tau) = D\tan(\omega\tau)
```

Pour les calculs chiffrés, la fermeture en 1 s est traduite ainsi : la direction visée passe de l'axe (θ = 0) au rasant (θ = 90°) en 1 s, soit ω = π/2 rad/s. Toutes les formules restent vraies pour un ω quelconque.

Attention au sens de x(τ) : c'est le point du tableau que vise la lumière émise à l'instant τ. La tache n'y apparaît que plus tard, après le temps de trajet R/c.

La dérivée de x par rapport à τ s'obtient avec deux règles : la dérivée de tan u est 1/cos² u, et 1/cos² θ = 1 + tan² θ.

```latex
\begin{aligned}
\dot{x} \equiv \frac{dx}{d\tau} &= \frac{D\,\omega}{\cos^2(\omega\tau)} = D\,\omega\left(1 + \frac{x^2}{D^2}\right) \\
&= \frac{\omega\,(D^2 + x^2)}{D} = \frac{\omega R^2}{D}
\end{aligned}
```

**Lecture mécanique.** ẋ est la vitesse de visée : la vitesse à laquelle le point visé glisse sur le tableau. C'est une quantité purement géométrique, que rien ne limite à c. Au centre, elle vaut Dω = 1,571 × 10⁸ km/s, soit 524 fois c, et elle grandit sans borne quand la visée devient rasante.

Deux repères chiffrés servent dans toute la suite : c = 299 792,458 km/s, et D/c = 333,6 s, soit 5 min 34 s de trajet jusqu'au centre du tableau.

&#91;embedded content: géométrie du tableau plat · 3 rayons, écran sphérique en pointillé\]

Les trois rayons partent du même point O. La partie en couleur, absente sur un écran sphérique, grandit avec x : c'est elle qui retarde la tache.

### 1.2 Vitesse réelle de la tache sur le tableau

La tache dépasse largement c près du centre, puis sa vitesse retombe vers c à mesure que la diagonale s'allonge.

La lumière émise à l'instant τ atteint le tableau après avoir parcouru la diagonale R :

```latex
t_{\text{écran}}(\tau) = \tau + \frac{R\big(x(\tau)\big)}{c} = \tau + \frac{\sqrt{D^2 + x(\tau)^2}}{c}
```

On dérive par rapport à τ. La dérivée de la diagonale par rapport à x est le sinus de l'angle θ :

```latex
\begin{aligned}
\frac{dR}{dx} &= \frac{x}{\sqrt{D^2 + x^2}} = \sin\theta \\
\frac{dt_{\text{écran}}}{d\tau} &= 1 + \frac{1}{c}\,\frac{dR}{dx}\,\frac{dx}{d\tau} = 1 + \frac{\dot{x}}{c}\,\sin\theta
\end{aligned}
```

La vitesse de la tache est le rapport de deux dérivées prises par rapport au même paramètre τ :

```latex
v_{\text{écran}} = \frac{dx}{dt_{\text{écran}}} = \frac{dx/d\tau}{dt_{\text{écran}}/d\tau} = \frac{\dot{x}}{1 + \dfrac{\dot{x}}{c}\,\sin\theta}
```

C'est exactement la formule demandée. En inversant les deux membres, elle devient une addition de délais :

```latex
\frac{1}{v_{\text{écran}}} = \frac{1}{\dot{x}} + \frac{\sin\theta}{c}
\qquad\Longleftrightarrow\qquad
v_{\text{écran}} = \frac{c}{\sin\theta + \dfrac{c}{\dot{x}}}
```

**Lecture mécanique.** Les délais s'additionnent comme deux tâches en série. Pour avancer d'un kilomètre sur le tableau, il faut le temps que la source vise ce kilomètre (1/ẋ), plus le supplément de trajet dû à l'allongement de la diagonale (sin θ / c).

Près du centre, la diagonale ne s'allonge presque pas : la source donne le rythme. Loin du centre, le trajet de la lumière devient le goulot d'étranglement.

**Au centre** (θ → 0, donc sin θ → 0), le second délai disparaît :

```latex
v_{\text{écran}} \;\longrightarrow\; \dot{x}(0) = D\,\omega \approx 1{,}571 \times 10^{8}\ \text{km/s} \approx 524\,c
```

**Très loin** (x → ∞), sin θ → 1 et c/ẋ → 0 :

```latex
\lim_{x \to \infty} v_{\text{écran}} = \lim_{x \to \infty} \frac{c}{\dfrac{x}{\sqrt{D^2 + x^2}} + \dfrac{c\,D}{\omega\,(D^2 + x^2)}} = \frac{c}{1 + 0} = c
```

Pour savoir de quel côté la limite est approchée, on développe pour x ≫ D. On utilise sin θ ≈ 1 − D²/(2x²) et c/ẋ ≈ cD/(ωx²) :

```latex
v_{\text{écran}} \approx c\left[\,1 + \frac{D}{x^2}\left(\frac{D}{2} - \frac{c}{\omega}\right)\right] \qquad (x \gg D)
```

Ici D/2 = 5 × 10⁷ km dépasse largement c/ω = 1,9 × 10⁵ km : la parenthèse est positive, et la tache approche c par le haut.

Le critère exact s'obtient avec c/ẋ = (c/Dω) cos² θ et cos² θ = (1 − sin θ)(1 + sin θ) :

```latex
\begin{aligned}
v_{\text{écran}} > c \;&\iff\; \sin\theta + \frac{c}{D\omega}\cos^2\theta < 1 \\
&\iff\; \frac{c}{D\omega}\,(1 - \sin\theta)(1 + \sin\theta) < 1 - \sin\theta \\
&\iff\; 1 + \sin\theta < \frac{D\omega}{c}
\end{aligned}
```

Comme 1 + sin θ ne dépasse jamais 2, la tache est supraluminique partout dès que Dω > 2c. Ici Dω/c = 524 : la vitesse décroît de 524 c vers c sans jamais l'atteindre. Avec un balayage lent (Dω < c), la tache resterait sous c et tendrait vers c par le bas : la limite est la même dans tous les cas.

**Lecture mécanique.** Loin du centre, la tache ne peut pas distancer la lumière qui la peint. Pour un éclair instantané (ω infini), il reste v = c / sin θ : c'est la vitesse à laquelle une sphère de lumière en expansion coupe un plan.

**Contre-épreuve : l'écran sphérique.** Sur un écran courbé autour de la source, R = D est constant, donc dR/dx = 0 et le second délai n'existe pas. La tache y court à Dω partout, sans frein. La vulgarisation qui annonce « Dω » suppose donc, sans le dire, un écran courbe ou de petits angles.

### 1.3 Vitesse perçue par l'observateur : l'aller-retour du photon

La vitesse perçue tend bien vers c/2 quand la tache s'éloigne à l'infini. Avec un balayage rapide, elle y tend par le haut : c/2 est alors un plancher, pas un plafond.

Pour que l'observateur voie la tache, la lumière doit revenir du tableau jusqu'à O. Le tableau diffuse la lumière dans toutes les directions, et le chemin du retour est la même diagonale R :

```latex
t_{\text{obs}}(\tau) = \tau + \frac{2\,R\big(x(\tau)\big)}{c} = \tau + \frac{2\sqrt{D^2 + x(\tau)^2}}{c}
```

Le calcul est celui de la section 1.2, avec un facteur 2 sur la diagonale :

```latex
\begin{aligned}
\frac{dt_{\text{obs}}}{d\tau} &= 1 + \frac{2}{c}\,\frac{dR}{dx}\,\frac{dx}{d\tau} = 1 + \frac{2\,\dot{x}}{c}\,\sin\theta \\
v_{\text{obs}} &= \frac{dx}{dt_{\text{obs}}} = \frac{dx/d\tau}{dt_{\text{obs}}/d\tau} = \frac{\dot{x}}{1 + \dfrac{2\,\dot{x}}{c}\,\sin\theta}
\end{aligned}
```

C'est exactement la formule demandée. Sous forme de délais en série :

```latex
\frac{1}{v_{\text{obs}}} = \frac{1}{\dot{x}} + \frac{2\sin\theta}{c}
\qquad\Longleftrightarrow\qquad
v_{\text{obs}} = \frac{c}{2\sin\theta + \dfrac{c}{\dot{x}}}
```

**Preuve de la limite c/2.** Quand x → ∞, sin θ = x/√(D² + x²) → 1 et c/ẋ = cD/(ω(D² + x²)) → 0 :

```latex
\lim_{x \to \infty} v_{\text{obs}} = \frac{c}{2 \times 1 + 0} = \frac{c}{2} = 149\,896{,}229\ \text{km/s}
```

Cette limite ne dépend ni de ω ni de D. Le développement pour x ≫ D précise comment elle est approchée :

```latex
v_{\text{obs}} \approx \frac{c}{2}\left[\,1 + \frac{D}{2x^2}\left(D - \frac{c}{\omega}\right)\right] \qquad (x \gg D)
```

**Plancher ou plafond ?** La même méthode qu'en 1.2 donne le critère exact :

```latex
\begin{aligned}
v_{\text{obs}} > \frac{c}{2} \;&\iff\; 2\sin\theta + \frac{c}{D\omega}\cos^2\theta < 2 \\
&\iff\; \frac{c}{D\omega}\,(1 - \sin\theta)(1 + \sin\theta) < 2\,(1 - \sin\theta) \\
&\iff\; \frac{1 + \sin\theta}{2} < \frac{D\omega}{c}
\end{aligned}
```

Le membre de gauche est toujours compris entre 1/2 et 1. Trois régimes en découlent.

| Régime | Condition | Rôle de c/2 |
| --- | --- | --- |
| Balayage rapide | Dω ≥ c | Plancher : la vitesse perçue décroît de Dω vers c/2 sans jamais passer dessous |
| Balayage intermédiaire | c/2 < Dω < c | La vitesse perçue passe sous c/2, puis y remonte |
| Balayage lent | Dω ≤ c/2 | Plafond : la vitesse perçue reste sous c/2 et y tend par le bas |

Avec les chiffres du problème, Dω/c = 524 : le régime est rapide. L'observateur voit la tache démarrer à 524 c, ralentir, passer sous c vers x ≈ 57,6 millions de km (θ ≈ 30°), puis tendre vers c/2 par le haut.

**Correction du mot « plafonne ».** La limite c/2 est démontrée. Mais ici la vitesse perçue ne monte pas vers un plafond : elle descend vers un plancher. c/2 ne serait un plafond que pour un balayage lent, Dω ≤ c/2.

**Lecture mécanique.** Le retour du photon double le second délai : loin du centre, chaque kilomètre de tableau coûte presque deux kilomètres de trajet. À l'instant t, l'observateur voit ce qui se trouve sur une sphère centrée sur lui, dont le rayon grandit à c/2.

```latex
R_{\text{vu}}(t) = \frac{c\,(t - \tau)}{2}
\qquad\Longrightarrow\qquad
v_{\text{obs}} \;\xrightarrow[\;\omega \to \infty\;]{}\; \frac{c}{2\sin\theta} \;\ge\; \frac{c}{2}
```

Cette « sphère du visible » fixe le rythme loin du centre. L'analogie du tunnel entre deux miroirs est juste : chaque image plus lointaine est plus vieille d'un aller-retour.

### 1.4 Application numérique

Les quatre cas confirment les deux limites : dès que x dépasse quelques fois D, la tache court à c et l'observateur la voit avancer à c/2. Pour x = 1 million d'années-lumière, il attend bien 2 millions d'années.

Données : D = 10⁸ km, ω = π/2 rad/s, c = 299 792,458 km/s, 1 année-lumière = 9,4607 × 10¹² km. Les temps sont comptés depuis le début de la fermeture.

| Position x | Émission τ (s) | Arrivée sur le tableau | Vue par l'observateur | Vitesse sur le tableau (en c) | Vitesse perçue (en c) |
| --- | --- | --- | --- | --- | --- |
| Centre, x = 0 | 0 | 5 min 34 s | 11 min 7 s | 524 | 524 |
| 10 millions de km (θ = 5,7°) | 0,063 | 5 min 35 s | 11 min 11 s | 9,86 | 4,98 |
| 100 millions de km (θ = 45°) | 0,500 | 7 min 52 s | 15 min 44 s | 1,412 | 0,707 |
| 1 milliard de km (θ = 84,3°) | 0,937 | 55 min 53 s | 1 h 51 min 45 s | 1,0050 | 0,5025 |
| 1 million d'années-lumière (θ ≈ 90°) | 1 − 7 × 10⁻¹² | 1 000 000 ans + 1 s | 2 000 000 ans + 1 s | 1 + 6 × 10⁻²³ | 0,5 + 3 × 10⁻²³ |

En km/s, la vitesse perçue vaut successivement 1 492 000, 211 842, 150 642 puis 149 896 km/s pour les quatre distances demandées.

**Détail du dernier cas.** Pour x = 10⁶ années-lumière = 9,46 × 10¹⁸ km, le rapport x/D vaut 9,46 × 10¹⁰. La diagonale se confond alors avec x :

```latex
R = x\,\sqrt{1 + \frac{D^2}{x^2}} \approx x\left(1 + \frac{D^2}{2x^2}\right) = x\,\big(1 + 5{,}6 \times 10^{-23}\big)
```

Par définition de l'année-lumière, x/c vaut exactement un million d'années. Le temps de réception suit :

```latex
\begin{aligned}
t_{\text{obs}} &= \tau + \frac{2R}{c} \approx 1\ \text{s} + 2 \times \frac{10^{6}\ \text{années-lumière}}{c} \\
&= 2\,000\,000\ \text{ans} + 1\ \text{s}
\end{aligned}
```

**Lecture mécanique.** Tous les photons quittent la source en 1 seconde. Ceux qui peignent les pointes, à un million d'années-lumière, partent dans les 7 derniers milliardièmes de milliseconde de la fermeture. Le spectacle dure pourtant 2 millions d'années pour l'observateur : cette durée est du temps de trajet, pas du temps de fermeture.

### 1.5 Inversion du signe : les jets de quasars

La même mécanique, avec un trajet qui raccourcit au lieu de s'allonger, donne la formule de Rees pour les jets de quasars.

Les sections 1.2 et 1.3 obéissent à une règle unique. Soit L(τ) la longueur du trajet entre le point qui émet à l'instant τ et l'œil, et x⊥ sa position en travers de la ligne de visée :

```latex
\begin{aligned}
t_{\text{obs}}(\tau) &= \tau + \frac{L(\tau)}{c} \\
v_{\text{app}} &= \frac{dx_{\perp}/d\tau}{dt_{\text{obs}}/d\tau} = \frac{\dot{x}_{\perp}}{1 + \dfrac{\dot{L}}{c}}
\end{aligned}
```

- Tableau plat : L = 2R, donc L̇ = 2ẋ sin θ est positif. Le trajet s'allonge et la vitesse apparente est comprimée.
- Jet de quasar : la source est un nodule de matière qui avance vers l'observateur. Le trajet raccourcit, L̇ est négatif, et la vitesse apparente est amplifiée.

Le nodule avance à la vitesse v, sous un angle θ par rapport à la ligne de visée. Ici θ n'est plus l'angle du tableau : c'est l'angle entre le jet et la direction de l'observateur. Pour un observateur très lointain, à la distance d₀ :

```latex
x_{\perp}(\tau) = v\,\tau\,\sin\theta, \qquad L(\tau) = d_0 - v\,\tau\,\cos\theta
```

```latex
\frac{dt_{\text{obs}}}{d\tau} = 1 - \frac{v}{c}\cos\theta
\qquad\Longrightarrow\qquad
v_{\text{app}} = \frac{v\,\sin\theta}{1 - \dfrac{v}{c}\cos\theta}
```

C'est exactement la formule demandée. Son maximum se trouve en dérivant par rapport à θ, avec β = v/c :

```latex
\begin{aligned}
\frac{d}{d\theta}\left(\frac{\beta\sin\theta}{1 - \beta\cos\theta}\right) &= \frac{\beta\cos\theta\,(1 - \beta\cos\theta) - \beta^2\sin^2\theta}{(1 - \beta\cos\theta)^2} \\
&= \frac{\beta\,(\cos\theta - \beta)}{(1 - \beta\cos\theta)^2}
\end{aligned}
```

La dérivée s'annule pour cos θ = β, donc sin θ = √(1 − β²) :

```latex
v_{\text{app}}^{\max} = \frac{\beta\sqrt{1 - \beta^2}}{1 - \beta^2}\;c = \gamma\,\beta\,c, \qquad \gamma = \frac{1}{\sqrt{1 - \beta^2}}
```

La vitesse apparente dépasse c dès que γβ > 1, c'est-à-dire v > c/√2 ≈ 0,707 c. Exemple : pour v = 0,99 c et θ = 8,1°, on trouve γ = 7,09 et une vitesse apparente de 7,02 c. Rien ne dépasse pourtant c.

**Lecture mécanique.** Le nodule court presque aussi vite que sa propre lumière. Les photons émis plus tard ont moins de chemin à faire et arrivent presque en même temps que les premiers. L'observateur voit un long déplacement latéral comprimé dans un temps de réception très court.

**Une différence de nature.** Pour un nodule matériel, v < c : le dénominateur ne s'annule jamais et l'ordre des événements est préservé. Pour une tache qui revient vers le centre du tableau (ẋ négatif), rien ne borne la vitesse de visée :

```latex
\frac{dt_{\text{obs}}}{d\tau} = 1 - \frac{2\,|\dot{x}|}{c}\,\sin\theta
```

Dès que 2|ẋ| sin θ dépasse c, ce facteur devient négatif : l'observateur voit le film à l'envers. Nemiroff (2015) a décrit ces images de taches inversées ou dédoublées.

**Travaux établis.** Couderc (1939) a expliqué ainsi l'expansion apparente plus rapide que c des auréoles de la Nova Persei 1901 : ce sont des échos de lumière. Les points vus au même instant forment un ellipsoïde dont la source et l'observateur sont les foyers. Quand les deux foyers se confondent, comme ici, l'ellipsoïde devient la sphère de la section 1.3.

Rees (1966) a prédit les vitesses apparentes supraluminiques des sources radio relativistes. Elles sont observées en interférométrie radio depuis les années 1970.

### 1.6 Conditions de validité

- Espace-temps plat, vide, c constant ; la source, le tableau et l'observateur sont immobiles les uns par rapport aux autres.
- Optique géométrique : l'ombre a un bord net. À 10⁸ km, la diffraction étale ce bord sur environ 230 m en lumière visible. L'ombre de vrais ciseaux serait noyée : c'est une expérience de pensée, ou une tache laser.
- Le tableau diffuse la lumière sans délai et dans toutes les directions.
- L'observateur est exactement à la source. Sinon le retour n'emprunte plus la même diagonale, et la sphère du visible redevient un ellipsoïde.
- La vitesse angulaire ω est constante. Seul le terme c/ẋ en dépend : les limites c et c/2 n'en dépendent pas.
- Ces vitesses sont celles d'un motif, une succession d'impacts indépendants. Ni matière, ni énergie, ni information ne va d'un point du tableau à l'autre : c'est l'objet du pilier 2.

## Pilier 2 — La lumière « actuelle, émergente, locale »

Les deux volets de l'intuition se démontrent : rien ne se propage de A vers B le long du tableau, et toute détection est un événement local, produit par une interaction avec la matière. Une nuance s'impose : en transit, le champ n'est pas « rien », il transporte de l'énergie et de l'impulsion.

### 2.1 Absence de causalité latérale

Soient deux impacts A et B sur le tableau, séparés par une durée Δt et une distance Δx. L'hypothèse est que la tache va plus vite que c entre les deux : |Δx| > c|Δt|. L'intervalle d'espace-temps est alors négatif :

```latex
\Delta s^2 = c^2\,\Delta t^2 - \Delta x^2 < 0 \qquad \text{car } |\Delta x| > c\,|\Delta t|
```

On dit que l'intervalle est de genre espace. La démonstration se fait en trois étapes.

**Étape 1 : le signe de l'intervalle est absolu.** Un observateur qui glisse le long du tableau à la vitesse u, inférieure à c, mesure d'autres durées et d'autres distances. La transformation de Lorentz les donne :

```latex
\begin{aligned}
\Delta t' &= \gamma_u\left(\Delta t - \frac{u\,\Delta x}{c^2}\right), \qquad \Delta x' = \gamma_u\,(\Delta x - u\,\Delta t) \\
\gamma_u &= \frac{1}{\sqrt{1 - u^2/c^2}}
\end{aligned}
```

On calcule l'intervalle vu par cet observateur, en développant les deux carrés. Les termes croisés en Δt Δx s'annulent :

```latex
\begin{aligned}
c^2\Delta t'^2 - \Delta x'^2 &= \gamma_u^2\left[\left(c\,\Delta t - \frac{u}{c}\,\Delta x\right)^2 - (\Delta x - u\,\Delta t)^2\right] \\
&= \gamma_u^2\left(1 - \frac{u^2}{c^2}\right)\left(c^2\Delta t^2 - \Delta x^2\right) \\
&= c^2\Delta t^2 - \Delta x^2
\end{aligned}
```

Tous les observateurs trouvent le même Δs². « Genre espace » est donc un fait absolu, pas une affaire de point de vue.

**Étape 2 : l'ordre dans le temps, lui, n'est pas absolu.** On choisit la vitesse particulière u\* ci-dessous. Elle est inférieure à c, précisément parce que |Δx| > c|Δt| :

```latex
\begin{aligned}
u^{*} &= \frac{c^2\,\Delta t}{\Delta x}, \qquad |u^{*}| = c \times \frac{c\,|\Delta t|}{|\Delta x|} < c \\
\Delta t' &= \gamma_{u^{*}}\left(\Delta t - \frac{u^{*}\,\Delta x}{c^2}\right) = 0
\end{aligned}
```

Pour cet observateur, A et B sont simultanés. Pour un observateur un peu plus rapide, Δt' change de signe : B a lieu avant A.

**Étape 3 : conclusion.** Une cause précède son effet pour tous les observateurs. Or l'ordre de A et B dépend de l'observateur. Donc A ne cause pas B, et B ne cause pas A.

Ce raisonnement s'appuie sur un principe physique, pas sur les seules mathématiques : aucune influence ne se propage plus vite que c. Toutes les expériences le confirment à ce jour.

**La vraie chaîne causale.** Chaque impact est relié à sa propre émission par un trajet de lumière, donc par un intervalle nul :

```latex
c^2\,(t_A - \tau_A)^2 - R_A^2 = 0, \qquad c^2\,(t_B - \tau_B)^2 - R_B^2 = 0
```

La causalité dessine un éventail qui part de la source, pas une chaîne le long du tableau. A et B partagent une cause commune, les ciseaux, et rien d'autre.

**Lecture mécanique.** En langage de projet, A et B sont deux livraisons du même expéditeur, pas deux étapes d'une même chaîne. Le test est simple : posez la main sur le tableau en A. L'impact en B a lieu quand même, car la lumière qui va en B n'est jamais passée par A.

**Lien avec le pilier 1.** Avec Dω = 524 c, la tache dépasse c partout sur le tableau. Deux impacts quelconques vérifient donc |Δx| > c|Δt| : toutes les paires d'impacts sont de genre espace.

**Portée exacte.** Même pour un balayage lent, où la tache resterait sous c, aucun impact n'en causerait un autre : la tache n'est jamais un objet. La condition de genre espace ajoute que ce lien est impossible par principe. C'est la structure décrite par Minkowski (1908) : passé, futur et « ailleurs » sont séparés de façon absolue.

### 2.2 Transparence en transit et émergence locale

En transit, l'état du champ évolue sans produire aucun événement. Un événement lumineux n'existe que là où un atome interagit avec le champ, en un lieu et à un instant précis.

**Le champ libre.** Dans le vide, le champ électromagnétique est une collection de modes k, chacun avec sa pulsation. Son hamiltonien, c'est-à-dire son énergie, compte les photons de chaque mode :

```latex
\hat{H}_0 = \sum_{k} \hbar\,\omega_k\left(\hat{a}_k^{\dagger}\hat{a}_k + \tfrac{1}{2}\right), \qquad \hat{n}_k = \hat{a}_k^{\dagger}\hat{a}_k
```

L'opérateur â† crée un photon dans le mode k, â en détruit un, et leur produit les compte. L'état du champ évolue de façon unitaire :

```latex
|\psi(t)\rangle = \hat{U}(t)\,|\psi(0)\rangle, \qquad \hat{U}(t) = e^{-i\hat{H}_0 t/\hbar}, \qquad \hat{U}^{\dagger}\hat{U} = \hat{1}
```

Deux conséquences suivent, l'une de l'unitarité, l'autre du fait que l'énergie et le nombre de photons commutent :

```latex
\begin{aligned}
\langle\psi(t)|\psi(t)\rangle &= \langle\psi(0)|\hat{U}^{\dagger}\hat{U}|\psi(0)\rangle = 1 \\
[\hat{H}_0, \hat{n}_k] = 0 \quad&\Longrightarrow\quad \frac{d}{dt}\langle\hat{n}_k\rangle = 0
\end{aligned}
```

Pour un photon unique réparti sur plusieurs modes, l'évolution se réduit à des phases qui tournent :

```latex
\begin{aligned}
|\psi(0)\rangle &= \sum_k c_k\,\hat{a}_k^{\dagger}|0\rangle \\
|\psi(t)\rangle &= \sum_k c_k\,e^{-i\omega_k t}\,\hat{a}_k^{\dagger}|0\rangle
\end{aligned}
```

**Lecture mécanique.** En transit, seules des phases tournent. Aucun photon n'est créé, absorbé ou dévié, car le vide ne contient aucun terme d'interaction. Il ne se produit donc aucun événement, et rien n'est envoyé vers un œil placé sur le côté.

**Le champ en un point.** Le champ électrique se décompose en deux parties. La partie notée (+) ne contient que des opérateurs qui détruisent un photon : c'est la partie « absorption ». La polarisation est omise pour alléger.

```latex
\begin{aligned}
\hat{E}(\vec{r},t) &= \hat{E}^{(+)}(\vec{r},t) + \hat{E}^{(-)}(\vec{r},t), \qquad \hat{E}^{(-)} = \big(\hat{E}^{(+)}\big)^{\dagger} \\
\hat{E}^{(+)}(\vec{r},t) &= i\sum_k \sqrt{\frac{\hbar\,\omega_k}{2\,\varepsilon_0 V}}\;\hat{a}_k\,e^{\,i(\vec{k}\cdot\vec{r} - \omega_k t)}
\end{aligned}
```

**Le détecteur.** Un atome placé au point r (rétine, grain de l'écran, pixel) est couplé au champ par son dipôle électrique d :

```latex
\hat{H}_{\text{int}}(t) = -\,\hat{\vec{d}}\cdot\hat{\vec{E}}(\vec{r},t)
```

Le champ n'y figure qu'au point r où se trouve l'atome. L'atome passe de son état de repos g à un état excité e pendant que le champ passe de l'état i à l'état f. Au premier ordre, l'amplitude de cette transition est :

```latex
\mathcal{A}_{fi} = -\frac{i}{\hbar}\int_0^{t} dt'\,\langle e, f|\hat{H}_{\text{int}}(t')|g, i\rangle \;\propto\; \langle f|\hat{E}^{(+)}(\vec{r},t)|i\rangle
```

L'état final du champ n'est pas observé : on additionne les probabilités sur tous les états f possibles. La somme se simplifie grâce à la relation de fermeture, Σ |f⟩⟨f| = 1 :

```latex
\sum_f \big|\langle f|\hat{E}^{(+)}|i\rangle\big|^2 = \sum_f \langle i|\hat{E}^{(-)}|f\rangle\langle f|\hat{E}^{(+)}|i\rangle = \langle i|\hat{E}^{(-)}\hat{E}^{(+)}|i\rangle
```

On obtient la formule de Glauber (1963) pour le taux de détection, c'est-à-dire la probabilité de clic par unité de temps. Le facteur η est l'efficacité du détecteur :

```latex
\begin{aligned}
w(\vec{r},t) &= \eta\,\langle\psi|\hat{E}^{(-)}(\vec{r},t)\,\hat{E}^{(+)}(\vec{r},t)|\psi\rangle \\
&= \eta\,\big\|\hat{E}^{(+)}(\vec{r},t)\,|\psi\rangle\big\|^2 \;\ge\; 0
\end{aligned}
```

**Correction de la formule demandée.** La probabilité n'est pas le module d'un élément de matrice entre deux états différents i et f. C'est la valeur moyenne du produit E(−)E(+) dans l'état du champ, soit la somme des probabilités sur tous les états finals.

**Lecture mécanique.** Les trois mots du modèle se lisent dans la formule. Local : seul le champ au point r du détecteur intervient. Actuel : seul l'instant t de l'interaction intervient. Émergent : sans atome ni couplage, il n'y a pas de clic du tout.

**Pourquoi le faisceau est invisible de côté.** Pour un photon unique, le taux de clic en un point r' est le carré d'une amplitude :

```latex
w(\vec{r}^{\,\prime},t) = \eta\,\big|\langle 0|\hat{E}^{(+)}(\vec{r}^{\,\prime},t)|\psi\rangle\big|^2
```

Cette amplitude est nulle hors du faisceau : un œil placé sur le côté ne reçoit rien. Pour voir un faisceau de profil, il faut de la matière sur son trajet, poussière ou air, qui dévie des photons vers l'œil. On voit alors la matière éclairée, pas la lumière en transit.

**Un photon, un seul clic.** La probabilité de deux clics en deux endroits fait intervenir deux destructions successives. Pour un photon unique, elle est nulle :

```latex
G^{(2)} = \langle\psi|\hat{E}^{(-)}(\vec{r}_1)\,\hat{E}^{(-)}(\vec{r}_2)\,\hat{E}^{(+)}(\vec{r}_2)\,\hat{E}^{(+)}(\vec{r}_1)|\psi\rangle = 0
```

Un photon détecté de côté n'arrive donc plus sur l'écran : observer le transit, c'est le consommer. Grangier, Roger et Aspect (1986) l'ont vérifié sur une lame séparatrice.

### 2.3 Conditions de validité et nuances

- « Potentiel » ne veut pas dire « rien ». En transit, chaque photon porte une énergie ħω et une impulsion ħk ; on peut le bloquer, le retarder ou le dévier. Ce qui reste potentiel, c'est l'événement de détection.
- Le photon n'a pas d'opérateur de position au sens strict (Newton et Wigner, 1949). La question « où est le photon en transit ? » n'a pas de réponse générale : seules existent des probabilités de détection. Ce point appuie l'émergence locale.
- La transparence du vide est une excellente approximation, pas un absolu. L'électrodynamique quantique prévoit une diffusion de la lumière par la lumière, mise en évidence à très haute énergie (ATLAS, 2017) et négligeable en lumière visible.
- Détecter n'exige pas toujours d'absorber. Certaines mesures comptent des photons sans les détruire (travaux de Serge Haroche). Elles exigent quand même une interaction locale avec la matière.
- Le formalisme ne tranche pas l'interprétation : l'état du champ est-il une onde réelle ou un catalogue de probabilités ? Heisenberg (1958) parlait de « potentia », la formulation historique la plus proche de l'intuition.
- Le mot « rayon » reste valide comme approximation des petites longueurs d'onde. Un rayon est la perpendiculaire aux fronts d'onde, pas une tige rigide : sur ce point, l'intuition vise juste.
- Approximations du calcul : couplage dipolaire (atome petit devant la longueur d'onde), premier ordre de perturbation, détecteur à large bande.

## Pilier 3 — L'univers à la cadence c et la masse comme frein local

La relativité donne un sens précis à l'intuition : tout objet avance dans l'espace-temps à la cadence c, et une masse ralentit les horloges voisines par rapport aux horloges lointaines. La gravité de Newton vaut exactement c² fois la pente de ce ralentissement. Deux corrections portent sur la formule de réfraction : son signe, et un facteur 2 entre la lumière et la matière lente.

### 3.1 Tout avance à la cadence c : la quadri-vitesse

Un événement est repéré par quatre coordonnées (ct, x, y, z). Dans ce pilier, τ désigne le temps propre : le temps lu sur l'horloge que l'objet transporte avec lui. L'intervalle de Minkowski le relie au temps t d'un observateur qui voit l'objet passer à la vitesse v :

```latex
\begin{aligned}
c^2\,d\tau^2 &= c^2\,dt^2 - dx^2 - dy^2 - dz^2 = c^2\,dt^2\left(1 - \frac{v^2}{c^2}\right) \\
d\tau &= \frac{dt}{\gamma}, \qquad \gamma = \frac{1}{\sqrt{1 - v^2/c^2}}
\end{aligned}
```

La quadri-vitesse est le déplacement dans l'espace-temps par unité de temps propre :

```latex
U^{\mu} = \frac{dx^{\mu}}{d\tau} = \frac{dt}{d\tau}\,\frac{dx^{\mu}}{dt} = \gamma\,(c,\ \vec{v}) = (\gamma c,\ \gamma\vec{v})
```

Sa norme se calcule avec la métrique de Minkowski, qui compte le temps en positif et l'espace en négatif :

```latex
\begin{aligned}
\eta_{\mu\nu}\,U^{\mu}U^{\nu} &= (\gamma c)^2 - (\gamma v)^2 = \gamma^2 c^2\left(1 - \frac{v^2}{c^2}\right) = c^2 \\
\|U\| &= c
\end{aligned}
```

C'est exactement le résultat demandé : la norme vaut c pour tout objet massif, quelle que soit sa vitesse. Le partage du budget s'obtient en divisant l'intervalle par dt² :

```latex
c^2\,d\tau^2 = c^2\,dt^2 - v^2\,dt^2
\qquad\Longrightarrow\qquad
\left(c\,\frac{d\tau}{dt}\right)^2 + v^2 = c^2
```

**Lecture mécanique.** Le premier terme est la cadence de l'horloge embarquée, convertie en vitesse. Le second est la vitesse dans l'espace. La somme de leurs carrés est fixe : ce que l'objet dépense en déplacement, il le retire à son horloge.

Au repos, tout le budget passe dans le temps et l'horloge bat à plein régime. À v = 0,6 c, elle ne bat plus qu'à 80 %. Quand v approche c, il ne reste rien pour le temps.

**Portée exacte.**

- C'est une identité de construction : elle découle de la définition du temps propre. Ce n'est pas une loi dynamique supplémentaire.
- La norme de Minkowski est une différence de carrés. La forme « somme égale à c² » apparaît quand on compte le budget par seconde du temps t de l'observateur.
- Pour la lumière, dτ = 0 : la quadri-vitesse n'est pas définie. Tout le budget est dans l'espace.
- Le sens précis de « l'univers tourne à c » est donc : tout objet massif parcourt sa ligne d'univers à la norme c, même immobile. L'espace lui-même ne se déplace pas.

### 3.2 La masse ralentit son voisinage : la métrique de Schwarzschild

Près d'une masse, une horloge immobile bat plus lentement qu'une horloge lointaine, et ce rapport tombe à zéro à l'horizon d'un trou noir. Comptée en temps lointain, la lumière y ralentit aussi ; mesurée sur place, elle va toujours à c.

Autour d'une masse sphérique M, l'intervalle d'espace-temps s'écrit :

```latex
\begin{aligned}
ds^2 &= \left(1 - \frac{r_s}{r}\right)c^2\,dt^2 - \left(1 - \frac{r_s}{r}\right)^{-1}dr^2 - r^2\,d\Omega^2 \\
r_s &= \frac{2GM}{c^2}
\end{aligned}
```

- t est le temps des horloges très éloignées de la masse.
- r est la coordonnée radiale, et dΩ repère les déplacements à r constant.
- Le rayon de Schwarzschild, noté r indice s, vaut 8,87 mm pour la Terre et 2,95 km pour le Soleil.

La norme de la quadri-vitesse reste égale à c avec cette métrique courbe. La masse ne réduit donc pas la cadence locale : elle modifie le taux de change entre le temps local et le temps lointain.

**Horloge immobile.** Pour une horloge qui reste à r fixé, dr = 0 et dΩ = 0. Son temps propre vérifie ds² = c² dτ² :

```latex
c^2\,d\tau^2 = \left(1 - \frac{r_s}{r}\right)c^2\,dt^2
\qquad\Longrightarrow\qquad
d\tau = dt\,\sqrt{1 - \frac{r_s}{r}}
```

C'est exactement la formule demandée. En termes de budget, la cadence d'une horloge immobile, comptée en temps lointain, n'est plus c mais c multiplié par cette racine.

| Lieu | Rayon de Schwarzschild | Rapport rayon de Schwarzschild / r | Retard de l'horloge locale |
| --- | --- | --- | --- |
| Surface de la Terre | 8,87 mm | 1,39 × 10⁻⁹ | 0,022 s par an |
| Surface du Soleil | 2,95 km | 4,25 × 10⁻⁶ | 67 s par an |
| Étoile à neutrons (1,4 masse solaire, rayon 12 km) | 4,13 km | 0,345 | 19 % |
| Horizon d'un trou noir | égal à r | 1 | arrêt apparent |

**Le gel à l'horizon.** Quand r tend vers le rayon de Schwarzschild, le rapport dτ/dt tend vers 0. Ce gel est bien « apparent », comme le dit l'intuition : il décrit ce que constate l'observateur lointain. Un objet qui tombe franchit l'horizon en un temps propre fini, sans rien remarquer sur place.

**La lumière, comptée en temps lointain.** Pour la lumière, ds² = 0. Sur un trajet radial (dΩ = 0) :

```latex
\begin{aligned}
0 &= \left(1 - \frac{r_s}{r}\right)c^2\,dt^2 - \left(1 - \frac{r_s}{r}\right)^{-1}dr^2 \\
\frac{dr}{dt} &= \pm\,c\left(1 - \frac{r_s}{r}\right)
\end{aligned}
```

Cette vitesse, dite « coordonnée », diminue près de la masse et tend vers 0 à l'horizon.

**La lumière, mesurée sur place.** Un observateur immobile à la distance r utilise sa propre règle et sa propre horloge. Les deux sont affectées par la masse, et les deux effets se compensent :

```latex
\begin{aligned}
d\ell &= \frac{dr}{\sqrt{1 - r_s/r}}, \qquad d\tau = dt\,\sqrt{1 - \frac{r_s}{r}} \\
\frac{d\ell}{d\tau} &= \frac{1}{1 - r_s/r}\,\frac{dr}{dt} = c
\end{aligned}
```

Sur place, la lumière va toujours exactement à c. Le ralentissement n'existe que dans la comparaison entre deux lieux.

**Effet Shapiro.** Le temps lointain que met la lumière pour aller de r₁ à r₂ le long d'un rayon se calcule en intégrant dt = dr / (vitesse coordonnée) :

```latex
\begin{aligned}
\Delta t &= \int_{r_1}^{r_2}\frac{dr}{c\,(1 - r_s/r)} = \frac{1}{c}\int_{r_1}^{r_2}\left(1 + \frac{r_s}{r - r_s}\right)dr \\
&= \frac{r_2 - r_1}{c} + \frac{r_s}{c}\,\ln\frac{r_2 - r_s}{r_1 - r_s}
\end{aligned}
```

Le premier terme est le temps de trajet sans masse. Le second est le retard gravitationnel prédit par Shapiro (1964). Pour un écho radar Terre–Vénus qui frôle le Soleil, la formule de la section 3.3 donne 233 microsecondes de retard sur l'aller-retour. Shapiro annonçait près de 200 microsecondes, et la sonde Cassini (2003) a confirmé l'effet à 0,002 % près.

Les satellites GPS en donnent une preuve quotidienne. Plus haut dans le champ terrestre, leurs horloges avancent de 45,7 microsecondes par jour. Leur vitesse les retarde de 7,2 microsecondes, et le système corrige l'écart net de 38,5.

**Lecture mécanique.** La masse agit comme un goulot d'étranglement sur les cadences : près d'elle, tout processus prend plus de temps lointain. Ce frein n'est pourtant pas un frottement. Aucune énergie n'est dissipée, et sur place tout paraît normal.

### 3.3 La gravité comme réfraction vers la zone lente

Réécrite en coordonnées isotropes, la métrique donne au vide un indice n ≈ 1 + 2GM/(rc²), et le principe de Fermat courbe les rayons vers la masse. Deux corrections s'imposent : la déviation suit +∇n, et cet indice donne pour la lumière le double de la gravité de Newton.

**Coordonnées isotropes.** Dans la métrique de Schwarzschild, la vitesse coordonnée de la lumière diffère selon la direction. Pour définir un indice unique, on cherche une coordonnée radiale ρ qui traite toutes les directions de la même façon :

```latex
\left(1 - \frac{r_s}{r}\right)^{-1}dr^2 + r^2\,d\Omega^2 = \lambda(\rho)^2\left(d\rho^2 + \rho^2\,d\Omega^2\right)
```

L'identification des parties angulaires, puis des parties radiales, impose deux relations :

```latex
r = \lambda\,\rho, \qquad \frac{dr}{\sqrt{1 - r_s/r}} = \lambda\,d\rho
```

En éliminant λ, on obtient une équation à variables séparées, qui s'intègre directement :

```latex
\begin{aligned}
\frac{d\rho}{\rho} &= \frac{dr}{\sqrt{r^2 - r_s\,r}} \\
\ln\rho &= \ln\left(r - \frac{r_s}{2} + \sqrt{r^2 - r_s\,r}\right) + \text{constante}
\end{aligned}
```

La constante est fixée pour que ρ et r coïncident loin de la masse. On inverse ensuite la relation :

```latex
\begin{aligned}
\rho &= \frac{1}{2}\left(r - \frac{r_s}{2} + \sqrt{r^2 - r_s\,r}\right) \\
r &= \rho\left(1 + \frac{r_s}{4\rho}\right)^{2}
\end{aligned}
```

En reportant dans la métrique de Schwarzschild :

```latex
ds^2 = \left(\frac{1 - \dfrac{r_s}{4\rho}}{1 + \dfrac{r_s}{4\rho}}\right)^{2} c^2\,dt^2 - \left(1 + \frac{r_s}{4\rho}\right)^{4}\left(d\rho^2 + \rho^2\,d\Omega^2\right)
```

**L'indice du vide.** Pour la lumière, ds² = 0. On note dℓ² = dρ² + ρ² dΩ² la longueur coordonnée, identique dans toutes les directions :

```latex
\begin{aligned}
\frac{d\ell}{dt} &= c\,\frac{1 - \dfrac{r_s}{4\rho}}{\left(1 + \dfrac{r_s}{4\rho}\right)^{3}} \equiv \frac{c}{n(\rho)} \\
n(\rho) &= \frac{\left(1 + \dfrac{r_s}{4\rho}\right)^{3}}{1 - \dfrac{r_s}{4\rho}}
\end{aligned}
```

Loin de la masse, ρ ≈ r et le rayon de Schwarzschild est très petit devant r. Au premier ordre :

```latex
\begin{aligned}
n(r) &\approx 1 + \frac{r_s}{r} = 1 + \frac{2GM}{r\,c^2} \\
v(r) &= \frac{c}{n(r)} \approx c\left(1 - \frac{2GM}{r\,c^2}\right)
\end{aligned}
```

Ce sont exactement les deux formules demandées. L'écart n − 1 vaut 4,2 × 10⁻⁶ au bord du Soleil et 1,4 × 10⁻⁹ à la surface de la Terre.

**Deux moitiés.** L'excès d'indice vient pour moitié du temps et pour moitié de l'espace. Les horloges ralenties comptent pour GM/(rc²), les longueurs modifiées pour GM/(rc²) aussi. Ce partage explique le facteur 2 qui apparaît plus bas.

**Principe de Fermat.** La lumière suit le trajet qui rend stationnaire le temps de parcours, proportionnel à ∫ n dℓ. On décrit le trajet par une position qui dépend d'un paramètre σ, et le point désigne la dérivée par rapport à σ :

```latex
\delta\int n(\vec{r})\,\big|\dot{\vec{r}}\big|\,d\sigma = 0, \qquad \mathcal{L} = n(\vec{r})\,\big|\dot{\vec{r}}\big|
```

```latex
\frac{\partial\mathcal{L}}{\partial\dot{\vec{r}}} = n\,\frac{\dot{\vec{r}}}{|\dot{\vec{r}}|} = n\,\hat{s}, \qquad \frac{\partial\mathcal{L}}{\partial\vec{r}} = \big|\dot{\vec{r}}\big|\,\vec{\nabla}n
```

Le vecteur ŝ est le vecteur unitaire tangent au rayon. L'équation d'Euler-Lagrange, avec dℓ = |ṙ| dσ, donne l'équation des rayons :

```latex
\frac{d}{d\sigma}\left(\frac{\partial\mathcal{L}}{\partial\dot{\vec{r}}}\right) = \frac{\partial\mathcal{L}}{\partial\vec{r}}
\qquad\Longrightarrow\qquad
\frac{d}{d\ell}\big(n\,\hat{s}\big) = \vec{\nabla}n
```

On développe la dérivée du produit, avec dn/dℓ = ŝ · ∇n. Il reste la partie du gradient perpendiculaire au rayon, notée ∇⊥ :

```latex
\frac{d\hat{s}}{d\ell} = \frac{1}{n}\Big[\vec{\nabla}n - (\hat{s}\cdot\vec{\nabla}n)\,\hat{s}\Big] = \frac{\vec{\nabla}_{\!\perp}n}{n} \approx \vec{\nabla}_{\!\perp}n
```

Le rayon tourne vers les n croissants, c'est-à-dire vers la zone où la lumière est la plus lente. Huygens dit la même chose : le côté du front d'onde le plus proche de la masse avance moins vite, et le front pivote vers elle.

**Accélération transverse de la lumière.** Le rayon est parcouru à une vitesse très proche de c. L'accélération transverse vaut donc c² fois le taux de rotation du rayon. Comme n augmente quand on s'approche de la masse, son gradient pointe vers elle :

```latex
\begin{aligned}
\vec{a}_{\perp} &= c^2\,\frac{d\hat{s}}{d\ell} = c^2\,\vec{\nabla}_{\!\perp}n = -\,c\,\vec{\nabla}_{\!\perp}v \\
\vec{\nabla}n &= -\frac{2GM}{r^2c^2}\,\hat{r}
\quad\Longrightarrow\quad
\vec{a}_{\perp} = -\frac{2GM}{r^2}\,\hat{r}_{\perp}
\end{aligned}
```

**Déviation totale.** Pour un rayon qui passe à la distance b de la masse, on additionne les rotations le long du trajet, repéré par z :

```latex
\begin{aligned}
\alpha &= \int_{-\infty}^{+\infty}\left|\frac{\partial n}{\partial b}\right|dz = \frac{2GM}{c^2}\int_{-\infty}^{+\infty}\frac{b\,dz}{(b^2 + z^2)^{3/2}} \\
&= \frac{2GM}{c^2}\left[\frac{z}{b\,\sqrt{b^2 + z^2}}\right]_{-\infty}^{+\infty} = \frac{4GM}{b\,c^2}
\end{aligned}
```

Au bord du Soleil, on trouve 1,75 seconde d'arc, une valeur compatible avec les mesures de l'éclipse de 1919. Le même indice donne aussi le retard Shapiro de la section 3.2 :

```latex
\begin{aligned}
\Delta t &= \frac{1}{c}\int (n - 1)\,dz = \frac{2GM}{c^3}\int_{-z_1}^{z_2}\frac{dz}{\sqrt{b^2 + z^2}} \\
&\approx \frac{2GM}{c^3}\,\ln\frac{4\,r_1 r_2}{b^2}
\end{aligned}
```

**Corrections de la formule demandée.** La formule proposée était une accélération proportionnelle à −c²∇n, égale à −GM/r². Deux points changent.

1. Le signe. Le gradient de n pointe vers la masse, et la déviation suit +c²∇n. Avec un signe moins, la lumière serait repoussée. Le signe moins redevient correct si l'on dérive la vitesse : a = −c∇v.
2. Le facteur 2. Avec n = 1 + 2GM/(rc²), on trouve 2GM/r², le double de Newton. Ce n'est pas une erreur de calcul : c'est le résultat propre à la relativité générale.

Einstein (1911), avec le seul ralentissement du temps, annonçait 0,83 seconde d'arc, la moitié environ. Sa théorie complète, publiée en 1916, ajoute la part de l'espace et donne 1,7 seconde d'arc. L'éclipse de 1919 a tranché en faveur du double : 1,98 ± 0,12 seconde d'arc à Sobral, 1,61 ± 0,30 à Principe.

**La matière lente et la loi de Newton.** Un corps libre suit la trajectoire qui rend stationnaire son temps propre. En champ faible, avec le potentiel de Newton Φ, la métrique isotrope s'écrit :

```latex
ds^2 \approx \left(1 + \frac{2\Phi}{c^2}\right)c^2\,dt^2 - \left(1 - \frac{2\Phi}{c^2}\right)d\ell^2, \qquad \Phi = -\frac{GM}{r}
```

Pour un corps lent, on divise par c² dt² et on développe la racine au premier ordre. Le terme en Φv² est négligeable :

```latex
\frac{d\tau}{dt} = \sqrt{1 + \frac{2\Phi}{c^2} - \left(1 - \frac{2\Phi}{c^2}\right)\frac{v^2}{c^2}} \;\approx\; 1 + \frac{\Phi}{c^2} - \frac{v^2}{2c^2}
```

L'action d'un corps libre de masse m est −mc² fois son temps propre :

```latex
S = -mc^2\int d\tau \;\approx\; \int\left(-mc^2 + \frac{1}{2}mv^2 - m\Phi\right)dt
```

On reconnaît le lagrangien de Newton : énergie cinétique moins énergie potentielle, à une constante près. L'équation d'Euler-Lagrange donne :

```latex
\frac{d}{dt}\big(m\,\vec{v}\big) = -m\,\vec{\nabla}\Phi
\qquad\Longrightarrow\qquad
\vec{a} = -\vec{\nabla}\Phi = -\frac{GM}{r^2}\,\hat{r}
```

La loi de Newton est retrouvée. Elle s'écrit avec la cadence N des horloges immobiles, c'est-à-dire le rapport dτ/dt au repos :

```latex
\begin{aligned}
N(r) &\equiv \left.\frac{d\tau}{dt}\right|_{v=0} \approx 1 + \frac{\Phi}{c^2} = 1 - \frac{GM}{r\,c^2} \\
\vec{a} &= -\,c^2\,\vec{\nabla}N
\end{aligned}
```

C'est la forme correcte de la formule demandée : un signe moins, le facteur c², et le gradient de la cadence des horloges plutôt que celui de l'indice de la lumière.

**Vérification chiffrée.** À la surface de la Terre, une horloge placée 1 m plus haut avance de 1,09 × 10⁻¹⁶ en valeur relative. Multipliée par c², cette pente par mètre donne 9,81 m/s² : la pesanteur. Chou et ses collègues (2010) ont mesuré cet écart entre deux horloges optiques séparées de 33 cm en hauteur.

**Formule unifiée.** Les géodésiques de la métrique en champ faible donnent, pour un corps de vitesse v quelconque :

```latex
\vec{a}_{\perp} = -\left(1 + \frac{v^2}{c^2}\right)\vec{\nabla}_{\!\perp}\Phi
```

Pour v très petit devant c, on retrouve Newton. Pour v = c, on retrouve le double.

**Lecture mécanique.** Une masse crée autour d'elle une pente de cadence. Tout ce qui avance librement vire vers la zone lente, comme un essieu dont une roue tourne moins vite que l'autre.

La matière lente ne ressent que la pente du temps. La lumière, qui parcourt beaucoup d'espace, ressent aussi la déformation des longueurs : d'où le facteur 2.

### 3.4 Conditions de validité

- Champ faible et statique : les formules sont au premier ordre en GM/(rc²). Près d'un astre compact, il faut l'indice exact ; sous l'horizon, l'image d'un indice ne tient plus.
- L'indice dépend du choix des coordonnées. Seules les comparaisons entre deux lieux sont mesurables : décalage des horloges, retard Shapiro, déviation.
- Le « frein » n'est pas un frottement : aucune énergie n'est dissipée.
- L'analogie décrit comment la lumière et la matière répondent à l'indice. Elle ne dit pas pourquoi une masse le crée : c'est le rôle des équations d'Einstein.
- Hors du cadre : ondes gravitationnelles, expansion de l'univers, masses en rotation.
- L'image d'un vide d'indice variable a été formulée par Einstein (1911), puis par Dicke (1957). Evans, Nandi et Islam (1996) en ont donné la forme exacte pour les champs statiques. C'est une réécriture de la relativité générale, pas une théorie de remplacement.

## Pilier 4 — Le choix retardé de Wheeler et le réel « graduellement donné »

Le formalisme donne raison au refus du cadre binaire : avant la mesure, l'état n'est ni « une route » ni « deux routes », et le choix fait sur Terre ne modifie aucun fait passé. Deux nuances s'imposent. Le choix n'exige pas d'intention consciente, et la lecture participative est une interprétation, pas un théorème.

### 4.1 L'état en transit, le choix de la mesure, les probabilités

**L'état.** Le photon peut contourner la galaxie par la gauche ou par la droite. On note |G⟩ et |D⟩ les deux états correspondants. L'état en transit est leur superposition :

```latex
\begin{aligned}
|\Psi\rangle &= \frac{1}{\sqrt{2}}\left(|G\rangle + e^{i\varphi}|D\rangle\right) \\
\langle G|G\rangle &= \langle D|D\rangle = 1, \qquad \langle G|D\rangle = 0
\end{aligned}
```

La phase φ est le décalage accumulé entre les deux routes. Elle dépend de la différence de longueur des trajets et de la masse de la galaxie.

Cet état n'est pas un tirage « 50 % gauche, 50 % droite ». La phase φ relie les deux termes, et elle est mesurable : c'est ce qui distingue une superposition d'une simple ignorance.

**Premier choix : mesurer la route.** Sur Terre, on pointe un télescope sur chaque image du quasar. Cette mesure est décrite par deux projecteurs :

```latex
\hat{P}_G = |G\rangle\langle G|, \qquad \hat{P}_D = |D\rangle\langle D|, \qquad \hat{P}_G + \hat{P}_D = \hat{1}
```

Chacun est hermitien et vérifie P² = P. La règle de Born donne les probabilités :

```latex
\begin{aligned}
P(G) &= \langle\Psi|\hat{P}_G|\Psi\rangle = \big|\langle G|\Psi\rangle\big|^2 = \left|\frac{1}{\sqrt{2}}\right|^2 = \frac{1}{2} \\
P(D) &= \langle\Psi|\hat{P}_D|\Psi\rangle = \big|\langle D|\Psi\rangle\big|^2 = \left|\frac{e^{i\varphi}}{\sqrt{2}}\right|^2 = \frac{1}{2}
\end{aligned}
```

La phase φ a disparu du résultat : cette mesure n'en apprend rien.

**Second choix : mesurer l'interférence.** On superpose cette fois les deux images sur une lame semi-réfléchissante. La mesure se fait dans une autre base :

```latex
\begin{aligned}
|\pm\rangle &= \frac{1}{\sqrt{2}}\left(|G\rangle \pm |D\rangle\right) \\
\hat{P}_{\pm} &= |\pm\rangle\langle\pm|, \qquad \hat{P}_{+} + \hat{P}_{-} = \hat{1}
\end{aligned}
```

On calcule l'amplitude, puis la probabilité, en utilisant l'orthogonalité de |G⟩ et |D⟩ :

```latex
\begin{aligned}
\langle\pm|\Psi\rangle &= \frac{1}{2}\big(\langle G| \pm \langle D|\big)\big(|G\rangle + e^{i\varphi}|D\rangle\big) = \frac{1 \pm e^{i\varphi}}{2} \\
P(\pm) &= \frac{(1 \pm e^{i\varphi})(1 \pm e^{-i\varphi})}{4} = \frac{1 \pm \cos\varphi}{2}
\end{aligned}
```

Autrement dit P(+) = cos²(φ/2) et P(−) = sin²(φ/2). Cette fois, la phase φ commande tout le résultat.

**Les deux questions sont incompatibles.** Les projecteurs des deux mesures ne commutent pas :

```latex
\hat{P}_G\,\hat{P}_{+} - \hat{P}_{+}\,\hat{P}_G = \frac{1}{2}\big(|G\rangle\langle D| - |D\rangle\langle G|\big) \neq 0
```

Aucun appareil ne peut donc répondre aux deux questions à la fois. C'est la complémentarité de Bohr, dont les relations de Heisenberg sont la forme chiffrée.

**Lecture mécanique.** L'état en transit est un potentiel de réponses, pas une trajectoire. Chaque appareil pose une question différente au même état. Dans le formalisme, rien n'indique que la réponse « gauche » ou « droite » existait avant l'interaction avec le détecteur.

### 4.2 Aucune action ne remonte le temps

Le choix de la mesure ne change ni l'état passé du photon, ni l'état de quoi que ce soit d'autre. Deux résultats l'établissent, et le second est le théorème de non-communication.

**La matrice densité.** Elle rassemble tout ce que l'état permet de prédire. Dans la base gauche-droite :

```latex
\hat{\rho} = |\Psi\rangle\langle\Psi| = \frac{1}{2}\begin{pmatrix} 1 & e^{-i\varphi} \\ e^{i\varphi} & 1 \end{pmatrix}, \qquad P_k = \mathrm{Tr}\big(\hat{\rho}\,\hat{P}_k\big)
```

La diagonale contient les probabilités de route, 1/2 et 1/2. Les termes hors diagonale, appelés cohérences, portent la capacité d'interférer. On vérifie par exemple :

```latex
\mathrm{Tr}\big(\hat{\rho}\,\hat{P}_{+}\big) = \langle +|\hat{\rho}|+\rangle = \frac{1}{4}\big(1 + e^{-i\varphi} + e^{i\varphi} + 1\big) = \frac{1 + \cos\varphi}{2}
```

**Résultat 1 : l'état passé ne dépend pas du choix futur.** Jusqu'à l'instant de la mesure, noté t indice m, l'état suit l'évolution unitaire du pilier 2 :

```latex
\hat{\rho}(t) = \hat{U}(t)\,\hat{\rho}(0)\,\hat{U}^{\dagger}(t) \qquad \text{pour tout } t < t_m
```

Aucun réglage de l'appareil terrestre ne figure dans cette expression. Une mesure faite en chemin aurait donné les mêmes probabilités, quel que soit le choix final.

**Résultat 2 : le choix n'agit sur aucun autre système.** Soit E n'importe quel autre système : un témoin près de la galaxie, un enregistrement, la galaxie elle-même. Le photon P et E ont un état conjoint. On mesure le photon dans une base quelconque, sans communiquer le résultat. L'état de E devient :

```latex
\begin{aligned}
\hat{\rho}_E' &= \mathrm{Tr}_P\Big[\sum_k \big(\hat{P}_k \otimes \hat{1}\big)\,\hat{\rho}_{PE}\,\big(\hat{P}_k \otimes \hat{1}\big)\Big] \\
&= \mathrm{Tr}_P\Big[\Big(\sum_k \hat{P}_k^{\,2} \otimes \hat{1}\Big)\,\hat{\rho}_{PE}\Big] \\
&= \mathrm{Tr}_P\big[\hat{\rho}_{PE}\big] = \hat{\rho}_E
\end{aligned}
```

La trace partielle sur P signifie : « on ignore le photon ». Deux règles justifient les étapes.

- De la première à la deuxième ligne : sous la trace sur P, un opérateur qui n'agit que sur P peut passer d'un bout à l'autre du produit.
- De la deuxième à la troisième : P² = P pour un projecteur, et la somme des projecteurs d'une base vaut l'identité.

La base choisie n'apparaît plus dans le résultat. L'état de E est le même avant et après, que l'on mesure la route ou l'interférence. C'est le théorème de non-communication (Ghirardi, Rimini et Weber, 1980).

**Exemple explicite : un témoin près de la galaxie.** Supposons qu'un système M ait gardé une trace, même partielle, de la route. L'état conjoint est intriqué :

```latex
|\Phi\rangle = \frac{1}{\sqrt{2}}\Big(|G\rangle|m_G\rangle + e^{i\varphi}|D\rangle|m_D\rangle\Big)
```

Si la Terre mesure la route, le témoin se retrouve dans l'état m indice G une fois sur deux, et m indice D une fois sur deux :

```latex
\hat{\rho}_M' = \frac{1}{2}\,|m_G\rangle\langle m_G| + \frac{1}{2}\,|m_D\rangle\langle m_D|
```

Si la Terre mesure l'interférence, on additionne les deux résultats possibles, + et −. Les termes croisés s'annulent entre eux :

```latex
\begin{aligned}
\hat{\rho}_M' &= \sum_{\pm}\frac{1}{4}\Big(|m_G\rangle \pm e^{i\varphi}|m_D\rangle\Big)\Big(\langle m_G| \pm e^{-i\varphi}\langle m_D|\Big) \\
&= \frac{1}{2}\,|m_G\rangle\langle m_G| + \frac{1}{2}\,|m_D\rangle\langle m_D|
\end{aligned}
```

Les deux matrices sont identiques. Le témoin ne peut déceler, ni aujourd'hui ni dans ses archives, ce que l'observateur terrestre a choisi.

**Correction de portée.** Le théorème de non-communication porte sur deux systèmes. Pour le photon seul, il n'y a personne à qui « communiquer » : c'est le résultat 1 qui s'applique. Les deux ensemble donnent l'énoncé exact : aucun fait enregistré, passé ou lointain, ne change avec le choix.

**Rétrodiction n'est pas rétro-action.** Quand le télescope de gauche détecte le photon, on conclut qu'il « est passé par la gauche ». C'est une déduction faite aujourd'hui sur le passé, comme dans une enquête. Aucune grandeur physique du passé n'a été modifiée.

**Lecture mécanique.** Le piège vient d'une hypothèse ajoutée au formalisme : que le photon ait dû « décider », près de la galaxie, d'être onde ou particule. Les équations ne contiennent aucune décision de ce genre. Elles ne disent pas non plus ce qui s'est « réellement » passé en chemin : sur ce point, les interprétations divergent.

### 4.3 Le réel « graduellement donné »

Le mot « graduellement » a deux traductions rigoureuses. Le caractère onde ou particule varie de façon continue, et la connaissance s'accumule clic par clic, à raison d'un bit au plus par photon.

**Ni binaire, ni figé.** Reprenons le témoin de la section 4.2. En ignorant le témoin, l'état du photon seul devient :

```latex
\hat{\rho}_P = \mathrm{Tr}_M\,|\Phi\rangle\langle\Phi| = \frac{1}{2}\begin{pmatrix} 1 & e^{-i\varphi}\langle m_D|m_G\rangle \\ e^{i\varphi}\langle m_G|m_D\rangle & 1 \end{pmatrix}
```

Les cohérences sont multipliées par le recouvrement des deux états du témoin. On note V son module, compris entre 0 et 1, et α sa phase. La probabilité d'interférence devient :

```latex
\begin{aligned}
P(\pm) &= \langle\pm|\hat{\rho}_P|\pm\rangle = \frac{1}{2}\Big[1 \pm V\cos(\varphi + \alpha)\Big] \\
\langle m_G|m_D\rangle &= V\,e^{i\alpha}
\end{aligned}
```

V est la visibilité des franges : le contraste de l'interférence. La distinguabilité mesure, elle, la qualité de l'information de route gardée par le témoin. Les deux sont liées :

```latex
\begin{aligned}
V &= \big|\langle m_G|m_D\rangle\big|, \qquad \mathcal{D} = \sqrt{1 - \big|\langle m_G|m_D\rangle\big|^2} \\
V^2 + \mathcal{D}^2 &= 1
\end{aligned}
```

Dans le cas général, l'égalité devient une inégalité : la somme ne dépasse jamais 1 (Englert, 1996). Entre « tout onde » (V = 1) et « tout particule » (distinguabilité égale à 1), tous les intermédiaires existent.

Le cadre binaire dénoncé par l'intuition est donc bien un piège : la théorie contient un curseur continu, pas un interrupteur.

**Un bit au plus par photon.** Chaque détection donne une réponse parmi deux. L'information qu'un photon apporte sur la phase φ se chiffre par l'information de Fisher, calculée avec p = P(+) = cos²(φ/2) :

```latex
F(\varphi) = \frac{1}{p\,(1 - p)}\left(\frac{dp}{d\varphi}\right)^{2} = \frac{\tfrac{1}{4}\sin^2\varphi}{\cos^2\tfrac{\varphi}{2}\,\sin^2\tfrac{\varphi}{2}} = 1
```

La simplification utilise sin φ = 2 sin(φ/2) cos(φ/2). Après N photons indépendants, la borne de Cramér-Rao limite la précision :

```latex
\Delta\varphi \;\ge\; \frac{1}{\sqrt{N\,F}} = \frac{1}{\sqrt{N}}
```

Pour connaître φ à 0,01 radian près, il faut donc au moins 10 000 photons. Chaque clic met à jour l'état, par la règle de Lüders, et la connaissance, par la règle de Bayes :

```latex
\begin{aligned}
\hat{\rho} \;&\longrightarrow\; \frac{\hat{P}_k\,\hat{\rho}\,\hat{P}_k}{\mathrm{Tr}\big(\hat{\rho}\,\hat{P}_k\big)} \\
p(\varphi\,|\,k_1 \dots k_N) \;&\propto\; p(\varphi)\prod_{j=1}^{N} P(k_j\,|\,\varphi)
\end{aligned}
```

Ces mises à jour ont lieu à l'instant et à l'endroit de chaque interaction. Le réel connu se construit clic par clic : c'est le sens rigoureux de « graduellement donné », et l'idée que Wheeler a résumée par « it from bit ».

**Lecture mécanique.** Comme dans un suivi de projet, l'information arrive par constats successifs, locaux et datés. Chaque constat met à jour l'état du dossier. Aucun constat ne réécrit les constats précédents.

### 4.4 Conditions de validité et nuances

- « Choix » n'exige pas « intention ». Dans l'expérience de Jacques et ses collègues (2007), le choix est tiré par un générateur quantique de nombres aléatoires, sans lien causal possible avec l'entrée du photon dans un interféromètre de 48 m. Les statistiques sont celles de la section 4.1. Ce qui compte physiquement est la configuration de l'appareil au moment de l'interaction.
- Wheeler lui-même écartait la conscience, qui n'a selon lui rien à voir avec le processus quantique. L'essentiel est un acte d'enregistrement irréversible, quel que soit ce qui l'accomplit (« Law without Law », 1983, p. 196).
- Trois lectures s'accordent avec l'intuition : l'univers participatif de Wheeler, la mécanique quantique relationnelle de Rovelli (1996), où les faits sont relatifs aux systèmes qui interagissent, et le QBisme (Fuchs, Mermin et Schack, 2014), où l'état exprime les attentes d'un agent. C'est dans le QBisme que le mot « intention » trouve le mieux sa place.
- D'autres lectures donnent les mêmes prédictions sans élément participatif : l'onde pilote de De Broglie et Bohm, où le photon suit toujours une seule route guidée par une onde qui emprunte les deux, et les mondes multiples d'Everett. L'expérience ne les départage pas.
- Chaves, Lemos et Pienaar (2018) ont montré que les statistiques de l'expérience de Wheeler admettent un modèle causal classique, sans rétro-causalité. L'expérience ne prouve donc pas, à elle seule, que le passé était indéterminé. Une variante proposée par les mêmes auteurs permet en revanche d'exclure ces modèles classiques, à dimension égale.
- La version cosmique reste une expérience de pensée. Les versions réalisées vont du laboratoire (48 m, 2007) aux satellites (jusqu'à 3 500 km, 2017). Pour un vrai quasar, le délai entre les deux images dépasse de très loin le temps de cohérence de la lumière.
- Les formules de la section 4.3 supposent deux routes de même poids, un état conjoint pur et des photons indépendants.

## Pilier 5 — La cristallisation de l'information

L'intuition se formalise en trois temps, tous établis : une question est un potentiel qui se compte en bits, l'interaction inscrit la réponse, et la décohérence la fige en un enregistrement stable et recopié. Deux précisions s'imposent. « Actualiser » et « cristalliser » sont deux temps distincts, et ces équations ne disent pas pourquoi c'est telle réponse qui sort plutôt que l'autre.

&#91;embedded content: trois temps de la mesure · une boucle d'effacement\]

La flèche de retour n'existe qu'entre l'inscription et la question : c'est la gomme quantique. Après la cristallisation, il n'y a plus de retour.

### 5.1 Question = potentiel

**Une question est un jeu de projecteurs.** Poser une question à un système, c'est choisir une mesure, donc une famille de projecteurs comme au pilier 4. La question la plus simple, par oui ou par non, est un seul projecteur : il vaut 1 pour « oui » et 0 pour « non ».

```latex
\hat{P}_k^{\,2} = \hat{P}_k, \qquad \sum_k \hat{P}_k = \hat{1}, \qquad p_k = \mathrm{Tr}\big(\hat{\rho}\,\hat{P}_k\big)
```

**Le potentiel se compte en bits.** Avant la réponse, la question a déjà un contenu mesurable : ce que la réponse apprendra en moyenne. C'est l'entropie de Shannon (1948) des probabilités de réponse :

```latex
H = -\sum_k p_k \log_2 p_k \qquad \text{(en bits)}
```

H vaut 0 quand la réponse est certaine : il n'y a rien à apprendre, donc aucun potentiel. H est maximal quand toutes les réponses sont également probables. Pour le photon du pilier 4 :

| Question posée | Probabilités des deux réponses | Potentiel H |
| --- | --- | --- |
| Route : gauche ou droite | 1/2 et 1/2 | 1 bit |
| Interférence, avec une phase φ de 90° | 1/2 et 1/2 | 1 bit |
| Interférence, avec une phase φ de 60° | 3/4 et 1/4 | 0,81 bit |
| Interférence, avec une phase φ nulle | 1 et 0 | 0 bit |

Le même état porte donc un potentiel différent selon la question. Le potentiel n'est pas une propriété du photon seul : c'est une propriété du couple formé par l'état et la question.

**Le stock est limité.** Pour deux routes, il existe trois questions mutuellement complémentaires : la route, l'interférence, et l'interférence décalée d'un quart de période. Cette troisième question se calcule comme les deux autres :

```latex
|\pm i\rangle = \frac{1}{\sqrt{2}}\big(|G\rangle \pm i\,|D\rangle\big), \qquad p_{\pm i} = \big|\langle\pm i|\Psi\rangle\big|^2 = \frac{1 \pm \sin\varphi}{2}
```

Pour chaque question, l'écart entre les deux probabilités, élevé au carré, vaut 1 si la réponse est certaine et 0 si elle est tirée à pile ou face. La somme sur les trois questions est fixe :

```latex
\underbrace{(p_G - p_D)^2}_{0} \;+\; \underbrace{(p_{+} - p_{-})^2}_{\cos^2\varphi} \;+\; \underbrace{(p_{+i} - p_{-i})^2}_{\sin^2\varphi} \;=\; 1
```

C'est la mesure d'information de Brukner et Zeilinger (1999) : un bit en tout pour un état pur, moins pour un état mélangé. La borne de Holevo (1973) dit la même chose autrement : aucune mesure ne tire plus d'un bit d'un système à deux états.

**Lecture mécanique.** Une question ouverte est un stock de réponses possibles, et H en donne la valeur. Ce stock est borné : un bit pour deux routes. Poser la question complémentaire n'ajoute pas un second bit, elle redistribue le même.

C'est la paire de postulats de Rovelli (1996) : l'information qu'on peut tirer d'un système est limitée, mais on peut toujours lui poser une question nouvelle. C'est aussi le « it from bit » de Wheeler : le réel connu est fait de réponses à des questions par oui ou par non.

### 5.2 Actualiser : l'interaction inscrit la réponse

L'actualisation est une interaction locale qui lie le système à une mémoire. À ce stade, la réponse est inscrite mais pas encore figée : l'inscription reste réversible.

**Le schéma de von Neumann (1932).** Le système S est dans une superposition de réponses k. La mémoire M, par exemple un atome du détecteur, attend dans un état « prêt ». L'interaction est construite pour recopier la réponse dans la mémoire :

```latex
\hat{U}\,\big(|k\rangle|M_0\rangle\big) = |k\rangle|M_k\rangle, \qquad \langle M_j|M_k\rangle = \delta_{jk}
```

L'évolution est linéaire. Appliquée à une superposition, elle donne donc la superposition des copies :

```latex
\hat{U}\,\Big(\sum_k c_k\,|k\rangle\Big)|M_0\rangle = \sum_k c_k\,|k\rangle|M_k\rangle
```

L'état de la mémoire dépend maintenant de celui du système : une corrélation est née. C'est une interaction locale, au point et à l'instant du détecteur, comme au pilier 2.

**Combien d'information est inscrite ?** On la mesure par l'information mutuelle, construite avec l'entropie de von Neumann S = −Tr(ρ log₂ ρ) :

```latex
I(S\!:\!M) = S(\hat{\rho}_S) + S(\hat{\rho}_M) - S(\hat{\rho}_{SM})
```

Pour le photon à deux routes de même poids, le système seul et la mémoire seule valent chacun 1 bit. L'état conjoint est pur et vaut 0 :

```latex
I(S\!:\!M) = 1 + 1 - 0 = 2\ \text{bits}
```

Deux bits, alors qu'un enregistrement ordinaire n'en porterait qu'un. Cet excès signale une corrélation quantique, l'intrication. La mémoire n'indique pas encore « gauche » ou « droite » : elle est elle-même en superposition des deux.

**L'inscription est réversible.** L'opération inverse défait la corrélation :

```latex
\hat{U}^{\dagger}\sum_k c_k\,|k\rangle|M_k\rangle = \Big(\sum_k c_k\,|k\rangle\Big)|M_0\rangle
```

La mémoire revient à son état « prêt » et l'interférence redevient possible. C'est le principe de la gomme quantique, proposée par Scully et Drühl (1982) et réalisée sous cette forme par Kim et ses collègues (2000).

**Lecture mécanique.** L'actualisation ressemble à une écriture au crayon. La réponse est notée, mais on peut encore l'effacer sans laisser de trace. Tant que rien d'autre n'a lu la mémoire, la question peut être retirée.

**Précision sur « actualise = cristallise ».** Le formalisme sépare deux temps que l'intuition réunit. L'inscription est une corrélation réversible. La cristallisation, décrite dans la section suivante, est ce qui la rend définitive.

### 5.3 Cristalliser : décohérence, copies, verrouillage

La réponse devient un fait quand l'environnement lit la mémoire. Trois effets se calculent : les interférences entre réponses s'éteignent, la réponse est recopiée en un très grand nombre d'exemplaires, et une barrière d'énergie la verrouille.

**L'environnement lit la mémoire.** Une mémoire n'est jamais isolée. Des particules de l'environnement, photons ou molécules d'air, la heurtent l'une après l'autre. Chacune repart dans un état qui dépend de ce que la mémoire indique. Après N particules :

```latex
\sum_k c_k\,|k\rangle|M_k\rangle\,|e_0\rangle^{\otimes N} \;\longrightarrow\; |\Omega\rangle = \sum_k c_k\,|k\rangle|M_k\rangle\,|e_k\rangle^{\otimes N}
```

L'exposant ⊗N désigne N particules, chacune dans le même état.

**Premier effet : la décohérence.** Personne ne contrôle l'environnement. On en prend donc la trace partielle, comme au pilier 4 :

```latex
\hat{\rho}_{SM} = \mathrm{Tr}_E\,|\Omega\rangle\langle\Omega| = \sum_{j,k} c_j\,c_k^{*}\;\langle e_k|e_j\rangle^{N}\;|j, M_j\rangle\langle k, M_k|
```

Pour j = k, le facteur vaut 1 : les probabilités ne changent pas. Pour j ≠ k, les cohérences sont multipliées par un recouvrement élevé à la puissance N. Pour deux réponses, on note ε le module de ce recouvrement, inférieur à 1, et ν le nombre de collisions par seconde :

```latex
\big|\langle e_1|e_0\rangle\big|^{N} = \varepsilon^{N} = e^{-N\ln(1/\varepsilon)} = e^{-t/\tau_D}, \qquad \tau_D = \frac{1}{\nu\,\ln(1/\varepsilon)}
```

Les cohérences s'éteignent de façon exponentielle. Il reste un mélange ordinaire de deux enregistrements, et l'information mutuelle tombe de 2 bits à 1 bit :

```latex
\begin{aligned}
\hat{\rho}_{SM} \;&\longrightarrow\; \sum_k |c_k|^2\,|k, M_k\rangle\langle k, M_k| \\
I(S\!:\!M) :\quad 2\ \text{bits} \;&\longrightarrow\; 1\ \text{bit}
\end{aligned}
```

Exemple chiffré : une mémoire de 1 cm² en plein jour reçoit environ 2,5 × 10¹⁷ photons par seconde. Même si chaque photon distingue très mal les deux réponses (ε = 0,999999), les cohérences s'éteignent en 4 × 10⁻¹² s.

Le calcul complet de Joos et Zeh (1985) suit la même loi exponentielle. Pour deux positions x et x' d'un objet, la cohérence décroît à un taux Λ qui dépend de l'environnement. La loi vaut tant que l'écart entre les deux positions reste petit devant la longueur d'onde du rayonnement :

```latex
\rho(x, x', t) = \rho(x, x', 0)\,e^{-\Lambda\,t\,(x - x')^2}
\qquad\Longrightarrow\qquad
\tau_D = \frac{1}{\Lambda\,(x - x')^2}
```

Pour un grain de poussière de 10 micromètres et deux positions distantes de 0,1 micromètre, les taux de leur tableau donnent 10⁻¹¹ s à la lumière du soleil et 10⁻⁹ s sous le seul rayonnement thermique ambiant. Dans le vide interstellaire, où ne reste que le rayonnement cosmologique, il faut tout de même près de trois heures.

**Deuxième effet : la redondance.** Chaque particule emporte une copie partielle de la réponse. Pour deux réponses de même poids, un paquet de m particules en contient :

```latex
I(m) = h\!\left(\frac{1 + \varepsilon^{m}}{2}\right), \qquad h(x) = -x\log_2 x - (1 - x)\log_2(1 - x)
```

Cette quantité tend vers 1 bit quand m grandit. Dans l'exemple précédent, un million de photons portent 90 % du bit. La réponse est donc recopiée plus de cent milliards de fois par seconde.

Chaque observateur peut lire un paquet différent, sans toucher au système, et tous lisent la même réponse. C'est ainsi qu'une réponse devient un fait partagé : Zurek (2009) appelle ce mécanisme le darwinisme quantique. C'est aussi le sens le plus littéral du mot cristal : un même motif répété un très grand nombre de fois.

Ces copies voyagent au plus à la vitesse c. Un fait cristallisé n'est donc disponible que dans le cône de lumière futur de l'événement : la cristallisation reste locale et actuelle, au sens du pilier 2.

**Troisième effet : le verrouillage.** Pour défaire l'enregistrement, il faudrait rattraper toutes les particules et inverser leur trajet. Dans l'exemple, après un milliardième de seconde, il reste moins de 10⁻¹⁰⁰ de la cohérence initiale. L'effacement spontané par l'agitation thermique est bloqué, lui, par une barrière d'énergie ΔE :

```latex
\tau = \tau_0\,e^{\Delta E / k_B T}, \qquad Q_{\text{effacement}} \;\ge\; k_B T\,\ln 2
```

- Durée de vie τ : pour conserver un bit dix ans à température ambiante, avec un temps d'essai de 1 ns, il faut une barrière d'environ 40 fois l'énergie thermique kT, soit 1 eV.
- Coût d'effacement : le principe de Landauer (1961) impose de dissiper au moins kT ln 2 par bit effacé, soit 2,9 × 10⁻²¹ J à 300 K. Bérut et ses collègues (2012) l'ont vérifié expérimentalement.

**Le germe et l'avalanche.** Les détecteurs réels amplifient avant de figer. Dans une émulsion photographique, un amas de trois à cinq atomes d'argent suffit pour que le développement transforme le grain entier : le gain est d'environ cent millions (Belloni, 2002). Le mot cristal est ici à prendre au pied de la lettre, puisque le grain est un cristal d'halogénure d'argent.

Dans un photomultiplicateur, chaque électron arraché par un photon en libère un à dix millions.

**Lecture mécanique.** Cristalliser, c'est passer du crayon à la gravure. La réponse ne peut plus interférer, elle existe en d'innombrables copies, et une barrière d'énergie la protège.

L'image de la solution sursaturée est juste. Le détecteur est un milieu prêt à basculer, et la réponse microscopique en est le germe.

### 5.4 Conditions de validité et nuances

- Deux temps, pas un. « Actualise = cristallise » réunit l'inscription, qui est réversible, et la cristallisation, qui ne l'est plus en pratique. La gomme quantique le montre : une information de route encore non cristallisée peut être effacée, et les franges reviennent.
- La décohérence fige la réponse, elle ne la choisit pas. Les équations donnent un mélange « gauche ou droite » avec les bonnes probabilités. Elles ne disent pas pourquoi une seule réponse est constatée : c'est le « problème des résultats » (Schlosshauer, 2004), auquel les interprétations du pilier 4 répondent différemment.
- L'irréversibilité est pratique, pas de principe. L'évolution de l'ensemble reste unitaire : les cohérences ne sont pas détruites, elles sont diluées dans l'environnement.
- La redondance multiplie les copies, pas l'information. Il y a toujours un seul bit, écrit un très grand nombre de fois.
- « Cristallisation » est une image. Son contenu rigoureux porte trois noms : décohérence (Joos et Zeh, 1985 ; Zurek, 2003), darwinisme quantique (Zurek, 2009) et principe de Landauer (1961). L'image devient littérale dans les modèles où l'appareil subit une transition de phase déclenchée par le système mesuré (Allahverdyan, Balian et Nieuwenhuizen, 2013).
- Ces effets sont observés. Brune et ses collègues (1996) ont suivi la décohérence d'une superposition de quelques photons, d'autant plus rapide que ses composantes sont éloignées. Hornberger et ses collègues (2003) ont vu le contraste des franges de grosses molécules décroître exponentiellement avec la pression du gaz. Unden et ses collègues (2019) ont testé la redondance prévue par le darwinisme quantique.
- Hypothèses du modèle simplifié de la section 5.3 : particules d'environnement identiques et indépendantes, états purs, deux réponses de même poids, mémoire dont les états ne sont pas perturbés par l'environnement.

## Synthèse

Chaque intuition correspond à un résultat établi. Le tableau donne les équations qui la traduisent, les théorèmes correspondants, et la correction ou la limite à retenir.

| Intuition, en langage mécanique | Équations démontrées | Théorèmes et travaux établis | Correction ou limite |
| --- | --- | --- | --- |
| 1. Géométrie de l'observateur : sur un tableau plat, la diagonale s'allonge et le photon doit revenir à la source | Sur le tableau : 1/v = 1/ẋ + sin θ / c, limite c. Vitesse perçue : 1/v = 1/ẋ + 2 sin θ / c, limite c/2. Jets : v sin θ / (1 − (v/c) cos θ) | Échos de lumière (Couderc, 1939). Vitesses apparentes supraluminiques (Rees, 1966) | c/2 est une limite. C'est un plancher pour un balayage rapide, comme dans le cas chiffré, et un plafond seulement si Dω ≤ c/2 |
| 2. Lumière actuelle, émergente, locale : rien ne voyage de A à B, et l'éclat naît à l'impact | Intervalle Δs² = c²Δt² − Δx² négatif et invariant. Taux de détection w = η ⟨E(−)E(+)⟩, pris au point et à l'instant du détecteur | Causalité relativiste (Einstein, Minkowski). Théorie de la photodétection (Glauber, 1963). « Potentia » (Heisenberg, 1958) | La formule de Glauber est une valeur moyenne. En transit, le champ porte énergie et impulsion : « potentiel » ne veut pas dire « rien » |
| 3. Cadence c et masse comme frein : la gravité est une déviation vers la zone lente | Norme de la quadri-vitesse égale à c. Budget : (c dτ/dt)² + v² = c². Horloges : dτ = dt √(1 − 2GM/(rc²)). Indice : n ≈ 1 + 2GM/(rc²). Matière lente : a = −c²∇N. Lumière : déviation 4GM/(bc²) | Espace-temps de Minkowski. Solution de Schwarzschild. Principe de Fermat. Effet Shapiro. Analogie optique (Einstein, 1911 ; Dicke, 1957) | La déviation suit +∇n. Un facteur 2 sépare la lumière de la matière lente. Sur place, la lumière va toujours à c |
| 4. Choix retardé : le choix est local et actuel, et le réel est graduellement donné | Superposition des deux routes avec une phase φ. Probabilités (1 ± cos φ)/2. État de tout autre système inchangé par le choix. Visibilité² + distinguabilité² ≤ 1. Précision Δφ ≥ 1/√N | Règle de Born. Théorème de non-communication (Ghirardi, Rimini, Weber, 1980). Complémentarité (Bohr ; Englert, 1996). Wheeler, Rovelli, QBisme | Le choix n'exige pas d'intention consciente. Les lectures participatives sont des interprétations, que l'expérience ne départage pas |
| 5. Cristallisation de l'information : la question est un potentiel, et l'actualisation fige la réponse | Potentiel H = −Σ p log₂ p, borné à 1 bit pour deux routes. Inscription : 2 bits de corrélation quantique, réversibles. Cristallisation : cohérence multipliée par ε à la puissance N, soit exp(−t/τ) ; il reste 1 bit classique, recopié dans l'environnement | Entropie de Shannon. Borne de Holevo. Schéma de mesure de von Neumann. Décohérence (Zeh, Zurek). Darwinisme quantique (Zurek, 2009). Principe de Landauer (1961) | Inscrire et cristalliser sont deux temps distincts. La décohérence fige la réponse mais ne la choisit pas. L'irréversibilité est pratique, pas de principe |

Une fois ces corrections faites, le modèle ne contredit aucun résultat établi : il reformule des résultats connus en langage de flux et de délais. Pour devenir une théorie à part entière, il lui faudrait une prédiction chiffrée qui diffère de la physique standard.

## Références

Chaque référence a été contrôlée sur la page liée : éditeur, archive ouverte ou copie institutionnelle. L'article de Couderc, le détail de celui de Dicke et le tableau de Joos et Zeh n'ont pu être contrôlés que sur des sources secondaires. Les valeurs chiffrées sans référence sont calculées à partir des formules du document.

**Pilier 1**

- Couderc, P. (1939). « Les auréoles lumineuses des novae ». Annales d'Astrophysique 2, 271–302. Cité et résumé par [R. Tylenda, « On the light echo in V838 Mon »](https://ar5iv.labs.arxiv.org/html/astro-ph/0306555).
- Rees, M. J. (1966). [Appearance of Relativistically Expanding Radio Sources](https://www.nature.com/articles/211468a0). Nature 211, 468–470.
- Nemiroff, R. J. (2015). [Superluminal Spot Pair Events in Astronomical Settings: Sweeping Beams](https://arxiv.org/abs/1412.7581). Publications of the Astronomical Society of Australia 32, e001.

**Pilier 2**

- Minkowski, H. (1909). [Raum und Zeit](https://www.minkowskiinstitute.org/mip/MinkowskiFreemiumMIP2012.pdf), conférence de Cologne du 21 septembre 1908. Physikalische Zeitschrift 10, 104–111.
- Glauber, R. J. (1963). [The Quantum Theory of Optical Coherence](https://journals.aps.org/pr/abstract/10.1103/PhysRev.130.2529). Physical Review 130, 2529–2539.
- Grangier, P., Roger, G., Aspect, A. (1986). [Experimental Evidence for a Photon Anticorrelation Effect on a Beam Splitter](https://iopscience.iop.org/article/10.1209/0295-5075/1/4/004). Europhysics Letters 1, 173–179.
- Newton, T. D., Wigner, E. P. (1949). [Localized States for Elementary Systems](https://journals.aps.org/rmp/abstract/10.1103/RevModPhys.21.400). Reviews of Modern Physics 21, 400–406.
- ATLAS Collaboration (2017). [Evidence for light-by-light scattering in heavy-ion collisions with the ATLAS detector at the LHC](https://www.nature.com/articles/nphys4208). Nature Physics 13, 852–858.
- Heisenberg, W. (1958). Physics and Philosophy: The Revolution in Modern Science. Harper & Brothers, New York. La notion de « potentia » figure au chapitre 2.

**Pilier 3**

- Einstein, A. (1911). [Über den Einfluß der Schwerkraft auf die Ausbreitung des Lichtes](https://zenodo.org/records/1424213). Annalen der Physik 35, 898–908.
- Einstein, A. (1916). [Die Grundlage der allgemeinen Relativitätstheorie](https://zenodo.org/records/1424302). Annalen der Physik 49, 769–822.
- Dyson, F. W., Eddington, A. S., Davidson, C. (1920). [A Determination of the Deflection of Light by the Sun's Gravitational Field](https://zenodo.org/records/1432106). Philosophical Transactions of the Royal Society A 220, 291–333.
- Dicke, R. H. (1957). [Gravitation without a Principle of Equivalence](https://journals.aps.org/rmp/abstract/10.1103/RevModPhys.29.363). Reviews of Modern Physics 29, 363–376.
- Shapiro, I. I. (1964). [Fourth Test of General Relativity](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.13.789). Physical Review Letters 13, 789–791.
- Bertotti, B., Iess, L., Tortora, P. (2003). [A test of general relativity using radio links with the Cassini spacecraft](https://www.nature.com/articles/nature01997). Nature 425, 374–376.
- Chou, C. W., Hume, D. B., Rosenband, T., Wineland, D. J. (2010). [Optical Clocks and Relativity](https://tf.nist.gov/general/pdf/2447.pdf). Science 329, 1630–1633.
- Evans, J., Nandi, K. K., Islam, A. (1996). [The optical-mechanical analogy in general relativity](https://link.springer.com/article/10.1007/BF02105085). General Relativity and Gravitation 28, 413–439.

**Pilier 4**

- Wheeler, J. A. (1978). [The “Past” and the “Delayed-Choice” Double-Slit Experiment](https://doi.org/10.1016/B978-0-12-473250-6.50006-6). Dans A. R. Marlow (dir.), Mathematical Foundations of Quantum Theory, Academic Press, p. 9–48.
- Wheeler, J. A. (1983). « Law without Law ». Dans J. A. Wheeler et W. H. Zurek (dir.), Quantum Theory and Measurement, Princeton University Press, p. 182–213.
- Wheeler, J. A. (1990). « Information, Physics, Quantum: The Search for Links ». Dans W. H. Zurek (dir.), Complexity, Entropy, and the Physics of Information, Addison-Wesley.
- Ghirardi, G. C., Rimini, A., Weber, T. (1980). [A general argument against superluminal transmission through the quantum mechanical measurement process](https://link.springer.com/article/10.1007/BF02817189). Lettere al Nuovo Cimento 27, 293–298.
- Englert, B.-G. (1996). [Fringe Visibility and Which-Way Information: An Inequality](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.77.2154). Physical Review Letters 77, 2154–2157.
- Jacques, V., et al. (2007). [Experimental Realization of Wheeler's Delayed-Choice Gedanken Experiment](https://arxiv.org/abs/quant-ph/0610241). Science 315, 966–968.
- Vedovato, F., et al. (2017). [Extending Wheeler's delayed-choice experiment to space](https://arxiv.org/abs/1704.01911). Science Advances 3, e1701180.
- Chaves, R., Lemos, G. B., Pienaar, J. (2018). [Causal Modeling the Delayed-Choice Experiment](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.120.190401). Physical Review Letters 120, 190401.
- Rovelli, C. (1996). [Relational quantum mechanics](https://arxiv.org/abs/quant-ph/9609002). International Journal of Theoretical Physics 35, 1637–1678.
- Fuchs, C. A., Mermin, N. D., Schack, R. (2014). [An introduction to QBism with an application to the locality of quantum mechanics](https://arxiv.org/abs/1311.5253). American Journal of Physics 82, 749–754.
- Ma, X.-S., Kofler, J., Zeilinger, A. (2016). [Delayed-choice gedanken experiments and their realizations](https://journals.aps.org/rmp/abstract/10.1103/RevModPhys.88.015005). Reviews of Modern Physics 88, 015005. Synthèse des expériences réalisées.

**Pilier 5**

- Shannon, C. E. (1948). [A Mathematical Theory of Communication](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf). Bell System Technical Journal 27, 379–423 et 623–656.
- Holevo, A. S. (1973). [Bounds for the quantity of information transmitted by a quantum communication channel](https://www.mathnet.ru/eng/ppi903). Problems of Information Transmission 9, 177–183.
- Brukner, Č., Zeilinger, A. (1999). [Operationally Invariant Information in Quantum Measurements](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.83.3354). Physical Review Letters 83, 3354–3357.
- von Neumann, J. (1932). Mathematische Grundlagen der Quantenmechanik. Springer, Berlin. [Notice de catalogue](https://ci.nii.ac.jp/ncid/BA04044067?l=en).
- Scully, M. O., Drühl, K. (1982). [Quantum eraser: A proposed photon correlation experiment concerning observation and “delayed choice” in quantum mechanics](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.25.2208). Physical Review A 25, 2208–2213.
- Kim, Y.-H., Yu, R., Kulik, S. P., Shih, Y., Scully, M. O. (2000). [Delayed “Choice” Quantum Eraser](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.84.1). Physical Review Letters 84, 1–5.
- Joos, E., Zeh, H. D. (1985). [The emergence of classical properties through interaction with the environment](https://link.springer.com/article/10.1007/BF01725541). Zeitschrift für Physik B 59, 223–243. Tableau des taux lu dans [Kiefer et Joos, « Decoherence: Concepts and Examples »](https://ar5iv.labs.arxiv.org/html/quant-ph/9803052).
- Zurek, W. H. (2003). [Decoherence, einselection, and the quantum origins of the classical](https://journals.aps.org/rmp/abstract/10.1103/RevModPhys.75.715). Reviews of Modern Physics 75, 715–775.
- Schlosshauer, M. (2004). [Decoherence, the measurement problem, and interpretations of quantum mechanics](https://journals.aps.org/rmp/abstract/10.1103/RevModPhys.76.1267). Reviews of Modern Physics 76, 1267–1305.
- Zurek, W. H. (2009). [Quantum Darwinism](https://www.nature.com/articles/nphys1202). Nature Physics 5, 181–188.
- Unden, T. K., et al. (2019). [Revealing the Emergence of Classicality Using Nitrogen-Vacancy Centers](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.123.140402). Physical Review Letters 123, 140402.
- Brune, M., et al. (1996). [Observing the Progressive Decoherence of the “Meter” in a Quantum Measurement](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.77.4887). Physical Review Letters 77, 4887–4890.
- Hornberger, K., et al. (2003). [Collisional Decoherence Observed in Matter Wave Interferometry](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.90.160401). Physical Review Letters 90, 160401.
- Landauer, R. (1961). « Irreversibility and Heat Generation in the Computing Process ». IBM Journal of Research and Development 5, 183–191. DOI 10.1147/rd.53.0183.
- Bérut, A., et al. (2012). [Experimental verification of Landauer's principle linking information and thermodynamics](https://www.nature.com/articles/nature10872). Nature 483, 187–189.
- Allahverdyan, A. E., Balian, R., Nieuwenhuizen, T. M. (2013). [Understanding quantum measurement from the solution of dynamical models](https://arxiv.org/abs/1107.2138). Physics Reports 525, 1–166.
- Belloni, J. (2002). [The role of silver clusters in photography](<https://comptes-rendus.academie-sciences.fr/physique/item/10.1016/S1631-0705(02)01321-X.pdf>). Comptes Rendus Physique 3, 381–390.
- Gain des photomultiplicateurs : [page technique d'Evident Scientific](https://evidentscientific.com/en/microscope-resource/knowledge-hub/digitalimaging/concepts/photomultipliers).
