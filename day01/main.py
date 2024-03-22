with open("./input.txt", "r") as inputFile:
    elves = [[]]
    for line in inputFile:
         if line == "\n":
             elves.append([])
         else:
             elves[-1].append(int(line.strip()))
     caloriesPerElf = list(map(sum, elves))
     sortedElves = sorted(caloriesPerElf)
     # print(sortedElves)
    print(sum(sortedElves[-3:]))
