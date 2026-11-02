# Phoenix — état de construction

Dernière mise à jour : 2 novembre 2026

## Réalisé

- Création d'un package applicatif `phoenix/`, indépendant des écrans historiques.
- Nouveau répertoire de données dédié : `Wedone Operate Phoenix`, séparé des données de l'application historique.
- Première version du schéma SQLite, versionnée via `PRAGMA user_version`.
- Tables initiales pour les préférences, enseignants, classes, groupes, élèves, plans d'exercices, sessions et réponses.
- Transactions explicites et contraintes de clés étrangères.
- Sauvegarde cohérente avec l'API SQLite Backup.
- Restauration après validation de l'intégrité, avec création préalable d'une sauvegarde de sécurité.
- Premiers tests automatisés pour le schéma, le choix du mode, les transactions et les sauvegardes.
- CI configurée pour exécuter ses contrôles sur `phoenix-rebuild`.

## À vérifier avant de considérer cette étape comme terminée

- Résultat réel des tests sur macOS, Windows et Linux via GitHub Actions.
- Tests de restauration en présence de fichiers WAL/SHM et de bases verrouillées.
- Gestion des migrations successives et récupération après interruption.
- Validation manuelle des sauvegardes produites et restaurées.

## Prochaine étape

Construire un prototype vertical minimal avec PySide6 + Qt Quick/QML : démarrage, choix « Utilisation individuelle » / « Utilisation en classe », persistance du choix dans SQLite, puis navigation vers deux espaces distincts. Le prototype sera évalué et empaqueté avant toute migration de l'interface complète.

## Règles de sécurité

- Aucun import automatique des anciens JSON.
- Aucun accès implicite au dossier courant ou à Téléchargements.
- Aucune suppression de l'ancien dossier de données.
- Aucun changement sur `main` et aucune publication sans validation explicite.
