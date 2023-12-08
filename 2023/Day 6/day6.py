import math
import re

file = open('input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]


def part1():
    times = [int(d) for d in re.findall(r'\d+', lines[0])]
    distances = [int(d) for d in re.findall(r'\d+', lines[1])]
    ways_to_win = [0 for _ in range(len(times))]

    for i in range(len(times)):
        for holding_time in range(times[i]):
            distance = (times[i] - holding_time) * holding_time
            if distance > distances[i]:
                ways_to_win[i] += 1

    print("Part 1: ", end="")
    print(math.prod(ways_to_win))


def part2():
    time = int("".join(re.findall(r'\d+', lines[0])))
    distance = int("".join(re.findall(r'\d+', lines[1])))
    ways_to_win = 0

    for holding_time in range(time):
        calculated_distance = (time - holding_time) * holding_time
        if calculated_distance > distance:
            ways_to_win += 1

    print("Part 2: ", end="")
    print(ways_to_win)


if __name__ == "__main__":
    part1()
    part2()
