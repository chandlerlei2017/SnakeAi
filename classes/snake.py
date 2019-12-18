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
            (0, -1): "U",
            (1, 0): "R",
            (0, 1): "D",
            (-1, 0): "L"
        }
        curr_dir = dir_mapping[(self.head.dir_x, self.head.dir_y)]

        body_pos = list(map(lambda square: (square.x, square.y), self.body))
        body_pos = list(filter(lambda square: (self.head.x, self.head.y) != square, body_pos))

        s_u = s_ur = s_r = s_dr = s_d = s_dl = s_l = s_ul = 0

        if snack_x == self.head.x:
            if snack_y < self.head.y:
                s_u = 1
            elif snack_y > self.head.y:
                s_d = 1
        elif snack_y == self.head.y:
            if snack_x < self.head.x:
                s_l = 1
            elif snack_x > self.head.x:
                s_r = 1
        elif snack_y - self.head.y == self.head.x - snack_x:
            if snack_x > self.head.x:
                s_ur = 1
            elif snack_x < self.head.x:
                s_dl = 1
        elif snack_y - self.head.y == snack_x - self.head.x:
            if snack_y > self.head.y:
                s_dr = 1
            elif snack_y < self.head.y:
                s_ul = 1

        wall_u = 1 / (self.head.y + 1)
        wall_ur = 1 / min(self.head.y + 1, cols - self.head.x)
        wall_r = 1 / (cols - self.head.x)
        wall_dr = 1 / min(rows - self.head.y, cols - self.head.x)
        wall_d = 1 / (rows - self.head.y)
        wall_dl = 1 / min(self.head.x + 1, rows - self.head.y)
        wall_l = 1 / (self.head.x + 1)
        wall_ul = 1 / min(self.head.x + 1, self.head.y + 1)

        dir_snake = [0] * 8

        for square in body_pos:
            if square[0] == self.head.x:
                if square[1] < self.head.y:
                    dir_snake[0] = 1
                elif square[1] > self.head.y:
                    dir_snake[4] = 1
            elif square[1] == self.head.y:
                if square[0] < self.head.x:
                    dir_snake[6] = 1
                elif square[0] > self.head.x:
                    dir_snake[2] = 1
            elif square[1] - self.head.y == self.head.x - square[0]:
                if square[0] > self.head.x:
                    dir_snake[1] = 1
                elif square[0] < self.head.x:
                    dir_snake[5] = 1
            elif square[1] - self.head.y == square[0] - self.head.x:
                if square[1] > self.head.y:
                    dir_snake[3] = 1
                elif square[1] < self.head.y:
                    dir_snake[7] = 1

        if curr_dir == "U":
            snack_params = [s_u, s_ur, s_r, s_dr, s_d, s_dl, s_l, s_ul]
            wall_params = [wall_u, wall_ur, wall_r, wall_dr, wall_d, wall_dl, wall_l, wall_ul]
            snake_params = dir_snake

        elif curr_dir == "R":
            snack_params = [s_r, s_dr, s_d, s_dl, s_l, s_ul, s_u, s_ur]
            wall_params = [wall_r, wall_dr, wall_d, wall_dl, wall_l, wall_ul, wall_u, wall_ur]
            snake_params = dir_snake[2:] + dir_snake[:2]

        elif curr_dir == "L":
            snack_params = [s_l, s_ul, s_u, s_ur, s_r, s_dr, s_d, s_dl]
            wall_params = [wall_l, wall_ul, wall_u, wall_ur, wall_r, wall_dr, wall_d, wall_dl]
            snake_params = dir_snake[6:] + dir_snake[:6]

        elif curr_dir == "D":
            snack_params = [s_d, s_dl, s_l, s_ul, s_u, s_ur, s_r, s_dr]
            wall_params = [wall_d, wall_dl, wall_l, wall_ul, wall_u, wall_ur, wall_r, wall_dr]
            snake_params = dir_snake[4:] + dir_snake[:4]

        predict_input = snack_params + wall_params + snake_params

        res = network.predict(predict_input)

        if res.index(max(res)) == 1:
            temp = self.head.dir_y
            self.head.dir_y = - self.head.dir_x
            self.head.dir_x = temp

            self.turns[(self.head.x, self.head.y)] = [self.head.dir_x, self.head.dir_y]

        elif res.index(max(res)) == 2:
            temp = self.head.dir_y
            self.head.dir_y = self.head.dir_x
            self.head.dir_x = - temp

            self.turns[(self.head.x, self.head.y)] = [self.head.dir_x, self.head.dir_y]

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
