import init
import time
import pygame

from classes import Coordonnee, Couleur, ActiveValue
from rangee import Rangee, int2str


class Mouse:
    def __init__(self):
        self.pos = (0, 0)
        self.button = 0


class Board:
    TILE_SIZE = 20

    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.cols = self.width // self.TILE_SIZE
        self.rows = self.height // self.TILE_SIZE
        self.mouse = Mouse()
        self.font = pygame.font.SysFont(None, 24)

        print("Taille Board:", self.cols, "x", self.rows)
        self.points = {}
        self.tuile_under_mouse = None
        self.mouse_button_down_on = None
        self.rangees = []
        self.add_rangee(Couleur.ROUGE, Coordonnee(5, 17), Coordonnee(0, -1), 10_000, (ActiveValue(Couleur.ROUGE, 0),))
        self.add_rangee(Couleur.VERT, Coordonnee(12, 17), Coordonnee(0, -1), 10_000, (ActiveValue(Couleur.ROUGE, 1_000),))
        bleuc = Couleur.BLEU.clair(3)
        self.add_rangee(bleuc, Coordonnee(19, 17), Coordonnee(0, -1), 10_000, (ActiveValue(Couleur.VERT, 1_000),))
        self.add_rangee(Couleur.BLANC, Coordonnee(26, 17), Coordonnee(0, -1), 10_000, (ActiveValue(bleuc, 1_000),))

        self.add_rangee(Couleur.JAUNE, Coordonnee(5, 27), Coordonnee(0, 1), 10_000, (ActiveValue(Couleur.BLANC, 1_000),))
        self.add_rangee(Couleur.ROSE, Coordonnee(12, 27), Coordonnee(0, 1), 10_000, (ActiveValue(Couleur.JAUNE, 10_000),))
        self.add_rangee(Couleur.CYAN, Coordonnee(19, 27), Coordonnee(0, 1), 10_000, (ActiveValue(Couleur.ROSE, 10_000),))
        blancf = Couleur.BLANC.fonce(3)
        blancf.libelle = "gris"
        self.add_rangee(blancf, Coordonnee(26, 27), Coordonnee(0, 1), 10_000, (ActiveValue(Couleur.CYAN, 10_000),))

        self.add_rangee(Couleur.MARRON, Coordonnee(40, 17), Coordonnee(0, -1), 10_000_000, (ActiveValue(blancf, 10_000),))
        self.add_rangee(Couleur.MAJENTA, Coordonnee(47, 17), Coordonnee(0, -1), 10_000_000, (ActiveValue(Couleur.MARRON, 100_000),))
        self.add_rangee(Couleur.VIOLET, Coordonnee(55, 17), Coordonnee(0, -1), 10_000_000, (ActiveValue(Couleur.MAJENTA, 100_000),))
        self.add_rangee(Couleur.C5, Coordonnee(62, 17), Coordonnee(0, -1), 1_000_000_000, 
            (ActiveValue(Couleur.ROUGE, 1_000), ActiveValue(Couleur.VERT, 10_000), ActiveValue(bleuc, 2_000),))

        self.time = time.perf_counter()

    def add_rangee(self, couleur, position: Coordonnee, direction: Coordonnee, max_value: int, actives_value: tuple[ActiveValue]):
        self.points[couleur] = 0
        self.rangees.append(Rangee(self, couleur, position, direction, self.TILE_SIZE, max_value, actives_value))

    def update(self):
        if time.perf_counter() - self.time > 2:
            self.time = time.perf_counter()
            update_points = True
        else:
            update_points = True  # False

        for rangee in self.rangees:
            rangee.update(update_points)

    def draw(self):
        self.screen.fill((20, 20, 20))
        for ligne in range(1, self.cols):
            pygame.draw.line(self.screen, (20, 60, 60), (ligne * self.TILE_SIZE, 0), (ligne * self.TILE_SIZE, self.height), 1)
        for col in range(1, self.rows):
            pygame.draw.line(self.screen, (20, 60, 60), (0, col * self.TILE_SIZE), (self.width, col * self.TILE_SIZE), 1)
        for rangee in self.rangees:
            rangee.draw()

        for i, points in enumerate(self.points):
            lib = self.font.render(points.libelle.title(), True, points.codes)
            self.screen.blit(lib, (1_003, 2 * i * self.TILE_SIZE + 404))
            lib = self.font.render(int2str(self.points[points]), True, points.codes)
            width, _ = lib.get_size()
            self.screen.blit(lib, (1_138 - width, 2 * i * self.TILE_SIZE + 404))

        for rangee in self.rangees:
            rangee.show_info(self.mouse)

        pygame.display.update()

    def mouse_move(self, mouse):
        self.mouse = mouse
        if self.tuile_under_mouse:
            self.tuile_under_mouse.is_mouse_in = False
            self.tuile_under_mouse = None

        for rangee in self.rangees:
            for tuile in rangee.tuiles:
                if tuile.enable and not tuile.active and tuile.rect.collidepoint(mouse.pos):
                    tuile.is_mouse_in = True
                    self.tuile_under_mouse = tuile
                    return

    def mouse_button_down(self, mouse):
        if self.tuile_under_mouse and mouse.button == 1:
            self.mouse_button_down_on = self.tuile_under_mouse
        else:
            self.mouse_button_down_on = None

    def mouse_button_up(self, mouse):
        if self.mouse_button_down_on and self.tuile_under_mouse and \
          self.mouse_button_down_on == self.tuile_under_mouse and mouse.button == 1:
            if self.tuile_under_mouse.onclick:
                if callable(self.tuile_under_mouse.onclick):
                    self.tuile_under_mouse.onclick()
                else:
                    for fonction in self.tuile_under_mouse.onclick:
                        fonction()
