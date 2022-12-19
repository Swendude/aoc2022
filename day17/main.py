from typing import Union, Literal, NamedTuple
from pprint import pprint
import os
import time
import math

block = list[list[Union[Literal[0], Literal[1]]]]

rocks: list[block] = [
    [[1, 1, 1, 1]],
    [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [0, 0, 1], [0, 0, 1]],
    [[1], [1], [1], [1]],
    [[1, 1], [1, 1]],
]

BlockPosition = NamedTuple(
    "BlockPosition", [("rockI", int), ("rockR", int), ("rockH", int)]
)

Grid = list[BlockPosition]
blockers: set[tuple[int, int]] = set()
gridH: int = 0


def blockWidth(b: BlockPosition) -> int:
    return max([len(list(filter(bool, row))) for row in rocks[b.rockI]])


def blockToCells(b: BlockPosition) -> list[tuple[int, int]]:
    results: list[tuple[int, int]] = []
    rock = rocks[b.rockI]
    for row in range(len(rock)):
        for col in range(len(rock[row])):
            if rock[row][col]:
                results.append((col + b.rockR, row + b.rockH))
    return results


# def gridMax(g: Grid) -> int:
#     if not grid:
#         return 0
#     return max(map(lambda b: b.rockH + len(rocks[b.rockI]), g))


# def printGrid(g: Grid, w: int = 7) -> None:
#     maxH = max(10, gridMax(g))
#     print(" ", "".join(["-" for _ in range(w)]))
#     rockCells = [blockToCells(bp) for bp in grid]

#     for row in reversed(range(maxH)):
#         sRow: str = ""
#         for col in range(w):
#             rock_here = [i for (i, rc) in enumerate(rockCells) if (col, row) in rc]
#             if len(rock_here) > 1:
#                 sRow += str("!")
#             elif rock_here:
#                 # sRow += str(rock_here[0])
#                 sRow += str("#")
#             else:
#                 sRow += "."

#         print(str(row).ljust(1), sRow)
#         sRow = ""
#     print(" ", "".join([str(c) for c in range(w)]))


def hits(bp: BlockPosition):
    bpCells = set(blockToCells(bp))
    return bool(len(bpCells.intersection(blockers)))


def drop(bp: BlockPosition) -> BlockPosition:
    return BlockPosition(bp.rockI, bp.rockR, bp.rockH - 1)


def blow(bp: BlockPosition, mod: int) -> BlockPosition:
    bw = blockWidth(bp)
    if bp.rockR + bw + mod < 8 and bp.rockR + mod >= 0:
        return BlockPosition(bp.rockI, bp.rockR + mod, bp.rockH)
    else:
        return bp


def updateBlockers(
    bp: BlockPosition, blockers: set[tuple[int, int]], oldMax: int
) -> int:
    cells = blockToCells(bp)
    blockers.update(cells)
    return max(oldMax, bp.rockH + len(rocks[bp.rockI]))


states: list[tuple[str, int, int]] = []


def saveState(
    blockers: set[tuple[int, int]], rockI: int, jetI: int, gridH: int, rockN: int
) -> Union[tuple[int, int], None]:
    depth = 10
    # print(gridH)
    # print(blockers)
    serializedBlockers = [
        (blocker[0], blocker[1] - gridH)
        for blocker in blockers
        if blocker[1] > (gridH - depth)
    ]
    serialized = str(serializedBlockers) + str(rockI) + str(jetI)
    if old := [state for state in states if state[0] == serialized]:
        last = old[0]
        # print(last)
        # print(
        #     f"CYCLE: saw this same state at iteration {last[-1]}, current iteration {rockN}."
        # )
        # print(f"Difference is {gridH} - {last[1]}= {gridH - last[1]}")
        return (
            rockN - last[2],
            gridH - last[1],
        )
    states.append((serialized, gridH, rockN))


puzzleFile, iterations, correct = [
    ("input_test.txt", 1000000000000, 1514285714288),
    ("input_test.txt", 2022, 3068),
    ("input.txt", 2022, 3090),
    ("input.txt", 1000000000000, 0),
][-1]
with open(puzzleFile, "r") as inpFile:
    cycle_check = True
    start = time.time()
    jets: list[str] = list(inpFile.read().strip())
    jetI = 0
    rockI = 0
    rockM = iterations
    while True:
        print(rockI)
        rockR = 2
        rockH = gridH + 3
        current = BlockPosition(rockI % len(rocks), rockR, rockH)
        hitted = False
        while not hitted:
            currentJet = jets[jetI % len(jets)]

            # blow
            blown = blow(current, 1 if currentJet == ">" else -1)
            if not hits(blown):
                current = blown

            # fall
            dropped = drop(current)
            if hits(dropped) or dropped.rockH < 0:
                gridH = updateBlockers(current, blockers, gridH)
                hitted = True
                if cycle_check:
                    dcycle_dh = saveState(
                        blockers, rockI % len(rocks), jetI % len(jets), gridH, rockI
                    )

                    if dcycle_dh:
                        print(dcycle_dh)
                        cycles_left = rockM - rockI
                        fits = math.floor(cycles_left / dcycle_dh[0])
                        if fits:
                            print(f"Left: {rockM - rockI}, cycle fits {fits} time")
                            deltaH = fits * dcycle_dh[1]
                            gridH += deltaH
                            blockers = {(y, x + deltaH) for (y, x) in blockers}
                            rockI += fits * dcycle_dh[0]

            else:
                current = dropped

            jetI += 1
        rockI += 1
        if rockI == rockM:
            break

    print(time.time() - start, "s")
    print(gridH)
    print(gridH == correct)
