def sub_coords(first, second):
    return [first[0] - second[0], first[1] - second[1]]


def add_coords(first, second):
    return [first[0] + second[0], first[1] + second[1]]


def draw_grid(size, h_pos, t_pos, t_visits):
    row = None
    for y in range(-size, size):
        if row:
            print(row)
        row = ""
        for x in range(-size, size):
            if [x, y] == h_pos:
                row += "H"
            elif [x, y] == t_pos:
                row += "T"
            elif [x, y] == [0, 0]:
                row += "s"
            elif [x, y] in t_visits:
                row += "#"
            else:
                row += "."


with open("input.txt", "r") as inpfile:
    h_pos = [0, 0]
    rope = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    t_visits = [[0, 0]]
    for instruction in inpfile.readlines():
        instruction, amount = instruction.split(" ")
        mod = [0, 0]
        if instruction == "U":
            mod = [0, -1]
        if instruction == "L":
            mod = [-1, 0]
        if instruction == "D":
            mod = [0, 1]
        if instruction == "R":
            mod = [1, 0]

        for i in range(int(amount)):
            h_pos = add_coords(h_pos, mod)
            following = h_pos
            for t_i, t in enumerate(rope):
                t_pos = rope[t_i]
                dif_x, dif_y = sub_coords(following, t_pos)
                distance = abs(dif_x) + abs(dif_y)
                # print(distance)
                if abs(dif_x) > 1 or abs(dif_y) > 1:
                    if dif_x > 0 and dif_y > 0:
                        t_pos = add_coords(t_pos, [1, 1])
                    elif dif_x < 0 and dif_y < 0:
                        t_pos = add_coords(t_pos, [-1, -1])
                    elif dif_x > 0 and dif_y < 0:
                        t_pos = add_coords(t_pos, [1, -1])
                    elif dif_x < 0 and dif_y > 0:
                        t_pos = add_coords(t_pos, [-1, 1])
                    elif dif_x > 0:
                        t_pos = add_coords(t_pos, [1, 0])
                    elif dif_x < 0:
                        t_pos = add_coords(t_pos, [-1, 0])
                    elif dif_y > 0:
                        t_pos = add_coords(t_pos, [0, 1])
                    elif dif_y < 0:
                        t_pos = add_coords(t_pos, [0, -1])
                    print(t_pos)
                    rope[t_i] = t_pos
                following = t_pos
            t_visits.append(rope[-1])
            print(rope)
        # print("INST:", instruction)
        # print("DIF:", dif_x, dif_y)
        # draw_grid(50, h_pos, t_pos, t_visits)
        # print("----")
    print(t_visits)
    print(len(set([str(visit) for visit in t_visits])))
