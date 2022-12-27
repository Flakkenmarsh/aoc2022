import copy
from copy import deepcopy
import numpy as np
from pprint import pprint
import math

file = open('input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]
lines = [[c for c in line] for line in lines]


def snafu_to_dec(number):
    total = 0
    power = 0
    for i in range(len(number) - 1, -1, -1):
        if number[i] == "-":
            total += -1 * math.pow(5, power)
        elif number[i] == "=":
            total += -2 * math.pow(5, power)
        else:
            total += int(number[i]) * math.pow(5, power)
        power += 1

    return int(total)


def dec_to_snafu(number):
    if number == 0:
        return "0"

    basics = ["0", "1", "2", "=", "-"]
    string = ""

    while number > 0:
        res = number % 5
        string = basics[res] + string
        number //= 5
        if res == 3 or res == 4:
            number += 1
    print(string)

    return string


def part1():
    total = 0
    for line in lines:
        dec = snafu_to_dec(line)
        total += dec
    dec_to_snafu(total)


if __name__ == "__main__":
    part1()
