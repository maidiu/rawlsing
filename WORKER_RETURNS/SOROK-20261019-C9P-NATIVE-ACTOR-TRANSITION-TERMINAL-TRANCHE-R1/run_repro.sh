#!/usr/bin/env bash
# C9P candidate tranche: exact reproducible runner.
# Runs the full test suite, the proof-integrity witnesses and the
# separate-process severance court from the repository root.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
RETURN_DIR="WORKER_RETURNS/SOROK-20261019-C9P-NATIVE-ACTOR-TRANSITION-TERMINAL-TRANCHE-R1"
cd "$ROOT"

echo "== C9P candidate tranche repro =="
echo "repo root: $ROOT"
echo "startup:   aa55bca9020d15b539f13a71c526e3d3849a9cbf"

echo ""
echo "== 1. Full test suite =="
python3 -m pytest "$RETURN_DIR/tests/" -q \
  --junitxml="$RETURN_DIR/evidence/junit_repro.xml"

echo ""
echo "== 2. Proof-integrity witnesses =="
python3 /tmp/proof_integrity_gate_r1.py witness \
  "$RETURN_DIR/tests/test_severance_witnesses.py.proof.json" \
  --root . \
  --receipt "$RETURN_DIR/evidence/proof_witness_severance_repro.json"

python3 /tmp/proof_integrity_gate_r1.py witness \
  "$RETURN_DIR/tests/test_later_action_consumer.py.proof.json" \
  --root . \
  --receipt "$RETURN_DIR/evidence/proof_witness_consumer_repro.json"

echo ""
echo "== 3. Separate-process severance court =="
python3 "$RETURN_DIR/severance/run_severance.py" \
  --root . \
  --receipt "$RETURN_DIR/evidence/severance_receipt_repro.json"

echo ""
echo "== 4. Release gate (native ceiling) =="
python3 -c "
import sys; sys.path.insert(0, '$RETURN_DIR'); sys.path.insert(0, '.')
from candidate.release_gate import evaluate_release_gate
gate = evaluate_release_gate()
print('outcome:', gate.outcome.value)
print('holds:', len(gate.holds))
for hold in gate.holds:
    print(' -', hold.hold_code.value)
"

echo ""
echo "== C9P repro complete =="
