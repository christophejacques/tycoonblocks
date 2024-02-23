from time import time
import math
import init
import pygame

from classes import Coordonnee, DefCouleur, Couleur, ActiveValue
from controleur import VarDecl, ExplicitDeclaration


def un_tick_sur_deux() -> int:
    return divmod(divmod(int(3*time()), 10)[1], 2)[1]


@VarDecl().ctrl()
def get_font(size: int) -> pygame.font.Font:
    return pygame.font.SysFont(None, size)


@VarDecl().ctrl()
def int2str(i: int) -> str:
    s = str(i)
    longueur = len(s)
    if longueur > 9:
        unite = " B"
        unite = " Md"
        s = "1"
    elif longueur > 7:
        unite = " M"
        s = s[:longueur-6]
    elif longueur > 6:
        unite = " M"
        s = s[:longueur-6] + "." + s[1]
    elif longueur > 4:
        unite = " K"
        s = s[:longueur-3]
    elif longueur > 3:
        unite = " K"
        s = s[:longueur-3] + "." + s[1]
    else:
        unite = ""
    return s + unite


@VarDecl().ctrl()
def coefficiant(maximum: int) -> int:
    f = [10, 10]
    a = b = 10
    while b < maximum:
        a, b = a+b,  a+2*b
        f.extend([a, b])

    while f[-1] > maximum:
        f.pop()

    res = f[-28:].copy()
    while res:
        val = res.pop(0)
        yield val // (10**int(math.log10(val)-1)) * 10**int(math.log10(val)-1)

    while True:
        yield 0


class ShowInfo(metaclass=ExplicitDeclaration):

    def show_info(self) -> None:
        if self.enable and self.parent.active:
            self.couleur_cadre = Couleur.C3.codes
            couleur_rangee = Couleur.BLANC.codes
        else:
            self.couleur_cadre = Couleur.BLANC.fonce().codes
            couleur_rangee = Couleur.BLANC.fonce(2.5).codes

        maxx = maxy = 0
        for element in self.texte:
            libelle, taille, couleur, dx, dy = element
            libr = get_font(taille).render(libelle, True, couleur)
            width, height = libr.get_size()
            if dy + height+4 > maxy: maxy = dy + height+4

        for i, active_value in enumerate(self.actives_value):
            self.texte.append((f"{active_value.couleur.libelle.title()}", 24, active_value.couleur.codes, 75, maxy+20*i))
            if self.parent.parent.points.get(active_value.couleur, -1) >= active_value.value:
                texte_controle = "Ok"
                couleur_controle = Couleur.C3.codes
                couleur_rangee = Couleur.BLANC.codes
            else:
                self.couleur_cadre = Couleur.BLANC.fonce().codes
                texte_controle = "Ko"
                couleur_controle = Couleur.ROUGE.codes
                couleur_rangee = Couleur.BLANC.fonce(2.5).codes

            self.texte.append((f"{int2str(active_value.value)}", 24, couleur_rangee, 25, maxy+20*i))
            self.texte.append((texte_controle, 24, couleur_controle, 170, maxy+20*i))

        maxx = maxy = 0
        for element in self.texte:
            libelle, taille, couleur, dx, dy = element

            libr = get_font(taille).render(libelle, True, couleur)
            width, height = libr.get_size()
            if dx + width + 10 > maxx: maxx = dx + width + 10
            if dy + height + 10 > maxy: maxy = dy + height + 10

        if self.rect[0]+250 < self.parent.parent.width:
            self.posx = self.rect[0] + self.rect[2] + 10
        else:
            self.posx = self.rect[0] - 10 - maxx

        if self.rect[1]+maxy+10 > self.parent.parent.height:
            self.posy = self.parent.parent.height - 10 - maxy
        else:
            self.posy = self.rect[1]

        pygame.draw.rect(self.screen, (10, 10, 10, 30), (self.posx+10, self.posy+10, maxx, maxy))
        if self.enable:
            pygame.draw.rect(self.screen, (20, 60, 60), (self.posx, self.posy, maxx, maxy))
        else:
            pygame.draw.rect(self.screen, (20, 50, 50), (self.posx, self.posy, maxx, maxy))

        for element in self.texte:
            libelle, taille, couleur, dx, dy = element
            libr = get_font(taille).render(libelle, True, couleur)
            self.screen.blit(libr, (self.posx+dx, self.posy+5+dy))

        pygame.draw.rect(self.screen, self.couleur_cadre, (self.posx, self.posy, maxx, maxy), 1)
        pass


