# Auteurs: À compléter

from Partie1.piece import Piece
from Partie1.position import Position


class Damier:
    """Plateau de jeu d'un jeu de dames. Contient un ensemble de pièces positionnées à une certaine position
    sur le plateau.

    Attributes:
        cases (dict): Dictionnaire dont une clé représente une Position, et une valeur correspond à la Piece
            positionnée à cet endroit sur le plateau. Notez bien qu'une case vide (sans pièce blanche ou noire)
            correspond à l'absence de clé la position de cette case dans le dictionnaire.

        n_lignes (int): Le nombre de lignes du plateau. La valeur est 8 (constante).
        n_colonnes (int): Le nombre de colonnes du plateau. La valeur est 8 (constante).

    """

    def __init__(self):
        """Constructeur du Damier. Initialise un damier initial de 8 lignes par 8 colonnes.

        """
        self.n_lignes = 8
        self.n_colonnes = 8

        self.cases = {
            Position(7, 0): Piece("blanc", "pion"),
            Position(7, 2): Piece("blanc", "pion"),
            Position(7, 4): Piece("blanc", "pion"),
            Position(7, 6): Piece("blanc", "pion"),
            Position(6, 1): Piece("blanc", "pion"),
            Position(6, 3): Piece("blanc", "pion"),
            Position(6, 5): Piece("blanc", "pion"),
            Position(6, 7): Piece("blanc", "pion"),
            Position(5, 0): Piece("blanc", "pion"),
            Position(5, 2): Piece("blanc", "pion"),
            Position(5, 4): Piece("blanc", "pion"),
            Position(5, 6): Piece("blanc", "pion"),
            Position(2, 1): Piece("noir", "pion"),
            Position(2, 3): Piece("noir", "pion"),
            Position(2, 5): Piece("noir", "pion"),
            Position(2, 7): Piece("noir", "pion"),
            Position(1, 0): Piece("noir", "pion"),
            Position(1, 2): Piece("noir", "pion"),
            Position(1, 4): Piece("noir", "pion"),
            Position(1, 6): Piece("noir", "pion"),
            Position(0, 1): Piece("noir", "pion"),
            Position(0, 3): Piece("noir", "pion"),
            Position(0, 5): Piece("noir", "pion"),
            Position(0, 7): Piece("noir", "pion"),
        }

    def recuperer_piece_a_position(self, position):
        """Récupère une pièce dans le damier à partir d'une position.

        Args:
            position (Position): La position où récupérer la pièce.

        Returns:
            La pièce (de type Piece) à la position reçue en argument, ou None si aucune pièce n'était à cette position.

        """
        if position not in self.cases:
            return None

        return self.cases[position]

    def position_est_dans_damier(self, position):
        """Vérifie si les coordonnées d'une position sont dans les bornes du damier (entre 0 inclusivement et le nombre
        de lignes/colonnes, exclusement.

        Args:
            position (Position): La position à valider.

        Returns:
            bool: True si la position est dans les bornes, False autrement.

        """
        return 0 <= position.ligne <= self.n_lignes - 1 and 0 <= position.colonne <= self.n_colonnes - 1

    def piece_peut_se_deplacer_vers(self, position_piece, position_cible):
        """Cette méthode détermine si une pièce (à la position reçue) peut se déplacer à une certaine position cible.
        On parle ici d'un déplacement standard (et non une prise).

        Une pièce doit être positionnée à la position_piece reçue en argument (retourner False autrement).

        Une pièce de type pion ne peut qu'avancer en diagonale (vers le haut pour une pièce blanche, vers le bas pour
        une pièce noire). Une pièce de type dame peut avancer sur n'importe quelle diagonale, peu importe sa couleur.
        Une pièce ne peut pas se déplacer sur une case déjà occupée par une autre pièce. Une pièce ne peut pas se
        déplacer à l'extérieur du damier.

        Args:
            position_piece (Position): La position de la pièce source du déplacement.
            position_cible (Position): La position cible du déplacement.

        Returns:
            bool: True si la pièce peut se déplacer à la position cible, False autrement.

        """
        piece = self.recuperer_piece_a_position(position_piece)
        piece_sur_cible = self.recuperer_piece_a_position(position_cible)

        if not piece or not self.position_est_dans_damier(position_cible) or piece_sur_cible:
            return False
        if piece.est_pion():
            if piece.est_noire():
                return position_cible in position_piece.positions_diagonales_bas()
            else:
                return position_cible in position_piece.positions_diagonales_haut()
        else:
            return position_cible in position_piece.quatre_positions_diagonales()

    def piece_peut_sauter_vers(self, position_piece, position_cible):
        """Cette méthode détermine si une pièce (à la position reçue) peut sauter vers une certaine position cible.
        On parle ici d'un déplacement qui "mange" une pièce adverse.

        Une pièce doit être positionnée à la position_piece reçue en argument (retourner False autrement).

        Une pièce ne peut que sauter de deux cases en diagonale. N'importe quel type de pièce (pion ou dame) peut sauter
        vers l'avant ou vers l'arrière. Une pièce ne peut pas sauter vers une case qui est déjà occupée par une autre
        pièce. Une pièce ne peut faire un saut que si elle saute par dessus une pièce de couleur adverse.

        Args:
            position_piece (Position): La position de la pièce source du saut.
            position_cible (Position): La position cible du saut.

        Returns:
            bool: True si la pièce peut sauter vers la position cible, False autrement.

        """
        global position_a_manger
        piece = self.recuperer_piece_a_position(position_piece)
        piece_sur_cible = self.recuperer_piece_a_position(position_cible)
        if piece and not piece_sur_cible:
            position_a_manger = position_piece.position_a_manger(position_cible)

        if (not piece
                or not self.position_est_dans_damier(position_cible)
                or not self.position_est_dans_damier(position_a_manger)
                or piece_sur_cible
                or position_cible not in position_piece.quatre_positions_sauts()):
            return False

        if position_a_manger:
            piece_a_manger = self.recuperer_piece_a_position(position_a_manger)
            if not piece_a_manger or piece_a_manger.couleur is piece.couleur:
                return False
        return True

    def piece_peut_se_deplacer(self, position_piece):
        """Vérifie si une pièce à une certaine position a la possibilité de se déplacer (sans faire de saut).

        ATTENTION: N'oubliez pas qu'étant donné une position, il existe une méthode dans la classe Position retournant
        les positions des quatre déplacements possibles.

        Args:
            position_piece (Position): La position source.

        Returns:
            bool: True si une pièce est à la position reçue et celle-ci peut se déplacer, False autrement.

        """
        piece = self.recuperer_piece_a_position(position_piece)
        if piece:
            for position in position_piece.quatre_positions_diagonales():
                if self.piece_peut_se_deplacer_vers(position_piece, position):
                    return True
        return False

    def piece_peut_faire_une_prise(self, position_piece):
        """Vérifie si une pièce à une certaine position a la possibilité de faire une prise.

        Warning:
            N'oubliez pas qu'étant donné une position, il existe une méthode dans la classe Position retournant
            les positions des quatre sauts possibles.

        Args:
            position_piece (Position): La position source.

        Returns:
            bool: True si une pièce est à la position reçue et celle-ci peut faire une prise. False autrement.

        """
        piece = self.recuperer_piece_a_position(position_piece)
        if piece:
            for position in position_piece.quatre_positions_sauts():
                if self.piece_peut_sauter_vers(position_piece, position):
                    return True
        return False

    def piece_de_couleur_peut_se_deplacer(self, couleur):
        """Vérifie si n'importe quelle pièce d'une certaine couleur reçue en argument a la possibilité de se déplacer
        vers une case adjacente (sans saut).

        ATTENTION: Réutilisez les méthodes déjà programmées!

        Args:
            couleur (str): La couleur à vérifier.

        Returns:
            bool: True si une pièce de la couleur reçue peut faire un déplacement standard, False autrement.
        """

        if couleur == "blanc":
            for position in self.cases:
                if self.cases[position].est_blanche() and self.piece_peut_se_deplacer(position):
                    return True

        if couleur == "noir":
            for position in self.cases:
                if self.cases[position].est_noire() and self.piece_peut_se_deplacer(position):
                    return True

        return False


    def piece_de_couleur_peut_faire_une_prise(self, couleur):
        """Vérifie si n'importe quelle pièce d'une certaine couleur reçue en argument a la possibilité de faire un
        saut, c'est à dire vérifie s'il existe une pièce d'une certaine couleur qui a la possibilité de prendre une
        pièce adverse.

        ATTENTION: Réutilisez les méthodes déjà programmées!

        Args:
            couleur (str): La couleur à vérifier.

        Returns:
            bool: True si une pièce de la couleur reçue peut faire un saut (une prise), False autrement.
        """

        if couleur == "blanc":
            for position in self.cases:
                if self.cases[position].est_blanche() and self.piece_peut_faire_une_prise(position):
                    return True

        if couleur == "noir":
            for position in self.cases:
                if self.cases[position].est_noire() and self.piece_peut_faire_une_prise(position):
                    return True

        return False

    def deplacer(self, position_source, position_cible):
        """Effectue le déplacement sur le damier. Si le déplacement est valide, on doit mettre à jour le dictionnaire
        self.cases, en déplaçant la pièce à sa nouvelle position (et possiblement en supprimant une pièce adverse qui a
        été prise).

        Cette méthode doit également:
        - Promouvoir un pion en dame si celui-ci atteint l'autre extrémité du plateau.
        - Retourner un message indiquant "ok", "prise" ou "erreur".

        ATTENTION: Si le déplacement est effectué, cette méthode doit retourner "ok" si aucune prise n'a été faite,
            et "prise" si une pièce a été prise.
        ATTENTION: Ne dupliquez pas de code! Vous avez déjà programmé (ou allez programmer) des méthodes permettant
            de valider si une pièce peut se déplacer vers un certain endroit ou non.

        Args:
            position_source (Position): La position source du déplacement.
            position_cible (Position): La position cible du déplacement.

        Returns:
            str: "ok" si le déplacement a été effectué sans prise, "prise" si une pièce adverse a été prise, et
                "erreur" autrement.

        """
        #si la pièce peut se déplacer et qu'elle arrive à une extrémité
        piece_source = self.recuperer_piece_a_position(position_source)
        couleur = piece_source.couleur
        if self.piece_peut_se_deplacer_vers(position_source, position_cible):
            if position_cible.ligne == 0 or position_cible.ligne == 7:
                self.cases.pop(position_source)
                self.cases[position_cible] = Piece(couleur, "dame")
                return "ok"
            #si elle n'arrive pas à une extrémité
            else:
                self.cases.pop(position_source)
                self.cases[position_cible] = Piece(couleur, "pion")
                return "ok"


        #si la pièce peut faire un prise et qu'elle arrive à une extrémité
        if self.piece_peut_faire_une_prise(position_source):
            if position_cible.ligne == 0 or position_cible.ligne == 7:
                self.cases.pop(position_source)
                self.cases.pop(position_source.position_a_manger(position_cible))
                self.cases[position_cible] = Piece(couleur, "dame")
                return "prise"
            #si elle n'arrive pas à une extrémité
            else:
                self.cases.pop(position_source)
                self.cases.pop(position_source.position_a_manger(position_cible))
                self.cases[position_cible] = Piece(couleur, "pion")
                return "prise"
        return "erreur"




        # TODO: À compléter

    def __repr__(self):
        """Cette méthode spéciale permet de modifier le comportement d'une instance de la classe Damier pour
        l'affichage. Faire un print(un_damier) affichera le damier à l'écran.

        """
        s = " +-0-+-1-+-2-+-3-+-4-+-5-+-6-+-7-+\n"
        for i in range(0, 8):
            s += str(i) + "| "
            for j in range(0, 8):
                if Position(i, j) in self.cases:
                    s += str(self.cases[Position(i, j)]) + " | "
                else:
                    s += "  | "
            s += "\n +---+---+---+---+---+---+---+---+\n"

        return s


