#!/usr/bin/env python3

import gzip
import sys
import textwrap

inp = sys.argv[1]
out = sys.argv[2]
pct = float(sys.argv[3])

with gzip.open(inp, "rt") as fin, gzip.open(out, "wt") as fout:
    name = None
    seqs = []

    def write_record(name, seq):
        if name is None:
            return

        n = max(1, int(len(seq) * pct))

        fout.write(f">{name}\n")
        for chunk in textwrap.wrap(seq[:n], 60):
            fout.write(chunk + "\n")

    for line in fin:
        line = line.strip()

        if line.startswith(">"):
            write_record(name, "".join(seqs))
            name = line[1:].split()[0]
            seqs = []
        else:
            seqs.append(line)

    write_record(name, "".join(seqs))