#!/usr/bin/env python

from sys import argv
from ohno.utils import grid_from_file
from ohno.board import Board

b = Board(grid_from_file(argv[1]))
b.draw()
print 'solving...'
b.solve()
b.draw()
