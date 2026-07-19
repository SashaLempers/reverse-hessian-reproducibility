# Renversement de rang dans la tour de Fitting du Hessien

## Résultat

Soit

\[
V=\mathbf C^{16},\qquad
F=z\,\operatorname{per}_3\in \operatorname{Sym}^4(V^*).
\]

Le calcul et l'argument algébrique contenus dans ce paquet établissent

\[
\boxed{
[F]\notin \overline{GL(V)\cdot[\det_4]}.
}
\]

L'obstruction n'est pas le rang total des premières pièces de l'idéal
\(I_2\) ni un flattening binaire de \(\Phi_3\). Elle apparaît dans une
sous-pièce beaucoup plus profonde de la même tour déterminantale : le
neuvième composé du Hessien, réduit modulo le polynôme lui-même.

Aucune revendication de nouveauté bibliographique n'est faite ici. Le résultat
est présenté comme un théorème exact, autonome et reproductible pour le cas
pilote \(\det_4\) contre \(z\operatorname{per}_3\).

## 1. Le covariant quotient-Fitting

Pour une quartique non nulle \(f\in S_4:=\operatorname{Sym}^4(V^*)\), posons

\[
H_f=\operatorname{Hess}(f),
\qquad
\Phi_9(f)=C_9(H_f).
\]

Les coordonnées de \(\Phi_9(f)\) sont tous les mineurs \(9\times9\) du
Hessien. Comme les entrées de \(H_f\) ont degré \(2\), ces coordonnées
appartiennent à \(S_{18}\).

Avec

\[
A_9=\bigwedge^9V^*\otimes\bigwedge^9V^*,
\]

on peut écrire

\[
\Phi_9(f)\in A_9\otimes S_{18}.
\]

La classe réellement pertinente est

\[
\Theta_9(f):=[\Phi_9(f)]
\in A_9\otimes (S/(f))_{18}.
\]

Cette notation à quotient variable se remplace par un rang universel fixe.
Considérons la multiplication

\[
\mu_f:A_9\otimes S_{14}\longrightarrow A_9\otimes S_{18},
\qquad Q\longmapsto fQ,
\]

et la matrice augmentée

\[
\mathcal A_9(f)=\bigl[\,\mu_f\mid\Phi_9(f)\,\bigr].
\]

Comme l'anneau des polynômes est intègre, \(\mu_f\) est injective pour tout
\(f\ne0\). Son rang

\[
N=\dim(A_9)\dim(S_{14})
\]

est donc constant. Par conséquent,

\[
\Theta_9(f)=0
\iff
\operatorname{rang}\mathcal A_9(f)=N,
\]

et

\[
\Theta_9(f)\ne0
\iff
\operatorname{rang}\mathcal A_9(f)=N+1.
\]

Avec les mineurs ordonnés utilisés dans le certificat,

\[
\dim A_9=\binom{16}{9}^2=130\,873\,600,
\]

\[
\dim S_{14}=\binom{29}{14}=77\,558\,760,
\]

et

\[
N=10\,150\,394\,132\,736\,000.
\]

La taille de cette matrice n'est pas un obstacle à la certification : la
différence de rang est équivalente à une question de divisibilité, qui se
vérifie par la géométrie du lieu zéro et par un seul témoin entier.

Enfin,

\[
I_9(H_f)\subseteq I_2(H_f),
\]

comme pour toute matrice. L'obstruction est donc bien une sous-pièce de degré
\(18\) située profondément dans la tour de Fitting issue de \(I_2\), plutôt
qu'un invariant étranger au programme initial.

## 2. Pourquoi la condition est fermée et équivariante

La condition

\[
\Phi_9(f)\in f\,(A_9\otimes S_{14})
\]

équivaut à

\[
\operatorname{rang}\mathcal A_9(f)\le N.
\]

Elle est donc définie par l'annulation de tous les mineurs de taille
\(N+1\) de la matrice augmentée. Ses entrées dépendent polynomialement des
coefficients de \(f\). Il s'agit ainsi d'un fermé de Zariski dans l'espace
projectif des quartiques.

Pour \(g\in GL(V)\), la règle de chaîne donne une congruence du Hessien :

\[
H_{g\cdot f}(x)
=
J_g^{\mathsf T}\,H_f(g^{-1}x)\,J_g
\]

à convention d'action près. Cauchy--Binet montre alors que les mineurs
\(9\times9\) sont transformés par des applications linéaires inversibles sur
\(A_9\), tandis que la divisibilité par \(f\) devient la divisibilité par
\(g\cdot f\). La condition est donc \(GL(V)\)-invariante.

Elle contient l'orbite de \(\det_4\) si elle contient \(\det_4\), puis elle
contient automatiquement sa clôture.

## 3. Côté déterminant : rang hessien au plus huit sur \(\det_4=0\)

Le groupe \(GL_4\times GL_4\) agit transitivement sur chaque strate de rang
des matrices \(4\times4\). Il suffit donc de regarder les matrices
canoniques

\[
X_s=\operatorname{diag}(I_s,0),\qquad 0\le s\le4.
\]

Le calcul exact donne les rangs hessiens

\[
0,\ 0,\ 4,\ 8,\ 16
\]

pour les strates matricielles de rang \(0,1,2,3,4\).

