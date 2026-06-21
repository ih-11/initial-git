# initial-git

Personal initialization repository for environment setup, reference data, and reusable bioinformatics utilities.

Repositories:
- https://github.com/ih-11
- https://github.com/ha-ibnu

---

# Repository Structure

```text
initial-git/
├── data/       reference genomes and annotations
├── dotfiles/   shell configuration files
├── env/        conda environments and setup scripts
├── lib/        reusable bioinformatics utility scripts
```

---

# Dotfiles

- `bashrc`
  - interactive shell settings
  - PATH and PYTHONPATH configuration
  - Conda initialization
  - Korf Lab environment configuration

- `profile`
  - login shell setup
  - sources `.bashrc`

---

# Environment Setup

## 1. Create conda environment

```bash
conda env create -f env/environment.yml
```

## 2. Activate environment

```bash
conda activate ibnu
```

## 3. Install private libraries

```bash
bash env/install_private_libs.sh
```

---

# Reference Data

The `data/` directory stores lightweight reusable reference datasets for development, testing, benchmarking, and bioinformatics workflows.

## Chlamydomonas reinhardtii Reference

Current reference files:

| File | Description |
|---|---|
| `cref.fa.gz` | Chlamydomonas reinhardtii CC-4532 genome assembly v6.0 |
| `cref.gff3.gz` | Chlamydomonas reinhardtii CC-4532 gene annotation v6.1 |

Reference source:

- Joint Genome Institute (JGI) / Phytozome
- Organism: *Chlamydomonas reinhardtii* CC-4532
- Assembly version: v6.0
- Annotation version: v6.1

Compressed FASTA and GFF3 files are stored to reduce repository size and simplify distribution.

Please cite:

Craig RJ, Gallaher SD, Shu S, et al. (2022).

*The Chlamydomonas Genome Project, version 6: reference assemblies for mating type plus and minus strains reveal extensive structural mutation in the laboratory.*

https://doi.org/10.1101/2022.06.16.496473

---

# Miniature Reference Genomes

Small reference genomes are provided for rapid testing, lightweight benchmarking, pipeline development, and teaching.

Current miniature reference:

| File | Description |
|---|---|
| `cref1pct.fa.gz` | 1% Chlamydomonas reference genome |
| `cref1pct.gff3.gz` | Matching annotation |

These datasets are intended for:

- rapid alignment testing
- pipeline prototyping
- benchmark development
- teaching
- visualization
- CI/testing workflows

---

# Utility Scripts

The `lib/` directory contains reusable helper scripts for generating benchmark datasets.

## fasample.py

Generate a sampled reference FASTA.

Usage

```bash
python lib/fasample.py input.fa.gz output.fa.gz fraction
```

Examples

```bash
python lib/fasample.py genome.fa.gz genome1pct.fa.gz 0.01
python lib/fasample.py genome.fa.gz genome5pct.fa.gz 0.05
python lib/fasample.py genome.fa.gz genome10pct.fa.gz 0.10
```

---

## gffcut.py

Generate a matching GFF3 annotation from a sampled reference FASTA.

Usage

```bash
python lib/gffcut.py sampled.fa.gz input.gff3.gz output.gff3.gz
```

Example

```bash
python lib/gffcut.py \
genome1pct.fa.gz \
genome.gff3.gz \
genome1pct.gff3.gz
```

---

## fqsample.py

Generate a reproducible random FASTQ subset.

Usage

```bash
python lib/fqsample.py input.fastq.gz output.fastq.gz fraction seed
```

Examples

```bash
python lib/fqsample.py reads.fastq.gz reads1pct.fastq.gz 0.01 42
python lib/fqsample.py reads.fastq.gz reads5pct.fastq.gz 0.05 42
python lib/fqsample.py reads.fastq.gz reads10pct.fastq.gz 0.10 42
```

The random seed guarantees reproducible sampling.

---

# Typical Workflow

Create a sampled reference genome

```bash
python lib/fasample.py genome.fa.gz genome1pct.fa.gz 0.01
```

Generate the corresponding annotation

```bash
python lib/gffcut.py genome1pct.fa.gz genome.gff3.gz genome1pct.gff3.gz
```

Generate a sampled sequencing dataset

```bash
python lib/fqsample.py reads.fastq.gz reads1pct.fastq.gz 0.01 42
```

These scripts allow rapid generation of lightweight benchmark datasets for testing and development.

---

# Notes

- Private libraries are NOT included in this repository.
- Update `LIB_ROOT` paths if needed.
- Large sequencing datasets are managed outside this repository.
- This repository is intended for lightweight reusable setup, development, and benchmarking.

---

# Future Development

Planned additions:

- additional reference genomes
- benchmark sequencing datasets
- reusable workflow templates
- alignment test datasets
- alternative splicing benchmark resources
- transcriptome benchmark datasets