import copy
import math
import re
from copy import deepcopy
from operator import itemgetter
import time


file = open('2022/Day 16/input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]
valves = {}
max_pressure = 0


class Valve:
    def __init__(self, name, flow_rate, neighbour_names):
        self.name = name
        self.flow_rate = flow_rate
        self.neighbour_names = neighbour_names
        self.distance_to_others = {}
        self.is_open = False
        self.neighbours = []

    def dead_end(self):
        return len(self.neighbours) == 1


def print_state(minute, open_valves, pressure_release):
    print("== Minute", minute, "==")
    print("Open valves:", [o.name for o in open_valves], "releasing pressure =", pressure_release)


def get_sorted_neighbours(prev, current):
    neighbours = []
    for n in current.neighbours:
        if not n.is_open and n != prev:
            neighbours.append(n)
    neighbours.sort(key=lambda neighbour: neighbour.flow_rate, reverse=True)
    if prev is not None and not prev.is_open:
        neighbours.append(prev)
    for n in current.neighbours:
        if n.is_open and not neighbours.__contains__(n):
            neighbours.append(n)

    return neighbours


def all_are_open(open_valves):
    global valves

    openable_valves = [valves[v].flow_rate != 0 for v in valves].count(True)

    return openable_valves - len(open_valves) == 0


def calculate_pressure_release(open_valves):
    global valves

    release = 0
    for valve in open_valves:
        release += valves[valve].flow_rate

    return release


def BFS_SP(start, goal):
    global valves

    explored = []

    # Queue for traversing the graph in the BFS
    queue = [[valves[start]]]

    # If the desired node is reached
    if start == goal:
        return [start]

    # Loop to traverse the graph with the help of the queue
    while queue:
        path = queue.pop(0)
        node = path[-1]

        # Condition to check if the current node is not visited
        if node not in explored:
            neighbours = node.neighbours

            # Loop to iterate over the neighbours of the node
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)

                # Condition to check if the neighbour node is the goal
                if neighbour.name == goal:
                    return [v.name for v in new_path]

            explored.append(node)
    print("No way from", start, "to", goal)
    return None


def do_thing(part):
    global valves

    valves_to_open = []
    for v in valves:
        if valves[v].flow_rate != 0:
            valves_to_open.append(v)

    for v1 in valves:
        for v2 in valves:
            if v1 == v2:
                continue
            if valves[v2].flow_rate == 0:
                continue
            valves[v1].distance_to_others[v2] = len(BFS_SP(v1, v2)) - 1

    if part == 1:
        traverse(30, "AA", valves_to_open, 0)
        print("----------------------------")
    else:
        traverse_with_elephant(26, valves_to_open, [], 0, 1, 1, "AA", None, "AA", None)


def copy_valves(rem_valves):
    result = []
    for i in rem_valves:
        result.append(i)
    return result


def traverse(minutes_remaining, current, remaining_valves, total_pressure):
    global valves
    global max_pressure

    if total_pressure > max_pressure:
        max_pressure = total_pressure
        print(max_pressure)

    distances = []
    for valve in remaining_valves:
        pressure_released = (minutes_remaining - valves[current].distance_to_others[valve] - 1)*valves[valve].flow_rate
        if pressure_released > 0:
            distances.append((valve, pressure_released))

    distances = sorted(distances, key=itemgetter(1), reverse=True)

    for i in range(len(distances)):
        rem_valves = copy_valves(remaining_valves)
        rem_valves.remove(distances[i][0])
        traverse(minutes_remaining - valves[current].distance_to_others[distances[i][0]] - 1, distances[i][0],
                 rem_valves, total_pressure + distances[i][1])


def get_distances(remaining_valves, minutes_remaining, current):
    distances = []
    for valve in remaining_valves:
        pressure_releasable = (minutes_remaining - valves[current].distance_to_others[valve] - 1) * valves[
            valve].flow_rate
        if pressure_releasable > 0:
            distances.append((valve, pressure_releasable))

    return sorted(distances, key=itemgetter(1), reverse=True)


