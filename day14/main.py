import math

from pprint import pprint
import itertools
import time


def printGrid(g: dict[tuple[int, int], str], sand: list[tuple[tuple[int, int], bool]]):
    allX = [key[0] for key in g.keys()]
    allY = [key[1] for key in g.keys()]
    min_y = 0
    min_x = min(allX) - 1
    max_y = max(allY) + 1
    max_x = max(allX) + 1
    rows: dict[int, list[str]] = {}
    row: list[str] = []
    allSand = list(map(lambda sand: sand[0], sand))
    print("[", min_x, max_x, "-", min_y, max_y, "]\n")
    for x, y in sorted(
        (itertools.product(range(min_x, max_x), range(min_y, max_y))),
        key=lambda t: t[1],
    ):
        if (x, y) in allSand:
            row.append("o")
        elif (x, y) in g:
            row.append(g[(x, y)])
        else:
            row.append(".")
        if x == max_x - 1:
            rows[y] = row
            row = []
    headers = list(map(str, range(min_x, max_x)))

    for i in reversed(range(max(map(lambda h: len(h), headers)))):
        hrow = "  "
        for header in headers:
            # print(header)
            hrow += header[i]
        print(hrow)

    for i in rows:
        print(f"{i} {''.join(rows[i])}")


with open("input.txt", "r") as inpfile:
    lines: list[list[tuple[int, int]]] = [
        list(map(lambda c: tuple(map(int, c.split(","))), line.split("->")))
        for line in inpfile.read().split("\n")
    ]

    grid: dict[tuple[int, int], str] = {}
    for chunk in lines:
        for i in range(len(chunk) - 1):
            f: tuple[int, int] = chunk[i]
            s: tuple[int, int] = chunk[i + 1]
            f, s = sorted([f, s])

            if f[1] == s[1]:
                # horizontal
                for i in range(f[0], s[0] + 1):
                    grid[(i, f[1])] = "#"
            elif f[0] == s[0]:
                # vertical
                for i in range(f[1], s[1] + 1):
                    grid[(f[0], i)] = "#"
            else:
                raise (Exception("Diagonal line?"))
    currentSand: list[tuple[tuple[int, int], bool]] = [((500, 0), False)]
    print("\033c", end="")
    print("======")
    printGrid(grid, currentSand)
    round = 0
    while True:
        blockers = [*grid.keys(), *list(map(lambda s: s[0], currentSand))]
        (x, y), resting = currentSand[-1]
        if y > max([key[1] for key in grid.keys()]):
            print(len(currentSand[:-1]))
            break
        if resting:
            currentSand.append(((500, 0), False))
        else:
            if not (down := (x, y + 1)) in blockers:
                currentSand[-1] = (down, False)
            elif not (down := (x - 1, y + 1)) in blockers:
                currentSand[-1] = (down, False)
            elif not (down := (x + 1, y + 1)) in blockers:
                currentSand[-1] = (down, False)
            else:
                currentSand[-1] = ((x, y), True)

        # print("\033c", end="")
        # time.sleep(0.033)
        print(f"=={round}===")
        round += 1
        # printGrid(grid, currentSand)
