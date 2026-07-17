#!/usr/bin/env python3

import gzip
import sys

fa = sys.argv[1]
gff = sys.argv[2]
out = sys.argv[3]

limits = {}

with gzip.open(fa, "rt") as f:
    name = None
    length = 0

    for line in f:
        line = line.strip()
        if line.startswith(">"):
            if name:
                limits[name] = length
            name = line[1:].split()[0]
            length = 0
        else:
            length += len(line)

    if name:
        limits[name] = length

with gzip.open(gff, "rt") as fin, gzip.open(out, "wt") as fout:
    for line in fin:
        if line.startswith("#"):
            fout.write(line)
            continue

        parts = line.rstrip("\n").split("\t")
        if len(parts) < 5:
            continue

        chrom = parts[0]
        start = int(parts[3])
        end = int(parts[4])

        if chrom in limits and end <= limits[chrom]:
            fout.write(line)