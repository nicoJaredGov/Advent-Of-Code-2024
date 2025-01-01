import os
from collections import deque

def isOnMap(map, position):
    row, col = position
    if row < 0 or row >= len(map):
        return False
    if col < 0 or col >= len(map[0]):
        return False
    return True

def getRegionCost(map, position, exploredCells: set) -> int:
    frontierQueue = deque([position])
    exploredCells.add(position)
    numCells = 1
    numFences = 0
    while len(frontierQueue) != 0:
        x, y = frontierQueue.popleft()
        adjacentPositions = [
            (x + 1, y),
            (x - 1, y),
            (x, y - 1),
            (x, y + 1),
        ]
        
        numAdjacent = 0
        numFound = 0
        for p in adjacentPositions:
            if isOnMap(map, p) and map[p[0]][p[1]] == map[x][y]:
                numAdjacent += 1
                if p not in exploredCells:
                    frontierQueue.append(p)
                    exploredCells.add(p)
                    numFound += 1
        
        numFences += (4 - numAdjacent)
        numCells += numFound
    
    cost = numCells * numFences
    # print(cost)
    return cost

def getGardenFenceCost(fileName):
    currentFilePath = os.path.abspath(f'{os.path.dirname(__file__)}/{fileName}.txt')
    with open(currentFilePath, mode="r") as file:
        map = file.read().split("\n")
    
    exploredCells = set()
    totalCost = 0
    for r in range(len(map)):
        for c in range(len(map[r])):
            if (r,c) not in exploredCells:
                totalCost += getRegionCost(map, (r,c), exploredCells)
            
    print(totalCost)


getGardenFenceCost("example")
getGardenFenceCost("input")