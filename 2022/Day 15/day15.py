import math
import re
from xml.sax.xmlreader import XMLReader

file = open('2022/Day 15/input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]


class Reading:
    def __init__(self, sensor, beacon):
        self.sensor = sensor
        self.beacon = beacon
        self.distance = manhattan(sensor, beacon)


def manhattan(point_a, point_b):
    return abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1])


def get_min(current_min, sensor, beacon):
    if sensor[0] - manhattan(sensor, beacon) < current_min:
        current_min = sensor[0] - manhattan(sensor, beacon)
    if beacon[0] < current_min:
        current_min = beacon[0]

    return current_min


def get_max(current_max, sensor, beacon):
    if sensor[0] + manhattan(sensor, beacon) > current_max:
        current_max = sensor[0] + manhattan(sensor, beacon)
    if beacon[0] > current_max:
        current_max = beacon[0]

    return current_max


def can_have_beacon(readings, test_point):
    for reading in readings:
        if reading.beacon[0] == test_point[0] and reading.beacon[1] == test_point[1]:
            return False
        if reading.sensor[0] == test_point[0] and reading.sensor[1] == test_point[1]:
            return False

        dist = reading.distance
        if manhattan(reading.sensor, test_point) <= dist:
            return False

    return True


def circle_x_range(reading, y):
    mid = reading.sensor
    x_min = mid[0] - (reading.distance - abs(mid[1] - y))
    x_max = mid[0] + (reading.distance - abs(mid[1] - y))
    return x_min, x_max  # min(x_min, x_max), max(x_min, x_max)


def puzzle(part2):
    sensors_beacons = {}
    x_range = [math.inf, -math.inf]
    readings = []
    for line in lines:
        numbers = [int(x) for x in re.findall('[-+]?\d+', line)]
        sensor = (numbers[0], numbers[1])
        beacon = (numbers[2], numbers[3])
        sensors_beacons[sensor] = beacon
        readings.append(Reading(sensor, beacon))
        x_range[0] = get_min(x_range[0], sensor, beacon)
        x_range[1] = get_max(x_range[1], sensor, beacon)+1

    if len(lines) > 18:
        y = 2000000
        MAX = 4000000
    else:
        y = 11
        MAX = 20
    x_offset = abs(x_range[0])
    found = False

    if part2:
        y0 = MAX
        y1 = 0
        y2 = -1
    else:
        y0 = y
        y1 = y+1
        y2 = 1

    for y in range(y0, y1, y2):
        if part2:
            if y % 1000 == 0:
                print(y)
        if not part2:
            row = ["." for _ in range(x_range[1]+x_offset+20)]
    
            for reading in readings:
                if reading.beacon[1] == y:
                    row[reading.beacon[0] + x_offset] = "B"
                elif reading.sensor[1] == y:
                    row[reading.sensor[0] + x_offset] = "S"

        ranges = []
        invalid = False
        for reading in readings:
            start_x, end_x = circle_x_range(reading, y)
            r = (min(start_x, end_x), max(start_x, end_x))
            r = (max(r[0], 0), min(r[1], MAX))
            if r == (0, MAX):
                invalid = True
                break
            if not ranges.__contains__(r) and start_x <= end_x:
                ranges.append(r)
            if not part2:
                for x in range(start_x, end_x+1):
                    if row[x + x_offset] == "B" or row[x + x_offset] == "S":
                        continue

                    row[x + x_offset] = "#"


        if part2:
            if invalid:
                continue
            if ranges.__contains__((0, MAX)):
                continue

            ranges.sort()
            left = ranges[0][0]
            right = ranges[0][1]
            for i in range(len(ranges)-1):
                if left <= ranges[i+1][0] <= right:
                    if ranges[i+1][1] > right:
                        right = ranges[i+1][1]
                if ranges[i+1][0] - right > 1:
                    print("Part 2:", (right+1)*4000000 + y)
                    found = True
                    break
            if found:
                break

    if not part2:
        print("Part 1:", row.count("#"))


if __name__ == "__main__":
    puzzle(False)
    puzzle(True)
