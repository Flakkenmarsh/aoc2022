import copy
from copy import deepcopy
import numpy as np
from pprint import pprint
import math
import sys

file = open('input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]
width = len(lines[0])
height = len(lines)
min_minutes = math.inf


class Blizzard:
    def __init__(self, row, col, movement, direction):
        self.row = row
        self.col = col
        self.movement = movement
        self.direction = direction

    def move(self):
        global width
        global height

        self.row += self.movement[0]
        if self.row == 0:
            self.row = height - 2
        elif self.row == height - 1:
            self.row = 1

        self.col += self.movement[1]
        if self.col == 0:
            self.col = width - 2
        elif self.col == width - 1:
            self.col = 1


def print_map(map0, row, col):
    global height
    global width

    result = ""
    for r in range(height):
        for c in range(width):
            if r == row and c == col:
                result += "E"
                continue
            if map0[r][c] == math.inf:
                result += "#"
            elif map0[r][c] == 0:
                result += "."
            else:
                result += str(map0[r][c])
        result += "\n"
    print(result)
    print("----------")


def print_map_plain(map0):
    for row in map0:
        print("".join(row))
    print("===================")


# Place the winds onto a blank map
def place_blizzard(winds):
    global height
    global width

    result = [["." for _ in range(width)] for _ in range(height)]
    for w in winds:
        if result[w.row][w.col] != ".":
            result[w.row][w.col] = "2"  # or more
        else:
            result[w.row][w.col] = w.direction
    for row in range(height):
        result[row][0] = "#"
        result[row][-1] = "#"
    for col in range(width):
        result[0][col] = "#"
        result[-1][col] = "#"
    result[-1][-2] = "."
    result[0][1] = "."

    return result


def get_neighbours(blizzard_map, row, col):
    result = []
    if row+1 < len(blizzard_map):
        if blizzard_map[row+1][col] == ".":
            result.append((row+1, col))
    if blizzard_map[row][col + 1] == ".":
        result.append((row, col + 1))
    if blizzard_map[row][col] == ".":  # if it's possible to wait
        result.append((row, col))
    if blizzard_map[row-1][col] == ".":
        result.append((row-1, col))
    if blizzard_map[row][col-1] == ".":
        result.append((row, col-1))

    return result


def move(winds, minutes, positions):
    global height
    global width
    global min_minutes

    if minutes > min_minutes:
        # print("Taking too long")
        return None

    # create a map of the current wind conditions
    new_map = place_blizzard(winds)
    new_positions = []

    # for every "E" on the map (stored in positions),
    # check where it can go and store that position in new_positions
    for p in positions:
        n = get_neighbours(new_map, p[0], p[1])
        if len(n) > 0:
            new_positions += n

    # for every new position, check whether it's the target.
    # If not, place an "E" on the new map
    for new_pos in new_positions:
        if new_pos[0] == height - 1 and new_pos[1] == width - 2:
            print("SUCCESS in", minutes)
            return winds, minutes
        new_map[new_pos[0]][new_pos[1]] = "E"

    # keep only the last 3 "Es" in every row (furthest 3 to the right).
    # Can adjust this number if necessary.
    keep_positions = []
    for row in range(len(new_map)):
        e_positions = [i for i, x in enumerate(new_map[row]) if x == "E"]
        for i in range(min(len(e_positions), 3)):
            keep_positions.append((row, e_positions[-i]))

    # print_map_plain(new_map)
    # all wind must advance by one positions
    for w in winds:
        w.move()
    return move(winds, minutes + 1, keep_positions)


# this is just a reverse of the "move" function. Didn't feel like adding a condition.
def move_back(winds, minutes, positions):
    global height
    global width
    global min_minutes

    if minutes > min_minutes:
        # print("Taking too long")
        return None

    new_map = place_blizzard(winds)
    new_positions = []

    for p in positions:
        n = get_neighbours(new_map, p[0], p[1])
        if len(n) > 0:
            new_positions += n

    for new_pos in new_positions:
        if new_pos[0] == 0 and new_pos[1] == 1:
            print("SUCCESS in", minutes)
            return winds, minutes
        new_map[new_pos[0]][new_pos[1]] = "E"

    keep_positions = []
    for row in range(len(new_map)):
        e_positions = [i for i, x in enumerate(new_map[row]) if x == "E"]
        for i in range(min(len(e_positions), 3)):
            keep_positions.append((row, e_positions[i]))

    for w in winds:
        w.move()
    return move_back(winds, minutes + 1, keep_positions)


def part1():
    global height
    global width

    valley_map = [[c for c in line] for line in lines]
    winds = []
    for row in range(height):
        for col in range(width):
            c = valley_map[row][col]
            if c == ">":
                winds.append(Blizzard(row, col, (0, 1), c))
            elif c == "<":
                winds.append(Blizzard(row, col, (0, -1), c))
            elif c == "v":
                winds.append(Blizzard(row, col, (1, 0), c))
            elif c == "^":
                winds.append(Blizzard(row, col, (-1, 0), c))

    times = []
    new_winds, minutes = move(winds, 0, [(0, 1)])
    times.append(minutes)
    new_winds, minutes = move_back(new_winds, 0, [(height-1, width-2)])
    times.append(minutes)
    _, minutes = move(new_winds, 0, [(0, 1)])
    times.append(minutes)
    print("Part 2:", sum(times))


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    part1()
