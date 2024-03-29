import pygame

import init
from board import Board


def main():
    pygame.init()
    screen = pygame.display.set_mode((1360, 820), )
    clock = pygame.time.Clock()

    board = Board(screen)
    board.load_from_disk()
    running = True
    while running:
        board.update()
        board.draw()
        clock.tick(60)
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False        

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            elif event.type in [pygame.KEYUP, pygame.TEXTINPUT, pygame.TEXTEDITING]:
                pass

            elif event.type == pygame.MOUSEMOTION:
                board.mouse_move(event)

            elif event.type in [pygame.MOUSEBUTTONUP]:
                board.mouse_button_up(event)

            elif event.type in [pygame.MOUSEBUTTONDOWN]:
                board.mouse_button_down(event)

            elif event.type in [pygame.MOUSEWHEEL]:
                pass

            elif event.type in [pygame.WINDOWFOCUSGAINED, pygame.WINDOWFOCUSLOST, pygame.WINDOWSHOWN]:
                pass

            elif event.type in [pygame.WINDOWENTER, pygame.WINDOWLEAVE, pygame.WINDOWEXPOSED]:
                pass

            elif event.type in [pygame.VIDEOEXPOSE, pygame.VIDEORESIZE]:
                pass

            elif event.type in [pygame.WINDOWMINIMIZED, pygame.WINDOWRESTORED]:
                pass

            elif event.type == pygame.JOYDEVICEADDED:
                pass

            elif event.type == pygame.AUDIODEVICEADDED:
                pass

            elif event.type == pygame.ACTIVEEVENT:
                pass

            else:
                print(event)
                
    board.save_to_disk()
    pygame.quit()
