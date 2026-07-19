# Mineurs hessiens composés, flattenings de Young et idéaux de Fitting

## Cas étudié

Le calcul porte sur le premier cas paddé non trivial choisi, de tailles `M=4` et `m=3`, où les deux formes ont le même degré et le même espace ambiant :

\[
\det_4\in \operatorname{Sym}^4(\mathbf C^{16})^*,
\qquad
F=z\,\operatorname{per}_3\in \operatorname{Sym}^4(\mathbf C^{16})^*.
\]

La forme `F` dépend de dix variables actives — `z` et les neuf entrées du permanent — et de six directions ambiantes inutilisées. Pour une forme quartique `f`, on note

\[
\Phi_r(f)=C_r(\operatorname{Hess} f),
\]

où `C_r` est la matrice composée constituée de tous les mineurs `r × r` du Hessien. Les entrées de `\Phi_r(f)` sont homogènes de degré `2r`.

L’objectif était de mettre en œuvre trois familles d’obstructions fermées :

1. les catalecticants et flattenings de Young de `\Phi_r(f)` ;
2. les composantes de Schur autorisées par la covariance ;
3. les pièces graduées de l’idéal engendré par les mineurs hessiens.

## Verdict

**La construction anti-padding fonctionne : `\Phi_2(z\operatorname{per}_3)` est non nulle. En revanche, aucune des obstructions de rang calculées ne sépare le permanent paddé de la clôture d’orbite du déterminant. Toutes les inégalités obtenues vont dans la direction opposée :**

\[
\operatorname{rang}(\text{observable sur }z\operatorname{per}_3)
<
\operatorname{rang}(\text{même observable sur }\det_4).
\]

Ce résultat ne prouve aucune inclusion de clôtures. Il élimine rigoureusement les tests précis qui ont été calculés.

## 1. Hessien composé d’ordre `r=2`

La matrice `C_2(Hess f)` possède `7260` coordonnées symétriques dans l’espace ambiant de dimension `16`.

| forme | coordonnées non nulles | polynômes non nuls distincts à scalaire près |
|---|---:|---:|
| `det_4` | 4032 | 1152 |
| `z per_3` | 540 | 213 |

Ainsi, contrairement au déterminant hessien total, le covariant composé ne s’annule pas sous le padding.

### Catalecticants vectoriels

Pour les ordres `k=0,1,2`, les rangs sur `Q` sont exacts :

| ordre `k` | `det_4` | `z per_3` |
|---:|---:|---:|
| 0 | 1 | 1 |
| 1 | 16 | 10 |
| 2 | 136 | 55 |

Les rangs ont été calculés modulo `1009`, `10007` et `32003`. Aux ordres `1` et `2`, ils atteignent la borne supérieure donnée par le nombre de variables actives ; cela certifie les rangs rationnels exacts.

## 2. Goulot d’étranglement de Schur

Le tenseur des mineurs `2 × 2` d’une matrice symétrique satisfait l’identité de Bianchi algébrique et appartient au facteur `S_(2,2)V*`. La polarisation de la construction donne une application équivariante

\[
\operatorname{Sym}^2(\operatorname{Sym}^4 V^*)
\longrightarrow
S_{(2,2)}V^*\otimes \operatorname{Sym}^4V^*.
\]

Les décompositions exactes sont

\[
\operatorname{Sym}^2(\operatorname{Sym}^4V^*)
=
S_{(8)}V^*\oplus S_{(6,2)}V^*\oplus S_{(4,4)}V^*,
\]

et, par Pieri,

\[
S_{(2,2)}V^*\otimes S_{(4)}V^*
=
S_{(6,2)}V^*\oplus S_{(5,2,1)}V^*\oplus S_{(4,2,2)}V^*.
\]

Le seul facteur commun est donc

\[
\boxed{S_{(6,2)}V^*.}
\]

En particulier, projeter `\Phi_2(f)` sur les composantes isotypiques ordinaires ne peut produire plusieurs blocs concurrents : la construction est forcée dans un seul module irréductible. Cette conclusion est théorique, et les symétriseurs de Young l’ont également vérifiée sur les tenseurs calculés.

## 3. Les quatre flattenings de Young à deux cases

Pour un tenseur de type `S_(6,2)`, les règles de Littlewood–Richardson autorisent exactement quatre types de flattenings obtenus en séparant deux cases :

\[
S_{(2)}V\to S_{(4,2)}V^*,\qquad
S_{(2)}V\to S_{(5,1)}V^*,\qquad
S_{(2)}V\to S_{(6)}V^*,\qquad
S_{(1,1)}V\to S_{(5,1)}V^*.
\]

Ils ont tous été réalisés par polarisation complète, contraction de slots et symétriseurs de Young entiers.

| source | cible | rang `det_4` | rang `z per_3` | conclusion |
|---|---|---:|---:|---|
| `S_(2)` | `S_(4,2)` | 136 | 55 | mauvaise direction |
| `S_(2)` | `S_(5,1)` | 36 | 18 | mauvaise direction |
| `S_(2)` | `S_(6)` | 136 | 55 | mauvaise direction |
| `S_(1,1)` | `S_(5,1)` | 120 | 45 | mauvaise direction |

