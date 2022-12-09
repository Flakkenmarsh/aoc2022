import time

file = open('input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]
padding = 0


class Point:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name


def print_map(map0, head, tail):
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


def print_map_2(rope, height, width):
    global padding

    window_size = 10

    temp = [["." for _ in range(height + padding)] for _ in range(width + padding)]
    for i in range(len(rope) - 1, -1, -1):
        print(i)
        knot = rope[i]
        temp[knot.x][knot.y] = knot.name

    for i in range(rope[0].x - window_size, rope[0].x + window_size):
        print("".join(temp[i][rope[0].y - window_size:rope[0].y + window_size]))

    print("\n"*(10))
    print("")
    time.sleep(0.1)


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


def move_tail_2(map0, head, tail):
    if ends_touch(head, tail):
        return tail

    if head.x == tail.x and abs(head.y - tail.y) == 2:
        diff = get_move_diff(head.y - tail.y)
        tail.y += diff
    elif head.y == tail.y and abs(head.x - tail.x) == 2:
        diff = get_move_diff(head.x - tail.x)
        tail.x += diff
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
    time.sleep(10)
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

    visited[tail.x][tail.y] = "#"
    visits = 0
    for row in visited:
        visits += row.count("#")

    print(visits)


def part2():
    global padding
    x = y = 0
    left = right = top = bottom = 0

    for line in lines:
        values = line.split(" ")
        if values[0] == 'R' or values[0] == 'L':
            if values[0] == 'R':
                x += int(values[1])
            else:
                x -= int(values[1])

            if x >= right:
                right = x
            elif x <= left:
                left = x
        else:
            if values[0] == 'D':
                y += int(values[1])
            else:
                y -= int(values[1])

            if y <= top:
                top = y
            elif y >= bottom:
                bottom = y

    start = Point(abs(left), abs(top), "H")
    width = abs(right) + abs(left)
    height = abs(top) + abs(bottom)
    rope = [Point(start.x, start.y, str(i)) for i in range(10)]

    map0 = [["." for _ in range(height + padding)] for _ in range(width + padding)]
    visited = [["." for _ in range(height + padding)] for _ in range(width + padding)]
    visited[rope[-1].x][rope[-1].y] = "#"
    for line in lines:
        values = line.split(" ")
        for i in range(int(values[1])):
            if values[0] == "U" or values[0] == "D":
                rope[0].x += 1 if values[0] == "D" else -1

            elif values[0] == "R":
                rope[0].y += 1
            else:
                rope[0].y -= 1

            for j in range(len(rope)-1):
                rope[j+1] = move_tail_2(map0, rope[j], rope[j+1])
                print_map_2(rope, height, width)
            visited[rope[-1].x][rope[-1].y] = "#"
            
    visits = 0
    for row in visited:
        visits += row.count("#")
        print("".join(row))
    
    for knot in rope:
        print(knot.name, ": ", knot.x, ",", knot.y)
    print(visits)


if __name__ == "__main__":
    # part1()
    part2()
