ranges = [(0, 5), (0, 6), (6, 8), (7, 10), (12, 20), (12, 15), (14, 17)]

ranges.sort()
print(ranges)

left = ranges[0][0]
right = ranges[0][1]

for i in range(len(ranges)-1):
    if left <= ranges[i+1][0] <= right:
        if ranges[i+1][1] > right:
            right = ranges[i+1][1]
    if ranges[i+1][0] - right > 1:
        print(right + 1)
        break

print("Done")
