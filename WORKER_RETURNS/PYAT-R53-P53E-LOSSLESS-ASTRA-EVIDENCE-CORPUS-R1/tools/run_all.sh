#!/bin/bash
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
R="WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1"
export PYTHONHASHSEED=0
printf 'P53E deterministic run start: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
python3 "$R/tools/collect_environment.py"
python3 "$R/tools/build_shards.py"
python3 "$R/tools/verify_corpus.py" --json-out "$R/receipts/verify_corpus.json"
python3 "$R/tools/challenge_scope.py"
python3 "$R/tools/build_lookup.py"
python3 "$R/tools/adversarial_test.py"
python3 "$R/tools/render_index.py"
printf 'P53E deterministic run end: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
