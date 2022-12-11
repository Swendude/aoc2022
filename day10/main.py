from collections import namedtuple

BufferItem = namedtuple("BufferItem", ["command", "value", "cyclesLeft"])

BufferItem.__repr__ = lambda bi: f"{bi.command} {bi.value} ({bi.cyclesLeft})"
with open("input.txt") as inpfile:
    crt = []
    command_buffer = []
    x = 1
    for cycle in range(241):
        # crt.append(str(cycle))

        for cc, command in enumerate(command_buffer):
            command_buffer[cc] = BufferItem(
                command.command, command.value, command.cyclesLeft - 1
            )
            if command.cyclesLeft == 0:
                x += command.value
        if len(list(filter(lambda c: c.cyclesLeft >= 0, command_buffer))) == 0:
            try:
                command = next(inpfile).strip()
                if command != "noop":
                    command_buffer.append(
                        BufferItem("add", int(command.split(" ")[1]), 1)
                    )
            except Exception as e:
                pass
        print(cycle, x, [x - 1, x, x + 1])
        if (cycle % 40) in [x - 1, x, x + 1]:
            crt += "#"
            # print(crt)
        else:
            crt += "."

    print(crt)
    for i, j in [[0, 40], [40, 80], [80, 120], [120, 160], [160, 200], [200, 240]]:
        # print(i, j)
        print("".join(crt[i:j]))
