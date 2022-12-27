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
            self.reverse_operation = None
            self.is_value = True
        else:
            self.value = None
            self.required_monkeys = [params[0], params[2]]
            if params[1] == "+":
                self.operation = lambda x, y: x + y
                self.reverse_operation = lambda target, y: target - y
            elif params[1] == "-":
                self.operation = lambda x, y: x - y
                self.reverse_operation = lambda target, y: target + y
            elif params[1] == "*":
                self.operation = lambda x, y: x * y
                self.reverse_operation = lambda target, y: target / y
            elif params[1] == "/":
                self.operation = lambda x, y: x / y
                self.reverse_operation = lambda target, y: target * y
            elif params[1] == "=":
                self.operation = lambda x, y: x == y
                self.reverse_operation = lambda target, y: target == y


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
            print("Part 1:", monkeys["root"].value)
            return monkeys["root"].value


def calculate(monkeys, monkey_name):
    monkey = monkeys[monkey_name]
    if monkey.name == "humn":
        return None
    if monkey.is_value:
        return monkey.value
    left = calculate(monkeys, monkey.required_monkeys[0])
    right = calculate(monkeys, monkey.required_monkeys[1])
    if left == None or right == None:
        return None
    return monkey.operation(left, right)


def calculate_part2(monkeys, monkey_name, target):
    monkey = monkeys[monkey_name]
    if monkey.name == "humn":
        print("humn value =", target)
        return target
    if monkey.is_value:
        return monkey.value

    left = calculate(monkeys, monkey.required_monkeys[0])
    right = calculate(monkeys, monkey.required_monkeys[1])

    if left == None:
        if monkey.statement.__contains__("="):
            left = calculate_part2(monkeys, monkey.required_monkeys[0], target)
        else:
            left = calculate_part2(monkeys, monkey.required_monkeys[0], monkey.reverse_operation(target, right))
    if right == None:
        if monkey.statement.__contains__("/"):
            right = calculate_part2(monkeys, monkey.required_monkeys[1], monkey.reverse_operation(left, 1/target))
        elif monkey.statement.__contains__("="):
            right = calculate_part2(monkeys, monkey.required_monkeys[0], target)
        elif monkey.statement.__contains__("-"):
            right = calculate_part2(monkeys, monkey.required_monkeys[1], monkey.reverse_operation(-1*target, left))
        else:
            right = calculate_part2(monkeys, monkey.required_monkeys[1], monkey.reverse_operation(target, left))

    return monkey.operation(left, right)


def part2():
    monkeys = {}
    for line in lines:
        params = line.split(": ")
        if params[0] == "root":
            params[1] = params[1].replace("+", "=")
        m = Monkey(params[0], params[1])
        monkeys[params[0]] = m
    
    monkey = monkeys["root"]
    left = calculate(monkeys, monkey.required_monkeys[0])
    right = calculate(monkeys, monkey.required_monkeys[1])
    if left == None:
        a = calculate_part2(monkeys, monkey.name, right)
    elif right == None:
        a = calculate_part2(monkeys, monkey.name, left)
    print("Part 2:", a)

    monkeys["humn"].value = 3330805295850  # paste the printed humn value here to validate it
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
            print("Part 2 (validation):", monkeys["root"].value)
            return monkeys["root"].value

if __name__ == "__main__":
    # part1()
    part2()