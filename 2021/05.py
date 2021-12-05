from collections import Counter
import re

data = open('05_input.txt').read().splitlines()

over = Counter()

def rrange(a, b):
    if a < b:
        return range(a, b+1)
    else:
        return range(b, a+1)

for line in data:
    m = re.match(r'^(\d+),(\d+) -> (\d+),(\d+)$' , line)
    x1, y1, x2, y2 = m.groups()
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

    if x1 == x2:
        for i in rrange(y1, y2):
            over[(x1, i)] += 1
    elif y1 == y2:
        for i in rrange(x1, x2):
            over[(i, y1)] += 1

print(over)

p1 = sum(1 for pos, n in over.items() if n >= 2)
print(p1)

# For now, only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2.





