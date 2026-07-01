#!/usr/bin/env python3

import argparse
import gzip
import re
from collections import defaultdict


def open_text(path):
    if path.endswith(".gz"):
        return gzip.open(path, "rt")
    return open(path)


def parse_attrs(attr):
    d = {}
    for item in attr.split(";"):
        if "=" in item:
            k, v = item.split("=", 1)
            d[k] = v
    return d


def read_utr_bounds(utr_gff):
    """
    Return mRNA parent -> min/max UTR coordinate.
    Skip Parent=missing-* records.
    """
    bounds = {}

    with open_text(utr_gff) as f:
        for line in f:
            if line.startswith("#"):
                continue

            parts = line.rstrip("\n").split("\t")
            if len(parts) != 9:
                continue

            if parts[2] != "three_prime_UTR":
                continue

            start = int(parts[3])
            end = int(parts[4])
            attrs = parse_attrs(parts[8])
            parent = attrs.get("Parent")

            if not parent or parent.startswith("missing-"):
                continue

            if parent not in bounds:
                bounds[parent] = [start, end]
            else:
                bounds[parent][0] = min(bounds[parent][0], start)
                bounds[parent][1] = max(bounds[parent][1], end)

    return bounds


def main():
    parser = argparse.ArgumentParser(
        description="Merge NCBI GFF3 with 3UTR features and expand gene/mRNA/terminal exon coordinates."
    )
    parser.add_argument("ncbi_gff")
    parser.add_argument("utr_gff")
    parser.add_argument("-o", "--out", required=True)
    args = parser.parse_args()

    utr_bounds = read_utr_bounds(args.utr_gff)

    lines = []
    mrna_to_gene = {}
    mrna_strand = {}
    gene_to_mrnas = defaultdict(list)
    exon_by_mrna = defaultdict(list)

    with open_text(args.ncbi_gff) as f:
        for idx, line in enumerate(f):
            if line.startswith("##FASTA"):
                break

            if line.startswith("#"):
                lines.append([idx, line.rstrip("\n"), None])
                continue

            parts = line.rstrip("\n").split("\t")
            if len(parts) != 9:
                lines.append([idx, line.rstrip("\n"), None])
                continue

            attrs = parse_attrs(parts[8])
            feature = parts[2]

            if feature == "mRNA":
                mrna_id = attrs.get("ID")
                gene_id = attrs.get("Parent")
                if mrna_id and gene_id:
                    mrna_to_gene[mrna_id] = gene_id
                    mrna_strand[mrna_id] = parts[6]
                    gene_to_mrnas[gene_id].append(mrna_id)

            if feature == "exon":
                parent = attrs.get("Parent")
                if parent:
                    exon_by_mrna[parent].append((idx, int(parts[3]), int(parts[4])))

            lines.append([idx, line.rstrip("\n"), parts])

    genes_to_expand = defaultdict(lambda: [10**18, -1])
    mrnas_to_expand = {}

    for mrna_id, (utr_start, utr_end) in utr_bounds.items():
        gene_id = mrna_to_gene.get(mrna_id)
        if not gene_id:
            continue

        mrnas_to_expand[mrna_id] = (utr_start, utr_end)

        genes_to_expand[gene_id][0] = min(genes_to_expand[gene_id][0], utr_start)
        genes_to_expand[gene_id][1] = max(genes_to_expand[gene_id][1], utr_end)

    n_gene = 0
    n_mrna = 0
    n_exon = 0

    updated_lines = []

    for idx, raw, parts in lines:
        if parts is None:
            updated_lines.append(raw)
            continue

        feature = parts[2]
        attrs = parse_attrs(parts[8])

        if feature == "gene":
            gene_id = attrs.get("ID")
            if gene_id in genes_to_expand:
                old_start = int(parts[3])
                old_end = int(parts[4])
                new_start = min(old_start, genes_to_expand[gene_id][0])
                new_end = max(old_end, genes_to_expand[gene_id][1])
                if new_start != old_start or new_end != old_end:
                    parts[3] = str(new_start)
                    parts[4] = str(new_end)
                    n_gene += 1

        elif feature == "mRNA":
            mrna_id = attrs.get("ID")
            if mrna_id in mrnas_to_expand:
                utr_start, utr_end = mrnas_to_expand[mrna_id]
                old_start = int(parts[3])
                old_end = int(parts[4])
                new_start = min(old_start, utr_start)
                new_end = max(old_end, utr_end)
                if new_start != old_start or new_end != old_end:
                    parts[3] = str(new_start)
                    parts[4] = str(new_end)
                    n_mrna += 1

        elif feature == "exon":
            parent = attrs.get("Parent")
            if parent in mrnas_to_expand:
                strand = mrna_strand.get(parent)
                exons = exon_by_mrna[parent]

                if strand == "+":
                    terminal_idx = max(exons, key=lambda x: x[2])[0]
                else:
                    terminal_idx = min(exons, key=lambda x: x[1])[0]

                if idx == terminal_idx:
                    utr_start, utr_end = mrnas_to_expand[parent]
                    old_start = int(parts[3])
                    old_end = int(parts[4])
                    new_start = min(old_start, utr_start)
                    new_end = max(old_end, utr_end)
                    if new_start != old_start or new_end != old_end:
                        parts[3] = str(new_start)
                        parts[4] = str(new_end)
                        n_exon += 1

        updated_lines.append("\t".join(parts))

    with open(args.out, "w") as fout:
        for line in updated_lines:
            fout.write(line + "\n")

        with open_text(args.utr_gff) as f:
            for line in f:
                if line.startswith("##gff-version"):
                    continue
                fout.write(line)

    print(f"mRNA parents with UTR: {len(utr_bounds)}")
    print(f"Updated genes: {n_gene}")
    print(f"Updated mRNAs: {n_mrna}")
    print(f"Updated terminal exons: {n_exon}")


if __name__ == "__main__":
    main()