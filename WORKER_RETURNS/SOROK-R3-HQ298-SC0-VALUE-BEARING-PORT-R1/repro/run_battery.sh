#!/usr/bin/env bash
# HQ298 SC0 full sourcefree execution battery — real commands, JUnit retained.
set -u
RETURN_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$RETURN_DIR/../.." && pwd)"
export PYTHONPATH="$REPO_ROOT:$RETURN_DIR:$RETURN_DIR/staging/ns:$RETURN_DIR/staging/ns/rawlsing_next/tests:$REPO_ROOT/rawlsing_next/tests"
export HQ297_EXACT_PE_ROOT="$RETURN_DIR/staging/ns"
cd "$RETURN_DIR"
OUT=repro

echo "== [1/4] port K9(8)+K10(28) two-contract court =="
python3 -m pytest port/ -q -p no:cacheprovider --junitxml="$OUT/port_k9_k10.junit.xml" 2>&1 | tee "$OUT/port_k9_k10.log" | tail -2

echo "== [2/4] N10E provider (43) + C1 composition (13) owner suites =="
python3 -m pytest staging/ns/rawlsing_next/tests/test_pre553_empirical_possibility_provider.py staging/ns/rawlsing_next/tests/test_pre553_analytical_composition.py -q -p no:cacheprovider --junitxml="$OUT/n10e_c1.junit.xml" 2>&1 | tee "$OUT/n10e_c1.log" | tail -2

echo "== [3/4] PE author suite (21) =="
python3 -m pytest staging/ns/rawlsing_next/tests/test_postastra_pe_generic_world_possibility.py -q -p no:cacheprovider --junitxml="$OUT/pe_21.junit.xml" 2>&1 | tee "$OUT/pe_21.log" | tail -2

echo "== [4/4] HQ297 independent reviewer PE-boundary suite (13) =="
python3 -m pytest staging/ns/rawlsing_next/tests/test_hq297_k9k10_sc0_pe_independent.py -q -p no:cacheprovider --junitxml="$OUT/reviewer_13.junit.xml" 2>&1 | tee "$OUT/reviewer_13.log" | tail -2

echo "== done =="
