#!/usr/bin/env python
# Written by Yu-Jie Lin

import json
import sys

WORDS_FILE = sys.argv[1]
DATA_FILE = 'bwtf'

def make_conn(data, a, b):

  if a not in data:
    data[a] = [[b],
               [0]]
  if b not in data[a][0]:
    data[a][0].append(b)
    data[a][1].append(0)

  i = data[a][0].index(b)
  data[a][1][i] += 1


def main():

  data = {}

  # number of chars to look back
  n_lb = 2

  with open(WORDS_FILE, 'r') as f:
    for _word in f:
      if _word[0] == '#':
        continue
      word = '^%s$' % _word.rstrip('\n').decode('utf-8')
      for i in range(1, len(word)):
        for i_lb in range(i - n_lb - 1, i):
          w_lb = word[max(0, i_lb):i]
          make_conn(data, w_lb, word[i])

  with open(DATA_FILE + '.json', 'w') as f:
    json.dump(data, f, separators=(',', ':'))

  # cumulative data
  # FIXME this is not deep copy
  data_c = data.copy()
  for a in data_c:
    total = sum(data_c[a][1])
    c = 0
    for i in range(len(data_c[a][0])):
      c += data_c[a][1][i]
      data_c[a][1][i] = c

  with open(DATA_FILE + '.c.json', 'w') as f:
    json.dump(data_c, f, separators=(',', ':'))


if __name__ == '__main__':
  main()
