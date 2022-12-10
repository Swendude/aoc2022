from collections import namedtuple

BufferItem = namedtuple("BufferItem", ["command", "value", "cyclesLeft"])

BufferItem.__repr__ = lambda bi: f"{bi.command} {bi.value} ({bi.cyclesLeft})"
with open("input.txt") as inpfile:
    command_buffer = []
    x = 1
    result = 0
    for cycle in range(220):

        # print("BEGIN", cycle, x)
        # print(list(filter(lambda c: c.cyclesLeft >= 0, command_buffer)))
        # new_buffer = command_buffer.copy()

        for cc, command in enumerate(command_buffer):
            command_buffer[cc] = BufferItem(
                command.command, command.value, command.cyclesLeft - 1
            )
            if command.cyclesLeft == 0:
                x += command.value

        if (cycle) in [19, 59, 99, 139, 179, 219]:
            result += (cycle + 1) * x
        if len(list(filter(lambda c: c.cyclesLeft >= 0, command_buffer))) == 0:
            try:
                command = next(inpfile).strip()
                if command != "noop":
                    command_buffer.append(
                        BufferItem("add", int(command.split(" ")[1]), 1)
                    )
            except Exception as e:

                pass
        # print("END", cycle, x)
        # print(list(filter(lambda c: c.cyclesLeft >= 0, command_buffer)))
        # print("====")
    print(result)
