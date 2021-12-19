'''
https://adventofcode.com/2021/day/18
'''

import json


def part1(input_data):
    for line in input_data.splitlines():
        n = json.loads(line)
        print(line, n)


def add(x, y):
    return reduce_sn([x, y])


def reduce_sn(num):
    while True:
        num2 = explode(num)
        if num2 == num:
            num2 = split(num)
            if num2 == num:
                return num


def explode(num):
    '''
    If any pair is nested inside four pairs, the leftmost such pair explodes.
    To explode a pair, the pair's left value is added to the first regular number to the left of the exploding pair (if any),
    and the pair's right value is added to the first regular number to the right of the exploding pair (if any).
    Exploding pairs will always consist of two regular numbers. Then, the entire exploding pair is replaced with the regular number 0.
    '''

assert explode([[[[[9,8],1],2],3],4]) == [[[[0,9],2],3],4])
assert explode([7,[6,[5,[4,[3,2]]]]]) == [7,[6,[5,[7,0]]]]
assert explode([[6,[5,[4,[3,2]]]],1]) == [[6,[5,[7,0]]],3]


assert add([[[[4,3],4],4],[7,[[8,4],9]]], [1,1]) == [[[[0,7],4],[[7,8],[6,0]]],[8,1]]

assert add([[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]], [[[[4,2],2],6],[8,7]]) == [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]

assert magnitude([[1,2],[[3,4],5]]) == 143
assert magnitude([[[[0,7],4],[[7,8],[6,0]]],[8,1]]) == 1384

print('Part 1:', part1(open('18_input.txt').read()))

