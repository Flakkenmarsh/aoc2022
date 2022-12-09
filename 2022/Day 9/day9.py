import math
file = open('input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def print_map(map0, head, tail):
    return
    for i in range(len(map0)):
        line = ""
        for j in range(len(map0[0])):
            if i == head.x and j == head.y:
                line += "H"
            elif i == tail.x and j == tail.y:
                line += "T"
            elif map0[i][j] == "#":
                line += "#"
            else:
                line += "."
        print(line)
    print("")


def ends_touch(head, tail):
    if abs(head.x - tail.x) <= 1 and abs(head.y - tail.y) <= 1:
        return True

    return False


def get_move_diff(diff):
    if abs(diff) == 2:
        diff = int(diff/2)
    return diff


def move_tail(map0, head, tail):
    if ends_touch(head, tail):
        return tail

    if head.x == tail.x and abs(head.y - tail.y) == 2:
        diff = get_move_diff(head.y - tail.y)
        tail.y += diff
        map0[tail.x][tail.y] = 'T'
    elif head.y == tail.y and abs(head.x - tail.x) == 2:
        diff = get_move_diff(head.x - tail.x)
        tail.x += diff
        map0[tail.x][tail.y] = 'T'
    else:
        # diagonal
        diff_x = get_move_diff(head.x - tail.x)
        diff_y = get_move_diff(head.y - tail.y)
        tail.x += diff_x
        tail.y += diff_y

    return tail


def part1():
    width = 0
    height = 0
    start = Point(0, 0)

    for line in lines:
        values = line.split(" ")
        if values[0] == 'R' or values[0] == 'L':
            width += int(values[1])
            if values[0] == 'L':
                start.x += int(values[1])
        else:
            height += int(values[1])
            if values[0] == 'U':
                start.y += int(values[1])
    start.y += 1
    start.x += 1
    head = Point(start.x, start.y)
    tail = Point(start.x, start.y)

    map0 = [["." for _ in range(width + 4)] for _ in range(height + 4)]
    visited = [["." for _ in range(width + 4)] for _ in range(height + 4)]
    visited[tail.x][tail.y] = "#"
    print_map(visited, head, tail)
    for line in lines:
        print(line)
        values = line.split(" ")
        for i in range(int(values[1])):
            print(i)
            map0[tail.x][tail.y] = "T"
            visited[tail.x][tail.y] = "#"
            if values[0] == "U":
                head.x -= 1
            elif values[0] == "D":
                head.x += 1
            elif values[0] == "R":
                head.y += 1
            else:
                head.y -= 1
            print("===========")
            print_map(map0, head, tail)
            tail = move_tail(map0, head, tail)
            print_map(map0, head, tail)
            print("===========")
            # print_map(visited, head, tail)

    visits = 0
    for row in visited:
        visits += row.count("#")

    print(visits)


def part2():
    for line in lines:
        pass


if __name__ == "__main__":
    part1()
    part2()
