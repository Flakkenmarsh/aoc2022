file = open('2022/Day 20/input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]


class Item:
    def __init__(self, value, original_index):
        self.value = value
        self.original_index = original_index
        self.has_moved = False
        self.next = None
        self.previous = None


    def __str__(self):
        return self.value


def print_list(circ):
    string = ""
    for c in circ:
        if c.has_moved:
            string += "[" + str(c.value) + "] "
        else:
            string += str(c.value) + " "

    string += "\n"
    print(string)


def part1():
    circular = []
    for line in lines:
        circular.append(Item(int(line)))

    all_done = False
    while not all_done:
        index = 0
        while index < len(circular):
            if circular[index].has_moved:
                index += 1
                continue
            #print(circular[index].value)
            if circular[index].value == 0:
                circular[index].has_moved = True
                #print_list(circular)
                continue
            new_index = index + circular[index].value
            if new_index >= len(circular):
                #print("gt")
                new_index = new_index % (len(circular)-1)# + 1
            elif new_index < 0:
                #print("lt")
                new_index = new_index % (len(circular)-1)# - 1
            temp_item = circular[index]
            temp_item.has_moved = True
            new_circular = circular[:index] + circular[index+1:]
            #print_list(new_circular)
            new_circular.insert(new_index, temp_item)
            
            
            #print_list(new_circular)
            
            circular = new_circular
            # circular = new_circular[:new_index] + [temp_item] + new_circular[new_index:]
            # print_list(circular)
            break
        if index == len(circular):
            all_done = True
        # print_list(circular)

    zero = 0
    for i in range(len(circular)):
        if circular[i].value == 0:
            zero = i
            break

    #print_list(circular)
    values = []
    index = zero + 1000
    index = index % len(circular)
    values.append(circular[index].value)
    print(circular[index].value)
    index = zero + 2000
    index = index % len(circular)
    values.append(circular[index].value)
    print(circular[index].value)
    index = zero + 3000
    index = index % len(circular)
    values.append(circular[index].value)
    print(circular[index].value)
    print(sum(values))


def part2():
    circular = []
    index = 0
    last_item = None
    for line in lines:
        circular.append(Item(int(line), index))
        index += 1
    for i in range(len(circular)-1):
        circular[i].next = circular[i+1]
        circular[i].previous = circular[i-1]

    head = circular[0]

    all_done = False
    while not all_done:
        index = 0
        while index < len(circular):
            if circular[index].has_moved:
                index += 1
                continue
            #print(circular[index].value)
            if circular[index].value == 0:
                circular[index].has_moved = True
                #print_list(circular)
                continue
            new_index = index + circular[index].value
            if new_index >= len(circular):
                #print("gt")
                new_index = new_index % (len(circular)-1)# + 1
            elif new_index < 0:
                #print("lt")
                new_index = new_index % (len(circular)-1)# - 1
            temp_item = circular[index]
            temp_item.has_moved = True
            new_circular = circular[:index] + circular[index+1:]
            #print_list(new_circular)
            new_circular.insert(new_index, temp_item)
            
            
            #print_list(new_circular)
            
            circular = new_circular
            # circular = new_circular[:new_index] + [temp_item] + new_circular[new_index:]
            # print_list(circular)
            break
        if index == len(circular):
            all_done = True
        # print_list(circular)

    zero = 0
    for i in range(len(circular)):
        if circular[i].value == 0:
            zero = i
            break

    #print_list(circular)
    values = []
    index = zero + 1000
    index = index % len(circular)
    values.append(circular[index].value)
    print(circular[index].value)
    index = zero + 2000
    index = index % len(circular)
    values.append(circular[index].value)
    print(circular[index].value)
    index = zero + 3000
    index = index % len(circular)
    values.append(circular[index].value)
    print(circular[index].value)
    print(sum(values))

    
if __name__ == "__main__":
    part1()