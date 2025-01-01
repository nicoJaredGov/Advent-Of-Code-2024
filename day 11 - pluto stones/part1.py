def addToListAndMemo(ls: list, memo: dict[int, list], key, value):
    ls.append(value)
    if key in memo:
        memo[key].append(value)
    else:
        memo[key] = [value]

def countNumStones(input: str, numIterations=25):
    values = list(i for i in input.split())
    memo = dict[int, list]()
    swapList = []
    memoHits = 0
    totalCalcs = 0
    for _ in range(numIterations):
        while len(values) > 0:
            totalCalcs += 1
            v = values.pop()
            if v in memo:
                swapList.extend(memo[v])
                memoHits += 1
            else:
                if int(v) == 0:
                    addToListAndMemo(swapList, memo, v, '1')
                elif len(v) % 2 == 0:
                    addToListAndMemo(swapList, memo, v, v[:len(v)//2])
                    addToListAndMemo(swapList, memo, v, str(int(v[len(v)//2:])))
                else:
                    addToListAndMemo(swapList, memo, v, str(int(v)*2024))
        
        values.extend(swapList)
        swapList.clear()

    print(len(values))
    print(f"Total calcs: {totalCalcs} \tMemo hits: {memoHits} \tHit rate: {(memoHits/totalCalcs)*100}%")

countNumStones('125 17')
countNumStones('0 4 4979 24 4356119 914 85734 698829')