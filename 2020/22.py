from pprint import pprint
import re

raw_input = open('22_input.txt').read()

m = re.match(r'^Player 1:\s([\d\s]+)Player 2:\s([\d\s]+)$', raw_input, re.MULTILINE)

p1 = [int(n) for n in m.group(1).split()]
p2 = [int(n) for n in m.group(2).split()]

print('p1:', p1)
print('p2:', p2)

while p1 and p2:
    top1, *p1 = p1
    top2, *p2 = p2
    if top1 > top2:
        p1.append(top1)
        p1.append(top2)
    elif top2 > top1:
        p2.append(top2)
        p2.append(top1)
    else:
        raise Exception('should not happen')
    print('p1:', p1)
    print('p2:', p2)

score = sum(pos * value for pos, value in enumerate(reversed(p1 or p2), start=1))
print('score:', score)
