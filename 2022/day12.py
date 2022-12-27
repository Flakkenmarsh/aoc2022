from contextlib import redirect_stdout
import copy
from copy import deepcopy
import math
from re import X
from xml.dom.minidom import NamedNodeMap

file = open('2022/input12.csv', 'r')
lines = file.readlines()
lines = ["~" + line.strip('\n' ',') + "~" for line in lines]
min_distance = math.inf
min_distances = [min_distance]


class Node:
    def __init__(self, value, neighbours, is_destination, x, y):
        self.value = value
        self.neighbours = neighbours
        self.is_destination = is_destination
        self.x = x
        self.y = y
        self.dead_end = False


def print_visited(visited_map):
    screen = ""
    for row in visited_map:
        screen += "".join(row) + "\n"
    print(screen)
    print("\n"*20)


def get_neighbours(h_map, n_map, x, y):
    current_value = h_map[x][y]
    if current_value == "~":
        return None

    neighbours = []

    # right
    if ord(h_map[x][y+1]) - ord(current_value) <= 1:
        neighbours.append(n_map[x][y+1])
    # up
    if ord(h_map[x-1][y]) - ord(current_value) <= 1:
        neighbours.append(n_map[x-1][y])

    # down
    if ord(h_map[x+1][y]) - ord(current_value) <= 1:
        neighbours.append(n_map[x+1][y])

    # left
    if ord(h_map[x][y-1]) - ord(current_value) <= 1:
        neighbours.append(n_map[x][y-1])

    return neighbours


def search(visited_map, visited, node, distance):
    global min_distances
    global node_map

    print_visited(visited_map)

    if node_map[node.x][node.y].dead_end:
        return False
    if visited_map[node.x][node.y] == "." or visited.__contains__(node):
        node_map[node.x][node.y].dead_end = True
        return False

    if distance >= min(min_distances):
        node_map[node.x][node.y].dead_end = True
        return False
    if node.is_destination:
        print("Found: ", distance)
        min_distances.append(distance)
        return True

    visited.append(node)
    visited_map[node.x][node.y] = "."

    overall_found = False
    for neighbour in node.neighbours:
        if visited.__contains__(neighbour):
            continue

        found = search(copy.deepcopy(visited_map), visited, neighbour, distance+1)
        if found:
            overall_found = True

    return overall_found


def BFS_SP(start, goal):
    # https://www.geeksforgeeks.org/building-an-undirected-graph-and-finding-shortest-path-using-dictionaries-in-python/
    explored = []
     
    # Queue for traversing the
    # graph in the BFS
    queue = [[start]]
     
    # If the desired node is
    # reached
    if start == goal:
        print("Same Node")
        return
    
    # Loop to traverse the graph
    # with the help of the queue
    while queue:
        path = queue.pop(0)
        node = path[-1]
        # Condition to check if the
        # current node is not visited
        if node not in explored:
            neighbours = node.neighbours
             
            # Loop to iterate over the
            # neighbours of the node
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                 
                # Condition to check if the
                # neighbour node is the goal
                if neighbour == goal:
                    print("Shortest path = ", len(new_path)-1)
                    return
            explored.append(node)

    return


def part1():
    global min_distance
    global min_distances
    global node_map
    global height_map
    
    height_map = [[c for c in line] for line in lines]
    height_map.insert(0, "~"*(len(height_map[0])))
    height_map.append(['~']*(len(height_map[0])))

    start = (-1, -1)
    end = (-1, -1)
    for i in range(len(height_map)):
        for j in range(len(height_map[0])):
            if height_map[i][j] == "S":
                start = (i, j)
                height_map[i][j] = "a"
            elif height_map[i][j] == "E":
                end = (i, j)
                height_map[i][j] = "z"
            if start[0] != -1 and end[0] != -1:
                break
        if start[0] != -1 and end[0] != -1:
                break

    node_map = [[Node('~', [], False, 0, 0) for _ in row] for row in height_map]
    node_map[end[0]][end[1]].is_destination = True
    node_map[end[0]][end[1]].value = "z"
    node_map[start[0]][start[1]].value = "a"
    for i in range(0, len(height_map)):
        for j in range(0, len(height_map[0])):
            node_map[i][j].value = height_map[i][j]
            if node_map[i][j].value != "~":
                node_map[i][j].neighbours = get_neighbours(height_map, node_map, i, j)
            node_map[i][j].x = i
            node_map[i][j].y = j

    start_node = node_map[start[0]][start[1]]
    end_node = node_map[end[0]][end[1]]
    BFS_SP(start_node, end_node)
    return


if __name__ == "__main__":
    part1()
