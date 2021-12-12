from collections import defaultdict
from pprint import pprint
from textwrap import dedent

small = lambda cave: cave.islower()

def part1(input_data):
    '''
    How many paths through this cave system are there that visit small caves at most once?
    '''
    edges = defaultdict(list)
    for line in input_data.splitlines():
        a, b = line.split('-')
        print(f'  {a} -> {b}')
        edges[a].append(b)
        edges[b].append(a)
    assert edges['start']
    assert edges['end']
    front = [('start', )]
    all_paths = set()
    while front:
        new_front = []
        for path in front:
            assert isinstance(path, tuple)
            last_node = path[-1]
            for next_node in edges[last_node]:
                print(repr(path), repr(next_node))
                new_path = path + (next_node, )
                if next_node == 'end':
                    all_paths.add(new_path)
                elif small(next_node) and next_node in path:
                    continue
                else:
                    new_front.append(new_path)
        front = new_front
    print(len(all_paths))
    pprint(all_paths)
    return len(all_paths)


sample_input_0 = dedent('''\
    start-A
    start-b
    A-c
    A-b
    b-d
    A-end
    b-end
''')

assert part1(sample_input_0) == 10

sample_input_1 = dedent('''\
    dc-end
    HN-start
    start-kj
    dc-start
    dc-HN
    LN-dc
    HN-end
    kj-sa
    kj-HN
    kj-dc
''')

assert part1(sample_input_1) == 19

sample_input_2 = dedent('''\
    fs-end
    he-DX
    fs-he
    start-DX
    pj-DX
    end-zg
    zg-sl
    zg-pj
    pj-he
    RW-he
    fs-DX
    pj-RW
    zg-RW
    start-pj
    he-WI
    zg-he
    pj-fs
    start-RW
''')

assert part1(sample_input_2) == 226

print('Part 1:', part1(open('12_input.txt').read()))
