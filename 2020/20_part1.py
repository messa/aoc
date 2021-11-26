'''
https://adventofcode.com/2020/day/20
'''

from collections import Counter
from functools import reduce
from pprint import pprint
import re

data = open('20_input.txt').read().splitlines()
assert len(data) % 12 == 11

tiles = {}
it = iter(data)
while True:
    ident, = re.match(r'^Tile ([0-9]+):$', next(it)).groups()
    tiles[int(ident)] = [next(it) for i in range(10)]
    try:
        assert next(it) == ''
    except StopIteration:
        break

borders = Counter()

def norm(line):
    return min(line, ''.join(reversed(line)))

for ident, tile in tiles.items():
    flipped = [''.join(x) for x in zip(*tile)]
    borders[norm(tile[0])] += 1
    borders[norm(tile[-1])] += 1
    borders[norm(flipped[0])] += 1
    borders[norm(flipped[-1])] += 1

corners = []

for ident, tile in tiles.items():
    flipped = [''.join(x) for x in zip(*tile)]
    nums = (
        borders[norm(tile[0])],
        borders[norm(tile[-1])],
        borders[norm(flipped[0])],
        borders[norm(flipped[-1])],
    )
    assert all(num <= 2 for num in nums)
    if sum(nums) == 1 + 1 + 2 + 2:
        corners.append(ident)

print('Solution 1:', corners, reduce(lambda a, b: a * b, corners, 1))
