"""Ce fichier contient le jeu du pendu.

Il s'appuie sur les fichiers :
- donnees.py
- fonctions.py"""

from poker import joueur
from poker import croupier

# Initialisation
croupier = croupier.Croupier() 	# Initialisation du pot

Thibaut = joueur.Joueur('Thibaut')
croupier.liste_joueur.append(Thibaut)

Negreanu = joueur.Joueur('Negreanu')
croupier.liste_joueur.append(Negreanu)

Helmut = joueur.Joueur('Helmut')
croupier.liste_joueur.append(Helmut)

croupier.nouvelle_donne()
