# Portée exacte des affirmations

## Démontré dans ce paquet

1. Le rang du Hessien de `det_4` est au plus `8` en tout point de
   l'hypersurface `det_4=0`.
2. Tous les mineurs `9x9` de ce Hessien sont divisibles par `det_4`.
3. Pour le point entier fourni, `per_3=0` mais le déterminant du Hessien de
   `per_3` vaut `-128`.
4. Le covariant `Phi_9(z*per_3)` n'est donc pas divisible par
   `z*per_3`.
5. La condition de divisibilité est une condition fermée et
   `GL_16`-invariante, exprimable comme un rang de matrice augmentée.
6. Par conséquent,
   `[z*per_3]` n'appartient pas à la clôture projective de l'orbite
   `GL_16*[det_4]`.

## Non revendiqué

- Aucune séparation asymptotique entre les familles permanent et déterminant.
- Aucune conséquence `VP != VNP`.
- Aucune revendication de nouveauté bibliographique.
- Aucun renversement dans les flattenings binaires déjà testés de `Phi_3`.

Le résultat est une obstruction exacte pour le premier cas paddé
`det_4` contre `z*per_3`.
