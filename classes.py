import pygame
from random import randrange, choice
import math

import tkinter as tk
from tkinter import messagebox

white = (255, 255, 255)
green = (34, 139, 34)
red = (255, 8, 0)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


class Board(object):
    snake = None
    snack = None

    def __init__(self, surface, width, height, rows, cols, colour, human_playing=True, timeout=100):
        self.surface = surface
        self.colour = colour
        self.human_playing = human_playing
        self.timeout = timeout

        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.squareWidth = self.width // self.cols
        self.squareHeight = self.height // self.rows

        self.reset_game()

    def update_network(self, network):
        self.network = network

    def reset_game(self):
        self.score = 0
        self.finished = False
        self.count = 0

        snake_x, snake_y = randrange(
            3, self.cols - 3), randrange(3, self.rows - 3)
        snack_x, snack_y = snake_x, snake_y

        while [snack_x, snack_y] == [snake_x, snake_y]:
            [snack_x, snack_y] = [randrange(self.cols), randrange(self.rows)]

        if self.snake:
            del self.snake
        if self.snack:
            del self.snack

        init_dir_x = choice([0, choice([1, -1])])

        if init_dir_x != 0:
            init_dir_y = 0
        else:
            init_dir_y = choice([1, -1])

        self.snake = Snake(snake_x, snake_y, init_dir_x, init_dir_y,
                           green, self.squareHeight, self.squareWidth)

        self.snack = Square(snack_x, snack_y, 0, 0, red, self.squareHeight, self.squareWidth)

        self.snake_snack_dist = math.sqrt((snake_x - snack_x)**2 + (snake_y - snack_y)**2)

    def redraw_surface(self):
        if self.count > self.timeout:
            self.finished = True

        self.surface.fill((0, 0, 0))
        self.draw_grid()

        if self.human_playing:
            self.snake.update_dir_human()
        else:
            self.snake.update_dir_ai(self.network, self.snack.x, self.snack.y, self.cols, self.rows)

        self.move_snake()
        self.draw_snake()
        self.draw_snack()
        pygame.display.update()
        self.count += 1

    def draw_grid(self):
        for x in range(1, self.rows):
            pygame.draw.line(
                self.surface, white, (0, x * self.squareHeight),
                (self.width, x * self.squareHeight))

        for y in range(1, self.cols):
            pygame.draw.line(
                self.surface, white, (y * self.squareWidth, 0),
                (y * self.squareWidth, self.height))

    def move_snake(self):
        self.snake.move()

        if not self.snake.valid() or not self.snake_inbounds():
            if self.human_playing:
                message_box("You Died!", "Your final score was: {}, Start Over?".format(self.score))
                self.reset_game()
            self.finished = True

        elif [self.snake.head.x, self.snake.head.y] == [self.snack.x, self.snack.y]:
            self.score += 15
            self.snake.addSquare()
            self.random_snack()
        else:
            new_dist = math.sqrt(
                (self.snake.head.x - self.snack.x)**2 + (self.snake.head.y - self.snack.y)**2)

            if new_dist > self.snake_snack_dist:
                self.score -= 2
            else:
                self.score += 1

            self.snake_snack_dist = new_dist

    def snake_inbounds(self):
        if self.snake.head.x < 0 or self.snake.head.x >= self.cols or self.snake.head.y < 0 or self.snake.head.y >= self.rows:
            return False

        return True

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
        pygame.draw.rect(surface, self.colour, (self.x*self.width,
                                                self.y*self.height, self.width, self.height))


class Snake(object):
    def __init__(self, x, y, dir_x, dir_y, colour, height, width):
        self.head = Square(x, y, dir_x, dir_y, colour, height, width)
        self.body = [self.head]
        self.turns = {}
        self.square_height = height
        self.square_width = width

    def update_dir_human(self):
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

    def update_dir_ai(self, network, snack_x, snack_y, cols, rows):
        dir_mapping = {
            (1, 0): "R",
            (-1, 0): "L",
            (0, -1): "U",
            (0, 1): "D"
        }
        curr_dir = dir_mapping[(self.head.dir_x, self.head.dir_y)]
        body_pos = map(lambda square: (square.x, square.y), self.body)

        up_cond = self.head.y > 0 and (self.head.x, self.head.y - 1) not in body_pos
        left_cond = self.head.x > 0 and (self.head.x - 1, self.head.y) not in body_pos
        down_cond = self.head.y < rows - 1 and (self.head.x, self.head.y + 1) not in body_pos
        right_cond = self.head.x < cols - 1 and (self.head.x + 1, self.head.y) not in body_pos

        snack_up = snack_y < self.head.y
        snack_left = snack_x < self.head.x
        snack_down = snack_y > self.head.y
        snack_right = snack_x > self.head.x

        if curr_dir == "R":
            c_left = up_cond
            c_right = down_cond
            c_foward = right_cond

            s_left = snack_up
            s_right = snack_down
            s_foward = snack_right

        elif curr_dir == "L":
            c_left = down_cond
            c_right = up_cond
            c_foward = left_cond

            s_left = snack_down
            s_right = snack_up
            s_foward = snack_left

        elif curr_dir == "U":
            c_left = left_cond
            c_right = right_cond
            c_foward = up_cond

            s_left = snack_left
            s_right = snack_right
            s_foward = snack_up

        elif curr_dir == "D":
            c_left = right_cond
            c_right = left_cond
            c_foward = down_cond

            s_left = snack_right
            s_right = snack_left
            s_foward = snack_down

        res = network.predict(
            [
                int(c_foward),
                int(c_left),
                int(c_right),
                int(s_foward),
                int(s_left),
                int(s_right)])

        print(res, max(res))

        if res.index(max(res)) == 1:
            temp = self.head.dir_y
            self.head.dir_y = - self.head.dir_x
            self.head.dir_x = temp

            self.turns[(self.head.x, self.head.y)] = [self.head.dir_x, self.head.dir_y]

        if res.index(max(res)) == 2:
            temp = self.head.dir_y
            self.head.dir_y = self.head.dir_x
            self.head.dir_x = - temp

            self.turns[(self.head.x, self.head.y)] = [self.head.dir_x, self.head.dir_y]

        else:
            pass

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

    def valid(self):
        if [self.head.x, self.head.y] in [[square.x, square.y] for square in self.body[1:]]:
            return False

        return True

    def addSquare(self):
        prev_square = self.body[-1]
        self.body.append(Square(prev_square.x - prev_square.dir_x, prev_square.y - prev_square.dir_y,
                                prev_square.dir_x, prev_square.dir_y, green, self.square_height, self.square_width))
