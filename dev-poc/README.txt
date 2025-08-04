README.md : POC IA Local avec ECS

Bienvenue dans le sous-dossier dev-poc du Workspace VSCode, où tout prend vie ! Ce projet est une démonstration de pipeline IA local, orchestré via ECS (Entity Component System), avec Flecs pour la gestion des entités et Ollama pour les traitements IA.

🌐 Généralité ECS

L'Entity Component System (ECS) est une architecture logicielle qui permet de structurer des applications complexes en séparant les données (composants) et les comportements (systèmes).

Exemple TypeScript

class Entity {
  id: number;
  components: Map<string, any>;

  constructor(id: number) {
    this.id = id;
    this.components = new Map();
  }

  addComponent(name: string, data: any) {
    this.components.set(name, data);
  }

  getComponent(name: string) {
    return this.components.get(name);
  }
}

class System {
  update(entities: Entity[]) {
    entities.forEach(entity => {
      // Logique de mise à jour
    });
  }
}

const entity = new Entity(1);
entity.addComponent("position", { x: 0, y: 0 });
console.log(entity.getComponent("position"));

Cette approche favorise la modularité et la réutilisabilité, rendant les systèmes plus faciles à maintenir et à étendre.

🧱 Architecture du projet

🎯 Objectif

Mettre en place un pipeline de traitement modulaire basé sur ECS (Entity Component System), en exploitant Flecs pour la gestion des entités et Ollama pour les traitements IA locaux.

🛠️ Technologies clés

Flecs : framework ECS performant en C/C++

Ollama : interface locale pour modèles LLM (type LLaMA)

GitHub Actions : pour automatiser la CI/CD

VS Code + Docker : environnement de développement

🧩 Flecs : Structuration ECS

✅ Avancées

Dans le feu de l'action, Flecs a permis de structurer notre pipeline IA avec une précision chirurgicale :

Mise en place de World, Entity, Component & System

Définition de TagComponent pour les entités sans données

Système de mise à jour avec filtrage par composants

🧠 Points à creuser

Mais chaque bataille a ses défis :

Abstraction du système de dispatcher

Intégration temps réel : pub/sub, events ?

Modularisation des systèmes de traitement

🤖 Ollama : LLM local & intégration

✅ Ce qui fonctionne

Modèle LLaMA lancé localement via Ollama

Appels via API REST simples

Structure asynchrone prévue pour le traitement par lots

🔍 À améliorer

Gestion du contexte / mémoire conversationnelle

Benchmarking des performances sur ton laptop

Possibilité d'intégrer des hooks personnalisés (pré/post traitement)

🧪 Pipeline ECS : Orchestration

🔄 Architecture proposée

Chaque entité représente une "requête" IA

Les composants représentent :

le prompt

le modèle cible

les métadonnées

les résultats

Les systèmes orchestrent :

l’appel au modèle

le stockage des résultats

le logging & monitoring

📂 Structure du repo

Dans le feu de l'action, voici comment le projet est organisé :

src/ : Contient le code source principal

tests/ : Scripts de test pour valider les fonctionnalités

docs/ : Documentation et guides

scripts/ : Automatisation des tâches

🗓️ Prochaines étapes

[ ] Rédiger un schéma visuel du pipeline ECS

[ ] Tester la modularité avec plusieurs modèles dans Flecs

[ ] Ajouter logging/trace dans les systèmes Ollama

[ ] Script d’automatisation du setup (makefile ou bash)