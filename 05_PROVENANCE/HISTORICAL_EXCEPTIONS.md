# Exceptions historiques explicites

Les snapshots et ZIP historiques ne sont jamais réécrits.

- les manifestes historiques incomplets restent des objets de provenance, pas des sceaux actifs ;
- les caches, logs non UTF-8, chemins absolus et artefacts LaTeX anciens restent dans la couche forensique ;
- `barrier_BC_patch` demeure supersédé/quarantined ;
- les archives n x n, VP/VNP, compound et combined clean sont des jalons historiques qui peuvent dupliquer le noyau canonique ;
- l’audit initial et les registres mixtes v2 ont été déplacés dans les assets de release ;
- le projet Prime est désormais autonome et son absence de deux sources TeX reste explicitement documentée dans son dépôt.
