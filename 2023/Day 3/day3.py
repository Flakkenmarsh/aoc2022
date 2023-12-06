import re

file = open('input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]


def adjacency_square(index, length, row):
    global lines

    left = 0
    right = len(lines[0])
    top = 0
    bottom = len(lines)

    if row - 1 > 0:
        top = row - 1
    if row + 1 < len(lines):
        bottom = row + 2
    if index - 1 > 0:
        left = index - 1
    if index + length + 1 < len(lines[0]):
        right = index + length + 1

    return [i[left:right] for i in lines[top:bottom]]


def small_adjacency_square(index, row, square):
    left = 0
    right = len(square[0])
    top = 0
    bottom = len(square)

    if row - 1 > 0:
        top = row - 1
    if row + 2 < len(lines):
        bottom = row + 2
    if index - 1 > 0:
        left = index - 1
    if index + 2 < len(lines[0]):
        right = index + 2

    return [i[left:right] for i in square[top:bottom]]


def gear_adjacency_square(index, row):
    global lines

    left = 0
    right = len(lines[0])
    top = 0
    bottom = len(lines)

    if row - 1 > 0:
        top = row - 1
    if row + 1 < len(lines):
        bottom = row + 2
    if index - 3 > 0:
        left = index - 3
    if index + 4 < len(lines[0]):
        right = index + 4

    return [i[left:right] for i in lines[top:bottom]], row-top, index-left


def has_adjacent_characters(sub_grid):
    for i in range(0, len(sub_grid)):
        for j in range(0, len(sub_grid[0])):
            if not sub_grid[i][j].isdigit() and not sub_grid[i][j] == ".":
                return True


def setup():
    global lines

    total = 0
    row = 0
    for line in lines:
        matches = re.finditer(r'\d+', line)
        for match in matches:
            s = int(match.group())
            index = match.start()
            length = match.end() - match.start()
            square = adjacency_square(index, length, row)
            if has_adjacent_characters(square):
                total += s

        row += 1

    print(total)


def part2():
    global lines

    total = 0
    row = 0
    for line in lines:
        gear_indexes = [i for i, ltr in enumerate(line) if ltr == "*"]
        for gear_index in gear_indexes:
            if gear_index is []:
                continue
            gear_square, gear_row, gear_left = gear_adjacency_square(gear_index, row)
            numbers = [re.findall(r'\d+', n) for n in small_adjacency_square(gear_left, gear_row, gear_square)]
            if len([el for sub in numbers for el in sub]) != 2:
                continue

            gear_square = ["......."] + gear_square + ["......."]
            gear_square = ["." + g + "." for g in gear_square]
            gear_row += 1
            gear_left += 1

            gear_ratio = 1
            matches = re.finditer(r'\d+', gear_square[gear_row-1])
            for match in matches:
                if match.start()-1 <= gear_left < match.end()+1:
                    gear_ratio *= int(match.group())
            matches = re.finditer(r'\d+', gear_square[gear_row])
            for match in matches:
                if match.start() - 1 <= gear_left < match.end() + 1:
                    gear_ratio *= int(match.group())
            matches = re.finditer(r'\d+', gear_square[gear_row + 1])
            for match in matches:
                if match.start() - 1 <= gear_left < match.end() + 1:
                    gear_ratio *= int(match.group())

            # print(gear_ratio)

            total += gear_ratio

        row += 1

    print(total)


if __name__ == "__main__":
    part2()
