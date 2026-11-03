# PDEV01 GAP-007 independent integration review

## Verdict

**REVISE**

The core 210/630/840 binding and execution claims are reproduced, but the exact
candidate is **not cold-replayable**: source, C11 release, 210 bound query refs,
BatchManifest ref and I05 compilation ref change between two independent runs.
The committed `actual_trace.json` is not reproduced by the exact candidate.

## Candidate and scope

- Branch: `review/pyat-pdev01-gap007-r1`
- Startup/candidate: `6a305523074898dda9c75e3e24fb6ea6fa2eeb40`
- Candidate read-only; no candidate or production edit.
- Sourcefree synthetic TEST_ONLY engineering; no original data, source rights,
  science, merge, CI, actor or wake.
- Write scope: `WORKER_RETURNS/PDEV01-GAP007-INDEPENDENT-REVIEW/**`.

## Reproduced core claims

- P1 operation identity preserved: `original_plan_ref == bound_plan_ref`
  (`e0d4180c…`), 840 operations.
- One-to-one binding within each run:
  - 210 DISTRIBUTION operations
  - 210 distinct bound query refs
  - 210 distinct Batch units
  - 840 distinct original operation refs
- Complete disjoint accounting:
  - 210 `BOUND_I03_QUERY`
  - 630 `TYPED_REFUSAL`
  - `CONDITIONAL=210`, `JOINT=210`, `HETEROGENEITY=105`,
    `RECURSIVE_BRANCH=105`
  - 630 refusal reason:
    `P1_OPERATION_KIND_HAS_NO_EXACT_CURRENT_I03_BINDING`
- Actual I03/Batch outputs in both runs:
  - 210 receipts
  - 210 `COMPLETED`
  - 210 result refs
  - 210 facts `SUPPORTED`
- Wrong-release refusal is exact:
  `BatchIntegrityError: exact C11 release unavailable; no latest/default/fuzzy/nearest fallback`.
- Wrong-authority/query refusal is exact:
  `CarrierExecutionBindingError: query_ref exact preimage unavailable; no latest/default/fuzzy/hash-inversion fallback`.
- I05 is separate from P1 binding:
  - independent Q00A/Q00B inventory and governed frontier
  - `ExactBoundedDiscoveryResult`, 16 receipts, 30 facts, 16 candidates
  - no I05 operation in the 840 P1 accounting
- Single synthetic carrier reuse: yes. All 35 roster/wave entries receive the
  same one synthetic `C11LogicalRelease`; all 210 bound units use that release.
  This is TEST_ONLY synthetic-carrier reuse, not per-wave source independence.

## Measured failure

The candidate's source construction is time-dependent:

- Committed trace source SHA: `443ebf5c74ad119fed2f79e148146e8772ad6f12317dcfcfcbe014136bf27eb4`
- Independent run 1 source SHA: `bb1311528841379cbb26d5bb8dec766c6a5e7efd9533a01d51bf4e1449fea082`
- Independent run 2 source SHA: `c940318ed53daf89beb4037bd28d07403f615c54a3133173d32360a57633223a`
- Release refs also differ:
  `383716e4…`, `fc90ac68…`, `d7839194…`
- All 210 bound job refs differ between runs and from the committed trace.
- BatchManifest refs differ: `d48c70f1…`, `2844168d…`, `c8846c5a…`
- I05 compilation refs differ: `4d9dc83d…`, `bbb9d7a4…`, `1d4a24d8…`

Cause: `replay_repair.py` writes a fresh synthetic SAV through
`write_rows`/`pyreadstat.write_sav`. The SAV header timestamp changes with time.
A control with byte-identical 12×2 rows/columns written two seconds apart
produced different source hashes and differed in **1 byte at offset 108**.

The candidate's `test_repair.py` passes 5/5 because it reads the committed
`actual_trace.json`; it does not cold-replay the source or exact identities.

## Smallest repair

1. Freeze the synthetic source bytes or make the SAV header deterministic at a
   pinned source SHA.
2. Regenerate `actual_trace.json` from that frozen source.
3. Add a two-run cold-replay assertion covering source SHA, release ref, all 210
   bound query refs, BatchManifest ref, and I05 compilation ref.
4. Re-run the 210/630/840, Batch and refusal checks. Do not change P1 operation
   identities or production owners.

## Exact commands

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 WORKER_RETURNS/PDEV01-GAP007/repair/replay_repair.py \
  > WORKER_RETURNS/PDEV01-GAP007-INDEPENDENT-REVIEW/evidence/replay_repair_observed.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 WORKER_RETURNS/PDEV01-GAP007/repair/replay_repair.py \
  > WORKER_RETURNS/PDEV01-GAP007-INDEPENDENT-REVIEW/evidence/replay_repair_observed_2.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m pytest \
  WORKER_RETURNS/PDEV01-GAP007/repair/test_repair.py -q -o addopts=''
```

Observed candidate test: **5 passed**.

## Limits

- Verdict is REVISE for exact cold replay/source identity, not for the core
  within-run 210/630/840 counts.
- No original data, source rights, scientific result, N5/N6, N9/N11/N12, actor,
  CI, merge or wake is claimed.
- The single synthetic carrier is not evidence of independent per-wave source
  identity.
