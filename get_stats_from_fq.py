import sys
from statistics import mean, median

fq = open(sys.argv[1], 'r')

lengths = []
idx = 1
for line in fq:
	if idx % 4 == 2:
		lengths.append(len(line))
	idx += 1

print('Total bases: ' + str(sum(lengths)))
print('Mean length: ' + str(round(mean(lengths))))
print('Median length: ' + str(median(lengths)))