import math

# Screen size
WIDTH, HEIGHT = 800, 600

# Board rect (64, 64, 672, 472)
BOARD_X = BOARD_Y = 64
BOARD_W = WIDTH - BOARD_X * 2
BOARD_H = HEIGHT - BOARD_Y * 2

SUB_BOARD_ROW = SUB_BOARD_COLS = 3

COLORS = [
    (0,0,0),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,1,0),
    (1,0,1),
    (1,1,1),
    (.5,.5,.5)
]


def get_sub_board(row, col, max_row = SUB_BOARD_ROW, max_col = SUB_BOARD_COLS):
    return (
        BOARD_X + math.floor(BOARD_W / max_row) * row,
        BOARD_Y + math.floor(BOARD_H / max_col) * col,
        math.floor(BOARD_W / max_row),
        math.floor(BOARD_H / max_col)
    )    
def get_sub_boards(max_row = SUB_BOARD_ROW, max_col = SUB_BOARD_COLS):
    sub_boards = []
    for r in range(0, max_row):
        for c in range(0, max_col):
            get_sub_board(r, c)
            sub_boards.append(get_sub_board(r, c, max_row, max_col))
    return sub_boards

