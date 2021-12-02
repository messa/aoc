'''
https://adventofcode.com/2021/day/2
'''

import re

lines = open('02_input.txt').read().splitlines()

horizontal, depth = 0, 0

for line in lines:
    m = re.match(r'^([a-z]+) (\d+)$', line)
    direction, amount = m.groups()
    amount = int(amount)
    if direction == 'forward':
        horizontal += amount
    elif direction == 'down':
        depth += amount
    elif direction == 'up':
        depth -= amount
    else:
        raise Exception(f'Unknown diirection: {direction}')

print(horizontal * depth)

horizontal, depth, aim = 0, 0, 0

for line in lines:
    m = re.match(r'^([a-z]+) (\d+)$', line)
    direction, amount = m.groups()
    amount = int(amount)
    if direction == 'forward':
        horizontal += amount
        depth += aim * amount
    elif direction == 'down':
        aim += amount
    elif direction == 'up':
        aim -= amount
    else:
        raise Exception(f'Unknown diirection: {direction}')

print(horizontal * depth)
