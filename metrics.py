import math
import pygame

# Screen size
WIDTH, HEIGHT = 800, 600

# Used for manage cards
CARD_WIDTH = 74
CARD_HEIGHT = 113
CARD_OFFSET = 15

# Board rect (64, 64, 672, 472)
BOARD_X = BOARD_Y = 64
BOARD_W = WIDTH - BOARD_X * 2
BOARD_H = HEIGHT - BOARD_Y * 2

# Used for split board
SUB_BOARD_ROW = SUB_BOARD_COLS = 3
def get_sub_board(row, col, max_row = SUB_BOARD_ROW, max_col = SUB_BOARD_COLS):
    return pygame.Rect(
        BOARD_X + math.floor(BOARD_W / max_row) * row,
        BOARD_Y + math.floor(BOARD_H / max_col) * col,
        math.floor(BOARD_W / max_row),
        math.floor(BOARD_H / max_col)
    )    
def get_player_boards():
    sub_boards = []
    for r in range(0, 3):
        for c in range(0, 3):
            sub_board = get_sub_board(r, c, 3, 3)
            if not (sub_board.x == sub_board.w + BOARD_X and sub_board.y == BOARD_Y):   
                sub_boards.append(sub_board)
    return sub_boards
def get_dealer_board():
    return get_sub_board(1, 0, 3, 3)