import pygame
from classes.board import Board
from classes.NN import Network


width = 600
height = 600
rows = 24
cols = 24

black = (0, 0, 0)

surface = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
b = Board(surface, width, height, rows, cols, black, False, 500)

gens = 2
pop_size = 20


def main():
    cont = True

    for i in range(gens):
        for j in range(pop_size):
            network = Network()
            b.update_network(network)

            while cont:
                pygame.time.delay(50)
                clock.tick(10)

                if pygame.QUIT in list(map(lambda event: event.type, pygame.event.get())):
                    pygame.quit()

                b.redraw_surface()
                cont = not b.finished

            b.reset_game()
            cont = True


main()
