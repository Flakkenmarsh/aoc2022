import math
import re

file = open('input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]


def manhattan(sensor, beacon):
    return abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])


def get_min(current_min, sensor, beacon):
    if sensor[0] - manhattan(sensor, beacon) < current_min:
        current_min = sensor[0] - manhattan(sensor, beacon)
    if beacon[0] < current_min:
        current_min = beacon[0]

    return current_min


def get_max(current_max, sensor, beacon):
    if sensor[0] - manhattan(sensor, beacon) > current_max:
        current_max = sensor[0] - manhattan(sensor, beacon)
    if beacon[0] > current_max:
        current_max = beacon[0]

    return current_max


def part1():
    sensors_beacons = {}
    x_range = [math.inf, -math.inf]
    y_range = [math.inf, -math.inf]

    for line in lines:
        numbers = [int(x.group()) for x in re.finditer(r'\d+', line)]
        sensor = (numbers[0], numbers[1])
        beacon = (numbers[2], numbers[3])
        sensors_beacons[sensor] = beacon
        x_range[0] = get_min(x_range[0], sensor, beacon)
        x_range[1] = get_max(x_range[1], sensor, beacon)
        y_range[0] = get_min(y_range[0], sensor, beacon)
        y_range[1] = get_max(y_range[1], sensor, beacon)

    y = 10  # 2000000
    print(x_range)
    row = ["." for _ in range(y_range[1]-y_range[0])]
    beaconless = []
    beaconless_count = 0
    for x in range(y_range[0], y_range[1]):
        possible = True
        for sensor in sensors_beacons:
            beacon = sensors_beacons[sensor]
            if beacon[1] == y:
                row[beacon[0] + x_range[0]] = "B"
            dist = manhattan(sensor, beacon)
            if manhattan(sensor, (y, x)) < dist:
                possible = False
                break
        if possible:
            beaconless.append((y, x))
            beaconless_count += 1
            row[x + x_range[0]] = "."
        else:
            row[x + x_range[0]] = "#"
    print(beaconless_count)
    print(beaconless)
    print(row)




if __name__ == "__main__":
    part1()
