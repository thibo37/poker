import random
from statistics import *


class Croupier(object):

    # Définition de notre classe Croupier
    """Classe définissant une personne caractérisée par :
    - son nom
    - ses jetons
    - cartes"""
    liste_cartes_tirees = []
    liste_joueur = []
    petite_blinde = 10
    grande_blinde = 20

    # Liste des mots du pendu
    LISTE_CARTES = ["Pas de carte attribuée",
                    "As de carreau",
                    "Deux de carreau",
                    "Trois de carreau",
                    "Quatre de carreau",
                    "Cinq de carreau",
                    "Six de carreau",
                    "Sept de carreau",
                    "Huit de carreau",
                    "Neuf de carreau",
                    "Dix de carreau",
                    "Valet de carreau",
                    "Dame de carreau",
                    "Roi de carreau",
                    "As de coeur",
                    "Deux de coeur",
                    "Trois de coeur",
                    "Quatre de coeur",
                    "Cinq de coeur",
                    "Six de coeur",
                    "Sept de coeur",
                    "Huit de coeur",
                    "Neuf de coeur",
                    "Dix de coeur",
                    "Valet de coeur",
                    "Dame de coeur",
                    "Roi de coeur",
                    "As de pique",
                    "Deux de pique",
                    "Trois de pique",
                    "Quatre de pique",
                    "Cinq de pique",
                    "Six de pique",
                    "Sept de pique",
                    "Huit de pique",
                    "Neuf de pique",
                    "Dix de pique",
                    "Valet de pique",
                    "Dame de pique",
                    "Roi de pique",
                    "As de trefle",
                    "Deux de trefle",
                    "Trois de trefle",
                    "Quatre de trefle",
                    "Cinq de trefle",
                    "Six de trefle",
                    "Sept de trefle",
                    "Huit de trefle",
                    "Neuf de trefle",
                    "Dix de trefle",
                    "Valet de trefle",
                    "Dame de trefle",
                    "Roi de trefle"]
    
    def __init__(self):
        """Constructeur de notre classe"""
        self.jetons = 0
        self.carte_flop_1 = 0
        self.carte_flop_2 = 0
        self.carte_flop_3 = 0
        self.carte_turn = 0
        self.carte_river = 0
        self.donneur = 0

    def mise(self, joueur, montant, tour):
        if joueur.jetons > montant:
            joueur.jetons = joueur.jetons - montant
            self.jetons = self.jetons + montant
            joueur.mise_au_tour(montant, tour)

    def distribution_cartes(self):
        # Distribution des cartes aux joueurs
        self.donneur = (self.donneur + 1) % self.nombre_joueur_partie()
        print('Les cartes sont distribuées')
        for ii in self.liste_joueur:
            carte = self.tirage_une_carte()
            ii.carte_1 = carte
            self.liste_cartes_tirees.append(carte)

            carte = self.tirage_une_carte()
            ii.carte_2 = carte
            self.liste_cartes_tirees.append(carte)

    def condition_passage_tour(self, tour):
        #  Retourne 1 si il faut continuer le tour et 0 si le tour est fini
        etat_des_mises = []
        kk = 0
        for joueur in self.liste_joueur:
            if joueur.couche == 0:
                kk = kk + 1
                etat_des_mises.append(joueur.a_mise_au_tour(tour))
        if pstdev(etat_des_mises) > 0:
            return 1
        elif kk < 2:
            return 0
        else:
            return 0

    def joueur_parle(self, joueur, tour):
        if joueur.couche == 1:
            print(joueur.prenom + ' s\'est couché.')
        else:
            print(' Au tour de ' + joueur.prenom)
            print('Voici la liste des mises pour ce tour :')
            for parleur in self.liste_joueur:
                print(parleur.prenom + ' a misé ' + str(parleur.a_mise_au_tour(tour)))
                
            montant_mise = input_number('Mise :')
            if montant_mise < 0:
                joueur.se_couche()
            elif self.verif_mise_suffisante(joueur, tour, montant_mise):
                self.mise(joueur, montant_mise, tour)
            else:
                print("La mise n''est pas suffisante. Pour se coucher entrer -1")
                self.joueur_parle(joueur, tour)

    def verif_mise_suffisante(self, joueur, tour, mise):
        kk = 1
        for parleur in self.liste_joueur:
            if parleur.a_mise_au_tour(tour) > mise + joueur.a_mise_au_tour(tour):
                kk = 0
        return kk

    def nouvelle_donne(self):
        print("*****     Nouvelle donne !!     *****")
        self.affiche_jetons()
        self.donneur = (self.donneur + 1) % self.nombre_joueur_partie()
        self.distribution_cartes()
        self.montre_ses_cartes(self.liste_joueur[0])
        self.tour_enchere('preflop')
        self.montre_ses_cartes(self.liste_joueur[0])
        if self.reste_au_moins_deux_joueurs_tour():
            self.tirage_flop()
            self.tour_enchere('flop')
            if self.reste_au_moins_deux_joueurs_tour():
                self.tirage_turn()
                self.tour_enchere('turn')
                if self.reste_au_moins_deux_joueurs_tour():
                        self.tirage_river()
                        self.tour_enchere('river')
                        if self.reste_au_moins_deux_joueurs_tour():
                            gagnant = self.determine_gagnant()
                            self.remporte_le_pot(gagnant)
        self.reinitialise_donne()
        print('*****     Nouvelle donne     *****')

    def reinitialise_donne(self):
        for joueur in self.liste_joueur:
            joueur.reinitialise_donne_joueur()
        self.nouvelle_donne()

    def affiche_jetons(self):
        for joueur in self.liste_joueur:
            print(joueur.prenom + " a " + str(joueur.jetons) + " jetons")

    def determine_gagnant(self):
        print("Celui ci a gagné : ")
        print(self.liste_joueur[0].prenom)
        return self.liste_joueur[0]

    def reste_au_moins_deux_joueurs_tour(self):
        nbre_survivant = 0
        for joueur in self.liste_joueur:
            if joueur.couche == 0:
                nbre_survivant = nbre_survivant + 1
                gagnant = joueur
        if nbre_survivant < 2:
            self.remporte_le_pot(gagnant)
            return 0
        else:
            return 1

    def nombre_joueur_partie(self):
        nbre_survivant = 0
        for joueur in self.liste_joueur:
            if joueur.jetons > 0:
                nbre_survivant = nbre_survivant+1
        return nbre_survivant

    def reste_au_moins_deux_joueurs_partie(self):
        nbre_survivant = 0
        for joueur in self.liste_joueur:
            if joueur.jetons > 0:
                nbre_survivant = nbre_survivant + 1
                gagnant = joueur
        if nbre_survivant < 2:
            self.remporte_la_partie(gagnant)
        else:
            return True

    def remporte_la_partie(self, joueur):
        print(joueur.prenom + " a gagne la partie ! Bien joue !")
        pass

    def remporte_le_pot(self, joueur):
        joueur.jetons = joueur.jetons + self.jetons
        self.fin_tour()
        print(joueur.prenom + " a gagné " + str(self.jetons) + "jetons")
        self.fin_tour()

    def fin_tour(self):
        self.jetons = 0
        self.RAZ_cartes()
        if self.reste_au_moins_deux_joueurs_partie():
            self.reinitialise_donne()

    def RAZ_cartes(self):
        self.jetons = 0
        self.carte_flop_1 = 0
        self.carte_flop_2 = 0
        self.carte_flop_3 = 0
        self.carte_turn = 0
        self.carte_river = 0
        for joueur in self.liste_joueur:
            joueur.carte_1 = 0
            joueur.carte_2 = 0
        self.liste_cartes_tirees = []

    def tour_enchere(self, tour):
        if tour == 'preflop':
        # Petite et grande blinde
            self.mise(self.liste_joueur[(self.donneur+1) % len(self.liste_joueur)], self.petite_blinde, 'preflop')
            self.mise(self.liste_joueur[(self.donneur+2) % len(self.liste_joueur)], self.grande_blinde, 'preflop')

        # Premiere phase : on permet aux joueurs de s'exprimer une fois
            for jj in range(len(self.liste_joueur)):
                if self.reste_au_moins_deux_joueurs_tour():
                    joueur_qui_parle = (self.donneur+3+jj) % len(self.liste_joueur)
                    self.joueur_parle(self.liste_joueur[joueur_qui_parle], tour)

        # Deuxième phase : on tourne jusqu'à tant que tout le monde soit aligné
            kk = 1
            while self.condition_passage_tour(tour):
                if self.reste_au_moins_deux_joueurs_tour():
                    self.joueur_parle(self.liste_joueur[joueur_qui_parle], tour)
                    joueur_qui_parle = (self.donneur + 2 + kk) % len(self.liste_joueur)
                    kk = kk+1
                else:
                    break
        else:
            # Premiere phase : on permet aux joueurs de s'exprimer une fois
            for jj in range(len(self.liste_joueur)):
                if self.reste_au_moins_deux_joueurs_tour():
                    joueur_qui_parle = (self.donneur + 1 + jj) % len(self.liste_joueur)
                    self.joueur_parle(self.liste_joueur[joueur_qui_parle], tour)

            # Deuxième phase : on tourne jusqu'à tant que tout le monde soit aligné
            kk = 1
            while self.condition_passage_tour(tour):
                if self.reste_au_moins_deux_joueurs_tour():
                    self.joueur_parle(self.liste_joueur[joueur_qui_parle], tour)
                    joueur_qui_parle = (self.donneur + 2 + kk) % len(self.liste_joueur)
                    kk = kk + 1
                else:
                    break

        print('Fin du tour d\'enchère ' + tour + '. Il y a ' + str(self.jetons) + ' jetons dans le pot')

    def tirage_une_carte(self):
        carte = random.randint(1, 52)
        while carte in self.liste_cartes_tirees:
            carte = random.randint(1, 52)
        return carte

    def tirage_flop(self):
        print('Tirage du Flop')
        
        carte = self.tirage_une_carte()

        self.carte_flop_1 = carte
        self.liste_cartes_tirees.append(carte)
            
        carte = self.tirage_une_carte()

        self.carte_flop_2 = carte
        self.liste_cartes_tirees.append(carte)

        carte = self.tirage_une_carte()

        self.carte_flop_3 = carte
        self.liste_cartes_tirees.append(carte)

        print('**************      ' + self.LISTE_CARTES[self.carte_flop_1])
        print('**************      ' + self.LISTE_CARTES[self.carte_flop_2])
        print('**************      ' + self.LISTE_CARTES[self.carte_flop_3])

    def tirage_turn(self):
        print('Tirage de la turn')
        carte = self.tirage_une_carte()

        self.carte_turn = carte
        self.liste_cartes_tirees.append(carte)

        print('**************      ' + self.LISTE_CARTES[self.carte_flop_1])
        print('**************      ' + self.LISTE_CARTES[self.carte_flop_2])
        print('**************      ' + self.LISTE_CARTES[self.carte_flop_3])
        print('**************      ' + self.LISTE_CARTES[self.carte_turn])

    def tirage_river(self):
        print('Tirage de la river')
        carte = self.tirage_une_carte()

        self.carte_river = carte
        self.liste_cartes_tirees.append(carte)

        print('**************      ' + self.LISTE_CARTES[self.carte_flop_1])
        print('**************      ' + self.LISTE_CARTES[self.carte_flop_2])
        print('**************      ' + self.LISTE_CARTES[self.carte_flop_3])
        print('**************      ' + self.LISTE_CARTES[self.carte_turn])
        print('**************      ' + self.LISTE_CARTES[self.carte_river])

    def montre_ses_cartes(self, joueur):
        print('**************      **********')
        print(' Cartes de ' + joueur.prenom+ ' :')
        print('**************      ' + self.LISTE_CARTES[joueur.carte_1])
        print('**************      ' + self.LISTE_CARTES[joueur.carte_2])
        print('**************      **********')
        
def input_number(message):
    kk = 1
    while kk:
        try:
            user_input = int(input(message))
        except ValueError:
            print("Not an integer! Try again.")
        else:
            kk = 0
            return user_input
