import numpy as np
import re
import os
import math
import matplotlib.pyplot as plt

def getPosAndVelocityMatrices(lines):
    posMat = np.empty((len(lines), 2), np.int16)
    vMat = np.empty((len(lines), 2), np.int16)
    for i in range(len(lines)):
        numbers = re.findall(r'[-]*[0-9]+', lines[i])
        posMat[i] = numbers[0:2]
        vMat[i] = numbers[2:4]
    
    return posMat, vMat

def getSafetyFactor(fileName, width=1, height=1, period=100):
    currentFilePath = os.path.abspath(f'{os.path.dirname(__file__)}/{fileName}.txt')
    with open(currentFilePath, mode="r") as file:
        lines = file.read().split("\n")

    def displayPositions(posMat, t):
        dispMap = np.zeros((width, height))
        for point in posMat:
            dispMap[point[0]][point[1]] += 1
        plt.imshow(dispMap)
        plt.savefig(f"{os.path.dirname(__file__)}/images/{t}")
    
    posMat, velMat = getPosAndVelocityMatrices(lines)
    limits = np.array([width, height])
    
    for _ in range(period):
        posMat += velMat
        posMat %= limits

    displayPositions(posMat, period)
    midX = width // 2
    midY = height // 2
    quadrantCounts = {i:0 for i in [1,2,3,4]}
    for point in posMat:
        x, y = point
        if x < midX and y < midY:
            quadrantCounts[1] += 1
        elif x < midX and y > midY:
                quadrantCounts[2] += 1
        elif x > midX and y < midY:
            quadrantCounts[3] += 1
        elif x > midX and y > midY:
            quadrantCounts[4] += 1
    safetyFactor = math.prod(quadrantCounts.values())
    print(safetyFactor, quadrantCounts)
    return safetyFactor

#getSafetyFactor("example", 11, 7, 100)
r = getSafetyFactor("input", 101, 103, 7569)

