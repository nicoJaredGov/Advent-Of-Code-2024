#part 1
list1 = []
list2 = []
with open("day1input.txt", mode="r") as file:
    for pair in file.readlines():
        a, b = [int(i) for i in pair.strip().split()]
        list1.append(a)
        list2.append(b)
list1.sort()
list2.sort()
result = sum(abs(a-b) for a,b in zip(list1, list2))
print(result)

#part 2
similarityScore = sum([i*list2.count(i) for i in list1])
print(similarityScore)
