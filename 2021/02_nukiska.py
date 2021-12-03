input_list = [line.split() for line in open('02_input.txt')]

horizontal_position = 0
depth = 0
aim = 0

for direction in input_list:
    match direction:
        case 'forward', value:
            horizontal_position += int(value)
            depth += int(value) * aim
        case 'down', value:
            aim += int(value)
        case 'up', value:
            aim -= int(value)

print(horizontal_position * depth)
