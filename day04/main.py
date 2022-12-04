def isContaining(first, second):
    return (
        not len(
            [
                num
                for num in range(first[0], first[1] + 1)
                if num in range(second[0], second[1] + 1)
            ]
        )
        == 0
    )


with open("input.txt", "r") as inpfile:
    result = 0
    for line in inpfile.readlines():
        line = line.strip()
        first, second = [tuple(map(int, f.split("-"))) for f in line.split(",")]
        if isContaining(first, second) or isContaining(second, first):
            result += 1
    print(result)
