from collections import Counter

'''
After one day, its internal timer would become 2.
After another day, its internal timer would become 1.
After another day, its internal timer would become 0.
After another day, its internal timer would reset to 6, and it would create a new lanternfish with an internal timer of 8.
After another day, the first lanternfish would have an internal timer of 5, and the second lanternfish would have an internal timer of 7.
'''

def part1(input_data):
    nums = list(map(int, input_data.split(',')))
    for i in range(80):
        new_nums = []
        for n in nums:
            new_nums.extend(transition(n))
        nums = new_nums
    return len(nums)

def transition(n):
    if n == 0:
        yield 6
        yield 8
    else:
        yield n - 1

assert part1('3,4,3,1,2') == 5934

print('Part1:', part1(open('06_input.txt').read()))

def part2(input_data):
    nums = Counter(map(int, input_data.split(',')))
    for i in range(256):
        #print(nums)
        new_nums = Counter()
        for n, count in nums.items():
            for nn in transition(n):
                new_nums[nn] += count
        nums = new_nums
    return sum(nums.values())

assert part2('3,4,3,1,2') == 26984457539

print('Part2:', part2(open('06_input.txt').read()))
