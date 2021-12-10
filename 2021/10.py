'''
https://adventofcode.com/2021/day/10
'''

input_data = open('10_input.txt').read().splitlines()

def validate(chunks):
    stack = []
    for c in chunks:
        if c in '[({<':
            stack.append(c)
        elif c in '])}>':
            if '[({<'.index(stack.pop()) != '])}>'.index(c):
                return 'bad', c
        else:
            raise Exception(f"Unknown character: {c!r}")
    if stack != []:
        return 'incomplete', ''.join(stack)
    return 'ok',

assert validate('([])') == ('ok',)
assert validate('{()()()}') == ('ok',)
assert validate('<([{}])>') == ('ok',)
assert validate('[<>({}){}[([])<>]]') == ('ok',)
assert validate('(((((((((())))))))))') == ('ok',)

assert validate('(]') == ('bad', ']')
assert validate('{()()()>') == ('bad', '>')
assert validate('(((()))}') == ('bad', '}')
assert validate('<([]){()}[{}])') == ('bad', ')')

points = 0
for line in input_data:
    res = validate(line)
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
middle = scores[len(scores) // 2]
assert sum(m < middle for m in scores) == sum(m > middle for m in scores)

print('Part 2:', middle)
