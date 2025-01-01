def determineAntinodes(fileName, withinDistance=True):
    with open(fileName + ".txt", mode="r") as file:
        lines = file.read().split("\n")
    
    def isWithinMap(point):
        row, col = point
        if row < 0 or row >= len(lines):
            return False
        if col < 0 or col >= len(lines[0]):
            return False
        return True
    
    getSumVector = lambda p1, p2: (p1[0]+p2[0], p1[1]+p2[1])
    getNegVector = lambda p: (-p[0], -p[1])

    def getNextAntinode(diffVector, point):
        antinode = getSumVector(diffVector, point)
        if isWithinMap(antinode):
            antinodePositions.add(antinode)
            return True, antinode
        return False, None

    antennaPositions = dict()
    for row in range(len(lines)):
        for col in range(len(lines[0])):
            obj = lines[row][col]
            if obj != ".":
                if obj in antennaPositions:
                    antennaPositions[obj].append((row,col))
                else:
                    antennaPositions[obj] = [(row,col)]
    
    antinodePositions = set()
    for antenna in antennaPositions:
        positions = antennaPositions[antenna]
        for i in range(len(positions)-1):
            for j in range(i+1, len(positions)):
                diffVector = getSumVector(getNegVector(positions[i]), positions[j])
                # print(positions[i], positions[j], diffVector, getNegVector(diffVector))
                hasNextAntinode1, hasNextAntinode2 = True, True
                position1, position2 = positions[i], positions[j]
                while hasNextAntinode1:
                    hasNextAntinode1, position1 = getNextAntinode(getNegVector(diffVector), position1)
                    if withinDistance:
                        break
                while hasNextAntinode2:
                    hasNextAntinode2, position2 = getNextAntinode(diffVector, position2)
                    if withinDistance:
                        break
                
                if not withinDistance:
                    antinodePositions.add(positions[i])
                    antinodePositions.add(positions[j])

    print(len(antinodePositions))
                

determineAntinodes("example", withinDistance=False)
determineAntinodes("input", withinDistance=False)