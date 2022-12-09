file = open('input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]


def puzzle(message_len):
    for line in lines:
        for i in range(len(line)-message_len):
            substring = line[i:i+message_len]
            if len(set(substring)) == len(substring):
                print(i+message_len)
                break


if __name__ == "__main__":
    puzzle(4)
    puzzle(14)
