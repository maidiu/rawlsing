# COLD BUILDER HANDOFF — exact fresh-extraction commands

**Artifact:** `REPAIRED_PACKAGE.zip` in this return root. **Authority:** preparation artifact only, `PENDING_SAME_DISTINCT_C_RECHECK`; no native science, architecture selection, source/actor right, independent C or H1.

## Declared external anchors only

- Original ZIP: `/Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip`, SHA-256 `526d835d64a98c886a8cbb159fb39f06af7c287ebe1029a93fbbfc9131072332`, 280 entries.
- Shared Git object store: `/Users/matthewsmith/s2b-work/rawlsing`.
- No author worktree, parent copy, hidden fixture or undeclared path is required.

## Literal cold commands (run exactly)

```bash
set -e
WORK=$(python3 -c 'import tempfile; print(tempfile.mkdtemp(prefix="anvil-cold-"))')
unzip -q REPAIRED_PACKAGE.zip -d "$WORK"
cd "$WORK/ANVIL_R7/tools"

python3 r7_inventory.py verify \
  --source-root ../EVIDENCE/SOURCE_118 \
  --repo /Users/matthewsmith/s2b-work/rawlsing \
  --zip /Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip \
  --inventory ../EVIDENCE/SOURCE_IDENTITY_INVENTORY.json

python3 -m unittest test_r7_integrated -q
python3 test_integrated_strict.py

python3 r7_integrated.py FRAME ../EVIDENCE/FRAME.json \
  --evidence-root ../EVIDENCE --source-root ../EVIDENCE/SOURCE_118 \
  --repo /Users/matthewsmith/s2b-work/rawlsing \
  --zip /Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip

python3 r7_integrated.py DECISION ../EVIDENCE/DECISION.json \
  --evidence-root ../EVIDENCE --source-root ../EVIDENCE/SOURCE_118 \
  --repo /Users/matthewsmith/s2b-work/rawlsing \
  --zip /Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip

python3 r7_integrated.py C_INTEGRATED ../EVIDENCE/C.json \
  --evidence-root ../EVIDENCE --source-root ../EVIDENCE/SOURCE_118 \
  --repo /Users/matthewsmith/s2b-work/rawlsing \
  --zip /Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip

python3 r7_build.py verify ../EVIDENCE/DECISION.json \
  --evidence-root ../EVIDENCE --source-root ../EVIDENCE/SOURCE_118 \
  --repo /Users/matthewsmith/s2b-work/rawlsing \
  --zip /Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip \
  --out ../BUILT
```

Expected local statuses: inventory `PASS_SOURCE_IDENTITY_INVENTORY_S1_DOCUMENTARY`; 29 inherited tests OK; 11 closure tests OK; FRAME `PASS_LOCAL_COMMON_REQUIREMENTS_SOURCE_IDENTITY_NOT_NATIVE_AUTHENTICATED`; DECISION `PASS_LOCAL_INTEGRATED_DECISION_PENDING_C`; C `PASS_LOCAL_C_PACKET_ONLY_INDEPENDENCE_UNVERIFIED` with `C_HOLD_EXACT`; builder `PASS_SIX_PROJECTIONS_BYTE_IDENTICAL`.

## Sabotage / restore

`test_integrated_strict.py` mutates exact packet bytes and requires RED for C's W1–W6 plus inherited negative controls, then restores the source packet. `r7_build.py verify` refuses changed projections and passes only after byte-identical rebuild.

## Honest limits

No native SAV/DTA read, no dense 100k/600–1,300-slot, no process-tree ≤6 GiB, no 1/10/100 distinct-operation benchmark; no source/actor/science grant; no actual F1–F8/N9/N10W/SOROK first reader; no independent C or H1. Local receipts/human summaries can be forged by an evidence-root author; external runner/source-owner custody remains required. F26 exact caller/invalidation remains the existing K3 `K1-CAP-24` / `P4R-R02` / `PYAT-PC-R11-21` hold.
