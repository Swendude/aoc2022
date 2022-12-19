import time
import re
from pprint import pprint
from typing import NamedTuple, Union, NewType
from itertools import permutations
from tqdm import tqdm
import math

pattern = re.compile(
    r"Valve ([A-Z]+) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? ([A-Z, ]*)"
)

Valve = NamedTuple("Valve", [("fr", int), ("reachables", dict[str, tuple[int, str]])])


def updateRoutings(
    current: str,
    nb: str,
    old: dict[str, tuple[int, str]],
    new: dict[str, tuple[int, str]],
    dist: int,
) -> dict[str, tuple[int, str]]:
    old = dict(old)
    for nk in new:
        if nk == current:
            continue

        if nk in old and old[nk][0] > (dist + new[nk][0]):
            old[nk] = (dist + new[nk][0], nb)

        elif nk not in old:
            old[nk] = (dist + new[nk][0], nb)

    return old


with open("input_test.txt") as inpfile:
    lines = inpfile.read().split("\n")
    valvesRouting: dict[str, Valve] = {}
    for line in lines:
        match = re.match(pattern, line.strip())
        if match:
            valve, fr, reachable = match.groups()
            valvesRouting[valve] = Valve(
                int(fr),
                {r.strip(): (1, r.strip()) for r in reachable.split(",")},
            )
    # pprint(valvesRouting)
    # start routing, every valve askes the routing table for every reachable and updates with lowest score
    print("building routing...")
    while True:
        before_ser = str(valvesRouting)
        current_valvesRouting = dict(valvesRouting)
        for valve in valvesRouting:
            this_valve = current_valvesRouting[valve]
            current_reachables = dict(this_valve.reachables)
            direct_nbs = [
                r for r in current_reachables if current_reachables[r][0] == 1
            ]
            new_reachables = dict(current_reachables)
            for nb in direct_nbs:
                nb_r = dict(current_valvesRouting[nb].reachables)
                nb_d = current_reachables[nb][0]
                new_reachables = updateRoutings(valve, nb, new_reachables, nb_r, nb_d)
            valvesRouting[valve] = Valve(valvesRouting[valve].fr, new_reachables)
        after_ser = str(valvesRouting)

        if after_ser == before_ser:
            break
    print("routing builded!")

    routings = [len(valvesRouting[v].reachables) for v in valvesRouting]
    print(routings)
    # pprint(valvesRouting["JJ"])

    # print(list(permutations([key for key in valvesRouting if valvesRouting[key].fr])))

    # target_lists = [["DD", "BB", "JJ", "HH", "EE", "CC"]]

    results: list[int] = []
    target_valves = [key for key in valvesRouting if valvesRouting[key].fr]
    result_pairs = []

    def travel(target_list: list[str], valvesRouting: dict[str, Valve]):
        current = "AA"
        opened: list[str] = []
        total = 0
        targetI = 0
        target: Union[None, str] = None
        for _ in range(30):
            added_flow = sum([valvesRouting[v].fr for v in opened])
            total += added_flow
            # print(f"Valves {', '.join(opened)} are open. Producing {added_flow} flow")
            currentRouting = valvesRouting[current]

            if not target:
                if targetI > len(target_list) - 1:
                    # print(f"No more valves")
                    continue
                target = target_list[targetI]
                targetI += 1
                # print(f"Target set to {target}")

            # move to target if not there
            if target != current:
                current = currentRouting.reachables[target][1]
                # print(f"Move to {current}")
            else:
                # print(f"Open {current}")
                opened.append(target)
                target = None
        return total
