#!/usr/bin/env python3

import sys

results = set([])

for line in sys.stdin:
    if len(line) >= 8 and line not in results:
        results.add(line)
        print(line, end='')

