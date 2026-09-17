# EE-R6B — FINAL A/B/C BAKEOFF PREASSEMBLY — governed return

Status: `PASS__14_READY_CELLS_ASSEMBLED__FOUR_WVS7_CELLS_EXACT_SPLICE_ONLY__NO_ABC_RUN`

Worker: `EE-R6B`  
Branch: `agent/rabochii-prev3-ee-r6b-final-bakeoff-assembly-r1`  
Commission tip: `5ec735fe02fc0659613ec888ec32f5b2ee74accd`  
Exact grain: `ASSEMBLE_ONE_EXACT_CANDIDATE_NEUTRAL_FINAL_ABC_EXECUTION_PACKAGE_FROM_ALL_ALREADY_READY_SELECTION_CRITICAL_PREMISES_AND_PHYSICAL_BINDINGS__LEAVE_ONLY_WVS7_OP003_OP006_AS_AN_EXACT_FOUR_CELL_CONDITIONAL_SPLICE`

## Canonical HQ authority

The preassembly is pinned to canonical checkpoint `20260916T1647-0400`, control-branch tip
`e2380933058de742660ae7de06ecb64ac6f8a6f0`, handoff commit
`87340b9f091a8277a6dfc275c95b8ffb15097f05`, latest substantive authority
`5ec735fe02fc0659613ec888ec32f5b2ee74accd`, and semantic PRE-MAIN
`1dcd2a79dd6d4208738f655ab7fe4e71c219e354`.

No MAIN or semantic PRE-MAIN mutation is part of this return.

## Exact preassembly result

The final selection floor is frozen at 18 universe×operation cells in one candidate-neutral order:

1. WVS7 OP001–OP006;
2. WVS7 OP020–OP022;
3. LiTS-I OP001–OP006;
4. LiTS-I OP020–OP022.

Exactly 14 cells are ready now:

- WVS7 OP001–OP002;
- WVS7 OP020–OP022;
- LiTS-I OP001–OP006;
- LiTS-I OP020–OP022.

Exactly four cells remain conditional splice slots and no others:

- `WVS7::OP003`;
- `WVS7::OP004`;
- `WVS7::OP005`;
- `WVS7::OP006`.

Those four slots occupy fixed final-order ordinals 3–6 and may only be filled by an HQ-accepted EE-R6A payload satisfying
`03_EE_R6A_FOUR_CELL_SPLICE_CONTRACT.json`.

## Candidate and physical bindings

The package binds the exact EE-R4B owners without substitution:

- A — `R5_LONG_COMPACT_V2__SERIAL_V4__AUDIT69__C05R2A_FACADE`;
  owner `0b96b8de9aac774566f872cf0630ebd4ddeb70e6:rawlsing_next/pre553_r5_source_backed_adapter.py@d4915e7e6755ba1850756aebff72f982f73a332b`.
- B — `SOURCE_BACKED_VIRTUAL_C11`;
  owner `0b96b8de9aac774566f872cf0630ebd4ddeb70e6:rawlsing_next/pre553_source_backed_c11_facade.py@7c509c2098d0030f253344eb3f682471378812a8`.
- C — `SOURCE_BACKED_HYBRID_WITH_REGENERABLE_ACCELERATORS`;
  owner `0b96b8de9aac774566f872cf0630ebd4ddeb70e6:rawlsing_next/pre553_route_c_accelerators.py@abfdc91a71ef5e18c4a8a6bf62fa65750d8d9889`;
  permitted accelerators are exactly `CACC1_LITS1_SEMANTIC_EXECUTION_BUNDLE` and
  `CACC2_FRONTIER_ATOMIC_PREDICATE_RISK_MASK_BANK`.

The exact EE-R5B mechanical bridge is pinned at
`WORKER_RETURNS/EE-R5B/05_BOUNDED_W4_ADAPTER.py@d169be112f454732df161620743ea6332866255e`.
The accepted physical-readiness premise remains **27/27 candidate×operation cells ready, zero proved physical gaps**.
No alternate candidate implementation or bridge was searched for or created.

