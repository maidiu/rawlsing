# FIABC-T5 — Live I07 Succession Preflight Binding

## Accepted implementation

T5 transposes the accepted Wave-3 I07 implementation byte-exact:

- `rawlsing_next/fiabc_succession_preflight.py`
  - blob `e9591b3f4beba3a5aa35039edc85163635582959`;
- exact B05 schema blob `484678375abcdd94151b72b425629ccb535be5eb`;
- governing profile blob `57effa49428f8274cf7ca73e8442f75cca1b8267`.

No semantic ownership is moved into T5.

## Governing succession chain

Every comparison-required obligation must close:

`INHERITED OBLIGATION`
→ `ACCEPTED AUTHORITY`
→ `CURRENT AUTHORITATIVE OWNER`
→ `EXECUTABLE BINDING`
→ `LIVE CONSUMER`
→ `A/B/C INVARIANT CLASS`
→ `COST OWNER`.

Repository presence does not satisfy the live-consumer edge.

A historical receipt may establish genealogy/provenance but cannot become a current execution receipt merely by existing.

## Exact current six-cell law

T5 consumes:

`WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json`.

Required current cells are exactly:

- LITS_I/A;
- LITS_I/B;
- LITS_I/C;
- WVS7/A;
- WVS7/B;
- WVS7/C.

The current T5 machine contract rejects any missing seventh/sixth-shape drift and explicitly rejects the old LiTS-C or WVS-C failure receipt as a current capability ref.

## Frozen inherited identities

The T5 machine contract pins the exact live identities inherited from T1-T4.

This gives I07 a stable current-court envelope, but it does **not** substitute for I07's live evidence chain.

The real succession manifest must still supply exact immutable refs and governed live-consumer receipts for all required F001-F036 obligations.

## Driver preflight

The live driver adds:

- `--current-court-contract`;
- `--succession-manifest`;
- `--succession-lifecycle-context`;
- `--succession-preflight-receipt`.

`--preflight` executes accepted I07 against the supplied real sealed manifest/lifecycle context.

A T5 wrapper receipt is emitted only after I07 PASS and binds:

- current repo head;
- manifest identity;
- evaluated-manifest identity;
- lifecycle-context SHA;
- T5 current-court contract SHA;
- pre-candidate state.

`--run` and `--resume` verify that exact receipt and refuse stale-head substitution.

## T4 accounting closure

The current T5 court contract requires the live T4 accounting surfaces:

- T3 process-isolation provenance;
- write-once telemetry semantics;
- actual lifecycle actions;
- typed-null missing telemetry;
- preserved-work classification;
- exact source/candidate/process/action identities.

Accepted I07 P09 still requires real governed accounting evidence.

At S16, T5 additionally consumes the actual live T4 accounting receipt, verifies the write-once telemetry receipt exists and matches its SHA, and refuses a semantic/oracle PASS without that accounting closure.

## Fail-closed conditions

Preflight remains BLOCK when, among other conditions:

- required authority is missing/stale;
- current owner is unresolved;
- binding does not match owner;
- repository presence lacks live consumption;
- negative-state law collapses;
- oracle is not independent/pre-output frozen;
- one of six capabilities is missing;
- synthetic realization substitutes for production capability;
- accounting is unresolved;
- process attribution is not candidate-local;
- lifecycle/failure-scope context is absent or stale.

No warning/partial state is upgraded to PASS.
