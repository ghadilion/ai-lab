import random
import math
import matplotlib.pyplot as plt
import csv

def getPathCost(adjMat, path):
    pathCost = adjMat[path[0]-1][path[-1]-1]
    for i in range(len(path)-1):
        pathCost += adjMat[path[i]-1][path[i+1]-1]        
    return pathCost

def getRandomPath(adjMat):
    nodes = list(range(1,len(adjMat)+1))
    path = []
    while len(nodes) > 0:
        path.append(nodes[random.randint(0, len(nodes)-1)])
        nodes.remove(path[-1])
    pathCost = getPathCost(adjMat, path)
    return (pathCost, path)

def getRandomNeighbour(adjMat, path):
    a = random.randint(0,len(path)-1)
    b = random.randint(0,len(path)-1)
    while a == b:
        b = random.randint(0, len(path)-1)
    path[a], path[b] = path[b], path[a]
    pathCost = getPathCost(adjMat, path)
    return (pathCost, path)

def simulatedanalling(adjMat):
    maxIterations = 100
    temperature = 1
    beta = 5
    cost, path = getRandomPath(adjMat)
    costs = [cost]
    temperatures = [temperature]
    for i in range(maxIterations):
        temperature = temperature/(1 + beta * temperature) 
        randomNeighbourCost, randomNeighbourPath = getRandomNeighbour(adjMat, path[:])
        deltaE = randomNeighbourCost - cost
        # print(path, cost)
        if deltaE < 0 or random.uniform(0,1) < math.exp(-deltaE/temperature):
            path = randomNeighbourPath
            cost = randomNeighbourCost
            print(cost, '\t', path, '\t', deltaE, '\t', temperature)
            costs.append(cost)
            temperatures.append(temperature)
    return (temperatures, costs, path)

graph = []

with open('tsp_input.csv', 'r') as fd:
    reader = csv.reader(fd)
    for row in reader:
        graph.append(list(map(int,row)))
        
x, y, optimalPath = simulatedanalling(graph)
print('Optimal Path: ', optimalPath, 'Optimal Cost: ', y[-1])
plt.plot(x,y)
plt.xlabel("Temperature")
plt.ylabel("Cost")
plt.show()
