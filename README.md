<div align="center">
  <h1>Wedone Operate</h1>
  <p><strong>Logiciel de calcul mental pour l'école</strong></p>
  <p>
    <img src="https://img.shields.io/badge/version-2026.03.17-blue" alt="version"/>
    <img src="https://img.shields.io/badge/python-3.10%2B-green" alt="python"/>
    <img src="https://img.shields.io/badge/PyQt6-6.4%2B-orange" alt="pyqt6"/>
    <img src="https://img.shields.io/badge/licence-Apache%202.0-lightgrey" alt="licence"/>
    <img src="https://img.shields.io/badge/plateforme-Windows%20%7C%20Linux-informational" alt="plateforme"/>
  </p>
</div>

---

## Présentation

Wedone Operate est un logiciel de calcul mental destiné aux élèves du **CP au Lycée**. Il permet aux enseignants de créer des classes, des groupes de niveaux et des modèles de session personnalisés, tout en offrant un suivi détaillé des progrès de chaque élève.

### Fonctionnalités principales

- **Trois rôles** : Administrateur (établissement), Professeur, Élève
- **Hiérarchie** : Classes → Groupes (avec niveau scolaire CP→Lycée) → Élèves
- **Niveaux scolaires** : plages de calcul adaptées à chaque classe, du CP au Lycée
- **Modèles de session** : le prof définit une configuration par défaut pour son groupe (l'élève peut la modifier)
- **Recommandations automatiques** : analyse des résultats pour adapter le niveau proposé
- **Tableau de bord** admin/prof : stats rapides + alertes élèves en difficulté
- **Statistiques détaillées** : historique, progression, export CSV par groupe
- **Thème clair/sombre** : automatique selon le système (Windows/GNOME) ou manuel
- **Mises à jour automatiques** via l'API GitHub Releases

---

## Installation

### Prérequis

- Python 3.10 ou supérieur
- pip

### Étapes

```bash
# 1. Cloner le dépôt
git clone https://github.com/WedoneOfficiel/Wedone-Operate.git
cd Wedone-Operate

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
python main.py
```

> **Linux (Fedora/Ubuntu)** : si pip échoue, utiliser `pip install -r requirements.txt --break-system-packages`

---

## Première utilisation

### Connexion administrateur

Au premier lancement, connectez-vous avec le compte administrateur :

| Champ | Valeur |
|-------|--------|
| Mot de passe | `admin1234` |

> ⚠️ **Changez ce mot de passe dès la première connexion** via Paramètres → Mot de passe.

### Mise en place recommandée

1. **Admin** : créer les comptes professeurs (Gestion → Professeurs)
2. **Prof** : créer les classes (Gestion → Classes)
3. **Prof** : créer les groupes avec leur niveau scolaire (Gestion → Groupes)
4. **Prof** : ajouter les élèves et les assigner aux groupes (Gestion → Élèves)
5. **Prof** *(optionnel)* : créer un modèle de session pour chaque groupe (Gestion → Modèles)
6. **Élève** : se connecter en sélectionnant Classe → Groupe → Profil

---

## Structure du projet

```
wedone-operate/
├── main.py              # Point d'entrée
├── constants.py         # Niveaux scolaires, plages de calcul, palettes
├── database.py          # Couche de données JSON (users, classes, groupes, scores)
├── session.py           # Session utilisateur courante (rôle, permissions)
├── settings.py          # Paramètres applicatifs (settings.json)
├── updater.py           # Vérification des mises à jour via GitHub API
├── requirements.txt
├── icon.png             # Icône de l'application (à fournir)
└── ui/
    ├── theme.py             # Feuilles de style Qt (thème clair/sombre)
    ├── screen_login.py      # Connexion : Admin/Prof (mdp) + Élève (3 étapes)
    ├── screen_dashboard.py  # Tableau de bord admin/prof
    ├── screen_main.py       # Écran de jeu élève
    ├── screen_game.py       # Déroulé des épreuves + chronomètre
    ├── screen_results.py    # Résultats avec jauge circulaire animée
    ├── screen_stats.py      # Statistiques personnelles + groupe + export CSV
    ├── screen_admin.py      # Gestion classes/groupes/élèves/profs/modèles
    ├── screen_settings.py   # Paramètres (filtrés selon le rôle)
    └── dialog_update.py     # Dialogue de mise à jour disponible
```

### Fichiers de données (générés automatiquement)

| Fichier | Contenu |
|---------|---------|
| `users.json` | Comptes admin, profs et élèves |
| `classes.json` | Classes de l'établissement |
| `groups.json` | Groupes avec niveau scolaire |
| `scores.json` | Historique des sessions par élève |
| `templates.json` | Modèles de session créés par les profs |
| `settings.json` | Préférences (thème, mise à jour…) |

> Ces fichiers sont exclus du dépôt Git (`.gitignore`). Ils sont créés au premier lancement.

---

## Niveaux scolaires et plages de calcul

| Niveau | Addition | Soustraction | Multiplication | Division | Chrono |
|--------|----------|--------------|----------------|----------|--------|
| CP | 1–9 | 1–10 | tables ×2 | ÷1–2 | 45 s |
| CE1 | 1–20 | 1–20 | tables ×5 | ÷1–5 | 40 s |
| CE2 | 1–50 | 1–50 | tables ×5 | ÷1–5 | 35 s |
| CM1 | 1–100 | 1–100 | tables ×9 | ÷1–9 | 30 s |
| CM2 | 1–500 | 1–500 | tables ×10 | ÷1–10 | 25 s |
| 6e | 1–999 | 1–999 | tables ×12 | ÷1–12 | 20 s |
| 5e | 1–9 999 | 1–9 999 | ×2–15 | ÷2–15 | 18 s |
| 4e | 1–9 999 | 1–9 999 | ×2–20 | ÷2–20 | 15 s |
| 3e | 1–99 999 | 1–99 999 | ×2–25 | ÷2–25 | 12 s |
| Lycée | 1–99 999 | 1–99 999 | ×2–50 | ÷2–50 | 10 s |

---

## Versionnage

Ce projet utilise le format **`année.mois.jour`** (ex. `2026.03.17`).  
Chaque nouvelle version rend la précédente obsolète. Il n'y a pas de système de patch séparé.

Les mises à jour sont vérifiées au démarrage via l'**API GitHub Releases** et peuvent être désactivées dans les paramètres.

---

## Distribution

| Plateforme | Format | Outil |
|------------|--------|-------|
| Windows | `.exe` | PyInstaller |
| Linux (universel) | `.flatpak` | Flatpak (install local sans Flathub) |

Les binaires sont disponibles dans les [Releases GitHub](https://github.com/WedoneOfficiel/Wedone-Operate/releases).

---

## Développement

```bash
# Lancer en mode développement
python main.py

# Vérifier la syntaxe de tous les fichiers
python -c "
import ast, os
for r, d, files in os.walk('.'):
    for f in files:
        if f.endswith('.py'):
            p = os.path.join(r, f)
            try: ast.parse(open(p).read()); print(f'✔ {p}')
            except SyntaxError as e: print(f'✘ {p}: {e}')
"
```

### Contribuer

1. Fork le dépôt
2. Créer une branche (`git checkout -b feature/ma-feature`)
3. Commiter (`git commit -m 'Ajout de ma feature'`)
4. Pusher (`git push origin feature/ma-feature`)
5. Ouvrir une Pull Request

---

## Licence

Distribué sous licence **Apache 2.0**.  
Voir [LICENSE](LICENSE) pour plus de détails.

---

## Crédits

Développé par [WedoneOfficiel](https://github.com/WedoneOfficiel)  
© 2022–2026 WedoneOfficiel
