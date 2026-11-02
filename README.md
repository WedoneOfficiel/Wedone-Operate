<div align="center">
  <img src="https://raw.githubusercontent.com/WedoneOfficiel/Wedone-Operate/phoenix-rebuild/icon.png" width="96" alt="Logo Wedone Operate"/>
  <h1>Wedone Operate — Projet Phoenix</h1>
  <p><em>Application de calcul mental — du CP au lycée</em></p>
  <p>
    <img src="https://img.shields.io/badge/canal-Beta%202026.11.02-DA8A16?style=flat-square" alt="Beta 2026.11.02"/>
    <img src="https://img.shields.io/badge/statut-en%20développement-orange?style=flat-square" alt="En développement"/>
    <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.11"/>
    <img src="https://img.shields.io/badge/PySide6%20%2B%20Qt%20Quick-QML-41CD52?style=flat-square" alt="PySide6 et Qt Quick"/>
    <img src="https://img.shields.io/badge/licence-Apache%202.0-lightgrey?style=flat-square" alt="Licence Apache 2.0"/>
  </p>
</div>

---

> **Projet Phoenix — canal bêta rouvert le 2 novembre 2026.**
> Cette version est une reconstruction majeure de Wedone Operate. Elle est destinée aux essais et aux retours : **elle n'est pas stable et ne doit pas être présentée comme une version de production**.

## Présentation

Wedone Operate est un logiciel de calcul mental conçu pour accompagner les élèves du CP au lycée. Le **Projet Phoenix** repart sur une nouvelle architecture et une nouvelle interface, sans supprimer ni réutiliser automatiquement les données de l'ancienne application.

La bêta actuelle pose les fondations du futur logiciel : entraînement individuel, premiers parcours de classe, moteur de calcul, suivi des séances et gestion locale des données. Toutes les compétences annoncées pour les niveaux scolaires ne sont pas encore disponibles : seules les compétences disposant d'un générateur implémenté sont activées.

## Télécharger et essayer la bêta

Les compilations de préversion sont publiées comme artefacts des workflows GitHub Actions de la branche `phoenix-rebuild` :

