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

        directions = [[0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1]]
        clear = [[], [], [], [], [], [], [], []]

        for index, direction in enumerate(directions):
            head_x, head_y = self.head.x, self.head.y

            for count in range(4):
                head_x += direction[0]
                head_y += direction[1]

                clear[index].append(0 <= head_x <= cols - 1 and 0 <= head_y <=
                                    rows - 1 and (head_x, head_y) not in body_pos)

        # up_cond = self.head.y > 0 and (self.head.x, self.head.y - 1) not in body_pos
        # left_cond = self.head.x > 0 and (self.head.x - 1, self.head.y) not in body_pos
        # down_cond = self.head.y < rows - 1 and (self.head.x, self.head.y + 1) not in body_pos
        # right_cond = self.head.x < cols - 1 and (self.head.x + 1, self.head.y) not in body_pos

        snack_up = snack_y < self.head.y
        snack_left = snack_x < self.head.x
        snack_down = snack_y > self.head.y
        snack_right = snack_x > self.head.x

        if curr_dir == "R":
            # c_left = up_cond
            # c_right = down_cond
            # c_foward = right_cond

            s_left = snack_up
            s_foward = snack_right
            s_right = snack_down
            s_backward = snack_left

            c_l = clear[0]
            c_lf = clear[1]
            c_f = clear[2]
            c_rf = clear[3]
            c_r = clear[4]
            c_rb = clear[5]
            c_b = clear[6]
            c_lb = clear[7]

        elif curr_dir == "L":
            # c_left = down_cond
            # c_right = up_cond
            # c_foward = left_cond

            s_left = snack_down
            s_foward = snack_left
            s_right = snack_up
            s_backward = snack_right

            c_l = clear[4]
            c_lf = clear[5]
            c_f = clear[6]
            c_rf = clear[7]
            c_r = clear[0]
            c_rb = clear[1]
            c_b = clear[2]
            c_lb = clear[3]

        elif curr_dir == "U":
            # c_left = left_cond
            # c_right = right_cond
            # c_foward = up_cond

            s_left = snack_left
            s_foward = snack_up
            s_right = snack_right
            s_backward = snack_down

            c_l = clear[6]
            c_lf = clear[7]
            c_f = clear[0]
            c_rf = clear[1]
            c_r = clear[2]
            c_rb = clear[3]
            c_b = clear[4]
            c_lb = clear[5]

        elif curr_dir == "D":
            # c_left = right_cond
            # c_right = left_cond
            # c_foward = down_cond

            s_left = snack_right
            s_foward = snack_down
            s_right = snack_left
            s_backward = snack_up

            c_l = clear[2]
            c_lf = clear[3]
            c_f = clear[4]
            c_rf = clear[5]
            c_r = clear[6]
            c_rb = clear[7]
            c_b = clear[0]
            c_lb = clear[1]

        # res = network.predict(
        #     [
        #         int(c_foward),
        #         int(c_left),
        #         int(c_right),
        #         int(s_foward),
        #         int(s_left),
        #         int(s_right)])

        predict_input = [int(s_left), int(s_right), int(s_foward), int(s_backward)]
        predict_input += [int(x) for x in c_l]
        predict_input += [int(x) for x in c_lf]
        predict_input += [int(x) for x in c_f]
        predict_input += [int(x) for x in c_rf]
        predict_input += [int(x) for x in c_r]
        predict_input += [int(x) for x in c_rb]
        predict_input += [int(x) for x in c_b]
        predict_input += [int(x) for x in c_lb]

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
