import math
import re

file = open('input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]


class Card:
    def __init__(self, duplicates):
        self.duplicates = duplicates

    def print(self):
        print("duplicates: " + str(self.duplicates))


def part1():
    total_winnings = 0
    separator = 6
    # separator = 11
    for line in lines:
        numbers = re.findall(r'\d+', line)
        winning_numbers = [int(n) for n in numbers[1:separator]]
        my_numbers = [int(n) for n in numbers[separator:]]
        total_matches = 0
        first = True
        for my_number in my_numbers:
            if my_number in winning_numbers:
                if first:
                    total_matches = 1
                    first = False
                else:
                    total_matches *= 2
        if total_matches > 0:
            print(numbers[0] + ": " + str(total_matches) + " => " + str(total_winnings))
        total_winnings += total_matches

    print(total_winnings)


def part2():
    # separator = 6 23, 11 40
    print(lines[0].find("|"))
    separator = (lines[0].find("|") - 8)/3 + 1

    card_duplicates = [1 for _ in range(len(lines))]
    card_number = 0

    while card_number < len(lines):
        numbers = re.findall(r'\d+', lines[card_number])
        winning_numbers = [int(n) for n in numbers[1:separator]]
        my_numbers = [int(n) for n in numbers[separator:]]
        number_of_matches = 0
        for my_number in my_numbers:
            if my_number in winning_numbers:
                number_of_matches += 1

        winning_range = card_number + number_of_matches + 1
        for i in range(card_number+1, winning_range):
            card_duplicates[i] += card_duplicates[card_number]

        card_number += 1

    number_of_cards = 0
    for card in card_duplicates:
        number_of_cards += card

    print(number_of_cards)


if __name__ == "__main__":
    # part1()
    part2()
