#!/bin/bash
# Script to produce global words file and JSON for different implementations

for src in sources/*.txt; do
  src_base=${src#sources/}
  echo -n "$src... "

  echo -n 'picking words... '
  grep -v '^#' "$src" |
  while read w; do echo ${#w} $w; done |
  sort -s -n -k 1 |
  tee >(shuf -n 50) >(tail -200) |
  sort |
  uniq |
  shuf -n 200 |
  cut -f 2 -d ' ' > "$src_base"

  echo -n 'generating JSON... '
  echo -n $(../py/blah g "$src_base" "${src_base%.txt}.json") ' '

  echo "done"
done
