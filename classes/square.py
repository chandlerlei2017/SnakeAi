import pygame


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
