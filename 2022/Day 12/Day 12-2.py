import numpy as np
import sys
import heapq
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

file = open('input.csv', 'r')
lines = file.readlines()
lines = ["~" + line.strip('\n' ',') + "~" for line in lines]
grid = [[c for c in line] for line in lines]
grid.insert(0, "~"*(len(grid[0])))
grid.append('~'*(len(grid[0])))
# grid = np.array(grid)

start = (0, 0)
goal = (0, 0)
for i in range(len(grid)):
    for j in range(len(grid[0])):
        if grid[i][j] == "S":
            start = (i, j)
        elif grid[i][j] == "E":
            end = (i, j)
        if grid[start[0]][start[1]] == "S" and grid[goal[0]][goal[1]] == "E":
            break
    if grid[start[0]][start[1]] == "S" and grid[goal[0]][goal[1]] == "E":
        break


class Graph():
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for _ in range(vertices[0])]
                      for _ in range(vertices[1])]

    def print_solution(self, dist):
        print("Vertex \tDistance from Source")
        for node in range(self.V):
            print(node, "\t", dist[node])

    # A utility function to find the vertex with
    # minimum distance value, from the set of vertices
    # not yet included in shortest path tree
    def min_distance(self, dist, sptSet):
        # Initialize minimum distance for next node
        min = sys.maxsize

        # Search not nearest vertex not in the
        # shortest path tree
        for u in range(self.V):
            if dist[u] < min and sptSet[u] is False:
                min = dist[u]
                min_index = u

        return min_index

    # Function that implements Dijkstra's single source
    # shortest path algorithm for a graph represented
    # using adjacency matrix representation
    def dijkstra(self, src):
        dist = [sys.maxsize] * self.V
        dist[src] = 0
        sptSet = [False] * self.V

        for cout in range(self.V[0]):

            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            # x is always equal to src in first iteration
            x = self.min_distance(dist, sptSet)

            # Put the minimum distance vertex in the
            # shortest path tree
            sptSet[x] = True

            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shortest path tree
            for y in range(self.V[1]):
                if self.graph[x][y] > 0 and sptSet[y] is False and \
                        dist[y] > dist[x] + self.graph[x][y]:
                    dist[y] = dist[x] + self.graph[x][y]

        self.print_solution(dist)


# Driver's code
if __name__ == "__main__":
    g = Graph((len(grid), len(grid[0])))
    g.graph = grid

    g.dijkstra(0)
