import pygame
from random import randrange
white = (255, 255, 255)
green = (34, 139, 34)
red = (255, 8, 0)


class Board(object):
    def __init__(self, surface, width, height, rows, cols, colour):
        [snake_x, snake_y] = [randrange(cols), randrange(rows)]
        [snack_x, snack_y] = [snake_x, snake_y]

        while [snack_x, snack_y] == [snake_x, snake_y]:
            [snack_x, snack_y] = [randrange(cols), randrange(rows)]

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

    def draw_snake(self):
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

    def move(self, dirx, diry):
        self.x += dirx
        self.y += diry

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

    def move(self):
        pass


class Snack(Square):
    def __init__(self):
        pass
