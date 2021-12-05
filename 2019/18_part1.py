'''
https://adventofcode.com/2019/day/18
'''

from collections import deque
from pprint import pprint
from textwrap import dedent


def part1(input_data):
    _find_next_keys_cache.clear()
    maze, initial_state, all_keys = load_data(input_data)
    pprint((maze, initial_state, all_keys))
    solution_steps = None
    stack = deque([
        (0, initial_state),
    ])
    visited = {}
    i = 0
    while stack:
        i += 1
        if i & 1:
            top_step_count, top_state = stack.pop()
        else:
            top_step_count, top_state = stack.popleft()
        if solution_steps is not None and top_step_count >= solution_steps:
            continue
        if top_state in visited and visited[top_state] <= top_step_count:
            continue
        visited[top_state] = top_step_count
        possible_next_states = find_next_keys(maze, top_state)
        #print(top_step_count, top_state, '->', possible_next_states)
        for next_step_count, next_state in possible_next_states:
            next_step_count += top_step_count
            next_row, next_col, next_keys = next_state
            if len(next_keys) == len(all_keys):
                assert set(next_keys) == set(all_keys)
                if solution_steps is None or solution_steps > next_step_count:
                    solution_steps = next_step_count
                    print('Solution:', solution_steps, 'Stack size:', len(stack), 'i:', i, 'cache size:', len(_find_next_keys_cache))
                    #print('Stack:', stack)
                continue
            if solution_steps is not None and next_step_count >= solution_steps:
                continue
            if next_state in visited and visited[next_state] <= next_step_count:
                continue
            stack.append((next_step_count, next_state))
    return solution_steps


_find_next_keys_cache = {}

def find_next_keys(maze, state):
    if (maze, state) in _find_next_keys_cache:
        return _find_next_keys_cache[(maze, state)]
    row, col, keys = state
    front = [(row, col, 0)]
    visited = {(row, col)}
    next_keys = []
    while front:
        next_front = []
        for row, col, step_count in front:
            neighbours = [
                (row, col + 1),
                (row, col - 1),
                (row + 1, col),
                (row - 1, col),
            ]
            step_count += 1
            for n_row, n_col in neighbours:
                if (n_row, n_col) in visited:
                    continue
                if maze[n_row][n_col] == '#':
                    continue
                visited.add((n_row, n_col))
                if maze[n_row][n_col] == '.' or maze[n_row][n_col].lower() in keys:
                    next_front.append((n_row, n_col, step_count))
                elif maze[n_row][n_col].islower():
                    next_keys.append((step_count, (n_row, n_col, ''.join(sorted(keys + maze[n_row][n_col])))))
                else:
                    assert maze[n_row][n_col].isupper()
                    assert maze[n_row][n_col].lower() not in keys
        front = next_front
    _find_next_keys_cache[(maze, state)] = next_keys
    return next_keys


def load_data(input_data):
    maze = input_data.splitlines()
    assert all(len(line) == len(maze[0]) for line in maze)
    initial_state = None
    all_keys = set()
    for row, line in enumerate(maze):
        for col, cell in enumerate(line):
            if cell == '@':
                assert initial_state is None
                initial_state = (row, col, '')
                maze[row] = maze[row].replace('@', '.')
            elif cell not in '.#' and cell.islower():
                all_keys.add(cell)
    assert initial_state is not None
    return tuple(maze), initial_state, ''.join(sorted(all_keys))


sample_input_1 = dedent('''\
    #########
    #b.A.@.a#
    #########
''')

assert part1(sample_input_1) == 8

sample_input_2 = dedent('''\
    ########################
    #f.D.E.e.C.b.A.@.a.B.c.#
    ######################.#
    #d.....................#
    ########################
''')

assert part1(sample_input_2) == 86

sample_input_3 = dedent('''\
    ########################
    #...............b.C.D.f#
    #.######################
    #.....@.a.B.c.d.A.e.F.g#
    ########################
''')

assert part1(sample_input_3) == 132

sample_input_4 = dedent('''\
    #################
    #i.G..c...e..H.p#
    ########.########
    #j.A..b...f..D.o#
    ########@########
    #k.E..a...g..B.n#
    ########.########
    #l.F..d...h..C.m#
    #################
''')

assert part1(sample_input_4) == 136

sample_input_5 = dedent('''\
    ########################
    #@..............ac.GI.b#
    ###d#e#f################
    ###A#B#C################
    ###g#h#i################
    ########################
''')

assert part1(sample_input_5) == 81

print(part1(open('18_input.txt').read()))
