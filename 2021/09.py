from collections import Counter
from pprint import pprint

cave = [[int(n) for n in line] for line in open('09_input.txt').read().splitlines()]
height, width = len(cave), len(cave[0])

risk_level_sum = 0
for row, line in enumerate(cave):
    for col, cell in enumerate(line):
        neighbors = []
        if row > 0: neighbors.append(cave[row-1][col])
        if row < height - 1: neighbors.append(cave[row+1][col])
        if col > 0: neighbors.append(cave[row][col-1])
        if col < width - 1: neighbors.append(cave[row][col+1])
        if all(int(n) > int(cell) for n in neighbors):
            risk_level_sum += 1 + int(cell)

print('Part 1:', risk_level_sum)

basins = [[None for _ in line] for line in cave]

def find_basin(row, col):
    if cave[row][col] == 9 or basins[row][col] is not None:
        return basins[row][col]
    is_low_point = True
    if row > 0:
        if cave[row-1][col] < cave[row][col]:
            is_low_point = False
            basins[row][col] = find_basin(row-1, col)
    if row < height - 1:
        if cave[row+1][col] < cave[row][col]:
            is_low_point = False
            basins[row][col] = find_basin(row+1, col)
    if col > 0:
        if cave[row][col-1] < cave[row][col]:
            is_low_point = False
            basins[row][col] = find_basin(row, col-1)
    if col < width - 1:
        if cave[row][col+1] < cave[row][col]:
            is_low_point = False
            basins[row][col] = find_basin(row, col+1)
    if is_low_point:
        assert basins[row][col] is None
        basins[row][col] = (row, col)
    assert basins[row][col]
    return basins[row][col]


bc = Counter()
for row, line in enumerate(cave):
    for col, cell in enumerate(line):
        bc[find_basin(row, col)] += 1

del bc[None]
mc = bc.most_common(3)
print('Part 2:', mc[0][1] * mc[1][1] * mc[2][1])
