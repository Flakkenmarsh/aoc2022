import copy
import re

file = open('input.csv', 'r')
# file = open('example.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]


class ConversionMap:
    def __init__(self, title, conversion_range, change):
        self.title = title
        self.conversion_range = conversion_range  # [from; to]
        self.change = change


def translate(index, source):
    global lines

    while lines[index] != ".":
        map_line = [int(d) for d in re.findall(r'\d+', lines[index])]
        if map_line[1] <= source < map_line[1] + map_line[2]:
            return source - map_line[1] + map_line[0], index, True
        index += 1

    return source, index, False


def part1():
    line_index = 0
    line = lines[line_index]
    line_values = [int(d) for d in re.findall(r'\d+', line)]

    locations = []

    for seed in line_values:
        line_index += 3
        source = seed
        for i in range(0, 7):
            source, line_index, found = translate(line_index, source)
            if found:
                while not lines[line_index] == ".":
                    line_index += 1
            line_index += 2

        line_index = 0
        locations.append(source)

    print(min(locations))


def split(range_to_split, range2):
    if range_to_split == range2:
        return [range_to_split], False

    if range_to_split[1] < range2[0]:
        return [range_to_split], False

    if range_to_split[0] > range2[1]:
        return [range_to_split], False

    if range_to_split[0] >= range2[0] and range_to_split[1] <= range2[1]:
        return [range_to_split], False

    # if range_to_split is on the left
    if range_to_split[0] < range2[0] and range_to_split[1] < range2[1]:
        return [[range_to_split[0], range2[0] - 1], [range2[0], range_to_split[1]]], True

    if range_to_split[0] < range2[0] and range_to_split[1] > range2[1]:
        return [[range_to_split[0], range2[0] - 1], [range2[0], range2[1]], [range2[1] + 1, range_to_split[1]]], True

    if range_to_split[0] == range2[0] and range_to_split[1] < range2[1]:
        return [[range_to_split[0], range2[0]], [range2[0] + 1, range_to_split[1]]], True

    if range_to_split[0] == range2[0] and range_to_split[1] > range2[1]:
        return [[range_to_split[0], range2[0]], [range2[0] + 1, range2[1]], [range2[1] + 1, range_to_split[1]]], True

    # if range_to_split is on the right
    if range_to_split[0] < range2[1] and range_to_split[1] > range2[1]:
        return [[range_to_split[0], range2[1]], [range2[1] + 1, range_to_split[1]]], True

    return [range_to_split], False


def is_in_range(range_to_test, range2):
    if range_to_test == range2:
        return True

    if range2[0] <= range_to_test[0] and range_to_test[1] <= range2[1]:
        return True

    return False


def part2():
    line_index = 0
    line = lines[line_index]
    line_values = [int(d) for d in re.findall(r'\d+', line)]

    seed_ranges = []
    for i in range(0, int(len(line_values)/2)):
        seed_ranges.append([line_values[2*i], line_values[2*i] + line_values[2*i + 1] - 1])

    map_list = [[] for _ in range(0, 7)]
    line_index = 2
    map_type_index = 0
    while line_index < len(lines):
        map_type = lines[line_index]

        line_index += 1
        while lines[line_index] != ".":
            line = lines[line_index]
            line_values = [int(d) for d in re.findall(r'\d+', line)]

            cm = ConversionMap(map_type, [], 0)
            cm.conversion_range = [line_values[1], line_values[1] + line_values[2] - 1]
            cm.change = line_values[0] - line_values[1]

            map_list[map_type_index].append(cm)
            line_index += 1

        line_index += 1
        map_type_index += 1

    # setup complete

    output = copy.deepcopy(seed_ranges)
    for map_type in map_list:
        input_range = copy.deepcopy(output)
        output = []
        while input_range:
            range_to_split = input_range.pop()
            split_applied = False
            for test_range in map_type:
                result, split_applied = split(range_to_split, test_range.conversion_range)
                if split_applied:
                    input_range.extend(result)
                    break
            if not split_applied:
                output.extend(result)

        for item in output:
            for test_range in map_type:
                if is_in_range(item, test_range.conversion_range):
                    item[0] += test_range.change
                    item[1] += test_range.change
                    break

    output.sort()
    print(output[0][0])


if __name__ == "__main__":
    # part1()
    part2()
