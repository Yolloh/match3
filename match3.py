import itertools
import unittest
import random

def hasMatchOfExactLength(matchLength, row):
    groups = [(k, sum(1 for i in g)) for k,g in itertools.groupby(row)]
    for group in groups:
        if group[1] == matchLength and group[0] is not None:
            return True
    return False

def _transposeBoard( board):
    return [list(i) for i in zip(*board)]

def countMatchInRows(matchLength, board):
    count = 0
    for row in board:
        if hasMatchOfExactLength(matchLength, row):
            count += 1
    return count
    
def countMatchInColumns(matchLength, board):
    board = _transposeBoard(board)
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
        slid, topRow, bottomRow = _slideDownRow( board[rowIndex], board[rowIndex+1])
        if slid:
            slideOccurred = True
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

def _removeMatchesInRow(matchLength, row):
    result = []
    matchTarget = None
    currentRun = []
    for cell in row:
        if cell == matchTarget:
            currentRun.append(cell)
        else:
            if len(currentRun)  == matchLength:
                result += [None]*matchLength
            else:
                result += currentRun
            currentRun = [ cell]
            matchTarget = cell
    if len(currentRun) == matchLength:
        result += [None]*matchLength
    else:
        result += currentRun
    return result

def _removeHorizontalMatches(matchLength, board):
    result = []
    for row in board:
        result.append( _removeMatchesInRow( matchLength, row))
    return result

def _removeVerticalMatches( matchLength, board):
    board = _transposeBoard(board)
    board = _removeHorizontalMatches( matchLength, board)
    board = _transposeBoard(board)
    return board

def combineBoards( left, right):
    result = []
    for leftRow, rightRow in zip(left,right):
        resultRow = []
        for leftCell, rightCell in zip(leftRow, rightRow):
            if leftCell is None or rightCell is None:
                resultRow.append(None)
            else:
                resultRow.append(leftCell)
        result.append(resultRow)
    return( result)

def removeMatches( matchLength, board):
    rowResult = _removeHorizontalMatches( matchLength, board)
    colResult = _removeVerticalMatches( matchLength, board) 
    return combineBoards( rowResult, colResult)

def boardToString( board):
    result = ""
    for row in board:
        rowString = ""
        for cell in row:
            if cell is None:
                rowString += '_'
            else:
                rowString += chr(cell + ord('A') - 1)
        result += ' '.join(rowString) + '\n'
    return result

def countMatches(minMatchLength, board):
    result = []
    for matchLength in range( minMatchLength, len(board)+1 ):
        result.append( (matchLength, countMatchN(matchLength, board)) )
    return result

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
        self.assertBoardEqual( result, [ [None, None, 3],
                                         [None, 2, 5],
                                         [1, 4, 6] ] )
    def test_slideDownToFill_worksWithLargerBoards(self):
        given = [ [ 1, 2, 3, 1 ],
                  [ None, 4, 5, 1],
                  [ None, None, 6, 1],
                  [ None, None, None, None ]]
        result = slideDownToFill( given)
        self.assertBoardEqual( result, [ [None, None, None, None],
                                         [None, None, 3, 1],
                                         [None, 2, 5, 1],
                                         [1, 4, 6, 1] ] )
    def test__slideDownRow(self):
        top = [ 1, 2]
        bottom = [ None, 3 ]
        occurred, top2, bottom2 = _slideDownRow( top, bottom)
        self.assertEqual(occurred, True)
        self.assertListEqual( top2, [ None, 2] )
        self.assertListEqual( bottom2, [1, 3])
    def test__removeMatchesInRow_noMatches(self):
        given = [ 1, 2, 3, 4]
        result = _removeMatchesInRow(3, given)
        self.assertListEqual(result, [ 1, 2, 3, 4])
    def test__removeMatchesInRow_matchAtStart(self):
        given = [ 2, 2, 2, 4]
        result = _removeMatchesInRow(3, given)
        self.assertListEqual(result, [ None, None, None, 4])
    def test__removeMatchesInRow_matchAtEnd(self):
        given = [ 4, 2, 2, 2]
        result = _removeMatchesInRow(3, given)
        self.assertListEqual(result, [ 4, None, None, None ])
    def test__removeMatchesInRow_moreThanOneMatch(self):
        given = [ 4, 2, 2, 2, 3, 7, 7, 7, 9]
        result = _removeMatchesInRow(3, given)
        self.assertListEqual(result, [ 4, None, None, None, 3, None, None, None, 9])
    def test__removeMatchesInRow_moreThanOneMatch(self):
        given = [ 4, 2, 2, 2, 3, 7, 7, 7, 9]
        result = _removeMatchesInRow(3, given)
        self.assertListEqual(result, [ 4, None, None, None, 3, None, None, None, 9])
    def test_removeMatches_removesHorizontalMatch(self):
        given = [ [ 1, 1, 1],
                  [ 2, 3, 3],
                  [ 3, 3, 4] ]
        result = removeMatches(3, given)
        self.assertBoardEqual( result, [ [ None, None, None],
                                         [ 2, 3, 3],
                                         [ 3, 3, 4] ] )
    def assertBoardEqual( self, result, expected):
        for expectedRow, resultRow in zip(expected, result):
            self.assertListEqual(expectedRow, resultRow)
    def test_removeMatches_removesVerticalMatch(self):
        given = [ [1, 2, 3],
                  [1, 3, 4],
                  [1, 2, 4] ]
        result = removeMatches(3, given)
        self.assertBoardEqual( result, [[ None, 2, 3],
                                        [ None, 3, 4],
                                        [ None, 2, 4]])
    def test_removeMatches_removesIntersectingMatches(self):
        given = [ [1, 1, 1],
                  [1, 3, 4],
                  [1, 2, 4] ]
        result = removeMatches(3, given)
        self.assertBoardEqual( result, [[ None, None, None],
                                        [ None, 3, 4],
                                        [ None, 2, 4]])
    def test_boardToString_formatsCorrectly(self):
        given = [ [1, 1, None],
                  [1, 3, 4],
                  [1, 2, 4] ]
        result = boardToString(given)
        self.assertEqual(result, "A A _\nA C D\nA B D\n")
    def test_countMatchesOnBoard(self):
        given = [ [1, 1, 1, 1],
                  [1, 3, 4, 2],
                  [1, 2, 4, 2],
                  [3, 2, 4, 2]]
        result = countMatches(3, given)
        self.assertEqual(result, [ (3, 3), (4, 1) ])
    def test_countMatches_ignoresEmptyCells(self):
        given = [[ None, None, None],
                 [ None, 3, 4],
                 [ None, 2, 4]]
        result = countMatches(3, given)
        self.assertEqual(result, [ (3,0) ])

if __name__ == '__main__':
    unittest.main()

