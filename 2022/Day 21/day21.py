file = open('2022/Day 21/input.csv', 'r')
lines = file.readlines()
lines = [line.strip('\n' ',') for line in lines]


class Monkey:
    def __init__(self, name, statement):
        self.name = name
        self.statement = statement
        params = statement.split(" ")
        self.required_monkeys = []
        self.has_shouted = False
        self.is_value = False
        if len(params) == 1:
            self.value = int(params[0])
            self.operation = None
            self.is_value = True
        else:
            self.value = None
            self.required_monkeys = [params[0], params[2]]
            if params[1] == "+":
                self.operation = lambda x, y: x + y
            elif params[1] == "-":
                self.operation = lambda x, y: x - y
            elif params[1] == "*":
                self.operation = lambda x, y: x * y
            elif params[1] == "/":
                self.operation = lambda x, y: x / y
            elif params[1] == "=":
                self.operation = lambda x, y: x == y


def all_have_shouted(monkeys):
    for key in monkeys:
        if not monkeys[key].has_shouted:
            return False

    return True


def part1():
    monkeys = {}
    for line in lines:
        params = line.split(": ")
        m = Monkey(params[0], params[1])
        monkeys[params[0]] = m

    while not all_have_shouted(monkeys):
        for key in monkeys:
            monkey = monkeys[key]
            if monkey.is_value:
                monkey.has_shouted = True
            else:
                if monkeys[monkey.required_monkeys[0]].has_shouted and monkeys[monkey.required_monkeys[1]].has_shouted:
                    monkey.value = monkey.operation(monkeys[monkey.required_monkeys[0]].value, monkeys[monkey.required_monkeys[1]].value)
                    monkey.has_shouted = True
        if monkeys["root"].has_shouted:
            print(monkeys["root"].value)
            break


def part2():
    monkeys = {}
    for line in lines:
        params = line.split(": ")
        if params[0] == "root":
            params[1] = params[1].replace("+", "=")
        m = Monkey(params[0], params[1])
        monkeys[params[0]] = m

    while False:  # not all_have_shouted(monkeys):
        for key in monkeys:
            monkey = monkeys[key]
            if monkey.is_value:
                monkey.has_shouted = True
            else:
                if monkeys[monkey.required_monkeys[0]].has_shouted and monkeys[monkey.required_monkeys[1]].has_shouted:
                    monkey.value = monkey.operation(monkeys[monkey.required_monkeys[0]].value, monkeys[monkey.required_monkeys[1]].value)
                    monkey.has_shouted = True
        if monkeys["root"].has_shouted:
            print(monkeys["root"].value)
            break
    
    monkey = monkeys["root"]
    queue = [monkey]
    values = []
    equation = ""
    while len(queue) > 0:
        monkey = queue.pop()
        if monkey.name == "humn":
            print(monkey.value)
            break
        if monkey.is_value:
            monkey.has_shouted = True
        else:
            if not monkeys[monkey.required_monkeys[0]].has_shouted and not queue.__contains__(monkey.required_monkeys[0]):
                queue.append(monkeys[monkey.required_monkeys[0]])
            if not monkeys[monkey.required_monkeys[1]].has_shouted and not queue.__contains__(monkey.required_monkeys[1]):
                queue.append(monkeys[monkey.required_monkeys[1]])




if __name__ == "__main__":
    # part1()
    part2()
