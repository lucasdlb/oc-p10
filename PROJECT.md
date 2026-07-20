# Projet BrainScanAI - Detection semi-supervisee de tumeurs cerebrales

## 1. Contexte

CurelyticsIA est une startup specialisee dans la e-sante. Elle developpe des solutions d'intelligence artificielle destinees a assister les professionnels de sante dans l'analyse d'images medicales, notamment les IRM cerebrales.

Dans le cadre d'un projet R&D, l'entreprise souhaite evaluer la faisabilite d'une solution capable d'automatiser une partie de la detection de tumeurs cerebrales a partir d'images medicales.

Le projet s'inscrit dans une premiere phase exploratoire : il ne s'agit pas de livrer un dispositif medical final, mais de construire une preuve de concept robuste, documentee et techniquement defendable.

## 2. Objectifs

L'objectif principal est de concevoir une approche de labellisation et de classification semi-supervisee a partir d'un jeu de donnees partiellement annote.

Les objectifs operationnels sont les suivants :

- Explorer le jeu de donnees et verifier la qualite des images.
- Extraire des caracteristiques visuelles a l'aide d'un modele pre-entraine.
- Identifier des structures naturelles dans les donnees avec des methodes de clustering.
- Produire une labellisation faible pour les images non etiquetees.
- Entrainer et evaluer une approche semi-supervisee.
- Comparer l'approche semi-supervisee avec une approche supervisee classique.
- Formuler des recommandations techniques pour un passage a l'echelle.

## 3. Donnees Disponibles

Le jeu de donnees contient 1 500 images cerebrales au format JPEG, toutes redimensionnees en 512 x 512 pixels.

Repartition connue :

| Type de donnees | Volume | Description |
| --- | ---: | --- |
| Images non etiquetees | 1 400 | Images sans label disponible |
| Images etiquetees | 100 | Images annotees par des experts |

Les images etiquetees sont reparties en deux classes :

- `normal` : cerveau sans signe apparent de tumeur.
- `cancer` : cerveau presentant des signes de tumeur.

Structure actuelle du dataset :

```text
mri_dataset_brain_cancer_oc/
├── avec_labels/
│   ├── normal/
│   └── cancer/
└── sans_label/
```

## 4. Contraintes Et Hypotheses

Contraintes imposees :

- Travailler en Python.
- Tester plusieurs algorithmes.
- Utiliser des metriques pertinentes selon le risque principal.
- Definir clairement ce qui constitue un objectif atteint.
- Produire une synthese exploitable en soutenance.
- Evaluer la faisabilite d'un passage a l'echelle pour 4 millions d'images avec un budget de 5 000 euros.

Hypotheses de travail :

- Les images fournies sont deja anonymisees.
- Les labels experts disponibles sont consideres comme les references les plus fiables.
- Les donnees fortement labellisees et faiblement labellisees doivent rester separees pendant les evaluations.
- Les resultats obtenus sur 1 500 images ne suffisent pas a conclure a une performance clinique.

## 5. Strategie De Travail

L'enonce mentionne des notebooks comme livrables. Ils peuvent etre utiles pour l'exploration, la visualisation et la restitution pedagogique, mais le projet sera organise de maniere plus professionnelle autour de code Python reproductible.

Approche retenue :

- Utiliser des scripts et modules Python pour le pipeline principal.
- Utiliser eventuellement des notebooks pour l'analyse exploratoire et la presentation des resultats.
- Sauvegarder les sorties intermediaires importantes : metadonnees, embeddings, predictions, metriques.
- Documenter les choix techniques et les limites des resultats.

## 6. Approche Technique

### 6.1 Exploration Des Donnees

Objectifs :

- Charger le dataset.
- Verifier la structure des dossiers.
- Controler le nombre d'images par classe.
- Inspecter les dimensions, formats, canaux couleur et eventuelles anomalies.
- Afficher un echantillon representatif d'images.

Resultats attendus :

- Vue d'ensemble du dataset.
- Observations sur la qualite des donnees.
- Identification des risques potentiels : doublons, images corrompues, desequilibre, artefacts visuels.

Outils pressentis :

- `Pillow`
- `NumPy`
- `pandas`
- `matplotlib`
- `seaborn`

### 6.2 Preprocessing Et Extraction De Features

Objectifs :