class Rangee:
    pass


class Tuile(metaclass=ExplicitDeclaration):

    def __init__(self, parent: Rangee, couleur: DefCouleur, rect: tuple[int], value: int, actives_value: tuple[ActiveValue]):
        self.parent = parent
        self.screen = parent.screen
        self.couleur = couleur
        self.rect = pygame.Rect(rect)
        self.value = value
        self.actives_value = actives_value
        self.enable = False
        self.active = False
        self.onclick = [self.activate]
        self.is_mouse_in = False

    def activate(self) -> None:
        if not self.active:
            self.active = True
            for active_value in self.actives_value:
                self.parent.parent.points[active_value.couleur] -= active_value.value

    def update(self, update_points: bool) -> None:
        self.enable = True
        for active_value in self.actives_value:
            self.enable = self.enable and self.parent.parent.points.get(active_value.couleur, -1) >= active_value.value
        if update_points and self.active:
            if self.parent.parent.points[self.couleur] < 1_000_000_000:
                self.parent.parent.points[self.couleur] += self.parent.value * self.value

    def show_info(self) -> None:
        if self.enable and self.parent.active:
            couleur_texte = Couleur.C3.codes
            couleur_rangee = Couleur.BLANC.codes
        else:
            couleur_texte = Couleur.C3.fonce(3.0).codes
            couleur_rangee = Couleur.BLANC.fonce(3.0).codes

        if self.value == 0:
            self.texte = [
                # libelle, taille, couleur, dx, dy
                ("Activation de la", 24, couleur_texte, 5, 0),
                ("rangée de", 24, couleur_rangee, 25, 20),
                (self.couleur.libelle.title(), 24, self.couleur.codes, 110, 20),
                ("pour un coût de", 24, couleur_texte, 5, 50),
            ]
        else:
            self.texte = [
                # libelle, taille, couleur, dx, dy
                ("Création d'une unité", 24, couleur_texte, 5, 0),
                ("de", 24, couleur_rangee, 25, 20),
                (self.couleur.libelle.title(), 24, self.couleur.codes, 55, 20),
                ("(toutes les 2s)", 18, Couleur.C2.codes, 5, 40),
                ("pour un coût de", 24, couleur_texte, 5, 60),
            ]
        ShowInfo.show_info(self)

    def draw(self) -> None:
        if self.enable:
            couleur = self.couleur
        elif self.parent.active:
            couleur = self.couleur.fonce()
        else:
            couleur = self.couleur.fonce(1.5)
        if self.active:
            pygame.draw.rect(self.screen, couleur.codes, self.rect)
        elif self.is_mouse_in and self.enable:
            if un_tick_sur_deux():
                pygame.draw.rect(self.screen, couleur.codes, self.rect, 2)
            else:
                pygame.draw.rect(self.screen, couleur.codes, self.rect)
        else:
            pygame.draw.rect(self.screen, couleur.codes, self.rect, 1)


