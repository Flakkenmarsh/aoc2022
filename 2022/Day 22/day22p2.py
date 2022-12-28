import re
import numpy as np
import math as m

file = open('input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]
board_map = []
board_tiles = []
instructions = ""
cube = {}


# class Side
class Side:
    def __init__(self, side):
        self.side = side
        self.values = []
        self.matrix = np.empty([4, 4], dtype=str)
        self.neighbours = []
        self.rotation = 0  # how many rot90s performed


# class Tile
class Tile:
    def __init__(self, coords, value):
        self.coords = coords
        self.value = value
        self.side = 0
        self.neighbours = {}


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
    direction = 0  # start facing right

    row = 0
    col = board_map[0].index(".")
    distances = [int(d) for d in re.findall(r'\d+', instructions)]
    turns = re.findall("[RL]+", instructions)

    tile = board_tiles[row][col]
    for i in range(len(turns)):
        for j in range(distances[i]):
            tile = get_next_tile(tile, currently_facing)
        direction += 1 if turns[i] == "R" else -1
        if direction < 0 or direction >= 4:
            direction %= 4
        currently_facing = movement_directions[direction]
    for j in range(distances[-1]):
        tile = get_next_tile(tile, currently_facing)

    print(tile.value, tile.coords[0] + 1, tile.coords[1] + 1)
    password = 1000*(tile.coords[0]+1) + 4*(tile.coords[1]+1) + direction
    print(password)


def setup_part2():
    global cube
    global instructions

    line_lengths = [len(line) for line in lines]
    longest_line = max(line_lengths)
    for line in lines:
        if not line.__contains__("."):
            break
        line += " " * (longest_line - len(line))
        board_map.append([c for c in line])
        board_tiles.append([Tile((0, 0), c) for c in line])

    instructions = lines[-1]
    cube = {1: Side(1), 2: Side(2), 3: Side(3), 4: Side(4), 5: Side(5), 6: Side(6)}
    #        1111
    #        1111
    #        1111
    #        1111
    #222233334444
    #222233334444
    #222233334444
    #222233334444
    #        55556666
    #        55556666
    #        55556666
    #        55556666
    cube[1].neighbours = {cube[2], cube[3], cube[4], cube[6]}
    cube[2].neighbours = {cube[1], cube[3], cube[5], cube[6]}
    cube[3].neighbours = {cube[1], cube[2], cube[4], cube[5]}
    cube[4].neighbours = {cube[1], cube[3], cube[5], cube[6]}
    cube[5].neighbours = {cube[2], cube[3], cube[4], cube[6]}
    cube[6].neighbours = {cube[1], cube[2], cube[4], cube[5]}

    for row in range(0, 4):
        cube[1].values.append(lines[row].strip())
    for row in range(4, 8):
        for col in range(0, 3):
            cube[2+col].values.append(lines[row][col*4:col*4 + 4])
    for row in range(8, 12):
        for col in range(0, 2):
            cube[5+col].values.append(lines[row].strip()[col*4:col*4 + 4])

    for c in range(1, 7):
        for row in range(len(cube[c].values)):
            for col in range(len(cube[c].values[row])):
                cube[c].matrix[row, col] = cube[c].values[row][col]

    instructions = lines[-1]


def part2():
    global cube
    global instructions

    distances = [int(d) for d in re.findall(r'\d+', instructions)]
    turns = re.findall("[RL]+", instructions)

    for c in cube:
        print("Side", c)
        for row in cube[c].values:
            print("".join(row))

    movements = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up, right, down, left
    movement_directions = ["right", "down", "left", "up"]
    currently_facing = "right"
    direction = 0  # start facing right
    face = 1
    pos = (0, 0)
    cube_length = len(cube[1].values)
    print(cube_length)

    for i in range(len(turns)):
        for j in range(distances[i]):
            pos += movements[direction]
            # tile = get_next_tile(tile, currently_facing)
        direction += 1 if turns[i] == "R" else -1
        if direction < 0 or direction >= 4:
            direction %= 4
        currently_facing = movement_directions[direction]
    # for j in range(distances[-1]):
        # tile = get_next_tile(tile, currently_facing)


if __name__ == "__main__":
    # setup_part1()
    # part1()
    setup_part2()
    part2()
