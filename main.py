import time

import pygame

pygame.init()
pygame.font.init()
WINDOW = pygame.display.set_mode((800, 600))
pygame.display.set_caption('ChessAI')
font = pygame.font.SysFont('BebasNeue-Regular.ttf', 40)

BLACK = (0, 0, 0)
RED = (255, 87, 51)
WHITE = (255, 255, 255)
GRAY = (105, 105, 105)
YELLOW = (255, 240, 31)

square_list = [] # will act as the main board
side_square_list = []
piece_list = []

piece_x_offset = 10
piece_y_offset = 12
side_piece_offset_x = 10
side_piece_offset_y = 12
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

pygame.display.set_icon(red_knight_img)

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


def find_by_id(id, board):
    for square in board:
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


def make_side_squares():
    global side_square_list, GRAY
    curr_num = "1"
    curr_letter = "a"
    for y in range(15, 115, 50):
        for x in range(0, 176, 25):
            side_square_list.append(Square(curr_num + curr_letter, x, y, GRAY))
            inc(curr_letter)
        inc(curr_num)

    curr_num = "3"
    curr_letter = "a"
    for y in range(500, 600, 50):
        for x in range(0, 176, 25):
            side_square_list.append(Square(curr_num + curr_letter, x, y, GRAY))
            inc(curr_letter)
        inc(curr_num)


def blit_board():
    global RED, WHITE, square_list, side_square_list
    for square in square_list:
        pygame.draw.rect(WINDOW, square.color, (square.x, square.y, 75, 75))
        if square.piece is not None: # if there is a piece on the square
            WINDOW.blit(square.piece.img, [square.piece.x, square.piece.y])

    for square in side_square_list:
        pygame.draw.rect(WINDOW, square.color, (square.x, square.y, 25, 100))
        if square.piece is not None:  # if there is a piece on the square
            WINDOW.blit(pygame.transform.scale(square.piece.img, (40, 40)), [square.piece.x, square.piece.y])


def blit_highlight(square):
    pygame.draw.rect(WINDOW, YELLOW, (square.x, square.y, 10, 75))
    pygame.draw.rect(WINDOW, YELLOW, (square.x + 65, square.y, 10, 75))
    pygame.draw.rect(WINDOW, YELLOW, (square.x, square.y, 75, 10))
    pygame.draw.rect(WINDOW, YELLOW, (square.x, square.y + 65, 75, 10))


def update_side_panel(square):
    global side_square_list, side_piece_offset_x, side_piece_offset_y

    if square.piece is None:
        return

    if square.piece.id[0] == "r":
        idx = 16
    else:
        idx = 0

    while side_square_list[idx].piece is not None: # searching for the next empty square
        idx += 1
    side_square_list[idx].piece = Piece(square.piece.id, square.piece.img, side_square_list[idx].x - side_piece_offset_x, side_square_list[idx].y - side_piece_offset_y)


def square_selected():
    for square in square_list:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if square.piece is not None and square.piece.id[0] == "b" and (square.x < mouse_x < square.x + 75) and (square.y < mouse_y < square.y + 75) and pygame.mouse.get_pressed()[0]:
            return True, square
    return False, None


def swap_pieces(old_square, new_square):
    new_square.piece = Piece(old_square.piece.id, old_square.piece.img, new_square.x - piece_x_offset, new_square.y - piece_y_offset)
    old_square.piece = None


