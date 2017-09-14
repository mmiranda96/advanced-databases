import math
import sys
from functools import reduce

def gauss(m, s, x):
    return 1 / (s * math.sqrt(2 * math.pi)) * math.exp(-math.pow(x - m, 2) / (2 * s * s))

# CLI values
if len(sys.argv) != 3:
    print('This script receives the path to an edges table and the number of pages wanted.')
    exit()
path = sys.argv[1]
count = int(sys.argv[2])

# Loading file
with open(path, 'r') as f:
    edges = list(map(lambda x: x.strip('\n').split(','), f.readlines()))[1:]
likes = {}
for e in edges:
    src = e[0]
    if src in likes:
        likes[src] += 1
    else:
        likes[src] = 1

# Statistic data
m = reduce(lambda x, y: x + y, likes.values()) / len(likes)
s = 0
for x in likes.values():
    s += math.pow(x - m, 2)
s = math.sqrt(s / (len(likes) - 1))
p = gauss(m, s, m + 1.5 * s)
print('+===============================================+')
print('| Statistic data                                |')
print('+===============================================+')
print(' Median:\t\t' + str(m))
print(' Standard deviation:\t' + str(s))
print(' Minimum probability:\t' + str(p))
print()

# Finding outliers
outliers = {}
for id, l in likes.items():
    if gauss(m, s, l) <= p:
        outliers[id] = l
print('+===============================================+')
print('| Outliers                                      |')
print('+===============================================+')
for o in outliers.items():
    print(' ' + str(o))
print()

data_without = {}
for e in edges:
    src = e[0]
    dest = e[1]
    if src not in outliers and dest not in outliers:
        if dest in data_without:
            data_without[dest] += 1
        else:
            data_without[dest] = 1

# Results
sorted_data_without = sorted(data_without.items(), key=lambda x: x[1], reverse=True)
print('+===============================================+')
print('| Most influential pages (without outliers)     |')
print('+===============================================+')
for i in range(count):
    print(' ' + str(sorted_data_without[i]))
print()

data_with = {}
for e in edges:
    dest = e[1]
    if dest in data_with:
        data_with[dest] += 1
    else:
        data_with[dest] = 1

# Results
sorted_data_with = sorted(data_with.items(), key=lambda x: x[1], reverse=True)
print('+===============================================+')
print('| Most influential pages (with outliers):       |')
print('+===============================================+')
for i in range(count):
    print(' ' + str(sorted_data_with[i]))
