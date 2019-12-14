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
B = Board(SURFACE, WIDTH, HEIGHT, ROWS, COLS, BLACK, False)

GENS = 3
POP_SIZE = 10


def get_file_name():
    files = os.listdir("data")
    files.sort()

    if not len(files):
        return "data/1.csv"

    return "data/{}.csv".format(int(files[-1][0]) + 1)


def get_file_name_nn():
    files = list(filter(lambda x: "_nn" in x, os.listdir("data")))
    files.sort()

    if not len(files):
        return "data/1_nn.csv"

    return "data/{}_nn.csv".format(int(files[-1][0]) + 1)


def main():
    cont = True
    file_name = get_file_name()
    file_name_nn = get_file_name_nn()

    with open(file_name, 'w') as res_file:
        writer = csv.writer(res_file)
        writer.writerow(["Gen"] + ["s_{}".format(i) for i in range(1, POP_SIZE + 1)])

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

        final = sorted(list(zip(scores, networks)), key=lambda x: x[0], reverse=True)

        with open(file_name, 'a') as res_file:
            writer = csv.writer(res_file)
            writer.writerow([str(i + 1)] + [score for score in scores])

        with open(file_name_nn, 'a') as res_file:
            writer = csv.writer(res_file)

            for network in final[:5]:
                writer.writerow(network[1].get_weights())

            writer.writerow([])


main()
