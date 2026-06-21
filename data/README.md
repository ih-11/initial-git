# Reference Data

The `data/` directory stores reusable reference genomes, gene annotations, and lightweight benchmark references for development, testing, and bioinformatics workflows.

Each reference consists of:

- reference genome (FASTA)
- gene annotation (GFF3)
- optional miniature reference genomes
- optional miniature annotations

---

# Available References

| Prefix | Organism | Assembly | Annotation |
|---------|----------|----------|------------|
| `at` | *Arabidopsis thaliana* | TAIR10 | Araport11 |
| `cref` | *Chlamydomonas reinhardtii* CC-4532 | v6.0 | v6.1 |

---

# Arabidopsis thaliana

Current files:

| File | Description |
|------|-------------|
| `at.fa.gz` | Arabidopsis thaliana TAIR10 reference genome |
| `at.gff3.gz` | Araport11 gene annotation |

## Reference Source

- The Arabidopsis Information Resource (TAIR)
- Genome assembly: TAIR10 (GCA_000001735.1)
- Annotation: Araport11 (201606)

## Repository Notes

This repository stores a cleaned version of the reference used for downstream analyses.

Modifications include:

- removal of the external Renilla luciferase (Rluc) spike-in sequence
- removal of corresponding spike-in annotations
- chromosome naming follows the `Chr1`–`Chr5`, `ChrM`, and `ChrC` convention

## Citation

Cheng CY, Krishnakumar V, Chan AP, et al. (2017).

*Araport11: a complete reannotation of the Arabidopsis thaliana reference genome.*

The Plant Journal, 89(4), 789–804.

https://doi.org/10.1111/tpj.13415

---

# Chlamydomonas reinhardtii

Current files:

| File | Description |
|------|-------------|
| `cref.fa.gz` | Chlamydomonas reinhardtii CC-4532 genome assembly v6.0 |
| `cref.gff3.gz` | Chlamydomonas reinhardtii CC-4532 gene annotation v6.1 |
| `cref1pct.fa.gz` | 1% benchmark reference genome |
| `cref1pct.gff3.gz` | Matching 1% annotation |

## Reference Source

- Joint Genome Institute (JGI) / Phytozome
- Organism: *Chlamydomonas reinhardtii* CC-4532
- Genome assembly: v6.0
- Annotation: v6.1

## Repository Notes

The miniature reference was generated using the utility scripts in `../lib/`:

- `fasample.py`
- `gffcut.py`

The benchmark reference is intended for:

- rapid pipeline testing
- alignment debugging
- workflow prototyping
- teaching
- benchmarking

## Citation

Craig RJ, Gallaher SD, Shu S, et al. (2022).

*The Chlamydomonas Genome Project, version 6: reference assemblies for mating type plus and minus strains reveal extensive structural mutation in the laboratory.*

https://doi.org/10.1101/2022.06.16.496473

---

# Naming Convention

Reference files follow a short prefix convention.

| Prefix | Organism |
|---------|----------|
| `at` | *Arabidopsis thaliana* |
| `cref` | *Chlamydomonas reinhardtii* |

Miniature benchmark references append the sampling level.

Examples:

```
at.fa.gz
at.gff3.gz

cref.fa.gz
cref.gff3.gz

cref1pct.fa.gz
cref1pct.gff3.gz
```

---

# Future References

Additional species will be added following the same structure.

Examples include:

- *Oryza sativa*
- *Nicotiana benthamiana*
- additional model organisms
- benchmark reference genomes