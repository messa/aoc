from collections import Counter
from pprint import pprint
import re

input_data = open('10_input.txt').read().splitlines()

'''
If a chunk opens with (, it must close with ).
If a chunk opens with [, it must close with ].
If a chunk opens with {, it must close with }.
If a chunk opens with <, it must close with >.
'''

'''
A corrupted line is one where a chunk closes with the wrong character - that is, where the characters it opens and closes with do not form one of the four legal pairs listed above.
'''

def validate(chunks):
    stack = []
    for c in chunks:
        if c in '[({<':
            stack.append(c)
        elif c == ']':
            x = stack.pop()
            if x != '[':
                return 'bad', c
        elif c == '>':
            x = stack.pop()
            if x != '<':
                return 'bad', c
        elif c == '}':
            x = stack.pop()
            if x != '{':
                return 'bad', c
        elif c == ')':
            x = stack.pop()
            if x != '(':
                return 'bad', c
        else:
            assert 0, repr(c)
    if stack != []:
        return 'incomplete', ''.join(stack)
    return 'ok',

assert validate('([])') == ('ok',)
assert validate('{()()()}') == ('ok',)
assert validate('<([{}])>') == ('ok',)
assert validate('[<>({}){}[([])<>]]') == ('ok',)
assert validate('(((((((((())))))))))') == ('ok',)

assert validate('(]') != True
assert validate('{()()()>') != True
assert validate('(((()))}') != True
assert validate('<([]){()}[{}])') != True


points = 0
for line in input_data:
    res = validate(line)
    if res != True:
        if res == ('bad', ')'): points += 3
        if res == ('bad', ']'): points += 57
        if res == ('bad', '}'): points += 1197
        if res == ('bad', '>'): points += 25137

print('Part 1:', points)


scores = []
for line in input_data:
    res = validate(line)
    score = 0
    if res[0] == 'incomplete':
        for c in reversed(res[1]):
            if c == '(': score = score * 5 + 1
            if c == '[': score = score * 5 + 2
            if c == '{': score = score * 5 + 3
            if c == '<': score = score * 5 + 4
    if score:
        scores.append(score)

scores.sort()
middle = scores[(len(scores)-1) // 2]
assert sum(m < middle for m in scores) == sum(m > middle for m in scores)
print('Part 2:', middle)











