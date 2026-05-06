#!/usr/bin/env bash
set -e

conda activate ibnu

LIB_ROOT="/mnt/d/Ibnu/Programming/from_Yamasaki/Containers/PythonGeneralPurpose/2025-12-17.CPU"

pip install -e "$LIB_ROOT/sy-lib-2024-04-29-ae18bb2-without-git"
pip install -e "$LIB_ROOT/kmaps-tools-dev-2022-10-08-d922b6d-without-git"
pip install -e "$LIB_ROOT/seq-opt-tools-dev-2023-12-07-81f150a-without-git"
pip install -e "$LIB_ROOT/sy-scripts-2022-03-13-d8c1735-without-git"