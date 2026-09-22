# FIABC FINAL LOCAL LAUNCH PACK — R1
## Measured six-cell court launch

### Current holding

The repository contains a single driver command that, once its pre-candidate artifacts and current-head seams are lawfully repaired, executes the six current cells serially on one host. **It is not lawful to run that command at audited head `858b3b52674044e020b85f8697c5f2c61ce15371` because the blockers in `05_BLOCKERS_IF_ANY.md` are unresolved.**

Do not run measured P2X merely because the CLI exists.

### Exact existing driver command shape after repair + regenerated launch pack

Assumptions supplied by the repaired pre-candidate pack:

- working checkout is the required existing P2X execution branch fast-forwarded to the exact sealed launch head;
- `LITS_PATH` and `WVS_PATH` name the exact canonical source files;
- `WORK_ROOT` is the same isolated court root used for preflight;
- `FROZEN_UPSTREAM_RECEIPT` is the validated final two-source T3 freeze receipt;
- `$WORK_ROOT/court/fiabc_t5_succession_preflight.json` is the PASS current-head T5/I07 preflight receipt.

```bash
set -euo pipefail

python rawlsing_next/ee_p2x_darwin_court_driver.py \
  --run \
  --continuation-map WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json \
  --current-court-contract WORKER_RETURNS/FIABC-T5/04_CURRENT_SIX_CELL_COURT_CONTRACT.json \
  --succession-preflight-receipt "$WORK_ROOT/court/fiabc_t5_succession_preflight.json" \
  --frozen-upstream-receipt "$FROZEN_UPSTREAM_RECEIPT" \
  --backend-module rawlsing_next.ee_p2x_process_isolated_backend \
  --work-root "$WORK_ROOT" \
  --repo-root "$PWD" \
  --lits-path "$LITS_PATH" \
  --wvs-path "$WVS_PATH"
```

This is one driver process with a repository/working-root lock. Candidate work is source-order then A/B/C order from the current manifest. Each source×candidate cell is delegated to the process-isolated backend. Progress is emitted to stderr; the machine run result is stdout JSON.

If an interrupted run has a lawful durable ledger and all static/pre-candidate identities remain unchanged, the existing resume form is:

```bash
python rawlsing_next/ee_p2x_darwin_court_driver.py \
  --resume \
  --continuation-map WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json \
  --current-court-contract WORKER_RETURNS/FIABC-T5/04_CURRENT_SIX_CELL_COURT_CONTRACT.json \
  --succession-preflight-receipt "$WORK_ROOT/court/fiabc_t5_succession_preflight.json" \
  --frozen-upstream-receipt "$FROZEN_UPSTREAM_RECEIPT" \
  --backend-module rawlsing_next.ee_p2x_process_isolated_backend \
  --work-root "$WORK_ROOT" \
  --repo-root "$PWD" \
  --lits-path "$LITS_PATH" \
  --wvs-path "$WVS_PATH"
```

### Court law preserved by the existing driver

- cells: LiTS-I/A, LiTS-I/B, LiTS-I/C, WVS7/A, WVS7/B, WVS7/C;
- one physical host and one driver lock;
- no direct candidate backend;
- frozen oracle before candidate execution;
- parity admission before performance;
- candidate-local failures do not suppress later lawful cells;
- S17 success verifier runs only when the six-cell success prerequisites are satisfied;
- measured synthesis is not performed by the driver;
- P3/final carrier selection is downstream and must not begin before this court terminal.

### Embargo

A command being syntactically present is not launch authorization. The current pack is PASS under commission law **B**, not law A. Repair the exact blockers, seal a new launch head, re-run source-free qualification, regenerate the current-head T3/I07 receipts, and only then use the command above.
