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

def draw(board):
    coords = {v:k[0] for k,v in months.items()} | {v:str(k)[-1] for k,v in days.items()}
    template = [[coords.get((row,col),' ') for col in range(7)] for row in range(7)]
    template = [[' ' for col in range(7)] for row in range(7)]    
    for index, val in enumerate(board.pieces.items()):
        anchor = val[0]
        shape = val[1]
        for c in [add_coords(_, anchor) for _ in shape]:
            template[c[0]][c[1]] = str(index)
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
        # print(months[month], days[day])
        next_boards = []
        self.boards[0].avail_coords.remove(months[month])
        self.boards[0].avail_coords.remove(days[day])
        for piece_variant in piece_variants:
            print("piece: ", piece_variant[0])
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
        return self.boards

test_month = (0,2) # march
test_day = (6, 3) # 30
