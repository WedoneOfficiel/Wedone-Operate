#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <locale.h>

int main(void)
{
    int nombre_epreuves = 0;
    int i = 0; // compteur de boucle
    //addition
    int nombre1addition = 0;
    int nombre2addition = 0;
    //soustraction
    int nombre1soustraction = 0;
    int nombre2soustraction = 0;
    //multiplication
    int nombre1multiplication = 0;
    int nombre2multiplication = 0;
    //division
    int nombre1division = 0;
    int nombre2division = 0;
    int operation = 0;
    int resultat = 0;
    int reponse = 0; // réponse de l'utilisateur
    int score = 0; // nombre d'épreuves réussies
    int pourcentage = 0; // pourcentage de réussite
    srand(time(NULL)); // initialiser le générateur avec le temps actuel
    setlocale(LC_CTYPE,"fr_FR.UTF-8"); // utiliser le paramètre régional du système
    printf("Bienvenue dans Wedone Operate (stable 2.1) ! Bonne aventure !\n\n");
    printf("Combien d'épreuves voulez-vous faire ? ");
    scanf("%d", &nombre_epreuves);
    for(i = 1; i <= nombre_epreuves; i++) // boucle pour répéter les épreuves
    {
        nombre1addition = (rand() % 100) + 1; // générer un nombre entre 1 et 100
        nombre2addition = (rand() % 50) + 1; // générer un autre nombre entre 1 et 50

        nombre1soustraction = (rand() % 100) + 1; // générer un nombre entre 1 et 100
        nombre2soustraction = (rand() % 50) + 1; // générer un autre nombre entre 1 et 50

        nombre1multiplication = (rand() % 10) + 0; // générer un nombre entre 0 et 10
        nombre2multiplication = (rand() % 10) + 0; // générer un autre nombre entre 0 et 10

        nombre1division = (rand() % 10) + 0; // générer un nombre entre 0 et 10
        nombre2division = (rand() % 10) + 0; // générer un autre nombre entre 0 et 10

        operation = (rand() % 4) + 1; // générer un nombre entre 1 et 4 pour choisir l'opération
        switch(operation)
        {
            case 1: // addition
                resultat = nombre1addition + nombre2addition;
                printf("Épreuve %d : %d + %d = ?\n", i, nombre1addition, nombre2addition);
                break;
            case 2: // soustraction
                resultat = nombre1soustraction - nombre2soustraction;
                printf("Épreuve %d : %d - %d = ?\n", i, nombre1soustraction, nombre2soustraction);
                break;
                if(nombre2soustraction > 0)
                {
                    resultat = nombre1soustraction / nombre2soustraction;
                    printf("Épreuve %d : %d / %d = ?\n", i, nombre1soustraction, nombre2soustraction);
                }
                else
                {
                    resultat < 0; // valeur impossible à deviner
                    printf("Épreuve %d : Soustraction impossible\n", i);
                }
            case 3: // multiplication
                resultat = nombre1multiplication * nombre2multiplication;
                printf("Épreuve %d : %d * %d = ?\n", i, nombre1multiplication, nombre2multiplication);
                break;
            case 4: // division
                if(nombre2division != 0) // éviter la division par zéro
                {
                    resultat = nombre1division / nombre2division;
                    printf("Épreuve %d : %d / %d = ?\n", i, nombre1division, nombre2division);
                }
                else if(nombre2division == 0){
                    resultat = 0; // valeur impossible à deviner
                    printf("Épreuve %d : Division par zéro impossible\n", i);
                }
                else if(nombre1division == 0){
                    resultat = 0; // valeur impossible à deviner
                    printf("Épreuve %d : Division par zéro impossible\n", i);
                }
                else{
                    resultat < 0; // valeur impossible à deviner
                    printf("Épreuve %d : Division par une valeur négative impossible\n", i);
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
