class Direction:
    WEST   = 'west'
    NORTH  = 'north'
    EAST   = 'east'
    SOUTH  = 'south'

    @classmethod
    def directions(cls):
        return [cls.WEST, cls.NORTH, cls.EAST, cls.SOUTH]

class Tile:
    BLOCKED   = '*'
    EMPTY     = '-'
    FILLED    = '='

    def __init__(self, value):
        self.value = value
        self.neighbors = {}
        for direction in Direction.directions():
            self.neighbors[direction] = None

    def __getitem__(self, direction):
        return self.neighbors[direction]

    def __setitem__(self, direction, tile):
        self.neighbors[direction] = tile

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return '[{}] sees {} tiles'.format(str(self.value), str(self.sees()))

    def clone(self):
        tile = Tile(self.value)
        for direction in Direction.directions():
            tile[direction] = self.neighbors[direction]
        return tile

    def blocked(self):
        return self.value == Tile.BLOCKED

    def known(self):
        return self.value not in [Tile.BLOCKED, Tile.EMPTY]

    def empty(self):
        return self.value == Tile.EMPTY

    def given(self):
        return self.value != Tile.FILLED and self.known()

    def surrounded(self):
        for direction in Direction.directions():
            if self.neighbors[direction] is not None and not self.neighbors[direction].blocked():
                return False
        return True

    def has(self, direction):
        return self.neighbors[direction] is not None

    def sees(self, direction=None):
        if direction is not None:
            sees = 0
            next = self
            while next.has(direction) and next[direction].known():
                sees += 1
                next = next[direction]
            return sees
        return sum([self.sees(direction) for direction in Direction.directions()])

    def max_sees(self, direction=None):
        if direction is not None:
            sees = 0
            next = self
            while next.has(direction) and not next[direction].blocked():
                sees += 1
                next = next[direction]
            return sees
        return sum([self.max_sees(direction) for direction in Direction.directions()])

    def first_empty(self, direction):
        next = self[direction]
        while next is not None and not next.empty():
            next = next[direction]
        return next

    def update(self, block=False):
        if self.value == Tile.EMPTY and block:
            self.value = Tile.BLOCKED
        elif self.value == Tile.EMPTY:
            self.value = Tile.FILLED

    def fill(self, amount, direction, add_block=False):
        next = self[direction]
        for _ in xrange(amount):
            next.update()
            next = next[direction]
        if add_block:
            next.update(True)

class Board:
    def __init__(self, grid):
        self.board = map(lambda row: map(lambda val: Tile(val), row), grid)
        for r, row in enumerate(self.board):
            for c, tile in enumerate(row):
                if c > 0:
                    tile[Direction.WEST] = self.board[r][c-1]
                if r > 0:
                    tile[Direction.NORTH] = self.board[r-1][c]
                if c + 1 < len(row):
                    tile[Direction.EAST] = self.board[r][c+1]
                if r + 1 < len(self.board):
                    tile[Direction.SOUTH] = self.board[r+1][c]

    def __getitem__(self, i):
        return self.board[i]

    def draw(self):
        print '~' * (len(self.board) * 2 - 1)
        for row in self.board:
            print ' '.join(map(str, row))
        print '~' * (len(self.board) * 2 - 1)

    def is_complete(self):
        for row in self.board:
            for tile in row:
                if tile.empty():
                    return False
        return True

    def is_correct(self):
        for row in self.board:
            for tile in row:
                if tile.given() and tile.value < tile.sees():
                    return False
                elif tile.known() and tile.surrounded():
                    return False
        return True

    def clone(self):
        grid = []
        for row in self.board:
            grid.append(map(lambda x: x.value, row))
        return Board(grid)

    def board_on_update(self, row, col, block=False):
        clone = self.clone()
        clone[row][col].update(block)
        return clone

    def fill_via_contrapositive(self):
        for r, row in enumerate(self.board):
            for c, tile in enumerate(row):
                if tile.empty():
                    if not self.board_on_update(r, c).is_correct():
                        tile.update(True)
                    elif not self.board_on_update(r, c, True).is_correct():
                        tile.update()

    def fill_via_counting(self):
        for r, row in enumerate(self.board):
            for c, tile in enumerate(row):
                if tile.given():
                    for direction in Direction.directions():
                        amount = tile.value - sum([tile.max_sees(d) for d in Direction.directions() if d != direction])
                        tile.fill(amount, direction)

    def solve(self, iterations=0):
        if iterations == 0:
            while not self.is_complete():
                self.fill_via_contrapositive()
                self.fill_via_counting()
        else:
            for _ in xrange(iterations):
                if not self.is_complete():
                    self.fill_via_contrapositive()
                    self.fill_via_counting()
                else:
                    return