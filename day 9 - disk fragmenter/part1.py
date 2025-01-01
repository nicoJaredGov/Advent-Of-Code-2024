from math import floor

def defragmentDisk(encoding: str):
    front = 0
    if len(encoding) % 2 == 0:
        back = len(encoding)-2
    else:
        back = len(encoding)-1
    pos = int(encoding[0])

    checksum = 0
    backCounter = int(encoding[back])
    while front < back:
        front += 1
        frontNumSpaces = int(encoding[front])
        
        # taken spaces
        if front % 2 == 0:
            if front == back:
                frontNumSpaces = backCounter
            val = floor(front / 2)
            checksum += sum((pos+i)*val for i in range(frontNumSpaces))
        
        # free spaces
        else:
            val = floor(back / 2)
            for i in range(pos, pos+frontNumSpaces, 1):
                checksum += i*val
                backCounter -=1
                if backCounter == 0:
                    back -= 2
                    if front >= back:
                        break
                    backCounter = int(encoding[back])
                    val = floor(back / 2)

        pos += frontNumSpaces
    print(checksum)
   
defragmentDisk('12345')
defragmentDisk('2333133121414131402')
long = open("input.txt").read()
defragmentDisk(long)

