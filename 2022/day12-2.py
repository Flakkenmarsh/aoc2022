import copy
from copy import deepcopy
import math

file = open('2022/input12.csv', 'r')
lines = file.readlines()
lines = ["~" + line.strip('\n' ',') + "~" for line in lines]
min_distance = math.inf
height_map = [[c for c in line] for line in lines]
height_map.insert(0, "~" * (len(height_map[0])))
height_map.append('~' * (len(height_map[0])))

min_distance = math.inf
min_distances = [min_distance]

start = (0, 0)
end = (0, 0)
for m in range(len(height_map)):
    for n in range(len(height_map[0])):
        if height_map[m][n] == "S":
            start = (m, n)
        elif height_map[m][n] == "E":
            end = (m, n)


def print_map(map0):
    for row in map0:
        print("".join(row))
    print("")


# Python3 program to find
# path between two cell in matrix

# Method for finding and printing
# whether the path exists or not


def isPath(matrix, m, n):
    global min_distances

    print_map(matrix)
    # Defining visited array to keep
    # track of already visited indexes
    visited = [[False for _ in range(n)] for _ in range(m)]

    # Flag to indicate whether the
    # path exists or not
    flag = False

    checkPath(copy.deepcopy(height_map), start[0], start[1], copy.deepcopy(visited), 0)
    print(min_distances)
    if flag:
        print("YES")
    else:
        print("NO")


# Method for checking boundaries
def isSafe(i, j, matrix):
    if matrix[i][j] != "~":
        return True
    return False
    if (i >= 0 and i < len(matrix) and
            j >= 0 and j < len(matrix[0])):
        return True
    return False


# Returns true if there is a
# path from a source(a
# cell with value 1) to a
# destination(a cell with
# value 2)
def checkPath(matrix, i, j, visited, distance):
    global end
    global min_distances

    # Checking the boundaries, walls and
    # whether the cell is unvisited
    print_map(matrix)
    print(i, ", ", j)
    if matrix[i][j] == "~" or visited[i][j]:
        return False

    # Make the cell visited
    visited[i][j] = True

    # If the cell is the required
    # destination then return true
    if i == end[0] and j == end[1]:
        min_distances.append(distance)
        print(distance)
        return True

    # traverse up
    if ord(matrix[i][j]) - ord(matrix[i-1][j]) <= 1:
        up = checkPath(matrix, i - 1, j, visited, distance+1)
        # If path is found in up direction return true
        if up:
            return True

    # Traverse left
    if ord(matrix[i][j]) - ord(matrix[i][j-1]) <= 1:
        left = checkPath(matrix, i, j - 1, visited, distance+1)
        # If path is found in left direction return true
        if left:
            return True

    # Traverse down
    if ord(matrix[i][j]) - ord(matrix[i+1][j]) <= 1:
        down = checkPath(matrix, i + 1, j, visited, distance+1)
        # If path is found in down direction return true
        if down:
            return True

    # Traverse right
    if ord(matrix[i][j]) - ord(matrix[i][j + 1]) <= 1:
        right = checkPath(matrix, i, j + 1, visited, distance+1)
        # If path is found in right direction return true
        if right:
            return True

    # No path has been found
    return False


# Driver code
if __name__ == "__main__":
    # calling isPath method
    isPath(height_map, len(height_map), len(height_map[0]))
