from random import randint
from copy import deepcopy
import csv
import textwrap

def createBoard():
    
    # create empty board
    
    row = [0] * 9
    board = [row[:] for i in range(9)]
    
    # seed nine cells with 1 to 9 randomly

    for i in range(1,10):
        x, y = randint(0,8), randint(0,8)
        while board[x][y] != 0:
            x, y = randint(0,8), randint(0,8) 
        board[x][y] = i
    
    # solve board using backtracking

    position = (0,0)
    if board[0][0] != 0:
        position = getNextPosition(board, (0,0))

    board = solveBoard(board, position, findCandidates(board, position))

    return board

def getNextPosition(board, position):

    nextPositionFunc = lambda p : (
        p[0] + int((p[1] + 1) / 9), 
        (p[1] + 1) % 9
    )
    
    nextPosition = nextPositionFunc(position)

    while nextPosition != (9,0) and board[nextPosition[0]][nextPosition[1]] != 0:
        nextPosition = nextPositionFunc(nextPosition)
    
    return nextPosition

def findCandidates(board, position):

    candidates = list(range(1,10))

    # remove numbers in same row, col, block from candidates
    candidates = list(
        set(candidates)
        - set(board[position[0]])
        - set(transpose(board)[position[1]]) 
        - set(block(board, position))
    )
    
    return candidates

def transpose(board):
    return [[board_row[col] for board_row in board] for col in range(len(board))]

def block(board, position):

    ranges = [range(0,3), range(3,6), range(6,9)]
    xRange = next(r for r in ranges if position[0] in r)
    yRange = next(r for r in ranges if position[1] in r)

    return [board[i][j] for i in xRange for j in yRange]

def solveBoard(board, position, candidates):
    
    nextPosition = getNextPosition(board, position)
    
    # backtracking loop

    while True:
        if len(candidates) == 0:
            break
        
        board[position[0]][position[1]] = candidates[0]    
        
        if nextPosition == (9,0):
            return board

        res = solveBoard(deepcopy(board), nextPosition, findCandidates(board, nextPosition))
        
        if res == None:
            candidates = candidates[1:]
        else:
            return res

def verify(board):
    return (
        all(sorted(board[row]) == list(range(1,10)) for row in range(9))
        and all(sorted(transpose(board)[row]) == list(range(1,10)) for row in range(9))
        and all(sorted(block(board, (x,y))) == list(range(1,10)) for x in range(0,9,3) for y in range(0,9,3))
    )

# board = createBoard()
f = open('./archive/sudoku.csv', 'r')
csvFile = csv.reader(f) 
next(csvFile, None)

i = 0

for line in csvFile:
    board = [[int(c) for c in row] for row in textwrap.wrap(line[0], 9)]
    print(*board, sep='\n')
    print()

    position = (0,0)
    if board[0][0] != 0:
        position = getNextPosition(board, (0,0))

    board = solveBoard(board, position, findCandidates(board, position))

    print(*board, sep='\n')
    
    print(board == [[int(c) for c in row] for row in textwrap.wrap(line[1], 9)])

    i += 1

    if i == 10:
        break