def get_path(square, board):
    global square_list
    possible_spaces = []
    if square.piece.id[1] == "p": # pawn
        # space in front
        if square.piece.id[0] == "b":
            new_square = find_by_id(inc(square.id[0]) + square.id[1], board)
        else:
            new_square = find_by_id(inc(square.id[0], -1) + square.id[1], board)
        if new_square is not None:
            if new_square.piece is None:
                possible_spaces.append(new_square)

        # the space 2 squares ahead can be added only if this is pawns first move
        # refactor this for red pawn
        if square.id[0] == "2" and square.piece.id[0] == "b" and new_square in possible_spaces:
            new_square = find_by_id(inc(square.id[0], 2) + square.id[1], board)
            if new_square.piece is None:
                possible_spaces.append(new_square)

        if square.id[0] == "7" and square.piece.id[0] == "r" and new_square in possible_spaces:
            new_square = find_by_id(inc(square.id[0], -2) + square.id[1], board)
            if new_square.piece is None:
                possible_spaces.append(new_square)


        # can move diagonally if piece is present
        if square.piece.id[0] == "b":
            new_square = find_by_id(inc(square.id[0]) + inc(square.id[1], -1), board)
        else:
            new_square = find_by_id(inc(square.id[0], -1) + inc(square.id[1], -1), board)
        if new_square is not None:
            if new_square.piece is not None:
                if new_square.piece.id[0] != square.piece.id[0]: # if a pawn of the opposite color is present
                    possible_spaces.append(new_square)

        if square.piece.id[0] == "b":
            new_square = find_by_id(inc(square.id[0]) + inc(square.id[1]), board)
        else:
            new_square = find_by_id(inc(square.id[0], -1) + inc(square.id[1]), board)
        if new_square is not None:
            if new_square.piece is not None:
                if new_square.piece.id[0] != square.piece.id[0]:
                    possible_spaces.append(new_square)


    elif square.piece.id[1] == "k": # knight
        # all possible movements that knight can take, creates list of ids of possible spaces
        knight_movements = [inc(square.id[0], 2) + inc(square.id[1], 1), inc(square.id[0], 2) + inc(square.id[1], -1),
                            inc(square.id[0], 1) + inc(square.id[1], 2), inc(square.id[0], 1) + inc(square.id[1], -2),
                            inc(square.id[0], -1) + inc(square.id[1], 2), inc(square.id[0], -1) + inc(square.id[1], -2),
                            inc(square.id[0], -2) + inc(square.id[1], 1), inc(square.id[0], -2) + inc(square.id[1], -1)]
        for new_square in square_list:
            if new_square.id in knight_movements:
                if new_square.piece is not None:
                    if new_square.piece.id[0] == square.piece.id[0]:
                        continue
                possible_spaces.append(new_square)

    elif square.piece.id[1] == "r": # rook
        up = True
        left = True
        right = True
        down = True

        for i in range(1, 9):
            if up:
                new_square = find_by_id(inc(square.id[0], i) + square.id[1], board)
                if new_square is not None:
                    if new_square.piece is not None:
                        if new_square.piece.id[0] == square.piece.id[0]:
                            up = False
                        else:
                            possible_spaces.append(new_square)
                            up = False
                    else:
                        possible_spaces.append(new_square)
                else:  # if square doe not exists, path has gone off of board and will stop
                    up = False

            if down:
                new_square = find_by_id(inc(square.id[0], -i) + square.id[1], board)
                if new_square is not None:
                    if new_square.piece is not None:
                        if new_square.piece.id[0] == square.piece.id[0]:
                            down = False
                        else:
                            possible_spaces.append(new_square)
                            down = False
                    else:
                        possible_spaces.append(new_square)
                else:  # if square doe not exists, path has gone off of board and will stop
                    down = False

            if left:
                new_square = find_by_id(square.id[0] + inc(square.id[1], -i), board)
                if new_square is not None:
                    if new_square.piece is not None:
                        if new_square.piece.id[0] == square.piece.id[0]:
                            left = False
                        else:
                            possible_spaces.append(new_square)
                            left = False
                    else:
                        possible_spaces.append(new_square)
                else:  # if square doe not exists, path has gone off of board and will stop
                    left = False

            if right:
                new_square = find_by_id(square.id[0] + inc(square.id[1], i), board)
                if new_square is not None:
                    if new_square.piece is not None:
                        if new_square.piece.id[0] == square.piece.id[0]:
                            right = False
                        else:
                            possible_spaces.append(new_square)
                            right = False
                    else:
                        possible_spaces.append(new_square)
                else:  # if square doe not exists, path has gone off of board and will stop
                    right = False


    elif square.piece.id[1] == "b": # bishop
        top_right = True
        top_left = True
        bottom_right = True
        bottom_left = True

        for i in range(1, 9):
            if top_right:
                new_square = find_by_id(inc(square.id[0], i) + inc(square.id[1], i), board)
                if new_square is not None:
                    if new_square.piece is not None:
                        if new_square.piece.id[0] == square.piece.id[0]:  # if opposing piece is of same color
                            top_right = False
                        else:
                            possible_spaces.append(new_square)
                            top_right = False
                    else:
                        possible_spaces.append(new_square)
                else: # if square does not exists, path has gone off of board and will stop
                    top_right = False

            if top_left:
                new_square = find_by_id(inc(square.id[0], i) + inc(square.id[1], -i), board)
                if new_square is not None:
                    if new_square.piece is not None:
                        if new_square.piece.id[0] == square.piece.id[0]:
                            top_left = False
                        else:
                            possible_spaces.append(new_square)
                            top_left = False
                    else:
                        possible_spaces.append(new_square)
                else: # if square doe not exists, path has gone off of board and will stop
                    top_left = False

            if bottom_right:
                new_square = find_by_id(inc(square.id[0], -i) + inc(square.id[1], i), board)
                if new_square is not None:
                    if new_square.piece is not None:
                        if new_square.piece.id[0] == square.piece.id[0]:
                            bottom_right = False
                        else:
                            possible_spaces.append(new_square)
                            bottom_right = False
                    else:
                        possible_spaces.append(new_square)
                else: # if square doe not exists, path has gone off of board and will stop
                    bottom_right = False

            if bottom_left:
                new_square = find_by_id(inc(square.id[0], -i) + inc(square.id[1], -i), board)
                if new_square is not None:
                    if new_square.piece is not None:
                        if new_square.piece.id[0] == square.piece.id[0]:
                            bottom_left = False
                        else:
                            possible_spaces.append(new_square)
                            bottom_left = False
                    else:
                        possible_spaces.append(new_square)
                else: # if square doe not exists, path has gone off of board and will stop
                    bottom_left = False

    elif square.piece.id[1] == "q": # queen
        top_right = True
        top_left = True
        bottom_right = True
        bottom_left = True
        up = True
        left = True
        right = True
        down = True

        for i in range(1, 9):
            if top_right:
                new_square = find_by_id(inc(square.id[0], i) + inc(square.id[1], i), board)
                if new_square is not None:
                    if new_square.piece is not None:
                        if new_square.piece.id[0] == square.piece.id[0]: # if opposing piece is of same color
                            top_right = False
                        else:
                            possible_spaces.append(new_square)
                            top_right = False
                    else:
                        possible_spaces.append(new_square)
                else:  # if square doe not exists, path has gone off of board and will stop
                    top_right = False

            if top_left:
                new_square = find_by_id(inc(square.id[0], i) + inc(square.id[1], -i), board)
                if new_square is not None:
                    if new_square.piece is not None:
                        if new_square.piece.id[0] == square.piece.id[0]:
                            top_left = False
                        else:
                            possible_spaces.append(new_square)
                            top_left = False
                    else:
                        possible_spaces.append(new_square)
                else:  # if square doe not exists, path has gone off of board and will stop
                    top_left = False

            if bottom_right:
                new_square = find_by_id(inc(square.id[0], -i) + inc(square.id[1], i), board)
                if new_square is not None:
                    if new_square.piece is not None:
                        if new_square.piece.id[0] == square.piece.id[0]:
                            bottom_right = False
                        else:
                            possible_spaces.append(new_square)
                            bottom_right = False
                    else:
                        possible_spaces.append(new_square)
                else:  # if square doe not exists, path has gone off of board and will stop
                    bottom_right = False

            if bottom_left:
                new_square = find_by_id(inc(square.id[0], -i) + inc(square.id[1], -i), board)
                if new_square is not None:
                    if new_square.piece is not None:
                        if new_square.piece.id[0] == square.piece.id[0]:
                            bottom_left = False
                        else:
                            possible_spaces.append(new_square)
                            bottom_left = False
                    else:
                        possible_spaces.append(new_square)
                else:  # if square doe not exists, path has gone off of board and will stop
                    bottom_left = False

            if up:
                new_square = find_by_id(inc(square.id[0], i) + square.id[1], board)
                if new_square is not None:
                    if new_square.piece is not None:
                        if new_square.piece.id[0] == square.piece.id[0]:
                            up = False
                        else:
                            possible_spaces.append(new_square)
                            up = False
                    else:
                        possible_spaces.append(new_square)
                else:  # if square doe not exists, path has gone off of board and will stop
                    up = False

            if down:
                new_square = find_by_id(inc(square.id[0], -i) + square.id[1], board)
                if new_square is not None:
                    if new_square.piece is not None:
                        if new_square.piece.id[0] == square.piece.id[0]:
                            down = False
                        else:
                            possible_spaces.append(new_square)
                            down = False
                    else:
                        possible_spaces.append(new_square)
                else:  # if square doe not exists, path has gone off of board and will stop
                    down = False

            if left:
                new_square = find_by_id(square.id[0] + inc(square.id[1], -i), board)
                if new_square is not None:
                    if new_square.piece is not None:
                        if new_square.piece.id[0] == square.piece.id[0]:
                            left = False
                        else:
                            possible_spaces.append(new_square)
                            left = False
                    else:
                        possible_spaces.append(new_square)
                else:  # if square doe not exists, path has gone off of board and will stop
                    left = False

            if right:
                new_square = find_by_id(square.id[0] + inc(square.id[1], i), board)
                if new_square is not None:
                    if new_square.piece is not None:
                        if new_square.piece.id[0] == square.piece.id[0]:
                            right = False
                        else:
                            possible_spaces.append(new_square)
                            right = False
                    else:
                        possible_spaces.append(new_square)
                else:  # if square doe not exists, path has gone off of board and will stop
                    right = False

    elif square.piece.id[1] == "K":  # King

        # values to increment id by
        around_piece = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]

        for incs in around_piece:
            new_square = find_by_id(inc(square.id[0], incs[0]) + inc(square.id[1], incs[1]), board)
            if new_square is not None:
                if new_square.piece is not None:
                    if new_square.piece.id[0] != square.piece.id[0]:
                        possible_spaces.append(new_square)
                else:
                    possible_spaces.append(new_square)

    return tuple(possible_spaces)


