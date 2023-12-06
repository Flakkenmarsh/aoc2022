import re

file = open('input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]
number_names = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]


def setup():
    total = 0
    for line in lines:
        match = re.findall(r'\d+', line)
        value = int(match[0][0])*10 + int(match[-1][-1])
        total += value

    print(total)


def part2():
    global number_names

    total = 0
    for line in lines:
        numbers = re.findall(r'\d+', line)
        first_index = line.find(numbers[0][0])
        last_index = line.rfind(numbers[-1][-1])
        first_value = numbers[0][0]
        last_value = numbers[-1][-1]
        i = 1
        for n in number_names:
            if line.__contains__(n) and i > -1:
                if line.find(n) < first_index:
                    first_index = line.find(n)
                    first_value = i

                if line.rfind(n) > last_index:
                    last_index = line.rfind(n)
                    last_value = i
            i += 1
        print(str(first_value) + ", " + str(last_value))
        total += int(first_value) * 10 + int(last_value)

        print(total)


if __name__ == "__main__":
    part2()
