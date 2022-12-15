import copy
from copy import deepcopy
import math

file = open('input.csv', 'r')
lines = file.readlines()
lines = ["~" + line.strip('\n' ',') + "~" for line in lines]
min_distance = math.inf
height_map = [[c for c in line] for line in lines]
height_map.insert(0, "~" * (len(height_map[0])))
height_map.append('~' * (len(height_map[0])))

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
    print_map(matrix)
    # Defining visited array to keep
    # track of already visited indexes
    visited = [[False for _ in range(m)] for _ in range(n)]

    # Flag to indicate whether the
    # path exists or not
    flag = False

    for i in range(m):
        for j in range(n):
            # If matrix[i][j] is source
            # and it is not visited
            if matrix[i][j] == "S" and not visited[i][j]:

                # Starting from i, j and
                # then finding the path
                if (checkPath(matrix, i,
                              j, visited)):
                    # If path exists
                    flag = True
                    break
    if flag:
        print("YES")
    else:
        print("NO")


# Method for checking boundaries
def isSafe(i, j, matrix):
    if (i >= 0 and i < len(matrix) and
            j >= 0 and j < len(matrix[0])):
        return True
    return False


# Returns true if there is a
# path from a source(a
# cell with value 1) to a
# destination(a cell with
# value 2)
def checkPath(matrix, i, j, visited):
    # Checking the boundaries, walls and
    # whether the cell is unvisited
    print_map(matrix)
    print(i, ", ", j)
    if matrix[i][j] != "~" and not visited[i][j]:
        # Make the cell visited
        visited[i][j] = True

        # If the cell is the required
        # destination then return true
        if matrix[i][j] == "E":
            return True

        # traverse up
        if ord(matrix[i][j]) - ord(matrix[i-1][j]) <= 1:
            up = checkPath(matrix, i - 1, j, visited)
            # If path is found in up direction return true
            if up:
                return True

        # Traverse left
        if ord(matrix[i][j]) - ord(matrix[i][j-1]) <= 1:
            left = checkPath(matrix, i, j - 1, visited)
            # If path is found in left direction return true
            if left:
                return True

        # Traverse down
        if ord(matrix[i][j]) - ord(matrix[i+1][j]) <= 1:
            down = checkPath(matrix, i + 1, j, visited)
            # If path is found in down direction return true
            if down:
                return True

        # Traverse right
        if ord(matrix[i][j]) - ord(matrix[i][j + 1]) <= 1:
            right = checkPath(matrix, i, j + 1, visited)
            # If path is found in right direction return true
            if right:
                return True

    # No path has been found
    return False


# Driver code
if __name__ == "__main__":
    # calling isPath method
    isPath(height_map, len(height_map), len(height_map[0]))
