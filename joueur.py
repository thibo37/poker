class Joueur:

    # Définition de notre classe Joueur
    """Classe définissant une personne caractérisée par :
    - son nom
    - ses jetons"""
    
    def __init__(self, prenom):

        """Constructeur de notre classe"""

        self.prenom = prenom
        self.jetons = 1000
        self.carte_1 = 0
        self.carte_2 = 0
        self.mise_preflop = 0
        self.mise_flop = 0
        self.mise_turn = 0
        self.mise_river = 0
        self.couche = 0

    def mise_au_tour(self, mise, tour):
        if tour == 'preflop':
            self.mise_preflop = self.mise_preflop + mise
        if tour == 'flop':
            self.mise_flop = self.mise_flop + mise
        if tour == 'turn':
            self.mise_turn = self.mise_turn + mise
        if tour == 'river':
            self.mise_river = self.mise_river + mise

    def a_mise_au_tour(self, tour):
        if tour == 'preflop':
            return self.mise_preflop
        if tour == 'flop':
            return self.mise_flop
        if tour == 'turn':
            return self.mise_turn
        if tour == 'river':
            return self.mise_river

    def se_couche(self):
        self.couche = 1

    def reinitialise_donne_joueur(self):
        self.couche = 0
        self.mise_preflop = 0
        self.mise_flop = 0
        self.mise_turn = 0
        self.mise_river = 0