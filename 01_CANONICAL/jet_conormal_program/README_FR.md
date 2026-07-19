# Reverse Hessian — programme jet–conormal

Ce paquet introduit et teste une extension au-delà du Hessien classique.

Contenu :

- preuve du fait que les jets bruts du déterminant saturent dès l'ordre 3 sur
  la strate lisse de rang `n-1`;
- rangs exacts des jets mixtes pour `det4` et `ell*per3`;
- calcul exact des premières syzygies jacobiennes linéaires;
- sonde modulaire des premiers brins de l'idéal du graphe de Gauss;
- définition d'une tour conormale jet–syzygétique résolue par blocs de Schur.

Reproduction principale :

```bash
python scripts/mixed_jet_probe.py --out certificates/mixed_jet_exact.json
python scripts/jacobian_linear_syzygies.py --out certificates/jacobian_linear_syzygies_exact.json
python verify_package.py
```

La sonde conormale complète est plus coûteuse :

```bash
python scripts/conormal_graph_probe.py --out certificates/conormal_graph_modular.json
```
