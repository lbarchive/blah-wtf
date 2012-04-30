#!/usr/bin/env python3

import argparse
import json
import random
import sys


# Default number of lookback characters
LOOKBACK = 2


class Blaher():

  def __init__(self):

    self.idiotize()

  def idiotize(self):

    self._brain = {}
    self._raw_brain = {}
    self._think_again = False

  def brainwash(self, raw_imprint=None, imprint=None):

    if raw_imprint:
      raw_brain = {}
      for key, data in raw_imprint.items():
        raw_brain[key] = [data[0][:], data[1][:]]
      self._raw_brain = raw_brain

    if imprint:
      brain = {}
      for key, data in imprint.items():
        if len(data) == 1:
          brain[key] = data
        else:
          brain[key] = [data[0][:], data[1][:]]
      self._brain = brain

    self._think_again = False

  def clone_brain(self, clone_raw_brain=True, clone_brain=True):

    if self._think_again and clone_brain:
      self.think()

    raw_brain = self._raw_brain if clone_raw_brain else None
    brain     = self._brain     if clone_brain     else None

    self.brainwash(raw_brain, brain)
    return raw_brain, brain

  def _read(self, a, b):

    raw_brain = self._raw_brain
    if a not in raw_brain:
      raw_brain[a] = [b, [0]]
    if b not in raw_brain[a][0]:
      raw_brain[a][0] += b
      raw_brain[a][1].append(0)

    i = raw_brain[a][0].index(b)
    raw_brain[a][1][i] += 1

  def read(self, word, lookback=2):

    word = '^%s$' % word
    for i in range(1, len(word)):
      for i_lb in range(i - lookback - 1, i):
        w_lb = word[max(0, i_lb):i]
        self._read(w_lb, word[i])

    self._think_again = True

  def think(self):

    brain, _ = self.clone_brain(clone_brain=False)
    for pat, d in brain.items():
      if len(d[0]) == 1:
        brain[pat] = d[0]
        continue
      c = 0
      for i in range(len(d[0])):
        c += d[1][i]
        d[1][i] = c

    self.brainwash(imprint=brain)
    self._think_again = False

  def blah_char(self, a):

    if self._think_again:
      self.think()

    brain = self._brain
    while a not in brain:
      a = a[1:]

    if len(brain[a]) == 1:
      return brain[a]

    k = brain[a][0]
    v = brain[a][1]
    r = random.randint(0, v[-1] - 1)
    for i in range(len(k)):
      if r < v[i]:
        return k[i]

  def blah_word(self, n_lb=LOOKBACK):

    brain = self._brain
    word = ''
    ch = '^'
    while ch != '$':
      next_ch = self.blah_char(ch)
      if next_ch not in ('^', '$'):
        word += next_ch
      if next_ch == '$':
        return word
      ch = word[-n_lb:]

  def blah(self, n_lb=LOOKBACK):

    words = [self.blah_word(n_lb)
             for i in range(abs(int(random.gauss(25, 5))))]
    words[0] = words[0].capitalize()
    return ' '.join(words) + '.'
