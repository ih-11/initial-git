#!/usr/bin/env python3

import argparse
import gzip


CHR_MAP = {
    "chrmt": "chrM",
}


def open_text(path, mode):
    if str(path).endswith(".gz"):
        return gzip.open(path, mode + "t")
    return open(path, mode)


parser = argparse.ArgumentParser(
    description="Standardize SGD GFF3 chromosome identifiers."
)
parser.add_argument("input")
parser.add_argument("output")
args = parser.parse_args()


with open_text(args.input, "r") as fin, open_text(args.output, "w") as fout:

    for line in fin:

        if line.startswith("#") or not line.strip():
            fout.write(line)
            continue

        fields = line.rstrip("\n").split("\t")

        if len(fields) != 9:
            fout.write(line)
            continue

        chromosome = fields[0]

        if chromosome in CHR_MAP:
            fields[0] = CHR_MAP[chromosome]

        fout.write("\t".join(fields) + "\n")