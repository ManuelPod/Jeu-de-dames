# Auteurs: À compléter

from Partie1.damier import Damier
from Partie1.position import Position
from builtins import input


class Partie:
    """Gestionnaire de partie de dames.

    Attributes:
        damier (Damier): Le damier de la partie, contenant notamment les pièces.
        couleur_joueur_courant (str): Le joueur à qui c'est le tour de jouer.
        doit_prendre (bool): Un booléen représentant si le joueur actif doit absolument effectuer une prise
            de pièce. Sera utile pour valider les mouvements et pour gérer les prises multiples.
        position_source_selectionnee (Position): La position source qui a été sélectionnée. Utile pour sauvegarder
            cette information avant de poursuivre. Contient None si aucune pièce n'est sélectionnée.
        position_source_forcee (Position): Une position avec laquelle le joueur actif doit absolument jouer. Le
            seul moment où cette position est utilisée est après une prise: si le joueur peut encore prendre
            d'autres pièces adverses, il doit absolument le faire. Ce membre contient None si aucune position n'est
            forcée.

    """

    def __init__(self):
        """Constructeur de la classe Partie. Initialise les attributs à leur valeur par défaut. Le damier est construit
        avec les pièces à leur valeur initiales, le joueur actif est le joueur blanc, et celui-ci n'est pas forcé
        de prendre une pièce adverse. Aucune position source n'est sélectionnée, et aucune position source n'est forcée.

        """
        self.damier = Damier()
        self.couleur_joueur_courant = "blanc"
        self.doit_prendre = False
        self.position_source_selectionnee = None
        self.position_source_forcee = None

    def position_source_valide(self, position_source):
        """Vérifie la validité de la position source, notamment:
            - Est-ce que la position contient une pièce?
            - Est-ce que cette pièce est de la couleur du joueur actif?
            - Si le joueur doit absolument continuer son mouvement avec une prise supplémentaire, a-t-il choisi la
              bonne pièce?

        Cette méthode retourne deux valeurs. La première valeur est Booléenne (True ou False), et la seconde valeur est
        un message d'erreur indiquant la raison pourquoi la position n'est pas valide (ou une chaîne vide s'il n'y a pas
        d'erreur).

        ATTENTION: Utilisez les attributs de la classe pour connaître les informations sur le jeu! (le damier, le joueur
            actif, si une position source est forcée, etc.

        ATTENTION: Vous avez accès ici à un attribut de type Damier. vous avez accès à plusieurs méthodes pratiques
            dans le damier qui vous simplifieront la tâche ici :)

        Args:
            position_source (Position): La position source à valider.

        Returns:
            bool, str: Un couple où le premier élément représente la validité de la position (True ou False), et le
                 deuxième élément est un message d'erreur (ou une chaîne vide s'il n'y a pas d'erreur).

        """
        piece = self.damier.recuperer_piece_a_position(position_source)
        erreur = ''
        position_valide = True
        if not piece:
            erreur = '\nAucune pièce à cette position.'
            position_valide = False
        elif piece.couleur is not self.couleur_joueur_courant:
            erreur = '\nCe n\'est pas votre pièce!'
            position_valide = False
        return position_valide, erreur

    def position_cible_valide(self, position_cible):
        """Vérifie si la position cible est valide (en fonction de la position source sélectionnée). Doit non seulement
        vérifier si le déplacement serait valide (utilisez les méthodes que vous avez programmées dans le Damier!), mais
        également si le joueur a respecté la contrainte de prise obligatoire.

        Returns:
            bool, str: Deux valeurs, la première étant Booléenne et indiquant si la position cible est valide, et la
                seconde valeur est une chaîne de caractères indiquant un message d'erreur (ou une chaîne vide s'il n'y
                a pas d'erreur).

        """
        if (self.damier.piece_peut_se_deplacer_vers(self.position_source_selectionnee, position_cible)
                or self.damier.piece_peut_sauter_vers(self.position_source_selectionnee, position_cible)):
            if (not self.position_source_forcee
                    and self.damier.piece_de_couleur_peut_faire_une_prise(self.couleur_joueur_courant) is False):
                print(self.damier.piece_de_couleur_peut_faire_une_prise(self.couleur_joueur_courant))
                print("1")
                return True, ""
            elif (not self.position_source_forcee
                  and self.damier.piece_de_couleur_peut_faire_une_prise(self.couleur_joueur_courant)):
                print("2")
                if self.damier.piece_peut_sauter_vers(self.position_source_selectionnee, position_cible):
                    print("ok")
                    return True, ""
                else:
                    return False, "\nVous devez faire une prise obligatoire!"
            elif self.position_source_forcee == self.position_source_selectionnee:
                print("4")
                return True, ""
            else:
                print("5")
                return False, "\nVous devez faire une prise obligatoire!"
        else:
            print("6")
            return False, "\nPosition cible invalide."

    def demander_positions_deplacement(self):
        """Demande à l'utilisateur les positions sources et cible, et valide ces positions. Cette méthode doit demander
        les positions à l'utilisateur tant que celles-ci sont invalides.

        Cette méthode ne doit jamais planter, peu importe ce que l'utilisateur entre.

        Returns:
            Position, Position: Un couple de deux positions (source et cible).

        """
        global position_source, position_cible
        positions_valides = False
        while positions_valides is False:
            try:
                ligne_source = int(input("\nligne de la pièce choisie: "))
                colonne_source = int(input("Colonne de la pièce choisie: "))
                ligne_cible = int(input("ligne de la destination choisie: "))
                colonne_cible = int(input("Colonne de la pièce choisie: "))
                position_source = Position(ligne_source, colonne_source)
                position_cible = Position(ligne_cible, colonne_cible)
                self.position_source_selectionnee = position_source
                if (self.position_source_valide(position_source)[0] is True
                        and self.position_cible_valide(position_cible)[0] is True):
                    positions_valides = True
                    return position_source, position_cible
                if self.position_source_valide(position_source)[0] is False:
                    raise TypeError(self.position_source_valide(position_source))
                if self.position_cible_valide(position_cible)[0] is False:
                    raise TypeError(self.position_cible_valide(position_cible))

            except TypeError:
                print(self.position_source_valide(position_source)[1])
                print(self.position_cible_valide(position_cible)[1])

            except ValueError:
                print("Cette coordonnée est invalide")







    def tour(self):
        """Cette méthode effectue le tour d'un joueur, et doit effectuer les actions suivantes:
        - Assigne self.doit_prendre à True si le joueur courant a la possibilité de prendre une pièce adverse.
        - Affiche l'état du jeu
        - Demander les positions source et cible (utilisez self.demander_positions_deplacement!)
        - Effectuer le déplacement (à l'aide de la méthode du damier appropriée)
        - Si une pièce a été prise lors du déplacement, c'est encore au tour du même joueur si celui-ci peut encore
          prendre une pièce adverse en continuant son mouvement. Utilisez les membres self.doit_prendre et
          self.position_source_forcee pour forcer ce prochain tour!
        - Si aucune pièce n'a été prise ou qu'aucun coup supplémentaire peut être fait avec la même pièce, c'est le
          tour du joueur adverse. Mettez à jour les attributs de la classe en conséquence.

        """

        # Détermine si le joueur courant a la possibilité de prendre une pièce adverse.
        if self.damier.piece_de_couleur_peut_faire_une_prise(self.couleur_joueur_courant):
            self.doit_prendre = True

        # Affiche l'état du jeu
        print(self.damier)
        print("")
        print("Tour du joueur", self.couleur_joueur_courant, end=".")
        if self.doit_prendre:
            if self.position_source_forcee is None:
                print(" Doit prendre une pièce.")
            else:
                print(" Doit prendre avec la pièce en position {}.".format(self.position_source_forcee))
        else:
            print("")

        # Demander les positions
        positions = self.demander_positions_deplacement()
        position_source = positions[0]
        position_cible = positions[1]

        # Effectuer le déplacement (à l'aide de la méthode du damier appropriée)
        statut = self.damier.deplacer(position_source, position_cible)

        # Mettre à jour les attributs de la classe
        self.doit_prendre = self.damier.piece_de_couleur_peut_faire_une_prise(self.couleur_joueur_courant)
        if statut == "prise":
            if self.doit_prendre is True:
                self.position_source_forcee = position_cible
            elif self.couleur_joueur_courant == "blanc":
                self.couleur_joueur_courant = "noir"
            else:
                self.couleur_joueur_courant = "blanc"
        elif statut == "ok":
            if self.couleur_joueur_courant == "blanc":
                self.couleur_joueur_courant = "noir"

            else:
                self.couleur_joueur_courant = "blanc"


    def jouer(self):
        """Démarre une partie. Tant que le joueur courant a des déplacements possibles (utilisez les méthodes
        appriopriées!), un nouveau tour est joué.

        Returns:
            str: La couleur du joueur gagnant.
        """

        while self.damier.piece_de_couleur_peut_se_deplacer(self.couleur_joueur_courant) or \
                self.damier.piece_de_couleur_peut_faire_une_prise(self.couleur_joueur_courant):
            self.tour()

        if self.couleur_joueur_courant == "blanc":
            return "noir"
        else:
            return "blanc"