- Preparer les images pour un modele pre-entraine.
- Appliquer un redimensionnement et une normalisation adaptes au modele choisi.
- Extraire des embeddings visuels a partir d'un CNN pre-entraine.
- Sauvegarder les embeddings dans un format exploitable.

Modeles candidats :

- `ResNet`
- `DenseNet`
- `VGG`
- `MobileNet`
- Modele equivalent disponible via `torchvision` ou `transformers`

Resultats attendus :

- Tableau de features indexe par image.
- Metadonnees associees : chemin, statut labelise ou non, label si disponible.
- Verification que les features sont exploitables pour le clustering et la classification.

### 6.3 Analyse Non Supervisee

Objectifs :

- Standardiser les features.
- Reduire la dimensionnalite pour analyse et visualisation.
- Tester plusieurs algorithmes de clustering.
- Comparer les clusters obtenus avec les labels experts disponibles.
- Produire une labellisation faible pour les images non etiquetees.

Methodes candidates :

- `PCA`
- `t-SNE`
- `UMAP` si pertinent
- `K-Means`
- `DBSCAN`
- `Agglomerative Clustering`

Metriques candidates :

- `ARI` : Adjusted Rand Index sur les donnees fortement labellisees.
- `NMI` : Normalized Mutual Information.
- Silhouette score pour evaluer la separation interne des clusters.

Point d'attention critique :

Les donnees fortement labellisees servent a evaluer la coherence du clustering. Elles ne doivent pas etre melangees sans controle avec les donnees faiblement labellisees lors de l'entrainement et de l'evaluation finale.

### 6.4 Apprentissage Semi-supervise

Objectifs :

- Construire un jeu faiblement labellise a partir du clustering.
- Entrainer un modele sur les labels faibles.
- Affiner ou comparer avec les labels experts disponibles.
- Comparer une approche supervisee classique et une approche semi-supervisee.

Comparaisons attendues :

| Strategie | Donnees d'entrainement | Objectif |
| --- | --- | --- |
| Supervisee | Donnees fortement labellisees uniquement | Baseline fiable |
| Semi-supervisee | Labels faibles puis labels experts | Mesurer l'apport des donnees non etiquetees |

Regles d'evaluation :

- Le jeu de test doit contenir uniquement des donnees fortement labellisees.
- Le jeu de test ne doit jamais etre vu pendant l'entrainement.
- Le split train/test doit etre stratifie si possible.
- Les metriques doivent etre choisies en fonction du risque metier.

Metriques candidates :

- `Recall` sur la classe cancer si l'objectif prioritaire est de limiter les faux negatifs.
- `F1-score` pour equilibrer precision et rappel.
- `Precision` si l'objectif est de limiter les faux positifs.
- Matrice de confusion.
- Courbe ROC et AUC si les probabilites sont disponibles.

## 7. Livrables

Livrables techniques :

- Pipeline Python d'exploration des donnees.
- Pipeline d'extraction de features.
- Experiments de clustering.
- Experiments de classification supervisee et semi-supervisee.
- Fichiers de resultats : embeddings, predictions, metriques.

Livrables de restitution :

- Synthese des resultats.
- Visualisations des clusters et performances.
- Support de presentation.
- Recommandations pour le passage a l'echelle.
- Auto-evaluation completee a partir du PDF fourni.

Notebooks possibles, sans obligation d'y placer tout le code :

- Exploration et qualite des donnees.
- Visualisation des embeddings et clustering.
- Synthese des resultats semi-supervises.

## 8. Definition Of Done

Le projet sera considere comme termine lorsque les elements suivants seront disponibles :

- Le dataset est explore et documente.
- Les anomalies ou limites des donnees sont identifiees.
- Les images sont transformees avec un preprocessing justifie.
- Les embeddings sont generes et sauvegardes.
- Plusieurs methodes de clustering sont testees.
- Les clusters sont evalues avec des metriques pertinentes.
- Une strategie de labellisation faible est proposee.
- Une baseline supervisee est entrainee et evaluee.
- Une approche semi-supervisee est entrainee et evaluee.
- Les resultats sont compares de maniere claire.
- Les recommandations de passage a l'echelle sont formulees.
- Les limites techniques, metiers et medicales sont explicitees.
- Les criteres du document d'auto-evaluation sont verifies.

## 9. Plan De Realisation

