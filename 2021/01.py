measurements = [int(line) for line in open('01_input.txt')]
increments = 0
for n, value in enumerate(measurements):
    if n > 0:
        if value > measurements[n-1]:
            increments += 1
print('Increments:', increments)

increases = 0
for n in range(len(measurements) + 1):
    if n >= 4:
        if sum(measurements[n-3:n]) > sum(measurements[n-4:n-1]):
            increases += 1

print('Sliding window increases:', increases)