def in_check(board):
    for new_square in board:
        if new_square.piece is not None:
            for path in get_path(new_square, board):
                if path.piece is not None and path.piece.id[1] == "K":
                    return path.piece.id[0]
    return "n"


def simulate_board(old_square, new_square, board):
    new_board = []
    for itr_square in board:
        curr_square = Square(itr_square.id, itr_square.x, itr_square.y, itr_square.color)
        if itr_square.piece is not None:
            curr_square.piece = Piece(itr_square.piece.id, itr_square.piece.img, itr_square.piece.x, itr_square.piece.y)
        new_board.append(curr_square)

    swap_pieces(find_by_id(old_square.id, new_board), find_by_id(new_square.id, new_board))
    '''for i in range(len(board)):
        print("=======================================================")
        if board[i].piece is not None:
            print("old", board[i].id, board[i].piece.id)
        else:
            print("old", board[i].id)
        if new_board[i].piece is not None:
            print("new", new_board[i].id, new_board[i].piece.id)
        else:
            print("new", new_board[i].id)'''
    return tuple(new_board)


def checkmate(id, board):
    for itr_square in board:
        if itr_square.piece is not None and itr_square.piece.id[0] == id:
            for path in get_path(itr_square, board):
                if in_check(simulate_board(itr_square, path, board)) != id:
                    return False

    return True


