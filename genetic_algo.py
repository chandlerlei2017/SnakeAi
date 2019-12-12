import pygame
from classes import Board

width = 600
height = 600
rows = 24
cols = 24
surface = pygame.display.set_mode((width, height))
black = (0, 0, 0)


def main():
    b = Board(surface, width, height, rows, cols, black, False, 500)
    clock = pygame.time.Clock()

    cont = True

    while cont:
        pygame.time.delay(50)
        clock.tick(10)

        if pygame.QUIT in list(map(lambda event: event.type, pygame.event.get())):
            pygame.quit()

        b.redraw_surface()
        cont = not b.finished


main()
