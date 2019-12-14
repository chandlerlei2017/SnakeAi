import pygame
from classes.board import Board
from classes.NN import Network
import csv
import os

WIDTH = 600
HEIGHT = 600
ROWS = 24
COLS = 24

BLACK = (0, 0, 0)

SURFACE = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
B = Board(SURFACE, WIDTH, HEIGHT, ROWS, COLS, BLACK, False, 150)

GENS = 50
POP_SIZE = 30


def get_file_name():
    files = os.listdir("data")
    files.sort()

    if not len(files):
        return "data/1.csv"

    return "data/{}.csv".format(int(files[-1][0]) + 1)


def main():
    cont = True
    # res_file = open(get_file_name(), 'w')

    for i in range(GENS):
        networks = [Network() for i in range(POP_SIZE)]
        scores = []

        for network in networks:
            cont = True
            B.update_network(network)

            while cont:
                pygame.time.delay(50)
                CLOCK.tick(10)

                if pygame.QUIT in list(map(lambda event: event.type, pygame.event.get())):
                    pygame.quit()

                B.redraw_surface()
                cont = not B.finished

            scores.append(B.score)
            print(B.score)

            B.reset_game()


main()