def game_over(winner):
    global font
    on_end_screen = True
    while on_end_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on_end_screen = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    on_end_screen = False
        blit_board()
        checkmate_text = font.render("Checkmate!", True, BLACK)
        game_over_text = font.render(winner + " Wins!", True, BLACK)
        WINDOW.blit(checkmate_text, (20, 275))
        WINDOW.blit(game_over_text, (22.5, 300))
        pygame.display.update()

    pygame.quit()

def AI_Player():
    global square_list
    if not checkmate("r", square_list):
        for new_square in square_list:
            if new_square.piece is not None and new_square.piece.id[0] == "r":
                for path in get_path(new_square, square_list):
                    if path.piece is not None and square.piece.id[1] == "K":
                        continue
                    if path.piece is not None:
                        update_side_panel(path)
                        swap_pieces(new_square, path)
                        return
        return
    else:
        game_over("Black")
        return


make_squares()
make_side_squares()
# for i in range(len(square_list)):
#   print(square_list[i].id, square_list[i].x, square_list[i].y, square_list[i].color)


running = True
square_active = False, None
human_playing = True
while running:
    WINDOW.fill(GRAY)
    blit_board()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    if human_playing:
        if not checkmate("b", square_list):
            if square_active[0]: # if a square is currently being clicked
                if square_active[1].piece is not None:
                    for square in get_path(square_active[1], square_list): # will return the possible spaces a piece can move
                        blit_highlight(square)
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if (square.x < mouse_x < square.x + 75) and (square.y < mouse_y < square.y + 75) and pygame.mouse.get_pressed()[0]:
                            if square.piece is not None and square.piece.id[1] == "K":
                                continue
                            if in_check(simulate_board(square_active[1], square, square_list)) != "b":
                                update_side_panel(square)
                                swap_pieces(square_active[1], square)
                                square_active = False, None
                                human_playing = False
                                time.sleep(.1)
                                break

                if pygame.mouse.get_pressed()[2]:
                    square_active = False, None
            else:
                square_active = square_selected() # will determine if square is being clicked
        else:
            game_over("Red")

    else:
        AI_Player()
        human_playing = True



    pygame.display.update()

