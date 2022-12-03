alphabet = "abcdefghijklmnopqrstuvwxyz"
with open("input.txt", "r") as inpfile:
    total = 0
    for line in inpfile:
        line = line.strip()
        half = int(len(line) / 2)
        first, second = line[half:], line[:half]
        common = [c for c in first if c in second][0]
        if common in alphabet:
            total += alphabet.index(common) + 1
        if common in alphabet.upper():
            total += alphabet.upper().index(common) + 27
    print(total)
