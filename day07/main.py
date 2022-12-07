from pprint import pprint

with open("input_test.txt") as inpfile:

    lines = inpfile.readlines()
    fs = {"dirs": {}}
    lines = list(map(lambda l: l.strip().split(" "), lines))
    cur_path = []

    for line in lines:
        # print("LINE: ", line)
        cur_dir = fs
        for path in cur_path:
            cur_dir = cur_dir["dirs"][path]

        if line[0] == "$":
            if line[1] == "cd":
                if line[2] == "..":
                    cur_path = cur_path[:-1]
                else:
                    cur_path.append(line[2])
                    if not line[2] in cur_dir["dirs"]:
                        cur_dir["dirs"][line[2]] = {"files": [], "dirs": {}}
            if line[1] == "ls":
                pass
                # ipc = 1
                # while (pc + ipc) < (len(lines) - 1) and lines[pc + ipc][0] != "$":
                #     inner_line = lines[pc + ipc]
                #     cur_dir.append(lines)
                #     ipc += 1

                # pc += ipc + 1
        else:

            if line[0] == "dir":
                pass
                # cur_dir["dirs"][line[2]] = {"files": [], "dirs": {}}
            else:
                cur_dir["files"].append(line)
        # print("FS: ", fs)
pprint(fs)


def calcate_size(files):

    return sum([int(file[0]) for file in files])


dirs_size = []


def get_size(name, directory):
    total = 0
    for dir in directory["dirs"]:
        size = get_size(dir, directory["dirs"][dir])
        total += size
    total += calcate_size(directory["files"])
    dirs_size.append((name, total))
    return total


# def get_small_dirs(directory, size):
#     small_dirs_size = []
#     size = get_size(directory)
#     if size > size:
#         small_dirs_size.append(size)
#     for dir in directory["dirs"]:
#         small_dirs_size += get_small_dirs(directory["dirs"][dir], size)
#     return small_dirs_size


# print(get_size(fs["dirs"]["/"]))
total_size = 70000000
required_space = 30000000
space_taken = get_size("/", fs["dirs"]["/"])
space_left = total_size - space_taken
to_delete = required_space - space_left

print(to_delete)
get_size("/", fs["dirs"]["/"])
print(
    sorted(
        list(filter(lambda ns: ns[1] > to_delete, dirs_size)), key=(lambda ns: ns[1])
    )
)
# print(get_small_dirs(fs["dirs"]["/"], to_delete))