class GrowTuile(Tuile, ShowInfo):
    def __init__(self, parent: Rangee, couleur: DefCouleur, rect: tuple[int], value: int, actives_value: tuple[ActiveValue]):
        super().__init__(parent, couleur, rect, value, actives_value)
        self.points = (
            (rect[0], rect[1] + rect[3]), 
            (rect[0] + rect[2], rect[1] + rect[3]), 
            (rect[0] + rect[2]//2, rect[1]))

    def activate(self):
        if self.enable:
            self.parent.value += self.value
            for active_value in self.actives_value:
                self.parent.parent.points[active_value.couleur] -= active_value.value

    def show_info(self):
        if self.enable:
            couleur_texte = Couleur.C3.codes
            couleur_rangee = Couleur.BLANC.codes
        else:
            couleur_texte = Couleur.C3.fonce(3.0).codes
            couleur_rangee = Couleur.BLANC.fonce(3.0).codes

        self.texte = [
            # libelle, taille, couleur, dx, dy
            ("Coefficiant augmenté de", 24, couleur_texte, 5, 0),
            (f"{int2str(self.value)}", 24, couleur_rangee, 25, 20),
            (self.couleur.libelle.title(), 24, self.couleur.codes, 75, 20),
            ("pour un coût de", 24, couleur_texte, 5, 50),
        ]
        ShowInfo.show_info(self)

    def draw(self):
        if self.enable:
            couleur = self.couleur
        else:
            couleur = self.couleur.fonce()

        if self.is_mouse_in and self.enable:
            if un_tick_sur_deux():
                pygame.draw.polygon(self.screen, couleur.codes, self.points, 2)
            else:
                pygame.draw.polygon(self.screen, couleur.codes, self.points)
        else:
            pygame.draw.polygon(self.screen, couleur.codes, self.points, 1)


class TransfertTuile(Tuile, ShowInfo):
    def __init__(self, parent: Rangee, couleur: DefCouleur, rect: tuple[int], value: int, actives_value: tuple[ActiveValue], destinataire: DefCouleur):
        super().__init__(parent, couleur, rect, value, actives_value)
        self.destinataire = destinataire
        self.pointsh = (
            (rect[0], rect[1]), 
            (rect[0] + rect[2], rect[1] + rect[3]//2), 
            (rect[0], rect[1] + rect[3]//2), 
            )
        self.pointsb = (
            (rect[0], 1+rect[1] + rect[3]//2), 
            (rect[0] + rect[2], 1+rect[1] + rect[3]//2), 
            (rect[0], rect[1]+rect[3]), 
            )

        # (rect[0] + rect[2], rect[1] + rect[3]), 
        # (rect[0] + rect[2]//2, rect[1]))

    def activate(self):
        if self.enable:
            for active_value in self.actives_value:
                self.parent.parent.points[active_value.couleur] -= active_value.value
                self.parent.parent.points[self.destinataire] += self.value

    def show_info(self):
        if self.enable:
            couleur_texte = Couleur.C3.codes
            couleur_rangee = Couleur.BLANC.codes
        else:
            couleur_texte = Couleur.C3.fonce(3.0).codes
            couleur_rangee = Couleur.BLANC.fonce(3.0).codes
            
        self.texte = [
            # libelle, taille, couleur, dx, dy
            ("Convertion en", 24, couleur_texte, 5, 0),
            (f"{int2str(self.value)}", 24, couleur_rangee, 25, 20),
            (self.destinataire.libelle.title(), 24, self.destinataire.codes, 75, 20),
            ("pour un coût de", 24, couleur_texte, 5, 50),
        ]
        ShowInfo.show_info(self)

    def draw(self):
        if self.enable:
            couleurh = self.couleur
            couleurb = self.destinataire
        else:
            couleurh = self.couleur.fonce()
            couleurb = self.destinataire.fonce()

        if self.is_mouse_in and self.enable:
            if un_tick_sur_deux():
                pygame.draw.polygon(self.screen, couleurh.codes, self.pointsh, 2)
                pygame.draw.polygon(self.screen, couleurb.codes, self.pointsb, 2)
            else:
                pygame.draw.polygon(self.screen, couleurh.codes, self.pointsh)
                pygame.draw.polygon(self.screen, couleurb.codes, self.pointsb)
        else:
            pygame.draw.polygon(self.screen, couleurh.codes, self.pointsh, 1)
            pygame.draw.polygon(self.screen, couleurb.codes, self.pointsb, 1)


class Board:
    pass


class Mouse:
    pass


class Rangee(metaclass=ExplicitDeclaration):
    NB_TUILE_ROWS = 14
    NB_TUILES_OPTION = 6
    BORDER_LEN = 2

    def __init__(self, parent: Board, couleur: DefCouleur, position: Coordonnee, direction: Coordonnee, 
      size: int, max_value: int, actives_value: tuple[ActiveValue], destinataire: DefCouleur) -> None:
        self.parent = parent
        self.screen = parent.screen
        self.couleur = couleur
        self.pos = position
        self.dir = direction
        self.tuiles = []
        self.value = 1
        self.max_value = max_value
        self.actives_value = actives_value
        self.size = size
        self.active = False

        self.font = get_font(24)
        self.lib_couleur = self.font.render(self.couleur.libelle.title(), True, self.couleur.codes)
        largeur, _ = self.lib_couleur.get_size()
        self.pos_name = Coordonnee((1 + self.pos.x) * self.size + self.BORDER_LEN - largeur//2 - 4, 
            (self.dir.y * (2+self.NB_TUILE_ROWS) + self.pos.y) * self.size + self.BORDER_LEN)

        self.pos_value = Coordonnee((self.dir.x * (1+self.NB_TUILE_ROWS) + self.pos.x) * self.size + self.BORDER_LEN, 
            (self.dir.y * (1+self.NB_TUILE_ROWS) + self.pos.y) * self.size + self.BORDER_LEN)

        dx = 1 if self.dir.x == 0 else 0
        dy = 1 if self.dir.y == 0 else 0

        # Tuile de deblocage de la rangee
        tuile = Tuile(self, self.couleur, 
            (self.pos.x * self.size + self.BORDER_LEN, 
             self.pos.y * self.size + self.BORDER_LEN, 
             2*self.size - 2*self.BORDER_LEN, 
             self.size - 2*self.BORDER_LEN), 0, actives_value)
        tuile.onclick = [self.activate, tuile.activate]
        self.tuiles.append(tuile)

        ycoef = coefficiant(max_value)
        coef = 0
        for idx in range(1, 1+self.NB_TUILE_ROWS):
            # Rangee de gauche
            tuile = Tuile(self, self.couleur, 
                ((self.dir.x * idx + self.pos.x) * self.size + self.BORDER_LEN, 
                 (self.dir.y * idx + self.pos.y) * self.size + self.BORDER_LEN, 
                 self.size - 2*self.BORDER_LEN, 
                 self.size - 2*self.BORDER_LEN), 1, (ActiveValue(couleur, coef),))
            self.tuiles.append(tuile)

            # coef = self.max_value * 2 * idx // (2 * self.NB_TUILE_ROWS)
            coef = next(ycoef)
            # Rangee de droite
            tuile = Tuile(self, self.couleur, 
                ((dx + self.dir.x * idx + self.pos.x) * self.size + self.BORDER_LEN, 
                 (dy + self.dir.y * idx + self.pos.y) * self.size + self.BORDER_LEN, 
                 self.size - 2*self.BORDER_LEN, 
                 self.size - 2*self.BORDER_LEN), 1, (ActiveValue(couleur, coef),))
            self.tuiles.append(tuile)

            # coef = self.max_value * (2 * idx + 1) // (2 * self.NB_TUILE_ROWS)
            coef = next(ycoef)

        # Tuiles de croissance
        coef = 10_000
        for idx in range(self.NB_TUILES_OPTION):
            tuile = GrowTuile(self, self.couleur, 
                ((self.pos.x - 2) * self.size + self.BORDER_LEN, 
                 (dy + self.dir.y * (2*idx+3) + self.pos.y) * self.size + self.BORDER_LEN, 
                 self.size - 2*self.BORDER_LEN, 
                 self.size - 2*self.BORDER_LEN), coef//10_000, (ActiveValue(couleur, coef),))
            self.tuiles.append(tuile)
            coef *= 10

        # Tuiles de convertion
        if destinataire:
            coef = 10_000
            for idx in range(self.NB_TUILES_OPTION):
                tuile = TransfertTuile(self, self.couleur, 
                    ((self.pos.x + 3) * self.size + self.BORDER_LEN, 
                     (dy + self.dir.y * (2*idx+3) + self.pos.y) * self.size + self.BORDER_LEN, 
                     self.size - 2*self.BORDER_LEN, 
                     self.size - 2*self.BORDER_LEN), coef//100, (ActiveValue(couleur, coef),), destinataire)
                self.tuiles.append(tuile)
                coef *= 10

    def activate(self) -> None:
        self.active = True

    def update(self, update_points: bool) -> None:
        self.tuiles[0].update(False)
        if self.active:
            for tuile in self.tuiles[1:]:
                tuile.update(update_points)

    def show_info(self, mouse: pygame.event.Event) -> None:
        for tuile in self.tuiles:
            if not tuile.active and tuile.actives_value and tuile.rect.collidepoint(mouse.pos):
                tuile.show_info()
                return

    def draw(self) -> None:
        # rectangle si inactif
        if not self.active:
            px = (self.pos.x-2)
            if self.dir.y > 0:
                py = self.pos.y + 1
            elif self.dir.y < 0:
                py = self.pos.y-16 

            pygame.draw.rect(
                self.screen, Couleur.ROUGE.codes, 
                (px*self.size, py*self.size, 6*self.size, 16*self.size), 1)

        for tuile in self.tuiles:
            tuile.draw()

        img = self.font.render(int2str(self.value), True, self.couleur.codes)
        self.screen.blit(img, (self.pos_value.x, self.pos_value.y))
        self.screen.blit(self.lib_couleur, (self.pos_name.x, self.pos_name.y))