## Source and semantic premise bindings

WVS7 is frozen to `WVS Wave 7.sav`, 185,163,494 bytes,
SHA-256 `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`.

LiTS-I is frozen to `LITS-2006-data.dta`, 139,531,180 bytes,
SHA-256 `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`,
with the accepted decoder blob `13aa733b511dc23e00bfcdf288c5b920e3f09983`.
The exact R3B roots/replay are frozen as R2 count 24,897/root
`f224533ce0a705bf0839e6bb40bd49dec0c8366e5a5ede0a389e3e67811a13b3`,
R7 count 28,325/root
`0978bd4d87afd88831593ca5977fa9978948d598bf981adfd7fd96ceab979844`,
R27 count 24,630/root
`f9c87f610bcaf0539cc91e7f2608b230cea39d806d3611d6a398519a86386d29`,
and replay identity
`b6c397f93a2dbcac3b37899b74bfd668b443116c19457342e373507a68c82e2d`.

For OP020–OP022 on both universes, EE-R6B does not restate or redesign lifecycle mechanics.
It binds the six exact EE-R3E W4 profiles by commit:path:blob and requires their steps, reset boundaries,
semantic hashes, and identity oracles to be consumed byte-for-byte.

For the eight already-ready OP001–OP006 source/query cells, R3F deliberately freezes candidate-independent
reference procedures and authority/root identities rather than inventing empirical distributions.
Accordingly, `02_READY_14_EXECUTION_ORACLE_PROFILES.json` freezes the exact reference-oracle inputs and the
pre-candidate oracle materialization law: before A/B/C is invoked, the pinned reference procedure is run on the
exact source/authority inputs, its exact result is canonicalized with the pinned EE-W4 canonical JSON function,
and that SHA-256 is installed as the common EE-W4 semantic oracle for A/B/C. Candidate output can never define or
modify that oracle. This is a deterministic execution preflight, not a new semantic or harness design step.

## Execution, measurement, and reset law

`04_EXECUTION_MEASUREMENT_ORDER_RESET_LAW.json` freezes:

- candidate order `A, B, C`;
- the exact 18-cell order above;
- one cold execution for selection-floor OP001–OP006 cells;
- no EE-R6B-synthesized warm repeats (EE-W1 OP023 is the separate warm/repeated-query operation and is outside this 18-cell floor);
- exact byte-for-byte EE-R3E step expansion for OP020–OP022;
- candidate-isolated scratch/durable/log/request/response roots;
- no cross-candidate or cross-universe state/denominator/metric pooling;
- the EE-W4 telemetry fields and `(candidate_id, universe_id, operation_id, phase)` aggregation key;
- semantic and requested identity parity before performance eligibility;
- missing authority as typed non-candidate-failure;
- omitted or incomplete work as incapable of improving a candidate's status.

No score, winner, ranking, or performance number is emitted by EE-R6B.

## Exact EE-R6A splice

The splice contract retains the frozen WVS proving pair:

- `question_impl.phase0.041c03bbacabe4e8d802`;
- `question_impl.phase0.075b1650737d99679b9c`;

with pair newline-stream SHA-256
`5636b4d8cb5249f876dd1bd14e41d96cf903a7b52ae0dfeab9bc76d2152f2406`.

Each of the four slots has a fixed operation, source identity, qid pair, request shape, required oracle-law list,
required authority/binding fields, and a canonical slot-content SHA-256 rule. The validator rejects source or qid
substitution, extra slots, reordering, candidate-specific semantics, or content-hash mismatch.

## Deterministic validation

Governed validator:

`WORKER_RETURNS/EE-R6B/05_validate_preassembly.py`

Governed tests:

`WORKER_RETURNS/EE-R6B/06_test_validate_preassembly.py`

Local validation result:

`{"abc_run": false, "candidate_count": 3, "pending_splice_slots": 4, "physical_cells_ready": 27, "ranking": false, "ready_cells": 14, "status": "PASS"}`

