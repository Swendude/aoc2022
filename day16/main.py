import time
import re
from pprint import pprint
from typing import NamedTuple, Union, Iterable
from itertools import permutations, product
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
    # pprint(valvesRouting)
    # calculated: list[list[str]] = []

    def travel(
        target_list: list[str],
        routing: dict[str, Valve],
        startOpened: list[str] = [],
    ) -> tuple[int, int, list[str]]:
        # print("INCOMING T: ", target_list)
        current = target_list[0]
        opened = list(startOpened)
        total = 0
        # target: Union[None, str] = None
        minutes = 0
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

            opened.append(target)
            current = target

        # total += (30 - minutes) * sum([routing[v].fr for v in opened])
        return (minutes, total, opened)

    def add_t(
        t1: tuple[int, int, list[str]], t2: tuple[int, int, list[str]]
    ) -> tuple[int, int, list[str]]:
        return (t1[0] + t2[0], t1[1] + t2[1], t2[2])

    # print(
    #     travel(["AA", "DD", "BB", "JJ", "HH", "EE", "CC"], valvesRouting),
    # )
    # print(
    #     add_t(
    #         travel(["AA", "DD", "BB"], valvesRouting),
    #         travel(["BB", "JJ", "HH", "EE", "CC"], valvesRouting, ["DD", "BB"]),
    #     )
    # )

    # target_lists = permutations([key for key in valvesRouting if valvesRouting[key].fr])

    # IF I CAN GENERATE ALL PERMUTATIONS FOR N = n - 1 I CAN GENERATE ALL PERMUTATIONS FOR N

    result_pairs: dict[tuple[str, ...], tuple[int, int, list[str]]] = {}
    target_valves = [key for key in valvesRouting if valvesRouting[key].fr]
    print(target_valves)
    perms: set[tuple[str, ...]] = {("AA",)}
    current_l = 1
    result_pairs[("AA",)] = (0, 0, [])
    while current_l <= len(target_valves) + 1:
        print(current_l)
        for np in [p for p in perms if len(p) == current_l]:
            for option in target_valves:
                # print(option, np, np in result_pairs, np in perms)
                if option in np or result_pairs[np][0] > 30:
                    continue
                result_pairs[(*np, option)] = add_t(
                    result_pairs[np],
                    travel(
                        [np[-1], option],
                        valvesRouting,
                        result_pairs[np][-1],
                    ),
                )
                # print("adding")
                if result_pairs[(*np, option)][0] < 30:
                    perms.add((*np, option))
                    # print("ADDED: ", (*np, option), result_pairs[(*np, option)][0])
                # else:
                # print("TOO LONG: ", (*np, option), result_pairs[(*np, option)][0])
        current_l += 1

    def get_flowr_minute(routing: dict[str, Valve], opened: list[str]) -> int:
        return sum([routing[v].fr for v in opened])

    # pprint([p for p in perms])
    # pprint(result_pairs)
    # print(len(target_valves))
    # print(max([len(p) for p in perms]))
    paths = [
        (v[0], v[1] + get_flowr_minute(valvesRouting, v[-1]) * (30 - v[0]), v[2], k)
        for (k, v) in result_pairs.items()
        if v[0] <= 30
    ]
    pprint(max(paths, key=lambda t: t[1]))
    # print(max(paths))
    # target_lists = [["DD", "BB", "JJ", "HH", "EE", "CC"]]
    # results: list[int] = []
    # target_valves = [key for key in valvesRouting if valvesRouting[key].fr]

    # result_pairs: dict[tuple[str, ...], tuple[int, int]] = {}

    # for target_list in tqdm(target_lists, total=math.factorial(15)):
    #     # results.append(travel(["AA"] + list(target_list), valvesRouting)[1])
    #     for slice in range(1, len(target_list)):
    #         before, after = target_list[:slice], target_list[slice:]
    #         # print(before, after)
    #         if before not in result_pairs:
    #             if not before[:-1] in result_pairs:
    #                 result_pairs[before] = travel(list(before), valvesRouting)
    #             else:
    #                 # print(list(before[-2:]))
    #                 oneLess_m, oneLess_t = result_pairs[before[:-1]]
    #                 latest_m, latest_t = travel(
    #                     list(before[-2:]), valvesRouting, oneLess_t
    #                 )
    #                 result_pairs[before] = (oneLess_m + latest_m, oneLess_t + latest_t)
    #             break

    #         if after not in result_pairs:
    #             if not after[:-1] in result_pairs:
    #                 result_pairs[after] = travel(list(after), valvesRouting)
    #             else:
    #                 oneLess_m, oneLess_t = result_pairs[after[:-1]]
    #                 latest_m, latest_t = travel(
    #                     list(after[-2:]), valvesRouting, oneLess_t
    #                 )
    #                 result_pairs[after] = (oneLess_m + latest_m, oneLess_t + latest_t)
    #             break
    #         result_pairs[before + after] = (
    #             result_pairs[before][0] + result_pairs[after][0],
    #             result_pairs[before][1] + result_pairs[after][1],
    #         )
    #         break

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
    # print(max(results))
    # pprint(result_pairs)
