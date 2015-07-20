import itertools
import unittest
import random

def hasMatchOfExactLength(matchLength, row):
    groups = [(k, sum(1 for i in g)) for k,g in itertools.groupby(row)]
    for group in groups:
        if group[1] == matchLength:
            return True
    return False

def transposeBoard( board):
    return zip(*board)

def countMatchInRows(matchLength, board):
    count = 0
    for row in board:
        if hasMatchOfExactLength(matchLength, row):
            count += 1
    return count
    
def countMatchInColumns(matchLength, board):
    board = transposeBoard(board)
    return countMatchInRows(matchLength, board)

def countMatchThrees(board):
    return countMatchN(3, board)

def countMatchN(matchLength, board):
    if matchLength == 1:
        r = countMatchInRows(1, board)
        c = countMatchInColumns(1, board)
        return min(r,c)
    return countMatchInRows(matchLength, board) + countMatchInColumns(matchLength, board)

def createEmptyBoard( size):
   return [ [None]*size ] * size 

def fillEmptyCells( board, minVal, maxVal):
    rng = random.Random()
    result = []
    for row in board:
        newRow = []
        for cell in row:
            if cell == None:
                newRow.append( rng.randint(minVal, maxVal))
            else:
                newRow.append( cell)
        result.append( newRow)
    return result

def slideDownToFill( board):
    didWork, board = _slideDownOnce(board)
    while didWork:
        didWork, board = _slideDownOnce(board)
    return board

def _slideDownOnce( board):
    slideOccurred = False
    for rowIndex in range(0, len(board) - 1):
        slideOccurred, topRow, bottomRow = _slideDownRow( board[rowIndex], board[rowIndex+1])
        board[rowIndex] = topRow
        board[rowIndex+1] = bottomRow
    return (slideOccurred, board)

def _slideDownRow( topRow, bottomRow):
    slideOccurred = False
    newTopRow = []
    newBottomRow = []
    for topCell,bottomCell in zip(topRow, bottomRow):
        if bottomCell is None and topCell is not None:
            bottomCell = topCell
            topCell = None
            slideOccurred = True
        newTopRow.append( topCell)
        newBottomRow.append( bottomCell)
    return (slideOccurred, newTopRow, newBottomRow)

class Match3Tests( unittest.TestCase):
    def test_pinningOriginalBehavior(self):
        a = [ [ 1, 2, 3], 
              [ 1, 2, 4], 
              [ 1, 1, 1] ]
        b = [ [ 1, 2, 3, 4],
              [ 1, 2, 3, 4],
              [ 1, 2, 3, 4],
              [ 5, 6, 3, 8] ]
        self.assertEqual( countMatchThrees(a), 2)
        self.assertEqual( countMatchThrees(b), 3)
        self.assertEqual( countMatchN(2, a), 1)
        self.assertEqual( countMatchN(1, b), 3)
    def test_createEmptyBoard_fillsBoardWithNone(self):
        result = createEmptyBoard(3)
        for row in result:
            for cell in row:
                self.assertEqual( cell, None)
    def test_createEmptyBoard_hasCorrectNumberOfRowsAndColumns(self):
        result = createEmptyBoard(4)
        for row in result:
            self.assertEqual( len(row), 4)
        self.assertEqual(len(result), 4)
    def test_fillEmptyCells_leavesNoCellEmpty(self):
        given = [ [ 1, None],
                  [ None, 8] ]
        result = fillEmptyCells(given, 0, 3)
        for row in result:
            for cell in row:
                self.assertNotEqual( cell, None)
    def test_fillEmptyCells_usesMinToMaxInclusiveValues(self):
        given = createEmptyBoard(20)
        result = fillEmptyCells( given, 0, 3)
        observedValues = []
        for row in result:
            for cell in row:
                if cell not in observedValues:
                    observedValues.append(cell)
        observedValues.sort()
        self.assertListEqual( observedValues, [0, 1, 2, 3] )
    def test_slideDownToFill_slidesCellContentsDownwards_leavingEmptyCells(self):
        given = [ [ 1, 2, 3],
                  [ None, 4, 5],
                  [None, None, 6] ]
        result = slideDownToFill( given)
        print result
        self.assertListEqual( result[0], [None, None, 3])    
        self.assertListEqual( result[1], [None, 2, 5])
        self.assertListEqual( result[2], [1, 4, 6])    
    def test__slideDownRow(self):
        top = [ 1, 2]
        bottom = [ None, 3 ]
        occurred, top2, bottom2 = _slideDownRow( top, bottom)
        self.assertEqual(occurred, True)
        self.assertListEqual( top2, [ None, 2] )
        self.assertListEqual( bottom2, [1, 3])

if __name__ == '__main__':
    unittest.main()

