# Reverse Hessian : fusion du noyau audité et de l’extension VP/VNP

Ce dépôt réunit les deux paquets en conservant une frontière nette entre preuve validée et recherche exploratoire.

- `core/` est le paquet de référence : théorème equal-size révisé après audit, preuves, trois moteurs de certification indépendants et protocole de reproductibilité.
- `extensions/vp_vnp/` contient l’étude du padding, la Hessienne transverse, les flattenings testés, les pistes de multiplicité et les échecs documentés.

En cas de divergence sur un résultat commun, **`core/` prévaut**. Les certificats de l’extension sont conservés parce qu’ils documentent des expériences supplémentaires, mais ils ne remplacent pas les certificats plus récents du noyau.

## Résultat principal conservé

Pour tout `n >= 3`, avec `D(f)=det Hess(f)` sur `M_n(C)`, le noyau établit l’incomparabilité des deux clôtures d’orbites hessiennes :

```text
D(det_n) n’appartient pas à closure(GL_{n^2} . D(per_n)),
D(per_n) n’appartient pas à closure(GL_{n^2} . D(det_n)).
```

## Limite essentielle

Le dépôt combiné ne démontre ni une obstruction pour le permanent paddé standard, ni une borne super-polynomiale de complexité déterminantale, ni `VP != VNP`. Le déterminant de la Hessienne ambiante complète s’annule dès que le polynôme paddé possède des variables ambiantes inutilisées.

## Vérification

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

./verify_all.sh       # rapide : tests, hashes internes et manifeste global
./rebuild_all.sh      # régénération des deux jeux de certificats
./verify_all_full.sh  # lent : ajoute les deux reconstructions isolées bit-à-bit
```

Consulter `MERGE_REPORT.md` pour les décisions de fusion et `CLAIMS.md` pour la hiérarchie des affirmations.
