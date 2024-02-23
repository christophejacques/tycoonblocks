from dataclasses import dataclass
from controleur import ExplicitDeclaration

import init


class DefCouleur(metaclass=ExplicitDeclaration):
    
    def __init__(self, codes: tuple[int, int, int], libelle: str):
        self.libelle = libelle
        self.codes = codes

    def update(self, clair: bool, coef: float = 2.0) -> tuple[int, int, int]:
        # res: list[int, int, int] = (0, 0, 0)
        res: list[int] = [0, 0, 0]
        for i in range(3):
            if clair:
                res[i] = (self.codes[i] + (255-self.codes[i]) // coef)
            else:
                res[i] = (self.codes[i] - (self.codes[i]) // coef)
        return tuple(res)

        #     if clair:
        #         res += (self.codes[i] + ((255-self.codes[i]) // coef),)
        #     else:
        #         res += (self.codes[i] - (self.codes[i]) // coef,)
        # return res[:3]

    def reverse(self):
        res: tuple = tuple()
        for i in range(3):
            res += (255-self.codes[i],)

        return DefCouleur(res, self.libelle+"r")

    def clair(self, coef: float = 2.0):
        return DefCouleur(self.update(True, coef), f"{self.libelle}c")

    def fonce(self, coef: float = 2.0):
        return DefCouleur(self.update(False, coef), f"{self.libelle}f")

    def __str__(self) -> str:
        return f"{self.codes} {self.libelle}"


class Couleur(metaclass=ExplicitDeclaration):
    NOIR = DefCouleur((0, 0, 0), "noir")
    BLANC = DefCouleur((255, 255, 255), "blanc")

    ROUGE = DefCouleur((255, 0, 0), "rouge")
    VERT = DefCouleur((0, 255, 0), "vert")
    BLEU = DefCouleur((0, 0, 255), "bleu")

    JAUNE = DefCouleur((255, 255, 0), "jaune")
    ROSE = DefCouleur((255, 0, 255), "rose")
    CYAN = DefCouleur((0, 255, 255), "cyan")

    MARRON = DefCouleur((165, 42, 42), "marron")
    # ? = DefCouleur((255, 128, 0), "?")
    ORANGE = DefCouleur((255, 165, 0), "orange")
    MAJENTA = DefCouleur((255, 0, 128), "majenta")

    C2 = DefCouleur((128, 255, 0), "c2")
    C3 = DefCouleur((0, 255, 128), "c3")

    VIOLET = DefCouleur((128, 0, 255), "violet")
    C5 = DefCouleur((0, 128, 255), "c5")


@dataclass
class Coordonnee(metaclass=ExplicitDeclaration):
    x: int
    y: int


@dataclass
class ActiveValue(metaclass=ExplicitDeclaration):
    couleur: Couleur
    value: int
