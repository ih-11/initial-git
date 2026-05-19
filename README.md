# initial-git

Personal initialization repository for environment setup, reference data, and reusable bioinformatics configuration.

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

The `data/` directory stores lightweight reusable reference datasets for development, testing, and bioinformatics workflows.

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

The numeric identifier `707` in the original JGI filenames is an internal Phytozome release identifier and is omitted here for simplicity. :contentReference[oaicite:0]{index=0}

Please cite:

Craig RJ, Gallaher SD, Shu S, et al. (2022).  
*The Chlamydomonas Genome Project, version 6: reference assemblies for mating type plus and minus strains reveal extensive structural mutation in the laboratory.*  
https://doi.org/10.1101/2022.06.16.496473

## Miniature Reference Genomes

Small "1% genomes" are provided for lightweight testing, rapid debugging, teaching, and benchmark development.

These datasets contain approximately the first 1% of each chromosome/contig together with matching annotation features.

Current miniature references:

| File | Description |
|---|---|
| `cref1pct.fa.gz` | 1% Chlamydomonas reinhardtii reference genome |
| `cref1pct.gff3.gz` | matching 1% gene annotation |

Miniature references are useful for:

- rapid alignment testing
- splice-aware alignment debugging
- lightweight benchmarking
- pipeline prototyping
- teaching and visualization
- CI/testing workflows

The miniature datasets are generated reproducibly using scripts in `lib/`:

| Script | Purpose |
|---|---|
| `mk1pct.py` | generate miniature FASTA references |
| `gffcut.py` | generate matching annotation subsets |

---

# Notes

- Private libraries are NOT included in this repository
- Update `LIB_ROOT` paths if needed
- Large sequencing datasets are managed outside this repository
- This repository is intended for lightweight reusable setup and development

---

# Future Development

Planned additions:

- miniature test genomes (1% genomes)
- small benchmark datasets
- reusable workflow templates
- alignment test datasets
- alternative splicing benchmark resources