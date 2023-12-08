import math

file = open('input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]


def part1():
    total_steps = 0
    steps = lines[0]
    the_map = []

    for line in lines:
        if "=" not in line:
            continue
        clean_line = line.replace(" ", "").replace("(", "").replace(")", "").replace("=", ",")
        the_map.append(clean_line.split(","))

    current_location = "AAA"
    location_indexes = [i[0] for i in the_map]

    step_index = 0
    while current_location != "ZZZ":
        if step_index >= len(steps):
            step_index = 0

        next_index = location_indexes.index(current_location)
        if steps[step_index] == "R":
            current_location = the_map[next_index][2]
        else:
            current_location = the_map[next_index][1]

        total_steps += 1
        step_index += 1

    print(total_steps)


def all_at_destination(locations):
    for l in locations:
        if not l.endswith("Z"):
            return False

    return True


def part2():
    total_steps = []
    steps = lines[0]
    the_map = []

    for line in lines:
        if "=" not in line:
            continue
        clean_line = line.replace(" ", "").replace("(", "").replace(")", "").replace("=", ",")
        the_map.append(clean_line.split(","))

    location_indexes = [i[0] for i in the_map]
    current_locations = []
    for li in location_indexes:
        if li.endswith("A"):
            current_locations.append(li)

    step_index = 0
    for i in range(len(current_locations)):
        current_location = current_locations[i]
        steps_taken = 0
        while not current_location.endswith("Z"):
            if step_index >= len(steps):
                step_index = 0

            next_index = location_indexes.index(current_location)
            if steps[step_index] == "R":
                current_location = the_map[next_index][2]
            else:
                current_location = the_map[next_index][1]

            step_index += 1
            steps_taken += 1
        total_steps.append(steps_taken)
    print(total_steps)
    print(math.lcm(11567, 21251, 12643, 16409, 19099, 14257))  # copy result of total steps in here


if __name__ == "__main__":
    # print("Part 1: ", end="")
    # part1()
    print("Part 2: ", end="")
    part2()
