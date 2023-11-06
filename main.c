#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <locale.h>
#include <windows.h>

#define VERSION "2.3"

void setTerminalTitle(const char* title) {
    SetConsoleTitleA(title);
}

void checkForUpdates(void) {
    setlocale(LC_CTYPE, "fr_FR.UTF-8"); // utiliser le paramètre régional du système

    const char versionURL[] = "https://wedoneofficiel.github.io/Boot-projets-Wedone-Officiel/Wedone-Logiciels-Versions/version-wedone-operate.txt";

    char curlCommand[256];
    sprintf(curlCommand, "curl -sSf %s", versionURL);

    FILE *curlProcess = popen(curlCommand, "r");
    if (curlProcess == NULL) {
        printf("Erreur lors de la vérification des mises à jour.\n");
        return;
    }

    char latestVersion[16];
    if (fgets(latestVersion, sizeof(latestVersion), curlProcess) != NULL) {
        latestVersion[strcspn(latestVersion, "\r\n")] = '\0';

        if (strcmp(latestVersion, VERSION) > 0) {
            printf("Une nouvelle version de Wedone Operate est disponible (version %s) !\n", latestVersion);
            printf("Veuillez la télécharger : https://github.com/WedoneOfficiel/Wedone-Operate/releases\n");
            printf("Nous vous recommandons de mettre à jour l'application pour obtenir les dernières fonctionnalités et correctifs de sécurité.\n\n");
        } else {
            printf("Vous utilisez la dernière version de Wedone Operate.\n");
        }
    } else {
        printf("Impossible de récupérer la version la plus récente.\n");
    }

    pclose(curlProcess);
}

int main(void) {
    setTerminalTitle("Wedone Operate");

    int nombre_epreuves = 0;
    int i = 0;
    int score = 0;
    int pourcentage = 0;

    srand(time(NULL));
    setlocale(LC_CTYPE, "");

    checkForUpdates();

    printf("Bienvenue dans Wedone Operate (version %s) ! Bonne aventure !\n\n", VERSION);
    printf("Combien d'épreuves voulez-vous faire ? ");
    scanf("%d", &nombre_epreuves);

    for (i = 1; i <= nombre_epreuves; i++) {
        int nombre1 = rand() % 100 + 1;
        int nombre2 = rand() % 50 + 1;
        int operation = rand() % 4 + 1;
        int resultat = 0;
        int reponse = 0;

        switch (operation) {
            case 1:
                resultat = nombre1 + nombre2;
                printf("Épreuve %d : %d + %d = ?\n", i, nombre1, nombre2);
                break;
            case 2:
                if (nombre1 < nombre2 || nombre1 - nombre2 > 100) {
                    nombre1 = rand() % 100 + 1;
                    nombre2 = rand() % 50 + 1;
                    i--; // Répéter cette épreuve
                    continue;
                }
                resultat = nombre1 - nombre2;
                printf("Épreuve %d : %d - %d = ?\n", i, nombre1, nombre2);
                break;
            case 3:
                nombre1 %= 10;
                nombre2 %= 10;
                resultat = nombre1 * nombre2;
                printf("Épreuve %d : %d * %d = ?\n", i, nombre1, nombre2);
                break;
            case 4:
                if (nombre2 != 0 && nombre1 % nombre2 == 0) {
                    resultat = nombre1 / nombre2;
                    printf("Épreuve %d : %d / %d = ?\n", i, nombre1, nombre2);
                } else {
                    nombre1 = rand() % 10 + 1;
                    nombre2 = rand() % 10 + 1;
                    i--; // Répéter cette épreuve
                    continue;
                }
                break;
        }

        printf("Votre réponse : ");
        scanf("%d", &reponse);

        if (reponse == resultat) {
            score++;
            printf("Bonne réponse !\n");
        } else {
            printf("Mauvaise réponse ! La bonne réponse était %d.\n", resultat);
        }
    }

    pourcentage = score * 100 / nombre_epreuves;
    printf("Vous avez réussi %d épreuves sur %d.\n", score, nombre_epreuves);
    printf("Votre pourcentage de réussite est de %d%%.\n", pourcentage);
    printf("La fenêtre se fermera automatiquement dans 10 secondes.\n");

    Sleep(10000); // Attendre pendant 10 secondes

    return 0;
}
