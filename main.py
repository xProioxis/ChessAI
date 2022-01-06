import random
import time

import pygame

pygame.init()
pygame.font.init()
WINDOW = pygame.display.set_mode((800, 600))
pygame.display.set_caption('ChessAI')
font = pygame.font.SysFont('BebasNeue-Regular.ttf', 40)
small_font = pygame.font.SysFont('BebasNeue-Regular.ttf', 25)


BLACK = (0, 0, 0)
RED = (255, 87, 51)
WHITE = (255, 255, 255)
GREEN = (0, 97, 62)
YELLOW = (255, 240, 31)

square_list = [] # will act as the main board
side_square_list = []
piece_list = []
total_moves = 0

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
    def __init__(self, id, img, x, y, val):
        self.id = id
        self.img = img
        self.x = x
        self.y = y
        self.value = val


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


def percent_change(final_val, init_val):
    return ((final_val - init_val) / init_val)


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
                new_square.piece = Piece("rp", red_pawn_img, new_square.x - piece_x_offset, new_square.y - piece_y_offset, 1)
                pass
            elif new_square.id[0] == "2":
                new_square.piece = Piece("bp", black_pawn_img, new_square.x - piece_x_offset, new_square.y - piece_y_offset, 1)
                pass
            elif new_square.id == "1a" or new_square.id == "1h":
                new_square.piece = Piece("br", black_rook_img, new_square.x - piece_x_offset, new_square.y - piece_y_offset, 5)
                pass
            elif new_square.id == "8a" or new_square.id == "8h":
                new_square.piece = Piece("rr", red_rook_img, new_square.x - piece_x_offset, new_square.y - piece_y_offset, 5)
                pass
            elif new_square.id == "1c" or new_square.id == "1f":
                new_square.piece = Piece("bb", black_bishop_img, new_square.x - piece_x_offset, new_square.y - piece_y_offset, 3)
                pass
            elif new_square.id == "8c" or new_square.id == "8f":
                new_square.piece = Piece("rb", red_bishop_img, new_square.x - piece_x_offset, new_square.y - piece_y_offset, 3)
                pass
            elif new_square.id == "1b" or new_square.id == "1g":
                new_square.piece = Piece("bk", black_knight_img, new_square.x - piece_x_offset, new_square.y - piece_y_offset, 3)
                pass
            elif new_square.id == "8b" or new_square.id == "8g":
                new_square.piece = Piece("rk", red_knight_img, new_square.x - piece_x_offset, new_square.y - piece_y_offset, 3)
            elif new_square.id == "1e":
                new_square.piece = Piece("bK", black_king_img, new_square.x - piece_x_offset, new_square.y - piece_y_offset, 2)
            elif new_square.id == "8e":
                new_square.piece = Piece("rK", red_king_img, new_square.x - piece_x_offset, new_square.y - piece_y_offset, 10)
            elif new_square.id == "1d":
                new_square.piece = Piece("bq", black_queen_img, new_square.x - piece_x_offset, new_square.y - piece_y_offset, 9)
                pass
            elif new_square.id == "8d":
                new_square.piece = Piece("rq", red_queen_img, new_square.x - piece_x_offset, new_square.y - piece_y_offset, 9)
                pass
            square_list.append(new_square)

            id_num -= 1
        id_letter = chr(ord(id_letter) + 1)


def make_side_squares():
    global side_square_list, GREEN
    curr_num = "1"
    curr_letter = "a"
    for y in range(15, 115, 50):
        for x in range(0, 176, 25):
            side_square_list.append(Square(curr_num + curr_letter, x, y, GREEN))
            inc(curr_letter)
        inc(curr_num)

    curr_num = "3"
    curr_letter = "a"
    for y in range(500, 600, 50):
        for x in range(0, 176, 25):
            side_square_list.append(Square(curr_num + curr_letter, x, y, GREEN))
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

def blit_labels():
    letter = "a"
    for x in range(201, 801, 75):
        label = small_font.render(letter, True, BLACK)
        WINDOW.blit(label, [x, 585])
        letter = chr(ord(letter) + 1)

    num = 8
    for y in range(5, 605, 75):
        label = small_font.render(f"{num}", True, BLACK)
        WINDOW.blit(label, [200, y])
        num -= 1

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
    side_square_list[idx].piece = Piece(square.piece.id, square.piece.img, side_square_list[idx].x - side_piece_offset_x, side_square_list[idx].y - side_piece_offset_y, square.piece.value)


def square_selected():
    for square in square_list:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if square.piece is not None and square.piece.id[0] == "b" and (square.x < mouse_x < square.x + 75) and (square.y < mouse_y < square.y + 75) and pygame.mouse.get_pressed()[0]:
            return True, square
    return False, None


