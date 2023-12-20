# Auteurs: À compléter

from tkinter import Tk, Label, NSEW
from Partie2.canvas_damier import CanvasDamier
from Partie1.partie import Partie
from Partie1.position import Position


class FenetrePartie(Tk):
    """Interface graphique de la partie de dames.

    Attributes:
        partie (Partie): Le gestionnaire de la partie de dame
        canvas_damier (CanvasDamier): Le «widget» gérant l'affichage du damier à l'écran
        messages (Label): Un «widget» affichant des messages textes à l'utilisateur du programme

        TODO: AJOUTER VOS PROPRES ATTRIBUTS ICI!
    """

    def __init__(self):
        """Constructeur de la classe FenetrePartie. On initialise une partie en utilisant la classe Partie du TP3 et
        on dispose les «widgets» dans la fenêtre.
        """

        # Appel du constructeur de la classe de base (Tk)
        super().__init__()

        # La partie
        self.partie = Partie()

        # Création du canvas damier.
        self.canvas_damier = CanvasDamier(self, self.partie.damier, 60)
        self.canvas_damier.grid(sticky=NSEW)
        self.canvas_damier.bind('<Button-1>', self.selectionner)

        # Ajout d'une étiquette d'information.
        self.messages = Label(self)
        self.messages.grid()

        # Nom de la fenêtre («title» est une méthode de la classe de base «Tk»)
        self.title("Jeu de dames")

        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def selectionner(self, event):
        """Méthode qui gère le clic de souris sur le damier.

        Args:
            event (tkinter.Event): Objet décrivant l'évènement qui a causé l'appel de la méthode.

        """

        # On trouve le numéro de ligne/colonne en divisant les positions en y/x par le nombre de pixels par case.
        ligne = event.y // self.canvas_damier.n_pixels_par_case
        colonne = event.x // self.canvas_damier.n_pixels_par_case
        position = Position(ligne, colonne)

        # piece = self.partie.damier.recuperer_piece_a_position(position)
        # if partie.position_source_selectionnee and piece is None:
        #     self.messages['foreground'] = 'red'
        #     self.messages['text'] = 'Erreur: Aucune pièce à cet endroit.'
        #     self.partie.effacer_selection()
        # else:
        #     self.messages['foreground'] = 'white'
        #     self.messages['text'] = 'Pièce sélectionnée à la position {}.'.format(position)

        resultat = self.valider_selection(position)
        self.messages['foreground'] = 'green' if resultat[0] else 'red'
        self.messages['text'] = resultat[1]

        self.canvas_damier.actualiser()

        # TODO: À continuer....

    def valider_selection(self, position):
        partie = self.partie
        selection_valide = True
        message = ''
        print('Click')

        if partie.position_source_selectionnee:
            validation_cible = partie.position_cible_valide(position)
            if not validation_cible[0]:
                partie.effacer_selection()
                message = validation_cible[1]
                selection_valide = False
            else:
                res = partie.jouer_tour(position)
                message = res[1]
        else:
            validation_source = partie.position_source_valide(position)
            if validation_source[0]:
                message = 'Selection valide'
                partie.position_source_selectionnee = position
            else:
                selection_valide = False
                message = 'Selection invalide'
                partie.effacer_selection()

        return selection_valide, message
