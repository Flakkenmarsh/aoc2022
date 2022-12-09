file = open('input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]
lines = [[int(c) for c in line] for line in lines]


def print_trees(forest0):
    for line in forest0:
        print(line)


def part1():
    visible = [[False for _ in line] for line in lines]
    visible[0][0] = visible[-1][0] = True
    visible[-1][-1] = visible[0][-1] = True
    forest = lines
    for i in range(len(forest)):
        tallest = -1
        for j in range(0, len(forest[0])):
            if forest[i][j] > tallest:
                visible[i][j] = True
                tallest = forest[i][j]
        tallest = -1
        for j in range(len(forest[0]) - 1, 0, -1):
            if forest[i][j] > tallest:
                visible[i][j] = True
                tallest = forest[i][j]

    for i in range(len(forest)):
        tallest = -1
        for j in range(0, len(forest[0])):
            if forest[j][i] > tallest:
                visible[j][i] = True
                tallest = forest[j][i]
        tallest = -1
        for j in range(len(forest[0]) - 1, 0, -1):
            if forest[j][i] > tallest:
                visible[j][i] = True
                tallest = forest[j][i]

    visible_trees = sum([line.count(True) for line in visible])

    print(visible_trees)


def get_scenic_score(forest0, i, j):
    tree = forest0[i][j]

    # left
    distance1 = 0
    for i2 in range(i-1, -1, -1):
        if forest0[i2][j] >= tree:
            distance1 += 1
            break
        distance1 += 1

    # right
    distance2 = 0
    for i2 in range(i+1, len(forest0)):
        if forest0[i2][j] >= tree:
            distance2 += 1
            break
        distance2 += 1

    # up
    distance3 = 0
    for j2 in range(j - 1, -1, -1):
        if forest0[i][j2] >= tree:
            distance3 += 1
            break
        distance3 += 1

    # down
    distance4 = 0
    for j2 in range(j + 1, len(forest0)):
        if forest0[i][j2] >= tree:
            distance4 += 1
            break
        distance4 += 1

    return distance1 * distance2 * distance3 * distance4


def part2():
    scenic_score = [[0 for _ in line] for line in lines]
    scenic_score[0][0] = scenic_score[-1][0] = 0
    scenic_score[-1][-1] = scenic_score[0][-1] = 0
    forest = lines
    for i in range(len(forest)):
        for j in range(0, len(forest[0])):
            scenic_score[i][j] = get_scenic_score(forest, i, j)

    print(max(max(x) for x in scenic_score))


if __name__ == "__main__":
    part1()
    part2()
