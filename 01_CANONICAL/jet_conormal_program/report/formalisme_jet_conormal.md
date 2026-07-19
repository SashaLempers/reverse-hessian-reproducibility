# Programme jet–conormal au-delà du Hessien classique

## 1. Diagnostic

Le Hessien classique est le premier différentiel du morphisme de Gauss. Une généralisation naïve consiste à utiliser les matrices mixtes

\[
\mathsf H_{a,b}(f)(u,v)=(uv)\cdot f,
\qquad
\mathsf H_{a,b}(f):S^aV\longrightarrow S^bV^*\otimes S^{d-a-b}V^*.
\]

Elles sont fonctorielles : pour une application linéaire \(B:W\to V\),

\[
\mathsf H_{a,b}(f\circ B)
=(S^aB)^T\bigl(\mathsf H_{a,b}(f)\circ B\bigr)(S^bB).
\]

Leurs mineurs sont donc des covariants réguliers compatibles avec les projections linéaires. Cependant, la déficience de rang spéciale du déterminant disparaît dès l'ordre trois.

## 2. Théorème de saturation du troisième jet du déterminant

Soit \(X_0=\operatorname{diag}(I_{n-1},0)\), avec \(n\ge3\). Écrivons une perturbation comme

\[
Y=\begin{pmatrix}A&b\\c^T&d\end{pmatrix}.
\]

La partie homogène d'ordre \(t\), pour \(2\le t\le n\), de
\(\det(X_0+Y)\) vaut

\[
P_t(A,b,c,d)
=d\,e_{t-1}(A)-c^TQ_{t-2}(A)b,
\]

où \(e_j(A)\) est la composante homogène de degré \(j\) de
\(\det(I+A)\), et \(Q_j(A)\) celle de degré \(j\) de
\(\operatorname{adj}(I+A)\).

**Proposition.** Pour tout \(3\le t\le n\), \(P_t\) est concise dans les
\(n^2\) variables. Équivalemment,

\[
\operatorname{rank}\operatorname{Flat}_{1,t-1}
\bigl(d^t\det_n\vert_{X_0}\bigr)=n^2.
\]

**Preuve.** Supposons qu'une direction constante
\((\Delta A,\Delta b,\Delta c,\Delta d)\) annule la dérivée directionnelle de
\(P_t\). Les monômes ne contenant que \(A\) imposent \(\Delta d=0\). Les
termes contenant \(d\) imposent
\(D_{\Delta A}e_{t-1}(A)=0\). Le polynôme \(e_k\) est concise sur l'espace des
matrices pour \(2\le k\le n-1\) : sa restriction aux matrices diagonales tue
les composantes diagonales de \(\Delta A\), puis le coefficient du monôme
\(A_{ji}\prod_{s\in S}A_{ss}\) isole chaque composante hors diagonale
\(\Delta A_{ij}\). Ainsi \(\Delta A=0\). Enfin,

\[
Q_{t-2}(\lambda I)
=\binom{n-2}{t-2}\lambda^{t-2}I,
\]

ce qui impose successivement \(\Delta b=0\) et \(\Delta c=0\). Il n'existe
donc aucune variable inessentielle. ∎

Conséquence : les flattenings bruts des dérivées d'ordre supérieur ne peuvent
pas simplement prolonger le défaut de rang \(2n\) du Hessien sur la strate de
rang \(n-1\). Il faut quotienter les informations déjà visibles aux étages
inférieurs.

## 3. Contrôle exact du premier cas paddé

Pour \(\det_4\) au point \(\operatorname{diag}(I_3,0)\), et
\(\ell\operatorname{per}_3\) au point
\(\ell=1\), \(X=J_3-3E_{11}\), les rangs exacts sont :

| jet et split | \(\det_4\) | \(\ell\operatorname{per}_3\) |
|---|---:|---:|
| ordre 2, \(1|1\) | 8 | 9 |
| ordre 3, \(1|2\) | 16 | 10 |
| ordre 4, \(1|3\) | 16 | 10 |
| ordre 4, \(2|2\) | 36 | 18 |

L'unique inversion favorable est donc celle du Hessien classique.

Les premières syzygies jacobiennes linéaires exactes vont également dans la
mauvaise direction : \(30\) pour \(\det_4\), contre \(101\) pour la forme
paddée si l'on conserve les seize générateurs ambiants. Parmi ces \(101\),
\(96\) proviennent des six dérivées identiquement nulles; après retrait de ces
sommets triviaux, il reste seulement \(5\) syzygies linéaires intrinsèques.

