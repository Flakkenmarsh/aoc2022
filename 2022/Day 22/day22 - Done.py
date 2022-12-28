import re
# import numpy as np
import math
from copy import deepcopy
from pprint import pprint

file = open('2022/Day 22/input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]
board_map = []
board_tiles = []
instructions = ""
cube = {}
# example
#vertical_band = [1, 4, 5, 2]
#horizontal_band = [1, 6, 5, 3]
# actual
vertical_band = [1, 3, 5, 6]
horizontal_band = [1, 2, 5, 4]
cube_length = 50


# class Side
class Side:
    def __init__(self, side):
        self.side = side
        self.values = []
        self.matrix =  [[0 for _ in range(cube_length)] for _ in range(cube_length)] # np.empty([4, 4], dtype=str)
        self.rotations_performed = 0  # how many rot90s performed


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
            if pos[0] == i and pos[1] == j:
                if facing == "right":
                    result += " > "
                elif facing == "left":
                    result += " < "
                elif facing == "up":
                    result += " ^ "
                else:
                    result += " v "
                continue
            result += " " + board[i][j] + " "
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


def get_next_tile(tile, direction):
    if tile.neighbours[direction].value == "#":
        return tile  # don't move if it hits a wall
    
    return tile.neighbours[direction]


# part 1
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

    #for row in range(0, 4):
    #    cube[1].values.append(lines[row].strip())
    #for row in range(4, 8):
    #    for col in range(0, 3):
    #        cube[2+col].values.append(lines[row][col*4:col*4 + 4])
    #for row in range(8, 12):
    #    for col in range(0, 2):
    #        cube[5+col].values.append(lines[row].strip()[col*4:col*4+4])

    for row in range(0, 50):
        cube[1].values.append(lines[row].strip()[0:50])
        cube[2].values.append(lines[row].strip()[50:100])
    for row in range(50, 100):
        cube[3].values.append(lines[row].strip())
    for row in range(100, 150):
        for col in range(0, 2):
            cube[4+col].values.append(lines[row].strip()[col*50:col*50 + 50])
    for row in range(150, 200):
        cube[6].values.append(lines[row].strip())

    for c in range(1, 7):
        for row in range(len(cube[c].values)):
            for col in range(len(cube[c].values[row])):
                cube[c].matrix[row][col] = cube[c].values[row][col]

    print("Setup done.")


def get_new_face_layout(direction):
    global vertical_band
    global horizontal_band

    v_band = deepcopy(vertical_band)
    h_band = deepcopy(horizontal_band)

    if direction == "down":
        v_band.append(v_band.pop(0))
        h_band[0] = v_band[0]
        h_band[2] = v_band[2]
    elif direction == "up":
        v_band.insert(0, v_band.pop())
        h_band[0] = v_band[0]
        h_band[2] = v_band[2]
    elif direction == "right":
        h_band.append(h_band.pop(0))
        v_band[0] = h_band[0]
        v_band[2] = h_band[2]
    elif direction == "left":
        h_band.insert(0, h_band.pop())
        v_band[0] = h_band[0]
        v_band[2] = h_band[2]

    return v_band, h_band


# rotate matrix counter clockwise
def rotate_matrix_ccw(matrix, times):
    times %= 4
    m = deepcopy(matrix)
    for _ in range(times):
        m = [[m[j][i] for j in range(len(m))] for i in range(len(m[0])-1,-1,-1)]
    return m


def rotate_matrix_cw(matrix, times):
    times %= 4
    m = deepcopy(matrix)
    for _ in range(times):
        m = list(list(x)[::-1] for x in zip(*m))
    return m

        
def part2():
    global cube
    global instructions
    global vertical_band
    global horizontal_band
    global cube_length

    instructions += "D"  # for Done
    distances = [int(d) for d in re.findall(r'\d+', instructions)]
    turns = re.findall("[RLD]+", instructions)
    for c in cube:
        print("Side", c) 
        for row in cube[c].values:
            print("".join(row))

    movements = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    movement_directions = ["right", "down", "left", "up"]
    direction = 0  # start facing right
    face = 1
    pos = [0, 0]
    cube_length = len(cube[1].values)
    
    # how many cw rotations should be performed when switching sides
    # example
    #attached_sides = {"1->2": 2, "1->3": 1, "1->4": 0, "1->6": 2,
    #                  "2->1": 2, "2->3": 0, "2->5": 2, "2->6": 3,
    #                  "3->1": 3, "3->2": 0, "3->4": 0, "3->5": 1,
    #                  "4->1": 0, "4->3": 0, "4->5": 0, "4->6": 3,
    #                  "5->2": 2, "5->3": 3, "5->4": 0, "5->6": 0,
    #                  "6->1": 2, "6->2": 1, "6->4": 1, "6->5": 0} 
    # actual
    attached_sides = {"1->2": 0, "1->3": 0, "1->4": 2, "1->6": 3,
                      "2->1": 0, "2->3": 3, "2->5": 2, "2->6": 0,
                      "3->1": 0, "3->2": 1, "3->4": 1, "3->5": 0,
                      "4->1": 2, "4->3": 3, "4->5": 0, "4->6": 0,
                      "5->2": 2, "5->3": 0, "5->4": 0, "5->6": 3,
                      "6->1": 1, "6->2": 0, "6->4": 0, "6->5": 1} 

    # print_board_with_position(cube[1].matrix, (0, 0), "right")
    for i in range(len(turns)):
        print(i, "/", len(turns)-1)
        #print(distances[i])
        temp_pos = [0, 0]
        for j in range(distances[i]):
            temp_pos[0] = pos[0] + movements[direction][0]
            temp_pos[1] = pos[1] + movements[direction][1]
            
            rotation_required = False
            if temp_pos[0] < 0:  # go up a face
                #print("Go up")
                v_band, h_band = get_new_face_layout("up")
                rotation_required = True
                temp_pos[0] = cube_length - 1
            elif temp_pos[0] >= cube_length:  # go down a face
                #print("Go down")
                v_band, h_band = get_new_face_layout("down")
                rotation_required = True
                temp_pos[0] = 0
            elif temp_pos[1] < 0:  # go to the left face
                #print("Go left")
                v_band, h_band = get_new_face_layout("left")
                rotation_required = True
                temp_pos[1] = cube_length - 1
            elif temp_pos[1] >= cube_length:  # go to the right face
                #print("Go right")
                v_band, h_band = get_new_face_layout("right")
                rotation_required = True
                temp_pos[1] = 0
            old_face = face
            if rotation_required:
                new_face = v_band[0]
                num_rotations = cube[face].rotations_performed + attached_sides[str(old_face) + "->" + str(new_face)]
                face_matrix = rotate_matrix_cw(cube[new_face].matrix, num_rotations)
                if face_matrix[temp_pos[0]][temp_pos[1]] != "#":
                    pos = temp_pos
                    vertical_band = v_band
                    horizontal_band = h_band
                    face = new_face
                    cube[new_face].matrix = deepcopy(face_matrix)
                    cube[new_face].rotations_performed += num_rotations
            
            if not rotation_required and cube[face].matrix[temp_pos[0]][temp_pos[1]] != "#":
                pos = deepcopy(temp_pos)
            #print("Face", face)
            #print_board_with_position(cube[face].matrix, pos, movement_directions[direction])
        direction += 1 if turns[i] == "R" else -1
        if direction < 0 or direction >= 4:
            direction %= 4
        #print("turn", turns[i])
    direction += 1  # to correct for the D at the end
    temp_matrix = [[[j, i] for i in range(cube_length)] for j in range(cube_length)]
    temp_matrix = rotate_matrix_ccw(temp_matrix, cube[face].rotations_performed)
    print("Rotations performed on current face:", cube[face].rotations_performed%4)
    print("Face:", face)
    print("Coords:", [(index, row.index(pos)) for index, row in enumerate(temp_matrix) if pos in row])
    print("Facing:", direction)


if __name__ == "__main__":
    # setup_part1()
    # part1()
    setup_part2()
    part2()
