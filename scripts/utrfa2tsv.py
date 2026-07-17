#!/usr/bin/env python3

import argparse
import re
import zipfile
from pathlib import Path


HEADER_RE = re.compile(
    r"_(?P<transcript_id>Y[A-P][LR]\d{3}[WC](?:-[A-Z])?_id\d+)_"
    r"(?:five_prime_UTR|three_prime_UTR)"
    r".*range=(?P<chrom>[^:]+):(?P<start>\d+)-(?P<end>\d+)"
    r".*strand=(?P<strand>[+-])"
)


parser = argparse.ArgumentParser(
    description="Convert SGD UTR FASTA headers to coordinate TSV."
)

parser.add_argument(
    "input_zip",
    type=Path,
    help="Input ZIP containing one UTR FASTA file.",
)

parser.add_argument(
    "output_tsv",
    type=Path,
    help="Output five-column TSV.",
)

args = parser.parse_args()


with zipfile.ZipFile(args.input_zip) as archive:

    fasta_files = [
        name
        for name in archive.namelist()
        if not name.endswith("/")
    ]

    if len(fasta_files) != 1:
        raise ValueError(
            f"Expected one file in {args.input_zip}, "
            f"found {len(fasta_files)}"
        )

    fasta_name = fasta_files[0]

    seen = set()
    count = 0

    with archive.open(fasta_name) as fin, args.output_tsv.open("w") as fout:

        for raw_line in fin:
            line = raw_line.decode("utf-8").rstrip("\n")

            if not line.startswith(">"):
                continue

            match = HEADER_RE.search(line)

            if match is None:
                raise ValueError(
                    f"Could not parse FASTA header:\n{line}"
                )

            transcript_id = match.group("transcript_id")
            chrom = match.group("chrom")
            start = match.group("start")
            end = match.group("end")
            strand = match.group("strand")

            if transcript_id in seen:
                raise ValueError(
                    f"Duplicate transcript ID: {transcript_id}"
                )

            seen.add(transcript_id)

            fout.write(
                f"{transcript_id}\t"
                f"{chrom}\t"
                f"{start}\t"
                f"{end}\t"
                f"{strand}\n"
            )

            count += 1


print(f"UTR records written: {count}")
print(f"Output: {args.output_tsv}")