# HQ196-R1 Return — R9 warrant/accounting successor structure

**Disposition:** `WARRANT_ACCOUNTING_SUCCESSOR_STRUCTURE_READY__TECHNICAL_VALUES_PENDING`
**Branch:** `agent/rabochii-pyat-hq196-r9-warrant-accounting-successor-r1`
**Startup SHA (verified exact):** `3e215413ead20bf62dd836f68eb22639ec873868`
**Documentary base:** `d43756fb3c80645ac887cca90026ecbdb10dd18c`
**Checkout mode:** `SPARSE_REQUIRED` — sufficient. No clone, no full materialisation.

This lane repaired a documentary instrument. It executed no source and closed no technical account.

---

## DQ-01 repaired

The C4 warrant candidate dropped C4B's per-source `source_access_accounting` block. I verified this
empirically from the exact git objects rather than taking it on faith:

| Object | Block present? |
|---|---|
| C4B template `c2af4f61d…` | **yes**, for all seven sources |
| C4 candidate `8ff40d37d…` | **no**, for all seven `per_source` entries |

**78 accounts** now exist across the seven fresh-read sources, each carrying:

- `account_name`, `layer`
- `expected_pre_launch_budget` — budget type + value/expression, `frozen_before_launch: true`
- `measurement_basis` — *what measured / layer / mechanism / point in run* (all four required)
- `runtime_observed_exact_count` — value, status, typed reason
- `stop_condition_if_exceeded`
- `provenance` — exact `artifact@commit:json.path` citations
- `pending_dependency` where a value awaits technical acceptance

The crosswalk accounts for all 78: **42 restored**, **7 restored-and-split**, **29 added by the
settled O1-C07 law**.

## The two stages are never merged

Stage 1 (pre-launch, frozen) holds budget + instrumentation + basis. Stage 2 (during run, measured)
holds the exact observed count, retained on return. These live in separate objects on every account —
asserted by `INV-STAGES-SEPARATE`.

This matters because `REQUIRED_EXACT_COUNT` means the *budget* must be exact before launch. It does
**not** mean the observed number must already have been observed before launch.

## What I bound — and what I refused to bind

**Bound (40 accounts):** 18 EXACT, 11 ZERO, 11 FLOOR.

- `retries = 0` (ZERO) for all seven
- SRC02/SRC06/SRC14: `selected_column_reads = 1` (EXACT), `full_reads = 0` (EXACT)
- SRC08/SRC12: `metadata_reads = 1` (EXACT); selected/row-data/selected-columns all `0` (ZERO)
- SRC26: `header_prefix_bytes = 176` (EXACT) at its own account
- SRC27: `governed_full_route_passes = 1` (EXACT; authority also supplies max 1)
- SRC35: `fresh_reads = 0`, excluded from the seven

**Refused to bind (38 accounts), typed `UNBOUND_PENDING_TECHNICAL_ACCEPTANCE`:** path opens,
existence checks, header-prefix reads, decoder invocations and byte counts on the six non-SRC27
sources; plus SRC27's path opens, selected reads, header-prefix reads, decoder invocations and bytes.

Two judgement calls worth flagging:

1. **SRC26's three numbers are not a contradiction.** `176` is the header-prefix **byte** account.
   `174` (raw nominal case size) and `332` (decoded dictionary width) are separate geometry accounts,
   both `equality_required: false`, with the divergence law preserved verbatim. They are never collapsed.
2. **SRC27's "exactly one pass" is a workload constraint, not an access budget.** The hardened note's
   *"will require at minimum"* wording supplies **FLOORs** for existence checks, hash passes, metadata
   reads and full reads. Those are bound as `FLOOR 1` and **not promoted to ceilings**, because no
   maximum is supplied. Authority's word *"multiple"* for SRC27 path opens is recorded verbatim and
   deliberately **not** numerified. No selected-read count was invented for SRC27.

I also caught myself over-constraining: I initially bound SRC26's header-prefix *read count* as
`EXACT 1`, but authority supplies only the *byte* count. It is now `FLOOR 1` with
`reviewer_confirmation_required: true`, consistent with the other derived minimums.

## Typed-null discipline, machine-readable

```json
"return_metric_null_permitted": true,
"return_metric_null_requires_typed_reason": true,
"pre_launch_budget_null_permitted": false,
"pre_launch_budget_unsupplied_representation": "UNBOUND_PENDING_TECHNICAL_ACCEPTANCE",
"pre_launch_budget_absent_representation_prohibited": true
```

All 78 return metrics are `null` with typed reason
`NOT_EXECUTED__UNSIGNED_UNISSUED_NON_AUTHORIZING_INSTRUMENT`, each marked
`must_not_be_read_as: "a zero, an empty result, or a PASS"`.

No pre-launch budget is null or absent. An unsupplied budget is a **typed blocker that waives
nothing** — which is the whole point of the distinction.

## Status unchanged

`signed=false`, `issued=false`, `authorizes_access=false`, `execution_authorized=false`. Both
approvals `UNSET`. All seven locator placeholders unfilled. **No locator search performed.**

## Verification

**23 asserted invariants, 23 passing, 0 failing** — executed against the emitted instrument by
`hq196_successor_model.check_invariants`, not asserted narratively. The suite caught two real defects
during construction: a wrong provenance constant, and an invariant that wrongly flagged the intended
`UNBOUND` representation. Both were fixed at source.

Totals: 78 accounts — 40 bound, 38 pending; 37 pending on
`PENDING_HQ196_BROKER_SELECTED_IMPLEMENTATION_ACCEPTANCE`, 1 on `R9-SEL-03`.

## Still open

- **R9-SEL-03** — frozen `selected_reads=1` for SRC02/SRC06/SRC14 has **no implementation owner**;
  the bound reader exposes no `usecols`. The budgets stay bound at `EXACT 1`. A missing owner is a
  blocker, not grounds to relax the budget.
- **R9-BROKER-ACCEPT** — 38 accounts await implementation acceptance.
- Seven locators unfilled; both approvals UNSET; independent integration review incomplete.

Restoring the accounting fields closes **DQ-01 only**. It closes no technical account and authorizes
nothing. This lane cannot close R9 and cannot issue the warrant.

## Artifacts

**Output** — `PYAT_CONTROL_ROOM/.../OPS-04/R9-WARRANT-ACCOUNTING-SUCCESSOR-R1/`
`01_UNSIGNED_SUCCESSOR.json` · `02_C4B_TO_SUCCESSOR_ACCOUNTING_CROSSWALK.json`
plus the reproducible generators `hq196_successor_generator.py`, `hq196_successor_model.py`,
`hq196_emit.py`.

**Return** — `WORKER_RETURNS/PYAT-HQ196-R9-WARRANT-ACCOUNTING-SUCCESSOR-R1/`
`00_RETURN.md` · `01_HISTORICAL_TO_SUCCESSOR_CROSSWALK.json` ·
`02_PER_SOURCE_ACCOUNTING_SCHEMA.json` · `03_BOUND_VALUES_AND_PENDING_VALUES.json` ·
`04_ISSUANCE_BLOCKER_MATRIX.json` · `05_INVARIANTS.json` · `06_FINAL_DISPOSITION.json`

## Recommended next step for HQ

Hostile review of the crosswalk and the floor/ceiling discipline — specifically the derived minimums
flagged `reviewer_confirmation_required`. Then commission the brokered selected-reader implementation
so the 38 pending values can be bound.

`HQ196_R9_WARRANT_SUCCESSOR_RETURNED__HQ_REVIEW_REQUIRED`
