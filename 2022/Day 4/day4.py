import copy

file = open('input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]


def contains(a, b):
    a_items = a.split("-")
    b_items = b.split("-")
    if int(a_items[0]) <= int(b_items[0]) and int(a_items[1]) >= int(b_items[1]):
        return True

    return False


def contains_part2(a, b):
    a_items = a.split("-")
    b_items = b.split("-")
    if int(b_items[0]) <= int(a_items[0]) <= int(b_items[1]):
        return True
    if int(b_items[0]) <= int(a_items[1]) <= int(b_items[1]):
        return True

    return False


def setup():
    count = 0
    for line in lines:
        pairs = line.split(",")
        if contains_part2(pairs[0], pairs[1]):
            print(line)
            count += 1
            print(count)
        elif contains_part2(pairs[1], pairs[0]):
            print(line)
            count += 1
            print(count)

    print(count)


def part1():
    pass


def part2():
    pass


if __name__ == "__main__":
    setup()
    part1()
    part2()