Test result: **11/11 passed**, 0 failures, 0 errors, exit code 0.

The tests cover owner substitution, unauthorized Candidate-C accelerators, missing ready work, source substitution,
qid substitution, metric-law mutation, candidate-order mutation, candidate-specific omission, and four-slot splice
content-hash validation. A test-only structurally complete splice fixture is explicitly non-authoritative and exists
only to exercise the checker.

## Governed artifacts

- `WORKER_RETURNS/EE-R6B/00_RETURN.md`
- `WORKER_RETURNS/EE-R6B/01_FINAL_PREASSEMBLY_MANIFEST.json`
- `WORKER_RETURNS/EE-R6B/02_READY_14_EXECUTION_ORACLE_PROFILES.json`
- `WORKER_RETURNS/EE-R6B/03_EE_R6A_FOUR_CELL_SPLICE_CONTRACT.json`
- `WORKER_RETURNS/EE-R6B/04_EXECUTION_MEASUREMENT_ORDER_RESET_LAW.json`
- `WORKER_RETURNS/EE-R6B/05_validate_preassembly.py`
- `WORKER_RETURNS/EE-R6B/06_test_validate_preassembly.py`
- `WORKER_RETURNS/EE-R6B/07_VALIDATION_RECEIPT.json`

Core artifact SHA-256 before Git publication:

- `01_FINAL_PREASSEMBLY_MANIFEST.json`: `0875869b742e7032165b559b81ae4be68c833e893ee14b4e9cafe40f6dfab981`
- `02_READY_14_EXECUTION_ORACLE_PROFILES.json`: `fc8bad4591cce4461495be31043fc38eca2705609900cc661382c93bff980a19`
- `03_EE_R6A_FOUR_CELL_SPLICE_CONTRACT.json`: `06c784760fa3e6d18fd252cd7af1858298ca0edbdb4da71148d313e5d045cc94`
- `04_EXECUTION_MEASUREMENT_ORDER_RESET_LAW.json`: `0b8d2e28f207273fd1123bf603e455c863d511dc2fcb05dc7a38cf2a6665f435`
- `05_validate_preassembly.py`: `129a8131ebf139390d82a670dda634175153125a28ca8d91c3d1cbd613a730a3`
- `06_test_validate_preassembly.py`: `075ea25c00d4fb3281bf3365bc3e45f6ff7fe8f328cef35203e715c53be4acfa`
- `07_VALIDATION_RECEIPT.json`: `f9b5298794258d93f9498f51c1783787f06c361b9d5fc1f5279b971d2ee03537`

## Final-bakeoff wake condition

The final-bakeoff successor remains asleep until **all** of the following are true:

1. HQ accepts an EE-R6A return for exactly WVS7 OP003–OP006.
2. The four returned slot payloads satisfy the frozen source/qid/request/oracle/hash contract and splice only at ordinals 3–6.
3. Post-splice validation reports 18 ready cells and 0 pending cells.
4. The exact EE-R4B owner pins, EE-R5B bridge and 27/27 physical-readiness premise, EE-W4/R2E harness laws,
   source identities, lifecycle profiles, and metric laws remain unchanged.

That wake authorizes the final-bakeoff successor only. It does not authorize EE-R6B to execute or rank A/B/C.

## Boundary audit

- A/B/C execution: `NONE`
- candidate ranking/selection: `NONE`
- empirical performance inspection: `NONE`
- surrogate performance values: `NONE`
- candidate redesign: `NONE`
- harness redesign: `NONE`
- workload redesign: `NONE`
- storage redesign: `NONE`
- MAIN mutation: `NONE`
- semantic PRE-MAIN mutation: `NONE`

Terminal:

`EE_R6B_PASS__FINAL_ABC_PREASSEMBLY_FROZEN__14_READY__4_EXACT_WVS7_SPLICE_SLOTS__NO_ABC_EXECUTION_OR_RANKING`
