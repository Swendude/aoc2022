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

    def travel(
        target_list: list[str],
        routing: dict[str, Valve],
        startOpened: list[str] = [],
    ) -> tuple[int, int, list[str]]:
        current = target_list[0]
        opened = list(startOpened)
        total = 0
        minutes = 0
        for target in target_list[1:]:
            minutes_passed = routing[current].reachables[target][0] + 1
            minutes += minutes_passed

            total += minutes_passed * sum([routing[v].fr for v in opened])

            opened.append(target)
            current = target

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
    max_minutes = 26

    def get_flowr_minute(routing: dict[str, Valve], opened: list[str]) -> int:
        return sum([routing[v].fr for v in opened])

    def finalize_route(
        route: tuple[int, int, list[str]], max_minutes: int, routing: dict[str, Valve]
    ):
        return route[1] + get_flowr_minute(routing, route[-1]) * (
            max_minutes - route[0]
        )

    # your_travel = travel(["AA", "JJ", "BB", "CC"], valvesRouting)
    # el_travel = travel(["AA", "DD", "HH", "EE"], valvesRouting)
    # print(your_travel, el_travel)
    # print(
    #     finalize_route(your_travel, max_minutes, valvesRouting)
    #     + finalize_route(el_travel, max_minutes, valvesRouting)
    # )

    result_pairs: dict[tuple[str, ...], tuple[int, int, list[str]]] = {}
    target_valves = [key for key in valvesRouting if valvesRouting[key].fr]

    perms: set[tuple[str, ...]] = {("AA",)}
    current_l = 1
    result_pairs[("AA",)] = (0, 0, [])
    while current_l <= len(target_valves) + 1:
        print(current_l)
        for np in [p for p in perms if len(p) == current_l]:
            for option in target_valves:

                if option in np or result_pairs[np][0] > max_minutes:
                    continue
                result_pairs[(*np, option)] = add_t(
                    result_pairs[np],
                    travel(
                        [np[-1], option],
                        valvesRouting,
                        result_pairs[np][-1],
                    ),
                )

                if result_pairs[(*np, option)][0] < 30:
                    perms.add((*np, option))

        current_l += 1

    # your_travel = result_pairs[("AA", "JJ", "BB", "CC")]
    # their_travel = result_pairs[("AA", "DD", "HH", "EE")]
    # print(
    #     finalize_route(your_travel, 26, valvesRouting)
    #     + finalize_route(their_travel, 26, valvesRouting)
    # )
    l = target_valves
    # print(l)
    # l = ["BB", "CC", "DD", "JJ"]
    options: list[tuple[tuple[str, ...], tuple[str, ...]]] = []
    splits_seen: list[
        tuple[
            tuple[str, ...],
            tuple[str, ...],
        ]
    ] = []
    for p in permutations(l):
        for i in range(1, len(p)):
            # if (p[1:], p[:1]) in splits_seen:
            #     print("skipped")
            #     continue
            # splits_seen.append((p[:1], p[1:]))
            options += [
                (("AA", *lps[0]), ("AA", *lps[1]))
                for lps in list(product(permutations(p[:i]), permutations(p[i:])))
            ]
    # pprint(options)
    # pprint([option for option in options if option[0] == ("AA", "BB", "DD")])
    # print((("AA", "JJ", "BB", "CC"), ("AA", "DD", "HH", "EE")) in options)
    # print((("AA", "DD", "HH", "EE"), ("AA", "JJ", "BB", "CC")) in options)

    # l = target_valves
    # print(target_valves)
    # options: list[tuple[tuple[str, ...], tuple[str, ...]]] = []
    # for i in range(0, len(l)):
    #     options += [
    #         (("AA", *l[0]), ("AA", *l[1]))
    #         for l in list(product(permutations(l[:i]), permutations(l[i:])))
    #     ]
    # pprint(options)

    paths = [
        (
            l,
            finalize_route(result_pairs[l[0]], 26, valvesRouting)
            + finalize_route(result_pairs[l[1]], 26, valvesRouting),
        )
        for l in options
    ]

    # # print(len(options))
    pprint(max([path for path in paths], key=lambda t: t[1]))
    # paths = [
    #     (v[0], finalize_route(v, 30, valvesRouting), k)
    #     for (k, v) in result_pairs.items()
    #     if v[0] <= 30
    # ]
    # pprint(max(paths, key=lambda t: t[1]))