if __name__ == "__main__":
    print('Test unitaires de la classe "Damier"...')

    damier = Damier()

    # TODO: À compléter
    assert damier.position_est_dans_damier(Position(0, 0)) is True
    assert damier.position_est_dans_damier(Position(8, 0)) is False
    assert damier.position_est_dans_damier(Position(0, 8)) is False

    print('Test position_est_dans_damier succès!')

    damier.cases[Position(5, 6)] = Piece("blanc", "dame")
    damier.cases[Position(4, 5)] = Piece("blanc", "dame")
    assert damier.piece_peut_se_deplacer_vers(Position(5, 0), Position(4, 1)) is True
    assert damier.piece_peut_se_deplacer_vers(Position(5, 0), Position(4, -1)) is False
    assert damier.piece_peut_se_deplacer_vers(Position(5, 0), Position(2, 3)) is False
    assert damier.piece_peut_se_deplacer_vers(Position(5, 0), Position(4, 0)) is False

    damier.cases.pop(Position(5, 6))
    damier.cases[Position(4, 5)] = Piece("blanc", "dame")
    assert damier.piece_peut_se_deplacer_vers(Position(4, 5), Position(4, 5)) is False
    assert damier.piece_peut_se_deplacer_vers(Position(4, 5), Position(3, 4)) is True
    assert damier.piece_peut_se_deplacer_vers(Position(4, 5), Position(5, 6)) is True

    print('Test piece_peut_se_deplacer_vers succès!')
    damier.cases.pop(Position(6, 3))

    assert damier.piece_peut_sauter_vers(Position(4, 5), Position(6, 3)) is False
    assert damier.piece_peut_sauter_vers(Position(4, 5), Position(2, 7)) is False
    assert damier.piece_peut_sauter_vers(Position(4, 5), Position(3, 6)) is False
    assert damier.piece_peut_sauter_vers(Position(4, 5), Position(5, 4)) is False
    assert damier.piece_peut_sauter_vers(Position(5, 2), Position(3, 2)) is False

    damier.cases[Position(5, 4)] = Piece('noir', 'pion')
    assert damier.piece_peut_sauter_vers(Position(4, 5), Position(6, 3)) is True

    print('Test piece_peut_sauter_vers succès!')


    assert damier.piece_peut_faire_une_prise(Position(6, 5)) is True
    assert damier.piece_peut_faire_une_prise(Position(4, 5)) is True
    assert damier.piece_peut_faire_une_prise(Position(5, 2)) is False
    assert damier.piece_peut_faire_une_prise(Position(6, 1)) is False
    assert damier.piece_peut_faire_une_prise(Position(5, 4)) is True
    assert damier.piece_peut_faire_une_prise(Position(6, 5)) is True
    assert damier.piece_peut_faire_une_prise(Position(5, 3)) is False

    print('Test piece_peut_faire_une_prise succès!')

    assert damier.piece_peut_se_deplacer(Position(4, 5)) is True
    assert damier.piece_peut_se_deplacer(Position(5, 4)) is True
    assert damier.piece_peut_se_deplacer(Position(6, 1)) is False
    assert damier.piece_peut_se_deplacer(Position(1, 4)) is False

    print('Test piece_peut_se_deplacer succès!')


    assert damier.piece_de_couleur_peut_se_deplacer("noir") is True
    assert damier.piece_de_couleur_peut_se_deplacer("blanc") is True
    damier.cases[Position(3, 0)] = Piece("blanc", "pion")
    damier.cases[Position(3, 2)] = Piece("blanc", "pion")
    damier.cases[Position(3, 4)] = Piece("blanc", "pion")
    damier.cases[Position(3, 6)] = Piece("blanc", "pion")
    damier.cases[Position(6, 3)] = Piece("blanc", "pion")
    assert damier.piece_de_couleur_peut_se_deplacer("noir") is False
    print('Test piece_de_couleur_peut_se_deplacer succès!')

    damier.cases.pop(Position(4,5))
    damier.cases.pop(Position(6,5))
    assert damier.piece_de_couleur_peut_faire_une_prise("noir") is True
    damier.cases.pop(Position(3, 0))
    damier.cases.pop(Position(3, 2))
    damier.cases.pop(Position(3, 4))
    damier.cases.pop(Position(3, 6))
    damier.cases.pop(Position(6, 3))
    assert damier.piece_de_couleur_peut_faire_une_prise("blanc") is False
    print('Test piece_de_couleur_peut_faire_une_prise succès!')

    assert damier.deplacer(Position(5,2), Position(4,3)) == "ok"
    assert damier.deplacer(Position(5,4), Position(3,2)) == "prise"
    assert damier.deplacer(Position(6,7), Position(4,5)) == "erreur"
    print('Test deplacer succès!')

    print('Test unitaires passés avec succès!')

    # NOTEZ BIEN: Pour vous aider lors du développement, affichez le damier!
    print(damier)
