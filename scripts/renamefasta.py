#!/usr/bin/env python3

import argparse
import gzip
import sys
from pathlib import Path
from typing import TextIO


CHR_MAP = {
    "NC_001133.9": "chrI",
    "NC_001134.8": "chrII",
    "NC_001135.5": "chrIII",
    "NC_001136.10": "chrIV",
    "NC_001137.3": "chrV",
    "NC_001138.5": "chrVI",
    "NC_001139.9": "chrVII",
    "NC_001140.6": "chrVIII",
    "NC_001141.2": "chrIX",
    "NC_001142.9": "chrX",
    "NC_001143.9": "chrXI",
    "NC_001144.5": "chrXII",
    "NC_001145.3": "chrXIII",
    "NC_001146.8": "chrXIV",
    "NC_001147.6": "chrXV",
    "NC_001148.4": "chrXVI",
    "NC_001224.1": "chrM",
}


def open_text(path: Path, mode: str) -> TextIO:
    """Open a plain-text or gzip-compressed file."""

    if path.suffix == ".gz":
        return gzip.open(path, mode, encoding="utf-8")

    return path.open(mode, encoding="utf-8")


def rename_fasta(input_path: Path, output_path: Path) -> None:
    """Rename chromosome identifiers in FASTA headers."""

    seen_headers = set()
    renamed_count = 0
    sequence_count = 0

    with open_text(input_path, "rt") as infile, open_text(
        output_path,
        "wt",
    ) as outfile:
        for line_number, line in enumerate(infile, start=1):
            if not line.startswith(">"):
                outfile.write(line)
                continue

            sequence_count += 1

            header = line[1:].rstrip("\n")
            parts = header.split(maxsplit=1)

            old_name = parts[0]

            if old_name not in CHR_MAP:
                raise ValueError(
                    f"Unknown FASTA identifier at line {line_number}: "
                    f"{old_name}"
                )

            new_name = CHR_MAP[old_name]

            if new_name in seen_headers:
                raise ValueError(
                    f"Duplicate renamed FASTA identifier: {new_name}"
                )

            seen_headers.add(new_name)
            renamed_count += 1

            if len(parts) == 2:
                outfile.write(f">{new_name} {parts[1]}\n")
            else:
                outfile.write(f">{new_name}\n")

    expected = set(CHR_MAP.values())
    observed = seen_headers

    missing = sorted(expected - observed)

    if missing:
        raise ValueError(
            "The following expected chromosomes were not found: "
            + ", ".join(missing)
        )

    print(
        f"Input sequences: {sequence_count}",
        file=sys.stderr,
    )
    print(
        f"Renamed sequences: {renamed_count}",
        file=sys.stderr,
    )
    print(
        f"Output: {output_path}",
        file=sys.stderr,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Rename SGD RefSeq chromosome identifiers in a FASTA file."
        )
    )

    parser.add_argument(
        "input_fasta",
        type=Path,
        help="Input FASTA file, optionally gzip-compressed.",
    )

    parser.add_argument(
        "output_fasta",
        type=Path,
        help="Output FASTA file, optionally ending in .gz.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not args.input_fasta.is_file():
        sys.exit(
            f"Error: input file not found: {args.input_fasta}"
        )

    args.output_fasta.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    try:
        rename_fasta(
            args.input_fasta,
            args.output_fasta,
        )
    except (OSError, ValueError) as error:
        sys.exit(f"Error: {error}")


if __name__ == "__main__":
    main()