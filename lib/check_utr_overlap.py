#!/usr/bin/env python3

import gzip
import re
import argparse
from collections import defaultdict


def open_text(path):
    return gzip.open(path, "rt") if path.endswith(".gz") else open(path)


def attrs_to_dict(s):
    d = {}
    for item in s.split(";"):
        if "=" in item:
            k, v = item.split("=", 1)
            d[k] = v
    return d


def main():
    p = argparse.ArgumentParser()
    p.add_argument("original_gff")
    p.add_argument("utr_gff")
    p.add_argument("-o", "--out", required=True)
    args = p.parse_args()

    genes = []
    mrna = {}

    with open_text(args.original_gff) as f:
        for line in f:
            if line.startswith("#"):
                continue
            parts = line.rstrip().split("\t")
            if len(parts) != 9:
                continue

            chrom, source, feature, start, end, score, strand, phase, attr = parts
            start, end = int(start), int(end)
            a = attrs_to_dict(attr)

            if feature == "gene":
                genes.append({
                    "id": a.get("ID"),
                    "locus_tag": a.get("locus_tag", "."),
                    "chrom": chrom,
                    "start": start,
                    "end": end,
                    "strand": strand,
                })

            elif feature == "mRNA":
                mrna_id = a.get("ID")
                if mrna_id:
                    mrna[mrna_id] = {
                        "id": mrna_id,
                        "gene": a.get("Parent"),
                        "locus_tag": a.get("locus_tag", "."),
                        "chrom": chrom,
                        "start": start,
                        "end": end,
                        "strand": strand,
                    }

    utr_by_parent = defaultdict(lambda: [10**18, -1])

    with open_text(args.utr_gff) as f:
        for line in f:
            if line.startswith("#"):
                continue
            parts = line.rstrip().split("\t")
            if len(parts) != 9 or parts[2] != "three_prime_UTR":
                continue

            start, end = int(parts[3]), int(parts[4])
            a = attrs_to_dict(parts[8])
            parent = a.get("Parent")

            if not parent or parent.startswith("missing-"):
                continue

            utr_by_parent[parent][0] = min(utr_by_parent[parent][0], start)
            utr_by_parent[parent][1] = max(utr_by_parent[parent][1], end)

    checked = 0
    overlap_cases = 0

    with open(args.out, "w") as out:
        out.write(
            "mrna_id\tgene_id\tlocus_tag\tchrom\told_start\told_end\t"
            "new_start\tnew_end\toverlap_gene_id\toverlap_locus_tag\t"
            "overlap_start\toverlap_end\toverlap_strand\n"
        )

        for parent, (utr_start, utr_end) in utr_by_parent.items():
            if parent not in mrna:
                continue

            m = mrna[parent]
            checked += 1

            new_start = min(m["start"], utr_start)
            new_end = max(m["end"], utr_end)

            for g in genes:
                if g["chrom"] != m["chrom"]:
                    continue
                if g["id"] == m["gene"]:
                    continue

                # overlap test
                if new_start <= g["end"] and new_end >= g["start"]:
                    overlap_cases += 1
                    out.write(
                        f"{parent}\t{m['gene']}\t{m['locus_tag']}\t{m['chrom']}\t"
                        f"{m['start']}\t{m['end']}\t{new_start}\t{new_end}\t"
                        f"{g['id']}\t{g['locus_tag']}\t{g['start']}\t{g['end']}\t{g['strand']}\n"
                    )

    print(f"Checked mRNAs: {checked}")
    print(f"Overlap rows: {overlap_cases}")
    print(f"Report: {args.out}")


if __name__ == "__main__":
    main()