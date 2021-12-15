from collections import Counter
import re
from textwrap import dedent

def part1(input_data, step_count=10):
    template, blank, *rule_lines = input_data.splitlines()
    assert template
    assert not blank
    rules = {}
    for line in rule_lines:
        a, b, c = re.match(r'^([A-Z])([A-Z]) -> ([A-Z])$', line).groups()
        assert (a, b) not in rules
        rules[(a, b)] = c
    poly = template
    for step_number in range(step_count):
        print(step_number, poly)
        new_poly = []
        for a, b in zip(poly, poly[1:]):
            new_poly.append(a)
            new_poly.append(rules[(a, b)])
        new_poly.append(poly[-1])
        poly = ''.join(new_poly)
    print(poly)
    c = Counter(poly)
    mc = c.most_common()
    return c[mc[0][0]] - c[mc[-1][0]]

def part2(input_data, step_count=40):
    template, blank, *rule_lines = input_data.splitlines()
    assert template
    assert not blank
    rules = {}
    for line in rule_lines:
        a, b, c = re.match(r'^([A-Z])([A-Z]) -> ([A-Z])$', line).groups()
        assert (a, b) not in rules
        rules[(a, b)] = c

    pairs = Counter()
    print(template)
    for a, b in zip(template, template[1:]):
        pairs[(a, b)] += 1
    for step_number in range(step_count):
        print(pairs)
        new_pairs = Counter()
        for (a, b), count in pairs.items():
            middle = rules[(a, b)]
            new_pairs[(a, middle)] += count
            new_pairs[(middle, b)] += count
        pairs = new_pairs

    letter_counter = Counter()
    for (a, b), count in pairs.items():
        letter_counter[a] += count
        letter_counter[b] += count
    letter_counter[template[0]] += 1
    letter_counter[template[-1]] += 1
    mc = letter_counter.most_common()
    print(letter_counter[mc[0][0]] / 2 - letter_counter[mc[-1][0]] / 2)
    return int(letter_counter[mc[0][0]] / 2 - letter_counter[mc[-1][0]] / 2)


sample_input = dedent('''\
    NNCB

    CH -> B
    HH -> N
    CB -> H
    NH -> C
    HB -> C
    HC -> B
    HN -> C
    NN -> C
    BH -> H
    NC -> B
    NB -> B
    BN -> B
    BB -> N
    BC -> B
    CC -> N
    CN -> C
''')

assert part1(sample_input) == 1588

print('Part 1:', part1(open('14_input.txt').read()))

assert part2(sample_input, 10) == 1588
assert part2(sample_input) == 2188189693529

print('Part 2:', part2(open('14_input.txt').read()))
