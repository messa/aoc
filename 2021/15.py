from collections import defaultdict
from pprint import pprint
import re
from textwrap import dedent
from heapq import heappop, heappush
from collections import deque

def part1(input_data):
    if isinstance(input_data, str):
        cave = [[int(n) for n in line] for line in input_data.splitlines()]
    else:
        cave = input_data
    assert all(len(line) == len(cave[0]) for line in cave)
    width = len(cave[0])
    height = len(cave)

    def adjacent(row, col):
        if row > 0: yield (row-1, col)
        if row < height-1: yield(row+1, col)
        if col > 0: yield (row, col-1)
        if col < width-1: yield (row, col+1)

    minmap = [[None for i in range(width)] for i in range(height)]
    #minmap[0][0] = cave[0][0]
    minmap[0][0] = 0
    stack = deque([(0, 0)])
    while stack:
        row, col = stack.popleft()
        for arow, acol in adjacent(row, col):
            score = minmap[row][col] + cave[arow][acol]
            if minmap[arow][acol] is None or score < minmap[arow][acol]:
                minmap[arow][acol] = score
                stack.append((arow, acol))
    print(minmap[-1][-1])
    return minmap[-1][-1]

def part2(input_data):
    cave = [[int(n) for n in line] for line in input_data.splitlines()]
    assert all(len(line) == len(cave[0]) for line in cave)
    width = len(cave[0])
    height = len(cave)
    bigcave = [
        [
            wrap9(
                cave[row%height][col%width]
            +  col//width + row//height )
            for col in range(5 * width)]
        for row in range(5 * height)
    ]
    print(cave)
    print(bigcave)
    return part1(bigcave)


def wrap9(n):
    while n > 9:
        n -= 9
    return n



sample_input = dedent('''\
    1163751742
    1381373672
    2136511328
    3694931569
    7463417111
    1319128137
    1359912421
    3125421639
    1293138521
    2311944581
''')

assert part1(sample_input) == 40

print('Part 1:', part1(open('15_input.txt').read()))

assert part2(sample_input) == 315

print('Part 2:', part2(open('15_input.txt').read()))

