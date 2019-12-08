import pygame
from classes import Snake

width = 500
height = 500
rows = 20


def drawGrid(width, rows, surface):
    sizeBtwn = width // rows
    inc = 0

    for l in range(rows):
        inc += sizeBtwn

        pygame.draw.line(surface, (255, 255, 255), (inc, 0), (inc, width))
        pygame.draw.line(surface, (255, 255, 255), (0, inc), (width, inc))


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
