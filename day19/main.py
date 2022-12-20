import re
from typing import NamedTuple, Union, Literal

pattern = re.compile(
    r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."
)

Resource = Union[Literal["ore"], Literal["clay"], Literal["obsidian"], Literal["geode"]]

Price = dict[Resource, int]


Blueprint = NamedTuple(
    "Blueprint",
    [
        ("id", int),
        ("ore_price", Price),
        ("clay_price", Price),
        ("obisidian_price", Price),
        ("geode_price", Price),
    ],
)

with open("input_test.txt", "r") as inpfile:
    for line in inpfile.readlines():
        if match := re.match(pattern, line):
            (
                id,
                ore_ore,
                clay_ore,
                obsidian_ore,
                obsidian_clay,
                geode_ore,
                geode_obsidian,
            ) = match.groups()
            Blueprint(
                id,
                {"ore": ore_ore},
                {"ore": clay_ore},,
                {"ore":obsidian_ore,
                "clay":obsidian_clay},
                {
                    "ore":geode_ore,
                    "obisidian":geode_obsidian,
                }
                
            )
