import re


def part1(input_data):
    x1, x2, y1, y2 = re.match(r'^target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)$', input_data).groups()
    x1, x2, y1, y2 = int(x1), int(x2), int(y1), int(y2)
    max_y = 0
    for xv in range(-100, 100):
        for yv in range(-100, 100):
            res = fire(xv, yv, x1, x2, y1, y2)
            #print(xv, yv, res)
            if res and res > max_y:
                max_y = res
    return max_y

def fire(xv, yv, x1, x2, y1, y2):
    x, y = 0, 0
    max_y = 0
    step_count = 0
    while True:
        step_count += 1
        if x1 <= x and x <= x2:
            if y1 <= y and y <= y2:
                return max_y
        if step_count == 1000:
            return None
        x += xv
        y += yv
        if xv > 0:
            xv -= 1
        elif xv < 0:
            xv += 1
        yv -= 1
        if y > max_y:
            max_y = y

assert part1('target area: x=20..30, y=-10..-5') == 45

task_input = 'target area: x=192..251, y=-89..-59'

print('Part 1:', part1(task_input))