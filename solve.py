#!/usr/bin/env python

from sys import argv
from pprint import pprint
from board import Board

def grid_from_file(filename):
    grid = []
    with open(filename) as f:
        for line in f.readlines():
            grid.append(map(lambda x: int(x) if x.isdigit() else x, line.rstrip()))
    return grid

b = Board(grid_from_file(argv[1]))
b.draw()
print 'solving...'
b.solve()
b.draw()
