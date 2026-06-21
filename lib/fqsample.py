#!/usr/bin/env python3

import gzip
import random
import sys

inp = sys.argv[1]
out = sys.argv[2]
pct = float(sys.argv[3])
seed = int(sys.argv[4])

random.seed(seed)

with gzip.open(inp, "rt") as fin, gzip.open(out, "wt") as fout:

    while True:
        header = fin.readline()
        if not header:
            break

        seq = fin.readline()
        plus = fin.readline()
        qual = fin.readline()

        if random.random() < pct:
            fout.write(header)
            fout.write(seq)
            fout.write(plus)
            fout.write(qual)