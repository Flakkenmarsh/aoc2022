import re
from enum import Enum
import numpy as np
import math as m

file = open('2022/Day 22/input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]
board_map = []
board_tiles = []
instructions = ""


# class Side
class Side:
    def __init__(self, side):
        self.side = side
        self.values = []
        self.neighbours = []
        self.rotation = 0  # how many rot90s performed


# class Tile
class Tile:
    def __init__(self, coords, value):
        self.coords = coords
        self.value = value
        self.side = 0
        self.neighbours = {"up": None, "down": None, "left": None, "right": None}


# print board
def print_board(board):
    for line in board:
        print("".join(line))


# print board with position
def print_board_with_position(board, pos, facing):
    result = ""
    for i in range(len(board)):
        for j in range(len(board[i])):
            if pos == (i, j):
                if facing == "right":
                    result += " > "
                elif facing == "left":
                    result += " < "
                elif facing == "up":
                    result += " ^ "
                else:
                    result += " v "
                continue
            result += " " + board[i][j].value + " "
        result += "\n"

    print(result)
    print("------------------------------")


# setup_part1
def setup_part1():
    global board_map
    global board_tiles
    global instructions

    line_lengths = [len(line) for line in lines]
    longest_line = max(line_lengths)
    for line in lines:
        if not line.__contains__("."):
            break
        line += (" ")*(longest_line-len(line))
        board_map.append([c for c in line])
        board_tiles.append([Tile((0,0), c) for c in line])

    instructions = lines[-1]

    # set values
    for i in range(len(board_tiles)):
        for j in range(len(board_tiles[i])):
            board_tiles[i][j].value = board_map[i][j]
            board_tiles[i][j].coords = (i, j)

    # inner tiles
    for i in range(0, len(board_tiles)):
        for j in range(1, len(board_tiles[i]) - 1):
            board_tiles[i][j].neighbours["left"] = board_tiles[i][j-1]
            board_tiles[i][j].neighbours["right"] = board_tiles[i][j+1]
    
    for i in range(1, len(board_tiles) - 1):
        for j in range(0, len(board_tiles[i])):
            board_tiles[i][j].neighbours["up"] = board_tiles[i-1][j]
            board_tiles[i][j].neighbours["down"] = board_tiles[i+1][j]

    # left and right borders
    for i in range(len(board_tiles)):
        board_tiles[i][0].neighbours["left"] = board_tiles[i][-1]
        board_tiles[i][0].neighbours["right"] = board_tiles[i][1]
        board_tiles[i][-1].neighbours["left"] = board_tiles[i][-2]
        board_tiles[i][-1].neighbours["right"] = board_tiles[i][0]
    # top and bottom borders
    for i in range(len(board_tiles[0])):
        board_tiles[0][i].neighbours["up"] = board_tiles[-1][i]
        board_tiles[0][i].neighbours["down"] = board_tiles[1][i]
        board_tiles[-1][i].neighbours["up"] = board_tiles[-2][i]
        board_tiles[-1][i].neighbours["down"] = board_tiles[0][i]

    for i in range(len(board_tiles)):
        for j in range(len(board_tiles[0])):
            if board_tiles[i][j].value == " ":
                continue
            tile = board_tiles[i][j].neighbours["up"]
            while tile.value == " ":
                tile = tile.neighbours["up"]
            board_tiles[i][j].neighbours["up"] = tile
            tile = board_tiles[i][j].neighbours["down"]
            while tile.value == " ":
                tile = tile.neighbours["down"]
            board_tiles[i][j].neighbours["down"] = tile
            tile = board_tiles[i][j].neighbours["left"]
            while tile.value == " ":
                tile = tile.neighbours["left"]
            board_tiles[i][j].neighbours["left"] = tile
            tile = board_tiles[i][j].neighbours["right"]
            while tile.value == " ":
                tile = tile.neighbours["right"]
            board_tiles[i][j].neighbours["right"] = tile

    return
    for i in range(0, len(board_tiles)):
        for j in range(0, len(board_tiles[i])):
            if board_tiles[i][j].value != " ":
                tile = board_tiles[i][j]
                a = not all(tile.neighbours.values())
                if a:
                    print(tile.value)


def get_next_tile(tile, direction):
    if tile.neighbours[direction].value == "#":
        return tile  # don't move if it hits a wall
    
    return tile.neighbours[direction]


def part1():
    global board_map
    global board_tiles
    global instructions

    movements = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up, right, down, left
    movement_directions = ["right", "down", "left", "up"]
    currently_facing = "right"
    direction = 0 # start facing right

    row = 0
    col = board_map[0].index(".")
    distances = [int(d) for d in re.findall(r'\d+', instructions)]
    #print(distances)
    turns = re.findall("[RL]+", instructions)

    tile = board_tiles[row][col]
    for i in range(len(turns)):
        #print(distances[i])
        for j in range(distances[i]):
            #print(j, "/", distances[i])
            #print_board_with_position(board_tiles, (tile.coords[0], tile.coords[1]), currently_facing)
            tile = get_next_tile(tile, currently_facing)
        direction += 1 if turns[i] == "R" else -1
        if direction < 0 or direction >= 4:
            direction %= 4
        currently_facing = movement_directions[direction]
    for j in range(distances[-1]):
        tile = get_next_tile(tile, currently_facing)
        #print_board_with_position(board_tiles, (tile.coords[0], tile.coords[1]), currently_facing)
    print(tile.value, tile.coords[0] + 1, tile.coords[1] + 1)
    password = 1000*(tile.coords[0]+1) + 4*(tile.coords[1]+1) + direction
    print(password)


class Colours(enum):
    UNKNOWN = 0
    WHITE = 1
    GREEN = 2
    RED = 3
    BLUE = 4
    YELLOW = 5
    ORANGE = 6


def setup_part2():
    global board_map
    global board_tiles
    global instructions

    line_lengths = [len(line) for line in lines]
    longest_line = max(line_lengths)
    for line in lines:
        if not line.__contains__("."):
            break
        line += (" ")*(longest_line-len(line))
        board_map.append([c for c in line])
        board_tiles.append([Tile((0,0), c) for c in line])

    instructions = lines[-1]
    mini_cube = [Tile(0, i) for i in range(7)]  # side 0 is ignored
#        1111 white
#        1111
#        1111
#        1111
#222233334444 green, 
#222233334444
#222233334444
#222233334444
#        55556666
#        55556666
#        55556666
#        55556666
    cube_arr[1].neighbours = [cube_arr[2], cube_arr[3], cube_arr[4], cube_arr[6]]
    cube_arr[2].neighbours = [cube_arr[1], cube_arr[3], cube_arr[5], cube_arr[6]]
    cube_arr[3].neighbours = [cube_arr[1], cube_arr[2], cube_arr[4], cube_arr[5]]
    cube_arr[4].neighbours = [cube_arr[1], cube_arr[3], cube_arr[5], cube_arr[6]]
    cube_arr[5].neighbours = [cube_arr[2], cube_arr[3], cube_arr[4], cube_arr[6]]
    cube_arr[6].neighbours = [cube_arr[1], cube_arr[2], cube_arr[4], cube_arr[5]]

    big_cube = [Side(i) for i in range(7)]  # side 0 is ignored




if __name__ == "__main__":
    setup_part1()
    # part1()
    setup_part2()
    part1()
    # part2()
