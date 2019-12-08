import pygame
white = (255, 255, 255)


class Board(object):
    def __init__(self, surface, width, height, rows, cols, colour):
        self.surface = surface
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.colour = colour
        self.snake = Snake

    def redraw_surface(self):
        self.surface.fill((0, 0, 0))
        self.draw_grid()
        self.draw_snake()
        self.draw_snack()
        pygame.display.update()

    def draw_grid(self):
        x_inc = self.width // self.cols
        y_inc = self.height // self.rows

        for x in range(1, self.rows):
            pygame.draw.line(self.surface, white, (x*x_inc, 0),
                             (x*x_inc, self.height))

        for y in range(1, self.cols):
            pygame.draw.line(self.surface, white, (0, y*y_inc),
                             (self.width, y*y_inc))

    def draw_snake(self):
        pass

    def draw_snack(self):
        pass


class Cube(object):
    def __init__(self):
        pass


class Snake(object):
    def __init__(self):
        pass


class Snack(Cube):
    def __init__(self):
        pass
