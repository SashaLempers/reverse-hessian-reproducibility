
# Statut et limitations — v2.1

## Statut opérationnel

- profil `quick` : destiné à être exécuté sur chaque push et pull request ;
- profil `full` : régénérations fraîches et PDF déterministes ;
- profil `heavy` : dépend de moteurs externes, notamment Sage ;
- les moteurs absents restent `BLOCKED_NOT_EXECUTED`.

## Statut scientifique

Le registre actif contient 27 claims. Les étiquettes de preuve, de calcul, de nouveauté et de limitation sont conservées séparément. Les claims textuels nécessitent toujours une lecture experte indépendante.

## Limites principales

- aucune conséquence générale `VP != VNP` ;
- aucune borne super-polynomiale ;
- nouveauté de plusieurs propositions non auditée ;
- calculs compound, modulaires et jet-conormal limités aux familles décrites ;
- aucune formalisation dans un assistant de preuve ;
- profil heavy non assimilé au profil quick.

## Attestation du 19 juillet 2026

Le profil quick est attesté PASS. Une tentative full a dépassé 30 minutes pendant la reconstruction fraîche Reverse-Hessian; elle reste donc NON TERMINÉE et n’est pas présentée comme PASS.
