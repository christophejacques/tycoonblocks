import pygame

pygame.init()

# Définir la couleur du fond
bg_color = (255, 255, 255)

# Définir la couleur de la bordure
border_color = (0, 0, 255)

# Définir la couleur de fond du rectangle avec un canal alpha
rect_color = (0, 0, 255, 128)

# Définir la taille et la position du rectangle
rect = pygame.Rect(100, 100, 200, 100)

# Créer une surface
screen = pygame.display.set_mode((640, 480))

# Remplir la surface avec la couleur de fond
screen.fill(bg_color)

# Dessiner le rectangle
pygame.draw.rect(screen, rect_color, rect, 50)

# Mettre à jour l'affichage
pygame.display.update()
input()
