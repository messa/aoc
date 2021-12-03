input_list = []
with open('day_02_input.txt', encoding='utf-8') as f:
    for line in f:
        input_list.append(line.split())

horizontal_position = 0
depth = 0
aim = 0

for direction in input_list:
    value = int(direction[1])
    match direction[0]:
        case 'forward':
            horizontal_position += value
            depth += value * aim
        case 'down':
            aim += value
        case 'up':
            aim -= value

print(horizontal_position * depth)

