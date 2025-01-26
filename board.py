import init
import time
import pygame
import json

from typing import Self
from classes import Coordonnee, DefCouleur, Couleur, ActiveValue
from rangee import Rangee, int2str, GrowTuile, TransfertTuile, Tuile
# from controleur import ExplicitDeclaration


class Board:
    TILE_SIZE = 20

    def __init__(self, screen: pygame.Surface):
        self.screen: pygame.Surface = screen
        self.width, self.height = screen.get_size()
        self.cols: int = self.width // self.TILE_SIZE
        self.rows: int = self.height // self.TILE_SIZE
        self.mouse = None
        self.font24 = pygame.font.SysFont(None, 24)

        print("Taille Board:", self.cols, "x", self.rows)
        self.points: dict = {}
        self.tuile_under_mouse = None
        self.mouse_button_down_on = None
        self.rangees: list = []
        self.add_rangee(Couleur.ROUGE, Coordonnee(5, 17), Coordonnee(0, -1), 6_000_000, (ActiveValue(Couleur.ROUGE, 0),), Couleur.VERT)
        bleuc = Couleur.BLEU.clair(1.8)
        bleuc.libelle = "bleu"
        self.add_rangee(Couleur.VERT,  Coordonnee(12, 17), Coordonnee(0, -1), 6_000_000, (ActiveValue(Couleur.ROUGE, 1_000),), bleuc)
        self.add_rangee(bleuc,         Coordonnee(19, 17), Coordonnee(0, -1), 6_000_000, (ActiveValue(Couleur.VERT, 1_000),),  Couleur.BLANC)
        self.add_rangee(Couleur.BLANC, Coordonnee(26, 17), Coordonnee(0, -1), 6_000_000, (ActiveValue(bleuc, 1_000),),         Couleur.JAUNE)

        # -------------------
        self.add_rangee(Couleur.JAUNE, Coordonnee(5, 23),  Coordonnee(0, 1), 6_000_000, (ActiveValue(Couleur.BLANC, 1_000),),  Couleur.CYAN)
        self.add_rangee(Couleur.CYAN,  Coordonnee(12, 23), Coordonnee(0, 1), 6_000_000, (ActiveValue(Couleur.JAUNE, 10_000),), Couleur.MAJENTA)
        tech = Couleur.CYAN.fonce(3.0)
        tech.libelle = "tech"
        self.add_rangee(Couleur.MAJENTA, Coordonnee(19, 23), Coordonnee(0, 1), 6_000_000, (ActiveValue(Couleur.CYAN, 10_000),),    tech)
        self.add_rangee(tech,            Coordonnee(26, 23), Coordonnee(0, 1), 6_000_000, (ActiveValue(Couleur.MAJENTA, 10_000),), None)

        # -------------------
        self.add_rangee(Couleur.ORANGE, Coordonnee(40, 17), Coordonnee(0, -1), 10_000_000, (ActiveValue(tech, 10_000),), None)
        self.add_rangee(Couleur.VIOLET, Coordonnee(47, 17), Coordonnee(0, -1), 10_000_000, (ActiveValue(Couleur.ORANGE, 10_000),), None)
        self.add_rangee(Couleur.MARRON, Coordonnee(54, 17), Coordonnee(0, -1), 10_000_000, (ActiveValue(Couleur.VIOLET, 10_000),), None)

        gris = Couleur.BLANC.fonce(4.0)
        gris.libelle = "gris"
        self.add_rangee(gris, Coordonnee(61, 17), Coordonnee(0, -1), 1_000_000_000, (ActiveValue(Couleur.MARRON, 10_000),), None)

        # -------------------
        mech = Couleur.NOIR.clair(4.0)
        mech.libelle = "mech"
        self.add_rangee(mech, 
            Coordonnee(40, 23), 
            Coordonnee(0, 1), 1_000_000_000, 
            (
                ActiveValue(Couleur.ROUGE,   1_000_000_000), ActiveValue(Couleur.VERT,   1_000_000_000), ActiveValue(bleuc,          1_000_000_000),
                ActiveValue(Couleur.BLANC,   1_000_000_000), ActiveValue(Couleur.JAUNE,  1_000_000_000), ActiveValue(Couleur.CYAN,   1_000_000_000), 
                ActiveValue(Couleur.MAJENTA, 1_000_000_000), ActiveValue(tech,           1_000_000_000), ActiveValue(Couleur.ORANGE, 1_000_000_000), 
                ActiveValue(Couleur.VIOLET,  1_000_000_000), ActiveValue(Couleur.MARRON, 1_000_000_000), ActiveValue(gris,           1_000_000_000), 
            ), 
            None)

        self.time = time.perf_counter()

    def add_rangee(self, couleur: DefCouleur, position: Coordonnee, direction: Coordonnee, 
      max_value: int, actives_value: tuple[ActiveValue], destinataire: DefCouleur | None) -> None:
        self.points[couleur] = 0
        self.rangees.append(
            Rangee(self, couleur, position, direction, self.TILE_SIZE, max_value, actives_value, destinataire))

    def get_rangee_from_color(self, couleurstr: str) -> Rangee | None:
        for rangee in self.rangees:
            if rangee.couleur.libelle.upper() == couleurstr.upper():
                return rangee
        return None


    def load_from_disk(self) -> None:
        with open("save.json", "r") as fp:
            js = json.load(fp)

        for couleur in js["POINTS"]:
            for point in self.points:
                if couleur == point.libelle.upper():
                    self.points[point] = js["POINTS"][couleur]
                    break

        rangee: Rangee | None
        for couleurstr in js["RANGEES"]:
            rangee = self.get_rangee_from_color(couleurstr)
            if not rangee or not js["RANGEES"].get(couleurstr):
                continue
            rangee.active = js["RANGEES"][couleurstr]["ACTIVE"]
            if rangee.active:
                rangee.value = js["RANGEES"][couleurstr]["VALUE"]
                for i, active_tile in enumerate(js["RANGEES"][couleurstr]["TILES"]):
                    if active_tile:
                        rangee.tuiles[i].active = True

    def save_to_disk(self) -> None:
        js: dict = {}
        js["POINTS"] = {}
        for couleur in self.points:
            js["POINTS"][couleur.libelle.upper()] = self.points[couleur]

        js["RANGEES"] = {}
        for rangee in self.rangees:
            js["RANGEES"][rangee.couleur.libelle.upper()] = {}
            js["RANGEES"][rangee.couleur.libelle.upper()]["ACTIVE"] = rangee.active
            js["RANGEES"][rangee.couleur.libelle.upper()]["VALUE"] = rangee.value
            js["RANGEES"][rangee.couleur.libelle.upper()]["TILES"] = []

            for tile in rangee.tuiles:
                if isinstance(tile, GrowTuile):
                    pass
                    # js["RANGEES"][rangee.couleur.libelle.upper()]["GROWS"].append(tile.active)
                elif isinstance(tile, TransfertTuile):
                    pass
                    # js["RANGEES"][rangee.couleur.libelle.upper()]["CONVERTS"].append(tile.active)
                elif isinstance(tile, Tuile):
                    js["RANGEES"][rangee.couleur.libelle.upper()]["TILES"].append(tile.active)
                else:
                    print("Type de la tuile inconnu:", type(tile))

        with open("save.json", "w") as fp:
            json.dump(js, fp, ensure_ascii=True, indent=4, sort_keys=True)

    def update(self) -> None:
        if time.perf_counter() - self.time > 2:  # 0.05
            self.time = time.perf_counter()
            update_points = True
        else:
            update_points = False  # False

        for rangee in self.rangees:
            rangee.update(update_points)

    def draw(self) -> None:
        self.screen.fill((20, 20, 20))
        for ligne in range(1, self.cols):
            pygame.draw.line(self.screen, (20, 60, 60), (ligne * self.TILE_SIZE, 0), (ligne * self.TILE_SIZE, self.height), 1)
        for col in range(1, self.rows):
            pygame.draw.line(self.screen, (20, 60, 60), (0, col * self.TILE_SIZE), (self.width, col * self.TILE_SIZE), 1)
        for rangee in self.rangees:
            rangee.draw()

        for i, points in enumerate(self.points):
            decaly = i // 4
            lib = self.font24.render(points.libelle.title(), True, points.codes)
            width, height = lib.get_size()
            self.screen.blit(lib, (50 * self.TILE_SIZE, 
                25*self.TILE_SIZE - height + (i+decaly) * self.TILE_SIZE))
            lib = self.font24.render(int2str(self.points[points]), True, points.codes)
            width, height = lib.get_size()
            self.screen.blit(lib, (58 * self.TILE_SIZE - width, 
                25*self.TILE_SIZE - height + (i+decaly) * self.TILE_SIZE))

        if isinstance(self.mouse, pygame.event.EventType):
            for rangee in self.rangees:
                rangee.show_info(self.mouse)

        pygame.display.update()

    def mouse_move(self, mouse: pygame.event.Event) -> None:
        self.mouse = mouse
        if self.tuile_under_mouse:
            self.tuile_under_mouse.is_mouse_in = False
            self.tuile_under_mouse = None

        for rangee in self.rangees:
            for tuile in rangee.tuiles:
                if not tuile.active and tuile.rect.collidepoint(mouse.pos):
                    tuile.is_mouse_in = True
                    self.tuile_under_mouse = tuile
                    return

    def mouse_button_down(self, mouse: pygame.event.Event) -> None:
        if self.tuile_under_mouse and mouse.button == 1:
            self.mouse_button_down_on = self.tuile_under_mouse
        else:
            self.mouse_button_down_on = None

    def mouse_button_up(self, mouse: pygame.event.Event) -> None:
        if self.mouse_button_down_on and self.tuile_under_mouse and \
          self.mouse_button_down_on == self.tuile_under_mouse and mouse.button == 1 and \
          self.mouse_button_down_on.enable:

            for event in self.tuile_under_mouse.onclick:
                event()