def swap_pieces(old_square, new_square):
    new_square.piece = Piece(old_square.piece.id, old_square.piece.img, new_square.x - piece_x_offset, new_square.y - piece_y_offset, old_square.piece.value)
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
        for new_square in board:
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
                else:  # if square does not exists, path has gone off of board and will stop
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
    result = []
    for new_square in board:
        if new_square.piece is not None:
            for path in get_path(new_square, board):
                if path.piece is not None and path.piece.id[1] == "K":
                    result.append(path.piece.id[0])
    return result


def simulate_board(old_square, new_square, board):
    # creates a hypothetical board if two pieces are switched
    new_board = []
    for itr_square in board:
        curr_square = Square(itr_square.id, itr_square.x, itr_square.y, itr_square.color)
        if itr_square.piece is not None:
            curr_square.piece = Piece(itr_square.piece.id, itr_square.piece.img, itr_square.piece.x, itr_square.piece.y, itr_square.piece.value)
        new_board.append(curr_square)

    if old_square is not None:
        swap_pieces(find_by_id(old_square.id, new_board), find_by_id(new_square.id, new_board))

    return tuple(new_board)


def checkmate(id, board):
    for itr_square in board:
        if itr_square.piece is not None and itr_square.piece.id[0] == id:
            for path in get_path(itr_square, board):
                if id not in in_check(simulate_board(itr_square, path, board)):
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


# update_side_panel(path)                  swap_pieces(new_square, path)

'''def predict_move(id, board):
    global total_moves
    if total_moves <= 3:
        opposite_pawns = []
        for itr_square in board:
            if itr_square.piece is not None and itr_square.piece.id[0] == id and itr_square.piece.id[1] == "p":
                opposite_pawns.append(itr_square)
            potential_moves = get_path(opposite_pawns[random.randint(0, len(opposite_pawns)-1)], board)
            return potential_moves[random.randint(0, len(potential_moves)-1)]
                
        best_move = None
        best_score = float("-inf")
        for itr_square in board:
            if itr_square.piece is not None and itr_square.piece.id[0] == "b":
                for path in get_path(itr_square, board):'''

def get_pieces_paths(id, board):
    possible_moves = []
    if checkmate(id, board) != id:
        for new_square in board:
            if new_square.piece is not None and new_square.piece.id[0] == id:
                for path in get_path(new_square, board):
                    if path.piece is not None and path.piece.id[1] == "K": # fix this to allow it to get out of check
                        continue
                    possible_moves.append([new_square, path])

    return possible_moves


def possible_king_spaces(enemy_id, board):
    friend_id = "r" if enemy_id == "b" else "b"
    sim_board = simulate_board(None, None, board)
    enemy_paths = get_pieces_paths(friend_id, sim_board)
    # king cannot move onto its own pieces
    # will use this loop to find king and to find pos of all other friendly pieces
    for king_square in sim_board:
        if king_square.piece is not None and king_square.piece.id == f"{enemy_id}K":
            break

    blocked_paths = []
    for path in enemy_paths:
        if path[0].piece.id[1] == "p":
            # pawns paths are ability to check is (for most cases) inconsistent with its path
            # can only check diagonally, so this must be manually done in this loop
            new_square = find_by_id(inc(path[0].id[0], -1) + inc(path[0].id[1], 1), sim_board)
            if new_square is not None:
                #print("blocked", new_square.id)
                blocked_paths.append(new_square)

            new_square = find_by_id(inc(path[0].id[0], -1) + inc(path[0].id[1], -1), sim_board)
            if new_square is not None:
                #print("blocked", new_square.id)
                blocked_paths.append(new_square)
        else:
            blocked_paths.append(path[1])

    for blocked_square in blocked_paths:
        if blocked_square.piece is not None and blocked_square.piece.id == f"{enemy_id}K":
            # cannot block the space king is on, will lead to inaccurate calculations
            continue
        blocked_square.id = "BLOCKED"

    search_queue = [king_square.id]
    king_square.id = "COUNTED"
    spaces_count = 0
    while len(search_queue) > 0:
        spaces_count += 1
        curr_id = search_queue.pop(0)
        #print(curr_id)
        search_area = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]
        # will search in a circle around current piece
        for inc_id in search_area: # increment id
            new_square = find_by_id(inc(curr_id[0], inc_id[0]) + inc(curr_id[1], inc_id[1]), sim_board)
            if new_square is not None:
                if new_square.piece is not None and new_square.piece.id[0] == "b":
                    continue
                search_queue.append(new_square.id)
                new_square.id = "COUNTED"

    #print("==========================================================================")
    return spaces_count


def endgame_mode(enemy_id, board):
    enemy_val = 0
    for itr_square in board:
        if itr_square.piece is not None and itr_square.piece.id[0] == enemy_id and itr_square.piece.id[1] != "K":
            enemy_val += itr_square.piece.value

    if enemy_val <= 5:
        print("ENDGAME")
        return True
    else:
        return False


