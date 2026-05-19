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

Current references:

| File | Description |
|---|---|
| `cref.fa.gz` | Chlamydomonas reinhardtii reference genome |
| `cref.gff3.gz` | Chlamydomonas reinhardtii gene annotation |

Compressed references are preferred to reduce repository size.

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