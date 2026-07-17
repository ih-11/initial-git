#!/usr/bin/env python3

import argparse
import gzip
import re


def open_text(path):
    if path.endswith(".gz"):
        return gzip.open(path, "rt")
    return open(path)


def read_chr_map(path):
    chr_map = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            old, new = line.split("\t")
            chr_map[old] = new
    return chr_map


def read_mrna_map(gff_path):
    """
    Build locus_tag -> mRNA ID map from NCBI GFF3.
    Example:
    locus_tag=YAL067C
    ID=rna-NM_001178208.1
    """
    mrna_map = {}

    with open_text(gff_path) as f:
        for line in f:
            if line.startswith("#"):
                continue

            parts = line.rstrip("\n").split("\t")
            if len(parts) != 9:
                continue

            feature = parts[2]
            attrs = parts[8]

            if feature != "mRNA":
                continue

            id_match = re.search(r"(?:^|;)ID=([^;]+)", attrs)
            locus_match = re.search(r"(?:^|;)locus_tag=([^;]+)", attrs)
            gene_match = re.search(r"(?:^|;)gene=([^;]+)", attrs)

            if not id_match or not locus_match:
                continue

            locus_tag = locus_match.group(1)
            mrna_id = id_match.group(1)
            gene_name = gene_match.group(1) if gene_match else "."

            mrna_map[locus_tag] = {
                "mrna_id": mrna_id,
                "gene_name": gene_name,
            }

    return mrna_map


def parse_utr_header(header):
    """
    Example:
    >sacCer3_ct_Pelechanoonlybased3primeUTRs_3950_YAL067C_id001_three_prime_UTR range=chrI:7013-7235 strand=-
    """
    header = header.strip().lstrip(">")

    locus_match = re.search(
        r"_(Y[A-P][LR]\d{3}[WC](?:-[A-Z])?)_id(\d+)_three_prime_UTR",
        header,
    )
    range_match = re.search(r"range=([^:]+):(\d+)-(\d+)", header)
    strand_match = re.search(r"strand=([+-])", header)

    if not locus_match or not range_match or not strand_match:
        return None

    return {
        "locus_tag": locus_match.group(1),
        "utr_id": locus_match.group(2),
        "chrom": range_match.group(1),
        "start": int(range_match.group(2)),
        "end": int(range_match.group(3)),
        "strand": strand_match.group(1),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Convert Pelechano 3prime UTR FASTA headers into GFF3 features."
    )
    parser.add_argument("utr_fasta")
    parser.add_argument("chr_map")
    parser.add_argument("ncbi_gff")
    parser.add_argument("-o", "--out", required=True)
    args = parser.parse_args()

    chr_map = read_chr_map(args.chr_map)
    mrna_map = read_mrna_map(args.ncbi_gff)

    n_total = 0
    n_written = 0
    n_missing_chr = 0
    n_missing_parent = 0
    n_bad_header = 0

    with open_text(args.utr_fasta) as fin, open(args.out, "w") as fout:
        fout.write("##gff-version 3\n")

        for line in fin:
            if not line.startswith(">"):
                continue

            n_total += 1
            rec = parse_utr_header(line)

            if rec is None:
                n_bad_header += 1
                continue

            if rec["chrom"] not in chr_map:
                n_missing_chr += 1
                continue

            ncbi_chrom = chr_map[rec["chrom"]]
            locus_tag = rec["locus_tag"]
            utr_id = rec["utr_id"]

            info = mrna_map.get(locus_tag)

            if info:
                parent = info["mrna_id"]
                gene_name = info["gene_name"]
                note = "Pelechano_validated_3prime_UTR"
            else:
                parent = f"missing-{locus_tag}"
                gene_name = "."
                note = "Pelechano_validated_3prime_UTR;Parent_not_found_in_NCBI_GFF3"
                n_missing_parent += 1

            feature_id = f"utr-{locus_tag}-id{utr_id}"

            attrs = (
                f"ID={feature_id};"
                f"Parent={parent};"
                f"locus_tag={locus_tag};"
                f"gene={gene_name};"
                f"gbkey=three_prime_UTR;"
                f"Note={note}"
            )

            fields = [
                ncbi_chrom,
                "Pelechano_3UTR",
                "three_prime_UTR",
                str(rec["start"]),
                str(rec["end"]),
                ".",
                rec["strand"],
                ".",
                attrs,
            ]

            fout.write("\t".join(fields) + "\n")
            n_written += 1

    print(f"Total UTR headers: {n_total}")
    print(f"Written GFF3 features: {n_written}")
    print(f"Bad headers: {n_bad_header}")
    print(f"Missing chromosome mappings: {n_missing_chr}")
    print(f"Missing mRNA parents: {n_missing_parent}")


if __name__ == "__main__":
    main()