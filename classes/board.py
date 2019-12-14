import pygame
from random import randrange, choice
import math
import tkinter as tk
from tkinter import messagebox

from classes.snake import Snake
from classes.square import Square

WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
RED = (255, 8, 0)


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

    def __init__(self, surface, width, height, rows, cols, colour, human_playing=True, timeout=500):
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

        self.resample = 20
        self.resample_limit = 50
        self.sample = [-1, -1]
        self.sample_repeat = 0

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
                           GREEN, self.squareHeight, self.squareWidth)

        self.snack = Square(snack_x, snack_y, 0, 0, RED, self.squareHeight, self.squareWidth)

        self.snake_snack_dist = math.sqrt((snake_x - snack_x)**2 + (snake_y - snack_y)**2)

    def redraw_surface(self):
        self.surface.fill((0, 0, 0))
        self.draw_grid()

        if self.human_playing:
            self.snake.update_dir_human()
            self.move_snake_human()
        else:
            self.snake.update_dir_ai(self.network, self.snack.x, self.snack.y, self.cols, self.rows)
            self.move_snake_ai()

        self.draw_snake()
        self.draw_snack()
        pygame.display.update()

    def draw_grid(self):
        for x in range(1, self.rows):
            pygame.draw.line(
                self.surface, WHITE, (0, x * self.squareHeight),
                (self.width, x * self.squareHeight))

        for y in range(1, self.cols):
            pygame.draw.line(
                self.surface, WHITE, (y * self.squareWidth, 0),
                (y * self.squareWidth, self.height))

    def move_snake_ai(self):
        self.snake.move()

        if self.count > self.timeout or not self.snake.valid() or not self.snake_inbounds():
            self.finished = True

        elif [self.snake.head.x, self.snake.head.y] == [self.snack.x, self.snack.y]:
            self.score += 100
            self.count = 0
            self.snake.addSquare()
            self.random_snack()

        else:
            new_dist = math.sqrt(
                (self.snake.head.x - self.snack.x)**2 + (self.snake.head.y - self.snack.y)**2)

            if new_dist > self.snake_snack_dist:
                self.score -= 3
            else:
                self.score += 2

            self.snake_snack_dist = new_dist

        if [self.snake.head.x, self.snake.head.y] == self.sample:
            self.resample = 0
            self.sample_repeat += 1

        elif self.resample == self.resample_limit:
            self.resample = 0
            self.sample_repeat = 0
            self.sample = [self.snake.head.x, self.snake.head.y]

        else:
            self.resample += 1

        if self.sample_repeat >= 3:
            self.score -= 100
            self.finished = True

        self.count += 1

    def move_snake_human(self):
        self.snake.move()

        if not self.snake.valid() or not self.snake_inbounds():
            message_box("You Died!", "Your final score was: {}, Start Over?".format(self.score))
            self.reset_game()

        elif [self.snake.head.x, self.snake.head.y] == [self.snack.x, self.snack.y]:
            self.score += 100
            self.snake.addSquare()
            self.random_snack()

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
