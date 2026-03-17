# Contribuer à Wedone Operate

Merci de l'intérêt pour le projet ! Voici comment contribuer.

## Signaler un bug

Ouvrez une [issue GitHub](https://github.com/WedoneOfficiel/Wedone-Operate/issues) en précisant :
- La version du logiciel (`2026.03.17`)
- Le système d'exploitation (Windows / Linux, distribution)
- La version de Python (`python --version`)
- Le message d'erreur complet (traceback)
- Les étapes pour reproduire le bug

## Proposer une fonctionnalité

Ouvrez une issue avec le label `enhancement` et décrivez :
- Le besoin pédagogique
- Le comportement attendu
- Des exemples d'utilisation

## Soumettre du code

```bash
# 1. Fork + clone
git clone https://github.com/VOTRE-USERNAME/Wedone-Operate.git
cd Wedone-Operate

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Créer une branche
git checkout -b feature/description-courte

# 4. Développer et tester
python main.py

# 5. Vérifier la syntaxe
python -c "import ast, os; [ast.parse(open(os.path.join(r,f)).read()) for r,d,fs in os.walk('.') for f in fs if f.endswith('.py')]"

# 6. Commiter et pusher
git commit -m "feat: description de la modification"
git push origin feature/description-courte
```

## Convention de versionnage

Le format est `année.mois.jour` (ex. `2026.06.15`).  
Chaque release rend la précédente obsolète.  
Pour publier une release, mettre à jour `APP_VERSION` dans `constants.py` et créer un tag Git correspondant.

## Structure du code

- `constants.py` — toutes les valeurs fixes (niveaux, palettes, fichiers)
- `database.py` — toutes les opérations sur les données JSON
- `session.py` — état de la session en cours (ne pas persister ici)
- `ui/` — un fichier par écran, logique UI uniquement
