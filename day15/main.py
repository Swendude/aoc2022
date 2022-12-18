import re
from typing import NamedTuple
from pprint import pprint
from tqdm import tqdm
import time
import itertools

Position = NamedTuple("Position", [("right", int), ("down", int)])
Sensor = NamedTuple("Sensor", [("sensor", Position), ("beacon", Position)])
pattern = re.compile(
    r"Sensor at x=(-*\d+), y=(-*\d+): closest beacon is at x=(-*\d+), y=(-*\d+)"
)


def manhattan(p1: Position, p2: Position) -> int:
    return sum([abs(p1[0] - p2[0]), abs(p1[1] - p2[1])])


# print(manhattan(Position(5, -5), Position(-5, 0)))


def printGrid(sensors: list[Sensor], empties: list[Position]):
    all_r = [r for p in [[s[0], b[0]] for (s, b) in sensors] for r in p]
    all_d = [d for p in [[s[1], b[1]] for (s, b) in sensors] for d in p]

    rs = list(range(min(all_r), max(all_r) + 1))

    headers = list(map(str, rs))
    max_h_len = max(map(lambda h: len(h), headers))
    hrow: list[str] = []
    for i in reversed(range(max_h_len)):

        for h in headers:
            try:
                hrow.append(h[i])
            except IndexError:
                hrow.append(" ")
        print("\t", "".join(hrow))
        hrow = []

    row: list[str] = []
    beaconsPoss = [s[1] for s in sensors]
    sensorPoss = [s[0] for s in sensors]

    for d in range(min(all_d), max(all_d) + 1):
        for r in range(min(rs), max(rs) + 1):

            if (r, d) in beaconsPoss:
                row.append("B")
            elif (r, d) in sensorPoss:
                row.append("S")
            elif (r, d) in empties:
                row.append("E")
            else:
                row.append(".")
        print(f"{d}\t", "".join(row))
        row = []


with open("input.txt") as inpfile:
    sensors: list[Sensor] = []
    for line in inpfile.read().split("\n"):
        match = re.match(pattern, line)
        if match:
            s_r, s_d, b_r, b_d = match.groups()
            sensors.append(
                Sensor(Position(int(s_r), int(s_d)), Position(int(b_r), int(b_d)))
            )

        else:
            raise (Exception(f'Can/t match line "{line}"'))

    all_r = [s[1][0] for s in sensors]
    rs = list(range(min(all_r), max(all_r) + 1))
    all_d = [s[1][1] for s in sensors]
    ds = list(range(min(all_d), max(all_d) + 1))
    beaconsPoss = [s[1] for s in sensors]

    def merge(chunks: list[tuple[int, int]]):
        saved: list[int] = list(chunks[0])
        for st, en in sorted([sorted(t) for t in chunks]):
            if st <= saved[1]:
                saved[1] = max(saved[1], en)
            else:
                yield tuple(saved)
                saved[0] = st
                saved[1] = en
        yield tuple(saved)

    def doStuff():
        lineMax = 4000000
        sensor_mins = list(map(lambda s: (s, manhattan(s[0], s[1])), sensors))
        for lineCheck in tqdm(range(lineMax + 1)):
            line_chuncks: list[tuple[int, int]] = []
            for (s, b), min_dist in sensor_mins:
                vert_dist = abs(s[1] - lineCheck)
                if vert_dist > min_dist:
                    # no need to check
                    continue

                hor_dist_left = min_dist - vert_dist

                line_chuncks.append((s[0] - hor_dist_left, s[0] + hor_dist_left))
            continues_chunks = list(merge(sorted(line_chuncks)))
            if len(continues_chunks) > 1:
                print(continues_chunks)
                print(
                    lineCheck,
                    continues_chunks[1][0] - 1,
                    ((continues_chunks[1][0] - 1) * 4000000) + lineCheck,
                )
                break
            line_chuncks = []

    doStuff()
