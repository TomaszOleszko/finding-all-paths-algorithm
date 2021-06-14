import random
import pygame

SIZE = 1000
ROWS = 40
WIN = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption("Algorytm Drogowy")

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)


class Cube:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_WHITE(self):
        return self.color == WHITE

    def set_WHITE(self):
        self.color = WHITE

    def make_BLACK(self):
        self.color = BLACK

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbor(self, matrix):
        self.neighbors = []
        if self.row < self.total_rows - 1:  # Down
            self.neighbors.append(matrix[self.row + 1][self.col])

        if self.row < self.total_rows - 1 and self.col < self.total_rows - 1:
            self.neighbors.append(matrix[self.row + 1][self.col + 1])  # DOWN-RIGHT

        if self.row < self.total_rows - 1 and self.col > 0:
            self.neighbors.append(matrix[self.row + 1][self.col - 1])  # DOWN-LEFT

        if self.row > 0:  # UP
            self.neighbors.append(matrix[self.row - 1][self.col])

        if self.row > 0 and self.col < self.total_rows - 1:
            self.neighbors.append(matrix[self.row - 1][self.col + 1])  # UP-RIGHT

        if self.row > 0 and self.col > 0:
            self.neighbors.append(matrix[self.row - 1][self.col - 1])  # UP-LEFT

        if self.col < self.total_rows - 1:  # RIGHT
            self.neighbors.append(matrix[self.row][self.col + 1])

        if self.col > 0:  # LEFT
            self.neighbors.append(matrix[self.row][self.col - 1])


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def algorithm(draw, matrix, current, color):
    draw()
    current.color = color
    for neighbor in current.neighbors:
        if neighbor.is_WHITE():
            algorithm(draw, matrix, neighbor, color)

    return False


def make_matrix(rows, width):
    matrix = []
    gap = width // rows
    for i in range(rows):
        matrix.append([])
        for j in range(rows):
            cube = Cube(i, j, gap, rows)
            matrix[i].append(cube)

    return matrix


def fill_matrix(rows, width):
    matrix = make_matrix(rows, width)
    for i in range(rows):
        matrix.append([])
        for j in range(rows):
            if bool(random.getrandbits(1)):
                matrix[i][j].make_BLACK()

    return matrix


def draw_matrix(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, matrix, rows, width):
    win.fill(WHITE)

    for row in matrix:
        for cube in row:
            cube.draw(win)

    draw_matrix(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


def main(win, width, ROWS):
    matrix = fill_matrix(ROWS, width)

    start = None
    end = None

    run = True
    started = False
    while run:
        draw(win, matrix, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:  # left
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                cube = matrix[row][col]
                cube.make_BLACK()

            elif pygame.mouse.get_pressed()[2]:  # right
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                cube = matrix[row][col]
                cube.make_WHITE()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in matrix:
                        for cube in row:
                            cube.update_neighbor(matrix)

                    for row in matrix:
                        for cube in row:
                            if cube.color == WHITE:
                                algorithm(lambda: draw(win, matrix, ROWS, width), matrix, cube,
                                          (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200)))

    pygame.quit()


main(WIN, SIZE, ROWS)
