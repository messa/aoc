'''
https://adventofcode.com/2021/day/24
'''

from random import randint


def part1(input_data):
    instructions = [line.split() for line in input_data.splitlines()]
    model_number = '9' * 14
    #model_number = str(int(model_number) - 7870897540 - 7870769674 - 7870806751)
    while True:
        print(model_number)
        if execute(instructions, model_number):
            break
        while True:
            model_number = str(int(model_number) - randint(1, 10000000))
            if '0' in model_number:
                continue
            break
    return model_number


def execute(instructions, model_number):
    assert len(model_number) == 14
    assert '0' not in model_number
    orig_model_number = model_number
    variables = {
        'w': 0,
        'x': 0,
        'y': 0,
        'z': 0,
    }
    for line in instructions:
        #print(line)
        match line:
            case 'inp', a:
                assert a in variables
                variables[a] = int(model_number[0])
                model_number = model_number[1:]
            case 'add', a, b:
                assert a in variables
                variables[a] += int(b) if isnum(b) else variables[b]
            case 'mul', a, b:
                assert a in variables
                variables[a] *= int(b) if isnum(b) else variables[b]
            case 'div', a, b:
                assert a in variables
                variables[a] = int(variables[a] / (int(b) if isnum(b) else variables[b] ))
            case 'mod', a, b:
                assert a in variables
                variables[a] = int(variables[a] % (int(b) if isnum(b) else variables[b] ))
            case 'eql', a, b:
                assert a in variables
                if variables[a] == (int(b) if isnum(b) else variables[b]):
                    variables[a] = 1
                else:
                    variables[a] = 0
            case _:
                assert 0, line
    assert model_number == ''
    print(orig_model_number, variables)
    return variables['z'] == 0


def isnum(s):
    return s[0] == '-' or s.isdigit()


print('Part 1:', part1(open('24_input.txt').read()))
