import re

file = open('input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]


def part1():
    total = 0
    for line in lines:
        numbers = [int(d) for d in re.findall(r'\d+', line)]
        print(numbers)

    print(total)


def part2():
    total = 0
    print(total)


if __name__ == "__main__":
    part1()
    # part2()
