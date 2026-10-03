# PYAT HQ196 — R9 warrant/accounting successor structure — R1

Repository: `maidiu/rawlsing`

Role: **RABOCHII / DOCUMENTARY INSTRUMENT IMPLEMENTER — SPACE BUNNY**

Branch:
`agent/rabochii-pyat-hq196-r9-warrant-accounting-successor-r1`

Documentary base:
`d43756fb3c80645ac887cca90026ecbdb10dd18c`

Checkout mode:
`SPARSE_REQUIRED`

Sparse materialization manifest:
- `/WORKER_COMMISSIONS/PYAT-HQ196-R9-WARRANT-ACCOUNTING-SUCCESSOR-R1/`
- `/WORKER_RETURNS/PYAT-HQ196-R9-WARRANT-ACCOUNTING-SUCCESSOR-R1/`
- `/PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/HQ196_R9_THREE_WAY_ADJUDICATION_R1.md`
- `/PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/OPS-04/R9-WARRANT-ACCOUNTING-SUCCESSOR-R1/`

Exact startup SHA is supplied by HQ after this commission commit.

Do not clone.
Do not materialize full repo.
Read historical warrant/freeze artifacts with exact `git show`.

## Mission

Repair DQ-01 and produce a new **unsigned, unissued, non-authorizing** warrant/accounting successor structure that accurately represents the now-settled two-stage O1-C07 law.

Do not attempt to close technical accounts by invention.

## Governing law

Accepted HQ196 interpretation:
- expected budgets + instrumentation/basis are frozen pre-launch;
- exact observed counts are measured during execution and retained on return;
- literal path opens are separate from reader/decoder counts;
- no proxy relabeling.

Historical inputs:
- C4B unsigned template `c2af4f61d68e9803af83f8e26f633acfe31062fa`;
- C4 warrant candidate `8ff40d37de69db2d8a6053a7c2242f481677f1a4`;
- O1-C07 law at same freeze;
- HQ190-C, HQ191, HQ192, HQ195 returns.

## DQ-01 repair

Restore a per-source `source_access_accounting` block for all seven fresh-read sources.

For each account, represent separately where applicable:
- account name;
- expected/pre-launch budget or exact expectation;
- budget type: EXACT / MAX / ZERO / FLOOR / UNBOUND_PENDING_TECHNICAL_ACCEPTANCE;
- instrumentation/measurement mechanism;
- measurement basis fields:
  - what measured;
  - layer;
  - mechanism;
  - point in run;
- runtime observed count placeholder;
- observed-count status;
- stop condition if budget exceeded;
- provenance.

Do not merge expected budget and observed count into one ambiguous field.

## Bind only frozen values

Bind values already frozen by authority, including:
- retries=0 for all seven;
- selected_reads=1 and full_reads=0 for SRC02/SRC06/SRC14;
- metadata/selected/full expectations where explicitly frozen for SRC08/SRC12/SRC26;
- SRC26 header-prefix bytes=176 at its declared account;
- SRC27 exactly one full Route-B pass, max one, zero retry, while preserving its lower-layer accounts separately;
- SRC35 remains excluded fresh_reads=0 and is not one of the seven fresh-source warrant entries.

Do NOT turn SRC27 floors into ceilings except where authority explicitly supplies a maximum.
Do NOT invent path-open, decoder-invocation or byte budgets not yet accepted.
Do NOT invent a selected-read count for SRC27.

Technical values depending on the broker implementation should be typed:
`PENDING_HQ196_BROKER_SELECTED_IMPLEMENTATION_ACCEPTANCE`

## Typed null discipline

A typed null may describe an unexecuted/unmeasurable RETURN metric only where the governing failure law allows it.

A typed null may not waive a mandatory pre-launch budget that the warrant must bind before execution.

Make that distinction machine-readable.

## Instrument status

Must remain:
- signed=false
- issued=false
- authorizes_access=false
- execution_authorized=false
- signatures/approvals unset
- locator placeholders unfilled

No locator search.

## Output

Create:
`PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/OPS-04/R9-WARRANT-ACCOUNTING-SUCCESSOR-R1/01_UNSIGNED_SUCCESSOR.json`

and an exact crosswalk.

Required return:
- `00_RETURN.md`
- `01_HISTORICAL_TO_SUCCESSOR_CROSSWALK.json`
- `02_PER_SOURCE_ACCOUNTING_SCHEMA.json`
- `03_BOUND_VALUES_AND_PENDING_VALUES.json`
- `04_ISSUANCE_BLOCKER_MATRIX.json`
- `05_INVARIANTS.json`
- `06_FINAL_DISPOSITION.json`

## Allowed dispositions

Exactly one:
- `WARRANT_ACCOUNTING_SUCCESSOR_STRUCTURE_READY__TECHNICAL_VALUES_PENDING`
- `WARRANT_SUCCESSOR_READY_FOR_INDEPENDENT_REVIEW`
- `MATERIAL_AUTHORITY_CONFLICT_FOUND`
- `STRUCTURE_CANNOT_REPRESENT_SETTLED_O1_C07_LAW`

This lane cannot close R9 or issue the warrant.

## Return law

Commit, push, re-fetch, verify remote == local.
Report substantive SHA and pushed tip separately.

Terminal:
`HQ196_R9_WARRANT_SUCCESSOR_RETURNED__HQ_REVIEW_REQUIRED`

## Holds

Zero source access, locator discovery, warrant issuance, live C4, production mutation, C7 or actor/person work.