Le rang huit sur la strate dense de rang trois se voit aussi directement.
Au voisinage de

\[
X_3=\begin{pmatrix}I_3&0\\0&0\end{pmatrix},
\]

écrivons une perturbation sous la forme

\[
\begin{pmatrix}I_3+A&b\\c^{\mathsf T}&d\end{pmatrix}.
\]

La formule de Schur donne

\[
\det
\begin{pmatrix}I_3+A&b\\c^{\mathsf T}&d\end{pmatrix}
=
\det(I_3+A)
\bigl(d-c^{\mathsf T}(I_3+A)^{-1}b\bigr).
\]

Sa partie quadratique est

\[
d\,\operatorname{tr}(A)-c^{\mathsf T}b.
\]

Le premier terme fournit un plan hyperbolique de rang deux et les trois
paires \((b_i,c_i)\) fournissent six directions supplémentaires. Le rang
hessien vaut donc huit. Les strates de rang inférieur sont dans la clôture de
la strate de rang trois, et le rang d'une matrice ne peut augmenter dans une
limite. Ainsi,

\[
\operatorname{rang}H_{\det_4}(X)\le8
\qquad\text{pour tout }X\text{ tel que }\det_4(X)=0.
\]

Tous les mineurs \(9\times9\) du Hessien s'annulent donc sur l'hypersurface
\(\det_4=0\). Cette hypersurface est irréductible : elle est la clôture de
l'orbite irréductible de la strate de rang trois. Par conséquent, chacun de
ces mineurs est divisible par \(\det_4\), soit

\[
\Theta_9(\det_4)=0
\]

et

\[
\operatorname{rang}\mathcal A_9(\det_4)=N.
\]

## 4. Côté permanent paddé : témoin entier de rang neuf

Prenons

\[
X_*=\begin{pmatrix}
-2&-1&-1\\
-1& 1& 1\\
-1& 1& 1
\end{pmatrix}.
\]

Un calcul direct donne

\[
\operatorname{per}_3(X_*)=0.
\]

En revanche,

\[
\det\bigl(H_{\operatorname{per}_3}(X_*)\bigr)=-128.
\]

Le Hessien de \(F=z\operatorname{per}_3\), restreint aux neuf variables de
la matrice, est

\[
H_F^{(x,x)}(z,X)=z\,H_{\operatorname{per}_3}(X).
\]

Au point \((z,X)=(1,X_*)\), on a donc

\[
F(1,X_*)=0
\]

mais le mineur principal \(9\times9\) dans les variables de matrice vaut

\[
-128\ne0.
\]

Cette coordonnée de \(\Phi_9(F)\) ne peut pas être divisible par \(F\), car
un multiple de \(F\) s'annulerait en tout point de \(F=0\). Ainsi,

\[
\Theta_9(F)\ne0
\]

et

\[
\operatorname{rang}\mathcal A_9(F)=N+1.
\]

## 5. Le rang inversé

On obtient finalement

\[
\boxed{
\operatorname{rang}\mathcal A_9(z\operatorname{per}_3)
=N+1
>
N
=
\operatorname{rang}\mathcal A_9(\det_4).
}
\]

C'est exactement l'orientation qui manquait aux rangs globaux des premiers
flattenings : le permanent paddé possède ici le rang strictement supérieur.

Puisque la condition \(\operatorname{rang}\mathcal A_9\le N\) est fermée et
\(GL_{16}\)-invariante, elle contient la clôture de l'orbite du déterminant,
mais pas \(z\operatorname{per}_3\). D'où

\[
\boxed{
[z\operatorname{per}_3]
\notin
\overline{GL_{16}\cdot[\det_4]}.
}
\]

## 6. Ce que cela change dans le programme

Le point décisif est que les premiers calculs comparaient la **quantité** de
mineurs et de relations. Le déterminant gagnait presque toujours parce qu'il
utilise seize directions actives contre dix pour le permanent paddé.

La nouvelle observable compare autre chose : les mineurs hessiens
s'annulent-ils **intrinsèquement sur l'hypersurface définie par le polynôme** ?
Le quotient par \((f)\) retire l'avantage artificiel provenant du nombre de
variables et révèle la géométrie tangentielle du lieu zéro.

La suite naturelle n'est donc pas de multiplier aveuglément les flattenings
bruts. Elle consiste à étudier, pour plusieurs \(r\), les classes

\[
[\Phi_r(f)]\in A_r\otimes(S/(f))_{r(d-2)}
\]

et leurs résolutions équivariantes. Pour le cas pilote, le premier indice qui
force la différence est \(r=9\), parce que le rang hessien maximal du
\(\det_4\) sur son hypersurface vaut huit.

## 7. Reproduction

Exécuter depuis la racine du paquet :

```bash
python scripts/verify_rank_reversal.py
python verify_package.py
```

Le premier script reconstruit exactement :

- le témoin entier \(X_*\) ;
- la valeur \(\operatorname{per}_3(X_*)=0\) ;
- le Hessien \(9\times9\) et son déterminant \(-128\) ;
- les rangs hessiens exacts \(0,0,4,8,16\) sur les cinq strates canoniques de
  \(\det_4\) ;
- le certificat du renversement \(N+1>N\).

Toute l'arithmétique est effectuée sur \(\mathbf Z\) ou \(\mathbf Q\), sans
appel à un oracle numérique.
