# FIABC-T3 — Execution Order Diff

## Before T3

The T2 live backend inherited the old P2X S03 defect:

1. a candidate process could already have produced candidate-owned state;
2. S03 assigned a local `oracle_frozen` event;
3. S03 synthesized an oracle identity from source labels/hashes;
4. S03 invoked the same candidate I03 twice;
5. equality of those two self-replays was mapped onto semantic, ExactRef, replay, fail-closed, and typed-negative parity dimensions.

That proved self-determinism, not independent expected truth.

The live driver also permitted direct selection of the candidate backend, so process isolation was not structurally mandatory.

## After T3

### Driver boundary

For `--run` or `--resume`:

1. load the T2 current execution manifest;
2. load and validate the frozen upstream receipt;
3. bind each current manifest source to its canonical source root;
4. verify source-identity authority and independent-oracle identity are present;
5. verify freeze order:
   - source identity;
   - authority/workload;
   - oracle materialization/freeze;
6. export the exact receipt path for the neutral process adapter;
7. reject any backend other than `rawlsing_next.ee_p2x_process_isolated_backend`;
8. only then import the neutral adapter and enter the court run.

### Cell boundary

For each executable source×candidate cell:

1. validate the candidate-neutral freeze receipt again;
2. verify the cell source equals the receipt's `source_id`;
3. verify `canonical_source_sha256` equals the StageContext source root;
4. verify the source has a frozen independent oracle identity;
5. validate cell root/cold-or-explicit-resume conditions;
6. take the parent candidate-envelope start timestamp;
7. write the exact cell owner marker;
8. spawn a fresh child process;
9. import the actual candidate backend only inside that child;
10. reject any pre-existing session registry or foreign candidate owner state.

### Backend causal order

Before any non-court candidate handler executes, `_gate(...)` binds the already-frozen upstream oracle into cell state with pre-process ordinal 0.

The current stage labels then mean:

- S01: candidate preparation where current execution requires it;
- S02: C11 reachability;
- S03: **pre-frozen oracle identity binding check only**;
- S04: I03 execution;
- S05: I05 learned production;
- S06–S16: later lifecycle/accounting surfaces;
- S17: terminal verification.

S03 no longer executes I03 and no longer creates parity truth.

The semantic causal sequence is therefore:

`SOURCE IDENTITY FREEZE`
→ `AUTHORITY/WORKLOAD FREEZE`
→ `INDEPENDENT ORACLE MATERIALIZE/FREEZE`
→ `FRESH CELL PROCESS START`
→ `C11`
→ `I03`
→ `I05`
→ `LIFECYCLE`
→ `TERMINAL VERIFICATION`.

The retained S03 label is an assertion point, not a new computation inserted between C11 and I03.

## Fail-closed transition

T3 sets the old parity dimensions to:

`PENDING__POST_I05_INDEPENDENT_ORACLE_COMPARISON`

rather than manufacturing PASS.

Consequently, the existing terminal metric gate cannot lawfully complete until the downstream comparison layer consumes the complete I03/I05 observation and produces the real independent-oracle match receipt.

This is intentional: T3 transposes the freeze and process boundary without stealing the next layer's terminal/comparison burden.
