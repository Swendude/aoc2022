alphabet = "abcdefghijklmnopqrstuvwxyz"


def groups(elves):
    cur_elf = 0
    while cur_elf < len(elves):
        yield elves[cur_elf : cur_elf + 3]
        cur_elf += 3


with open("input.txt", "r") as inpfile:
    total = 0
    lines = inpfile.readlines()
    for first, second, third in groups(lines):
        common = [c for c in first if c in second and c in third][0]
        if common in alphabet:
            total += alphabet.index(common) + 1
        if common in alphabet.upper():
            total += alphabet.upper().index(common) + 27
    print(total)
