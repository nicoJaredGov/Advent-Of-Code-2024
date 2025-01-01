import numpy as np
import re
import os

def solveLinearSystem(input: str, disp):
    c = [int(i) for i in re.findall(r'[0-9]+',input)]
    mat = np.array([
        [c[0], c[2]],
        [c[1], c[3]]
    ])
    dest = np.array([c[4]+disp, c[5]+disp])
    return np.dot(np.linalg.inv(mat), dest)

def getTotalTokenCost(fileName, disp=0):
    currentFilePath = os.path.abspath(f'{os.path.dirname(__file__)}/{fileName}.txt')
    with open(currentFilePath, mode="r") as file:
        machines = file.read().split("\n\n")
    
    totalCost = 0
    for machine in machines:
        a, b = solveLinearSystem(machine, disp)
        if round(a, 3) % 1 == 0 and round(b, 3) % 1 == 0:
            totalCost += 3*a + b
    print(int(totalCost))

getTotalTokenCost("example", 10000000000000)
getTotalTokenCost("input", 10000000000000)