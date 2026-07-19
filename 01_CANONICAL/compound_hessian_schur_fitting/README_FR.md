# Extension Reverse Hessian — Hessien composé / Schur / Fitting

Cette archive met en œuvre le programme de calcul suivant sur le premier cas paddé non trivial choisi, avec tailles `M=4` et `m=3`,

\[
\det_4 \quad\text{contre}\quad z\operatorname{per}_3
\quad\text{dans}\quad \operatorname{Sym}^4(\mathbf C^{16})^* :
\]

- mineurs hessiens composés `Phi_r` ;
- catalecticants et flattenings de Young par composantes de Schur ;
- pièces graduées des idéaux engendrés par les mineurs du Hessien.

## Résultat principal

Le covariant composé ne s’annule pas sous le padding, mais **aucun test calculé ne sépare les clôtures dans la direction requise**. Pour `r=2`, les quatre flattenings de Young à deux cases autorisés par le module `S_(6,2)` ont été épuisés et donnent tous un rang strictement plus grand pour `det_4`. Les pièces de Fitting de degrés `4`, `5` et `6` vont dans la même direction.

Le rapport détaillé se trouve dans [`report/rapport_resultats.md`](report/rapport_resultats.md). Le résumé machine est [`certificates/summary.json`](certificates/summary.json). Une reconstruction fraîche de l’ensemble des rangs a passé le vérificateur ; son attestation est dans [`certificates/reproduction_attestation.json`](certificates/reproduction_attestation.json).

## Statut des nombres

- Catalecticants `r=2`, ordres `0..2` : rangs exacts sur `Q`.
- Pièces de Fitting `r=2`, degrés `4..6` : rangs exacts sur `Q`.
- Quatre flattenings de Young à deux cases : rangs exacts sur `Q` ; certains sont établis par saturation de la dimension source, le bloc `36/18` possède des certificats rationnels/représentationnels dédiés.
- Pièce génératrice `r=3` côté permanent : rang exact `849` sur `Q`.
- Pièce génératrice `r=3` côté déterminant : borne inférieure rigoureuse `6832` sur `Q`, obtenue modulo `1009`.

## Reproduction

Prérequis : Python 3.11+, SymPy 1.14+, `g++` avec OpenMP.

```bash
./reproduce_all.sh
```

Le script reconstruit les objets dans `reproduced/`, régénère les douze tenseurs polarisés et compare les rangs essentiels aux valeurs certifiées. Le contrôle léger du paquet courant s’exécute aussi directement :

```bash
python3 verify_package.py
```
