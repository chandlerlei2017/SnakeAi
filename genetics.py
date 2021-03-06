import pygame
from classes.board import Board
from classes.NN import Network
from classes.mutator import Mutator
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

GENS = 250
POP_SIZE = 250
MUTATE_CHANCE = 0.3
MUTATE_WEIGHT_CHANCE = 0.02
RETAIN_TOP_RATIO = 0.3
RETAIN_REST_RATIO = 0.1

LAYERS = [24, 14, 3]


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


def write_data(file_name, file_name_nn, gen, scores, networks):
    with open(file_name, 'a') as res_file:
        writer = csv.writer(res_file)
        writer.writerow([str(gen)] + [score for score in scores] + [max(scores)])

    with open(file_name_nn, 'a') as res_file:
        writer = csv.writer(res_file)

        for network in networks[:5]:
            res = []

            for weight in network.get_weights():
                res += weight.flatten().tolist()

            writer.writerow(res)

        writer.writerow([])


# Genetics V1 -> 6 4 3 Neural Network
# Genetics V2 -> 36 20 3 Neural Network

def main():
    cont = True
    file_name = get_file_name()
    file_name_nn = get_file_name_nn()

    with open(file_name, 'w') as res_file:
        writer = csv.writer(res_file)
        writer.writerow(["Gen"] + ["s_{}".format(i) for i in range(1, POP_SIZE + 1)] + ["Max"])

    # networks = [Network([6, 4, 3]) for i in range(POP_SIZE)]
    networks = [Network(LAYERS) for i in range(POP_SIZE)]
    mutator = Mutator(MUTATE_CHANCE, MUTATE_WEIGHT_CHANCE, RETAIN_TOP_RATIO, RETAIN_REST_RATIO, LAYERS)

    for i in range(GENS):
        print("GEN {}".format(i + 1))
        print("##############################################")
        scores = []

        for network in networks:
            cont = True
            B.update_network(network)
            running = True

            while cont:
                pygame.time.delay(10)
                CLOCK.tick(50)

                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        pygame.quit()
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_SPACE:
                            running = not running

                if running:
                    B.redraw_surface()
                    cont = not B.finished

            scores.append(B.score)
            print(B.score)

            B.reset_game()

        new_scores, networks = (list(t) for t in zip(*sorted(zip(scores, networks), key=lambda x: x[0], reverse=True)))
        write_data(file_name, file_name_nn, i + 1, scores, networks)

        networks = mutator.generate_new_networks(networks)


main()
