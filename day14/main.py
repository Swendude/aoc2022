<<<<<<< HEAD
with open("input_test.txt", "r") as inpfile:
=======
import math
import tqdm
from pprint import pprint
import itertools
import time


def printGrid(
    g: dict[tuple[int, int], str],
    sand: list[tuple[tuple[int, int], bool]],
):
    allX = [key[0] for key in g.keys()]
    allY = [key[1] for key in g.keys()]
    min_y = 0
    min_x = min(allX) - 10
    max_y = max(allY) + 5
    max_x = max(allX) + 10
    rows: dict[int, list[str]] = {}
    row: list[str] = []
    allSand = list(map(lambda sand: sand[0], sand))
    print("[", min_x, max_x, "-", min_y, max_y, "]\n")
    for x, y in sorted(
        (itertools.product(range(min_x, max_x), range(min_y, max_y))),
        key=lambda t: t[1],
    ):
        if (x, y) in allSand:
            row.append("⚠️")
        elif y == (max_y + 2):
            row.append("🪨")
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
        print(f"{i}\t {''.join(rows[i])}")


with open("input.txt", "r") as inpfile:
>>>>>>> 1ff88b51d94a448d04131bdad383a0dbfb15f37a
    lines: list[list[tuple[int, int]]] = [
        list(map(lambda c: tuple(map(int, c.split(","))), line.split("->")))
        for line in inpfile.read().split("\n")
    ]

<<<<<<< HEAD
    all_y = [item[1] for sublist in lines for item in sublist]
    all_x = [item[0] for sublist in lines for item in sublist]
    # print(min(all_x))
    # print(max(all_y))
    grid: list[list[str]] = [[]]
=======
    grid: dict[tuple[int, int], str] = {}
>>>>>>> 1ff88b51d94a448d04131bdad383a0dbfb15f37a
    for chunk in lines:
        for i in range(len(chunk) - 1):
            f: tuple[int, int] = chunk[i]
            s: tuple[int, int] = chunk[i + 1]
<<<<<<< HEAD
            print(f, s)
=======
            f, s = sorted([f, s])

            if f[1] == s[1]:
                # horizontal
                for i in range(f[0], s[0] + 1):
                    grid[(i, f[1])] = "🪨"
            elif f[0] == s[0]:
                # vertical
                for i in range(f[1], s[1] + 1):
                    grid[(f[0], i)] = "🪨"
            else:
                raise (Exception("Diagonal line?"))
    currentSand: list[tuple[tuple[int, int], bool]] = [((500, 0), False)]

    toVisit: list[tuple[int, int]] = []
    floor = max([key[1] for key in grid.keys()]) + 1
    round = 0

    def play():
        while True:
            yield

    blockers = set([*grid.keys(), *list(map(lambda s: s[0], currentSand))])

    for _ in tqdm.tqdm(play()):
        (x, y), resting = currentSand[-1]
        if currentSand[-1] == ((500, 0), True):
            break
        if resting:
            blockers.add(currentSand[-1][0])
            if len(toVisit) and (next := toVisit.pop()):
                currentSand.append((next, False))
            else:
                currentSand.append(((500, 0), False))
        else:
            if y == floor:
                currentSand[-1] = ((x, y), True)
            elif not (down := (x, y + 1)) in blockers:
                if not (x, y) in toVisit:
                    toVisit.append((x, y))
                currentSand[-1] = (down, False)
            elif not (down := (x - 1, y + 1)) in blockers:
                if not (x, y) in toVisit:
                    toVisit.append((x, y))
                currentSand[-1] = (down, False)
            elif not (down := (x + 1, y + 1)) in blockers:
                if not (x, y) in toVisit:
                    toVisit.append((x, y))
                currentSand[-1] = (down, False)
            else:
                currentSand[-1] = ((x, y), True)

    # printGrid(grid, currentSand)
    print(len(currentSand))
>>>>>>> 1ff88b51d94a448d04131bdad383a0dbfb15f37a
