#!/usr/bin/env python3

"""
Add exon, five_prime_UTR, and three_prime_UTR features
to an existing transcript-level GFF3 annotation.

The UTR input files must be tab-separated with five columns:

    transcript_id    chromosome    start    end    strand

The UTR coordinates may include one CDS boundary nucleotide.
This script derives the final UTR boundaries from the CDS coordinates,
thereby excluding the CDS-overlapping nucleotide.
"""

import argparse
import gzip
from collections import defaultdict
from pathlib import Path
from typing import TextIO


def open_text(path: Path) -> TextIO:
    """Open a plain-text or gzip-compressed text file."""

    if path.suffix == ".gz":
        return gzip.open(path, "rt")

    return path.open("r")


def parse_attributes(text: str) -> dict[str, str]:
    """Parse the ninth GFF3 column into a dictionary."""

    attributes = {}

    for field in text.split(";"):
        if "=" not in field:
            continue

        key, value = field.split("=", 1)
        attributes[key] = value

    return attributes


def load_utr_records(path: Path) -> dict[str, dict]:
    """Load transcript-level UTR coordinates from a TSV file."""

    records = {}

    with path.open() as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.rstrip("\n")

            if not line or line.startswith("#"):
                continue

            fields = line.split("\t")

            if len(fields) != 5:
                raise ValueError(
                    f"{path}, line {line_number}: "
                    f"expected 5 columns, found {len(fields)}"
                )

            transcript_id, chromosome, start, end, strand = fields

            if strand not in {"+", "-"}:
                raise ValueError(
                    f"{path}, line {line_number}: "
                    f"invalid strand {strand!r}"
                )

            if transcript_id in records:
                raise ValueError(
                    f"{path}, line {line_number}: "
                    f"duplicate transcript ID {transcript_id}"
                )

            records[transcript_id] = {
                "chrom": chromosome,
                "start": int(start),
                "end": int(end),
                "strand": strand,
            }

    return records


