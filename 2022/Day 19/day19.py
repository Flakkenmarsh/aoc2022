import math
import re
from copy import deepcopy, copy

file = open('input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]
types = ["ore", "clay", "obsidian", "geode"]
max_geodes = 0


class Cost():
    def __init__(self, ore, clay, obsidian):
        self.ore_cost = ore
        self.clay_cost = clay
        self.obsidian_cost = obsidian
        self.as_dict = {"ore": ore, "clay": clay, "obsidian": obsidian, "geode": 0}

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
        self.as_dict = {"ore": ore, "clay": clay, "obsidian": obsidian, "geode": geode}

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


def ore_required(levels, bots, cost):
    global types

    max_required = 0
    max_type = ""

    for c in cost.as_dict:
        if bots[c] == 0:
            continue
        required = cost.as_dict[c] - levels[c]
        required = int(math.ceil(required/bots[c]))
        if required > max_required:
            max_required = required
            max_type = c

    return max_required  # , max_type


def pay_for_bot(levels, cost):
    for t in levels:
        levels[t] -= cost.as_dict[t]

    return levels


def collect(minutes, bots, levels, bp):
    global max_geodes

    if minutes == 24:
        if levels["geode"] > max_geodes:
            max_geodes = levels["geode"]
            print("Geodes:", max_geodes)
        # print(bots)
        # print(levels)
        return
    elif minutes > 24:
        return

    bot_types = can_generate(bots)  # the bot types that can be generated with the supply types currently being generated

    for t in bot_types:
        if minutes == 1 and t == "clay":
            print("Stop here")
        time_required = ore_required(levels, bots, bp.as_dict[t])
        if time_required > 24-minutes:  # not enough time left
            temp_bots = copy(bots)
            temp_levels = collect_ore(temp_bots, copy(levels), 24-minutes)  # generate everything until the end
            if temp_levels["geode"] > max_geodes:
                max_geodes = temp_levels["geode"]
                print("Geodes:", max_geodes)
            continue
        if time_required < 0:  # if time is negative, bot is ready to be built
            time_required = 0  # won't require extra time
        temp_bots = copy(bots)
        temp_levels = collect_ore(temp_bots, copy(levels), time_required)  # time elapses
        temp_levels = pay_for_bot(temp_levels, bp.as_dict[t])
        temp_levels = collect_ore(temp_bots, temp_levels, 1)
        temp_bots[t] += 1
        collect(minutes + time_required + 1, temp_bots, temp_levels, bp)


def part1():
    blueprints = []

    for line in lines:
        numbers = [int(x) for x in re.findall('[-+]?\d+', line)]
        orebot_cost = Cost(numbers[1], 0, 0)
        claybot_cost = Cost(numbers[2], 0, 0)
        obsidianbot_cost = Cost(numbers[3], numbers[4], 0)
        geodebot_cost = Cost(numbers[5], 0, numbers[6])
        bp = Blueprint(numbers[0], orebot_cost, claybot_cost, obsidianbot_cost, geodebot_cost)
        blueprints.append(bp)

    bots = {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0}
    levels = {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0}

    for bp in blueprints:
        print(str(bp))
        if str(bp).__contains__("Blueprint 1"):
            continue
        collect(1, deepcopy(bots), deepcopy(levels), bp)


if __name__ == "__main__":
    part1()
