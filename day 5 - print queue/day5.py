import time

def buildRulesDict(rules: str):
    rulesDict: dict[str, set] = dict()
    for rule in rules:
        key, value = rule.split('|')
        if key not in rulesDict:
            rulesDict[key] = { value }
        else:
            rulesDict[key].add(value)
    return rulesDict

def addDepsToSubList(output, rulesDict: dict[str, set], currentPage, found: set, wordSet):
    if currentPage not in found:
        found.add(currentPage)

        pages = rulesDict.get(currentPage, None)
        if pages != None:
            pages = pages & wordSet
        if pages == None or len(pages) == 0:
            output.append(currentPage)
            return 
        for page in pages:
            if page not in found:
                addDepsToSubList(output, rulesDict, page, found, wordSet)

        output.append(currentPage)

def fixInvalidUpdate(rulesDict: dict[str, set], update: str):
    queue = update.split(",")
    wordSet = set(queue)
    output = []
    found = set()
    for i in range(len(queue)):
        addDepsToSubList(output, rulesDict, queue[i], found, wordSet)
    return output

def checkIfValidUpdate(rulesDict: dict[str, set], update: str):
    queue = update.split(",")
    isValid = True
    found = set()
    invalidIfFound = set()
    for i in range(len(queue)-1, -1, -1):
        currentPage = queue[i]
        if currentPage in invalidIfFound:
            isValid = False
            queue = fixInvalidUpdate(rulesDict, update)
            break
        
        found.add(currentPage)
        invalidIfFound = (invalidIfFound | rulesDict.get(currentPage, set())) - found
    
    middleValue = int(queue[(len(queue)-1) // 2])
    return isValid, middleValue

def processPrintQueue(fileName):
    start = time.time()
    with open(fileName + ".txt", mode="r") as file:
        rules, updates = [ls.strip().split() for ls in file.read().split("\n\n")]
    rulesDict = buildRulesDict(rules)

    solveTime = time.time()
    totalValueUnfixed = 0
    totalValueFixed = 0
    for update in updates:
        isValid, middleValue = checkIfValidUpdate(rulesDict, update)
        if isValid:
            totalValueUnfixed += middleValue
        else:
            totalValueFixed += middleValue
    solveTime = time.time() - solveTime
            
    print(totalValueUnfixed, totalValueFixed)
    total = time.time() - start
    print("Total time:", total)
    print("Time to solve:", solveTime)

#processPrintQueue("example")
processPrintQueue("input")
#processPrintQueue("5")