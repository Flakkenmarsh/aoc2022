import re

file = open('input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]


def setup():
    possible_ids_sum = 0
    max_red = 12
    max_green = 13
    max_blue = 14
    for line in lines:
        line = line.replace(": ", ":").replace("; ", ";").replace(", ", ",")
        name_game = line.split(":")
        game_id = int(re.findall(r'\d+', name_game[0])[0])
        games = name_game[1].split(";")
        valid_game = True

        for draw in games:
            cubes = draw.split(",")
            for cube in cubes:
                if valid_game is False:
                    break
                count_colour = cube.split(" ")
                if count_colour[1] == "blue" and int(count_colour[0]) > max_blue:
                    valid_game = False
                if count_colour[1] == "red" and int(count_colour[0]) > max_red:
                    valid_game = False
                if count_colour[1] == "green" and int(count_colour[0]) > max_green:
                    valid_game = False

        if valid_game:
            print(game_id)
            possible_ids_sum = possible_ids_sum + game_id

    print(possible_ids_sum)


def part2():
    game_power = 0
    for line in lines:
        line = line.replace(": ", ":").replace("; ", ";").replace(", ", ",")
        name_game = line.split(":")
        games = name_game[1].split(";")
        max_red = 0
        max_green = 0
        max_blue = 0
        for draw in games:
            cubes = draw.split(",")
            for cube in cubes:
                count_colour = cube.split(" ")
                if count_colour[1] == "blue" and int(count_colour[0]) > max_blue:
                    max_blue = int(count_colour[0])
                if count_colour[1] == "red" and int(count_colour[0]) > max_red:
                    max_red = int(count_colour[0])
                if count_colour[1] == "green" and int(count_colour[0]) > max_green:
                    max_green = int(count_colour[0])

        game_power = game_power + max_red * max_green * max_blue

    print(game_power)


if __name__ == "__main__":
    part2()
