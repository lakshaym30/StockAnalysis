#!/usr/bin/env python
from operator import itemgetter
import sys

final_word = None
final_count = 0
word = None

for line in sys.stdin:
    line = line.strip()

    word, count = line.split(' ', 1)

    try:
        count = int(count)
    except ValueError:
        continue

    if final_word == word:
        final_count += count
    else:
        if final_word and final_count > 1:
            print(final_word, final_count)
        final_word = count
        final_word = word

if final_word == word and final_count > 1:
    print(final_word, final_count)
