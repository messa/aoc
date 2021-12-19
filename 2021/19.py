from collections import defaultdict, Counter
import re
from pprint import pprint


norm = ((1, 0, 0), (0, 1, 0), (0, 0, 1))


def right(vectors):
    return tuple((-v[1], v[0], v[2]) for v in vectors)


def up(vectors):
    return tuple((v[2], v[1], -v[0]) for v in vectors)


def rot(vectors):
    return tuple((v[0], v[2], -v[1]) for v in vectors)

basic_orientations = [
    norm,
    right(norm),
    right(right(norm)),
    right(right(right(norm))),
    up(norm),
    up(up(up(norm))),
]

orientations = []
for o in basic_orientations:
    orientations.append(o)
    orientations.append(rot(o))
    orientations.append(rot(rot(o)))
    orientations.append(rot(rot(rot(o))))


assert len(orientations) == len(set(orientations))

pprint(orientations)

assert len(orientations) == 24




def part1(input_data):
    input_data = parse_scanner_results(input_data)
    known_beacons = None
    for scanner_no in range(len(input_data)):
        if known_beacons is None:
            assert scanner_no == 0
            known_beacons = set(input_data[scanner_no])
            continue
        #for possible_orientation


        #input_data[scanner_no]:


def parse_scanner_results(input_data):
    current_scanner_number = None
    results = {}
    for line in input_data:
        if not line.strip():
            continue
        m = re.match(r'^--- scanner ([0-9]+) ---$', line)
        if m:
            current_scanner_number = int(m.group(1))
            assert current_scanner_number not in results
            results[current_scanner_number] = []
            continue
        a, b, c = line.split(',')
        a, b, c = int(a), int(b), int(c)
        results[current_scanner_number].append((a, b, c))
    return results



print('Part 1:', part1(open('19_input.txt')))


def part2(input_data):
    pass


print('Part 2:', part2(open('19_input.txt')))


