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

def hasMatchesLeft( board):
    matchesLeft = sum(zip(*countMatches(3, board))[1])
    return matchesLeft != 0

class IntegrationTests(unittest.TestCase):
    def test_variousBoardOperations(self):
        board = createEmptyBoard(6)
        board = fillEmptyCells(board, 1, 4)
        #print boardToString(board)
        board = clear3to6Matches(board)
        #print boardToString(board)
        board = slideDownToFill( board)
        #print boardToString(board)
        board = clear3to6Matches(board)
        print "various operations:\n" + boardToString(board)
    def test_clearAndSlideMatchesUntilNoneLeft(self):
        board = createEmptyBoard(6)
        board = fillEmptyCells(board, 1, 4)
        board = clear3to6Matches(board)
        board = slideDownToFill(board)
        while hasMatchesLeft(board):
            board = clear3to6Matches(board)
            board = slideDownToFill(board)
        print "fully slid:\n" + boardToString(board)
    def test_hasMatchesLeft_returnsFalseByDefault(self):
        given = [[1,2,3], [4,5,6],[ 7,8,9]]
        self.assertFalse( hasMatchesLeft(given))

if __name__ == '__main__':
    unittest.main()
