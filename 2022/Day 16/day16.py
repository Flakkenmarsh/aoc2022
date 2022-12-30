import copy
import math
import re
from copy import deepcopy
from operator import itemgetter
import time


file = open('input.csv', 'r')
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
        traverse_with_elephant(26, valves_to_open)


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


def traverse_with_elephant(minutes_remaining, remaining_valves):
    global valves
    global max_pressure

    total_pressure = 0
    my_time_left = 0
    ele_time_left = 0
    open_valves = []
    my_origin = "AA"
    ele_origin = "AA"
    my_destination = "AA"
    ele_destination = "AA"

    open_valves.append(my_destination)
    ele_distances = get_distances(remaining_valves, minutes_remaining, my_origin)
    my_distances = get_distances(remaining_valves, minutes_remaining, ele_origin)
    my_origin = my_destination
    ele_origin = ele_destination
    if ele_distances[0][0] == my_distances[0][0]:
        if my_distances[0][1] > ele_distances[0][1]:  # I take that valve
            my_time_left = 1 + valves[my_destination].distance_to_others[my_distances[0][0]]
            ele_time_left = 1 + valves[ele_destination].distance_to_others[ele_distances[1][0]]
            my_destination = my_distances[0][0]
            ele_destination = ele_distances[1][0]
        else:
            my_time_left = 1 + valves[my_origin].distance_to_others[my_distances[1][0]]
            ele_time_left = 1 + valves[ele_origin].distance_to_others[ele_distances[0][0]]
            my_destination = my_distances[1][0]
            ele_destination = ele_distances[0][0]
    remaining_valves.remove(ele_destination)
    remaining_valves.remove(my_destination)
    while minutes_remaining >= 0:
        minutes_remaining -= 1
        my_time_left -= 1
        ele_time_left -= 1
        total_pressure += calculate_pressure_release(open_valves)
        print(total_pressure)

        if ele_time_left == 0 and my_time_left == 0:  # choose new destination
            open_valves.append(my_destination)
            open_valves.append(ele_destination)
            ele_distances = get_distances(remaining_valves, minutes_remaining, ele_destination)
            my_distances = get_distances(remaining_valves, minutes_remaining, my_destination)
            my_origin = my_destination
            ele_origin = ele_destination
            if ele_distances[0][0] == my_distances[0][0]:
                if my_distances[0][1] > ele_distances[0][1]:  # I take that valve
                    my_time_left = 1 + valves[my_destination].distance_to_others[my_distances[0][0]]
                    ele_time_left = 1 + valves[ele_destination].distance_to_others[ele_distances[1][0]]
                    my_destination = my_distances[0][0]
                    ele_destination = ele_distances[1][0]
                elif my_distances[0][1] < ele_distances[0][1]:
                    my_time_left = 1 + valves[my_origin].distance_to_others[my_distances[1][0]]
                    ele_time_left = 1 + valves[ele_origin].distance_to_others[ele_distances[0][0]]
                    my_destination = my_distances[1][0]
                    ele_destination = ele_distances[0][0]
                else:
                    if my_distances[1][1] > ele_distances[1][1]:  # I take that valve
                        my_time_left = 1 + valves[my_destination].distance_to_others[my_distances[1][0]]
                        ele_time_left = 1 + valves[ele_destination].distance_to_others[ele_distances[2][0]]
                        my_destination = my_distances[1][0]
                        ele_destination = ele_distances[2][0]
                    elif my_distances[1][1] < ele_distances[1][1]:
                        my_time_left = 1 + valves[my_origin].distance_to_others[my_distances[2][0]]
                        ele_time_left = 1 + valves[ele_origin].distance_to_others[ele_distances[1][0]]
                        my_destination = my_distances[2][0]
                        ele_destination = ele_distances[1][0]
                    else:
                        print("Oh dear")
            remaining_valves.remove(my_destination)
            remaining_valves.remove(ele_destination)
        else:
            if ele_time_left == 0:
                ele_distances = get_distances(remaining_valves, minutes_remaining, ele_destination)
                open_valves.append(ele_destination)
                ele_origin = ele_destination
                ele_destination = ele_distances[0][0]
                remaining_valves.remove(ele_destination)
                ele_time_left = 1 + valves[ele_origin].distance_to_others[ele_destination]
            if my_time_left == 0:
                my_distances = get_distances(remaining_valves, minutes_remaining, my_destination)
                open_valves.append(my_destination)
                my_origin = my_destination
                my_destination = my_distances[0][0]
                remaining_valves.remove(my_destination)
                my_time_left = 1 + valves[my_origin].distance_to_others[my_destination]

    print(total_pressure)


def part1():
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


def part2():
    do_thing(2)


if __name__ == "__main__":
    part1()
    part2()
