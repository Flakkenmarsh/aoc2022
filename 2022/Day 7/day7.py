file = open('input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]


def print_directory(current_dir, depth):
    tab = ""
    for i in range(depth):
        tab += "  "
    for child in current_dir.children:

        if child.type == "File":
            print(tab, " - ", child.name, child.size)
        else:
            print(tab, " - ", child.name, "(dir) ", child.size)
            print_directory(child, depth+1)


def calculate_sizes(current_dirs):
    if current_dirs.type == "File":
        return current_dirs.size

    size = 0
    for child in current_dirs.children:
        if child.type == "File":
            size += child.size

        current_dirs.size += calculate_sizes(child)
    return current_dirs.size


def part1(current_dir):
    for child in current_dir.children:
        if child.type == "Directory":
            if child.size <= 100000:
                print(child.size)
            part1(child)


def part2(current_dir, space_required):
    for child in current_dir.children:
        if child.type == "Directory":
            if child.size >= space_required:
                print(child.size)
            part2(child, space_required)


class File:
    def __init__(self, name, size):
        self.type = "File"
        self.name = name
        self.size = size


class Directory:
    def __init__(self, name, files, parent, children, size):
        self.type = "Directory"
        self.name = name
        self.files = files
        self.parent = parent
        self.children = children
        self.size = size


def dir_exists(current_dir, name):
    if current_dir.children is None:
        return False, None
    for child in current_dir.children:
        if child.name == name:
            return True, child

    return False, None


def setup():
    computer = Directory("/", None, None, [], 0)
    current_dir = computer
    index = 0
    line = lines[index]
    while line != "Done":
        params = line.split(" ")
        if params[1] == "cd":
            if params[2] == "..":
                current_dir = current_dir.parent
            else:
                exists, new_current = dir_exists(current_dir, params[2])
                if exists:
                    current_dir = new_current
                else:
                    new_dir = Directory(params[2], None, current_dir, [], 0)
                    current_dir.children.append(new_dir)
                    current_dir = new_dir
            index += 1
            line = lines[index]
            continue

        if params[1] == "ls":
            index += 1
            ls = lines[index].split(" ")
            while ls[0] != "$" and ls[0] != "Done":
                if ls[0] == "dir":
                    if not dir_exists(current_dir, ls[1]):
                        current_dir.children.append(Directory(ls[1], None, current_dir, [], 0))
                else:  # type is file
                    new_file = File(ls[1], int(ls[0]))
                    current_dir.children.append(new_file)
                index += 1
                ls = lines[index].split(" ")

        line = lines[index]

    calculate_sizes(computer)
    # print_directory(computer, 0)
    print("Done.")
    print("Free space = ", 70000000 - computer.size)
    print("Space required = ", 30000000 - 70000000 + computer.size)
    # part1(computer)
    part2(computer, 30000000 - 70000000 + computer.size)


if __name__ == "__main__":
    setup()
