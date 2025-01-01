def getNextValue(curr):
    if int(curr) == 0:
        return ['1']
    elif len(curr) % 2 == 0:
        return [curr[:len(curr)//2], str(int(curr[len(curr)//2:]))]
    else:
        return [str(int(curr)*2024)]

def countNumStones(input: str, numIterations=25):
    values = {i:[1, getNextValue(i)] for i in input.split()}
    tempCounts = dict()
    for _ in range(numIterations):
        for v in values:
            if values[v][0] > 0:
                for next in values[v][1]:
                    if next in tempCounts:
                        tempCounts[next] += values[v][0]
                    else:
                        tempCounts[next] = values[v][0]
                values[v][0] = 0

        for next in tempCounts:
            if next in values:
                values[next][0] += tempCounts[next]
            else:
                values[next] = [tempCounts[next], getNextValue(next)]
        tempCounts.clear()

    print(sum(c[0] for c in values.values()))

countNumStones('125 17', 75)
countNumStones('0 4 4979 24 4356119 914 85734 698829', 75)