def make_feature(
    *,
    chrom: str,
    feature_type: str,
    start: int,
    end: int,
    strand: str,
    attributes: str,
    source: str = "derived",
) -> dict:
    """Construct one GFF3 feature record."""

    return {
        "chrom": chrom,
        "source": source,
        "type": feature_type,
        "start": start,
        "end": end,
        "score": ".",
        "strand": strand,
        "phase": ".",
        "attributes": attributes,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Add exon and UTR features to an existing GFF3 annotation."
        )
    )

    parser.add_argument(
        "--gff",
        required=True,
        type=Path,
        help="Input GFF3, optionally gzip-compressed",
    )

    parser.add_argument(
        "--utr5",
        required=True,
        type=Path,
        help="Five-prime UTR coordinate TSV",
    )

    parser.add_argument(
        "--utr3",
        required=True,
        type=Path,
        help="Three-prime UTR coordinate TSV",
    )

    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Output uncompressed GFF3",
    )

    args = parser.parse_args()

    utr5 = load_utr_records(args.utr5)
    utr3 = load_utr_records(args.utr3)

    headers = []
    original_features = []

    mrna_records = {}
    introns_by_transcript = defaultdict(list)
    cds_by_transcript = defaultdict(list)

    with open_text(args.gff) as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.rstrip("\n")

            if line.startswith("#"):
                headers.append(line)
                continue

            if not line:
                continue

            fields = line.split("\t")

            if len(fields) != 9:
                raise ValueError(
                    f"{args.gff}, line {line_number}: "
                    f"expected 9 GFF3 columns, found {len(fields)}"
                )

            (
                chrom,
                source,
                feature_type,
                start,
                end,
                score,
                strand,
                phase,
                attributes_text,
            ) = fields

            start = int(start)
            end = int(end)
            attributes = parse_attributes(attributes_text)

            original_features.append(
                {
                    "chrom": chrom,
                    "source": source,
                    "type": feature_type,
                    "start": start,
                    "end": end,
                    "score": score,
                    "strand": strand,
                    "phase": phase,
                    "attributes": attributes_text,
                }
            )

            if feature_type == "mRNA":
                transcript_id = attributes.get("ID")

                if transcript_id is None:
                    raise ValueError(
                        f"{args.gff}, line {line_number}: "
                        "mRNA feature has no ID"
                    )

                mrna_records[transcript_id] = {
                    "chrom": chrom,
                    "start": start,
                    "end": end,
                    "strand": strand,
                }

            elif feature_type == "intron":
                for transcript_id in attributes.get(
                    "Parent",
                    "",
                ).split(","):
                    if transcript_id:
                        introns_by_transcript[transcript_id].append(
                            (start, end)
                        )

            elif feature_type == "CDS":
                for transcript_id in attributes.get(
                    "Parent",
                    "",
                ).split(","):
                    if transcript_id:
                        cds_by_transcript[transcript_id].append(
                            (start, end)
                        )

    generated_features = []

    # ========================================
    # Generate exon features from mRNA spans
    # minus annotated introns
    # ========================================

    for transcript_id, mrna in mrna_records.items():
        introns = sorted(
            introns_by_transcript.get(transcript_id, [])
        )

        exon_start = mrna["start"]
        exon_number = 1

        for intron_start, intron_end in introns:
            exon_end = intron_start - 1

            if exon_start <= exon_end:
                generated_features.append(
                    make_feature(
                        chrom=mrna["chrom"],
                        feature_type="exon",
                        start=exon_start,
                        end=exon_end,
                        strand=mrna["strand"],
                        attributes=(
                            f"ID={transcript_id}.exon{exon_number};"
                            f"Parent={transcript_id}"
                        ),
                    )
                )

                exon_number += 1

            exon_start = intron_end + 1

        if exon_start <= mrna["end"]:
            generated_features.append(
                make_feature(
                    chrom=mrna["chrom"],
                    feature_type="exon",
                    start=exon_start,
                    end=mrna["end"],
                    strand=mrna["strand"],
                    attributes=(
                        f"ID={transcript_id}.exon{exon_number};"
                        f"Parent={transcript_id}"
                    ),
                )
            )

    # ========================================
    # Generate UTR features
    # ========================================

    shared_utr_ids = set(utr5) & set(utr3)

    missing_mrna = []
    missing_cds = []
    inconsistent_records = []

    for transcript_id in sorted(shared_utr_ids):
        if transcript_id not in mrna_records:
            missing_mrna.append(transcript_id)
            continue

        if transcript_id not in cds_by_transcript:
            missing_cds.append(transcript_id)
            continue

        mrna = mrna_records[transcript_id]
        five = utr5[transcript_id]
        three = utr3[transcript_id]

        if (
            five["chrom"] != mrna["chrom"]
            or three["chrom"] != mrna["chrom"]
            or five["strand"] != mrna["strand"]
            or three["strand"] != mrna["strand"]
        ):
            inconsistent_records.append(transcript_id)
            continue

        cds_records = cds_by_transcript[transcript_id]

        cds_start = min(start for start, _ in cds_records)
        cds_end = max(end for _, end in cds_records)

        if mrna["strand"] == "+":
            five_start = five["start"]
            five_end = cds_start - 1

            three_start = cds_end + 1
            three_end = three["end"]

        else:
            five_start = cds_end + 1
            five_end = five["end"]

            three_start = three["start"]
            three_end = cds_start - 1

        if five_start <= five_end:
            generated_features.append(
                make_feature(
                    chrom=mrna["chrom"],
                    feature_type="five_prime_UTR",
                    start=five_start,
                    end=five_end,
                    strand=mrna["strand"],
                    attributes=(
                        f"ID={transcript_id}.five_prime_UTR;"
                        f"Parent={transcript_id}"
                    ),
                )
            )

        if three_start <= three_end:
            generated_features.append(
                make_feature(
                    chrom=mrna["chrom"],
                    feature_type="three_prime_UTR",
                    start=three_start,
                    end=three_end,
                    strand=mrna["strand"],
                    attributes=(
                        f"ID={transcript_id}.three_prime_UTR;"
                        f"Parent={transcript_id}"
                    ),
                )
            )

    # Sort lexicographically by chromosome, then coordinate.
    # A later `sort -k1,1V` step can impose natural chromosome order.
    feature_rank = {
        "gene": 1,
        "mRNA": 2,
        "exon": 3,
        "five_prime_UTR": 4,
        "CDS": 5,
        "three_prime_UTR": 6,
        "intron": 7,
    }

    all_features = original_features + generated_features

    all_features.sort(
        key=lambda record: (
            record["chrom"],
            record["start"],
            record["end"],
            feature_rank.get(record["type"], 99),
            record["attributes"],
        )
    )

    args.output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with args.output.open("w") as output:
        if not any(
            header.startswith("##gff-version")
            for header in headers
        ):
            output.write("##gff-version 3\n")

        for header in headers:
            output.write(header + "\n")

        for record in all_features:
            output.write(
                "\t".join(
                    [
                        record["chrom"],
                        record["source"],
                        record["type"],
                        str(record["start"]),
                        str(record["end"]),
                        record["score"],
                        record["strand"],
                        record["phase"],
                        record["attributes"],
                    ]
                )
                + "\n"
            )

    exon_count = sum(
        record["type"] == "exon"
        for record in generated_features
    )

    utr5_count = sum(
        record["type"] == "five_prime_UTR"
        for record in generated_features
    )

    utr3_count = sum(
        record["type"] == "three_prime_UTR"
        for record in generated_features
    )

    print(f"mRNA records: {len(mrna_records)}")
    print(f"5' UTR input records: {len(utr5)}")
    print(f"3' UTR input records: {len(utr3)}")
    print(f"Shared UTR transcript IDs: {len(shared_utr_ids)}")
    print(f"Generated exon features: {exon_count}")
    print(f"Generated five_prime_UTR features: {utr5_count}")
    print(f"Generated three_prime_UTR features: {utr3_count}")
    print(f"UTR transcripts absent from mRNA annotation: {len(missing_mrna)}")
    print(f"UTR transcripts without CDS annotation: {len(missing_cds)}")
    print(f"Inconsistent chromosome/strand records: {len(inconsistent_records)}")
    print(f"Output: {args.output}")


if __name__ == "__main__":
    main()