<div align="center">
  <img src="https://raw.githubusercontent.com/WedoneOfficiel/Wedone-Operate/main/icon.png" width="96"/>
  <h1>Wedone Operate</h1>
  <p><em>Logiciel de calcul mental pour l'école — du CP au Lycée</em></p>

  <p>
    <img src="https://img.shields.io/badge/version-Stable%202026.03.17-0672BC?style=flat-square" alt="version"/>
    <img src="https://img.shields.io/badge/python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="python"/>
    <img src="https://img.shields.io/badge/PyQt6-6.4%2B-41CD52?style=flat-square" alt="pyqt6"/>
    <img src="https://img.shields.io/badge/licence-Apache%202.0-lightgrey?style=flat-square" alt="licence"/>
    <img src="https://img.shields.io/badge/plateforme-Windows%20%7C%20Linux-informational?style=flat-square" alt="plateforme"/>
  </p>
</div>

---

## Présentation

Wedone Operate est un logiciel de calcul mental destiné aux élèves du **CP au Lycée**. Il repose sur un principe simple : afficher une opération à l'écran et demander à l'élève d'en trouver le résultat — addition, soustraction, multiplication ou division.

Le logiciel est pensé pour un usage en établissement scolaire avec une gestion complète des classes, des groupes et des profils élèves, et un suivi des progrès par les enseignants.

**Compatibilité :** Windows 10/11 et Linux (Fedora, et toute distribution supportant les paquets RPM).

---

## Installation

### Depuis les sources (Windows & Linux)

```bash
# 1. Cloner le dépôt
git clone https://github.com/WedoneOfficiel/Wedone-Operate.git
cd Wedone-Operate

# 2. Installer les dépendances
pip install -r requirements.txt
# Sur Linux : pip install -r requirements.txt --break-system-packages

# 3. Lancer
python main.py
```

### Depuis un binaire (releases)

