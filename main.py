import pygame
from classes import Board

width = 600
height = 600
rows = 24
cols = 24
surface = pygame.display.set_mode((width, height))
black = (0, 0, 0)


def main():
    b = Board(surface, width, height, rows, cols, black)
    clock = pygame.time.Clock()

    while True:
        pygame.time.delay(50)
        clock.tick(10)

        if pygame.QUIT in list(map(lambda event: event.type, pygame.event.get())):
            pygame.quit()

        b.redraw_surface()


main()
