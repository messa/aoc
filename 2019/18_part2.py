'''
https://adventofcode.com/2019/day/18
'''

from collections import deque
from pprint import pprint
from textwrap import dedent


def part2(input_data):
    _find_next_keys_cache.clear()
    maze, initial_multistate, all_keys = load_data(input_data)
    pprint((maze, initial_multistate, all_keys))
    solution_steps = None
    stack = deque([
        (0, initial_multistate),
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
        possible_next_multistates = find_next_keys_4(maze, top_state)
        #print(top_step_count, top_state, '->', possible_next_states)
        for next_step_count, next_multistate in possible_next_multistates:
            next_step_count += top_step_count
            next_positions, next_keys = next_multistate
            if len(next_keys) == len(all_keys):
                assert set(next_keys) == set(all_keys)
                if solution_steps is None or solution_steps > next_step_count:
                    solution_steps = next_step_count
                    print('Solution:', solution_steps, 'Stack size:', len(stack), 'i:', i, 'cache size:', len(_find_next_keys_cache))
                    #print('Stack:', stack)
                continue
            if solution_steps is not None and next_step_count >= solution_steps:
                continue
            if next_multistate in visited and visited[next_multistate] <= next_step_count:
                continue
            stack.append((next_step_count, next_multistate))
    return solution_steps


def find_next_keys_4(maze, multistate):
    possibilities = []
    positions, keys = multistate
    assert len(positions) == 4
    for i, (row, col) in enumerate(positions):
        for next_step_count, (next_row, next_col, next_keys) in find_next_keys(maze, (row, col, keys)):
            next_positions = list(positions)
            next_positions[i] = (next_row, next_col)
            possibilities.append((next_step_count, (tuple(next_positions), next_keys)))
    return possibilities


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
    initial_positions = []
    all_keys = set()
    for row, line in enumerate(maze):
        for col, cell in enumerate(line):
            if cell == '@':
                initial_positions.append((row, col))
                maze[row] = maze[row].replace('@', '.')
            elif cell not in '.#' and cell.islower():
                all_keys.add(cell)
    assert len(initial_positions) == 4
    initial_multistate = tuple(initial_positions), ''
    return tuple(maze), initial_multistate, ''.join(sorted(all_keys))


sample_input_1 = dedent('''\
    #######
    #a.#Cd#
    ##@#@##
    #######
    ##@#@##
    #cB#Ab#
    #######
''')

assert part2(sample_input_1) == 8

sample_input_2 = dedent('''\
    ###############
    #d.ABC.#.....a#
    ######@#@######
    ###############
    ######@#@######
    #b.....#.....c#
    ###############
''')

assert part2(sample_input_2) == 24

sample_input_3 = dedent('''\
    #############
    #DcBa.#.GhKl#
    #.###@#@#I###
    #e#d#####j#k#
    ###C#@#@###J#
    #fEbA.#.FgHi#
    #############
''')

assert part2(sample_input_3) == 32

sample_input_4 = dedent('''\
    #############
    #g#f.D#..h#l#
    #F###e#E###.#
    #dCba@#@BcIJ#
    #############
    #nK.L@#@G...#
    #M###N#H###.#
    #o#m..#i#jk.#
    #############
''')

assert part2(sample_input_4) == 72

def fix_map_for_part2(maze):
    maze = [list(line) for line in maze.splitlines()]
    initial_position = None
    for row, line in enumerate(maze):
        for col, cell in enumerate(line):
            if cell == '@':
                assert initial_position is None
                initial_position = (row, col)
    assert initial_position
    row, col = initial_position

    assert maze[row-1][col-1] == '.'
    assert maze[row][col-1] == '.'
    assert maze[row+1][col-1] == '.'
    assert maze[row-1][col] == '.'
    assert maze[row][col] == '@'
    assert maze[row+1][col] == '.'
    assert maze[row-1][col+1] == '.'
    assert maze[row][col+1] == '.'
    assert maze[row+1][col+1] == '.'

    maze[row-1][col-1] = '@'
    maze[row][col-1] = '#'
    maze[row+1][col-1] = '@'
    maze[row-1][col] = '#'
    maze[row][col] = '#'
    maze[row+1][col] = '#'
    maze[row-1][col+1] = '@'
    maze[row][col+1] = '#'
    maze[row+1][col+1] = '@'

    maze = '\n'.join(''.join(line) for line in maze)
    return maze

print(part2(fix_map_for_part2(open('18_input.txt').read())))
