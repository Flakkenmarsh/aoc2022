import copy

file = open('input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]


def setup():
    score = 0
    win = ["A Y", "B Z", "C X"]
    draw = ["A X", "B Y", "C Z"]
    for line in lines:
        moves = line.split(" ")
        if moves[1] == "X":
            score += 1
        elif moves[1] == "Y":
            score += 2
        else:
            score += 3
        if win.__contains__(line):
            score += 6
        elif draw.__contains__(line):
            score += 3

    print(score)


def part1():
    pass


def part2():
    score = 0
    for line in lines:
        moves = line.split(" ")
        if moves[1] == "X":
            if moves[0] == "A":  # rock
                score += 3  # need to play scissors
            elif moves[0] == "B":  # paper
                score += 1  # need to play rock
            else:
                score += 2
        elif moves[1] == "Y":
            score += 3
            if moves[0] == "A":  # rock
                score += 1
            elif moves[0] == "B":  # paper
                score += 2
            else:
                score += 3
        else:
            score += 6
            if moves[0] == "A":  # rock
                score += 2
            elif moves[0] == "B":  # paper
                score += 3
            else:
                score += 1

    print(score)


if __name__ == "__main__":
    # setup()
    # part1()
    part2()
