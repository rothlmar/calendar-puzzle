from random import shuffle

def add_coords(a, b):
    return a[0] + b[0], a[1] + b[1]

pieces = [
    set(((0,1),(1,0),(1,1),(1,2),(2,1))),
    set(((0,0),(0,1),(1,0),(1,1))),
    set(((0,0),(0,1),(1,1),(2,1),(2,2))),
    set(((0,0),(0,1),(0,2),(1,0),(1,2))),
    set(((0,0),(0,1),(0,2),(1,1))),
    set(((0,0),(1,0),(1,1),(2,1))),
    set(((0,0),(1,0),(2,0),(3,0),(3,1))),
    set(((0,1),(1,0),(1,1),(2,0),(2,1))),
    set(((0,0),(1,0),(1,1),(1,2))),
]

months = {
    'jan': (0,0),
    'feb': (0,1),
    'mar': (0,2),
    'apr': (0,3),
    'may': (0,4),
    'jun': (0,5),
    'jul': (1,0),
    'aug': (1,1),
    'sep': (1,2),
    'oct': (1,3),
    'nov': (1,4),
    'dec': (1,5)
}

days = {
    1: (2,0),
    2: (2,1),
    3: (2,2),
    4: (2,3),
    5: (2,4),
    6: (2,5),
    7: (2,6),
    8: (3,0),
    9: (3,1),
    10: (3,2),
    11: (3,3),
    12: (3,4),
    13: (3,5),
    14: (3,6),
    15: (4,0),
    16: (4,1),
    17: (4,2),
    18: (4,3),
    19: (4,4),
    20: (4,5),
    21: (4,6),
    22: (5,0),
    23: (5,1),
    24: (5,2),
    25: (5,3),
    26: (5,4),
    27: (5,5),
    28: (5,6),
    29: (6,2),
    30: (6,3),
    31: (6,4)
}

def normalize_piece(coords):
    min_row = min(_[0] for _ in coords)
    min_col = min(_[1] for _ in coords)
    return frozenset([(_[0] - min_row, _[1] - min_col) for _ in coords])

def rotate_piece(coords):
    return normalize_piece([(_[1], -_[0]) for _ in coords])

def flip_piece(coords):
    return normalize_piece([(_[0], -_[1]) for _ in coords])

def variants(piece):
    v = [frozenset(piece)]
    for i in range(3):
        v.append(rotate_piece(v[-1]))
    for i in range(4):
        v.append(flip_piece(v[i]))
    return set(v)

piece_variants = [variants(p) for p in pieces]

def get_box_char(coord, shape):
    up = (coord[0] - 1, coord[1]) in shape
    down = (coord[0] + 1, coord[1]) in shape
    left = (coord[0], coord[1] - 1) in shape
    right = (coord[0], coord[1] + 1) in shape
    if up and down and left and right:
        return '╋'
    if up and down and left:
        return '┫'
    if up and down and right:
        return '┣'
    if left and right and up:
        return '┻'
    if left and right and down:
        return '┳'
    if left and right:
        return '━'
    if up and down:
        return '┃'
    if up and right:
        return '┗'
    if up and left:
        return '┛'
    if down and right:
        return '┏'
    if down and left:
        return '┓'
    if up:
        return '╹'
    if down:
        return '╻'
    if left:
        return '╸'
    if right:
        return '╺'
    return '╳'


def draw_box(board):
    template = [['.' if (row, col) in board.all_coords else ' ' for col in range(7)] for row in range(7)]    
    for index, val in enumerate(board.pieces.items()):
        anchor = val[0]
        shape = val[1]
        for c in shape:
            coord = add_coords(c, anchor)
            template[coord[0]][coord[1]] = get_box_char(c, shape)
    return '\n'.join([''.join(_) for _ in template])

def draw(board):
    emoji = ['⚫','⚪','🔴','🔵','🟢','🟡','🟠','🟣','🟤']
    template = [['🔲' if (row, col) in board.all_coords else '⬜' for col in range(7)] for row in range(7)] 
    for index, val in enumerate(board.pieces.items()):
        anchor = val[0]
        shape = val[1]
        for c in shape:
            coord = add_coords(c, anchor)
            template[coord[0]][coord[1]] = emoji[index]
    return '\n'.join([''.join(_) for _ in template])

    

class Board:
    def __init__(self):
        self.all_coords = self._get_coords()
        self.avail_coords = self.all_coords[:]
        self.pieces = dict()
        pass

    def clone(self):
        b = Board()
        b.avail_coords = self.avail_coords[:]
        b.pieces = dict(self.pieces)
        return b

    def empty(self, c):
        return c in self.avail_coords

    def does_fit(self, piece, coord):
        coords = [add_coords(coord, _) for _ in piece]
        for c in coords:
            if not self.empty(c):
                return False
        return True

    def place_piece(self, piece, coord):
        [self.avail_coords.remove(add_coords(coord, _)) for _ in piece]
        self.pieces[coord] = piece

    def _get_coords(self):
        c = [(a,b) for a in range(6) for b in range(7)]
        c.remove((0,6))
        c.remove((1,6))
        c.extend([(6,2), (6,3), (6,4)])
        return c

    def __str__(self):
        return ', '.join([str(_)  for _ in self.pieces])

class Game:
    def __init__(self):
        self.boards = [Board()]

    def solve(self, month, day):
        next_boards = []
        self.boards[0].avail_coords.remove(months[month])
        self.boards[0].avail_coords.remove(days[day])
        for piece_variant in piece_variants:
            print("piece: ", list(piece_variant)[0])
            for board in self.boards:
                for c in board.all_coords:
                    for p_v in piece_variant:
                        if board.does_fit(p_v, c):
                            next_board = board.clone()
                            next_board.place_piece(p_v,c)
                            next_boards.append(next_board)
            self.boards = next_boards
            next_boards = []
            print(f"boards: {len(self.boards)}")
            # for board in self.boards:
            #     print(draw(board) + "\n")
        return self.boards

    def solve_dfs_step(self, board, remaining_piece_variants):
        if len(remaining_piece_variants) == 0:
            return board
        for c in board.all_coords:
            for p_v in remaining_piece_variants[0]:
                if board.does_fit(p_v, c):
                    next_board = board.clone()
                    next_board.place_piece(p_v, c)
                    res = self.solve_dfs_step(next_board, remaining_piece_variants[1:])
                    if res:
                        return res


    def solve_dfs(self, month, day):
        board = Board()
        board.avail_coords.remove(months[month])
        board.avail_coords.remove(days[day])
        shuffled_pieces = piece_variants[:]
        shuffle(shuffled_pieces)
        return self.solve_dfs_step(board, shuffled_pieces)
        

    def solve_fast(self, month, day):
        next_boards = []
        self.boards[0].avail_coords.remove(months[month])
        self.boards[0].avail_coords.remove(days[day])
        for piece_variant in piece_variants[:4]:
            print("piece: ", list(piece_variant)[0])
            for board in self.boards:
                for c in board.all_coords:
                    for p_v in piece_variant:
                        if board.does_fit(p_v, c):
                            next_board = board.clone()
                            next_board.place_piece(p_v,c)
                            next_boards.append(next_board)
            filtered_next_boards = next_boards[:1]
            for board in next_boards[1:]:
                for filtered_board in filtered_next_boards:
                    if board.avail_coords == filtered_board.avail_coords:
                        break
                else:
                    filtered_next_boards.append(board)
            self.boards = filtered_next_boards
            next_boards = []
            print(f"boards: {len(self.boards)}")
            # for board in self.boards:
            #     print(draw(board) + "\n")
        return self.boards
