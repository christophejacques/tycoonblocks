from dataclasses import dataclass
import init


class DefCouleur:
    def __init__(self, codes: tuple[int], libelle: str):
        self.libelle = libelle
        self.codes = codes

    def update(self, clair: bool, coef: float = 2.0):
        res = ()
        for i in range(3):
            if clair:
                res += (self.codes[i] + ((255-self.codes[i]) // coef),)
            else:
                res += (self.codes[i] - (self.codes[i]) // coef,)
        return res

    def reverse(self):
        res = tuple()
        for i in range(3):
            res += (255-self.codes[i],)
        return DefCouleur(res, self.libelle+"r")

    def clair(self, coef: float = 2.0):
        return DefCouleur(self.update(True, coef), f"{self.libelle}c")

    def fonce(self, coef: float = 2.0):
        return DefCouleur(self.update(False, coef), f"{self.libelle}f")

    def __str__(self):
        return f"{self.codes} {self.libelle}"


class Couleur:
    NOIR = DefCouleur((0, 0, 0), "noir")
    BLANC = DefCouleur((255, 255, 255), "blanc")

    ROUGE = DefCouleur((255, 0, 0), "rouge")
    VERT = DefCouleur((0, 255, 0), "vert")
    BLEU = DefCouleur((0, 0, 255), "bleu")

    JAUNE = DefCouleur((255, 255, 0), "jaune")
    ROSE = DefCouleur((255, 0, 255), "rose")
    CYAN = DefCouleur((0, 255, 255), "cyan")

    MARRON = DefCouleur((255, 128, 0), "marron")
    MAJENTA = DefCouleur((255, 0, 128), "majenta")

    C2 = DefCouleur((128, 255, 0), "c2")
    C3 = DefCouleur((0, 255, 128), "c3")

    VIOLET = DefCouleur((128, 0, 255), "violet")
    C5 = DefCouleur((0, 128, 255), "c5")


@dataclass
class Coordonnee:
    x: int
    y: int


@dataclass
class ActiveValue:
    couleur: Couleur
    value: int
