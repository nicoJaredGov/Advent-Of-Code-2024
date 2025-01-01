def countNumberXMas(fileName):
    with open(fileName + ".txt", mode="r") as file:
        letterMat = [line.strip() for line in file.readlines()]

        numXmas = 0
        for row in range(1, len(letterMat)-1):
            for col in range(1, len(letterMat[0])-1):
                letter = letterMat[row][col]
                if letter == 'A':
                    if ((letterMat[row-1][col-1] == "M" and letterMat[row+1][col+1] == "S") or (
                        letterMat[row+1][col+1] == "M" and letterMat[row-1][col-1] == "S"
                    )) and ((letterMat[row+1][col-1] == "M" and letterMat[row-1][col+1] == "S") or (
                        letterMat[row-1][col+1] == "M" and letterMat[row+1][col-1] == "S"
                    )):
                        numXmas += 1
                                 
        print(numXmas)

countNumberXMas("example")
countNumberXMas("input",)
