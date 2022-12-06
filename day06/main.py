with open("input.txt") as inpfile:
    offset = 4
    line = inpfile.readline()
    for i, char in enumerate(line):
        next_four = line[i : i + offset]
        # print(next_four, len(set(next_four)) == 4)
        if len(set(next_four)) == offset:
            print(i + offset, next_four)
            break
