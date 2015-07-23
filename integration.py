from match3 import *
import unittest

def clear3to6Matches(board):
    board6 = removeMatches(6, board)
    board5 = removeMatches(5, board)
    board4 = removeMatches(4, board)
    board3 = removeMatches(3, board)
    board = combineBoards(board6, board5)
    board = combineBoards(board, board4)
    board = combineBoards(board, board3)
    return board

class IntegrationTests(unittest.TestCase):
    def test_whatever(self):
        print "\n"
        board = createEmptyBoard(6)
        board = fillEmptyCells(board, 1, 4)
        print boardToString(board)
        board = clear3to6Matches(board)
        print boardToString(board)
        board = slideDownToFill( board)
        print boardToString(board)
        board = clear3to6Matches(board)
        print boardToString(board)
