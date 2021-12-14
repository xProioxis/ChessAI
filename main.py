import pygame

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
piece_y_offset = 12.
board_border = [0, 1, 2, 3, 4, 5, 6, 7, 8, 16, 24, 32, 40, 48, 56, 15, 23, 31, 39, 47, 55, 63, 57, 58, 59, 60, 61, 62]

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


def inc(val, inc_val=1):
    try:
        val = int(val)
        return str(val + inc_val)

    except ValueError:
        return chr(ord(val) + inc_val)

def find_by_id(id):
    global square_list

    for square in square_list:
        if square.id == id:
            return square

    return None


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


def blit_highlight(square):
    pygame.draw.rect(WINDOW, YELLOW, (square.x, square.y, 10, 75))
    pygame.draw.rect(WINDOW, YELLOW, (square.x + 65, square.y, 10, 75))
    pygame.draw.rect(WINDOW, YELLOW, (square.x, square.y, 75, 10))
    pygame.draw.rect(WINDOW, YELLOW, (square.x, square.y + 65, 75, 10))



def square_selected():
    for square in square_list:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (square.x < mouse_x < square.x + 75) and (square.y < mouse_y < square.y + 75) and pygame.mouse.get_pressed()[0]:
            return True, square
    return False, None


def get_path(square):
    global square_list
    possible_spaces = []
    if square.piece.id == "bp": # pawn
        for new_square in square_list:
            if new_square.id == inc(square.id[0]) + square.id[1] and new_square.piece is None: # move in front
                possible_spaces.append(new_square)
            if square.id[0] == "2" and new_square.id == inc(square.id[0], 2) + square.id[1] and new_square.piece is None:
                possible_spaces.append(new_square)
            if (new_square.id == inc(square.id[0]) + inc(square.id[1]) or new_square.id == inc(square.id[0]) + inc(square.id[1], -1)) and new_square.piece is not None and new_square.piece.id[0] == "r":
                possible_spaces.append(new_square)

    elif square.piece.id == "bk": # knight
        # all possible movements that knight can take, creates list of ids of possible spaces
        knight_movements = [inc(square.id[0], 2) + inc(square.id[1], 1), inc(square.id[0], 2) + inc(square.id[1], -1),
                            inc(square.id[0], 1) + inc(square.id[1], 2), inc(square.id[0], 1) + inc(square.id[1], -2),
                            inc(square.id[0], -1) + inc(square.id[1], 2), inc(square.id[0], -1) + inc(square.id[1], -2),
                            inc(square.id[0], -2) + inc(square.id[1], 1), inc(square.id[0], -2) + inc(square.id[1], -1)]
        for new_square in square_list:
            if new_square.id in knight_movements:
                if new_square.piece is not None:
                    if new_square.piece.id[0] == "b":
                        continue
                possible_spaces.append(new_square)

    elif square.piece.id == "br": # rook
        curr_square = square_list.index(square)
        curr_square_save = curr_square

        # navigating up
        curr_square -= 1
        while 0 <= curr_square < len(square_list) and square_list[curr_square].id[1] == square.id[1]:
            if square_list[curr_square].piece is not None:
                if square_list[curr_square].piece.id[0] == "b":
                    break
                possible_spaces.append(square_list[curr_square])
                break
            if square_list[curr_square].id != square.id:
                possible_spaces.append(square_list[curr_square])

            curr_square -= 1
        curr_square = curr_square_save

        # navigating down
        curr_square += 1
        while 0 <= curr_square < len(square_list) and square_list[curr_square].id[1] == square.id[1]:
            if square_list[curr_square].piece is not None:
                if square_list[curr_square].piece.id[0] == "b":
                    break
                possible_spaces.append(square_list[curr_square])
                break
            if square_list[curr_square].id != square.id:
                possible_spaces.append(square_list[curr_square])

            curr_square += 1
        curr_square = curr_square_save

        # navigating left
        curr_square -= 8
        while 0 <= curr_square < len(square_list):
            if square_list[curr_square].piece is not None:
                if square_list[curr_square].piece.id[0] == "b":
                    break
                possible_spaces.append(square_list[curr_square])
                break
            if square_list[curr_square].id != square.id:
                possible_spaces.append(square_list[curr_square])

            curr_square -= 8
        curr_square = curr_square_save

        # navigating right
        curr_square += 8
        while 0 <= curr_square < len(square_list):
            if square_list[curr_square].piece is not None:
                if square_list[curr_square].piece.id[0] == "b":
                    break
                possible_spaces.append(square_list[curr_square])
                break
            if square_list[curr_square].id != square.id:
                possible_spaces.append(square_list[curr_square])

            curr_square += 8

    elif square.piece.id == "bb": # bishop
        curr_square = square_list.index(square)
        curr_square_save = curr_square
        possible_ids = []
        blocked_paths = []
        top_right = True
        top_left = True
        bottom_right = True
        bottom_left = True

        for i in range(1, 9):
            if top_right:
                new_square = find_by_id(inc(square.id[0], i) + inc(square.id[1], i))
                if new_square is not None:
                    if new_square.piece is not None:
                        if new_square.piece.id[0] == "b":
                            top_right = False
                        elif new_square.piece.id[0] == "r":
                            possible_spaces.append(new_square)
                            top_right = False
                    else:
                        possible_spaces.append(new_square)
                else: # if square doe not exists, path has gone off of board and will stop
                    top_right = False

            if top_left:
                new_square = find_by_id(inc(square.id[0], i) + inc(square.id[1], -i))
                if new_square is not None:
                    if new_square.piece is not None:
                        if new_square.piece.id[0] == "b":
                            top_left = False
                        elif new_square.piece.id[0] == "r":
                            possible_spaces.append(new_square)
                            top_left = False
                    else:
                        possible_spaces.append(new_square)
                else: # if square doe not exists, path has gone off of board and will stop
                    top_left = False

            if bottom_right:
                new_square = find_by_id(inc(square.id[0], -i) + inc(square.id[1], i))
                if new_square is not None:
                    if new_square.piece is not None:
                        if new_square.piece.id[0] == "b":
                            bottom_right = False
                        elif new_square.piece.id[0] == "r":
                            possible_spaces.append(new_square)
                            bottom_right = False
                    else:
                        possible_spaces.append(new_square)
                else: # if square doe not exists, path has gone off of board and will stop
                    bottom_right = False

            if bottom_left:
                new_square = find_by_id(inc(square.id[0], -i) + inc(square.id[1], -i))
                if new_square is not None:
                    if new_square.piece is not None:
                        if new_square.piece.id[0] == "b":
                            bottom_left = False
                        elif new_square.piece.id[0] == "r":
                            possible_spaces.append(new_square)
                            bottom_left = False
                    else:
                        possible_spaces.append(new_square)
                else: # if square doe not exists, path has gone off of board and will stop
                    bottom_left = False







        '''# navigating top right diagonally
        if curr_square % 8 != 0:
            curr_square += 7
            while 0 <= curr_square < len(square_list):
                if square_list[curr_square].piece is not None:
                    if square_list[curr_square].piece.id[0] == "b":
                        break
                    possible_spaces.append(square_list[curr_square])
                    break
                if square_list[curr_square].id != square.id:
                    possible_spaces.append(square_list[curr_square])

                curr_square += 7

            curr_square = curr_square_save


        # navigating top left diagonally
        curr_square -= 9
        while 0 <= curr_square < len(square_list):
            if square_list[curr_square].piece is not None:
                if square_list[curr_square].piece.id[0] == "b":
                    break
                possible_spaces.append(square_list[curr_square])
                break
            if square_list[curr_square].id != square.id:
                possible_spaces.append(square_list[curr_square])

            curr_square -= 9

        curr_square = curr_square_save

        # navigating bottom right diagonally
        curr_square += 9
        while 0 <= curr_square < len(square_list):
            if square.id[0] == "1": # if bishop is at the bottom of board, cannot move down
                break
            if square_list[curr_square].piece is not None:
                if square_list[curr_square].piece.id[0] == "b":
                    break
                possible_spaces.append(square_list[curr_square])
                break
            if square_list[curr_square].id != square.id:
                possible_spaces.append(square_list[curr_square])

                curr_square += 9

        curr_square = curr_square_save

        # navigating bottom left diagonally
        curr_square -= 7
        while 0 <= curr_square < len(square_list):
            if square.id[0] == "1": # if bishop is at the bottom of board, cannot move down
                break
            if square_list[curr_square].piece is not None:
                if square_list[curr_square].piece.id[0] == "b": # path stops once it encounters a piece
                    break
                possible_spaces.append(square_list[curr_square]) # can have a path onto one enemy
                break
            if square_list[curr_square].id != square.id:
                possible_spaces.append(square_list[curr_square])

                curr_square -= 7'''

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
            for square in get_path(square_active[1]): # will return the possible spaces a piece can move
                blit_highlight(square)
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

