# FIABC-W3-Q01 — Hostile Cross-Implementation Qualification

Worker: `FIABC-W3-Q01`

Repository: `maidiu/rawlsing`

Branch: `agent/rabochii-premain-fiabc-w3-q01-hostile-crossimplementation-review-r1`

Base SHA: `56697a27e94eb9603dfa412a15ab8f1feb819b0c`

Return path: `WORKER_RETURNS/FIABC-W3-Q01/`

## Status

`COMPLETE__QUALIFICATION_SPEC_AND_FIXTURES_READY_FOR_FANIN`

This worker is a qualification/review worker only. No sibling implementation, semantic owner, HQ handoff, decision ledger, frozen candidate owner, measured P2X state, or accepted authority was changed.

## Governing inputs read

The review was grounded from the exact Wave-2 HQ fan-in tip and consumed the governing Wave-2 adjudications rather than reopening them:

- `WORKER_RETURNS/FIABC-HQ-WAVE2-FANIN/00_RETURN.md`
- `WORKER_RETURNS/FIABC-HQ-WAVE2-FANIN/02_IMPLEMENTATION_OBLIGATION_LEDGER.csv`
- `WORKER_RETURNS/FIABC-HQ-WAVE2-FANIN/03_RESOLVED_AND_DEFERRED_DEBT.md`
- `WORKER_RETURNS/FIABC-HQ-WAVE2-FANIN/04_WAVE3_IMPLEMENTATION_MATRIX.md`
- `FIABC-W2-L01`, `L02`, `L03`, `L04`, `B01`, `B02`, `B03`, `B04`, and `B05` return packages at their registry-pinned refs.

The current PRE553 production surfaces relevant to I01-I08 were also inspected. The exact review map is in `01_PRODUCTION_SURFACE_MAP.csv`.

## Qualification holding

Wave-3 fan-in must be tested against the conserved object:

`FUNCTION + AUTHORITY + NEGATIVE-STATE LAW + PROVENANCE + DOWNSTREAM CAPABILITY`

The qualification must therefore reject implementation patches that are locally plausible but cross one of the settled ownership or comparison boundaries. In particular, a numeric diagnostic, an effective-N scalar, a cache/accelerator, a repackaged runtime blob, an oracle equality, a telemetry value, a manifest row, or an intermediate C11/I03 receipt is not sufficient merely because it exists or is numerically stable.

The return supplies an independent, return-local qualification contract and negative fixtures for the exact Wave-3 risks. It does not become a semantic owner. Integrated implementations may expose their evidence through adapters or receipts, but the underlying production fields/objects remain sibling-owned.

## Required qualification families

1. **I01 diagnostics** — diagnostics cannot become `EmpiricalFact`, semantic authority, structural authority, or exact-frontier control; typed unavailable/noncomparable/underpowered/invalid/unresolved states must not be upgraded to support merely because a score exists; diagnostic identity must bind exact fact/query/release/authority/replay determinants.
2. **I02 effective-N** — no implicit/default/inferred weight; RAW/unweighted work cannot manufacture numeric effective-N; authorized weighted results must bind exact weight/design/estimand and exact joint/risk/query scope; invalid/degenerate weights fail closed.
3. **I03 Candidate C** — identity remains Candidate C even when realization is source-backed; accelerators are optional and nonauthoritative; only CACC1/CACC2 can appear for LiTS within their scope; WVS has zero accelerators; no CACC3; LiTS q310/q311 remain in the workload and use exact-source fallback when outside accelerator scope.
4. **I04 packaging** — exact accepted derivative blobs and accepted identities survive rebinding; Node4A exact carrier is present; frozen candidate-owner identities remain frozen; lawful immutable historical roots are not reclassified as obsolete merely because their path is historical.
5. **I05 parity oracle** — expected truth is candidate-neutral and frozen before candidate output; no candidate root/output/session can enter oracle dependency closure; pairwise equality or self-replay cannot substitute for oracle agreement; frontier and negative-state closure must be complete.
6. **I06 accounting** — source×candidate cells are process-isolated; candidate sessions/state do not leak; RSS is candidate-process-local; canonical metrics are write-once; uncaptured telemetry is typed null rather than synthetic zero; observed I/O is not endpoint directory size; scratch and lifecycle measurements represent exercised work.
7. **I07 succession preflight** — repository presence is not live consumption; every required chain must close through current owner, executable binding and exact live receipt, with authority, negative-state, candidate capability, oracle and accounting closure.
8. **I08 final terminal** — PASS requires complete governed I05 learned empirical product identity plus semantic/replay/output identity, coverage and constituent I03 closure. C11 and I03 are mandatory intermediate invariants but are not the final comparison terminal.

## Artifacts

- `01_PRODUCTION_SURFACE_MAP.csv` — exact pre-fan-in surfaces, frozen identities and review hooks for I01-I08.
- `02_HOSTILE_FIXTURES.json` — positive controls plus exact negative-path fixtures and expected rejection codes.
- `03_ACCEPTANCE_CRITERIA.md` — normative acceptance law and required evidence per implementation family.
- `04_INTEGRATED_TEST_PROTOCOL.md` — deterministic fan-in qualification protocol and later execution commands.
- `05_TEST_INVENTORY.csv` — fixture-to-risk-to-worker inventory.
- `tests/qualification_contract.py` — court-local witness validators; no production imports or ownership changes.
- `tests/test_hostile_qualification_contract.py` — fixture-driven unit tests proving every listed negative case is rejected with the expected code and positive controls are accepted.
- `RETURN.json` — machine-readable return metadata.

## Tests

Added:

`WORKER_RETURNS/FIABC-W3-Q01/tests/test_hostile_qualification_contract.py`

The test is deliberately self-contained and requires no survey source bytes. It validates the qualification contract and its fixtures. It was not executed in this browser/GitHub-only commission because no Python execution surface was used and sibling fan-in is not yet present.

Run after fan-in:

```bash
python -m unittest discover -s WORKER_RETURNS/FIABC-W3-Q01/tests -p 'test_*.py' -v
```

Then apply the same contract to integrated sibling receipts/witnesses before any local/source-byte or measured P2X work. `04_INTEGRATED_TEST_PROTOCOL.md` fixes the order and stop conditions.

## Exact blockers

There is no blocker to delivering this qualification specification. There **is** an intentional execution dependency: no integrated Wave-3 implementation existed on this branch, so this worker does not claim that I01-I08 currently pass these tests. The WVS parity-oracle materialization and any measured P2X work remain outside this browser-only review and must not be fabricated.

## Terminal

`FIABC_W3_Q01_HOSTILE_IMPLEMENTATION_QUALIFICATION_SPEC_READY`
