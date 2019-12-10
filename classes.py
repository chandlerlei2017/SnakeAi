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
            [snack_x, snack_y] = [randrange(cols), randrange(rows)]

        self.surface = surface
        self.colour = colour

        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.squareWidth = self.width // self.cols
        self.squareHeight = self.height // self.rows

        self.snake = Snake(snake_x, snake_y, -1, 0, green,
                           self.squareHeight, self.squareWidth)

        self.snack = Square(snack_x, snack_y, 0, 0, red,
                            self.squareHeight, self.squareWidth)

    def redraw_surface(self):
        self.surface.fill((0, 0, 0))
        self.draw_grid()
        self.snake.update_dir()
        self.move_snake()
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

    def move_snake(self):
        self.snake.move()

        if self.snake.head.x == self.snack.x and self.snake.head.y == self.snack.y:
            self.random_snack()
            self.snake.addSquare()

    def draw_snake(self):
        self.snake.draw(self.surface)

    def draw_snack(self):
        self.snack.draw(self.surface)

    def random_snack(self):
        new_x = self.snake.head.x
        new_y = self.snake.head.y

        while [new_x, new_y] in map(lambda square: [square.x, square.y], self.snake.body):
            new_x = randrange(self.cols)
            new_y = randrange(self.rows)

        self.snack.x = new_x
        self.snack.y = new_y


class Square(object):
    def __init__(self, x, y, dir_x, dir_y, colour, height, width):
        self.x = x
        self.y = y
        self.dir_x = dir_x
        self.dir_y = dir_y

        self.colour = colour
        self.height = height
        self.width = width

    def move(self):
        self.x += self.dir_x
        self.y += self.dir_y

    def draw(self, surface):
        print(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, self.colour,
                         (self.x*self.width, self.y*self.height, self.width, self.height))


class Snake(object):
    def __init__(self, x, y, dir_x, dir_y, colour, height, width):
        self.head = Square(x, y, dir_x, dir_y, colour, height, width)
        self.body = [self.head]
        self.turns = {}
        self.square_height = height
        self.square_width = width

    def update_dir(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.head.dir_x == 0:
            self.head.dir_x = -1
            self.head.dir_y = 0

            self.turns[(self.head.x, self.head.y)] = [-1, 0]

        elif keys[pygame.K_RIGHT] and self.head.dir_x == 0:
            self.head.dir_x = 1
            self.head.dir_y = 0

            self.turns[(self.head.x, self.head.y)] = [1, 0]

        elif keys[pygame.K_UP] and self.head.dir_y == 0:
            self.head.dir_x = 0
            self.head.dir_y = -1

            self.turns[(self.head.x, self.head.y)] = [0, -1]

        elif keys[pygame.K_DOWN] and self.head.dir_y == 0:
            self.head.dir_x = 0
            self.head.dir_y = 1

            self.turns[(self.head.x, self.head.y)] = [0, 1]

    def draw(self, surface):
        for square in self.body:
            square.draw(surface)

    def move(self):
        for index, square in enumerate(self.body):
            temp_cord = (square.x, square.y)
            if temp_cord in self.turns:
                [square.dir_x, square.dir_y] = self.turns[temp_cord]

                if index == len(self.body) - 1:
                    del self.turns[temp_cord]

            square.move()

    def addSquare(self):
        prev_square = self.body[-1]
        self.body.append(Square(prev_square.x - prev_square.dir_x,
                                prev_square.y - prev_square.dir_y, prev_square.dir_x, prev_square.dir_y, green, self.square_height, self.square_width))


class Snack(Square):
    def __init__(self):
        pass
