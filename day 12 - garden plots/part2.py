import os
from collections import deque
from enum import Enum
from collections import namedtuple

class Side(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

AdjacentCell = namedtuple("AdjacentCell", "row col side")

def addToDictSet(dictionary: dict[any, set], item, value=None):
    if item in dictionary:
        if value == None:
            return
        dictionary[item].add(value)
    else:
        if value == None:
            dictionary[item] = set()
            return
        dictionary[item] = {value}

def isOnMap(map, position):
    if position.row < 0 or position.row >= len(map):
        return False
    if position.col < 0 or position.col >= len(map[0]):
        return False
    return True

def getRegionCost(map, position, exploredCells: dict) -> int:
    frontierQueue = deque([position])
    exploredCells[position] = set()
    numCells = 1
    numFences = 0
    while len(frontierQueue) != 0:
        x, y = frontierQueue.popleft()
        adjacentPositions = [
            AdjacentCell(x + 1, y, Side.SOUTH),
            AdjacentCell(x - 1, y, Side.NORTH),
            AdjacentCell(x, y - 1, Side.WEST),
            AdjacentCell(x, y + 1, Side.EAST),
        ]
        
        numAdjacent = 0
        numFound = 0
        existingNeighbors = set()
        for p in adjacentPositions:
            if isOnMap(map, p) and map[p.row][p.col] == map[x][y]:
                numAdjacent += 1
                if (p.row, p.col) not in exploredCells:
                    frontierQueue.append((p[0], p[1]))
                    addToDictSet(exploredCells, (p.row, p.col))
                    numFound += 1
                else:
                    existingNeighbors.add(p)
            else:
                addToDictSet(exploredCells, (x, y), p.side)
                        
        numSharedSides = 0
        for en in existingNeighbors:
              numSharedSides += len(exploredCells[(en.row, en.col)] & exploredCells[(x,y)])
        existingNeighbors.clear()

        numFences += 4 - numSharedSides - numAdjacent
        numCells += numFound
    
    cost = numCells * numFences
    # print(cost)
    return cost

def getGardenFenceCost(fileName):
    currentFilePath = os.path.abspath(f'{os.path.dirname(__file__)}/{fileName}.txt')
    with open(currentFilePath, mode="r") as file:
        map = file.read().split("\n")
    
    exploredCells = dict()
    totalCost = 0
    for r in range(len(map)):
        for c in range(len(map[r])):
            if (r,c) not in exploredCells:
                totalCost += getRegionCost(map, (r,c), exploredCells)
            
    print(totalCost)


getGardenFenceCost("example")
getGardenFenceCost("input")