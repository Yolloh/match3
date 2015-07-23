from match3 import *
import unittest

class IntegrationTests(unittest.TestCase):
    def test_whatever(self):
        print "\n"
        board = createEmptyBoard(6)
        board = fillEmptyCells(board, 1, 4)
        print boardToString(board)
        board = removeMatches(6, board)
        board = removeMatches(5, board)
        board = removeMatches(4, board)
        board = removeMatches(3, board)
        print boardToString(board)
