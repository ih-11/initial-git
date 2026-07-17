#!/usr/bin/env python3

import argparse
import gzip
from pathlib import Path


CHR_MAP = {
    "NC_001133": "chrI",
    "NC_001134": "chrII",
    "NC_001135": "chrIII",
    "NC_001136": "chrIV",
    "NC_001137": "chrV",
    "NC_001138": "chrVI",
    "NC_001139": "chrVII",
    "NC_001140": "chrVIII",
    "NC_001141": "chrIX",
    "NC_001142": "chrX",
    "NC_001143": "chrXI",
    "NC_001144": "chrXII",
    "NC_001145": "chrXIII",
    "NC_001146": "chrXIV",
    "NC_001147": "chrXV",
    "NC_001148": "chrXVI",
    "NC_001224": "chrM",
}


def open_text(path, mode):
    if str(path).endswith(".gz"):
        return gzip.open(path, mode + "t")
    return open(path, mode)


parser = argparse.ArgumentParser(
    description="Rename SGD FASTA chromosome identifiers."
)
parser.add_argument("input")
parser.add_argument("output")
args = parser.parse_args()


with open_text(args.input, "r") as fin, open_text(args.output, "w") as fout:

    for line in fin:

        if not line.startswith(">"):
            fout.write(line)
            continue

        header = line[1:].rstrip()

        # Example:
        # ref|NC_001133|
        accession = header.split("|")[1]

        if accession not in CHR_MAP:
            raise ValueError(
                f"Unknown chromosome accession: {accession}"
            )

        fout.write(f">{CHR_MAP[accession]}\n")