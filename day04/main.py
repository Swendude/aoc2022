def isContaining(first, second):
    return first[0] >= second[0] and first[1] <= second[1]


with open("input.txt", "r") as inpfile:

    result = 0
    for line in inpfile.readlines():
        line = line.strip()
        first, second = [tuple(map(int, f.split("-"))) for f in line.split(",")]
        if isContaining(first, second) or isContaining(second, first):
            result += 1
    print(result)