- [Phoenix packages — Windows x64, macOS Apple Silicon et Linux x64](https://github.com/WedoneOfficiel/Wedone-Operate/actions/workflows/build-phoenix.yml)
- [CI — tests automatisés](https://github.com/WedoneOfficiel/Wedone-Operate/actions/workflows/ci.yml)

Ouvrez une exécution terminée, puis récupérez l'artefact correspondant à votre système. Ces archives sont des compilations de test, pas des installateurs certifiés pour une diffusion stable.

### Précautions bêta

- Faites une copie de vos données importantes avant tout essai.
- Phoenix utilise son propre dossier de données : il ne remplace pas les données de l'ancienne version et ne les importe pas automatiquement.
- Les fonctionnalités, l'interface et le format de stockage peuvent encore évoluer.
- Sur macOS, la signature de préversion ne remplace pas une signature Developer ID et une notarisation Apple. Une distribution sans avertissement Gatekeeper nécessitera cette étape avant une publication publique.

## Nouveautés de la bêta Phoenix — 2 novembre 2026

### Nouvelle application et nouvelle interface

- Reconstruction dans un package applicatif `phoenix/`, séparé des anciens écrans.
- Nouvelle interface PySide6 et Qt Quick / QML.
- Écran de premier démarrage avec choix entre utilisation individuelle et utilisation en classe.
- Choix du mode mémorisé et modifiable ultérieurement sans effacer les données.
- En utilisation individuelle, accès direct à l'entraînement, sans compte ni faux profil.
- En utilisation classe, deux accès distincts : espace élève et espace professeur.
- Barre d'application et identité visuelle Phoenix ; réglages d'accessibilité persistants avec échelle de l'interface, contraste renforcé et réduction des animations.

### Calcul mental et séances

- Catalogue de compétences organisé par niveau, du CP à la Terminale.
- Premiers générateurs testables pour les additions, soustractions, multiplications, divisions exactes et calculs sur les nombres relatifs.
- Difficulté réglable sur cinq niveaux pour les générateurs compatibles.
- Prévention des doublons au sein d'une séance, y compris pour les opérations commutatives.
- Enregistrement des séances, des réponses, des corrections et du temps de réponse.
- Possibilité de terminer ou d'abandonner une séance en conservant les réponses déjà enregistrées.

### Premiers outils pour les classes

- Création de profils professeurs avec vérification des mots de passe par PBKDF2.
- Authentification dans l'espace professeur.
- Création de classes, de groupes et de profils élèves.
- Sélection d'une classe, d'un groupe et d'un élève dans le parcours élève.
- Entraînement rapide sans profil.
- Archivage des classes, groupes et élèves avec conservation de l'historique.
- Première fonction de modification du profil professeur.

### Progression et données

- Tableau de bord individuel initial : séances, réponses et taux de réussite.
- Progression calculée à partir des réponses réellement traitées, avec ventilation par compétence.
- Première vue de progression par élève.
- Nouvelle base SQLite transactionnelle, avec version de schéma.
- Dossier de données Phoenix séparé de celui de l'ancienne application.
- Sauvegarde SQLite cohérente et restauration après vérification de l'intégrité, avec copie de sécurité.
- Export et import JSON versionnés.
- Réinitialisation des données avec sauvegarde préalable et confirmation.
- Aucun import automatique des anciens fichiers JSON et aucune suppression des anciennes données.

### Qualité et distribution

- Tests automatisés du moteur de questions, des séances, de la progression, de la classe, de la sécurité et du stockage.
- Smoke test de l'interface QML dans la CI.
- Vérifications CI sur Windows, macOS et Linux.
- Workflow de compilation distinct pour Windows x64, macOS Apple Silicon et Linux x64.
- Intégration de l'icône de l'application dans les paquets et dans l'interface.

## Ce qui reste en développement

Cette bêta ne représente pas encore le périmètre final du logiciel. Les principaux chantiers restants sont :

- Compléter l'édition, la restauration et la gestion détaillée des classes, groupes, élèves et profils.
- Enrichir les tableaux de bord professeurs, les statistiques temporelles et les exports de rapports.
- Étendre le catalogue d'exercices et valider les compétences contre les programmes officiels, notamment au collège et au lycée.
- Compléter les tests de migration, de restauration en présence de fichiers SQLite auxiliaires, de corruption et d'interruption.
- Vérifier visuellement et fonctionnellement l'interface sur les trois systèmes, y compris clavier, redimensionnement et petites fenêtres.
- Finaliser la signature et la notarisation macOS avant une distribution publique sans avertissement de sécurité.
- Améliorer la documentation et les parcours de prise en main.

Une fonctionnalité mentionnée dans la feuille de route n'est pas nécessairement déjà disponible dans cette bêta.

## Données et confidentialité

Phoenix fonctionne localement. Les données de l'application sont stockées dans le dossier de données standard de l'utilisateur, sous le répertoire **Wedone Operate Phoenix** :

- **macOS** : `~/Library/Application Support/Wedone Operate Phoenix/`
- **Windows** : `%LOCALAPPDATA%/Wedone Operate Phoenix/`
- **Linux** : `$XDG_DATA_HOME/Wedone Operate Phoenix/` ou `~/.local/share/Wedone Operate Phoenix/`

Les anciennes données ne sont ni déplacées ni supprimées. L'import depuis l'ancien logiciel devra être une action volontaire et explicite.

## Blog

### Réouverture du canal bêta : bienvenue dans le Projet Phoenix — 02/11/2026

Après une période sans canal bêta, celui-ci rouvre avec le **Projet Phoenix**, une reconstruction majeure de Wedone Operate. L'objectif n'est pas de publier une simple mise à jour de l'ancienne application : Phoenix repart sur une base technique neuve, une interface entièrement repensée et une gestion des données plus sûre.

Cette première bêta apporte le choix entre usage individuel et usage en classe, un nouveau moteur de calcul mental, l'enregistrement des séances et des réponses, les premiers outils de gestion des classes et des élèves, des statistiques initiales, ainsi qu'un centre de sauvegarde, de restauration et d'export des données. Elle inaugure également une nouvelle chaîne de compilation pour Windows, macOS Apple Silicon et Linux.

Le canal est rouvert pour tester ces fondations, recueillir les retours et corriger les problèmes avant d'élargir les fonctionnalités. **Phoenix Beta 2026.11.02 n'est pas une version stable** : certaines fonctions sont encore partielles et les programmes de calcul seront enrichis progressivement.

Merci à toutes les personnes qui prendront le temps d'essayer cette préversion et de signaler les problèmes rencontrés.

*WedoneOfficiel — 02/11/2026*

## Historique des versions

### Projet Phoenix — Beta 2026.11.02 — 02/11/2026

- Réouverture du canal bêta.
- Première préversion de la reconstruction Phoenix.
- Nouvelle interface PySide6 / Qt Quick, nouveaux parcours individuels et classe.
- Moteur de calcul mental, premières statistiques et stockage SQLite.
- Sauvegarde, restauration, import/export et réinitialisation sécurisée.
- Premiers outils professeur / élève et compilations multiplateformes.

### Anciennes versions stables — génération historique

Les versions Stable 2026.03.17 et antérieures correspondent à l'ancienne génération de Wedone Operate. Elles ne décrivent pas l'architecture ni les fonctionnalités de Phoenix. La bêta Phoenix est développée séparément sur la branche `phoenix-rebuild`.

## Contact

- **Mastodon** : [@wedoneofficiel@mastodon.social](https://mastodon.social/@wedoneofficiel)
- **E-mail** : wedoneofficiel@outlook.fr

---

**Branche de développement :** [`phoenix-rebuild`](https://github.com/WedoneOfficiel/Wedone-Operate/tree/phoenix-rebuild) · **Branche stable historique :** `main` (non modifiée par le Projet Phoenix).