Les rangs `136`, `120`, `55` et `45` atteignent les dimensions maximales de leurs espaces sources actifs. Le rang `18` du permanent a été calculé exactement sur `Q` par une matrice sparse de taille `136 × 64800`.

Le rang `36` du déterminant possède en plus un certificat de représentation. Avec `V=A\otimes B`, `dim A=dim B=4`,

\[
\operatorname{Sym}^2(A\otimes B)
=
(\operatorname{Sym}^2A\otimes\operatorname{Sym}^2B)
\oplus
(\wedge^2A\otimes\wedge^2B),
\]

avec dimensions `100` et `36`. Le flattening `S_(2)→S_(5,1)` annule exactement un vecteur de plus haut poids du premier facteur et est non nul sur un vecteur de plus haut poids du second. Par équivariance et irréductibilité, son rang est donc exactement `36`.

**Conclusion exhaustive à ce niveau : aucun flattening de Young à deux cases de `\Phi_2` ne peut fournir l’obstruction recherchée dans le cas `det_4` contre `z per_3`.**

## 4. Pièces graduées de l’idéal de Fitting hessien

Soit `I_2(f)` l’idéal engendré par les mineurs `2 × 2` du Hessien. Les dimensions des trois premières pièces ont été calculées exactement sur `Q` :

| degré | `dim [I_2(det_4)]_d` | `dim [I_2(z per_3)]_d` |
|---:|---:|---:|
| 4 | 625 | 166 |
| 5 | 5312 | 1908 |
| 6 | 27608 | 12156 |

Chaque valeur est le rang exact d’une matrice de multiplication sparse sur les entiers, calculé par `DomainMatrix` puis interprété sur `Q`. Ici encore, le permanent paddé présente la plus petite pièce graduée, ce qui est compatible avec une dégénérescence et ne l’exclut pas.

## 5. Premier contrôle à `r=3`

Pour les mineurs `3 × 3`, la décomposition plethystique/Pieri exacte ne laisse qu’un facteur commun de multiplicité un :

\[
S_{(8,2,2)}V^*.
\]

La pièce génératrice de degré `6` de l’idéal `I_3` donne :

\[
\dim[I_3(z\operatorname{per}_3)]_6=849
\]

exactement sur `Q`, tandis qu’un calcul exhaustif modulo `1009` donne

\[
\dim[I_3(\det_4)]_6\ge 6832
\]

sur `Q`. Le second nombre est une borne inférieure rigoureuse, car le rang d’une matrice entière modulo un nombre premier ne dépasse jamais son rang rationnel.

Le passage de `r=2` à `r=3` ne renverse donc pas la direction de l’obstruction au degré générateur.

## Ce qui a réellement été obtenu

- un covariant polynomial qui survit aux six variables inutilisées du padding ;
- une classification représentationnelle exacte du covariant `r=2` comme tenseur de type `S_(6,2)` ;
- l’examen exhaustif des quatre flattenings de Young à deux cases de ce tenseur ;
- les dimensions exactes de trois pièces de l’idéal hessien `I_2` ;
- un contrôle `r=3` exact côté permanent et une borne inférieure forte côté déterminant ;
- une archive de scripts, certificats et témoins permettant de reconstruire les calculs.

## Ce qui n’est pas obtenu

- aucune séparation de clôtures d’orbites dans le cas paddé ;
- aucune borne inférieure de complexité déterminantale ;
- aucune conséquence pour `VP` contre `VNP` ;
- aucune affirmation de nouveauté bibliographique pour les décompositions de Schur utilisées.

## Prochaine cible rationnelle

Le calcul montre précisément où ne plus chercher. Les projections isotypiques ordinaires et tous les splits de deux cases de `S_(6,2)` sont épuisés. Les prochaines familles non redondantes sont :

1. les flattenings de Littlewood–Richardson avec source `S_(2,1)` ou des splits de quatre cases du tenseur `S_(6,2)` ;
2. les flattenings guidés par `S_(8,2,2)` pour `r=3` ;
3. les syzygies et nombres de Betti des idéaux `I_r`, plus fins que leurs seules fonctions de Hilbert initiales ;
4. des invariants de schémas d’incidence du Hessien qui ne soient pas dominés par le nombre de variables actives.

## Références de contexte

- J. M. Landsberg, G. Ottaviani, *Equations for secant varieties to Veronese varieties*, arXiv:1006.0180.
- J. M. Landsberg, G. Ottaviani, *Equations for secant varieties via vector bundles*, arXiv:1010.1825.
- A. Dimca, G. Sticlaru, *Hessian ideals of a homogeneous polynomial and generalized Tjurina algebras*, Documenta Mathematica 20 (2015), 689–705, DOI 10.4171/DM/502.
- P. Bürgisser, C. Ikenmeyer, G. Panova, *No occurrence obstructions in geometric complexity theory*, JAMS 32 (2019), 163–193, DOI 10.1090/jams/908.