def predict_best_move(id, board):
    # this section calculates the point advantage to moving pieces to certain spaces
    possible_moves = get_pieces_paths(id, board)
    best_move = None
    best_score = float("-inf")
    for x in range(len(possible_moves)):
        curr_score = 0

        if possible_moves[x][1].piece is None:  # initial values of moving, first instance of calculating choice value
            # curr_score += 0 - possible_moves[x][0].piece.value
            pass
        else:
            curr_score += possible_moves[x][1].piece.value - possible_moves[x][0].piece.value  # prioritizes moving least valuable pieces first

        if curr_score > best_score:
            best_score = curr_score
            best_move = possible_moves[x]

    if best_move[0].piece.id[1] == "p" and best_move[0].id[0] == "7" and best_score == -1:
        all_pawns = []
        for itr_square in possible_moves:
            if itr_square[0].piece.id == "rp":
                all_pawns.append(itr_square)

        random_num = random.randint(0, len(all_pawns) - 1)
        best_move = all_pawns[random_num]

    return best_move, best_score


def path_values(id, board):
    best_move = None
    best_move_total = float("-inf")
    check = False
    enemy_id = "b" if id == "r" else "r"
    equal_val_moves = []

    in_endgame = endgame_mode("b", board)
    if in_endgame:
        prev_king_spaces = possible_king_spaces("b", board)
    for itr_square in get_pieces_paths(id, board):
        potential_board = simulate_board(itr_square[0], itr_square[1], board)

        if id in in_check(board):
            # if currently in check, next move must get king out of check or else it wont be considered
            if in_check(potential_board) == id:
                continue

        if id in in_check(potential_board):  # cannot move into check, move will not be considered
            continue

        if enemy_id in in_check(potential_board):
            # check will add 5 to score if it does not result in piece being taken
            check = True
            curr_score = 0

        # curr_score gives determines the value of moving a piece to a certain space
        if checkmate(enemy_id, potential_board):
            curr_score = 1000
        elif itr_square[1].piece is None:  # initial values of moving, first instance of calculating choice value
            curr_score = 0 - itr_square[0].piece.value
        else:
            if itr_square[1].piece.id != "bK":
                curr_score = itr_square[1].piece.value - itr_square[0].piece.value  # prioritizes moving least valuable pieces first

        if in_endgame:
            curr_king_spaces = possible_king_spaces("b", potential_board)
            spaces_reduced_award = 10 * -percent_change(curr_king_spaces, prev_king_spaces)
            curr_score += spaces_reduced_award
            print(spaces_reduced_award, itr_square[0].piece.id)

        # the best move for the enemy to take after this potential move has been executed
        # second instance of calculating choice value

        if check:
            next_move = predict_best_move(enemy_id, simulate_board(itr_square[0], itr_square[1], board))
            if next_move[1] < 0: # must change this if it is decided that
                # if enemy is negatively affected by the check, the check will be valued, otherwise check has no value
                curr_score += 5

            check = False

        enemy_move = predict_best_move(enemy_id, simulate_board(itr_square[0], itr_square[1], board))
        curr_move_total = curr_score - enemy_move[1]

        if curr_move_total > best_move_total:
            best_move_total = curr_move_total
            best_move = itr_square
            equal_val_moves.clear()
            equal_val_moves.append([itr_square, best_move_total])
        elif curr_move_total == best_move_total:
            equal_val_moves.append([itr_square, best_move_total])

    if len(equal_val_moves) > 1:
        random_move = random.randint(0, len(equal_val_moves) - 1)
        return equal_val_moves[random_move][0], equal_val_moves[random_move][1]
    return best_move, best_move_total


def AI_Player():
    global square_list
    ai_possible_moves = []  # will contain all red pieces and their paths

    if not checkmate("r", square_list):
        # this section calculates the point advantage to moving pieces to certain spaces
        best_move = path_values("r", square_list)

        '''
        if best_move[0][0].piece.id[1] == "p" and best_move[0][0].id[0] == "7" and best_move[1] == 0:
                all_pawns = []
                for itr_square in square_list:
                    if itr_square[0].piece.id == "rp":
                        all_pawns.append(itr_square)
    
                random_num = random.randint(0, len(all_pawns) - 1)
                best_move = all_pawns[random_num]'''


        # best_move becomes the best combination of [current red piece,(and) next square for red piece to land on]
        update_side_panel(best_move[0][1])
        swap_pieces(best_move[0][0], best_move[0][1])
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
    WINDOW.fill(GREEN)
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
                            if square.piece is not None and square.piece.id == "rK":
                                continue
                            if "b" not in in_check(simulate_board(square_active[1], square, square_list)):
                                total_moves += 1
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

    blit_labels()



    pygame.display.update()

