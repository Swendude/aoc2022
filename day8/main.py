with open("input.txt", "r") as inpfile:

    lines = inpfile.readlines()
    grid = [list(map(int, line.strip())) for line in lines]

    for row in grid:
        print(row)

    edges = len(grid) * 2 + len(grid[0]) * 2 - 4

    visibles = []
    max = 0
    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[0]) - 1):
            # Check left & right
            current = grid[y][x]
            leftrow = reversed(grid[y][:x])
            rightrow = grid[y][x + 1 :]
            toprow = reversed([grid[i][x] for i in range(0, y)])
            bottomrow = [grid[i][x] for i in range(y + 1, len(grid))]
            print("-----", current)
            scenicscore = 1
            counter = 0
            for tree in leftrow:
                counter += 1
                if tree >= current:
                    break
            print(counter, " left")
            scenicscore = scenicscore * counter
            counter = 0
            for tree in rightrow:
                counter += 1
                if tree >= current:
                    break
            print(counter, " right")
            scenicscore = scenicscore * counter
            counter = 0
            for tree in toprow:
                counter += 1
                if tree >= current:
                    break
            print(counter, " top")
            scenicscore = scenicscore * counter
            counter = 0
            for tree in bottomrow:
                counter += 1
                if tree >= current:
                    break
            print(counter, " bottom")
            scenicscore = scenicscore * counter
            print(y, x, scenicscore)
            if scenicscore > max:

                max = scenicscore
            # blockersleft = [tree for tree in leftrow if tree >= current]
            # blockersright = [tree for tree in rightrow if tree >= current]
            # blockerstop = [tree for tree in toprow if tree >= current]
            # blockersbottom = [tree for tree in bottomrow if tree >= current]
            # if (
            #     not blockersleft
            #     or not blockersright
            #     or not blockersbottom
            #     or not blockerstop
            # ):

            #     visibles.append([y, x])

            # else:
            #     print("CELL: ", grid[y][x], f"{y}, {x}")
            #     print(leftrow)
            #     print("blockers:", blockersleft)
            #     print(toprow)
            #     print("blockers:", blockerstop)
            #     print(rightrow)
            #     print("blockers:", blockersright)
            #     print(bottomrow)
            #     print("blockers:", blockersbottom)
            #     print("--------")
    # visibles = [
    #     [y, x]
    #     for y, x in visibles
    #     if (x != 0) and (y != 0) and (x != len(grid) - 1) and (y != len(grid[0]) - 1)
    # ]
    # print(list(line.strip()))
    # visibles = set([f"{y},{x}" for x, y in visibles])
    # print(visibles)
    # print(edges + len(visibles))
    print(max)
