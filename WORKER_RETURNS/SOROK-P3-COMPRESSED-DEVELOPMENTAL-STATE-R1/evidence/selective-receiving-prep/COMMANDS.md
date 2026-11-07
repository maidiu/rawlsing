# Commands — selective receiving preparation

All commands below were read-only. No proposed receiving branch, PR, protected ref or code/test file was created or changed.

## Exact pins observed

```bash
git ls-remote --heads origin \
  refs/heads/integration/pre-main-reconciliation-r1 \
  refs/heads/agent/sorok-p3-compressed-developmental-state-20261106-r1 \
  refs/heads/main
```

Result:

```text
c852d7516e23fcb6cf2215e9be7c5fa268503516  refs/heads/integration/pre-main-reconciliation-r1
16275d03fc4724a694c48ed9d447c4eeadbe25f2  refs/heads/agent/sorok-p3-compressed-developmental-state-20261106-r1
25830fe7462bb9e29bc4087e6ae14f3f84cec377  refs/heads/main
```

`main` is an older ancestor and is not the P3 receiving base.

## Candidate delta inspection

```bash
git diff --name-status c852d7516e23fcb6cf2215e9be7c5fa268503516..16275d03fc4724a694c48ed9d447c4eeadbe25f2
git diff --stat c852d7516e23fcb6cf2215e9be7c5fa268503516..16275d03fc4724a694c48ed9d447c4eeadbe25f2
git rev-list --count c852d7516e23fcb6cf2215e9be7c5fa268503516..16275d03fc4724a694c48ed9d447c4eeadbe25f2
```

Observed: 30 commits, 292 changed paths.

## Dependency and code/test identity checks

```bash
# Base presence and exact hashes are recorded in DEPENDENCY_CHECK.json.
git cat-file -e c852d7516e23fcb6cf2215e9be7c5fa268503516:WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/contracts.py
git cat-file -e c852d7516e23fcb6cf2215e9be7c5fa268503516:WORKER_RETURNS/SOROK-S45-S47-PROJECTION-20261105-R1/s45_projection/projection.py
git cat-file -e c852d7516e23fcb6cf2215e9be7c5fa268503516:WORKER_RETURNS/SOROK-P2-PRODUCT-FANIN-20261105-R1/p2_product_fanin/integration.py

# E1 B1 is absent at base and is the exact included dependency.
git cat-file -e c852d7516e23fcb6cf2215e9be7c5fa268503516:WORKER_RETURNS/SOROK-P3-E1-DEVELOPMENTAL-ABI-RECONNAISSANCE-R1/probe/vendor/B1/bfirst.py || true
git show 16275d03fc4724a694c48ed9d447c4eeadbe25f2:WORKER_RETURNS/SOROK-P3-E1-DEVELOPMENTAL-ABI-RECONNAISSANCE-R1/probe/vendor/B1/bfirst.py | shasum -a 256
```

Expected B1 SHA-256:

```text
478b989730f49a5def41a367b6f53e4aae9c80961f7f466fe669c7dbd92201a3
```

## Proposed branch construction — NOT EXECUTED

The receiving owner may construct the candidate only after the focused review accepts exact `16275d03`. The path list is `SELECTIVE_PATHS.txt`.

```bash
set -euo pipefail
BASE=c852d7516e23fcb6cf2215e9be7c5fa268503516
CAND=16275d03fc4724a694c48ed9d447c4eeadbe25f2
BRANCH=codex/sorok-p3-selective-receiving-20261107-r1

git fetch origin integration/pre-main-reconciliation-r1
git switch -c "$BRANCH" "$BASE"
xargs -a WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/evidence/selective-receiving-prep/SELECTIVE_PATHS.txt \
  git checkout "$CAND" --

git diff --cached --check
git diff --cached --name-only | sort > /tmp/p3-selective-actual.txt
```

Verification against the inventory (run from repository root):

```bash
python3 - <<'PY'
import json
from pathlib import Path
root = Path("WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/evidence/selective-receiving-prep")
inventory = json.loads((root / "SELECTIVE_INVENTORY.json").read_text())
expected = {row["path"] for row in inventory["included"]}
actual = set(Path("/tmp/p3-selective-actual.txt").read_text().splitlines())
assert actual == expected, (sorted(actual - expected), sorted(expected - actual))
print("selective checkout matches", len(expected), "inventory paths")
PY
```

Do not commit or push the proposed receiving branch until the nonauthor review accepts exact `16275d03`. Do not merge or move protected PRE-MAIN from this preparation.
