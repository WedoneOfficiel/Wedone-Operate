# Wedone Operate : Tour du logiciel 
<p align="center">
  <img src="https://raw.githubusercontent.com/WedoneOfficiel/Wedone-Operate/main/app-icone.ico" />
</p>
Wedone Operate est un jeu adressé aux élèves (et classes) de cycle 3 (CM1, CM2 et 6ème). Ce jeu s'appuie sur le principe du calcul à mental, il consiste à demander le résultat d'un opération (ajoutée, multiplié, soustraite, divisée) en fonction d'un résultat qui apparait à l'écran.

Logiciel actuellement disponible uniquement pour les ordinateurs équipés de Microsoft Windows (x86 ET x86_64).

Nous vous certifions que ce logiciel est compatible avec ces versions de Microsoft Windows : 8.1 / 10 / 11. Les versions non citées ci-avant peuvent s'avérer compatibles avec le présent logiciel mais notre équipe ne l'a actuellement pas vérifié.

Nous vous recommandons donc d'utiliser une des éditions citées précédemment pour un rendu de qualité.

 
# Dernière version
Stable version 2.1 - télécharger à cette page : https://github.com/WedoneOfficiel/Wedone-Operate/releases/tag/Stable-v2.1

# Planning de publications
23/07/2023 | Stable 2.2

27/06/2023 | Stable 2.1 - Publié -

11/04/2023 | Stable 2.0 - Publié -

05/04/2023 | Stable 1.7 - Publié -

22/11/2022 | Stable 1.6 - Publié -

11/11/2022 | Stable 1.5 - Publié -

08/10/2022 | Stable 1.4 - Publié -

17/09/2022 | Stable 1.3 - Publié -

16/09/2022 | Stable 1.2 - Publié -

24/08/2022 | Stable 1.1 - Publié -

19/08/2022 | Stable 1.0 - Publié -

09/08/2022 | Bêta 1.1 - Publié -

05/08/2022 | Bêta 1.0 - Publié -

# Nouveautés de chaques versions
#### Stable 2.2 :
- Correction de bugs
- Amélioration de la gestion de la RAM
- Amélioration des propositions de calculs
- Recherche automatique de mises à jour : voir les détails dans le [blog](https://github.com/WedoneOfficiel/Wedone-Operate/blob/main/README.md#recherche-des-mises-%C3%A0-jour-automatique-")

#### Stable 2.1 :
- Correction de bugs
- Le logo de l'installateur est désormais le même que celui du logiciel
- Amélioration des propositions de calculs*

*La somme de l'addition ne peut pas être supérieure à 150, le résultat des soustractions ne peut pas être négatif et le premier nombre ne peut pas être soustrait par un nombre de plus de 50, les multiplications vont jusqu'à la table de 10 (idem pour les divisions). Les divisions par 0 et les résultats négatifs ne peuvent pas être proposés comme calculs.
#### Stable 2.0 :
- Changement du logo du logiciel
- Ajout d'un paramètre pour les caractères spéciaux en français (UTF-8)
- Correction de bugs
- Amélioration de la gestion des ressources de la mémoire vive (RAM)
- Revue complète du code de base du logiciel (= transformation du logiciel) : voir les détails dans le [blog](https://github.com/WedoneOfficiel/Wedone-Operate/blob/main/README.md#passage-%C3%A0-la-version-20- "article du blog concernant le passage à la version 2.0")
#### Stable 1.7 :
- Ajout de 2 épreuves
- Ajout de la fonction "quitter" en entrant 999 dans le logiciel
#### Stable 1.6 :
- Ajout de 1 épreuve
- Correction de bugs
- Amélioration de la gestion des ressources de la mémoire vive (RAM)
#### Stable 1.5 :
- Ajout de 6 épreuves
#### Stable 1.4 :
- Ajout de 5 épreuves
- Ajout de la fonctionnalité pourcentage de réussite
#### Stable 1.3 :
- Ajout d'une icône au logiciel
- Ajout de la fonctionnalité score
- Ajout de 2 épreuves
#### Stable 1.2 :
- Ajout de la fonctionalité bonne/mauvaise réponse
#### Stable 1.1 :
- Ajout d'un exercice
- Amélioration de la gestion des ressources de la mémoire vive (RAM)
#### Stable 1.0 :
- Ajout d'exercices
- Correctif de certains bugs
#### Bêta 1.1 :
- Ajout d'un exercice supplémentaire 
- Ajout d'un installateur .exe (setup)
- Amélioration compatibilité du logiciel
#### Bêta 1.0 : 
- Ajout d'un exercice 

# Comment compiler le programme ?
/!\ La compilation du programme n'est utile que si vous avez modifié le code source /!\
1) Installez le compialteur GCC.
2) Ouvrez dans un terminal l'emplacement où sont stockés les fichiers codes du logiciel.
3) Exécuter cette comande dans le terminal : gcc main.c icone.o -o main.    
4) Un fichier exécutable apparait alors dans le dossier où sont stockés les fichiers codes du logiciel. Vous pouvez dès lors l'éxécuter !

# Blog

## Recherche des mises à jour automatique !
A compter de la version 2.2 du logiciel, les mises à jour seront recherchées automatiquemet par le logiciel afin de vous alerter sur la sortie de nouvelle versions.
Attention, ceci ne s'applique pas au versions antérieures à la version 2.2.

WedoneOfficiel - le 23/07/2023 à 01:32

## Passage à la version 2.0 !
Le 11 Avril 2023 marque une rupture dans l'histoire du logiciel Wedone Operate. En effet, le logiciel est sorti en version 2.0. Ce passage à la version 2.0 s'explique par le fait que le code de base du logiciel à complètement été revu. Il y a donc eu de nombreuses modifications au sein même du logiciel :
- L'utilisateur choisit le nombre d'épreuves qu'il souhaite faire
- Le choix des opérations est devenu aléatoire
- Les valeurs des opérations sont devenues aléatoires*
- Le score ne s'affiche plus après chaque épreuve mais à la fin du "parcours" d'épreuves
- Supression de la fonctionalité "Arrêt du porgramme" lorsque l'on entre 999 dans le logiciel

*Pour la version 2.0, il y a deux valeurs qui sont définies aléatoirement :
1) La première partie d'un calcul pour les additions soustractions et multiplications (valeur comprise entre 0 et 50)
2) La dexuième partir d'un calcul pour les additions soustractions et multiplications (valeur comprise entre 0 et 50)

WedoneOfficiel - le 13/04/2023 à 17:46

## Suppression automatique des anciennes versions lors des mises à jour
A compter de la version 1.3, les mises à jour supprimeront et remplaceront l'exécutable du logiciel contrairement aux versions antérieures qui elles s'installaient à côté des autres versions.
Ceci ne s'applique pas aux versions antérieures à la version stable 1.3 (bêta 1.0/bêta 1.1/stable 1.0/stable 1.1/stable 1.2)

WedoneOfficiel - le 17/09/2022 à 23:43 (modifié le 21/09/2022 à 16:24)

## Abandon du canal Bêta
Il n'y aura plus de mises à jour pour le canal Bêta (plus de nouvelles versions), référez vous aux versions stables.

WedoneOfficiel - le 14/09/2022 à 18:25
