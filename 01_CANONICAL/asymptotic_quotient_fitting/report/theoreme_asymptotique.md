# Théorème asymptotique du quotient-Fitting hessien

## 1. Cadre

On travaille sur \(\mathbf C\). Soient \(m\ge 3\) et \(n\ge m\). Dans
\(V_n=\mathbf C^{n^2}\), on considère

\[
F_{n,m}=\ell^{\,n-m}\operatorname{per}_m,
\]

avec les variables restantes inutilisées. Pour une forme non nulle
\(f\in S^nV_n^*\), posons

\[
r_n=2n+1,\qquad e_n=r_n(n-2),
\]

\[
A_{r_n}=\bigwedge^{r_n}V_n^*\otimes\bigwedge^{r_n}V_n^*,
\]

et notons \(C_{r_n}(\operatorname{Hess}f)\) le tenseur de tous les mineurs
\(r_n\times r_n\) du Hessien. Le covariant quotient-Fitting est

\[
\Theta_n(f)=
\big[C_{r_n}(\operatorname{Hess}f)\big]
\in
A_{r_n}\otimes
\left(S^{e_n}V_n^*/fS^{e_n-n}V_n^*\right).
\]

La condition \(\Theta_n(f)=0\) signifie exactement que chaque mineur
\(r_n\times r_n\) du Hessien est divisible par \(f\).

## 2. Théorème principal

**Théorème.** Pour tous \(m\ge3\) et \(n\ge m\) :

\[
\Theta_n(\det_n)=0,
\]

et

\[
\boxed{
\Theta_n(F_{n,m})\ne0
\quad\Longleftrightarrow\quad
2n<m^2.
}
\]

En particulier, si \(2n<m^2\), alors

\[
\boxed{
[F_{n,m}]
\notin
\overline{GL_{n^2}\cdot[\det_n]}.
}
\]

Par conséquent,

\[
\boxed{
\overline{dc}(\operatorname{per}_m)
\ge \left\lceil\frac{m^2}{2}\right\rceil.
}
\]

Cette borne asymptotique est connue : elle correspond à la borne quadratique
de complexité déterminantale bordée de Landsberg--Manivel--Ressayre, après la
borne non bordée de Mignon--Ressayre. Le présent paquet en donne une
reconstruction dans le langage précis du rang augmenté quotient-Fitting et
avec le témoin uniforme fourni par la formule de ligne du Hessien du permanent.
Aucune revendication de nouveauté bibliographique n'est faite.

## 3. Côté déterminant

Le groupe \(GL_n\times GL_n\) agit transitivement sur chaque strate de rang de
\(M_n\). Sur la strate dense de l'hypersurface \(\det_n=0\), on peut donc se
placer en

\[
X_{n-1}=\operatorname{diag}(I_{n-1},0).
\]

Écrivons une perturbation sous la forme

\[
\begin{pmatrix}
I_{n-1}+A & b\\
c^{\mathsf T} & d
\end{pmatrix}.
\]

La formule du complément de Schur montre que la partie quadratique du
déterminant en ce point est

\[
d\,\operatorname{tr}(A)-c^{\mathsf T}b.
\]

Le premier terme a rang hessien \(2\), et les \(n-1\) paires
\((b_i,c_i)\) apportent \(2(n-1)\) directions. Ainsi

\[
\operatorname{rang}\operatorname{Hess}(\det_n)(X_{n-1})=2n.
\]

Les strates de rang plus faible sont dans la clôture de cette strate, et le
rang matriciel ne peut augmenter dans une spécialisation. Donc

\[
\operatorname{rang}\operatorname{Hess}(\det_n)(X)\le2n
\qquad(\det_n(X)=0).
\]

Tous les mineurs d'ordre \(2n+1\) s'annulent sur l'hypersurface irréductible
\(\det_n=0\). Chacun est donc divisible par \(\det_n\), d'où
\(\Theta_n(\det_n)=0\).

Les contrôles finis reconstruisent même les rangs exacts sur toutes les strates :

\[
0\quad(s\le n-3),\qquad
4\quad(s=n-2),\qquad
2n\quad(s=n-1),\qquad
n^2\quad(s=n).
\]

## 4. Témoin permanent uniforme

Posons

\[
X_m(t)=J_m+(t-1)E_{11}.
\]

Un comptage direct donne

\[
\operatorname{per}_m(X_m(t))
=(m-1)!(t+m-1).
\]

Le témoin zéro est donc

\[
X_m^*=X_m(1-m)=J_m-mE_{11}.
\]

La formule uniforme de ligne est

\[
\det\operatorname{Hess}(\operatorname{per}_m)(X_m(t))
=K_m(t+m-3)^{(m-2)^2},
\]

avec

\[
K_m=
\frac{((m-2)!)^{m^2}(m-1)^{2m}}
{(m-2)^{(m-2)^2}}\ne0.
\]

Voici son argument, afin que la présente preuve soit autonome. Posons

\[
A=J_m-I_m,
\qquad
C=0\oplus(J_{m-1}-I_{m-1}).
\]

Une dérivée seconde mixte du permanent est nulle si les deux variables
partagent une ligne ou une colonne; sinon elle est le permanent du mineur
complémentaire de taille \(m-2\). Sur \(X_m(t)\), cela donne

\[
\operatorname{Hess}(\operatorname{per}_m)(X_m(t))
=(m-2)!A\otimes A+(t-1)(m-3)!C\otimes C.
\]

