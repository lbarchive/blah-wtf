#!/usr/bin/env python
# Written by Yu-Jie Lin

import json
import random

def load_data():

  with open('../data/bwtf.c.json', 'r') as f:
    data = json.load(f)
  return data


def get_next_ch(data, a):

  while a not in data:
    a = a[1:]

  k = data[a][0]
  v = data[a][1]
  r = random.randint(0, v[-1] - 1)
  for i in range(len(k)):
    if r < v[i]:
      return k[i]


def gen_word(data, n_lb=2):

  word = ''
  ch = '^'
  while ch != '$':
    next_ch = get_next_ch(data, ch)
    if next_ch not in ('^', '$'):
      word += next_ch
    if next_ch == '$':
      return word
    ch = word[-n_lb:]


def main():

  data = load_data()

  words = [gen_word(data)
           for i in range(abs(int(random.gauss(25, 5))))]
  words[0] = words[0].capitalize()
  print ' '.join(words) + '.'

if __name__ == '__main__':
  main()
