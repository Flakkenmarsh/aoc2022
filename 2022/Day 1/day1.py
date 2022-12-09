file = open('input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]


def setup():
    arr = [0]
    i = 0
    for line in lines:
        if line == "":
            i += 1
            arr.append(0)
            continue
        arr[i] += int(line)

    print(max(arr))
    print(sum(sorted(arr, reverse=True)[0:3]))


if __name__ == "__main__":
    setup()
