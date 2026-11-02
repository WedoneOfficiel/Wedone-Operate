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
- CI configurée pour exécuter ses contrôles sur `phoenix-rebuild`, sur Ubuntu, Windows et macOS.
- Prototype PySide6 + Qt Quick/QML ajouté : écran de premier démarrage, choix individuel/classe, entrée élève et entrée professeur distinctes.
- Choix du mode enregistré dans SQLite et conservé au redémarrage.
- Commande de smoke test QML ajoutée au pipeline CI (`python -m phoenix.main --smoke-test`).

## À vérifier avant de considérer cette étape comme terminée

- Résultat réel des tests sur macOS, Windows et Linux via GitHub Actions : le pipeline est configuré, mais son résultat n'a pas encore été confirmé ici.
- Vérification visuelle manuelle du prototype QML sur les trois systèmes.
- Tests de restauration en présence de fichiers WAL/SHM et de bases verrouillées.
- Gestion des migrations successives et récupération après interruption.
- Validation manuelle des sauvegardes produites et restaurées.

## Prochaine étape

Valider le prototype vertical QML sur les trois systèmes, puis l'empaqueter dans un build autonome. Une fois le socle validé, enrichir les écrans élève/professeur et le parcours de pratique avant de migrer l'interface complète.

## Règles de sécurité

- Aucun import automatique des anciens JSON.
- Aucun accès implicite au dossier courant ou à Téléchargements.
- Aucune suppression de l'ancien dossier de données.
- Aucun changement sur `main` et aucune publication sans validation explicite.
