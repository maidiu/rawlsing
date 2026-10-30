#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BASELINE="${F0R4_BASELINE_REF:-299f41e97a43c67be9cc76a79fa49b48f4e12e54}"

for cut in current_head_59c9a7a4 sealed_342164; do
  out="$(cd "$HERE/$cut" && PYTHONDONTWRITEBYTECODE=1 python3 verify_branch_fanin.py --selftest --baseline-ref "$BASELINE" 2>&1)"
  printf '%s\n' "$out"
  grep -q "PASS sourcefree record integrity" <<<"$out"
  grep -q "PASS: 20 mutation witnesses rejected" <<<"$out"
done

PYTHONDONTWRITEBYTECODE=1 python3 "$HERE/f0r4_twenty_witness_run.py" \
  --validator "$HERE/verify_branch_fanin.py" \
  --control-dir "$HERE/current_head_59c9a7a4" \
  --expect candidate | grep -q '"all_expected": true'

PYTHONDONTWRITEBYTECODE=1 python3 "$HERE/f0r4_twenty_witness_run.py" \
  --validator "$HERE/verify_branch_fanin.py" \
  --control-dir "$HERE/sealed_342164" \
  --expect candidate | grep -q '"all_expected": true'

printf 'PASS F0R4 candidate 20-witness CI\n'
