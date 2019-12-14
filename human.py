import pygame
from classes.board import Board

WIDTH = 600
HEIGHT = 600
ROWS = 24
COLS = 24

BLACK = (0, 0, 0)

SURFACE = pygame.display.set_mode((WIDTH, HEIGHT))
B = Board(SURFACE, WIDTH, HEIGHT, ROWS, COLS, BLACK)
CLOCK = pygame.time.Clock()


def main():
    while True:
        pygame.time.delay(50)
        CLOCK.tick(10)

        if pygame.QUIT in list(map(lambda event: event.type, pygame.event.get())):
            pygame.quit()

        B.redraw_surface()


main()
