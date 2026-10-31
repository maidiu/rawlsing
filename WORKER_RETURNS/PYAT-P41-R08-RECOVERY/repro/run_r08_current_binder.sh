#!/usr/bin/env bash
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
RETURN=$(cd "$HERE/.." && pwd)
REPO=${REPO_ROOT:-$(git -C "$RETURN" rev-parse --show-toplevel)}
CURRENT=8e44ca9c751049d65e6def47600b5c073ee04b29
BINDER_COMMIT=80bb8c18241ebcd7ddbe559b76c6b39a72025b89
FIXTURE_COMMIT=d8a7b4005d23a1e39b35360ca96bf2aef5b9e591
REVIEW_COMMIT=2937966b3fc2388c8853bce2b984fb0cbfcdfa12
WORK=${WORK:-$(mktemp -d "${TMPDIR:-/tmp}/r08-current.XXXXXX")}
trap 'rm -rf "$WORK"' EXIT
git -C "$REPO" archive "$CURRENT" rawlsing_next | tar -x -C "$WORK"
git -C "$REPO" show "$BINDER_COMMIT:rawlsing_next/pre553_universal_evidence_binding.py" > "$WORK/rawlsing_next/pre553_universal_evidence_binding.py"
git -C "$REPO" show "$BINDER_COMMIT:rawlsing_next/tests/test_universal_evidence_binding.py" > "$WORK/rawlsing_next/tests/test_universal_evidence_binding.py"
git -C "$REPO" archive "$FIXTURE_COMMIT" WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2 WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R3 WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R8 | tar -x -C "$WORK"
mkdir -p "$WORK/probes" "$WORK/review"
git -C "$REPO" archive "$REVIEW_COMMIT" WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r8/probes | tar -x -C "$WORK/review"
cp "$WORK"/review/WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r8/probes/*.py "$WORK/probes/"
cd "$WORK"
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 -m pytest -q -p no:cacheprovider rawlsing_next/tests/test_universal_evidence_binding.py
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 -m pytest -q -p no:cacheprovider probes/test_r08v_r8_targeted_refusal_codes.py probes/test_r08v_r7_semantic_adapters.py
