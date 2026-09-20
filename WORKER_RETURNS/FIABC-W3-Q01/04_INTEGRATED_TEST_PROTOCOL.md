# FIABC-W3-Q01 — Integrated Qualification Protocol

This packet is deterministic and intentionally does not perform architecture discovery.

## Phase 0 — fan-in prerequisite

Run this protocol only on the HQ/browser integrated Wave-3 tree after I01-I08 and Q01 are fanned in. Confirm the integrated commit descends from Wave-2 HQ fan-in `56697a27e94eb9603dfa412a15ab8f1feb819b0c` and that frozen candidate-owner refs have not been rewritten.

STOP if the integrated tree does not contain the complete sibling return set or if any sibling return reports a blocker relevant to its own obligation.

## Phase 1 — Q01 contract self-test

```bash
python -m unittest discover -s WORKER_RETURNS/FIABC-W3-Q01/tests -p 'test_*.py' -v
```

Expected result: every PASS control is accepted and every negative fixture is rejected with its exact expected code. This proves the review contract is executable; it does **not** prove sibling implementations conform.

STOP on any failure.

## Phase 2 — sibling focused tests

Run every focused test command declared in `WORKER_RETURNS/FIABC-W3-I01/00_RETURN.md` through `FIABC-W3-I08/00_RETURN.md`. Do not replace a sibling's declared test with a weaker smoke test. Record command, integrated commit, exit status and test count.

STOP if any focused test fails, is skipped because a required fan-in file is absent, or silently substitutes a fixture for a production object.

## Phase 3 — exact evidence projection into Q01 dimensions

For each sibling, construct a read-only qualification witness from its real integrated implementation/receipts. The witness must contain only evidence already produced by the sibling or common court; it must not mint new semantic facts. Validate the evidence dimensions from `03_ACCEPTANCE_CRITERIA.md`:

- I01 -> `diagnostic`
- I02 -> `effective_n`
- I03 -> `candidate_c`
- I04 -> `packaging`
- I05 -> `oracle`
- I06 -> `accounting`
- I07 -> `succession`
- I08 -> `terminal`

An adapter is allowed only to rename/reshape already-existing receipt fields for the test. It may not infer a missing authority, fabricate a missing live receipt, recompute expected truth from a candidate, convert null to zero, or weaken a typed state.

STOP on the first Q01 rejection. Preserve the rejection code and exact originating evidence refs.

## Phase 4 — repository/static identity checks

Before any local source is opened, verify at minimum:

- no `CACC3` production/configuration path exists;
- no WVS-specific Candidate-C accelerator exists;
- LiTS q310 and q311 remain in the fixed workload;
- accepted packaging blobs match `03_ACCEPTANCE_CRITERIA.md`;
- frozen candidate owner commit is still `0b96b8de9aac774566f872cf0630ebd4ddeb70e6` where experimental identity requires it;
- current-tree B blob `c3647800f52fa81fdef34be6692207e092c48ee2` has not silently replaced frozen B blob `7c509c2098d0030f253344eb3f682471378812a8`;
- succession preflight requires live consumption, not only repository presence;
- final verifier requires full I05 terminal rather than C11/I03.

STOP on any mismatch.

## Phase 5 — browser-safe tests versus later local tests

Browser/GitHub-safe qualification includes source-code/static identity review, return-local fixture tests if a GitHub execution surface is available, and tests that do not open survey source bytes.

The following remain later local/runtime work and must not be fabricated here:

- WVS candidate-neutral parity-oracle source materialization from exact WVS bytes;
- LiTS/WVS source-opening execution that depends on local protected survey files;
- R6X stopped-ledger reconciliation requiring the real integrated runtime;
- process/RSS/I/O/scratch/lifecycle telemetry tests that require actual OS process/file activity;
- any six-cell P2X execution or measurement.

## Phase 6 — premeasurement stop law

Measured P2X is still unlawful unless all of the following are true on the same integrated commit:

1. I01-I08 focused tests PASS;
2. Q01 negative-path qualification PASSes against the real integrated receipts;
3. exact packaging/candidate identities PASS;
4. WVS and LiTS independent oracles are materially frozen as required and oracle independence PASSes;
5. six source×candidate capability is positively qualified or a competent premeasurement court has changed scope before execution;
6. succession preflight emits exact PASS;
7. equal-work accounting preflight emits exact PASS;
8. final verifier contract is configured to require full I05 terminal and the independent receipts rather than synthesize them;
9. all local-only qualification work specified by Q02 completes without a new blocker.

If any condition is absent, preserve the typed blocker and stop. Do not assign zeros, omit a cell, shorten a workload, switch candidate identity, or infer a missing authority to obtain a rectangular result.
