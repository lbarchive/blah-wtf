#!/usr/bin/env python3
# Written by Yu-Jie Lin

import argparse
import json
import sys


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

  parser = argparse.ArgumentParser(description='Blah, WTF? data generator')
  parser.add_argument('-l', '--limit',
                      default=0,
                      type=int,
                      help='Limit amount of words to process')
  parser.add_argument('-L', '--lookback',
                      default=2,
                      type=int,
                      help='Number of lookback characters')
  parser.add_argument('wordfile',
                      type=argparse.FileType('r'),
                      help='Words file',
                      metavar='WORDSFILE')
  parser.add_argument('outfile',
                      type=argparse.FileType('w'),
                      help='Output JSON file',
                      metavar='OUTFILE')
  args = parser.parse_args()

  data = {}

  words_count = 0
  for _word in args.wordfile:
    if _word[0] == '#':
      continue
    word = '^%s$' % _word.rstrip('\n')
    for i in range(1, len(word)):
      for i_lb in range(i - args.lookback - 1, i):
        w_lb = word[max(0, i_lb):i]
        make_conn(data, w_lb, word[i])
    words_count += 1
    if args.limit and words_count >= args.limit:
      break

  # cumulative data
  # FIXME this is not deep copy
  data_c = data.copy()
  for a in data_c:
    total = sum(data_c[a][1])
    c = 0
    for i in range(len(data_c[a][0])):
      c += data_c[a][1][i]
      data_c[a][1][i] = c

  json.dump(data_c, args.outfile, separators=(',', ':'))

  print(words_count, 'words processed.')

if __name__ == '__main__':
  main()
