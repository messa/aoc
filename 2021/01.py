measurements = [int(line) for line in open('01_input.txt')]

increments = 0
for n, value in enumerate(measurements):
    if n > 0:
        if value > measurements[n-1]:
            increments += 1
print('Increments:', increments)

increases = 0
for n in range(len(measurements) - 3):
    if sum(measurements[n+1:n+4]) > sum(measurements[n:n+3]):
        increases += 1
print('Sliding window increases:', increases)
