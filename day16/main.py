import time
import re
from pprint import pprint
from typing import NamedTuple, Union, Iterable
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


with open("input.txt") as inpfile:
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
    # print(valvesRouting.items())
    # routings = [len(valvesRouting[v].reachables) for v in valvesRouting]
    # print(routings)
    # exit()
    calculated: list[list[str]] = []

    def travel(
        target_list: list[str],
        routing: dict[str, Valve],
        startMinute: int = 0,
    ) -> tuple[int, int]:
        # if target_list in calculated:
        #     print("ERROR")
        #     exit()
        # calculated.append(target_list)

        # print(target_list)
        current = target_list[0]
        opened: list[str] = []
        total = 0
        target: Union[None, str] = None
        minutes = startMinute
        for target in target_list[1:]:
            # print("-")
            # print("c: ", current)
            # print("t: ", target)
            # print("o: ", opened)
            # print("t: ", total)
            # print("m: ", minutes)
            # print(routing[current].reachables)
            # input()
            minutes_passed = routing[current].reachables[target][0] + 1
            minutes += minutes_passed
            total += minutes_passed * sum([routing[v].fr for v in opened])
            if minutes > 30:
                break
            opened.append(target)
            current = target
        total += (30 - minutes) * sum([routing[v].fr for v in opened])
        return (minutes, total)
        # for _ in range(30):
        #     added_flow = sum([valvesRouting[v].fr for v in opened])
        #     total += added_flow
        #     # print(f"Valves {', '.join(opened)} are open. Producing {added_flow} flow")
        #     currentRouting = valvesRouting[current]

        #     if not target:
        #         if targetI > len(target_list) - 1:
        #             # print(f"No more valves")
        #             continue
        #         target = target_list[targetI]
        #         targetI += 1
        #         # print(f"Target set to {target}")

        #     # move to target if not there
        #     if target != current:
        #         current = currentRouting.reachables[target][1]
        #         # print(f"Move to {current}")
        #     else:
        #         # print(f"Open {current}")
        #         opened.append(target)
        #         target = None
        # return total

    target_lists = permutations([key for key in valvesRouting if valvesRouting[key].fr])

    # target_lists = [["DD", "BB", "JJ", "HH", "EE", "CC"]]
    results: list[int] = []
    target_valves = [key for key in valvesRouting if valvesRouting[key].fr]

    result_pairs: dict[tuple[str, ...], tuple[int, int]] = {}

    for target_list in tqdm(target_lists, total=math.factorial(15)):
        # results.append(travel(["AA"] + list(target_list), valvesRouting)[1])
        for slice in range(1, len(target_list)):
            before, after = target_list[:slice], target_list[slice:]
            # print(before, after)
            if before not in result_pairs:
                if not before[:-1] in result_pairs:
                    result_pairs[before] = travel(list(before), valvesRouting)
                else:
                    # print(list(before[-2:]))
                    oneLess_m, oneLess_t = result_pairs[before[:-1]]
                    latest_m, latest_t = travel(
                        list(before[-2:]), valvesRouting, oneLess_t
                    )
                    result_pairs[before] = (oneLess_m + latest_m, oneLess_t + latest_t)
                break

            if after not in result_pairs:
                if not after[:-1] in result_pairs:
                    result_pairs[after] = travel(list(after), valvesRouting)
                else:
                    oneLess_m, oneLess_t = result_pairs[after[:-1]]
                    latest_m, latest_t = travel(
                        list(after[-2:]), valvesRouting, oneLess_t
                    )
                    result_pairs[after] = (oneLess_m + latest_m, oneLess_t + latest_t)
                break
            result_pairs[before + after] = (
                result_pairs[before][0] + result_pairs[after][0],
                result_pairs[before][1] + result_pairs[after][1],
            )
            break

        #         break

        #     #         result_pairs[sp] = (
        #     #             before_m + after_m,
        #     #             before_t + after_t,
        #     #         )

        #     # else:
        #     #     tqdm.write("Shkip")
        #     #     break
        #     # tqdm.write("hit!")
        # # input()
        # #     tail_m, tail_t = travel(
        # #         list(target_list[slice:]),
        # #         valvesRouting,
        # #         sp[-1],
        # #         startMinute=result_pairs[sp][0],
        # #     )
        # #     head_m, head_t = result_pairs[sp]
        # #     if head_t + tail_m <

        # # print(target_list)
        # # print(list(result_pairs.keys()))
        # # input()
        # # break
    print(max(results))
    # pprint(result_pairs)