def traverse_with_elephant(minutes_remaining, remaining_valves, open_valves, total_pressure, my_time_left, ele_time_left,
                           my_origin, my_destination, ele_origin, ele_destination):
    global valves
    global max_pressure

    if minutes_remaining == 0:
        if total_pressure > max_pressure:
            max_pressure = total_pressure
            print("Time's up:", max_pressure)
        return

    if len(open_valves) == 15:
        total_pressure += calculate_pressure_release(open_valves)*(minutes_remaining)
        if total_pressure > max_pressure:
            max_pressure = total_pressure
            print("All are open:", max_pressure)
        return

    all_remaining = deepcopy(remaining_valves)
    if my_destination is not None and not all_remaining.__contains__(my_destination):
        all_remaining.append(my_destination)
    if ele_destination is not None and not all_remaining.__contains__(ele_destination):
        all_remaining.append(ele_destination)
    if total_pressure + calculate_pressure_release(all_remaining)*minutes_remaining < max_pressure:
        return

    if total_pressure > max_pressure:
        max_pressure = total_pressure
        print(max_pressure)

    # minutes_remaining -= 1
    my_time_left -= 1
    ele_time_left -= 1
    
    if ele_time_left == 0:
        if ele_destination is not None:
            if not open_valves.__contains__(ele_destination):
                open_valves.append(ele_destination)
            ele_origin = ele_destination
    if my_time_left == 0:
        if my_destination is not None:
            if not open_valves.__contains__(my_destination):
                open_valves.append(my_destination)
            my_origin = my_destination
    search_depth = 20
    pr = calculate_pressure_release(open_valves)
    #print("Open valves:", open_valves)
    #print("Minute:", 27-minutes_remaining, "Pressure released:", pr)
    total_pressure += pr

    if (ele_time_left == 0 and my_time_left == 0) and remaining_valves != []:  # choose new destination
        ele_distances = get_distances(remaining_valves, minutes_remaining, ele_origin)
        for i in range(min(search_depth, len(ele_distances))):
            ele_each = ele_distances[i]
            temp_remaining = deepcopy(remaining_valves)
            temp_remaining.remove(ele_each[0])
            my_distances = get_distances(temp_remaining, minutes_remaining, my_origin)
            for j in range(min(search_depth, len(my_distances))):
                my_each = my_distances[j]
                my_temp_remaining = deepcopy(temp_remaining)
                my_temp_remaining.remove(my_each[0])
                traverse_with_elephant(minutes_remaining - 1, my_temp_remaining, deepcopy(open_valves), total_pressure, 
                                       1 + valves[my_origin].distance_to_others[my_each[0]],
                                       1 + valves[ele_origin].distance_to_others[ele_each[0]],
                                       my_origin, my_each[0], ele_origin, ele_each[0])
            if my_distances == []:
                traverse_with_elephant(minutes_remaining - 1, [], deepcopy(open_valves), total_pressure, 
                                       0,
                                       1 + valves[ele_origin].distance_to_others[ele_each[0]],
                                       my_origin, None, ele_origin, ele_each[0])
    elif (ele_time_left == 0 or my_time_left == 0) and remaining_valves != []:
        if ele_time_left == 0:
            ele_distances = get_distances(remaining_valves, minutes_remaining, ele_origin)
            for i in range(min(search_depth, len(ele_distances))):
                each = ele_distances[i]
                ele_d = each[0]
                temp_remaining = deepcopy(remaining_valves)
                temp_remaining.remove(ele_d)
                traverse_with_elephant(minutes_remaining - 1, temp_remaining, deepcopy(open_valves), total_pressure, 
                                       my_time_left, 1 + valves[ele_origin].distance_to_others[ele_d],
                                       my_origin, my_destination, ele_origin, ele_d)
        elif my_time_left == 0:
            my_distances = get_distances(remaining_valves, minutes_remaining, my_origin)
            for i in range(min(search_depth, len(my_distances))):
                each = my_distances[i]
                my_d = each[0]
                temp_remaining = deepcopy(remaining_valves)
                temp_remaining.remove(my_d)
                traverse_with_elephant(minutes_remaining - 1, temp_remaining, deepcopy(open_valves), total_pressure, 
                                       1 + valves[my_origin].distance_to_others[my_d], ele_time_left,
                                       my_origin, my_d, ele_origin, ele_destination)
    else:
        traverse_with_elephant(minutes_remaining - 1, remaining_valves, deepcopy(open_valves), total_pressure, 
                                       my_time_left, ele_time_left,
                                       my_origin, my_destination, ele_origin, ele_destination)


def setup():
    global valves
    global max_pressure

    open_valves = []
    for line in lines:
        rate = [int(x.group()) for x in re.finditer(r'\d+', line)][0]
        params = line.split(" ")
        valve = params[1]
        neighbours = [p.replace(",", "") for p in params[9:]]
        valves[valve] = Valve(valve, rate, neighbours)
    for v in valves:
        for n in valves[v].neighbour_names:
            valves[v].neighbours.append(valves[n])

    do_thing(1)


def part1():
    do_thing(1)


def part2():
    do_thing(2)


if __name__ == "__main__":
    setup()
    max_pressure = 0
    part2()
