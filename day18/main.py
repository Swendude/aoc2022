from pprint import pprint
from itertools import product


Coord = tuple[int, int, int]


def add_(c1: Coord, c2: Coord) -> Coord:
    return Coord(c + c_ for (c, c_) in zip(c1, c2))


# x  y  z
# 0, 0, 0
#


nb_coords: list[Coord] = [
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (-1, 0, 0),
    (0, -1, 0),
    (0, 0, -1),
]


def enclosed(c: Coord, grid: set[Coord], openCells: set[Coord] = set()) -> bool:
    # if openCells:
    #     print("Checking with OC", c)
    cx, cy, cz = c
    all_x: list[int] = [cell[0] for cell in grid]
    all_y: list[int] = [cell[1] for cell in grid]
    all_z: list[int] = [cell[2] for cell in grid]
    max_x, max_y, max_z = max(all_x), max(all_y), max(all_z)
    min_x, min_y, min_z = min(all_x), min(all_y), min(all_z)
    # x up
    xup_enclosed = False
    for x in range(cx, max_x + 1):
        cell = (x, cy, cz)
        if cell in openCells:
            xup_enclosed = False
            break
        if cell in grid:
            xup_enclosed = True
            break

    # x down
    xdown_enclosed = False
    for x in reversed(range(min_x, cx + 1)):
        cell = (x, cy, cz)
        if cell in openCells:
            xdown_enclosed = False
            break
        if cell in grid:
            xdown_enclosed = True
            break
    # y up
    yup_enclosed = False
    for y in range(cy, max_y + 1):
        cell = (cx, y, cz)
        if cell in openCells:
            yup_enclosed = False
            break
        if cell in grid:
            yup_enclosed = True
            break
    # y down
    ydown_enclosed = False
    for y in reversed(range(min_y, cy + 1)):
        cell = (cx, y, cz)
        if cell in openCells:
            ydown_enclosed = False
            break
        if cell in grid:
            ydown_enclosed = True
            break
    # z up
    zup_enclosed = False
    for z in range(cz, max_z + 1):
        cell = (cx, cy, z)
        if cell in openCells:
            zup_enclosed = False
            break
        if cell in grid:
            zup_enclosed = True
            break
    # z down
    zdown_enclosed = False
    for z in reversed(range(min_z, cz + 1)):
        cell = (cx, cy, z)
        if cell in openCells:
            zup_enclosed = False
            break
        if cell in grid:
            zdown_enclosed = True
            break
    # print(c)
    # print(
    #     xup_enclosed,
    #     xdown_enclosed,
    #     ydown_enclosed,
    #     yup_enclosed,
    #     zdown_enclosed,
    #     zup_enclosed,
    # )
    if (
        xup_enclosed
        and xdown_enclosed
        and ydown_enclosed
        and yup_enclosed
        and zdown_enclosed
        and zup_enclosed
    ):

        return True
    else:

        return False


def generate_nb(coord: Coord) -> set[Coord]:
    return set([add_(coord, nbc) for nbc in nb_coords])


def visualize(grid: set[Coord]):
    all_x: list[int] = [cell[0] for cell in grid]
    all_y: list[int] = [cell[1] for cell in grid]
    all_z: list[int] = [cell[2] for cell in grid]
    all_cells = set(
        product(
            range(min(all_x), max(all_x) + 1),
            range(min(all_y), max(all_y) + 1),
            range(min(all_z), max(all_z) + 1),
        )
    )
    max_x, max_y, max_z = max(all_x), max(all_y), max(all_z)
    min_x, min_y, min_z = min(all_x), min(all_y), min(all_z)
    reachable_empties = set(
        filter(lambda r: not enclosed(r, grid), all_cells.difference(grid))
    )

    for z in range(min_z, max_z + 1):
        print("=", z, "=" * (max_y - 1))
        for x in range(min_x, max_x + 1):
            row: list[str] = []
            for y in range(min_y, max_y + 1):
                if (x, y, z) in grid:
                    row.append("#")
                elif (x, y, z) in reachable_empties:
                    row.append(",")
                elif enclosed((x, y, z), grid, reachable_empties):
                    row.append("0")
                else:
                    row.append(".")
            print(x, "".join(row))
            row = []


with open("input.txt", "r") as inpfile:
    grid: set[Coord] = set()
    for line in inpfile:
        grid.add(tuple([int(v) for v in line.strip().split(",")]))
    # visualize(grid)
    counts: dict[Coord, tuple[bool, int]] = {}
    total = 0
    all_x: list[int] = [cell[0] for cell in grid]
    all_y: list[int] = [cell[1] for cell in grid]
    all_z: list[int] = [cell[2] for cell in grid]
    all_cells = set(
        product(
            range(min(all_x), max(all_x) + 1),
            range(min(all_y), max(all_y) + 1),
            range(min(all_z), max(all_z) + 1),
        )
    )
    max_x, max_y, max_z = max(all_x), max(all_y), max(all_z)
    min_x, min_y, min_z = min(all_x), min(all_y), min(all_z)
    # print("x: ", min_x, max_x)
    # print("y: ", min_y, max_y)
    # print("z: ", min_z, max_z)

    for cell in all_cells:
        if cell in grid:
            nbs = generate_nb(cell)
            openCells = nbs.difference(grid)
            counts[cell] = (True, len(openCells))
        if cell not in grid:
            nbs = generate_nb(cell)
            openCells = nbs.difference(all_cells.difference(grid))
            counts[cell] = (False, len(openCells))
    emptyCells = {k: v for (k, v) in counts.items() if not v[0]}
    # print(emptyCells)
    # print(1, 2, 0)
    # print(enclosed((0, 0, 0), grid))
    # enc

    total_filled = {
        coord: (inGrid, openSides)
        for (coord, (inGrid, openSides)) in counts.items()
        if inGrid
    }
    total = sum([openSides for (_, openSides) in total_filled.values()])
    # print("Enclosed:")
    insideOpen = 0
    reachable_empties = set(
        filter(lambda r: not enclosed(r, grid), all_cells.difference(grid))
    )
    for c in emptyCells:
        if enclosed(c, grid, reachable_empties):
            # print("\t", c, counts[c])
            insideOpen += counts[c][1]
    print(insideOpen)
    print(total - insideOpen)
