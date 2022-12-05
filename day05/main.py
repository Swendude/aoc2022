from collections import defaultdict
import re


def stackPrint(stack):
    for key in sorted(stack.keys()):
        print(f"{key} => {stack[key]}")


def stackPrintResult(stack):
    res = ""
    for key in sorted(stack.keys()):
        res += f"{stack[key][-1]}"

    print(res)


def parse_stackline(line):
    i = 0
    while i < len(line):
        yield line[i : i + 3]
        i += 4


def parse_stacks(stacks):
    result = defaultdict(list)
    for line in stacks:
        parsed = parse_stackline(line)
        for i, item in enumerate(parsed):
            if item != "   ":
                result[i + 1] = [item[1:-1], *result[i + 1]]

    return result


def parse_moveline(line):
    matcher = re.compile("move (\d*) from (\d*) to (\d*)$")
    amount, fromStack, toStack = re.fullmatch(matcher, line).groups()
    return {"amount": int(amount), "fromStack": int(fromStack), "toStack": int(toStack)}


def modify_stack(stack, mover):
    # print(mover)
    # stackPrint(stack)
    for i in range(mover["amount"]):
        box = stack[mover["fromStack"]].pop()
        stack[mover["toStack"]].append(box)
    return stack


with open("input.txt", "r") as inpfile:
    stacks, moves = inpfile.read().split("\n\n")
    stacksLines = stacks.split("\n")[:-1]
    stack = parse_stacks(stacksLines)
    # stackPrint(stack)
    for move in moves.split("\n"):
        parsed = parse_moveline(move)
        stack = modify_stack(stack, parsed)
    stackPrintResult(stack)
