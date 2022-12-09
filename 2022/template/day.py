file = open('input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]


def part1():
    for line in lines:
        pass


if __name__ == "__main__":
    part1()
