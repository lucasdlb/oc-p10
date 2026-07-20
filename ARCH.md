# Architecture BrainScanAI

## Etat Actuel Du Repo

Le projet est un socle R&D Python pour evaluer une approche semi-supervisee de detection de tumeurs cerebrales sur images IRM.

Elements deja presents :

- `PROJECT.md` : cadrage metier, objectifs, contraintes et livrables attendus.
- `README.md` : present mais encore vide.
- `pyproject.toml` : configuration projet Python 3.12 avec outils de qualite.
- `uv.lock` : verrouillage des dependances via `uv`.
- `.python-version` : version Python fixee a `3.12`.
- `.pre-commit-config.yaml` : hooks de qualite.
- `mri_dataset_brain_cancer_oc/` : dataset brut fourni.

Outils de qualite deja configures :

- `ruff` pour lint et format.
- `pytest` et `pytest-cov` pour les tests.
- `ty` pour le type checking.
- `pre-commit` pour automatiser les controles.

Le repo ne contient pas encore de code applicatif, de pipelines, de tests ou de configuration runtime.

## Objectif Architectural

L'objectif est de garder un code R&D proche production-ready :

- modulaire par brique technique ;
- type checkable ;
- configure par fichiers `.yaml` ou `.toml` ;
- valide par `pydantic` ;
- reproductible ;
- testable ;
- comprehensible pour une soutenance et extensible vers un usage plus industriel.

Les notebooks peuvent servir a l'exploration ou la restitution, mais la logique principale doit rester dans `src/` et les pipelines executables dans `scripts/`.

## Structure Cible

```text
oc-p10/
+-- configs/
|   +-- dataset.yaml
|   +-- features.yaml
|   +-- clustering.yaml
|   +-- supervised.yaml
|   +-- semisupervised.yaml
+-- scripts/
|   +-- explore_data.py
|   +-- extract_features.py
|   +-- run_clustering.py
|   +-- train_supervised.py
|   +-- train_semisupervised.py
|   +-- evaluate.py
+-- src/
|   +-- brainscanai/
|       +-- config/
|       |   +-- loader.py
|       |   +-- schemas.py
|       +-- domain/
|       |   +-- entities.py
|       |   +-- protocols.py
|       |   +-- types.py
|       +-- utils/
|       |   +-- paths.py
|       +-- data/
|       |   +-- catalog.py
|       |   +-- validation.py
|       |   +-- splitting.py
|       +-- features/
|       |   +-- extractors.py
|       |   +-- preprocessing.py
|       |   +-- storage.py
|       +-- clustering/
|       |   +-- reducers.py
|       |   +-- clusterers.py
|       |   +-- weak_labeling.py
|       |   +-- metrics.py
|       +-- models/
|       |   +-- classifiers.py
|       |   +-- training.py
|       |   +-- evaluation.py
|       +-- reporting/
|           +-- plots.py
|           +-- reports.py
+-- tests/
|   +-- unit/
|   +-- integration/
+-- data/
|   +-- interim/
|   +-- processed/
|   +-- reports/
+-- notebooks/
```

La structure creee dans le repo pose uniquement les dossiers de base. Les fichiers Python ci-dessus seront ajoutes progressivement quand chaque brique sera implementee.

## Responsabilites Des Dossiers

### `configs/`

Contient toute la configuration runtime.

Regle : aucun chemin, hyperparametre ou choix de modele important ne doit etre hardcode dans le code pipeline.

Formats acceptes :

- `.yaml` pour les configs lisibles et frequemment modifiees ;
- `.toml` si la configuration est plus stable ou fortement structuree.

Chaque config devra etre validee par un schema `pydantic` avant execution.

### `scripts/`

Contient les points d'entree executables des pipelines.

Les scripts doivent rester fins :

- parser les arguments ;
- charger la config ;
- resoudre les chemins ;
- appeler les modules de `src/brainscanai/` ;
- gerer logs et code de sortie.

Ils ne doivent pas contenir la logique metier principale.

Mode d'execution initial recommande :

```bash
uv run python scripts/explore_data.py --config configs/dataset.yaml
```

Des entrees CLI declarees dans `pyproject.toml` pourront etre ajoutees plus tard quand les scripts seront stabilises.

### `src/brainscanai/`

Contient le code applicatif reusable, teste et type.

Les modules doivent etre organises par responsabilite technique, pas par notebook.

### `src/brainscanai/domain/`

Contient les types metier et les contrats abstraits.

Les interfaces seront definies avec `typing.Protocol` pour garder les briques interchangeables :

- catalogues dataset ;
- validateurs d'images ;
- extracteurs de features ;
- stores d'embeddings ;
- reducteurs de dimension ;
- clusterers ;
- generateurs de labels faibles ;
- classifieurs ;
- evaluateurs.

