from enum import Enum

class OPERATOR(Enum):
    ADD = '+'
    SUBTRACT = '-'
    MULTIPLY = 'x'
    DIVIDE = '/'
    CONCAT = '||'

def checkIfValidLine(line: list, orderedOperators: list) -> bool:
    testVal = line[0]
    stack = [( o, len(line)-1, testVal) for o in orderedOperators]

    while len(stack) != 0:
        op, idx, calc = stack.pop()     
        result = None
        if op is OPERATOR.ADD:
            result = calc - line[idx]
            if result < line[idx-1]:
                continue
        elif op is OPERATOR.MULTIPLY:
            result = calc / line[idx]
            if result % 1 > 0:
                continue
            else:
                result = int(result)
        elif op is OPERATOR.CONCAT:
            if (calc != line[idx] and 
                str(calc).endswith(str(line[idx]))):
                result = int(str(calc)[:-(len(str(line[idx])))])
            else:
                continue
        
        nextIdx = idx - 1
        if nextIdx == 1:
            if result != line[nextIdx]:
                continue
            else:
                return True
        
        stack.extend([( o, nextIdx, result) for o in orderedOperators])
        
    return False

def calculateValidOperations(fileName):
    with open(fileName + ".txt", mode="r") as file:
        lines = [ls.split() for ls in file.read().split("\n")]

    for line in lines:
        for i in range(len(line)):
            if i == 0:
                line[i] = line[i][:-1]
            line[i] = int(line[i])

    total = 0
    #operators = [OPERATOR.ADD, OPERATOR.MULTIPLY]
    operators = [OPERATOR.ADD, OPERATOR.MULTIPLY, OPERATOR.CONCAT]
    for line in lines:
        if checkIfValidLine(line, operators):
            total += line[0]
    print(total)

calculateValidOperations("example")
calculateValidOperations("input")