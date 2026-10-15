#!/usr/bin/env bash
# HQ300 C0 full battery: repaired candidate K9/K10, RC0 frozen 25, connection
# oracle, and the pinned owner suites 56+21.
set -u
RET="$(cd "$(dirname "$0")/.." && pwd)"
REPO="$(cd "$RET/../.." && pwd)"
export PYTHONPATH="$REPO:$RET:$RET/staging/ns:$RET/staging/ns/rawlsing_next/tests:$REPO/rawlsing_next/tests"
export RC0_RETURN="$RET/repro/rc0_runtime"
cd "$RET"

echo "== [1/5] repaired candidate K9 8 + K10 28 =="
python3 -m pytest port/test_k9_provider_swap.py port/test_k10_structural_conservation.py -q -p no:cacheprovider --junitxml=repro/k9_k10.junit.xml 2>&1 | tee repro/k9_k10.log | tail -2

echo "== [2/5] RC0 frozen independent 25 (unchanged reviewer source) =="
python3 -m pytest staging/rc0/test_rc0_hostile.py -q -p no:cacheprovider --junitxml=repro/rc0_25.junit.xml 2>&1 | tee repro/rc0_25.log | tail -2

echo "== [3/5] connection oracle (adapter -> pinned PE/C1/N10E call trace) =="
python3 -m pytest port/test_connection.py -q -p no:cacheprovider --junitxml=repro/connection.junit.xml 2>&1 | tee repro/connection.log | tail -2

echo "== [4/5] pinned N10E 43 + C1 13 owner suites =="
python3 -m pytest staging/ns/rawlsing_next/tests/test_pre553_empirical_possibility_provider.py staging/ns/rawlsing_next/tests/test_pre553_analytical_composition.py -q -p no:cacheprovider --junitxml=repro/n10e_c1.junit.xml 2>&1 | tee repro/n10e_c1.log | tail -2

echo "== [5/5] pinned PE author suite 21 =="
python3 -m pytest staging/ns/rawlsing_next/tests/test_postastra_pe_generic_world_possibility.py -q -p no:cacheprovider --junitxml=repro/pe_21.junit.xml 2>&1 | tee repro/pe_21.log | tail -2

echo "== done =="
