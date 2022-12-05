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


def isContaining_denis(first, second):
    firstNr = first[0]
    secondNr = first[1]
    thirdNr = second[0]
    fourthNr = second[1]
    return (firstNr >= thirdNr and firstNr <= fourthNr) or (
        secondNr >= thirdNr and secondNr <= fourthNr
    )


with open("input.txt", "r") as inpfile:
    result = 0
    for line in inpfile.readlines():
        line = line.strip()
        first, second = [tuple(map(int, f.split("-"))) for f in line.split(",")]
        if isContaining(first, second) or isContaining(second, first):
            if not (
                isContaining_denis(first, second) or (isContaining_denis(second, first))
            ):
                print(line)
    # print(result)
