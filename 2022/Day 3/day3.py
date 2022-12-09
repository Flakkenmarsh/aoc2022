import copy

file = open('input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]


def setup():
    priority = 0
    for line in lines:
        mid = int(len(line)/2)
        first = line[0:mid]
        second = line[mid:]
        both = ""
        for c in first:
            if second.__contains__(c):
                both += c
        unique = list(dict.fromkeys(both))
        # priority = 0
        for u in unique:
            print(u)
            value = ord(u)
            if value > 97:
                value -= 96
            else:
                value -= 38
            print(value)
            priority += value
            print(priority)

    print(priority)


def part1():
    priority = 0
    for line in lines:
        mid = int(len(line) / 2)
        first = line[0:mid]
        second = line[mid:]
        both = ""
        for c in first:
            if second.__contains__(c):
                both += c
        unique = list(dict.fromkeys(both))
        for u in unique:
            print(u)
            value = ord(u)
            if value > 97:
                value -= 96
            else:
                value -= 38
            priority += value

    print(priority)


def part2():
    priority = 0
    count = 0
    three_lines = []
    for line in lines:
        if count < 3:
            three_lines.append(line)
            count += 1

        if count != 3:
            continue
        # print(three_lines)
        common = ""
        for c in three_lines[0]:
            if three_lines[1].__contains__(c):
                if three_lines[2].__contains__(c):
                    common = c
                    break

        value = ord(common)
        if value > 97:
            value -= 96
        else:
            value -= 38
        # print(value)
        priority += value
        # print(priority)
        count = 0
        three_lines = []
    print(priority)


if __name__ == "__main__":
    # setup()
    # part1()
    part2()
