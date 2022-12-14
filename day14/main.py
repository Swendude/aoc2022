with open("input_test.txt", "r") as inpfile:
    lines: list[list[tuple[int, int]]] = [
        list(map(lambda c: tuple(map(int, c.split(","))), line.split("->")))
        for line in inpfile.read().split("\n")
    ]

    all_y = [item[1] for sublist in lines for item in sublist]
    all_x = [item[0] for sublist in lines for item in sublist]
    # print(min(all_x))
    # print(max(all_y))
    grid: list[list[str]] = [[]]
    for chunk in lines:
        for i in range(len(chunk) - 1):
            f: tuple[int, int] = chunk[i]
            s: tuple[int, int] = chunk[i + 1]
            print(f, s)
