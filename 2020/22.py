from pprint import pprint
import re

raw_input = open('22_input.txt').read()

m = re.match(r'^Player 1:\s([\d\s]+)Player 2:\s([\d\s]+)$', raw_input, re.MULTILINE)

initial_p1 = tuple(int(n) for n in m.group(1).split())
initial_p2 = tuple(int(n) for n in m.group(2).split())

p1 = initial_p1
p2 = initial_p2

#print('p1:', p1)
#print('p2:', p2)

while p1 and p2:
    top1, *p1 = p1
    top2, *p2 = p2
    if top1 > top2:
        p1 = [*p1, top1, top2]
    elif top2 > top1:
        p2 = [*p2, top2, top1]
    else:
        raise Exception('should not happen')
    #print('p1:', p1)
    #print('p2:', p2)

score = sum(pos * value for pos, value in enumerate(reversed(p1 or p2), start=1))
print('Part 1 score:', score)


def recursive_combat(p1, p2, level=0, history=()):
    history = set()
    while True:
        print()
        print('p1:', p1)
        print('p2:', p2)
        round_winner = None
        if (tuple(p1), tuple(p2)) in history:
            return 'p1'
        history.add((tuple(p1), tuple(p2)))
        top1, *p1 = p1
        top2, *p2 = p2

        if not p1:
            p2 = [*p2, top2, top1]
            score = sum(pos * value for pos, value in enumerate(reversed(p2), start=1))
            print('Part 2 score:', score)
            return 'p2'
        if not p2:
            p1 = [*p1, top1, top2]
            score = sum(pos * value for pos, value in enumerate(reversed(p1), start=1))
            print('Part 2 score:', score)
            return 'p1'


        if len(p1) >= top1 and len(p2) >= top2:
            round_winner = recursive_combat(p1[:top1], p2[:top2], level=level+1, history=history)
        else:
            if top1 > top2:
                # player 1 wins round
                round_winner = 'p1'
            else:
                # player 2 wins round
                round_winner = 'p2'

        if round_winner == 'p1':
            p1 = [*p1, top1, top2]
        elif round_winner == 'p2':
            p2 = [*p2, top2, top1]
        else:
            raise Exception('Invalid round_winner')

assert recursive_combat([9, 2, 6, 3, 1], [5, 8, 4, 7, 10])

print(recursive_combat(initial_p1, initial_p2))
