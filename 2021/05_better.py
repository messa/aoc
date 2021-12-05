'''
https://adventofcode.com/2021/day/5
'''

from collections import Counter
import re

def linear(a, b):
    return range(a, b+1) if a < b else range(a, b-1, -1)

assert list(linear(1, 1)) == [1]
assert list(linear(1, 3)) == [1, 2, 3]
assert list(linear(3, 1)) == [3, 2, 1]
assert list(linear(-1, -1)) == [-1]
assert list(linear(-1, -3)) == [-1, -2, -3]
assert list(linear(-3, -1)) == [-3, -2, -1]

def part1(input_data):
    over = Counter()
    for line in input_data.splitlines():
        m = re.match(r'^(\d+),(\d+) -> (\d+),(\d+)$', line)
        x1, y1, x2, y2 = map(int, m.groups())

        if x1 == x2:
            for y in linear(y1, y2):
                over[(x1, y)] += 1
        elif y1 == y2:
            for x in linear(x1, x2):
                over[(x, y1)] += 1

    return sum(n >= 2 for n in over.values())

print(part1(open('05_input.txt').read()))

def part2(input_data):
    over = Counter()
    for line in input_data.splitlines():
        m = re.match(r'^(\d+),(\d+) -> (\d+),(\d+)$', line)
        x1, y1, x2, y2 = map(int, m.groups())

        if x1 == x2:
            for y in linear(y1, y2):
                over[(x1, y)] += 1
        elif y1 == y2:
            for x in linear(x1, x2):
                over[(x, y1)] += 1
        elif abs(x1 - x2) == abs(y1 - y2):
            for x, y in zip(linear(x1, x2), linear(y1, y2)):
                over[(x, y)] += 1

    return sum(n >= 2 for n in over.values())

print(part2(open('05_input.txt').read()))