## 4. Nouvel objet : la tour conormale jet–syzygétique

Soit \(R=\mathbf C[V]\), \(J_f=(f_1,\dots,f_N)\) l'idéal jacobien, et
introduisons des coordonnées duales \(y_1,\dots,y_N\). Le graphe projectif du
morphisme polaire est décrit, avant saturation, par

\[
\mathscr G_f=
\bigl(f,\ y_if_j-y_jf_i\;:\;1\le i<j\le N\bigr)
\subset \mathbf C[x,y].
\]

Après saturation par l'idéal jacobien et les idéaux non pertinents, on obtient
le schéma conormal/Gauss. Cette construction ne s'annule pas sous padding : si
\(f\) ne dépend pas d'une variable \(u\), les équations imposent simplement
\(y_u=0\) sur le lieu où le gradient est non nul.

La donnée centrale devient la résolution bigraduée de la Rees-algèbre

\[
\mathcal R(J_f)=\bigoplus_{q\ge0}J_f^qt^q,
\]

ainsi que les voisinages infinitésimaux du graphe de Gauss. Les Hessiennes
supérieures sont alors les jets du graphe; les syzygies jacobiennes sont ses
équations; les décompositions de Schur découpent les différentielles en blocs
calculables.

## 5. Invariant de rang certifiable

Pour chaque degré bigradué \((a,b)\), degré homologique \(p\), profondeur de
jet \(s\) et type de Schur \(\lambda\), on construit une matrice dans des
espaces fixes

\[
\mathcal M^{(s)}_{p,\lambda;a,b}(f).
\]

Ses coefficients sont polynomiaux dans ceux de \(f\). Une inégalité

\[
\operatorname{rank}\mathcal M^{(s)}_{p,\lambda;a,b}
(\ell^{n-m}\operatorname{per}_m)
>
\operatorname{rank}\mathcal M^{(s)}_{p,\lambda;a,b}(\det_n)
\]

fournit donc une condition déterminantale fermée dans la bonne direction.
Les tables de Betti servent à découvrir le bloc, mais la certification finale
doit toujours être réécrite comme le rang d'une matrice universelle fixe; cela
évite les difficultés de platitude et de saturation fibre par fibre.

## 6. Rôle exact de la théorie des représentations

Une simple partition présente d'un côté et absente de l'autre est une
obstruction d'occurrence. Cette stratégie est connue pour être insuffisante
dans le régime asymptotique GCT pertinent. La cible correcte est un écart de
multiplicité, ou mieux un saut de rang dans un espace de multiplicité :

\[
\operatorname{rank}\mathcal M_{\lambda}(\text{permanent paddé})
>
\operatorname{rank}\mathcal M_{\lambda}(\determinant).
\]

La décomposition de Schur est donc utilisée comme microscope et comme outil de
compression, non comme garantie automatique d'une obstruction.

## 7. Programme de calcul

1. Construire les brins bigradués de \(\mathscr G_f\) et leurs premières
   syzygies pour \(\det_4\) et \(\ell\operatorname{per}_3\).
2. Séparer explicitement les sommants de Koszul et les sommants dus aux
   variables inutilisées, tout en conservant une matrice finale dans l'espace
   ambiant fixe.
3. Calculer les premiers voisinages conormaux
   \(\mathscr G_f^s/\mathscr G_f^{s+1}\), d'abord pour \(s=1,2\).
4. Décomposer chaque différentiel sous \(GL_4\times GL_4\) côté déterminant,
   puis reconstruire le rang global \(GL_{16}\)-invariant.
5. Chercher un bloc dont le rang est plus élevé côté permanent paddé; produire
   alors un mineur entier non nul côté permanent et un noyau symbolique côté
   déterminant.
6. Asymptotiser le bloc en utilisant la résolution déterminantale/Segre côté
   déterminant et un témoin uniforme côté permanent.

## 8. Statut

Le paquet ne prétend pas avoir obtenu une nouvelle borne. Il établit un
résultat négatif utile — la saturation des jets bruts dès l'ordre trois — et
fournit le formalisme précis qui combine les trois directions proposées sans
perdre la fermeture de Zariski nécessaire à la complexité bordée.
