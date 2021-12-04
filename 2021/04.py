
data = open('04_input.txt').read()
lines = data.splitlines()

numbers = [int(n) for n in lines[0].split(',')]
boards = []

lineno = 2
while lineno < len(lines):
    boards.append([
        [int(n) for n in lines[lineno].split()],
        [int(n) for n in lines[lineno+1].split()],
        [int(n) for n in lines[lineno+2].split()],
        [int(n) for n in lines[lineno+3].split()],
        [int(n) for n in lines[lineno+4].split()],
    ])
    lineno += 6

def part1():
    marked = [set() for board in boards]
    for selected in numbers:
        #print('sel:', selected)
        for bn, board in enumerate(boards):
            for row in range(5):
                for col in range(5):
                    if board[row][col] == selected:
                        marked[bn].add((row, col))
                        bingo = all((row, i) in marked[bn] for i in range(5))
                        bingo = bingo or all((i, col) in marked[bn] for i in range(5))
                        if bingo:
                            #print('bingo')
                            score = 0
                            for row in range(5):
                                for col in range(5):
                                    if (row, col) not in marked[bn]:
                                        score += board[row][col]
                            return score * selected

print('Part 1:', part1())

def part2():
    marked = [set() for board in boards]
    winned = set()
    for selected in numbers:
        #print('sel:', selected)
        for bn, board in enumerate(boards):
            for row in range(5):
                for col in range(5):
                    if board[row][col] == selected:
                        marked[bn].add((row, col))
                        bingo = all((row, i) in marked[bn] for i in range(5))
                        bingo = bingo or all((i, col) in marked[bn] for i in range(5))
                        if bingo:
                            winned.add(bn)
                            if len(winned) == len(boards):
                                #print('bingo')
                                score = 0
                                for row in range(5):
                                    for col in range(5):
                                        if (row, col) not in marked[bn]:
                                            score += board[row][col]
                                return score * selected

print('Part 2:', part2())
