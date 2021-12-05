import pygame
import time

pygame.init()
WINDOW = pygame.display.set_mode((800, 600))

BLACK = (0, 0, 0)
RED = (255, 87, 51)
WHITE = (255, 255, 255)
GRAY = (105, 105, 105)
YELLOW = (255, 240, 31)

square_list = []
piece_list = []

piece_x_offset = 10
piece_y_offset = 12.5

black_pawn_img = pygame.image.load('Assets/BlackPawn.png')
red_pawn_img = pygame.image.load('Assets/RedPawn.png')
black_rook_img = pygame.image.load('Assets/BlackRook.png')
red_rook_img = pygame.image.load('Assets/RedRook.png')
black_bishop_img = pygame.image.load('Assets/BlackBishop.png')
red_bishop_img = pygame.image.load('Assets/RedBishop.png')
black_knight_img = pygame.image.load('Assets/BlackKnight.png')
red_knight_img = pygame.image.load('Assets/RedKnight.png')
black_king_img = pygame.image.load('Assets/BlackKing.png')
red_king_img = pygame.image.load('Assets/RedKing.png')
black_queen_img = pygame.image.load('Assets/BlackQueen.png')
red_queen_img = pygame.image.load('Assets/RedQueen.png')


class Square:
    piece = None

    def __init__(self, id, x, y, color):
        self.id = id
        self.x = x
        self.y = y
        self.color = color


class Piece:
    def __init__(self, id, img, x, y):
        self.id = id
        self.img = img
        self.x = x
        self.y = y


def make_pieces():
    pass


def make_squares():
    global square_list, RED, WHITE, pawn_img, piece_x_offset, piece_y_offset
    id_letter = "a"
    is_white = True
    # defining squares and their methods
    for col in range(200, 800, 75):
        id_num = 8
        for row in range(0, 600, 75):
            if id_num != 8:
                is_white = not is_white # will switch color of square and ensure the same color is never adjacent
            if is_white:
                curr_color = WHITE
            else:
                curr_color = RED

            new_id = f"{id_num}{id_letter}"
            new_square = Square(new_id, col, row, curr_color)

            # setting pieces for each square on board
            # piece id is formatted as "(piece color)(piece type)"
            if new_square.id[0] == "7":
                new_square.piece = Piece("rp", red_pawn_img, new_square.x - piece_x_offset, new_square.y - piece_y_offset)
            elif new_square.id[0] == "2":
                new_square.piece = Piece("bp", black_pawn_img, new_square.x - piece_x_offset, new_square.y - piece_y_offset)
            elif new_square.id == "1a" or new_square.id == "1h":
                new_square.piece = Piece("br", black_rook_img, new_square.x - piece_x_offset, new_square.y - piece_y_offset)
            elif new_square.id == "8a" or new_square.id == "8h":
                new_square.piece = Piece("rr", red_rook_img, new_square.x - piece_x_offset, new_square.y - piece_y_offset)
            elif new_square.id == "1c" or new_square.id == "1f":
                new_square.piece = Piece("bb", black_bishop_img, new_square.x - piece_x_offset, new_square.y - piece_y_offset)
            elif new_square.id == "8c" or new_square.id == "8f":
                new_square.piece = Piece("rb", red_bishop_img, new_square.x - piece_x_offset, new_square.y - piece_y_offset)
            elif new_square.id == "1b" or new_square.id == "1g":
                new_square.piece = Piece("bk", black_knight_img, new_square.x - piece_x_offset, new_square.y - piece_y_offset)
            elif new_square.id == "8b" or new_square.id == "8g":
                new_square.piece = Piece("rk", red_knight_img, new_square.x - piece_x_offset, new_square.y - piece_y_offset)
            elif new_square.id == "1e":
                new_square.piece = Piece("bK", black_king_img, new_square.x - piece_x_offset, new_square.y - piece_y_offset)
            elif new_square.id == "8e":
                new_square.piece = Piece("rK", red_king_img, new_square.x - piece_x_offset, new_square.y - piece_y_offset)
            elif new_square.id == "1d":
                new_square.piece = Piece("bq", black_queen_img, new_square.x - piece_x_offset, new_square.y - piece_y_offset)
            elif new_square.id == "8d":
                new_square.piece = Piece("rq", red_queen_img, new_square.x - piece_x_offset, new_square.y - piece_y_offset)

            square_list.append(new_square)

            id_num -= 1
        id_letter = chr(ord(id_letter) + 1)


def blit_board():
    global RED, WHITE, square_list
    for square in square_list:
        pygame.draw.rect(WINDOW, square.color, (square.x, square.y, 75, 75))
        if square.piece is not None: # if there is a piece on the square
            WINDOW.blit(square.piece.img, [square.piece.x, square.piece.y])



def square_selected():
    for square in square_list:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (square.x < mouse_x < square.x + 75) and (square.y < mouse_y < square.y + 75) and pygame.mouse.get_pressed()[0]:
            return True, square
    return False, None


def get_path(square):
    global square_list
    possible_spaces = []
    if square.piece.id == "bp":
        new_ids = [str(int(square.id[0]) + 1) + square.id[1]]
        for new_square in square_list:
            if new_square.id in new_ids and new_square.piece is None:
                possible_spaces.append(new_square)

    return tuple(possible_spaces)


make_squares()
for i in range(len(square_list)):
    print(square_list[i].id, square_list[i].x, square_list[i].y, square_list[i].color)


running = True
square_active = False, None
while running:
    WINDOW.fill(GRAY)
    blit_board()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    if square_active[0]: # if a square is currently being clicked
        if square_active[1].piece is not None:
            for square in get_path(square_active[1]): # will return the possible space a piece can move
                pygame.draw.rect(WINDOW, YELLOW, (square.x, square.y, 75, 75))
                if square.piece is not None:
                    WINDOW.blit(square.piece.img, (square.x, square.y, square.x - piece_x_offset, square.y - piece_y_offset))

                mouse_x, mouse_y = pygame.mouse.get_pos()
                if (square.x < mouse_x < square.x + 75) and (square.y < mouse_y < square.y + 75) and pygame.mouse.get_pressed()[0]:
                    square.piece = Piece(square_active[1].piece.id, square_active[1].piece.img, square.x - piece_x_offset, square.y - piece_y_offset)
                    square_active[1].piece = None
                    square_active = False, None
                    break
        if pygame.mouse.get_pressed()[2]:
            square_active = False, None
    else:
        square_active = square_selected() # will determine if square is being clicked





    pygame.display.update()

