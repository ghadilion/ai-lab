# nqueen using simulated annealing

import random
import math
import matplotlib.pyplot as plt

def generateRandomState(boardLen):
    return [random.randint(0,boardLen-1) for i in range(boardLen)]

def generateBoard(state):
    board = [[0]*len(state)]
    for i in range(1,len(state)):
        board.append(board[i-1][:])
    for i in range(len(state)):
        board[i][state[i]] = 1
    return board

def calculateObjective(state):
    count = 0
    for i in range(len(state)):
        for j in range(i+1,len(state)):
            if state[i] == state[j] or state[j] == state[i]-i+j or state[j] == state[i]+i-j:
                count+=1
    return count

def randomNeighbour(state):
    randomIdx = random.randint(0, len(state)-1)
    curValue = state[randomIdx]
    newValue = curValue
    while newValue == curValue:
    	newValue = random.randint(0, len(state)-1) 
    state[randomIdx] = newValue 
    return (calculateObjective(state), state)

def simulatedanalling(state):
    temperature = 0.01
    beta = 20
    #cooldown = 0.99
    obj = calculateObjective(state)
    objectiveVals = [obj]
    temperatures = [temperature]
    while temperature > 0:
        #temperature *= cooldown
        temperature = temperature/(1 + beta * temperature) 
        randomNeighbourObj, randomNeighbourState = randomNeighbour(state)
        deltaE = randomNeighbourObj - obj
        if deltaE < 0 or random.uniform(0,1) < math.exp(-deltaE/temperature):
            print(obj, '\t', state, '\t', deltaE, '\t', temperature)
            state = randomNeighbourState
            obj = randomNeighbourObj
            objectiveVals.append(obj)
            temperatures.append(temperature)
        if obj == 0:
            return (temperatures, objectiveVals, state)
    return 'fail!'


size = int(input('Enter length of board: '))
randomState = generateRandomState(size)
print('Random board generated...')
print(*generateBoard(randomState), sep='\n')


x, y, optimalState = simulatedanalling(randomState)
print('Optimal Board...')
print(*generateBoard(optimalState), sep='\n')
print('Optimal state: ', optimalState)
plt.plot(x,y)
plt.xlabel("Temperature")
plt.ylabel("Objective Value")
plt.show()

