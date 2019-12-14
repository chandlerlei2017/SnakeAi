import pygame
from classes.square import Square

GREEN = (34, 139, 34)


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
        body_pos = list(map(lambda square: (square.x, square.y), self.body))

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
                                prev_square.dir_x, prev_square.dir_y, GREEN, self.square_height, self.square_width))
