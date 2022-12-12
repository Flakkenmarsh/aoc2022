import copy
from copy import deepcopy
import math

file = open('input.csv', 'r')
lines = file.readlines()
lines = ["~" + line.strip('\n' ',') + "~" for line in lines]
min_distance = math.inf

min_distances = [min_distance]


def print_map(map0):
    for row in map0:
        print("".join(row))
    print("")


def search(map0, x, y, distance):
    global min_distances

    if map0[x][y] == "E":
        print("Found: ", distance)
        min_distances.append(distance)
        return True
    if map0[x][y] == "~":
        return False
    if distance >= min(min_distances):
        return False

    found = False
    current = map0[x][y]
    map0[x][y] = "~"
    distance += 1

    # up
    if ord(map0[x-1][y]) - ord(current) <= 1:
        found = search(copy.deepcopy(map0), x-1, y, distance)

    # down
    if ord(map0[x+1][y]) - ord(current) <= 1:
        found = search(copy.deepcopy(map0), x+1, y, distance)

    # left
    if ord(map0[x][y-1]) - ord(current) <= 1:
        found = search(copy.deepcopy(map0), x, y-1, distance)

    # right
    if ord(map0[x][y+1]) - ord(current) <= 1:
        found = search(copy.deepcopy(map0), x, y+1, distance)

    return found


def part1():
    global min_distance
    global min_distances

    height_map = [[c for c in line] for line in lines]
    height_map.insert(0, "~"*(len(height_map[0])))
    height_map.append('~'*(len(height_map[0])))

    print_map(height_map)
    start = (0, 0)
    end = (0, 0)
    for i in range(len(height_map)):
        for j in range(len(height_map[0])):
            if height_map[i][j] == "S":
                start = (i, j)
            elif height_map[i][j] == "E":
                end = (i, j)
    height_map[start[0]][start[1]] = "a"
    search(copy.deepcopy(height_map), start[0], start[1], 0)
    print(min_distances)


if __name__ == "__main__":
    part1()
