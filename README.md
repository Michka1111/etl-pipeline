# ETL-pipeline

> Applied Research Project & Private Use  
> *An ETL job, IA assisted Data Gathering, ECS Oriented Design, CSV Output to load into a already set BI Star Schema implemented in a RDBMS — "un projet aux petits oignons".*

---

## 🌐 Description

Pipeline ECS de traitements de données ETL, de récolte de données assistée par IA, de Transformation Conçu selon le paradigme ECS, de production de sorties CSV pour chargement dans un schéma étoile BI pre-existant dans un RDBMS. Incluant : Ollama, Python, Pipeline orchestré avec le moteur ECS *Flecs*.  
Ce projet illustre l'application du paradigme ECS appliqué à un Workflow ETL — initialement inspiré par des cas d’usage sportifs (NFL), mais conçu pour être **générique et réutilisable**.

---

## 🧱 Architecture Technique

- **ETL personnalisé** : extraction / transformation depuis sources Web ou fichiers locaux, production de CSV  
- **ECS (Entity Component System)** : organisation des processus via *Flecs*  
- **Ollama + Python** : analyse de données par traitement IA  
- **VSCode workspace**, Git, GitHub.com  

---

## 🔁 Fonctionnalités prévues

- ✨ Conception selon le paradigme ECS  
- 🎯 Modèles IA via Ollama intégrés dans les **Système**s Flecs pour l'acquisition des données  
- 📊 Export intelligent CSV / LibreOffice Base pré-existant  
- 🧪 Mode synchrone pour PoC isolé (traitement "bloquant le flux)  
- 🧪 Mode asynchrone pour un Pipeline Flecs "vivant" et réel  
---

## 📁 Structure du dépôt

Ce dépôt regroupe différentes phases de développement de ETL-pipeline, PoC, Pipeline Synchrone, Pipeline Asynchrone, Application finale (si elle voit le jour), dans les dossiers de sous-projets connexes.

```plaintext
etl-pipeline/ 
├── bin-scripts/
├── dev-poc/
    └── README.md
├── web-docs/
└── README.md
```

### 📁 Sous-projets

Dans la racine du dépôt, un dossier "dev-*" par sous-projet de phase de développement.

| Dossier      | Description                                      | Statut |
|--------------|--------------------------------------------------|--------|
| `dev-poc/`   | Prototype initial de faisabilité                 | 🚧     |
| `dev-sync/`  | Pipeline optimisé pour extraction hebdomadaire   | 🧠     |
| `dev-async/` | (optionnel) Exploration d'une version asynchrone | 🧠     |
| `dev-appli/` | Interface utilisateur et intégration             | 🧠     |

| Légende          |
|------------------|
| ✅ Stable       |
| 🚧 En cours     |
| 🧪 Expérimental |
| 🔜 À planifier  |
| 🧠 En réflexion |

### 📦 Output

Le sous-projet `dev-sync/` produit un fichier `nfl-data-weekly.csv`, destiné à être chargé dans une base LibreOffice.

- Format : délimité par virgules, encodage UTF-8
- Fréquence : 1 fois par semaine durant la saison NFL
- Chargement a posteriori si le script n'est pas prêt ^^

### 🗓️ Calendrier NFL

La prochaine saison débute bientôt — le pipeline sera utilisé pour suivre les données hebdomadaires des matchs… s'il est prêt (la présaison commence bientôt).

## 🚀 Démarrage rapide

```bash
# Cloner le projet
# git clone https://github.com/Michka1111/etl-pipeline.git
# cd etl-pipeline

# (À venir) Exécuter le script de setup
# ./init-pipeline.bat

```

## 🤝 Contributions
Le projet est personnel à ce stade ; toute réflexion autour du paradigme ECS appliqué au domaine "pipelines ETL + IA" est la bienvenue !

## 📜 Licence

Usage privé et non commercial. À compléter avec une licence type MIT lorsque tu ouvres le projet.
---
