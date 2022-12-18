from tqdm import tqdm
from typing import Union, Literal, NamedTuple
from pprint import pprint
import os
from tqdm import tqdm
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
    "BlockPosition", [("resting", bool), ("rockI", int), ("rockR", int), ("rockH", int)]
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


def gridMax(g: Grid) -> int:
    if not grid:
        return 0
    return max(map(lambda b: b.rockH + len(rocks[b.rockI]), g))


def printGrid(g: Grid, w: int = 7) -> None:
    maxH = max(10, gridMax(g))
    print(" ", "".join(["-" for _ in range(w)]))
    rockCells = [blockToCells(bp) for bp in grid]

    for row in reversed(range(maxH)):
        sRow: str = ""
        for col in range(w):
            rock_here = [i for (i, rc) in enumerate(rockCells) if (col, row) in rc]
            if len(rock_here) > 1:
                sRow += str("!")
            elif rock_here:
                # sRow += str(rock_here[0])
                sRow += str("#")
            else:
                sRow += "."

        print(str(row).ljust(1), sRow)
        sRow = ""
    print(" ", "".join([str(c) for c in range(w)]))


def hits(bp: BlockPosition):
    bpCells = set(blockToCells(bp))
    # filledCells = set(
    #     [item for sublist in [blockToCells(bp) for bp in g] for item in sublist]
    # )
    return bool(len(bpCells.intersection(blockers)))


def drop(bp: BlockPosition) -> BlockPosition:
    return BlockPosition(bp.resting, bp.rockI, bp.rockR, bp.rockH - 1)


def blow(bp: BlockPosition, mod: int) -> BlockPosition:
    bw = blockWidth(bp)
    if bp.rockR + bw + mod < 8 and bp.rockR + mod >= 0:
        return BlockPosition(bp.resting, bp.rockI, bp.rockR + mod, bp.rockH)
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
    if serialized in [state[0] for state in states]:
        # print("CYCLE:")
        # print(gridH)
        # print([state[1] for state in states if state[0] == serialized][0])
        # print(gridH - [state[1] for state in states if state[0] == serialized][0])
        return (
            rockN - [state[2] for state in states if state[0] == serialized][0],
            gridH - [state[1] for state in states if state[0] == serialized][0],
        )
    states.append((serialized, gridH, rockN))

    # print("--", serialized)


hs: list[int] = []

with open("input_test.txt", "r") as inpfile:
    start = time.time()
    jets: list[str] = list(inpfile.read().strip())
    # grid: Grid = [BlockPosition(False, 0, 2, 3)]
    grid: Grid = []
    jetI = 0
    rockI = 0
    rockM = 2022
    while True:
        print(rockI)
        rockR = 2
        rockH = gridH + 3
        grid.append(BlockPosition(False, rockI % len(rocks), rockR, rockH))
        hitted = False
        while not hitted:
            # os.system("cls" if os.name == "nt" else "clear")
            # print(grid[-1])
            # printGrid(grid)
            # # time.sleep(0.2)
            currentJet = jets[jetI % len(jets)]

            # blow
            blown = blow(grid[-1], 1 if currentJet == ">" else -1)
            if not hits(blown):
                grid[-1] = blown

            # fall
            dropped = drop(grid[-1])

            if hits(dropped) or dropped.rockH < 0:
                gridH = updateBlockers(grid[-1], blockers, gridH)
                cycle_dh = saveState(
                    blockers, rockI % len(rocks), jetI % len(jets), gridH, rockI
                )
                if cycle_dh:
                    rockI += math.floor((rockM - rockI) / cycle_dh[0]) * cycle_dh[0]
                    gridH += math.floor((rockM - rockI) / cycle_dh[0]) * cycle_dh[1]
                hitted = True
                # input()
            else:
                grid[-1] = dropped

            jetI += 1
        rockI += 1
        if rockI == rockM:
            break

    print(time.time() - start, "s")
    print(gridMax(grid))
    print(gridH)
