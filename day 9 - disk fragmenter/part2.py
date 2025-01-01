from math import floor

def defragmentDiskFiles(encoding: str):
    freeSpaces = dict()
    pos = 0
    for i in range(1, len(encoding)):
        pos += int(encoding[i-1])
        if i % 2 != 0:
            freeSpaces[pos] = int(encoding[i])
    diskSize = pos+int(encoding[i])

    if len(encoding) % 2 == 0:
        back = len(encoding)-2
    else:
        back = len(encoding)-1
    backPos = diskSize-int(encoding[back])

    checksum = 0
    while back >= 0:
        numBackSpaces = int(encoding[back])
        val = floor(back / 2)
        spaceFound = False
        for f in sorted(freeSpaces.keys()):
            numFrontSpaces = freeSpaces[f]
            if f > backPos:
                break
            if numFrontSpaces >= numBackSpaces:
                checksum += sum((f+i)*val for i in range(numBackSpaces))
                if freeSpaces[f] != numBackSpaces:
                    freeSpaces[f+numBackSpaces] = freeSpaces[f] - numBackSpaces
                del freeSpaces[f]
                spaceFound = True
                break
        
        if not spaceFound:
            checksum += sum((backPos+i)*val for i in range(numBackSpaces))

        backPos = backPos - int(encoding[back-1]) - int(encoding[back-2])
        back -= 2
        
    print(checksum)
        

#defragmentDiskFiles('12345')
defragmentDiskFiles('2333133121414131402')
long = open("input.txt").read()
defragmentDiskFiles(long)
