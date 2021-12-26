'''
https://adventofcode.com/2021/day/25
'''

from copy import deepcopy
from textwrap import dedent

def part1(input_data):
    state = [list(line) for line in input_data.splitlines()]
    step_count = 1
    while True:
        new_state = transition(state)
        if new_state == state:
            break
        state = new_state
        step_count += 1
    return step_count


def transition(state):
    state = deepcopy(state)
    # east >
    will_move = []
    for lineno, line in enumerate(state):
        for colno, cell in enumerate(line):
            if cell == '>' and get_right(state, lineno, colno) == '.':
                will_move.append((lineno, colno))
    for lineno, colno in will_move:
        set_right(state, lineno, colno, state[lineno][colno])
        state[lineno][colno] = '.'
    # south v
    will_move = []
    for lineno, line in enumerate(state):
        for colno, cell in enumerate(line):
            if cell == 'v' and get_bottom(state, lineno, colno) == '.':
                will_move.append((lineno, colno))
    for lineno, colno in will_move:
        set_bottom(state, lineno, colno, state[lineno][colno])
        state[lineno][colno] = '.'
    return state


def get_right(state, lineno, colno):
    colno = (colno + 1) % len(state[lineno])
    return state[lineno][colno]


def set_right(state, lineno, colno, new_value):
    colno = (colno + 1) % len(state[lineno])
    state[lineno][colno] = new_value


def get_bottom(state, lineno, colno):
    lineno = (lineno + 1) % len(state)
    return state[lineno][colno]


def set_bottom(state, lineno, colno, new_value):
    lineno = (lineno + 1) % len(state)
    state[lineno][colno] = new_value


sample_input_1 = dedent('''\
    v...>>.vv>
    .vv>>.vv..
    >>.>v>...v
    >>v>>.>.v.
    v>v.vv.v..
    >.>>..v...
    .vv..>.>v.
    v.v..>>v.v
    ....v..v.>
''')

assert part1(sample_input_1) == 58

print('Part 1:', part1(open('25_input.txt').read()))

