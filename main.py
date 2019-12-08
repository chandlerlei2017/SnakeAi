import pygame
from classes import Snake

width = 500
height = 500
rows = 20


def drawGrid(width, rows, surface):
    sizeBtwn = width // rows
    x = y = 0

    for l in range(rows):
        x += sizeBtwn
        y += sizeBtwn

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, width))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (width, y))


def redrawWindow(surface):
    surface.fill((0, 0, 0))
    drawGrid(width, rows, surface)
    pygame.display.update()


def main():
    surface = pygame.display.set_mode((width, height))
    s = Snake((255, 0, 0), (10, 10))

    flag = True
    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        redrawWindow(surface)


main()
