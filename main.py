import pygame

pygame.init()
WINDOW = pygame.display.set_mode((800, 600))

BLACK = (0, 0, 0)
RED = (255, 87, 51)
WHITE = (255, 255, 255)

square_list = []
piece_list = []


class Square:
    def __init__(self, id, x, y, color):
        self.id = id
        self.x = x
        self.y = y
        self.color = color


class Piece:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color


def make_pieces():
    pass


def make_squares():
    global square_list, RED, WHITE
    id_letter = "a"
    is_white = True
    for col in range(200, 800, 75):
        id_num = 8
        for row in range(0, 600, 75):
            if id_num != 8:
                is_white = not is_white
            if is_white:
                curr_color = WHITE
            else:
                curr_color = RED

            new_id = f"{id_num}{id_letter}"
            square_list.append(Square(new_id, col, row, curr_color))
            id_num -= 1
        id_letter = chr(ord(id_letter) + 1)



def blit_board():
    global RED, WHITE, square_list
    for square in square_list:
        pygame.draw.rect(WINDOW, square.color, (square.x, square.y, 75, 75))
    pygame.display.update()


make_squares()
for i in range(len(square_list)):
    print(square_list[i].id, square_list[i].x, square_list[i].y, square_list[i].color)


running = True
while running:
    WINDOW.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    WINDOW.fill(BLACK)
    blit_board()
    pygame.display.update()

