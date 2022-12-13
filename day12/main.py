import itertools
from pprint import pprint
import math
from copy import deepcopy

levels = list("abcdefghijklmnopqrstuvwxyz")


def check_neighbours(current, hmap, tdist, unvisited):
    for dy, dx in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
        try:
            current_parsed = list(map(int, current.split(",")))
            nb_coords = f"{current_parsed[0] + dy},{current_parsed[1] + dx}"
            nb_val = hmap[current_parsed[0] + dy][current_parsed[1] + dx]
            if nb_val == "S":
                nb_val = "a"
            if nb_val == "E":
                nb_val = "z"
            cur_val = hmap[current_parsed[0]][current_parsed[1]]
            if cur_val == "S":
                cur_val = "a"
            if cur_val == "E":
                cur_val = "z"

            if nb_coords in unvisited:
                if current != nb_coords and (
                    levels.index(nb_val) >= levels.index(cur_val)
                    or levels.index(nb_val) == levels.index(cur_val) - 1
                ):

                    new_dist = tdist[current] + 1
                    if new_dist < tdist[nb_coords]:

                        tdist[nb_coords] = new_dist

        except Exception as e:

            continue
    unvisited.remove(current)
    return hmap, tdist, unvisited


with open("input.txt", "r") as inpfile:
    hmap = list(map(list, inpfile.read().split("\n")))
    tdist = {
        f"{y},{x}": math.inf
        for y, x in itertools.product(range(len(hmap)), range(len(hmap[0])))
    }
    start = None
    current = None

    destination = None
    unvisited = []
    for y, row in enumerate(hmap):
        for x, col in enumerate(hmap[y]):
            if hmap[y][x] == "S":
                destination = f"{y},{x}"
            if hmap[y][x] == "E":
                current = f"{y},{x}"
                start = f"{y},{x}"
            unvisited.append(f"{y},{x}")

    tdist[current] = 0
    dists = []
    while True:
        print(len(unvisited))
        hmap, tdist, visited = check_neighbours(current, hmap, tdist, unvisited)
        if not destination in unvisited:
            print(tdist)
            for coords in tdist:
                coordsP = list(map(int, coords.split(",")))
                if hmap[coordsP[0]][coordsP[1]] == "a":
                    dists.append(tdist[coords])
            break
        current = min(
            filter(lambda kv: kv[0] in unvisited, tdist.items()),
            key=lambda kv: kv[1],
        )[0]
    print(min(dists))
