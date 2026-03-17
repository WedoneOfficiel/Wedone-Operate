# Changelog — Wedone Operate

Toutes les modifications notables sont documentées ici.  
Format : `année.mois.jour`

---

## [2026.03.17] — Version actuelle

### Nouveautés majeures

#### Système de rôles
- Trois rôles : **Admin** (établissement), **Professeur**, **Élève**
- Admin crée les comptes profs ; profs créent les élèves
- Permissions filtrées selon le rôle (paramètres, mises à jour, gestion)

#### Hiérarchie Classe → Groupe → Élève
- Les **classes** regroupent plusieurs groupes
- Chaque **groupe** est associé à un niveau scolaire (CP → Lycée)
- Tous les élèves d'un groupe partagent le même niveau

#### Niveaux scolaires CP → Lycée
- 10 niveaux avec plages de calcul adaptées aux programmes officiels
- Chronomètre par niveau (45 s en CP → 10 s au Lycée)
- Remplace l'ancien système Facile/Moyen/Difficile

#### Connexion élève en 3 étapes
- Sélection : Classe → Groupe → Profil
- Cartes visuelles avec initiales colorées
- Plus d'affichage de tous les élèves d'un coup

#### Tableau de bord admin/prof
- Résumé : nb groupes, élèves, sessions, moyenne globale
- Alertes automatiques : élèves avec moyenne < 50 % sur les 3 dernières sessions
- Recommandations de niveau adaptées
- Aperçu rapide de chaque groupe

#### Modèles de session
- Le prof crée des configurations réutilisables (niveau, opérations, durée, chrono)
- Assignation d'un modèle à un groupe
- Bandeau informatif pour l'élève, qui peut modifier les options

#### Recommandations automatiques
- Analyse des 5 dernières sessions
- Proposition de monter ou baisser le niveau selon la moyenne
- Ciblage des opérations les moins réussies

### Améliorations UI
- Jauge circulaire animée sur l'écran de résultats
- Barre de progression permanente pendant les épreuves
- Flash de fond vert/rouge sur bonne/mauvaise réponse
- Chronomètre coloré (vert → orange → rouge)
- Thème sombre : automatique selon le système (Windows/GNOME) ou manuel
- Migration complète PyQt5 → **PyQt6**

### Système de mises à jour
- Vérification via **API GitHub Releases** (remplace les fichiers .txt)
- Comparaison de version robuste par tuple d'entiers
- Affichage du changelog dans la fenêtre de mise à jour
- Abandon du système de patchs séparés

### Versionnage
- Nouveau format : **`année.mois.jour`** (ex. `2026.03.17`)
- Chaque release rend la précédente obsolète

### Technique
- `database.py` : couche de données unifiée (users/classes/groups/scores/templates)
- `session.py` : singleton de session avec système de permissions
- Architecture multi-fichiers (`ui/` package)
- `.gitignore` : données locales exclues du dépôt

### Corrections de bugs
- `KeyError 'user'` à la fin d'une session de jeu
- `IndexError` dans le chronomètre en fin de session
- `KeyError 'card_hover'` dans les feuilles de style
- `TypeError: NoneType is not callable` dans la navigation admin

---

## [4.1] — Version précédente (PyQt5)

- Système de calcul mental basique (addition, soustraction, multiplication, division)
- Paramètres : opérations activées, mises à jour automatiques
- Vérification de version via fichiers `.txt` hébergés sur GitHub Pages
- Système de patchs de sécurité séparé
- Interface PyQt5, thème clair uniquement
- Un seul type d'utilisateur (pas de rôles)
