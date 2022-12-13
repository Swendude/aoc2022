from pprint import pprint
from typing import Union
import functools

signal = Union[list[list[int]], list[int], int]


def compare(l: signal, r: signal) -> int:
    # print(f"- compare {l} vs {r}")
    orderCorrect = 0
    if isinstance(l, int) and isinstance(r, int):
        if l < r:
            # print("left side is smaller, correct")
            return 1
        elif l == r:
            # print("left and right are the same, no decision")
            return 0
        else:
            # print("right side is smaller, incorrect")
            return -1
    elif not isinstance(l, list):
        return compare([l], r)
    elif not isinstance(r, list):
        return compare(l, [r])
    else:
        for i in range(max(len(r), len(l))):
            # print("-----", list(range(len(l))))
            # print("-- trying index:", i)
            try:
                lefti = l[i]
            except IndexError:
                # print("left ran out first, correct")
                return 1
            try:
                righti = r[i]
            except IndexError:
                # print("right ran out first, incorrect")
                return -1
            # print(f"--Comparing {l} and {r} on index {i}")
            orderCorrect = compare(lefti, righti)
            if orderCorrect != 0:
                # print(f"---decision made for {l} and {r} on index {i}")
                return orderCorrect
    # print("±±±±±±±±±±±±±ERROROROROROR±±±±±±±±±±±±±")
    return 0


with open("input.txt") as inpfile:
    correct: list[int] = []
    # signals: list[list[signal]] = [pair.split("\n") for pair in inpfile.read().split("\n")]

    signals: list[signal] = [
        eval(signal) for signal in inpfile.read().split("\n") if signal
    ]

    markers: list[signal] = [[[2]], [[6]]]
    sortedsignals = sorted(
        signals + markers, key=functools.cmp_to_key(compare), reverse=True
    )
    print((sortedsignals.index(markers[0]) + 1) * (sortedsignals.index(markers[1]) + 1))

    # for i, pair in enumerate(pairs):
    #     print(f"\nPair {i + 1} ==")
    #     if compare(pair[0], pair[1]) == 1:
    #         correct.append(i + 1)

    # print(sum(correct))
