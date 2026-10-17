#!/bin/sh
# GF1I — deterministic re-extraction of the reviewed closure.
#
# The staged 74-file native closure, the PV3/PV2I frozen packet and the
# candidate relation module are NOT committed into this return: they are the
# candidate's and PV3's material, byte-identical, and reproducible by extraction
# from the two pinned commits below.  Custody is re-verified at run time by
# gf1_bootstrap.py (Git blob SHA-1 NUL preimage + sha256 + byte count for all
# 74 files) and again by the reviewer's own test
# `test_native_closure_reattested_74_of_74`.
#
# Usage (from the repository root of the reviewer worktree):
#   sh WORKER_RETURNS/PYAT-R18-GF1I-INDEPENDENT-GENERIC-PAIR-R1/court/extract_closure.sh
#
CANDIDATE=9f4a23cef1482e0a81afb1e7a65df90879931465
GF1I=WORKER_RETURNS/PYAT-R18-GF1I-INDEPENDENT-GENERIC-PAIR-R1

git fetch origin agent/userdirect-pyat-20261016-r17-gf1-generic-native-pair-relation-r1

rm -rf "$GF1I/court/authority" "$GF1I/court/frozen_pv2i" \
       "$GF1I/court/observations" "$GF1I/court/repro" \
       "$GF1I/court/runtime_root" "$GF1I/court/tests" \
       "$GF1I/court/source_selector.json"

git archive "$CANDIDATE:WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1/court" \
  | tar -x -C "$GF1I/court"

# re-seat this reviewer's own files (they are authored, not extracted)
cp "$GF1I/court/repro.gf1i_backup/gf1i_driver.py" "$GF1I/court/gf1i_driver.py"
cp "$GF1I/court/repro.gf1i_backup/test_gf1i_independent.py" "$GF1I/court/test_gf1i_independent.py"

echo "closure extracted from $CANDIDATE; run:"
echo "  cd $GF1I/court && PYTHONDONTWRITEBYTECODE=1 python3 -m pytest test_gf1i_independent.py -q"