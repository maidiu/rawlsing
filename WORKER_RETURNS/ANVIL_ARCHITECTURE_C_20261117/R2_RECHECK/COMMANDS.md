# R2 RECHECK — commands and logs

All commands were read-only against the candidate/product; writes are only
under `WORKER_RETURNS/ANVIL_ARCHITECTURE_C_20261117/R2_RECHECK/`.

## Exact target and manifest

```
cd /Users/matthewsmith/s2b-work/rawlsing
git rev-parse 06e88a5ac7e4c14362a97a046f44e25d8eec4162
git rev-parse anvil-architecture-candidate-20261117-r2^{tag}
git rev-parse anvil-architecture-candidate-20261117-r2^{}
git ls-remote origin refs/heads/agent/anvil-integrated-architecture-20261117-r1 \
  refs/tags/anvil-architecture-candidate-20261117-r2
git diff --stat cea2d4d3009e9087d2267e9d1f53bec28b730dc7 \
  06e88a5ac7e4c14362a97a046f44e25d8eec4162 -- rawlsing_next
```

Result: target `06e88…`, tag object `3f55b…` peels `06e88…`, remote exact,
product diff empty. 120/120 manifest hashes pass (0 missing, 0 bad).
Log: `RUNS/refs_target_manifest.txt`.

## Snapshot extraction

```
git archive 06e88a5ac7e4c14362a97a046f44e25d8eec4162 \
  WORKER_RETURNS/ANVIL_ARCHITECTURE_20261117 \
  | tar -x -C R2_RECHECK/snapshot
```

The snapshot is read-only reference. No author runner was executed against
author `RUNS/`.

## Supplement guard baseline

The full snapshot was extracted for the run below. After execution it was
reduced to `snapshot/PACKAGE_MANIFEST.target.json` and `snapshot/README.md` to
avoid duplicating the authoritative candidate; re-extract with the `git archive`
command above before rerunning.

```
cd R2_RECHECK/snapshot/WORKER_RETURNS/ANVIL_ARCHITECTURE_20261117
PYTHONDONTWRITEBYTECODE=1 python3 GUARDS/v2_supplementary_guard.py \
  --decision S2_S3/FINAL_DECISION.json \
  --addendum S1/FRAME_V2_ADDENDUM.json \
  --crosswalk S2_S3/FINAL_OBLIGATION_CROSSWALK.tsv \
  --evidence-root "$PWD" --source-root "$PWD/SOURCE_118" \
  --repo /Users/matthewsmith/s2b-work/rawlsing \
  --zip /Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip
```

Result: `PASS_V2_SUPPLEMENTARY_STRUCTURAL_20_REQUIREMENTS_118_IDENTITIES`
(accepted base guard 16/16, supplement total 20/118). Log:
`RUNS/v2_guard_baseline_independent.txt`.

## Independent negative mutations

Cases in `WITNESS/negatives/`; run with `RUNS/run_negative_cases.sh` or the same
guard command plus `--decision/--addendum/--crosswalk` overrides. Results:

- empty v2 addendum/dispositions/crosswalk: `REFUSE_V2_SUPPLEMENTARY`;
- stale PENDING dependency: `REFUSE`;
- stale SC-ESTATE name: `REFUSE`;
- stale SC-ESTATE effect: `REFUSE`;
- `selected_design.durable_index_status=SELECTED`: `REFUSE`;
- `selected_design.construction_one_journal_one_certificate=SELECTED_UNCONDITIONAL`:
  `REFUSE`;
- sequence-status-only `SELECTED` with the literal “durable locator index” /
  “one source-derived Q2 certificate” action text: **PASS** (disclosed residual
  guard literal gap; actual corrected statuses are conditional/held).

Summary: `RUNS/negative_summary.tsv`; individual logs:
`RUNS/negative_*.txt`.

## Restore

The unchanged baseline was run again after the negatives. Result: PASS 20/118.
Log: `RUNS/v2_guard_restore_independent.txt`.

## Focused tests

Not rerun. `git diff cea2d4d..06e88 -- rawlsing_next` is empty; product source is
unchanged. R1’s focused sourcefree run (34 passed) and the direct prepared
3-test evidence remain separately identified; no native/100k inference.
