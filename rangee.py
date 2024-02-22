import init
import pygame

from classes import Coordonnee, Couleur, ActiveValue


def int2str(i: int) -> str:
    s = str(i)
    longueur = len(s)
    if longueur > 9:
        unite = " B"
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


class Tuile:

    def __init__(self, parent, couleur, rect, value: int, actives_value: tuple[ActiveValue]):  # , onclick: object = None):
        self.parent = parent
        self.screen = parent.screen
        self.couleur = couleur
        self.rect = pygame.Rect(rect)
        self.value = value
        self.actives_value = actives_value
        self.enable = False
        self.active = False
        self.onclick = []
        self.is_mouse_in = False
        self.font = pygame.font.SysFont(None, 24)

    def activate(self):
        self.active = True
        for active_value in self.actives_value:
            self.parent.parent.points[active_value.couleur] -= active_value.value

    def update(self, update_points: bool):
        self.enable = True
        for active_value in self.actives_value:
            self.enable = self.enable and self.parent.parent.points.get(active_value.couleur, -1) >= active_value.value
        if update_points and self.active:
            self.parent.parent.points[self.couleur] += self.value if self.parent.parent.points[self.couleur] < 1_000_000_000 else 0

    def show_info(self):
        dx = 200
        if self.rect[0]+250 < self.parent.parent.width:
            px = self.rect[0] + self.rect[2] + 10
        else:
            px = self.rect[0] - 10 - dx
        dy = 24 + 20*len(self.actives_value)

        pygame.draw.rect(self.screen, (30, 30, 30), (px+5, self.rect[1]+5, dx, dy))
        pygame.draw.rect(self.screen, (20, 60, 60), (px, self.rect[1], dx, dy))
        couleur = (0, 255, 128)
        lib = self.font.render("Activation:", True, couleur)
        self.screen.blit(lib, (px+5, self.rect[1]+5))
        couleur_cadre = couleur
        for i, active_value in enumerate(self.actives_value):
            lib = self.font.render(f"{int2str(active_value.value)} {active_value.couleur.libelle.title()}", True, Couleur.BLANC.codes)
            self.screen.blit(lib, (px+25, self.rect[1]+25 + 20*i))
            if self.parent.parent.points.get(active_value.couleur, -1) >= active_value.value:
                lib = self.font.render("Ok", True, couleur)
            else:
                couleur_cadre = Couleur.BLANC.fonce().codes
                lib = self.font.render("Ko", True, Couleur.ROUGE.codes)
            self.screen.blit(lib, (px+170, self.rect[1]+25 + 20*i))

        pygame.draw.rect(self.screen, couleur_cadre, (px, self.rect[1], dx, dy), 1)

    def draw(self):
        if self.enable:
            couleur = self.couleur
        else:
            couleur = self.couleur.fonce()
        if self.active:
            pygame.draw.rect(self.screen, couleur.codes, self.rect)
        elif self.is_mouse_in:
            pygame.draw.rect(self.screen, couleur.codes, self.rect, 4)
        else:
            pygame.draw.rect(self.screen, couleur.codes, self.rect, 1)


class Rangee:
    LONGUEUR = 14
    BORDER_LEN = 2

    def __init__(self, parent, couleur, position: Coordonnee, direction: Coordonnee, size: int, max_value: int, actives_value: tuple[ActiveValue]):
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

        self.font = pygame.font.SysFont(None, 24)
        self.lib_couleur = self.font.render(self.couleur.libelle.title(), True, self.couleur.codes)
        largeur, _ = self.lib_couleur.get_size()
        self.pos_name = Coordonnee((1 + self.pos.x) * self.size + self.BORDER_LEN - largeur//2 - 4, 
            (self.dir.y * (2+self.LONGUEUR) + self.pos.y) * self.size + self.BORDER_LEN)

        self.pos_value = Coordonnee((self.dir.x * (1+self.LONGUEUR) + self.pos.x) * self.size + self.BORDER_LEN, 
            (self.dir.y * (1+self.LONGUEUR) + self.pos.y) * self.size + self.BORDER_LEN)

        dx = 1 if self.dir.x == 0 else 0
        dy = 1 if self.dir.y == 0 else 0
        # Tuile de deblocage
        tuile = Tuile(self, self.couleur, 
            (self.pos.x * self.size + self.BORDER_LEN, 
             self.pos.y * self.size + self.BORDER_LEN, 
             2*self.size - 2*self.BORDER_LEN, 
             self.size - 2*self.BORDER_LEN), 0, actives_value)
        tuile.onclick = [self.activate, tuile.activate]
        self.tuiles.append(tuile)

        coef = 0
        for idx in range(1, 1+self.LONGUEUR):
            # Rangee de gauche
            tuile = Tuile(self, self.couleur, 
                ((self.dir.x * idx + self.pos.x) * self.size + self.BORDER_LEN, 
                 (self.dir.y * idx + self.pos.y) * self.size + self.BORDER_LEN, 
                 self.size - 2*self.BORDER_LEN, 
                 self.size - 2*self.BORDER_LEN), 1, (ActiveValue(couleur, coef),))
            tuile.onclick = tuile.activate
            self.tuiles.append(tuile)

            coef = self.max_value * 2 * idx // (2 * self.LONGUEUR)
            # Rangee de droite
            tuile = Tuile(self, self.couleur, 
                ((dx + self.dir.x * idx + self.pos.x) * self.size + self.BORDER_LEN, 
                 (dy + self.dir.y * idx + self.pos.y) * self.size + self.BORDER_LEN, 
                 self.size - 2*self.BORDER_LEN, 
                 self.size - 2*self.BORDER_LEN), 1, (ActiveValue(couleur, coef),))
            tuile.onclick = tuile.activate
            self.tuiles.append(tuile)

            coef = self.max_value * (2 * idx + 1) // (2 * self.LONGUEUR)

    def activate(self):
        self.active = True

    def update(self, update_points: bool):
        self.tuiles[0].update(False)
        if self.active:
            for tuile in self.tuiles[1:]:
                tuile.update(update_points)

    def show_info(self, mouse):
        for tuile in self.tuiles:
            if not tuile.active and tuile.actives_value and tuile.rect.collidepoint(mouse.pos):
                tuile.show_info()

    def draw(self):
        # rectangle si inactif
        if not self.active:
            dy = self.dir.y if self.dir.y > 0 else 0
            pygame.draw.rect(self.screen, Couleur.ROUGE.clair().codes, 
                ((self.pos.x-1)*self.size, (self.pos.y + dy)*self.size, 5*self.size, self.dir.y*16*self.size), 1)

        for tuile in self.tuiles:
            tuile.draw()

        img = self.font.render(str(self.value), True, self.couleur.codes)
        self.screen.blit(img, (self.pos_value.x, self.pos_value.y))
        self.screen.blit(self.lib_couleur, (self.pos_name.x, self.pos_name.y))
