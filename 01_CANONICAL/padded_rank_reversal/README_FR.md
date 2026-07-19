# Reverse Hessian — certificat de rang inversé

Ce paquet contient un certificat autonome pour le cas

\[
\det_4\quad\text{contre}\quad z\operatorname{per}_3
\in\operatorname{Sym}^4(\mathbf C^{16})^*.
\]

Le rang inversé se trouve dans le neuvième idéal de Fitting du Hessien,
considéré modulo le polynôme lui-même :

\[
\operatorname{rang}\mathcal A_9(z\operatorname{per}_3)
=
\operatorname{rang}\mathcal A_9(\det_4)+1.
\]

Il en résulte

\[
[z\operatorname{per}_3]\notin
\overline{GL_{16}\cdot[\det_4]}.
\]

Le témoin entier est

\[
X_*=\begin{pmatrix}
-2&-1&-1\\
-1&1&1\\
-1&1&1
\end{pmatrix},
\]

avec

\[
\operatorname{per}_3(X_*)=0,
\qquad
\det H_{\operatorname{per}_3}(X_*)=-128.
\]

## Vérification

```bash
python scripts/verify_rank_reversal.py
python verify_package.py
```

Le rapport complet se trouve dans `report/rapport_preuve.md`.
