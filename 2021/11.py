from pprint import pprint
from textwrap import dedent

def part1(input_data, step_count=100, first=False):
    matrix = [[int(c) for c in line] for line in input_data.splitlines()]
    height = len(matrix)
    width = len(matrix[0])
    assert all(len(line) == width for line in matrix)
    #pprint(matrix)

    def adjacent(row, col):
        for row_offset in -1, 0, 1:
            for col_offset in -1, 0, 1:
                if row_offset == 0 and col_offset == 0:
                    continue
                if (row + row_offset) < 0 or col + col_offset < 0:
                    continue
                if (row + row_offset) >= height or col + col_offset >= width:
                    continue
                yield (row + row_offset, col + col_offset)

    flash_count = 0
    for step_number in range(1, step_count+1):
        #print(f'Step {step_number}:')

        for row, line in enumerate(matrix):
            for col, cell in enumerate(line):
                matrix[row][col] += 1

        have_flashed = set()

        while True:
            any_flashed = False
            for row, line in enumerate(matrix):
                for col, cell in enumerate(line):
                    if matrix[row][col] > 9 and (row, col) not in have_flashed:
                        have_flashed.add((row, col))
                        #print('Flashed:', row, col)
                        any_flashed = True
                        for arow, acol in adjacent(row, col):
                            #print('Inc:', arow, acol)
                            matrix[arow][acol] += 1
            if not any_flashed:
                break

        if first and len(have_flashed) == width*height:
            return step_number

        for row, line in enumerate(matrix):
            for col, cell in enumerate(line):
                if matrix[row][col] > 9: # flashed, reset their energy level
                    matrix[row][col] = 0
                    flash_count += 1

        #pprint(matrix)

    return flash_count

sample_input_0 = dedent('''\
    11111
    19991
    19191
    19991
    11111
''')

assert part1(sample_input_0, 2) == 9

sample_input_1 = dedent('''\
    5483143223
    2745854711
    5264556173
    6141336146
    6357385478
    4167524645
    2176841721
    6882881134
    4846848554
    5283751526
''')

assert part1(sample_input_1) == 1656

print('Part 1:', part1(open('11_input.txt').read()))

assert part1(sample_input_1, step_count=999999, first=True) == 195

print('Part 2:', part1(open('11_input.txt').read(), step_count=999999, first=True))
