# PR697 receiving rehearsal R1

Engineering rehearsal only. Protects baseline
`8ffec40a6924848a49f95950aa9ce28c27ee3ec1`; candidate head
`da97d2624486b783bf5c4f465b17fdcdea3af20a`.

## Materialize exact candidate

```text
mkdir -p .local-logs/pr697-rehearsal/candidate
git archive da97d2624486b783bf5c4f465b17fdcdea3af20a \
  WORKER_COMMISSIONS/SOROK-20261105-S45-S47-CANONICAL-SOURCEFREE-PRODUCT-RECEIVING-R1 \
  WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1 \
  WORKER_RETURNS/SOROK-S45-S47-PROJECTION-20261105-R1 \
  WORKER_RETURNS/SOROK-S45-S47-CAUSAL-HARNESS-20261105-R1 \
  | tar -x -C .local-logs/pr697-rehearsal/candidate
```

## Run in fresh process

```text
cd .local-logs/pr697-rehearsal/candidate/WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product
env -u PYTHONPATH -u S37_JOIN_E_RETURN -u S37_LANGUAGE_RETURN \
  -u S37_S36_RETURN -u S37_M35_RETURN -u M35_JOIN_E_RETURN \
  -u M35_BP2_VENDOR -u SOROK_S45_S47_PROJECTION_ROOT \
  python3 -I -B run_s45_s47.py manifest
env -u PYTHONPATH -u S37_JOIN_E_RETURN -u S37_LANGUAGE_RETURN \
  -u S37_S36_RETURN -u S37_M35_RETURN -u M35_JOIN_E_RETURN \
  -u M35_BP2_VENDOR -u SOROK_S45_S47_PROJECTION_ROOT \
  python3 -I -B run_s45_s47.py demo --root ../../../..//runs --keep
```

First actual consuming command:

```text
python3 WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/run_s45_s47.py new --state <path>
python3 WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/run_s45_s47.py view --state <path> --text
```

## Evidence

- `evidence/rehearsal.json` — combined PASS checks.
- `evidence/changed_path_allowlist.json` — 497 additions only.
- `evidence/merge_tree.json` — merge-tree compatibility.
- `evidence/candidate_materialization.json` — 497/497 exact.
- `evidence/manifest.json`, `manifest_audit.json` — 424/424 source audit.
- `evidence/import_audit_scan.json` — zero external modules.
- `evidence/demo.json`, `evidence/causal_harness.json` — fresh-process runs.
- `evidence/projection_tests.xml` — 11 passed.
- `evidence/cli/` — user-facing CLI receipts.

Full logs remain in `.local-logs/pr697-rehearsal/`.
