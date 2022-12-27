import copy
from copy import deepcopy
import numpy as np
from pprint import pprint

file = open('input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]


class Elf:
    def __init__(self, position):
        # self.position = position
        self.row = position[0]
        self.col = position[1]
        self.proposed = (0, 0)


def move_proposals(first, grove, elf):
    if first == 0:
        if sum(grove[elf.row - 1, elf.col - 1:elf.col + 2]) == 0:
            return elf.row - 1, elf.col
        if sum(grove[elf.row + 1, elf.col - 1:elf.col + 2]) == 0:
            return elf.row + 1, elf.col
        if sum(grove[elf.row - 1: elf.row + 2, elf.col - 1]) == 0:
            return elf.row, elf.col - 1
        if sum(grove[elf.row - 1: elf.row + 2, elf.col + 1]) == 0:
            return elf.row, elf.col + 1
    elif first == 1:
        if sum(grove[elf.row + 1, elf.col - 1:elf.col + 2]) == 0:
            return elf.row + 1, elf.col
        if sum(grove[elf.row - 1: elf.row + 2, elf.col - 1]) == 0:
            return elf.row, elf.col - 1
        if sum(grove[elf.row - 1: elf.row + 2, elf.col + 1]) == 0:
            return elf.row, elf.col + 1
        if sum(grove[elf.row - 1, elf.col - 1:elf.col + 2]) == 0:
            return elf.row - 1, elf.col
    elif first == 2:
        if sum(grove[elf.row - 1: elf.row + 2, elf.col - 1]) == 0:
            return elf.row, elf.col - 1
        if sum(grove[elf.row - 1: elf.row + 2, elf.col + 1]) == 0:
            return elf.row, elf.col + 1
        if sum(grove[elf.row - 1, elf.col - 1:elf.col + 2]) == 0:
            return elf.row - 1, elf.col
        if sum(grove[elf.row + 1, elf.col - 1:elf.col + 2]) == 0:
            return elf.row + 1, elf.col
    else:
        if sum(grove[elf.row - 1: elf.row + 2, elf.col + 1]) == 0:
            return elf.row, elf.col + 1
        if sum(grove[elf.row - 1, elf.col - 1:elf.col + 2]) == 0:
            return elf.row - 1, elf.col
        if sum(grove[elf.row + 1, elf.col - 1:elf.col + 2]) == 0:
            return elf.row + 1, elf.col
        if sum(grove[elf.row - 1: elf.row + 2, elf.col - 1]) == 0:
            return elf.row, elf.col - 1

    return -1, -1


def elves_interested(elf_map_slice, row, col):
    elves = []
    for i in range(len(elf_map_slice)):
        for j in range(len(elf_map_slice[0])):
            if i == row and j == col:
                continue
            if elf_map_slice[i][j] is not None:
                if elf_map_slice[i][j].proposed[0] == row and elf_map_slice[i][j].proposed[1] == col:
                    elves.append(elf_map_slice[i][j])
    return elves


def print_grove(grove):
    result = "Grove map:\n"
    for i in range(len(grove)):
        for j in range(len(grove[i, :])):
            result += "." if grove[i, j] == 0 else "#"
        result += "\n"
    print(result + "\n")


def print_elves(elves):
    result = "Elf map:\n"
    for i in range(len(elves)):
        for j in range(len(elves[i, :])):
            result += "." if elves[i, j] is None else "#"
        result += "\n"
    print(result + "\n")


def should_move(grove, elf):
    grove_slice = grove[elf.row-1:elf.row+2, elf.col-1:elf.col+2]
    total = sum(sum(grove_slice)) - 1
    return total != 0


def count_ground_tiles(grove):
    top = len(grove)
    bottom = 0
    left = len(grove[0])
    right = 0
    # print_grove(grove)
    for row in range(1, len(grove) - 1):
        elf_indices = np.where(grove[row, 0:len(grove[0])] == 1)
        if len(elf_indices[0]) >= 1:
            elf_indices = elf_indices[0]
            if elf_indices[0] < left:
                left = elf_indices[0]
            if len(elf_indices) == 1:
                if elf_indices[0] > right:
                    right = elf_indices[0]
            elif elf_indices[-1] > right:
                right = elf_indices[-1]
    for col in range(1, len(grove[0]) - 1):
        elf_indices = np.where(grove[0:len(grove), col] == 1)
        if len(elf_indices[0]) >= 1:
            elf_indices = elf_indices[0]
            if elf_indices[0] < top:
                top = elf_indices[0]
            if len(elf_indices) == 1:
                if elf_indices[0] > bottom:
                    bottom = elf_indices[0]
            elif elf_indices[-1] > bottom:
                bottom = elf_indices[-1]

    #print_grove(grove)
    ground_area = 0
    elves = 0
    result = ""
    for row in range(top, bottom + 1):
        for col in range(left, right + 1):
            if grove[row, col] == 0:
                ground_area += 1
                result += "."
            else:
                elves += 1
                result += "#"
        result += "\n"
    #print(result)
    print(ground_area)


def part1():
    grove = np.array(
        [[0] + [int(c) for c in line.replace(".", "0").replace("#", "1")] + [0] for line in lines])

    elf_count = 0
    elf_map = np.array([[None for _ in range(len(grove[0]))] for _ in range(len(grove))])

    for row in range(0, len(grove)):
        for col in range(0, len(grove[0])):
            if grove[row, col] == 1:
                elf_map[row, col] = Elf((row, col))
                elf_count += 1
    print(elf_count)
    round_no = 0
    # print_grove(grove)
    while True:
        print(round_no+1)
        if sum(sum(grove[0:2, :])) > 0:  # prepend row
            grove = np.append(np.array([[0] * (len(grove[0]))]), grove, axis=0)
            grove = np.append(np.array([[0] * (len(grove[0]))]), grove, axis=0)
            elf_map = np.append(np.array([[None] * (len(elf_map[0]))]), elf_map, axis=0)
            elf_map = np.append(np.array([[None] * (len(elf_map[0]))]), elf_map, axis=0)
        # pprint(grove[len(grove)-2:len(grove), :])
        if sum(sum(grove[len(grove)-2:len(grove), :])) > 0:  # append row
            grove = np.concatenate((grove, np.array([[0] * (len(grove[0]))])), axis=0)
            grove = np.concatenate((grove, np.array([[0] * (len(grove[0]))])), axis=0)
            elf_map = np.concatenate((elf_map, np.array([[None] * (len(elf_map[0]))])), axis=0)
            elf_map = np.concatenate((elf_map, np.array([[None] * (len(elf_map[0]))])), axis=0)
        if sum(sum(grove[:, 0:2])) > 0:  # prepend column
            grove = np.concatenate((np.array([[0]] * len(grove)), grove), axis=1)
            grove = np.concatenate((np.array([[0]] * len(grove)), grove), axis=1)
            elf_map = np.concatenate((np.array([[None]] * len(elf_map)), elf_map), axis=1)
            elf_map = np.concatenate((np.array([[None]] * len(elf_map)), elf_map), axis=1)
        if sum(sum(grove[:, len(grove[0])-2:len(grove[0])])) > 0:  # append column
            grove = np.concatenate((grove, np.array([[0]] * len(grove))), axis=1)
            grove = np.concatenate((grove, np.array([[0]] * len(grove))), axis=1)
            elf_map = np.concatenate((elf_map, np.array([[None]] * len(elf_map))), axis=1)
            elf_map = np.concatenate((elf_map, np.array([[None]] * len(elf_map))), axis=1)
        for row in range(0, len(grove)):
            for col in range(0, len(grove[row])):
                if grove[row, col] == 1:
                    elf_map[row, col].row = row
                    elf_map[row, col].col = col
        # print_grove(grove)
        # propose moves
        # print_elves(elf_map)
        if round_no + 1 == 881:
            print_grove(grove)
        should_not_move = 0
        for row in range(1, len(grove) - 1):
            for col in range(1, len(grove[row]) - 1):
                if grove[row, col] == 1:  # elf_map[row, col] is not None:
                    if not should_move(grove, elf_map[row, col]):
                        should_not_move += 1
                        continue
                    else:
                        grove_slice = grove[row - 1:row + 2, col - 1:col + 2]
                        print_grove(grove_slice)
                    p_row, p_col = move_proposals(round_no % 4, grove, elf_map[row, col])
                    elf_map[row, col].proposed = (p_row, p_col)
        if should_not_move >= elf_count:
            print(should_not_move, elf_count)
            print_grove(grove)
            print("No moves left")
            print(round_no+1)
            break
        # print_grove(grove)
        # move
        new_elf_map = copy.deepcopy(elf_map)
        for row in range(1, len(grove) - 1):
            for col in range(1, len(grove[row]) - 1):
                elves = elves_interested(elf_map[row - 1:row + 2, col - 1:col + 2], row, col)
                if len(elves) == 1:  # if only one elf wants to move to the new tile
                    moving_elf = elves[0]
                    grove[row, col] = 1
                    grove[moving_elf.row, moving_elf.col] = 0
                    new_elf_map[row, col] = Elf((row, col))
                    new_elf_map[moving_elf.row, moving_elf.col] = None
        elf_map = copy.deepcopy(new_elf_map)
        # print_grove(grove)
        round_no += 1
        # if round_no == 10:
        #    count_ground_tiles(grove)
        #    break
        #print_grove(grove)


if __name__ == "__main__":
    part1()
