from collections import Counter
from textwrap import dedent

sample_data = dedent('''\
    00100
    11110
    10110
    10111
    10101
    01111
    00111
    11100
    10000
    11001
    00010
    01010
''')

def part1(data):
    lines = data.splitlines()
    size = len(lines[0])
    assert all(len(line) == size for line in lines)
    gamma = ''.join(most_common(line[i] for line in lines) for i in range(size))
    epsilon = ''.join(least_common(line[i] for line in lines) for i in range(size))
    return int(epsilon, 2) * int(gamma, 2)

def most_common(items):
    c = Counter(items)
    if c['0'] == c['1']:
        return '1'
    return c.most_common(1)[0][0]

def least_common(items):
    c = Counter(items)
    if c['0'] == c['1']:
        return '0'
    return c.most_common()[-1][0]

assert part1(sample_data) == 198

print('Part 1:', part1(open('03_input.txt').read()))

def part2(data):
    lines = data.splitlines()
    size = len(lines[0])
    assert all(len(line) == size for line in lines)
    ox = find_one(lines, most_common)
    co = find_one(lines, least_common)
    return int(ox, 2) * int(co, 2)

def find_one(lines, f, pos=0):
    if len(lines) == 1:
        return lines[0]
    bit = f(line[pos] for line in lines)
    lines = [line for line in lines if line[pos] == bit]
    return find_one(lines, f, pos=pos+1)

assert part2(sample_data) == 230

print('Part 2:', part2(open('03_input.txt').read()))
