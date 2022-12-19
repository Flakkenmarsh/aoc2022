import math
import re
from copy import deepcopy

file = open('2022/Day 19/input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]
types = ["ore", "clay", "obsidian", "geode"]


class Cost():
    def __init__(self, ore, clay, obsidian):
        self.ore_cost = ore
        self.clay_cost = clay
        self.obsidian_cost = obsidian
        self.as_dict = {}
        self.as_dict["ore"] = ore
        self.as_dict["clay"] = clay
        self.as_dict["obsidian"] = obsidian
        self.as_dict["geode"] = 0


    def __str__(self):
        result = "Cost: "
        result += str(self.ore_cost) + " ore "
        result += str(self.clay_cost) + " clay "
        result += str(self.obsidian_cost) + " obsidian"

        return result


class Blueprint():
    def __init__(self, number, ore, clay, obsidian, geode):
        self.number = number
        self.ore_cost = ore
        self.clay_cost = clay
        self.obsidian_cost = obsidian
        self.geode_cost = geode
        self.as_dict = {}
        self.as_dict["ore"] = ore
        self.as_dict["clay"] = clay
        self.as_dict["obsidian"] = obsidian
        self.as_dict["geode"] = geode


    def __str__(self):
        result = "Blueprint " + str(self.number) + ":\n"
        result += "\tOre robot: " + str(self.ore_cost) + "\n"
        result += "\tClay robot: " + str(self.clay_cost) + "\n"
        result += "\tObsidian robot: " + str(self.obsidian_cost) + "\n"
        result += "\tGeode robot: " + str(self.geode_cost) + "\n"

        return result


def collect_ore(bots, levels, minutes):
    global types

    for t in types:
        levels[t] += bots[t]*minutes

    return levels


def can_generate(bots):
    types = []
    if bots["ore"] > 0:
        types.append("ore")
        types.append("clay")
    if bots["clay"] > 0:
        types.append("obsidian")
    if bots["obsidian"] > 0:
        types.append("geode")

    return types


def ore_required(levels, cost):
    global types

    max_required = 0
    max_type = ""
    for t in types:
        required = cost.as_dict[t] - levels[t]
        if required > max_required:
            max_required = required
            max_type = t

    return max_required  # , max_type


def pay_for_bot(levels, cost):
    for t in levels:
        levels[t] -= cost.as_dict[t]

    return levels


def collect(minutes, bots, levels, bp):
    if minutes <= 0:
        print("Geodes: ", levels["geode"])
        return

    bot_types = can_generate(bots)  # the bot types that can be generated with the supply types currently being generated

    for t in bot_types:
        required = ore_required(levels, bp.as_dict[t])  # need to consider the amount of bots per type - this will decrease the required time
        if required <= 0:
            required = 1
        temp_bots = deepcopy(bots)
        temp_levels = collect_ore(temp_bots, levels, required)
        temp_levels = pay_for_bot(levels, bp.as_dict[t])
        temp_bots[t] += 1
        collect(minutes - required, temp_bots, temp_levels, bp)



def part1():
    blueprints = []

    for line in lines:
        # line = line.replace(":", "")
        # Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 2 ore and 11 clay. Each geode robot costs 2 ore and 7 obsidian.
        numbers = [int(x) for x in re.findall('[-+]?\d+', line)]
        orebot_cost = Cost(numbers[1], 0, 0)
        claybot_cost = Cost(numbers[2], 0, 0)
        obsidianbot_cost = Cost(numbers[3], numbers[4], 0)
        geodebot_cost = Cost(numbers[5], 0, numbers[6])
        bp = Blueprint(numbers[0], orebot_cost, claybot_cost, obsidianbot_cost, geodebot_cost)
        blueprints.append(bp)

    bots = {}
    bots["ore"] = 1
    bots["clay"] = 0
    bots["obsidian"] = 0
    bots["geode"] = 0
    levels = {}
    levels["ore"] = 1
    levels["clay"] = 0
    levels["obsidian"] = 0
    levels["geode"] = 0

    for bp in blueprints:
        print(str(bp))
        minutes = 23
        collect(minutes, bots, levels, bp)
        break


if __name__ == "__main__":
    part1()
