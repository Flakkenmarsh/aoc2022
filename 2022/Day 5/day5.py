import re

file = open('input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]

# For this to work, the crate layout in the input needs to be
# transposed to rows in excel, then all the extra characters need
# to be removed before pasting it back into the input file.


def print_crates(crates):
    for stack in crates:
        print(stack)
    print("")


def part1(moved_crates, crates, numbers):
    moved_crates.append(crates[numbers[1] - 1].pop())


def part2(moved_crates, crates, numbers):
    moved_crates.insert(0, crates[numbers[1] - 1].pop())


def puzzle(part_logic):
    crates = []
    for i in range(0, 9):
        crates.append([])
    crate_index = 0
    for line in lines:
        if line == "":
            break
        for c in line:
            crates[crate_index].insert(0, c)
        crate_index += 1

    for line in lines:
        if not line.startswith("move"):
            continue

        numbers = [int(s) for s in re.findall(r'\b\d+\b', line)]
        moved_crates = []
        for i in range(0, numbers[0]):
            part_logic(moved_crates, crates, numbers)

        crates[numbers[2] - 1] += moved_crates

    message = ""
    for crate in crates:
        message += crate[-1]

    print(message)


if __name__ == "__main__":
    puzzle(part1)
    puzzle(part2)
