import functools

file = open('input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]
hand_types = ["5", "4", "full", "3", "2p", "1p", "high"]
hand_values = ["6", "5", "4", "3", "2", "1", "0"]


def identify_hand(hand):
    if hand.__contains__("J"):
        return identify_hand_with_joker(hand)

    hand = ''.join(sorted(hand))

    if hand.count(hand[0]) == 5:
        return "6"
    elif hand.count(hand[0]) == 4 or hand.count(hand[-1]) == 4:
        return "5"
    elif (hand.count(hand[0]) == 3 and hand.count(hand[-1]) == 2) \
            or (hand.count(hand[0]) == 2 and hand.count(hand[-1]) == 3):
        return "4"
    elif hand.count(hand[0]) == 3 or hand.count(hand[1]) == 3 or hand.count(hand[2]) == 3:
        return "3"

    unique = set(hand)
    if len(unique) == 5:
        return "0"

    count_pairs = 0
    for c in unique:
        if hand.count(c) == 2:
            count_pairs += 1
    if count_pairs == 2:
        return "2"
    return "1"


def identify_hand_with_joker(hand):
    hand = ''.join(sorted(hand))
    jokerless_hand = ''.join(sorted(hand.replace("J", "")))
    jokers = hand.count("J")

    unique = set(jokerless_hand)
    count_pairs = 0
    for c in unique:
        if jokerless_hand.count(c) == 2:
            count_pairs += 1

    if jokers >= 4:
        return "6"  # JJJJJ or JJJJ1
    if jokers == 3:
        if len(unique) == 2:  # JJJ12
            return "5"
        elif len(unique) == 1:  # JJJ11
            return "6"
    if jokers == 2:
        if len(unique) == 1:  # JJ111
            return "6"
        if count_pairs == 1:  # JJ112
            return "5"
        if len(unique) == 3:  # JJ123
            return "3"
    if jokers == 1:
        if len(unique) == 1:
            return "6"
        if count_pairs == 2:  # J1122
            return "4"
        if count_pairs == 1:  # J1233
            return "3"
        if len(unique) == 2:  # J1112
            return "5"
        # J1234
        return "1"


card_values = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
card_values.reverse()


def secondary_compare(item1, item2):
    for i in range(len(item1)):
        val1 = card_values.index(item1[i])
        val2 = card_values.index(item2[i])
        if val1 == val2:
            continue
        if val1 < val2:
            return -1
        elif val1 > val2:
            return 1

    return 0


def compare(item1, item2):
    item1 = item1.split()[0]
    item2 = item2.split()[0]
    if identify_hand(item1) < identify_hand(item2):
        return -1
    elif identify_hand(item1) > identify_hand(item2):
        return 1
    return secondary_compare(item1, item2)


def part1():
    total_winnings = 0
    sorted_lines = sorted(lines, key=functools.cmp_to_key(compare))
    for i in range(len(sorted_lines)):
        total_winnings += (i + 1) * int(sorted_lines[i].split()[1])
    print(total_winnings)


def part2():
    total = 0
    print(total)


if __name__ == "__main__":
    part1()
    part2()
