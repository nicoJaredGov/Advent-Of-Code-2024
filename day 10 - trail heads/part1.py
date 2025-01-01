import os
#NOTE can optimize by remembering paths to 9

def isOnMap(map, position):
    row, col = position
    if row < 0 or row >= len(map):
        return False
    if col < 0 or col >= len(map[0]):
        return False
    return True

def getTrailHeadScore(map, pos) -> int:
    stack = [pos]
    seenPeaks = set()
    while len(stack) != 0:
        x, y = stack.pop()
        if map[x][y] == 9:
            seenPeaks.add((x, y))

        adjacentPositions = [
            (x + 1, y),
            (x - 1, y),
            (x, y - 1),
            (x, y + 1),
        ]
        for p in adjacentPositions:
            if isOnMap(map, p) and map[p[0]][p[1]] == map[x][y] + 1:
                stack.append(p)
    #print(len(seenPeaks))
    return len(seenPeaks)

def getTotalTrailScore(fileName):
    currentFilePath = os.path.abspath(f'{os.path.dirname(__file__)}/{fileName}.txt')
    with open(currentFilePath, mode="r") as file:
        map = [list(int(p) for p in l) for l in file.read().split("\n")]
    
    totalScore = 0
    for r in range(len(map)):
        for c in range(len(map[r])):
            if map[r][c] == 0:
                totalScore += getTrailHeadScore(map, (r,c))
    
    print(totalScore)


getTotalTrailScore("example")
getTotalTrailScore("input")
