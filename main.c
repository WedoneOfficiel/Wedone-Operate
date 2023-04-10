#include <stdio.h>

int boucle_infinie = 0;

int main(void)
{
	int epreuve_choisi = 0;
	int nombre_epreuves_jouees = 0;
	int nombre_epreuves_gagnees = 0;
	int pourcentage_reussite = 0;

	printf("Bienvenue dans Wedone Operate (stable 1.7) ! Bonne aventure !\nPour quitter, tape 999 apres que l'on t'ai demande a quel epreuve tu voulais jouer.\n");
	
	while(boucle_infinie = 200)
	{
		int epreuve_choisi = 0;
		int valeur_epreuve = 0;
		int nombre_utilisateur_epreuve = 0;
		int valeur_hypothese_utilisateur_epreuve = 0;
		
		printf("Entre le numero de l'epreuve a laquelle tu veux jouer : ");
		scanf("%d", &epreuve_choisi);

		
		if(epreuve_choisi == 1)
		{
			nombre_epreuves_jouees = nombre_epreuves_jouees + 1;
			valeur_epreuve = 10;
			nombre_utilisateur_epreuve = 0;
			valeur_hypothese_utilisateur_epreuve = 0;

			printf("Epreuve %d |\nIndiquez un chiffre : ", epreuve_choisi);

			scanf("%d", &nombre_utilisateur_epreuve);

			printf("A partir du resultat suivant : %d, indiquez quel nombre a ete ajoute : \n", nombre_utilisateur_epreuve + valeur_epreuve);

			scanf("%d", &valeur_hypothese_utilisateur_epreuve);
			
			if(valeur_hypothese_utilisateur_epreuve == valeur_epreuve)
			{
				nombre_epreuves_gagnees = nombre_epreuves_gagnees + 1;
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Bonne reponse !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);

			}
			else
			{
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Mauvaise reponse, la bonne reponse etait %d !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", valeur_epreuve, nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);
			}
		}
		else if(epreuve_choisi == 2)
		{
			nombre_epreuves_jouees = nombre_epreuves_jouees + 1;
			valeur_epreuve = 7;
			nombre_utilisateur_epreuve = 0;
			valeur_hypothese_utilisateur_epreuve = 0;

			printf("Epreuve %d |\nIndiquez un chiffre : ", epreuve_choisi);
	
			scanf("%d", &nombre_utilisateur_epreuve);

			printf("A partir du resultat suivant : %d, indiquez quel nombre a ete enleve : \n", nombre_utilisateur_epreuve - valeur_epreuve);

			scanf("%d", &valeur_hypothese_utilisateur_epreuve);

			if(valeur_hypothese_utilisateur_epreuve == valeur_epreuve)
			{
				nombre_epreuves_gagnees = nombre_epreuves_gagnees + 1;
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Bonne reponse !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);

			}
			else
			{
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Mauvaise reponse, la bonne reponse etait %d !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", valeur_epreuve, nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);
			}
		}
		else if(epreuve_choisi == 3)
		{
			nombre_epreuves_jouees = nombre_epreuves_jouees + 1;
			valeur_epreuve = 51;
			nombre_utilisateur_epreuve = 0;
			valeur_hypothese_utilisateur_epreuve = 0;

			printf("Epreuve %d |\nIndiquez un chiffre : ", epreuve_choisi);
	
			scanf("%d", &nombre_utilisateur_epreuve);

			printf("A partir du resultat suivant : %d, indiquez quel nombre a ete enleve : \n", nombre_utilisateur_epreuve - valeur_epreuve);

			scanf("%d", &valeur_hypothese_utilisateur_epreuve);

			if(valeur_hypothese_utilisateur_epreuve == valeur_epreuve)
			{
				nombre_epreuves_gagnees = nombre_epreuves_gagnees + 1;
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Bonne reponse !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);

			}
			else
			{
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Mauvaise reponse, la bonne reponse etait %d !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", valeur_epreuve, nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);
			}
		}
		else if(epreuve_choisi == 4)
		{
			nombre_epreuves_jouees = nombre_epreuves_jouees + 1;
			valeur_epreuve = 3;
			nombre_utilisateur_epreuve = 0;
			valeur_hypothese_utilisateur_epreuve = 0;

			printf("Epreuve %d |\nIndiquez un chiffre : ", epreuve_choisi);

			scanf("%d", &nombre_utilisateur_epreuve);

			printf("A partir du resultat suivant : %d, indiquez quel nombre a ete ajoute : \n", nombre_utilisateur_epreuve + valeur_epreuve);

			scanf("%d", &valeur_hypothese_utilisateur_epreuve);

			if(valeur_hypothese_utilisateur_epreuve == valeur_epreuve)
			{
				nombre_epreuves_gagnees = nombre_epreuves_gagnees + 1;
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Bonne reponse !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);

			}
			else
			{
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Mauvaise reponse, la bonne reponse etait %d !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", valeur_epreuve, nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);
			}
		}
		else if(epreuve_choisi == 5)
		{
			nombre_epreuves_jouees = nombre_epreuves_jouees + 1;
			valeur_epreuve = 2;
			nombre_utilisateur_epreuve = 0;
			valeur_hypothese_utilisateur_epreuve = 0;

			printf("Epreuve %d |\nIndiquez un chiffre PAIR : ", epreuve_choisi);

			scanf("%d", &nombre_utilisateur_epreuve);

			printf("A partir du resultat suivant : %d, indiquez par quel nombre votre chiffre a ete divise : \n", nombre_utilisateur_epreuve / valeur_epreuve);

			scanf("%d", &valeur_hypothese_utilisateur_epreuve);

			if(valeur_hypothese_utilisateur_epreuve == valeur_epreuve)
			{
				nombre_epreuves_gagnees = nombre_epreuves_gagnees + 1;
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Bonne reponse !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);

			}
			else
			{
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Mauvaise reponse, la bonne reponse etait %d !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", valeur_epreuve, nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);
			}
		}

		else if(epreuve_choisi == 6)
		{
			nombre_epreuves_jouees = nombre_epreuves_jouees + 1;
			valeur_epreuve = 3;
			nombre_utilisateur_epreuve = 0;
			valeur_hypothese_utilisateur_epreuve = 0;

			printf("Epreuve %d |\nIndiquez un chiffre : ", epreuve_choisi);

			scanf("%d", &nombre_utilisateur_epreuve);

			printf("A partir du resultat suivant : %d, indiquez par quel nombre votre chiffre a ete multiplie : \n", nombre_utilisateur_epreuve * valeur_epreuve);

			scanf("%d", &valeur_hypothese_utilisateur_epreuve);

			if(valeur_hypothese_utilisateur_epreuve == valeur_epreuve)
			{
				nombre_epreuves_gagnees = nombre_epreuves_gagnees + 1;
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Bonne reponse !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);

			}
			else
			{
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Mauvaise reponse, la bonne reponse etait %d !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", valeur_epreuve, nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);
			}
		}

		else if(epreuve_choisi == 7)
		{
			nombre_epreuves_jouees = nombre_epreuves_jouees + 1;
			valeur_epreuve = 5;
			nombre_utilisateur_epreuve = 0;
			valeur_hypothese_utilisateur_epreuve = 0;

			printf("Epreuve %d |\nIndiquez un chiffre : ", epreuve_choisi);

			scanf("%d", &nombre_utilisateur_epreuve);

			printf("A partir du resultat suivant : %d, indiquez quel nombre a ete enleve : \n", nombre_utilisateur_epreuve - valeur_epreuve);

			scanf("%d", &valeur_hypothese_utilisateur_epreuve);

			if(valeur_hypothese_utilisateur_epreuve == valeur_epreuve)
			{
				nombre_epreuves_gagnees = nombre_epreuves_gagnees + 1;
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Bonne reponse !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);

			}
			else
			{
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Mauvaise reponse, la bonne reponse etait %d !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", valeur_epreuve, nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);
			}
		}

		else if(epreuve_choisi == 8)
		{
			nombre_epreuves_jouees = nombre_epreuves_jouees + 1;
			valeur_epreuve = 5;
			nombre_utilisateur_epreuve = 0;
			valeur_hypothese_utilisateur_epreuve = 0;

			printf("Epreuve %d |\nIndiquez un chiffre : ", epreuve_choisi);

			scanf("%d", &nombre_utilisateur_epreuve);

			printf("A partir du resultat suivant : %d, indiquez par quel nombre votre chiffre a ete divise : \n", nombre_utilisateur_epreuve / valeur_epreuve);

			scanf("%d", &valeur_hypothese_utilisateur_epreuve);

			if(valeur_hypothese_utilisateur_epreuve == valeur_epreuve)
			{
				nombre_epreuves_gagnees = nombre_epreuves_gagnees + 1;
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Bonne reponse !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);

			}
			else
			{
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Mauvaise reponse, la bonne reponse etait %d !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", valeur_epreuve, nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);
			}
		}

		else if(epreuve_choisi == 9)
		{
			nombre_epreuves_jouees = nombre_epreuves_jouees + 1;
			valeur_epreuve = 12;
			nombre_utilisateur_epreuve = 0;
			valeur_hypothese_utilisateur_epreuve = 0;

			printf("Epreuve %d |\nIndiquez un chiffre : ", epreuve_choisi);

			scanf("%d", &nombre_utilisateur_epreuve);

			printf("A partir du resultat suivant : %d, indiquez quel nombre a ete soustrait : \n", nombre_utilisateur_epreuve - valeur_epreuve);

			scanf("%d", &valeur_hypothese_utilisateur_epreuve);
			
			if(valeur_hypothese_utilisateur_epreuve == valeur_epreuve)
			{
				nombre_epreuves_gagnees = nombre_epreuves_gagnees + 1;
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Bonne reponse !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);

			}
			else
			{
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Mauvaise reponse, la bonne reponse etait %d !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", valeur_epreuve, nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);
			}
		}

		else if(epreuve_choisi == 10)
		{
			nombre_epreuves_jouees = nombre_epreuves_jouees + 1;
			valeur_epreuve = 3;
			nombre_utilisateur_epreuve = 0;
			valeur_hypothese_utilisateur_epreuve = 0;

			printf("Epreuve %d |\nIndiquez un chiffre : ", epreuve_choisi);

			scanf("%d", &nombre_utilisateur_epreuve);

			printf("A partir du resultat suivant : %d, indiquez par quel nombre votre chiffre a ete multiplie : \n", nombre_utilisateur_epreuve * valeur_epreuve);

			scanf("%d", &valeur_hypothese_utilisateur_epreuve);
			
			if(valeur_hypothese_utilisateur_epreuve == valeur_epreuve)
			{
				nombre_epreuves_gagnees = nombre_epreuves_gagnees + 1;
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Bonne reponse !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);

			}
			else
			{
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Mauvaise reponse, la bonne reponse etait %d !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", valeur_epreuve, nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);
			}
		}

		else if(epreuve_choisi == 11)
		{
			nombre_epreuves_jouees = nombre_epreuves_jouees + 1;
			valeur_epreuve = 29;
			nombre_utilisateur_epreuve = 0;
			valeur_hypothese_utilisateur_epreuve = 0;

			printf("Epreuve %d |\nIndiquez un chiffre : ", epreuve_choisi);

			scanf("%d", &nombre_utilisateur_epreuve);

			printf("A partir du resultat suivant : %d, indiquez a ete ajoute : \n", nombre_utilisateur_epreuve + valeur_epreuve);

			scanf("%d", &valeur_hypothese_utilisateur_epreuve);
			
			if(valeur_hypothese_utilisateur_epreuve == valeur_epreuve)
			{
				nombre_epreuves_gagnees = nombre_epreuves_gagnees + 1;
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Bonne reponse !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);

			}
			else
			{
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Mauvaise reponse, la bonne reponse etait %d !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", valeur_epreuve, nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);
			}
		}

		else if(epreuve_choisi == 12)
		{
			nombre_epreuves_jouees = nombre_epreuves_jouees + 1;
			valeur_epreuve = 3;
			nombre_utilisateur_epreuve = 0;
			valeur_hypothese_utilisateur_epreuve = 0;

			printf("Epreuve %d |\nIndiquez un chiffre : ", epreuve_choisi);

			scanf("%d", &nombre_utilisateur_epreuve);

			printf("A partir du resultat suivant : %d, indiquez a ete ajoute : \n", nombre_utilisateur_epreuve + valeur_epreuve);

			scanf("%d", &valeur_hypothese_utilisateur_epreuve);
			
			if(valeur_hypothese_utilisateur_epreuve == valeur_epreuve)
			{
				nombre_epreuves_gagnees = nombre_epreuves_gagnees + 1;
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Bonne reponse !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);

			}
			else
			{
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Mauvaise reponse, la bonne reponse etait %d !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", valeur_epreuve, nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);
			}
		}

		else if(epreuve_choisi == 13)
		{
			nombre_epreuves_jouees = nombre_epreuves_jouees + 1;
			valeur_epreuve = 6;
			nombre_utilisateur_epreuve = 0;
			valeur_hypothese_utilisateur_epreuve = 0;

			printf("Epreuve %d |\nIndiquez un chiffre : ", epreuve_choisi);

			scanf("%d", &nombre_utilisateur_epreuve);

			printf("A partir du resultat suivant : %d, indiquez par quel nombre votre chiffre a ete divise : \n", nombre_utilisateur_epreuve / valeur_epreuve);

			scanf("%d", &valeur_hypothese_utilisateur_epreuve);

			if(valeur_hypothese_utilisateur_epreuve == valeur_epreuve)
			{
				nombre_epreuves_gagnees = nombre_epreuves_gagnees + 1;
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Bonne reponse !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);

			}
			else
			{
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Mauvaise reponse, la bonne reponse etait %d !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", valeur_epreuve, nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);
			}
		}

		else if(epreuve_choisi == 14)
		{
			nombre_epreuves_jouees = nombre_epreuves_jouees + 1;
			valeur_epreuve = 3;
			nombre_utilisateur_epreuve = 0;
			valeur_hypothese_utilisateur_epreuve = 0;

			printf("Epreuve %d |\nIndiquez un chiffre : ", epreuve_choisi);

			scanf("%d", &nombre_utilisateur_epreuve);

			printf("A partir du resultat suivant : %d, indiquez par quel nombre votre chiffre a ete multiplie : \n", nombre_utilisateur_epreuve * valeur_epreuve);

			scanf("%d", &valeur_hypothese_utilisateur_epreuve);
			
			if(valeur_hypothese_utilisateur_epreuve == valeur_epreuve)
			{
				nombre_epreuves_gagnees = nombre_epreuves_gagnees + 1;
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Bonne reponse !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);

			}
			else
			{
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Mauvaise reponse, la bonne reponse etait %d !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", valeur_epreuve, nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);
			}
		}


		else if(epreuve_choisi == 15)
		{
			nombre_epreuves_jouees = nombre_epreuves_jouees + 1;
			valeur_epreuve = 6;
			nombre_utilisateur_epreuve = 0;
			valeur_hypothese_utilisateur_epreuve = 0;

			printf("Epreuve %d |\nIndiquez un chiffre : ", epreuve_choisi);

			scanf("%d", &nombre_utilisateur_epreuve);

			printf("A partir du resultat suivant : %d, indiquez par quel nombre votre chiffre a ete multiplie : \n", nombre_utilisateur_epreuve * valeur_epreuve);

			scanf("%d", &valeur_hypothese_utilisateur_epreuve);
			
			if(valeur_hypothese_utilisateur_epreuve == valeur_epreuve)
			{
				nombre_epreuves_gagnees = nombre_epreuves_gagnees + 1;
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Bonne reponse !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);

			}
			else
			{
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Mauvaise reponse, la bonne reponse etait %d !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", valeur_epreuve, nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);
			}
		}

		else if(epreuve_choisi == 16)
		{
			nombre_epreuves_jouees = nombre_epreuves_jouees + 1;
			valeur_epreuve = 25;
			nombre_utilisateur_epreuve = 0;
			valeur_hypothese_utilisateur_epreuve = 0;

			printf("Epreuve %d |\nIndiquez un chiffre : ", epreuve_choisi);

			scanf("%d", &nombre_utilisateur_epreuve);

			printf("A partir du resultat suivant : %d, indiquez a ete ajoute : \n", nombre_utilisateur_epreuve + valeur_epreuve);

			scanf("%d", &valeur_hypothese_utilisateur_epreuve);
			
			if(valeur_hypothese_utilisateur_epreuve == valeur_epreuve)
			{
				nombre_epreuves_gagnees = nombre_epreuves_gagnees + 1;
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Bonne reponse !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);

			}
			else
			{
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Mauvaise reponse, la bonne reponse etait %d !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", valeur_epreuve, nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);
			}
		}

		else if(epreuve_choisi == 17)
		{
			nombre_epreuves_jouees = nombre_epreuves_jouees + 1;
			valeur_epreuve = 9;
			nombre_utilisateur_epreuve = 0;
			valeur_hypothese_utilisateur_epreuve = 0;

			printf("Epreuve %d |\nIndiquez un chiffre : ", epreuve_choisi);

			scanf("%d", &nombre_utilisateur_epreuve);

			printf("A partir du resultat suivant : %d, indiquez quel nombre a ete soustrait : \n", nombre_utilisateur_epreuve - valeur_epreuve);

			scanf("%d", &valeur_hypothese_utilisateur_epreuve);
			
			if(valeur_hypothese_utilisateur_epreuve == valeur_epreuve)
			{
				nombre_epreuves_gagnees = nombre_epreuves_gagnees + 1;
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Bonne reponse !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);

			}
			else
			{
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Mauvaise reponse, la bonne reponse etait %d !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", valeur_epreuve, nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);
			}
		}

		else if(epreuve_choisi == 18)
		{
			nombre_epreuves_jouees = nombre_epreuves_jouees + 1;
			valeur_epreuve = 12;
			nombre_utilisateur_epreuve = 0;
			valeur_hypothese_utilisateur_epreuve = 0;

			printf("Epreuve %d |\nIndiquez un chiffre : ", epreuve_choisi);

			scanf("%d", &nombre_utilisateur_epreuve);

			printf("A partir du resultat suivant : %d, indiquez quel nombre a ete soustrait : \n", nombre_utilisateur_epreuve - valeur_epreuve);

			scanf("%d", &valeur_hypothese_utilisateur_epreuve);
			
			if(valeur_hypothese_utilisateur_epreuve == valeur_epreuve)
			{
				nombre_epreuves_gagnees = nombre_epreuves_gagnees + 1;
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Bonne reponse !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);

			}
			else
			{
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Mauvaise reponse, la bonne reponse etait %d !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", valeur_epreuve, nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);
			}
		}

		else if(epreuve_choisi == 19)
		{
			nombre_epreuves_jouees = nombre_epreuves_jouees + 1;
			valeur_epreuve = 5;
			nombre_utilisateur_epreuve = 0;
			valeur_hypothese_utilisateur_epreuve = 0;

			printf("Epreuve %d |\nIndiquez un chiffre : ", epreuve_choisi);

			scanf("%d", &nombre_utilisateur_epreuve);

			printf("A partir du resultat suivant : %d, indiquez par quel nombre votre chiffre a ete divise : \n", nombre_utilisateur_epreuve / valeur_epreuve);

			scanf("%d", &valeur_hypothese_utilisateur_epreuve);

			if(valeur_hypothese_utilisateur_epreuve == valeur_epreuve)
			{
				nombre_epreuves_gagnees = nombre_epreuves_gagnees + 1;
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Bonne reponse !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);

			}
			else
			{
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Mauvaise reponse, la bonne reponse etait %d !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", valeur_epreuve, nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);
			}
		}

		else if(epreuve_choisi == 20)
		{
			nombre_epreuves_jouees = nombre_epreuves_jouees + 1;
			valeur_epreuve = 4;
			nombre_utilisateur_epreuve = 0;
			valeur_hypothese_utilisateur_epreuve = 0;

			printf("Epreuve %d |\nIndiquez un chiffre : ", epreuve_choisi);

			scanf("%d", &nombre_utilisateur_epreuve);

			printf("A partir du resultat suivant : %d, indiquez par quel nombre votre chiffre a ete multiplie : \n", nombre_utilisateur_epreuve * valeur_epreuve);

			scanf("%d", &valeur_hypothese_utilisateur_epreuve);
			
			if(valeur_hypothese_utilisateur_epreuve == valeur_epreuve)
			{
				nombre_epreuves_gagnees = nombre_epreuves_gagnees + 1;
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Bonne reponse !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);

			}
			else
			{
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Mauvaise reponse, la bonne reponse etait %d !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", valeur_epreuve, nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);
			}
		}

		else if(epreuve_choisi == 21)
		{
			nombre_epreuves_jouees = nombre_epreuves_jouees + 1;
			valeur_epreuve = 7;
			nombre_utilisateur_epreuve = 0;
			valeur_hypothese_utilisateur_epreuve = 0;

			printf("Epreuve %d |\nIndiquez un chiffre : ", epreuve_choisi);

			scanf("%d", &nombre_utilisateur_epreuve);

			printf("A partir du resultat suivant : %d, indiquez par quel nombre votre chiffre a ete multiplie : \n", nombre_utilisateur_epreuve * valeur_epreuve);

			scanf("%d", &valeur_hypothese_utilisateur_epreuve);
			
			if(valeur_hypothese_utilisateur_epreuve == valeur_epreuve)
			{
				nombre_epreuves_gagnees = nombre_epreuves_gagnees + 1;
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Bonne reponse !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);

			}
			else
			{
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Mauvaise reponse, la bonne reponse etait %d !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", valeur_epreuve, nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);
			}
		}

		else if(epreuve_choisi == 22)
		{
			nombre_epreuves_jouees = nombre_epreuves_jouees + 1;
			valeur_epreuve = 19;
			nombre_utilisateur_epreuve = 0;
			valeur_hypothese_utilisateur_epreuve = 0;

			printf("Epreuve %d |\nIndiquez un chiffre : ", epreuve_choisi);

			scanf("%d", &nombre_utilisateur_epreuve);

			printf("A partir du resultat suivant : %d, indiquez a ete ajoute : \n", nombre_utilisateur_epreuve + valeur_epreuve);

			scanf("%d", &valeur_hypothese_utilisateur_epreuve);
			
			if(valeur_hypothese_utilisateur_epreuve == valeur_epreuve)
			{
				nombre_epreuves_gagnees = nombre_epreuves_gagnees + 1;
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Bonne reponse !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);

			}
			else
			{
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Mauvaise reponse, la bonne reponse etait %d !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", valeur_epreuve, nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);
			}
		}

		else if(epreuve_choisi == 23)
		{
			nombre_epreuves_jouees = nombre_epreuves_jouees + 1;
			valeur_epreuve = 3;
			nombre_utilisateur_epreuve = 0;
			valeur_hypothese_utilisateur_epreuve = 0;

			printf("Epreuve %d |\nIndiquez un chiffre : ", epreuve_choisi);

			scanf("%d", &nombre_utilisateur_epreuve);

			printf("A partir du resultat suivant : %d, indiquez quel nombre a ete soustrait : \n", nombre_utilisateur_epreuve - valeur_epreuve);

			scanf("%d", &valeur_hypothese_utilisateur_epreuve);
			
			if(valeur_hypothese_utilisateur_epreuve == valeur_epreuve)
			{
				nombre_epreuves_gagnees = nombre_epreuves_gagnees + 1;
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Bonne reponse !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);

			}
			else
			{
				pourcentage_reussite = (nombre_epreuves_gagnees * 100) / nombre_epreuves_jouees;
				printf("Mauvaise reponse, la bonne reponse etait %d !\nTon score : %d / %d\nTon pourcentage de reussite est de %d\n", valeur_epreuve, nombre_epreuves_gagnees, nombre_epreuves_jouees, pourcentage_reussite);
			}
		}

		else if(epreuve_choisi == 999)
		{
			break;
		}

		if (epreuve_choisi > 23 && epreuve_choisi != 999 || epreuve_choisi == 0) { 
    		printf("Ce niveau n'existe pas !\n"); 
		}

	}

	return 0;
}