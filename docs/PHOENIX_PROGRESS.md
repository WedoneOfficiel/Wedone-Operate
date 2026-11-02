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
- Tests automatisés pour le schéma, le choix du mode, les transactions et les sauvegardes.
- Catalogue de compétences structuré de CP à terminale, avec activation uniquement des compétences dont un générateur fiable existe.
- Générateurs déterministes pour additions, soustractions, multiplications, divisions exactes et premiers calculs sur les nombres relatifs.
- Détection des doublons dans une séance, y compris les opérations commutatives.
- Cycle de séance persisté : démarrage, réponses, validation, résultat final et abandon avec conservation des réponses déjà données.
- Parcours classe initial : création de profils professeurs protégés par mot de passe PBKDF2, création de classes et ajout d'élèves ; sélection de classe/groupe/élève côté élève ; entraînement rapide sans profil.
- Workflow de packaging PyInstaller séparé pour Windows, macOS et Linux.
- Premiers réglages d'accessibilité persistants : échelle globale de l'interface, contraste renforcé et réduction des animations.
- Centre de données dans les paramètres : sauvegarde SQLite, restauration avec copie de sécurité, export/import JSON versionné et réinitialisation confirmée avec sauvegarde préalable.
- CI configurée pour exécuter ses contrôles sur `phoenix-rebuild`, sur Ubuntu, Windows et macOS.
- Prototype PySide6 + Qt Quick/QML ajouté : écran de premier démarrage, choix individuel/classe, entrée élève et entrée professeur distinctes.
- Choix du mode enregistré dans SQLite et conservé au redémarrage.
- Commande de smoke test QML ajoutée au pipeline CI (`python -m phoenix.main --smoke-test`).

## À vérifier avant de considérer cette étape comme terminée

- Résultat réel des tests sur macOS, Windows et Linux via GitHub Actions : le pipeline est configuré, mais son résultat n'a pas encore été confirmé ici.
- Vérification visuelle manuelle du prototype QML sur les trois systèmes.
- Exécution confirmée des workflows CI et de packaging : les workflows sont configurés, mais aucun résultat d'exécution n'est encore disponible ici.
- Compléter l'édition/archivage des classes, groupes et élèves dans l'espace professeur, les écrans de progression et l'édition complète des profils.
- Vérifier les dialogues natifs de sélection de fichiers et la lisibilité du centre de données aux petites tailles de fenêtre.
- Enrichir progressivement les compétences collège/lycée après validation pédagogique et tests de correction.
- Tests de restauration en présence de fichiers WAL/SHM et de bases verrouillées.
- Gestion des migrations successives et récupération après interruption.
- Validation manuelle des sauvegardes produites et restaurées.

## Prochaine étape

Valider les workflows de compilation et de smoke test, puis corriger les éventuels problèmes Qt/QML. Ensuite, compléter la gestion des groupes, les profils, les statistiques et les réglages d'accessibilité avant de migrer les anciens écrans.

## Règles de sécurité

- Aucun import automatique des anciens JSON.
- Aucun accès implicite au dossier courant ou à Téléchargements.
- Aucune suppression de l'ancien dossier de données.
- Aucun changement sur `main` et aucune publication sans validation explicite.
