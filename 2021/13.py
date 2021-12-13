'''
https://adventofcode.com/2021/day/13
'''

from pprint import pprint
import re
from textwrap import dedent

def fold(input_data, first=False):
    dots = set()
    line_it = iter(input_data.splitlines())
    for line in line_it:
        if not line:
            break
        col, row = re.match(r'^(\d+),(\d+)$', line).groups()
        col, row = int(col), int(row)
        dots.add((row, col))
    folds = []
    for line in line_it:
        axis, value = re.match(r'^fold along ([xy])=(\d+)$', line).groups()
        value = int(value)
        folds.append((axis, value))
    for axis, value in folds:
        print('Folding', axis, value)
        if axis == 'x':
            for line, col in set(dots):
                if col > value:
                    dots.add((line, value - col + value))
                    dots.remove((line, col))
        elif axis == 'y':
            for line, col in set(dots):
                if line > value:
                    dots.add((value - line + value, col))
                    dots.remove((line, col))
        #pprint(dots)
        #print(len(dots))
        line_min = min(line for line, col in dots)
        line_max = max(line for line, col in dots)
        col_min = min(col for line, col in dots)
        col_max = max(col for line, col in dots)
        for line in range(line_min, line_max + 1):
            for col in range(col_min, col_max + 1):
                print('#' if (line, col) in dots else '.', end='')
            print()
        if first:
            break
    return len(dots)

sample_data_1 = dedent('''\
    6,10
    0,14
    9,10
    0,3
    10,4
    4,11
    6,0
    6,12
    4,1
    0,13
    10,12
    3,4
    3,0
    8,4
    1,10
    2,14
    8,10
    9,0

    fold along y=7
    fold along x=5
''')

#assert fold(sample_data_1, first=True) == 17

#print('Part 1:', fold(open('13_input.txt').read(), first=True))

fold(open('13_input.txt').read())