Pour \(B=A^{-1}C\), le spectre est formé de \(1\) avec multiplicité
\(m-2\) et de \(0\) avec multiplicité \(2\). Ainsi
\(B\otimes B\) possède la valeur propre \(1\) avec multiplicité
\((m-2)^2\), toutes les autres valeurs propres étant nulles. En factorisant
le premier terme de Kronecker, on obtient exactement la formule affichée.

Au point \(t=1-m\), le facteur variable vaut \(-2\). Ainsi

\[
\operatorname{per}_m(X_m^*)=0,
\qquad
\det\operatorname{Hess}(\operatorname{per}_m)(X_m^*)
\ne0.
\]

Le Hessien du permanent a donc rang plein \(m^2\) en un point de son lieu zéro.

Pour \(F_{n,m}=\ell^{n-m}\operatorname{per}_m\), évalué en
\((\ell,X)=(1,X_m^*)\), le bloc hessien porté par les \(m^2\) variables du
permanent est précisément
\(\operatorname{Hess}(\operatorname{per}_m)(X_m^*)\). Dès que

\[
2n+1\le m^2,
\]

un mineur d'ordre \(2n+1\) est non nul en ce point, tandis que
\(F_{n,m}=0\). Ce mineur ne peut donc pas être divisible par \(F_{n,m}\).
Comme les quantités sont entières,

\[
2n+1\le m^2
\quad\Longleftrightarrow\quad
2n<m^2.
\]

## 5. Fermeture et rang augmenté

La condition de divisibilité se représente dans des espaces fixes. Soit

\[
\mu_f:
A_{r_n}\otimes S^{e_n-n}V_n^*
\longrightarrow
A_{r_n}\otimes S^{e_n}V_n^*,
\qquad Q\longmapsto fQ.
\]

Comme l'anneau polynomial est intègre, \(\mu_f\) est injective pour
\(f\ne0\). On ajoute la colonne
\(C_{r_n}(\operatorname{Hess}f)\) et on obtient

\[
\mathcal A_n(f)
=
\big[\mu_f\mid C_{r_n}(\operatorname{Hess}f)\big].
\]

Si

\[
B_n=
\binom{n^2}{2n+1}^{\!2}
\binom{n^2+e_n-n-1}{e_n-n},
\]

alors

\[
\operatorname{rang}\mathcal A_n(f)=
\begin{cases}
B_n,&\Theta_n(f)=0,\\
B_n+1,&\Theta_n(f)\ne0.
\end{cases}
\]

Par conséquent, dans toute la plage \(2n<m^2\), on a le renversement uniforme

\[
\boxed{
\operatorname{rang}\mathcal A_n(F_{n,m})
=
\operatorname{rang}\mathcal A_n(\det_n)+1.
}
\]

La condition \(\operatorname{rang}\mathcal A_n(f)\le B_n\) est définie par
des mineurs homogènes et est \(GL(V_n)\)-invariante. Elle contient l'orbite du
déterminant, donc sa clôture, mais pas \(F_{n,m}\) lorsque \(2n<m^2\).

## 6. Frontière exacte de cette méthode

Le seuil \(2n<m^2\) est sharp pour ce covariant.

### Cas \(2n>m^2\)

L'ordre critique vérifie

\[
2n+1>m^2+1.
\]

Or le polynôme paddé dépend d'au plus \(m^2+1\) variables actives. Tous ses
mineurs hessiens critiques sont donc identiquement nuls, et
\(\Theta_n(F_{n,m})=0\).

### Cas \(2n=m^2\)

Ici l'ordre critique est exactement \(m^2+1\), la taille du Hessien actif.
Pour un polynôme homogène \(p\) de degré \(m\) en \(M=m^2\) variables et
\(k=n-m>0\), un calcul par complément de Schur et les identités d'Euler donne

\[
\det\operatorname{Hess}_{(x,\ell)}(\ell^kp)
=
-\frac{k(k+m-1)}{m-1}
\ell^{k(M+1)-2}
 p\,\det\operatorname{Hess}(p).
\]

Puisque \(F_{n,m}=\ell^kp\), le quotient contient le facteur

\[
\ell^{kM-2},
\]

qui a un exposant non négatif sur la frontière \(m^2=2n\) avec \(m\ge3\).
Le mineur actif maximal est donc divisible par \(F_{n,m}\), et les autres sont
nuls. Ainsi \(\Theta_n(F_{n,m})=0\).

On obtient donc une classification complète :

\[
\boxed{
\text{cette obstruction hessienne fonctionne exactement pour }n<m^2/2.
}
\]

Elle donne une borne quadratique, mais elle ne peut pas, sous cette forme,
produire une borne super-quadratique ni séparer \(VP\) et \(VNP\).

## 7. Statut bibliographique

- T. Mignon et N. Ressayre, *A quadratic bound for the determinant and
  permanent problem*, IMRN 2004 : borne \(dc(\operatorname{per}_m)\ge m^2/2\).
- J. M. Landsberg, L. Manivel et N. Ressayre, *Hypersurfaces with degenerate
  duals and the Geometric Complexity Theory Program*, Comment. Math. Helv. 88
  (2013) : équations de divisibilité hessienne et borne bordée
  \(\overline{dc}(\operatorname{per}_m)\ge m^2/2\).

Le résultat asymptotique n'est donc pas nouveau. La valeur du présent travail
est de montrer que le « rang inversé » découvert au cas \((4,3)\) se place
exactement dans cette théorie connue, de fournir un témoin uniforme très
simple issu de la formule de ligne du projet, et de certifier la frontière où
le mécanisme cesse nécessairement de fonctionner.
