# FIABC-W3-Q02 — fan-in order and dependency plan

## 1. Two different integration operations must not be conflated

Wave-3 implementation branches are all based on Wave-2 HQ fan-in `56697a27e94eb9603dfa412a15ab8f1feb819b0c`. The stopped P2X execution line is a different, diverged history. At Q02 inspection, `617c9c9426db12a3c0f7fea6b68a582c10759553` was 76 commits ahead of the common merge base and 293 commits behind the Wave-2 HQ fan-in tip. It contains the current Darwin driver/backend, runtime-authority closure, continuation reducer, stopped ledger evidence, and R6X reconciler that are absent from the Wave-2 HQ base.

Therefore there are two bounded steps:

1. **PRE-MAIN Wave-3 fan-in:** fan I01-I08, Q01, Q02 into a fresh integration branch rooted exactly at `56697a27e94eb9603dfa412a15ab8f1feb819b0c`; qualify the implementation contracts and tests there.
2. **P2X execution rebinding:** after PRE-MAIN qualification, transpose only the accepted production/test deltas required for execution onto the HQ-authorized descendant of the existing P2X line. Do **not** wholesale merge the divergent PRE-MAIN history into the P2X branch, and do not copy HQ handoffs/decision ledgers.

A raw `git merge` of the full Wave-3 fan-in into the existing P2X line is not the mechanical plan because it would mix two divergent governance histories and can silently replace current P2X runtime surfaces with older-base lookalikes.

## 2. Required PRE-MAIN fan-in order

Use this order unless a sibling return proves a strictly disjoint patch:

1. **I01 diagnostics** — semantic leaf; no P2X orchestration dependency.
2. **I02 effective-N** — semantic leaf; preserve I01 and current EmpiricalFact ownership.
3. **I04 runtime packaging rebind** — establishes stable current runtime locators and exact Node4A carrier before any P2X core worker is resolved.
4. **I03 Candidate-C production binding** — bind LiTS source fallback and WVS zero-accelerator C through the stable I04 package paths.
5. **I05 independent parity oracle** — bind candidate-neutral expected truth after source/C capability is known, but before instrumentation decides measurement start.
6. **I06 equal-work instrumentation** — wrap the already integrated I03/I05 execution semantics in the fresh-process/observed-telemetry lifecycle.
7. **I07 mechanized succession preflight** — bind exact owners/bindings/consumers only after I01-I06 are stable.
8. **I08 final I05 terminal verifier** — last implementation worker because it consumes I07 PASS, I05 PASS, all admitted cells, and the final terminal identities.
9. **Q01 hostile qualification** — tests/fixtures against the integrated implementation. Do not weaken production contracts to satisfy a stale fixture; adjudicate exact mismatch.
10. **Q02** — planning artifacts only.

## 3. Mandatory per-function conflict resolution in the P2X core

The high-risk file is `rawlsing_next/ee_p2x_darwin_stage_backend.py`. At Q02 inspection I04 had already added this file from the current P2X substrate while I03/I05/I06/I08 were expected to touch overlapping seams. Resolve by function/obligation, never by choosing an entire worker copy:

- **I04 owns packaging locators/checks:** stable LiTS materializer path, stable WVS runtime package path, stable WVS projection materializer path, exact Node4A support fan-in.
- **I03 owns Candidate-C physical binding:** `_compose_lits`, `_compose_wvs`, `_bind`, `_gate`, or their current successors must admit C without moving semantic ownership; LiTS uses CACC1/CACC2 only within exact scope and exact source fallback otherwise; WVS C uses zero accelerators.
- **I05 owns independent oracle semantics:** the old `_s03` same-candidate replay cannot survive as the parity oracle. Candidate-neutral oracle freeze must occur before any candidate output.
- **I06 owns measurement lifecycle:** `_measure`, source-access accounting, process boundaries, write-once metrics, cold/warm separation, real invalidation/corruption/interruption actions, fresh replay, and candidate-local RSS/CPU/I/O.
- **I08 owns final S17 terminal acceptance:** full I05 closure plus exact identities and real preflight/oracle receipts.

