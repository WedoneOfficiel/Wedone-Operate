#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <locale.h>
#include <windows.h>

// Function to set the terminal title
void setTerminalTitle(const char* title) {
    SetConsoleTitleA(title);
}

#define VERSION "2.2" // Définir la version actuelle du logiciel

// Vérifier les mises à jour
void checkForUpdates(void)
{
    setlocale(LC_CTYPE, "fr_FR.UTF-8"); // utiliser le paramètre régional du système

    const char versionURL[] = "https://wedoneofficiel.github.io/Boot-projets-Wedone-Officiel/Wedone-Logiciels-Versions/version-wedone-operate.txt"; // Remplacez l'URL par l'emplacement réel du fichier version.txt sur votre serveur

    // Construire la commande "curl" avec l'URL
    char curlCommand[256];
    sprintf(curlCommand, "curl -sSf %s", versionURL);

    // Ouvrir un processus pour exécuter la commande "curl" et récupérer le contenu du fichier version.txt
    FILE *curlProcess = popen(curlCommand, "r");
    if (curlProcess == NULL)
    {
        printf("Erreur lors de la vérification des mises à jour.\n");
        return;
    }

    char latestVersion[16]; // Une chaîne pour stocker la version la plus récente (assumer que la version est inférieure à 16 caractères)
    if (fgets(latestVersion, sizeof(latestVersion), curlProcess) != NULL)
    {
        // Supprimer les caractères de nouvelle ligne ou d'espace de la chaîne récupérée
        latestVersion[strcspn(latestVersion, "\r\n")] = '\0';

        // Comparer la version actuelle avec la version la plus récente
        if (strcmp(latestVersion, VERSION) > 0)
        {
            printf("Une nouvelle version de Wedone Operate est disponible (version %s) !\n", latestVersion);
            printf("Veuillez la télécharger : https://github.com/WedoneOfficiel/Wedone-Operate/releases\n");
            printf("Vous pouvez ignorer cet avertissement et poursuivre, mais nous vous recommandons vivement de mettre à jour l'application afin d'obtenir les dernières nouveautés et derniers correctifs de sécurité.\n\n");
        }
        else
        {
            printf("Vous utilisez la dernière version de Wedone Operate.\n");
        }
    }
    else
    {
        printf("Impossible de récupérer la version la plus récente.\n");
    }

    pclose(curlProcess); // Fermer le processus "curl"
}

int main(void)
{
    setTerminalTitle("Wedone Operate"); // Set the terminal title to your desired title
    
    int nombre_epreuves = 0;
    int i = 0; // compteur de boucle
    int score = 0; // nombre d'épreuves réussies
    int pourcentage = 0; // pourcentage de réussite

    srand(time(NULL)); // initialiser le générateur avec le temps actuel
    setlocale(LC_CTYPE, ""); // utiliser le paramètre régional du système (utilise la locale du système)

    checkForUpdates(); // Vérifier les mises à jour avant de commencer les épreuves

    printf("Bienvenue dans Wedone Operate (stable %s) ! Bonne aventure !\n\n", VERSION);
    printf("Combien d'épreuves voulez-vous faire ? ");
    scanf("%d", &nombre_epreuves);

    for (i = 1; i <= nombre_epreuves; i++) // boucle pour répéter les épreuves
    {
        int nombre1 = 0;
        int nombre2 = 0;
        int operation = 0;
        int resultat = 0;
        int reponse = 0; // réponse de l'utilisateur

        // Générer les nombres aléatoires pour les opérations
        nombre1 = (rand() % 100) + 1;
        nombre2 = (rand() % 50) + 1;

        // Choix aléatoire de l'opération
        do
        {
            operation = (rand() % 4) + 1;
            switch (operation)
            {
            case 1: // addition
                resultat = nombre1 + nombre2;
                printf("Épreuve %d : %d + %d = ?\n", i, nombre1, nombre2);
                break;
            case 2: // soustraction
                if (nombre1 < nombre2 || nombre1 - nombre2 > 100)
                {
                    // Générer de nouveaux nombres pour la soustraction
                    nombre1 = (rand() % 100) + 1;
                    nombre2 = (rand() % 50) + 1;
                    continue; // Réessayer avec de nouveaux nombres
                }
                resultat = nombre1 - nombre2;
                printf("Épreuve %d : %d - %d = ?\n", i, nombre1, nombre2);
                break;
            case 3: // multiplication
                if (nombre1 > 10)
                {
                    nombre1 = nombre1 % 10;
                }
                if (nombre2 > 10)
                {
                    nombre2 = nombre2 % 10;
                }
                resultat = nombre1 * nombre2;
                printf("Épreuve %d : %d * %d = ?\n", i, nombre1, nombre2);
                break;
            case 4: // division
                if (nombre2 != 0 && nombre1 % nombre2 == 0)
                {
                    resultat = nombre1 / nombre2;
                    printf("Épreuve %d : %d / %d = ?\n", i, nombre1, nombre2);
                }
                else
                {
                    // Générer de nouveaux nombres pour la division
                    nombre1 = (rand() % 10) + 1;
                    nombre2 = (rand() % 10) + 1;
                    continue; // Réessayer avec de nouveaux nombres
                }
                break;
            default:
                printf("Opération invalide\n");
                continue; // Réessayer avec de nouveaux nombres
            }
        } while (resultat < 0); // Si le résultat est négatif, générer de nouveaux nombres pour l'opération

        printf("Votre réponse : ");
        scanf("%d", &reponse); // lire la réponse de l'utilisateur
        if (reponse == resultat) // vérifier si la réponse est correcte
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
