from functools import partial
import re
from pprint import pprint
from textwrap import dedent
from multiprocessing import Pool


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


def apply_orientation(v, o):
    return (
        o[0][0] * v[0] + o[0][1] * v[1] + o[0][2] * v[2],
        o[1][0] * v[0] + o[1][1] * v[1] + o[1][2] * v[2],
        o[2][0] * v[0] + o[2][1] * v[1] + o[2][2] * v[2],
    )


def compute(input_data, pool):
    input_data = parse_scanner_results(input_data)
    known_beacons = [input_data[0]]
    remaining_scanners = set(scanner_no for scanner_no in input_data.keys() if scanner_no != 0)
    scanner_positions = [(0, 0, 0)]

    while remaining_scanners:
        print('remaining_scanners:', remaining_scanners)
        for scanner_no in list(remaining_scanners):
            print('Scanner:', scanner_no)
            assert scanner_no != 0

            matching_orientations = pool.map(partial(match_orientation, known_beacons, input_data, scanner_no), orientations, 1)
            matching_orientations = [mo for mo in matching_orientations if mo]
            if matching_orientations:
                (matched_orientation, dx, dy, dz), = matching_orientations
                known_beacons.append([add_offset(apply_orientation(b, matched_orientation), dx, dy, dz) for b in input_data[scanner_no]])
                remaining_scanners.discard(scanner_no)
                scanner_positions.append((dx, dy, dz))

    all_known_beacons = set()
    for kb_subset in known_beacons:
        for kb in kb_subset:
            all_known_beacons.add(kb)

    manhattan_distances = []
    for sp1 in scanner_positions:
        for sp2 in scanner_positions:
            manhattan_distances.append(
                abs(sp1[0] - sp2[0]) + abs(sp1[1] - sp2[1]) + abs(sp1[2] - sp2[2]))

    return len(all_known_beacons), max(manhattan_distances)


def match_orientation(known_beacons, input_data, scanner_no, possible_orientation):
    beacons = [apply_orientation(b, possible_orientation) for b in input_data[scanner_no]]
    for kb_subset in known_beacons:
        res = match_beacons(kb_subset, beacons)
        if res:
            dx, dy, dz = res
            print('orientation:', possible_orientation, 'offset:', res)
            return (possible_orientation, dx, dy, dz)


def match_beacons(known_beacons, beacons):
    #print(known_beacons)
    #print(beacons)
    for kb in known_beacons:
        for b in beacons:
            dx = kb[0] - b[0]
            dy = kb[1] - b[1]
            dz = kb[2] - b[2]
            assert add_offset(b, dx, dy, dz) == kb
            #print('fmb:',dx, dy, dz, find_matching_beacons(known_beacons, beacons, dx, dy, dz))
            #assert find_matching_beacons(known_beacons, beacons, dx, dy, dz) >= 1
            if find_matching_beacons(known_beacons, beacons, dx, dy, dz) >= 12:
                print('fmb:',dx, dy, dz, find_matching_beacons(known_beacons, beacons, dx, dy, dz))
                return (dx, dy, dz)


def add_offset(v, dx, dy, dz):
    return (v[0] + dx, v[1] + dy, v[2] + dz)


def find_matching_beacons(known_beacons, beacons, dx, dy, dz, kbi=0, bi=0, have=0):
    num = 0
    for kb in known_beacons:
        for b in beacons:
            if kb == add_offset(b, dx, dy, dz):
                num += 1
    return num


def parse_scanner_results(input_data):
    assert isinstance(input_data, str)
    current_scanner_number = None
    results = {}
    for line in input_data.splitlines():
        if not line.strip():
            continue
        m = re.match(r'^--- scanner ([0-9]+) ---$', line)
        if m:
            current_scanner_number = int(m.group(1))
            assert current_scanner_number not in results
            results[current_scanner_number] = []
            continue
        try:
            a, b, c = line.split(',')
            a, b, c = int(a), int(b), int(c)
            results[current_scanner_number].append((a, b, c))
        except ValueError as e:
            pprint(line)
            raise e
    return results


sample_input_1 = dedent('''\
    --- scanner 0 ---
    404,-588,-901
    528,-643,409
    -838,591,734
    390,-675,-793
    -537,-823,-458
    -485,-357,347
    -345,-311,381
    -661,-816,-575
    -876,649,763
    -618,-824,-621
    553,345,-567
    474,580,667
    -447,-329,318
    -584,868,-557
    544,-627,-890
    564,392,-477
    455,729,728
    -892,524,684
    -689,845,-530
    423,-701,434
    7,-33,-71
    630,319,-379
    443,580,662
    -789,900,-551
    459,-707,401

    --- scanner 1 ---
    686,422,578
    605,423,415
    515,917,-361
    -336,658,858
    95,138,22
    -476,619,847
    -340,-569,-846
    567,-361,727
    -460,603,-452
    669,-402,600
    729,430,532
    -500,-761,534
    -322,571,750
    -466,-666,-811
    -429,-592,574
    -355,545,-477
    703,-491,-529
    -328,-685,520
    413,935,-424
    -391,539,-444
    586,-435,557
    -364,-763,-893
    807,-499,-711
    755,-354,-619
    553,889,-390

    --- scanner 2 ---
    649,640,665
    682,-795,504
    -784,533,-524
    -644,584,-595
    -588,-843,648
    -30,6,44
    -674,560,763
    500,723,-460
    609,671,-379
    -555,-800,653
    -675,-892,-343
    697,-426,-610
    578,704,681
    493,664,-388
    -671,-858,530
    -667,343,800
    571,-461,-707
    -138,-166,112
    -889,563,-600
    646,-828,498
    640,759,510
    -630,509,768
    -681,-892,-333
    673,-379,-804
    -742,-814,-386
    577,-820,562

    --- scanner 3 ---
    -589,542,597
    605,-692,669
    -500,565,-823
    -660,373,557
    -458,-679,-417
    -488,449,543
    -626,468,-788
    338,-750,-386
    528,-832,-391
    562,-778,733
    -938,-730,414
    543,643,-506
    -524,371,-870
    407,773,750
    -104,29,83
    378,-903,-323
    -778,-728,485
    426,699,580
    -438,-605,-362
    -469,-447,-387
    509,732,623
    647,635,-688
    -868,-804,481
    614,-800,639
    595,780,-596

    --- scanner 4 ---
    727,592,562
    -293,-554,779
    441,611,-461
    -714,465,-776
    -743,427,-804
    -660,-479,-426
    832,-632,460
    927,-485,-438
    408,393,-506
    466,436,-512
    110,16,151
    -258,-428,682
    -393,719,612
    -211,-452,876
    808,-476,-593
    -575,615,604
    -485,667,467
    -680,325,-822
    -627,-443,-432
    872,-547,-609
    833,512,582
    807,604,487
    839,-516,451
    891,-625,532
    -652,-548,-490
    30,-46,-14
''')

def main():
    with Pool() as pool:
        assert compute(sample_input_1, pool=pool) == (79, 3621)

        part1_res, part2_res = compute(open('19_input.txt').read(), pool=pool)
        print('Part 1:', part1_res)
        print('Part 2:', part2_res)


if __name__ == '__main__':
    main()