If `rawlsing_next/ee_p2x_darwin_court_driver.py` is touched by I05/I06/I07/I08, preserve the same layering: I05 freeze boundary first, I06 process/accounting lifecycle, I07 preflight receipt consumption, I08 terminal receipt consumption. A later worker must not erase an earlier obligation by replacing the whole driver.

## 4. Candidate-C makes the old continuation reducer stale for future measured execution

The historical reducer `WORKER_RETURNS/EE-P2X-CONTINUATION-REDUCER-R1/01_CONTINUATION_STATE_MACHINE.json` hard-codes:

- LiTS-C as requiring the old exact CACC1+CACC2-only prerequisite and historically stopping at q310/q311 reachability;
- WVS-C as having **no executable prerequisite**, with a preserved candidate-local portability failure and frozen-law skips.

Wave-2 adjudication, and now I03 implementation, supersede those **current runtime-capability conclusions** while preserving the historical receipts as immutable history. The accepted current law is source-backed hybrid C with optional accelerators and a lawful zero-accelerator state.

Consequently, measured six-cell P2X is forbidden if the post-fan-in executor still treats the old WVS-C preserved failure or LiTS-C q310/q311 nonqualification as current terminal law. Before measurement, the integrated tree must expose a current execution manifest/driver binding in which all six source×candidate cells are capability-proved and Candidate C remains Candidate C.

This is not permission to rewrite historical evidence. Old reducer/receipts remain immutable historical roots; they simply cannot serve as the current six-cell execution contract after I03 succeeds.

## 5. Independent-oracle ordering conflict that must be resolved at fan-in

The stopped P2X driver currently allows candidate preparation/output at S01 before `_s03` sets `oracle_frozen`. Wave-2 B03 identified this as an ordering defect, and B02 proved that candidate self-replay is not an independent oracle.

The integrated execution order must be:

`SOURCE/WORKLOAD/AUTHORITY FREEZE -> INDEPENDENT ORACLE MATERIALIZE+FREEZE -> CANDIDATE PROCESS START -> C11 -> I03 -> I05 -> lifecycle/replay -> terminal verification`

No fan-in is acceptable if the oracle is first created inside a candidate process after Candidate A/B/C has begun producing candidate-owned state.

## 6. Dependency DAG

- I01 -> I07, I08 (preterminal capability must be represented in succession manifest where required).
- I02 -> I07, I08.
- I04 -> I03, I06 (stable runtime packaging is the execution substrate).
- I03 -> I05 materialization capability checks, I06, I07, I08.
- I05 -> I06 measurement start law, I07 preflight, I08 terminal verifier.
- I06 -> I07 accounting-resolution gate and I08 lifecycle replay acceptance.
- I07 -> I08.
- I01-I08 -> Q01 hostile qualification.
- I01-I08 + Q01 PASS + R6X reconciliation + source-local oracle materialization + six-cell premeasurement qualification -> lawful measured P2X.

## 7. Hard fan-in stops

Stop integration and return to the responsible worker if any of these appear:

- a new semantic owner for an existing truth object;
- a current-tree Candidate A/B/C lookalike substituted for a frozen owner blob;
- CACC3, WVS accelerator, or q310/q311/workload truncation;
- Candidate C implemented by silently selecting Candidate B;
- diagnostics able to mint EmpiricalFact or control I05 frontier membership;
- numeric effective-N on RAW/unweighted P2X without exact weight authority;
- oracle expected truth derived from a candidate output or candidate-owned cache;
- oracle frozen after candidate start;
- whole-file backend/driver conflict resolution that drops a sibling obligation;
- I06 metric fields that overwrite prior measurements or use synthetic zero for uncaptured data;
- I07 PASS based on repository presence without executable/live consumption proof where required;
- I08 accepting C11, I03, or partial I05 as the terminal;
- any use of the historical WVS-C portability failure as current six-cell capability law after I03 is admitted.