### `src/brainscanai/config/`

Contient :

- les schemas `pydantic` ;
- le loader YAML/TOML ;
- la validation stricte des valeurs runtime.

### `src/brainscanai/utils/paths.py`

Contiendra la fonction singleton `find_root`.

Objectif : tous les chemins relatifs issus des configs doivent etre convertis en chemins absolus a partir de la racine du projet.

Comportement cible :

- detecter une seule fois la racine du repo ;
- memoriser le resultat ;
- permettre aux configs d'utiliser des chemins relatifs lisibles ;
- fournir une base stable quel que soit le repertoire depuis lequel un script est lance.

La racine pourra etre detectee via des marqueurs comme :

- `pyproject.toml` ;
- `.git/` ;
- `PROJECT.md`.

Cette fonction ne doit pas etre implementee tant que le squelette n'est pas valide.

### `data/`

Contient les artefacts generes localement.

Sous-dossiers prevus :

- `interim/` : metadonnees intermediaires, rapports de qualite image ;
- `processed/` : embeddings, splits, labels faibles ;
- `reports/` : metriques, figures, exports de synthese.

Les artefacts volumineux n'ont pas vocation a etre versionnes.

### `tests/`

Contient les tests unitaires et integration.

Priorites initiales :

- validation des schemas de config ;
- resolution des chemins ;
- construction du catalogue dataset ;
- invariants de split train/test ;
- calculs de metriques.

## Principes De Modularite

Chaque choix technique doit etre encapsule derriere un contrat stable.

Exemples :

- `ResNet50` et `DenseNet` doivent implementer le meme contrat d'extraction de features.
- `KMeans`, `DBSCAN` et `AgglomerativeClustering` doivent implementer le meme contrat de clustering.
- Une baseline supervisee et une approche semi-supervisee doivent produire des sorties evaluables de facon homogene.

Les pipelines dependent des contrats ou de services applicatifs, pas directement des details des librairies quand ce n'est pas necessaire.

## Typage

Tout nouveau code Python devra etre type.

Regles :

- pas de fonctions publiques sans annotations ;
- pas de structures de config non validees ;
- usage de `Protocol` pour les interfaces ;
- usage de types explicites pour labels, chemins, predictions et metriques ;
- controle par `ty check` via pre-commit.

## Configuration Runtime

Toute configuration d'execution doit venir de `configs/*.yaml` ou `configs/*.toml`.

Exemples de valeurs a configurer :

- chemins dataset ;
- chemins d'artefacts ;
- seed globale ;
- taille image ;
- batch size ;
- modele pre-entraine ;
- algorithme de clustering ;
- hyperparametres ;
- metriques attendues ;
- seuils de validation.

Chaque fichier de config devra etre charge puis valide par `pydantic` avant execution.

## Pipelines Prevues

### `scripts/explore_data.py`

Explore le dataset, verifie la structure, compte les images, detecte les anomalies et produit un catalogue d'images.

### `scripts/extract_features.py`

Charge le catalogue, applique le preprocessing et extrait les embeddings avec un modele pre-entraine.

### `scripts/run_clustering.py`

Charge les embeddings, reduit eventuellement la dimension, teste des algorithmes de clustering et produit des labels faibles.

### `scripts/train_supervised.py`

Entraine une baseline supervisee uniquement sur les donnees fortement labellisees disponibles pour l'entrainement.

### `scripts/train_semisupervised.py`

Entraine une approche semi-supervisee utilisant les labels faibles, tout en gardant l'evaluation finale sur labels experts separes.

### `scripts/evaluate.py`

Centralise les evaluations, comparaisons, metriques et exports de rapports.

## Contraintes Medicales Et Experimentales

Le projet reste une preuve de concept R&D.

Regles importantes :

- les donnees fortement labellisees et faiblement labellisees doivent rester distinguees ;
- le test set doit contenir uniquement des labels experts ;
- le test set ne doit jamais etre utilise pour entrainer, regler ou selectionner un modele ;
- le rappel sur la classe `cancer` doit etre surveille attentivement a cause du risque de faux negatifs ;
- les resultats ne doivent pas etre presentes comme une performance clinique validee.

## Commandes Qualite Cibles

Commandes a conserver comme references :

```bash
uv run ruff check .
uv run ruff format .
uv run ty check
uv run pytest
```

Ces commandes devront passer avant de considerer une brique comme terminee.

## Prochaines Etapes

1. Valider cette structure.
2. Completer `.gitignore` pour les artefacts locaux et dossiers IDE si necessaire.
3. Ajouter les dependances runtime minimales.
4. Creer les schemas `pydantic` initiaux.
5. Implementer `find_root` dans `src/brainscanai/utils/paths.py`.
6. Implementer le premier pipeline `scripts/explore_data.py`.
