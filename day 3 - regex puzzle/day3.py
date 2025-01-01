import re
import math

def getOperandsFromFuncStr(funcString):
    numbers = re.sub(r"mul\(", "", funcString)
    numbers = re.sub(r"\)", "", numbers)
    numbers = [int(i) for i in numbers.split(",")]
    return numbers

def getProductSumFromMul(mulMatches):
    sum = 0
    for match in mulMatches:
        operands = getOperandsFromFuncStr(match)
        product = math.prod(operands)
        sum += product
    return sum

def processCorruptedData(fileName):
    with open(fileName+".txt", mode="r") as file:
        text = file.read()
        matches = re.findall(r"mul\([0-9]{1,3},[0-9]{1,3}\)", text)
        sum = getProductSumFromMul(matches)
        print(sum)

processCorruptedData("example")
processCorruptedData("input")

def processCorruptedDataWithConditionals(fileName):
    with open(fileName+".txt", mode="r") as file:
        text = file.read()
        dontSegments = re.split(r"don\'t\(\)", text)

        sum = 0
        mulMatches = re.findall(r"mul\([0-9]{1,3},[0-9]{1,3}\)", dontSegments[0])
        sum += getProductSumFromMul(mulMatches)
        for segment in dontSegments[1:]:
            doSegments = re.split(r"do\(\)", segment)
            for doSegment in doSegments[1:]:
                mulMatches = re.findall(r"mul\([0-9]{1,3},[0-9]{1,3}\)", doSegment)
                sum += getProductSumFromMul(mulMatches)
        print(sum)
        
processCorruptedDataWithConditionals("example2")
processCorruptedDataWithConditionals("input2")