Les exécutables `.exe` (Windows) et `.rpm` (Linux, paquet RPM) sont disponibles sur la page [**Releases**](https://github.com/WedoneOfficiel/Wedone-Operate/releases).

> Le logiciel ne requiert aucun droit administrateur pour être installé.

---

## Première connexion

| Rôle | Mot de passe par défaut |
|------|------------------------|
| Administrateur | `admin1234` |

> ⚠️ **Modifiez ce mot de passe dès la première connexion** via Paramètres → Mot de passe.

### Mise en place recommandée

1. **Admin** → créer les comptes professeurs *(Gestion → Professeurs)*
2. **Prof** → créer les classes et les groupes avec leur niveau scolaire *(Gestion → Classes / Groupes)*
3. **Prof** → ajouter les élèves et les assigner aux groupes *(Gestion → Élèves)*
4. **Prof** *(optionnel)* → créer un modèle de session pour chaque groupe *(Gestion → Modèles)*
5. **Élève** → se connecter en sélectionnant Classe → Groupe → Profil

---

## Fonctionnalités

### Rôles et permissions

Trois types de comptes avec des accès distincts :

| Action | Admin | Prof | Élève |
|--------|:-----:|:----:|:-----:|
| Créer / supprimer des profs | ✅ | — | — |
| Créer des classes et groupes | ✅ | ✅ | — |
| Créer / supprimer des élèves | ✅ | ✅ | — |
| Créer des modèles de session | ✅ | ✅ | — |
| Voir les stats de ses groupes | ✅ | ✅ | — |
| Jouer | — | — | ✅ |
| Voir ses propres stats | — | — | ✅ |
| Mises à jour | ✅ | ✅ | — |
| Changer son mot de passe | ✅ | ✅ | — |

### Niveaux scolaires

Plages de calcul adaptées aux programmes officiels, du CP au Lycée :

| Niveau | Addition | Multiplication | Chrono |
|--------|----------|----------------|--------|
| CP | 1 – 9 | tables ×2 | 45 s |
| CE1 | 1 – 20 | tables ×5 | 40 s |
| CE2 | 1 – 50 | tables ×5 | 35 s |
| CM1 | 1 – 100 | tables ×9 | 30 s |
| CM2 | 1 – 500 | tables ×10 | 25 s |
| 6e | 1 – 999 | tables ×12 | 20 s |
| 5e | 1 – 9 999 | ×2–15 | 18 s |
| 4e | 1 – 9 999 | ×2–20 | 15 s |
| 3e | 1 – 99 999 | ×2–25 | 12 s |
| Lycée | 1 – 99 999 | ×2–50 | 10 s |

### Tableau de bord (admin / prof)

- Résumé rapide : nombre de groupes, d'élèves, de sessions, moyenne globale
- **Alertes automatiques** : élèves dont la moyenne est inférieure à 50 % sur les 3 dernières sessions
- **Recommandations de niveau** générées automatiquement selon les résultats
- Aperçu par groupe avec code couleur (vert / orange / rouge)

### Modèles de session

Un professeur peut créer une configuration de session (niveau, opérations, nombre d'épreuves, chronomètre) et l'assigner à un groupe. L'élève la retrouve pré-remplie à la connexion et peut la modifier librement avant de lancer.

### Statistiques

- Historique complet des sessions par élève
- Stats de groupe : moyenne, meilleur score, progression
- **Export CSV** des résultats d'un groupe

---

## Versionnage

Ce projet utilise le format **`Stable année.mois.jour`** (ex. `Stable 2026.03.17`).  
Chaque nouvelle version rend automatiquement la précédente obsolète. Seule la version la plus récente est supportée. Les mises à jour sont vérifiées au démarrage via l'**API GitHub Releases**.

---

## Contact

Pour toute demande d'assistance :

- **Mastodon** *(à privilégier)* : [@wedoneofficiel@mastodon.social](https://mastodon.social/@wedoneofficiel)
- **Mail** : wedoneofficiel@outlook.fr

---

## Historique des versions

### Stable 2026.03.17 — 18/03/2026

- **Migration PyQt5 → PyQt6**
- Nouveau système de rôles : Admin, Professeur, Élève
- Hiérarchie Classe → Groupe (avec niveau scolaire) → Élève
- Connexion élève en 3 étapes : Classe → Groupe → Profil (cartes visuelles)
- Tableau de bord admin/prof avec alertes et recommandations automatiques
- Modèles de session assignables par groupe
- Niveaux scolaires CP → Lycée (remplace Facile/Moyen/Difficile)
- Thème sombre automatique (Windows/GNOME) ou manuel
- Jauge circulaire animée sur l'écran de résultats
- Export CSV des stats de groupe
- Mises à jour via API GitHub Releases (remplace les fichiers .txt)
- Nouveau format de versionnage `Stable année.mois.jour`

### Stable 4.1 — 20/07/2024

- Optimisation du code et des performances
- Ajout d'un système de détection automatique des versions obsolètes
- Modifications mineures de l'interface

### Stable 4.0 — 09/05/2024

- Suppression automatique des fichiers installés par les versions précédentes
- Installation forcée en mode non-administrateur (compatibilité Windows)
- Changement de répertoire GitHub pour la gestion des mises à jour
- Ajout d'une fenêtre de paramètres complète :
  - **Options du logiciel** : activation/désactivation des types d'opérations
  - **Mises à jour** : recherche automatique et manuelle (mises à jour + patchs)
  - **À propos** : numéro de version, licence, informations du logiciel

### Stable 3.5 — 18/04/2024

- Correction de bugs de l'interface graphique
- Mise en place de la recherche automatique des patchs de sécurité

### Stable 3.4 — 07/04/2024

- Utilisation de la touche Entrée dans les zones de texte
- Refonte de la fenêtre des mises à jour
- Uniformisation du design (toutes les boîtes de dialogue deviennent des fenêtres)
- Optimisation du code

### Stable 3.3 — 27/03/2024

- Amélioration de l'accessibilité (choix des couleurs de l'interface)

### Stable 3.2 — 11/02/2024

- Correctif de bugs

### Stable 3.1 — 12/01/2024

- Refonte de l'interface graphique, design plus épuré
- Correctif de bugs

### Stable 3.0 — 08/11/2023

- **Interface graphique** (première version avec GUI)
- **Passage du C au Python** — toutes les fonctionnalités portées

### Stable 2.3 — 27/08/2023

- Correction du problème de compatibilité avec Windows 11
- Amélioration de la gestion de la RAM
- Correction de bugs

### Stable 2.2 — 23/07/2023

- **Recherche automatique des mises à jour** (première implémentation)
- Amélioration de la gestion de la RAM
- Amélioration des propositions de calculs

### Stable 2.1 — 27/06/2023

- Correction de bugs
- Le logo de l'installateur correspond désormais à celui du logiciel
- Amélioration des propositions de calculs : somme ≤ 150, résultats positifs garantis, multiplications et divisions jusqu'à la table de 10

### Stable 2.0 — 11/04/2023

- Nouveau logo
- Encodage UTF-8 (caractères spéciaux français)
- Refonte complète du code de base
- L'utilisateur choisit le nombre d'épreuves
- Opérations et valeurs aléatoires
- Score affiché en fin de session (plus après chaque épreuve)

### Stable 1.7 — 05/04/2023

- Ajout de 2 épreuves
- Ajout de la commande de sortie (saisir 999)

### Stable 1.6 — 22/11/2022

- Ajout d'une épreuve
- Correction de bugs, amélioration de la gestion RAM

### Stable 1.5 — 11/11/2022

- Ajout de 6 épreuves

### Stable 1.4 — 08/10/2022

- Ajout de 5 épreuves
- Ajout du pourcentage de réussite

### Stable 1.3 — 17/09/2022

- Ajout d'une icône au logiciel
- Ajout du score
- Ajout de 2 épreuves
- Les mises à jour remplacent désormais l'exécutable automatiquement

### Stable 1.2 — 16/09/2022

- Ajout du retour bonne/mauvaise réponse

### Stable 1.1 — 24/08/2022

- Ajout d'un exercice
- Amélioration de la gestion RAM

### Stable 1.0 — 19/08/2022

- Ajout d'exercices
- Correctifs de bugs

### Bêta 1.1 — 09/08/2022

- Exercice supplémentaire
- Ajout d'un installateur `.exe`
- Amélioration de la compatibilité

### Bêta 1.0 — 05/08/2022

- Premier exercice

---

## Versions obsolètes

| Version | Date de sortie |
|---------|---------------|
| Stable 4.1 | 20/07/2024 |
| Stable 4.0 | 09/05/2024 |
| Stable 3.5 | 18/04/2024 |
| Stable 3.4 | 07/04/2024 |
| Stable 3.3 | 27/03/2024 |
| Stable 3.2 | 11/02/2024 |
| Stable 3.1 | 12/01/2024 |
| Stable 3.0 | 08/11/2023 |
| Stable 2.3 | 27/08/2023 |
| Stable 2.2 | 23/07/2023 |
| Stable 2.1 | 27/06/2023 |
| Stable 2.0 | 11/04/2023 |
| Stable 1.7 | 05/04/2023 |
| Stable 1.6 | 22/11/2022 |
| Stable 1.5 | 11/11/2022 |
| Stable 1.4 | 08/10/2022 |
| Stable 1.3 | 17/09/2022 |
| Stable 1.2 | 16/09/2022 |
| Stable 1.1 | 24/08/2022 |
| Stable 1.0 | 19/08/2022 |
| Bêta 1.1 | 09/08/2022 |
| Bêta 1.0 | 05/08/2022 |

> Toutes ces versions sont obsolètes et ne reçoivent plus aucun support. Seule la version la plus récente est maintenue. Le canal bêta est définitivement abandonné.

---

## Blog

### Passage à la Stable 2026.03.17 — refonte complète

La version Stable 2026.03.17 sortira le 18 mars 2026. Wedone Operate passe de PyQt5 à **PyQt6** et s'enrichit d'un vrai système multi-utilisateurs avec trois rôles (Admin, Professeur, Élève), une hiérarchie de classes et de groupes, des niveaux scolaires du CP au Lycée, un tableau de bord enseignant avec alertes automatiques, et des modèles de session personnalisables. Le format de versionnage change également : finis les numéros 4.x, le projet adopte désormais le format `Stable année.mois.jour`.

*WedoneOfficiel — 17/03/2026*

---

### Passage à la version 4.0 — 09/05/2024

Le 9 mai 2024 a été introduite la nouvelle version majeure de Wedone Operate. En dehors des nombreuses améliorations apportées, il faut noter que l'installation pour tous les utilisateurs sous Windows a été bloquée car le système de gestion du logiciel faisait crasher le logiciel. Nous vous recommandons donc de désinstaller votre version actuelle puis de réinstaller la nouvelle version avec le mode "installer seulement pour moi" (sélectionné automatiquement), qui lui ne présente pas de problèmes.

*WedoneOfficiel — 09/05/2024*

---

### Changements concernant le support du logiciel — 09/05/2024

La politique de support stipulait que la dernière version d'une version majeure bénéficiait de 2 ans de support. Il a été décidé d'uniformiser et simplifier la gestion globale : le support est désormais de **1 an pour toutes les versions** (hors bêtas), y compris pour les versions antérieures à la Stable 4.0.

*WedoneOfficiel — 09/05/2024*

---

### Fichiers non supprimés avec la mise à jour 3.1 — 12/01/2024

Avec la version 3.1, un dossier `_internal` contenant de nombreux fichiers est présent dans le répertoire d'installation de Wedone Operate mais ne sert plus. Il faut le retirer manuellement. Si vous avez installé la version administrateur sans changer le répertoire, ce dossier se trouve dans `C:\Program Files (x86)\Wedone Operate`.

*WedoneOfficiel — 12/01/2024*

---

### La version 3.0 est arrivée ! — 08/11/2023

C'est avec plaisir que j'annonce l'arrivée de Wedone Operate 3.0 qui arrive pour la toute première fois avec une interface graphique ! Ce choix n'est pas sans conséquences : pour permettre un développement de qualité et rapide, il a fallu changer de langage de programmation. Le logiciel n'est donc plus développé en C mais en Python. Il sera un peu plus lourd, mais toutes les fonctionnalités de la version 2.3 ont été portées. Pensez à désinstaller l'ancien programme avant d'installer le nouveau.

*WedoneOfficiel — 08/11/2023*

---

### Problème de compatibilité avec Windows 11 réglé ! — 27/08/2023

Le souci que rencontrait Wedone Operate à s'ouvrir sous Windows 11 est maintenant réglé !

*WedoneOfficiel — 27/08/2023*

---

### Recherche des mises à jour automatique ! — 23/07/2023

À compter de la version 2.2, les mises à jour sont recherchées automatiquement par le logiciel afin de vous alerter sur la sortie de nouvelles versions. Ceci ne s'applique pas aux versions antérieures à la version 2.2.

*WedoneOfficiel — 23/07/2023*

---

### Passage à la version 2.0 ! — 13/04/2023

Le 11 avril 2023 marque une rupture dans l'histoire du logiciel. Le code de base a été complètement revu :
- L'utilisateur choisit lui-même le nombre d'épreuves
- Le choix des opérations est devenu aléatoire
- Les valeurs des opérations sont devenues aléatoires (entre 0 et 50 pour chaque terme)
- Le score s'affiche en fin de session et non plus après chaque épreuve
- Suppression de la commande d'arrêt par saisie de 999

*WedoneOfficiel — 13/04/2023*

---

### Suppression automatique des anciennes versions lors des mises à jour — 17/09/2022

À compter de la version 1.3, les mises à jour suppriment et remplacent l'exécutable du logiciel, contrairement aux versions antérieures qui s'installaient à côté des autres versions. Ceci ne s'applique pas aux versions antérieures à la Stable 1.3.

*WedoneOfficiel — 17/09/2022*

---

### Abandon du canal Bêta — 14/09/2022

Il n'y aura plus de mises à jour pour le canal Bêta. Référez-vous aux versions stables.

*WedoneOfficiel — 14/09/2022*

---

## Licence

Distribué sous licence **Apache 2.0** — voir [LICENSE](LICENSE).  
© 2022–2026 WedoneOfficiel
