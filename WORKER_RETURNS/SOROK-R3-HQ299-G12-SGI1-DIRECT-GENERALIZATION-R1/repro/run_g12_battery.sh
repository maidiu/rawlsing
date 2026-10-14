#!/usr/bin/env bash
# G12 full execution battery: original S-GI1 K11 suite + GI2 57 predicates on S-GI1.
set -u
RET="$(cd "$(dirname "$0")/.." && pwd)"
cd "$RET"

echo "== [1/2] ORIGINAL S-GI1 K11 24-case/98-predicate suite (frozen-record replay, 0 model calls) =="
echo "command: SGI1_MODEL=0 SGI1_REUSE_RECORDS=1 python3 01_LAB_IMPLEMENTATION/run_k11.py  (cwd repro/sigi1_run)"
( cd repro/sigi1_run/01_LAB_IMPLEMENTATION && SGI1_MODEL=0 SGI1_REUSE_RECORDS=1 python3 run_k11.py ) 2>&1 | tee repro/k11_stdout.txt | tail -10

echo "== [2/2] GI2 12-family / 57-predicate suite on ACTUAL S-GI1 =="
echo "command: python3 -m pytest gi2/test_gi2_on_sgi1.py -q --junitxml=repro/gi2_57.junit.xml"
python3 -m pytest gi2/test_gi2_on_sgi1.py -q -p no:cacheprovider --junitxml=repro/gi2_57.junit.xml 2>&1 | tee repro/gi2_57_stdout.txt | tail -3

echo "== done =="
