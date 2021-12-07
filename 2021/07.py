
def part1(input_data):
    numbers = [int(num) for num in input_data.strip().split(',')]

    def score(align_pos):
        # print(
        #     align_pos,
        #     [abs(num - align_pos) for num in numbers],
        #     sum(abs(num - align_pos) for num in numbers)
        # )
        return sum(abs(num - align_pos) for num in numbers)

    return min(score(align_pos) for align_pos in range(min(numbers), max(numbers)+1))

assert part1('16,1,2,0,4,2,7,1,2,14') == 37

print('Part 1:', part1(open('07_input.txt').read()))

def incremental_cost(n):
    return int((1 + n) * (n / 2))

def part2(input_data):
    numbers = [int(num) for num in input_data.strip().split(',')]

    def score(align_pos):
        # print(
        #     align_pos,
        #     [incremental_cost(abs(num - align_pos)) for num in numbers],
        #     sum(incremental_cost(abs(num - align_pos)) for num in numbers)
        # )
        return sum(incremental_cost(abs(num - align_pos)) for num in numbers)

    return min(score(align_pos) for align_pos in range(min(numbers), max(numbers)+1))

assert part2('16,1,2,0,4,2,7,1,2,14') == 168

print('Part 2:', part2(open('07_input.txt').read()))
