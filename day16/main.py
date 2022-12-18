import re
from pprint import pprint
from typing import NamedTuple, Union, NewType
from tqdm import tqdm

pattern = re.compile(
    r"Valve ([A-Z]+) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? ([[A-Z, ]*]*)"
)

Valve = NamedTuple("Valve", [("fr", int), ("reachables", list[str])])


with open("input_test.txt") as inpfile:
    lines = inpfile.read().split("\n")
    valvesg: dict[str, Valve] = {}
    for line in lines:
        match = re.match(pattern, line.strip())
        if match:
            valve, fr, reachable = match.groups()
            valvesg[valve] = Valve(
                int(fr),
                [r.strip() for r in reachable.split(",")],
            )
    all_valves = list(valvesg.keys())
    # pprint(list(valvesg.keys()))

    all_mapped_paths = {}

    all_paths: list[list[str]] = [["AA"]]
    i = 0
    while True:
        print(i)
        # for path in all_paths:
        #     print(i, path)
        # print("----")
        new_paths: list[list[str]] = []
        for path in all_paths:

            if len(path) == 10:
                new_paths.append(path)
            else:
                # print(path[-1], valvesg[path[-1]].reachables)
                for reachable in valvesg[path[-1]].reachables:
                    # print([*path, reachable])
                    new_paths.append([*path, reachable])
            # print(len(new_paths))
        all_paths = new_paths

        i += 1

        if len(list(filter(lambda p: len(p) != 10, all_paths))) == 0:
            break

    for path in all_paths:
        print(i, path)

    # potential_flow: dict[str, list[tuple[list[str], int]]] = {}

    # for valve in valvesg:
    #     potential_flow[valve] = [
    #         ([v], valvesg[v].fr) for v in valvesg[valve].reachables
    #     ]

    # # pprint(potential_flow["AA"])

    # Path = NamedTuple(
    #     "Path",
    #     [
    #         ("steps", list[str]),
    #         ("open", list[str]),
    #         ("frs", list[int]),
    #     ],
    # )
    # # startOptions = potential_flow["AA"]
    # options: list[Path] = [Path(["AA"], [], [])]
    # print(options)
    # new_options: list[tuple[int, list[str], int]] = []

    # for option in potential_flow["AA"]:
    #     for sec_option in potential_flow[option[1][-1]]:
    #         new_options.append(
    #             (
    #                 option[0] + sec_option[0],
    #                 [*option[1], *sec_option[1]],
    #                 option[2] + sec_option[2],
    #             )
    #         )
    # potential_flow["AA"] = new_options

    # pprint(potential_flow["AA"])

    # Path = NamedTuple(
    #     "Path",
    #     [
    #         ("costs", list[int]),
    #         ("visited", list[str]),
    #         ("open", list[str]),
    #         ("frs", list[int]),
    #     ],
    # )
    # startOptions = potential_flow["AA"]
    # options: list[Path] = [
    #     Path([cost], [valve], [valve], [fr]) for (cost, valve, fr) in startOptions
    # ]

    # pprint(options)

    # while True:
    #     # print("---")
    #     # pprint(options)
    #     new_options: list[Path] = []
    #     time_left = list(filter(lambda op: sum(op[0]) <= 30, options))
    #     if not time_left:
    #         break
    #     for option in time_left:
    #         costs, valves, opened, frs = option
    #         if sum(costs) <= 30:
    #             ncost, nvalve, nfr = max(potential_flow[valves[-1]], key=lambda t: t[2])
    #             if nvalve in opened:
    #                 new_options.append(
    #                     Path([*costs, ncost - 1], [*valves, nvalve], opened, frs)
    #                 )
    #             else:
    #                 new_options.append(
    #                     Path(
    #                         [*costs, ncost],
    #                         [*valves, nvalve],
    #                         [*opened, nvalve],
    #                         [*frs, nfr],
    #                     )
    #                 )
    #         else:
    #             new_options.append(option)
    #         options = new_options
    # break

    # pprint(options)
    #     else:
    #         new_options.append(option)
    # options = new_options
    # pprint(options)

    # pprint(potential_flow)
    # pprint(options)
