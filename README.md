# 🧠 NFL Data Pipeline

Ce dépôt regroupe les différentes phases de développement du pipeline de traitement de données NFL, avec export vers LibreOffice en format CSV.

## 📁 Sous-projets

| Dossier      | Description                                      | Statut         |
|--------------|--------------------------------------------------|----------------|
| `dev-poc/`   | Prototype initial de traitement synchrone        | ✅ Stable       |
| `dev-sync/`  | Pipeline optimisé pour extraction hebdomadaire   | 🚧 En cours     |
| `dev-async/` | (optionnel) Exploration d'une version asynchrone | 🧪 Expérimental |
| `dev-appli/` | (à venir) Interface utilisateur et intégration   | 🔜 À planifier  |

## 📦 Output

Le répertoire `dev-sync/` produit un fichier `nfl-data-weekly.csv`, destiné à être chargé dans une base LibreOffice.

- Format : délimité par virgules, encodage UTF-8
- Fréquence : 1 fois par semaine durant la saison NFL
- Chargement a posteriori possible si le script n'est pas prêt

## 🗓️ Calendrier NFL

La prochaine saison débute bientôt — le pipeline sera utilisé pour suivre les données hebdomadaires des matchs.

---

