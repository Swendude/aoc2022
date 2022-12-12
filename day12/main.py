import itertools
from pprint import pprint
import math

levels = list("abcdefghijklmnopqrstuvwxyz")


def check_neighbours(current, hmap, tdist, unvisited):
    for dy, dx in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
        try:
            current_parsed = list(map(int, current.split(",")))
            # print(current_parsed)
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
            # print("Checking: ", current, cur_val)
            if nb_coords in unvisited:

                # print("\t check nb: ", nb_coords, nb_val)
                if current != nb_coords and (
                    levels.index(nb_val) <= levels.index(cur_val)
                    or levels.index(nb_val) == levels.index(cur_val) + 1
                ):
                    # print(tdist[current])
                    new_dist = tdist[current] + 1
                    if new_dist < tdist[nb_coords]:
                        # print("\t\tsetting: ", new_dist)
                        tdist[nb_coords] = new_dist

        except Exception as e:
            # print("SKIPPING", e)
            continue
    unvisited.remove(current)
    return hmap, tdist, unvisited


with open("input.txt", "r") as inpfile:
    hmap = list(map(list, inpfile.read().split("\n")))
    tdist = {
        f"{y},{x}": math.inf
        for y, x in itertools.product(range(len(hmap)), range(len(hmap[0])))
    }
    current = None
    destination = None
    unvisited = []
    for y, row in enumerate(hmap):
        for x, col in enumerate(hmap[y]):
            if hmap[y][x] == "S":
                current = f"{y},{x}"
            if hmap[y][x] == "E":
                destination = f"{y},{x}"
            unvisited.append(f"{y},{x}")

    tdist[current] = 0
    while True:
        print(len(unvisited))
        hmap, tdist, unvisited = check_neighbours(current, hmap, tdist, unvisited)
        if not destination in unvisited:
            print(tdist[destination])
            break
        # pprint(tdist)
        current = min(
            filter(lambda kv: kv[0] in unvisited, tdist.items()), key=lambda kv: kv[1]
        )[0]

    # print(initial_node)
    # pprint(hmap)
    # pprint(tdist)
