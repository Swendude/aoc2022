from pprint import pprint
import math


def parse_monkey(monkeyBlock):
    result = {}
    lines = monkeyBlock.split("\n")
    result["ix"] = int(lines[0].strip()[:-1][-1])
    result["items"] = list(map(int, lines[1].strip().split(":")[1].split(",")))
    op = lines[2].split(":")[1].strip().replace("new =", "")
    result["op"] = eval(f"lambda old: {op}")  # I love python
    result["test"] = int(lines[3].split(":")[1].strip().replace("divisible by", ""))
    result["true"] = int(lines[4].split(":")[1].replace("throw to monkey ", ""))
    result["false"] = int(lines[5].split(":")[1].replace("throw to monkey ", ""))
    return result


def find_largest_module(items):
    biggest = max(items)
    while True:
        if all(biggest % x == 0 for x in items):
            break
        biggest = biggest + 1
    return biggest


with open("input.txt") as inpfile:
    monkeyBlocks = inpfile.read().split("\n\n")
    monkeys = sorted(list(map(parse_monkey, monkeyBlocks)), key=lambda mb: mb["ix"])
    monkeyMap = {m["ix"]: m for m in monkeys}
    inspectMap = {m["ix"]: 0 for m in monkeys}
    lcm = find_largest_module([monkey["test"] for monkey in monkeys])
    for round in range(10000):
        # print(round)

        for ix in monkeyMap:
            # inspect
            monkey = monkeyMap[ix]
            # print(f"Monkey {ix} inspects items with a worry level {monkey['items']}")
            monkey["items"] = list(map(monkey["op"], monkey["items"]))
            monkey["items"] = list(map(lambda n: n % lcm, monkey["items"]))

            # inspected_items = list(map(monkey["op"], monkey["items"]))
            # print(f"Monkey {ix} after inspecting {monkey['items']}")
            inspectMap[ix] += len(monkey["items"])

            # # bore
            # monkey["items"] = list(
            #     map(lambda item: math.floor(item / 3), monkey["items"])
            # )
            # print(f"Monkey {ix} after boring {monkey['items']}")

            # throw
            for item in monkey["items"]:
                if item % monkey["test"] == 0:
                    # print(f"Monkey {ix} throws item to {monkey['true']}")
                    monkeyMap[monkey["true"]]["items"].append(item)
                else:
                    # print(f"Monkey {ix} throws item to {monkey['false']}")
                    monkeyMap[monkey["false"]]["items"].append(item)
            monkey["items"] = []
            # print("===")
        # pprint(monkeyMap)
        pprint(inspectMap)
        print("======ROUND=======")

    first, second = sorted(inspectMap.values(), reverse=True)[:2]
    print(first * second)
