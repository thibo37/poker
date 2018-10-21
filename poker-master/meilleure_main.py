import numpy as np
from jeu_de_cartes import *

def determine_main(joueur, croupier):
    cartes = [joueur.carte_1, joueur.carte_2, croupier.carte_flop_1,
              croupier.carte_flop_2, croupier.carte_flop_3, croupier.carte_river, croupier.carte_turn]
    aa = [liste_cartes[x] for x in cartes ]
    print(aa)



    hauteur_cartes = [x % 13 for x in cartes]
    couleur_cartes = [y % 4 for y in cartes]

    # DETECTION SUITE
    diff_sans_doublon = np.diff(list(set(hauteur_cartes)))
    if str([1, 1, 1, 1])[1:-1] in str([diff_sans_doublon]):
        print('Suite')

    # DETECTION COULEUR

    compte_couleur = {k: hauteur_cartes.count(k) for k in set(couleur_cartes)}
    max_cartes_dune_couleur = np.array(list(compte_couleur.values())).max()
    if max_cartes_dune_couleur > 4:
        print('Suite')

    # DETECTION CARTES DOUBLES, TRIPLES OU CARRES
    compte_hauteur = {k: hauteur_cartes.count(k) for k in set(hauteur_cartes)}
    vecteur_cartes_pareilles = np.array(list(compte_hauteur.values()))
    vecteur_cartes_pareilles.sort()

    if vecteur_cartes_pareilles.max() == 4:
        print('carré')
    elif vecteur_cartes_pareilles.max() == 3:
        vecteur_cartes_pareilles.pop()
        if vecteur_cartes_pareilles.max() >1:
            print('Full')
        else:
            print('Brelan')
    elif vecteur_cartes_pareilles.max() == 2:
        print('Simple paire')
    elif vecteur_cartes_pareilles.max() == 1:
        print('Voir si il n''ya ni couleur ni suite')
    else:
        print('Ca ne devrait pas arriver, c''est un bug de codage')

    print('f')

    return cartes
