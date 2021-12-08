from collections import Counter
from pprint import pprint

input_data = [[part.split() for part in line.split('|')] for line in open('08_input.txt')]

total1478 = 0
for in_segments, out_segments in input_data:
    for s in out_segments:
        if len(s) in [2, 3, 4, 7]:
            total1478 += 1

print('Part 1:', total1478)


def get_number(wiring, displays):
    return int(''.join(str(get_digit(wiring, d)) for d in displays))

class InvalidDigitError (Exception):
    pass

def get_digit(wiring, display):
    '''
     0
    1 2
     3
    4 5
     6
    '''
    on = set(wiring.index(segment) for segment in display)
    if on == {0, 2, 5, 6, 4, 1}: return 0
    if on == {2, 5}: return 1
    if on == {0, 2, 3, 4, 6}: return 2
    if on == {0, 2, 3, 5, 6}: return 3
    if on == {1, 3, 2, 5}: return 4
    if on == {0, 1, 3, 5, 6}: return 5
    if on == {0, 1, 4, 6, 5, 3}: return 6
    if on == {0, 2, 5}: return 7
    if on == {0, 1, 2, 3, 4, 5, 6}: return 8
    if on == {0, 1, 2, 3, 5, 6}: return 9
    raise InvalidDigitError('Cannot get digit')

assert get_digit('..b..e.', 'be') == 1

def analyze(displays):
    pprint(displays)
    assert all(set(d) <= set('abcdefg') for d in displays)
    # brute force :)
    from itertools import permutations
    wiring = None
    for p in permutations('abcdefg'):
        p = ''.join(p)
        try:
            for display in displays:
                n = get_digit(p, display)
                print(p, display, n)
        except InvalidDigitError as e:
            print(p, '->', e)
            continue
        assert wiring is None
        wiring = p
    assert wiring
    return wiring


assert get_number(analyze('be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb fdgacbe cefdb cefbgd gcbe'.split()), 'fdgacbe cefdb cefbgd gcbe'.split()) == 8394
assert get_number(analyze('edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec fcgedb cgb dgebacf gc'.split()), 'fcgedb cgb dgebacf gc'.split()) == 9781


total_output = 0
for in_segments, out_segments in input_data:
    wiring = analyze(in_segments + out_segments)
    total_output += get_number(wiring, out_segments)

print('Part 2:', total_output)
