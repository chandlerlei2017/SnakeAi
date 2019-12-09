import pygame
from random import randrange
white = (255, 255, 255)
green = (34, 139, 34)
red = (255, 8, 0)


class Board(object):
    def __init__(self, surface, width, height, rows, cols, colour):
        [snake_x, snake_y] = [randrange(3, cols - 3), randrange(3, rows - 3)]
        [snack_x, snack_y] = [snake_x, snake_y]

        while [snack_x, snack_y] == [snake_x, snake_y]:
            [snack_x, snack_y] = [randrange(3, cols - 3), randrange(3, rows-3)]

        self.dir_x = -1
        self.dir_y = 0

        self.surface = surface
        self.colour = colour

        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.squareWidth = self.width // self.cols
        self.squareHeight = self.height // self.rows

        self.snake = Snake(snake_x, snake_y, green,
                           self.squareHeight, self.squareWidth)

        self.snack = Square(snack_x, snack_y, red,
                            self.squareHeight, self.squareWidth)

    def redraw_surface(self):
        self.surface.fill((0, 0, 0))
        self.draw_grid()
        self.update_dir()
        self.draw_snake()
        self.draw_snack()
        pygame.display.update()

    def draw_grid(self):
        for x in range(1, self.rows):
            pygame.draw.line(self.surface, white, (0, x*self.squareHeight),
                             (self.width, x*self.squareHeight))

        for y in range(1, self.cols):
            pygame.draw.line(self.surface, white, (y*self.squareWidth, 0),
                             (y*self.squareWidth, self.height))

    def update_dir(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.dir_x == 0:
            self.dir_x = -1
            self.dir_y = 0

        elif keys[pygame.K_RIGHT] and self.dir_x == 0:
            self.dir_x = 1
            self.dir_y = 0

        elif keys[pygame.K_UP] and self.dir_y == 0:
            self.dir_x = 0
            self.dir_y = -1

        elif keys[pygame.K_DOWN] and self.dir_y == 0:
            self.dir_x = 0
            self.dir_y = 1

    def draw_snake(self):
        self.snake.move(self.dir_x, self.dir_y)
        self.snake.draw(self.surface)

    def draw_snack(self):
        self.snack.draw(self.surface)

    def random_snack(self):
        new_x = randrange(self.cols)
        new_y = randrange(self.rows)
        # TODO


class Square(object):
    def __init__(self, x, y, colour, height, width):
        self.x = x
        self.y = y
        self.colour = colour
        self.height = height
        self.width = width

    def move(self, dir_x, dir_y):
        self.x += dir_x
        self.y += dir_y

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour,
                         (self.x*self.width, self.y*self.height, self.width, self.height))


class Snake(object):
    def __init__(self, x, y, colour, height, width):
        self.head = Square(x, y, colour, height, width)
        self.body = [self.head]

    def draw(self, surface):
        for square in self.body:
            square.draw(surface)

    def move(self, dir_x, dir_y):
        for square in self.body:
            square.move(dir_x, dir_y)


class Snack(Square):
    def __init__(self):
        pass
