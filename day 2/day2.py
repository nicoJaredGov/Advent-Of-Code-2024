from enum import Enum

MIN_VALUE = 1
MAX_VALUE = 3
NUM_ALLOWED_BAD_LEVELS = 1

isGreaterThanThreshold = lambda diff: abs(diff) < MIN_VALUE or abs(diff) > MAX_VALUE

class DIFF_TYPE(Enum):
    INCREASING = 0
    EQUAL = 1
    DECREASING = 2

def determineDiffType(diff):
    if diff < 0:
        return DIFF_TYPE.DECREASING
    elif diff > 0:
        return DIFF_TYPE.INCREASING
    else:
        return DIFF_TYPE.EQUAL

def isReportSafe(report):
    badLevels = []
    diffTypes = []
    diffTypeCounts = {
        DIFF_TYPE.DECREASING: 0,
        DIFF_TYPE.INCREASING: 0,
        DIFF_TYPE.EQUAL: 0
    }
    for i in range(len(report)-1):
        diff = report[i+1] - report[i]
        badLevels.append(isGreaterThanThreshold(diff))

        diffType = determineDiffType(diff)
        diffTypeCounts[diffType] += 1
        diffTypes.append(diffType)

    #check the number of increase/decrease violations
    baselineDiffType, count = max(diffTypeCounts.items(), key=lambda x: x[1])
    if baselineDiffType == DIFF_TYPE.EQUAL and count > NUM_ALLOWED_BAD_LEVELS:
        return False
    elif count < len(report) - NUM_ALLOWED_BAD_LEVELS - 1:
        return False
            
    #reconcile both threshold and increase/decrease violations
    badLevels = [badLevels[i] or (diffTypes[i] != baselineDiffType) for i in range(len(badLevels))]

    numBadLevels = 0
    b = 0
    while b < len(badLevels):
        if badLevels[b]:
            numBadLevels += 1
            if numBadLevels > NUM_ALLOWED_BAD_LEVELS:
                return False

            skipIndices = []
            validSkipFound = False
            #consecutive bad level
            if (b+1) < len(badLevels) and badLevels[b+1]:
                skipIndices.append(b+1)
            #single bad level at start or end
            elif b==0 or b==len(badLevels)-1:
                validSkipFound = True
                b += 1
                continue
            #single bad level in the middle
            else:
                skipIndices.append(b)
                skipIndices.append(b+1)
            
            for i in skipIndices:
                skipDiff = report[i+1] - report[i-1]
                skipDiffType = determineDiffType(skipDiff)
                if not (isGreaterThanThreshold(skipDiff) or skipDiffType != baselineDiffType):
                    validSkipFound = True
                    b = i
                    break
            
            if not validSkipFound:
                return False
        b += 1
    
    return True

def determineNumSafeLevels(fileName):
    numSafeLevels = 0
    with open(fileName+".txt", mode="r") as file:
        for line in file.readlines():
            report = [int(i) for i in line.strip().split()]
            if isReportSafe(report):
                numSafeLevels += 1
    print(numSafeLevels)

determineNumSafeLevels("example")
determineNumSafeLevels("input")