### Etape 1 - Importer Et Explorer Les Donnees

Actions :

- Lire la structure du dataset.
- Compter les images par dossier et par classe.
- Verifier les formats, dimensions et canaux couleur.
- Afficher des exemples d'images.
- Documenter les premieres observations.

Sortie attendue :

- Rapport court d'exploration.
- Tableau de metadonnees images.

### Etape 2 - Pretraiter Et Extraire Les Features

Actions :

- Choisir un modele pre-entraine.
- Appliquer les transformations attendues par ce modele.
- Extraire les embeddings.
- Sauvegarder les features.

Sortie attendue :

- Fichier de features exploitable par `scikit-learn` ou PyTorch.

### Etape 3 - Realiser L'Analyse Non Supervisee

Actions :

- Standardiser les embeddings.
- Reduire la dimensionnalite.
- Tester plusieurs methodes de clustering.
- Evaluer les clusters sur les donnees fortement labellisees.
- Produire une labellisation faible pour les donnees sans label.

Sortie attendue :

- Visualisations 2D.
- Scores de clustering.
- Fichier de labels faibles.

### Etape 4 - Entrainer Et Evaluer Les Modeles

Actions :

- Construire une baseline supervisee.
- Construire une approche semi-supervisee.
- Comparer les performances.
- Analyser les erreurs.

Sortie attendue :

- Tableau comparatif des metriques.
- Matrices de confusion.
- Commentaires sur les erreurs et limites.

### Etape 5 - Synthese Et Recommandations

Actions :

- Rediger la synthese technique.
- Preparer les recommandations de passage a l'echelle.
- Evaluer la faisabilite du budget de 5 000 euros pour 4 millions d'images.
- Completer la grille d'auto-evaluation.

Sortie attendue :

- Support de presentation.
- Recommandations techniques et metier.

## 10. Recommandations Pour Le Passage A L'Echelle

Le passage de 1 500 images a 4 millions d'images change fortement les contraintes techniques et budgetaires.

Points a evaluer :

- Cout de stockage des images et embeddings.
- Temps d'inference du modele d'extraction de features.
- Besoin GPU ou CPU selon le volume.
- Cout de labellisation humaine pour constituer un jeu de validation fiable.
- Strategie active learning pour prioriser les images les plus utiles a annoter.
- Controle qualite medical avant toute exploitation sensible.

Le budget de 5 000 euros parait limite pour une labellisation humaine exhaustive de 4 millions d'images. Une approche realiste serait de combiner :

- Extraction automatique de features.
- Clustering a grande echelle.
- Labellisation humaine ciblee sur un echantillon strategique.
- Active learning.
- Evaluation stricte sur un jeu expert independant.

## 11. Criteres D'Auto-evaluation

Les criteres issus du PDF d'auto-evaluation seront utilises comme checklist de fin de projet.

Preparation et transformation des donnees :

- Nettoyage des donnees.
- Traitement des valeurs aberrantes et images problematiques.
- Reduction des biais potentiels.
- Code commente et lisible.
- Transformations adaptees au modele.
- Normalisation ou standardisation si necessaire.
- Verification de l'exploitabilite des embeddings.

Identification du modele adapte :

- Test de plusieurs methodes de clustering.
- Justification de l'approche semi-supervisee.
- Utilisation de metriques pertinentes.
- Ajustement des hyperparametres.
- Recommandations pour le deploiement a grande echelle.
- Coherence entre resultats techniques et recommandations metier.

## 12. Risques Et Points D'Attention

- Volume tres limite de donnees fortement labellisees.
- Risque de surapprentissage sur les 100 images annotees.
- Labels faibles potentiellement bruites.
- Difference entre performance experimentale et performance clinique.
- Necessite de separer strictement entrainement, validation et test.
- Necessite de rester prudent dans les conclusions medicales.

## 13. Message Initial De Cadrage

Le projet provient d'une demande de Clara Martin, Responsable Data Science chez CurelyticsIA.

Synthese de la demande :

- Explorer un dataset d'images cerebrales partiellement annote.
- Extraire des features avec un modele pre-entraine.
- Realiser un clustering exploratoire.
- Utiliser les labels partiels pour mettre en place une approche semi-supervisee.
- Produire une synthese et des recommandations techniques.
- Evaluer la faisabilite d'un passage a l'echelle avec un budget contraint.
