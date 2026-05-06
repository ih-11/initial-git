# initial-git

https://github.com/ih-11 '\n'
https://github.com/ha-ibnu

----
# Dotfiles

- bashrc: interactive shell settings, PATH and PYTHONPATH for Korf Lab & Conda
- profile: login shell setup, sources bashrc

# Ibnu Environment Setup

## 1. Create conda environment

```bash
conda env create -f envs/ibnu.yml
```

## 2. Activate

```bash
conda activate ibnu
```

## 3. Install private libraries

```bash
bash install_private_libs.sh
```

## Notes

* Private libraries are NOT included in this repo
* Update LIB_ROOT path if needed
