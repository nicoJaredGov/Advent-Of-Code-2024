from enum import IntEnum
import os
import time

def addToDictList(dictionary: dict[any, list], item, value):
    if item in dictionary:
        dictionary[item].append(value)
    else:
        dictionary[item] = [value]

def addToDictSet(dictionary: dict[any, set], item, value):
    if item in dictionary:
        dictionary[item].add(value)
    else:
        dictionary[item] = {value}

class Direction(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

def turn90Degrees(currentDirection: Direction):
    return Direction((int(currentDirection) + 1) % 4)

def determineGuardPositions(fileName):
    currentFilePath = os.path.abspath(f'{os.path.dirname(__file__)}/{fileName}.txt')
    with open(currentFilePath, mode="r") as file:
        map = file.read().split("\n")

    start = time.time()
    # get guard and obstacle positions
    obsRows = dict[int, list]()
    obsCols = dict[int, list]()
    guardPosition = None
    guardDirection = None
    directionSymbols = {
        '^': Direction.NORTH,
        '>': Direction.EAST,
        'V': Direction.SOUTH,
        '<': Direction.WEST
    }
    for row in range(len(map)):
        for col in range(len(map[0])):
            currSymbol = map[row][col]
            if currSymbol == ".":
                continue
            elif currSymbol == "#":
                addToDictList(obsCols, col, row)
                addToDictList(obsRows, row, col)
            elif currSymbol in directionSymbols:
                guardDirection = directionSymbols[currSymbol]
                guardPosition = (row, col)         
    startPosition = guardPosition

    def isOnMap(position):
        row, col = position
        if row < 0 or row >= len(map):
            return False
        if col < 0 or col >= len(map[0]):
            return False
        return True

    def getNextObstacle(guardDirection: Direction, guardPosition):
        nextObsExists = True
        row, col = guardPosition
        obsRow, obsCol = None, None
        nextPosition = (None, None)

        if guardDirection == Direction.NORTH:
            obsCol = col
            tmp = obsCols.get(col)
            if tmp is not None and len(tmp) != 0:
                for r in range(len(obsCols[col])-1,-1,-1):
                    if obsCols[col][r] < row:
                        obsRow = obsCols[col][r]
                        break
            if obsRow is None:
                obsRow = -1
                nextObsExists = False
            nextPosition = (obsRow+1, col)

        elif guardDirection == Direction.SOUTH:
            obsCol = col
            tmp = obsCols.get(col)
            if tmp is not None and len(tmp) != 0:
                for r in range(len(obsCols[col])):
                    if obsCols[col][r] > row:
                        obsRow = obsCols[col][r]
                        break
            if obsRow is None:
                obsRow = len(map)
                nextObsExists = False
            nextPosition = (obsRow-1, col)

        elif guardDirection == Direction.EAST:
            obsRow = row
            tmp = obsRows.get(row)
            if tmp is not None and len(tmp) != 0:
                for c in range(len(obsRows[row])):
                    if obsRows[row][c] > col:
                        obsCol = obsRows[row][c]
                        break
            if obsCol is None:
                obsCol = len(map[0])
                nextObsExists = False
            nextPosition = (row, obsCol-1)

        elif guardDirection == Direction.WEST:
            obsRow = row
            tmp = obsRows.get(row)
            if tmp is not None and len(tmp) != 0:
                for c in range(len(obsRows[row])-1,-1,-1):
                    if obsRows[row][c] < col:
                        obsCol = obsRows[row][c]
                        break
            if obsCol is None:
                obsCol = -1
                nextObsExists = False
            nextPosition = (row, obsCol+1)

        nextObstacle = (obsRow, obsCol)
        return nextObsExists, nextObstacle, nextPosition

    def moveOneStepForward(position, direction: Direction):
        if direction == Direction.NORTH:
            return (position[0]-1, position[1])
        elif direction == Direction.SOUTH:
            return (position[0]+1, position[1])
        elif direction == Direction.EAST:
            return (position[0], position[1]+1)
        elif direction == Direction.WEST:
            return (position[0], position[1]-1)
        else:
            return position

    def hasPossibleLoop(guardPosition, guardDirection, foundObstacles: dict, exploredPositions: dict):
        #simulate adding new obstacle
        newObs = moveOneStepForward(guardPosition, guardDirection)
        if (not isOnMap(newObs) 
            or newObs == startPosition 
            or map[newObs[0]][newObs[1]] == "#"
            or newObs in exploredPositions):
            return False
        addToDictList(obsRows, newObs[0], newObs[1])
        addToDictList(obsCols, newObs[1], newObs[0])
        obsRows[newObs[0]].sort()
        obsCols[newObs[1]].sort()
        addToDictList(foundObstacles, newObs, guardDirection)

        loopFound = False
        nextObsExists = True
        currPosition = guardPosition
        currDirection = guardDirection
        pathExplored = dict()
        while nextObsExists:
            currDirection = turn90Degrees(currDirection)
            nextObsExists, nextObs, currPosition = getNextObstacle(currDirection, currPosition)
            if (currDirection in foundObstacles.get(nextObs, {})
                or currDirection in pathExplored.get(currPosition, {})):
                loopFound = True
                break
            addToDictSet(pathExplored, currPosition, currDirection)
        
        #undo simulation
        obsRows[newObs[0]].remove(newObs[1])
        obsCols[newObs[1]].remove(newObs[0])
        foundObstacles.pop(newObs)
        return loopFound

    def addPathToNextObstacle(guardPosition, guardDirection, exploredPositions: dict, foundObstacles: dict):
        nextObsExists = True
        nextPosition = None
        numLoops = 0

        nextObsExists, nextObs, nextPosition = getNextObstacle(guardDirection, guardPosition)
        currPosition = guardPosition
        while currPosition != nextPosition:
            if hasPossibleLoop(currPosition, guardDirection, foundObstacles, exploredPositions):
                numLoops += 1   
            currPosition = moveOneStepForward(currPosition, guardDirection)
            addToDictSet(exploredPositions, currPosition, guardDirection)
                   
        if nextObsExists:
            addToDictSet(foundObstacles, nextObs, guardDirection)
        return nextObsExists, nextPosition, numLoops

    # find guard positions
    exploredPositions = dict()
    foundObstacles = dict()
    nextObsExists = True
    possibleLoops = 0
    while isOnMap(guardPosition) and nextObsExists:
        nextObsExists, nextPosition, numLoops = addPathToNextObstacle(guardPosition, guardDirection, exploredPositions, foundObstacles)
        guardPosition = nextPosition
        guardDirection = turn90Degrees(guardDirection)
        possibleLoops += numLoops
    
    print("Time taken:", time.time() - start)
    print("guard positions:", len(exploredPositions))
    print("possible loops:", possibleLoops)


determineGuardPositions("example")
determineGuardPositions("input")
determineGuardPositions("6")
