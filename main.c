#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <locale.h>

int main(void)
{
    int nombre_epreuves = 0;
    int i = 0; // compteur de boucle
    int nombre1 = 0;
    int nombre2 = 0;
    int operation = 0;
    int resultat = 0;
    int reponse = 0; // réponse de l'utilisateur
    int score = 0; // nombre d'épreuves réussies
    int pourcentage = 0; // pourcentage de réussite
    srand(time(NULL)); // initialiser le générateur avec le temps actuel
    setlocale(LC_CTYPE,"fr_FR.UTF-8"); // utiliser le paramètre régional du système
    printf("Bienvenue dans Wedone Operate (stable 2.0) ! Bonne aventure !\n\n");
    printf("Combien d'épreuves voulez-vous faire ? ");
    scanf("%d", &nombre_epreuves);
    for(i = 1; i <= nombre_epreuves; i++) // boucle pour répéter les épreuves
    {
        nombre1 = (rand() % 50) + 1; // générer un nombre entre 1 et 50
        nombre2 = (rand() % 50) + 1; // générer un autre nombre entre 1 et 50
        operation = (rand() % 4) + 1; // générer un nombre entre 1 et 4 pour choisir l'opération
        switch(operation)
        {
            case 1: // addition
                resultat = nombre1 + nombre2;
                printf("Épreuve %d : %d + %d = ?\n", i, nombre1, nombre2);
                break;
            case 2: // soustraction
                resultat = nombre1 - nombre2;
                printf("Épreuve %d : %d - %d = ?\n", i, nombre1, nombre2);
                break;
            case 3: // multiplication
                resultat = nombre1 * nombre2;
                printf("Épreuve %d : %d * %d = ?\n", i, nombre1, nombre2);
                break;
            case 4: // division
                if(nombre2 != 0) // éviter la division par zéro
                {
                    resultat = nombre1 / nombre2;
                    printf("Épreuve %d : %d / %d = ?\n", i, nombre1, nombre2);
                }
                else
                {
                    resultat = -1; // valeur impossible à deviner
                    printf("Épreuve %d : Division par zéro impossible\n", i);
                }
                break;
            default:
                printf("Opération invalide\n");
        }
        printf("Votre réponse : ");
        scanf("%d", &reponse); // lire la réponse de l'utilisateur
        if(reponse == resultat) // vérifier si la réponse est correcte
        {
            score++; // augmenter le score
            printf("Bonne réponse !\n");
        }
        else
        {
            printf("Mauvaise réponse ! La bonne réponse était %d.\n", resultat);
        }
    }
    pourcentage = (score * 100) / nombre_epreuves; // calculer le pourcentage de réussite
    printf("Vous avez réussi %d épreuves sur %d.\n", score, nombre_epreuves);
    printf("Votre pourcentage de réussite est de %d%%.\n", pourcentage);
    printf("La fenetre va se fermer automatiquement dans 10s.\n");
    struct timespec ts; // déclarer une structure timespec
    ts.tv_sec = 10; // assigner le nombre de secondes à attendre
    ts.tv_nsec = 0; // assigner le nombre de nanosecondes à attendre
    nanosleep(&ts, NULL); // attendre le temps spécifié
    return 0;
}
