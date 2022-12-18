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


def generate_nb(coord: Coord) -> set[Coord]:
    return set([add_(coord, nbc) for nbc in nb_coords])


with open("input_test.txt", "r") as inpfile:
    grid: set[Coord] = set()
    for line in inpfile:
        grid.add(tuple([int(v) for v in line.strip().split(",")]))
    # print(grid)
    # counts : dict[Coord, int] = []
    total = 0
    for cell in grid:
        nbs = generate_nb(cell)
        openCells = nbs.difference(grid)
        total += len(openCells)
    print(total)
