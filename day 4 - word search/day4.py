def getNumWordMatches(letterMat, word, row, col):
    lineMatchings = [0, 0, 0, 0]

    for i in range(1, len(word)):
        rowWithinBounds = (row + i) < len(letterMat)
        colWithinBounds = (col + i) < len(letterMat[0])
        
        if colWithinBounds and letterMat[row][col+i] == word[i]:
            lineMatchings[0] += 1
        if rowWithinBounds:
            if letterMat[row+i][col] == word[i]:
                lineMatchings[1] += 1
            if colWithinBounds and letterMat[row+i][col+i] == word[i]:
                lineMatchings[2] += 1
            if (col - i) >= 0 and letterMat[row+i][col-i] == word[i]:
                lineMatchings[3] += 1
    numWords = sum(1 for l in lineMatchings if l == (len(word)-1))

    del lineMatchings
    return numWords

def solveWordSearch(fileName, word):
    with open(fileName + ".txt", mode="r") as file:
        letterMat = [line.strip() for line in file.readlines()]
        reverseWord = word[::-1]
        firstLetter = word[0]
        lastLetter = word[-1]

        numWords = 0
        for row in range(len(letterMat)):
            for col in range(len(letterMat[0])):
                letter = letterMat[row][col]
                if letter == firstLetter:
                    numWords += getNumWordMatches(letterMat, word, row, col)
                elif letter == lastLetter:
                    numWords += getNumWordMatches(letterMat, reverseWord, row, col)               
        print(numWords)

solveWordSearch("example", "XMAS")
solveWordSearch("input", "XMAS")
