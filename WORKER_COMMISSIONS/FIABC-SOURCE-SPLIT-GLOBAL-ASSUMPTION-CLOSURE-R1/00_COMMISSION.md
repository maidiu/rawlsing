# FIABC SOURCE-SPLIT GLOBAL-ASSUMPTION HOSTILE CLOSURE — R1

You are **FIABC SOURCE-SPLIT GLOBAL-ASSUMPTION HOSTILE CLOSURE — R1**.

Repository:

`maidiu/rawlsing`

**AGENT TYPE: LOCAL SOURCE-FREE CODE / TEST / FORENSIC REPAIR ONLY**

Use strongest available reasoning.

Do not open, hash, decode, inspect, or infer from LiTS/WVS raw survey sources.

Do not launch Candidate A/B/C.

Do not run measured P2X.

Do not mutate protected execution.

Do not mutate prior measured/pre-candidate work roots.

Do not touch any already-running measured process.

This court exists because the first RUN5 LiTS source-local measured invocation passed preflight but crashed before any A/B/C stage was recorded:

`StageStateError: progress address precedes current manifest entry or is unknown: LITS_I/A/S00_SOURCE_PREFLIGHT_IDENTITY`

HQ adjudication:

`HQD-2026-09-25-099`

This court MUST close the entire class of split-derived full-court-assumption defects before any further measured relaunch.

---

# EXACT BASES

Source-split closure branch:

`agent/vozhd-fiabc-source-split-global-assumption-closure-r1`

Exact branch base:

`4f0ee6bbc7e3387fb1c71837c1ae8bea658f64a2`

Protected execution branch:

`agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1`

Exact protected execution head:

`3d8f2ad62600b6777dcb23a28404a067502e77a0`

DO NOT MODIFY PROTECTED EXECUTION.

Current expanded runtime authority:

- CPython 3.11.3
- pyreadstat 1.3.6
- pyarrow 25.0.1
- pandas 2.3.1
- numpy 2.3.2
- Darwin x86_64

Current source-split runner files:

- `HQ_HANDOFF/launchers/FIABC_SOURCE_LOCAL_SPLIT_DRIVER.py`
- `HQ_HANDOFF/launchers/RUN_FIABC_SOURCE_LOCAL_SPLIT.sh`
- `HQ_HANDOFF/launchers/FIABC_SOURCE_LOCAL_SPLIT_MERGE.py`

Current qualification tests:

`rawlsing_next/tests/test_fiabc_source_local_split_qualification.py`

---

# OBSERVED DEFECT — MUST REPRODUCE SOURCE-FREE

The protected manifest has:

`first_unfinished_court_stage = LITS_I/A/S01_CANDIDATE_PREPARATION_BUILD`

but the source-local LiTS stage traversal intentionally begins at:

`LITS_I/A/S00_SOURCE_PREFLIGHT_IDENTITY`

because the split court uses a fresh work root and must reconstruct the preserved S00 binding.

The inherited full-court `ManifestProgressPlan` truncates its address universe at `machine.first_unfinished`.

Therefore the source-local runner calling:

`driver.progress.emit_stage(LITS_I/A/S00..., ...)`

causes:

`StageStateError("progress address precedes current manifest entry or is unknown")`

before A/B/C execution.

Reproduce this source-free against the exact protected manifest before repairing it.

Do not accept a fix that merely suppresses the one observed string without closing the generalized cursor/scope mismatch.

---

# GLOBAL CLOSURE BURDEN

The source split changes one globally ordered six-cell court into:

- LiTS host: `LITS_I/A -> B -> C`
- WVS host: `WVS7/A -> B -> C`

The closure must prove every reused full-court assumption remains lawful under this partition.

## G1 — SOURCE-LOCAL PROGRESS PLAN MUST BE SOURCE-LOCAL

Do not reuse a full-court progress plan whose address universe begins at the global `first_unfinished` cursor.

Implement a source-local progress scope that:

- contains exactly all governed stages for the selected source in manifest order;
- contains A/B/C only for that source;
- contains mechanical preserved/skipped stages needed to reconstruct a fresh source-local root;
- never contains the other source;
- never contains `COURT/S17`;
- allows all selected-source stage progress events without `StageStateError`;
- preserves the fact that progress telemetry is court-administrative and non-evidentiary;
- preserves cell-completion emission;
- does not alter backend/candidate measurement behavior.

Test it against the **actual protected execution manifest**, not only synthetic fake stages.

Required hostile cases:

- LiTS/A S00 before global first_unfinished;
- all LiTS A/B/C stage addresses;
- all WVS A/B/C stage addresses;
- preserved stages;
- skipped stages;
- candidate-local failure propagation;
- common-source blocker;
- common-court blocker.

## G2 — SOURCE-LOCAL DISPATCH MUST BE PROVED AGAINST GLOBAL TRANSITION LAW

The current source-local runner traverses every selected-source manifest stage in a deterministic list rather than following the global court's `next_stage` pointer literally.

Prove this is lawful.

For the exact current manifest, mechanically classify every divergence between:

1. the protected full-court next-stage graph, and
2. the source-local selected-source traversal.

Any extra stage executed/materialized by the source-local traversal must be:

- non-candidate-executable mechanical preservation/skip work only;
- required to make the fresh source-local source block complete;
- source-local;
- non-measured.

Specifically inspect known boundaries such as WVS7/B -> WVS7/C where the global transition points to C/S01 while C/S00 is a preserved mechanical stage.

No candidate-executable stage may be inserted, dropped, repeated, or reordered by the split traversal.

Add an exact-manifest hostile test that fails if a future manifest change violates this law.

## G3 — SOURCE CUT MUST BE EXACT

For each selected source:

- dispatch begins at that source's first governed stage needed for a fresh source-local root;
- dispatch ends after that source's C terminal stage;
- LiTS must never dispatch WVS;
- WVS must never dispatch LiTS;
- neither half may dispatch `COURT/S17`;
- cross-source `next_stage` pointers may be recorded in receipts as inherited manifest law but may not be followed by a source-local runner.

Test with the exact manifest.

## G4 — CANDIDATE FAILURE / BLOCKER PROPAGATION MUST REMAIN LAWFUL

Prove exact behavior under:

- Candidate A local failure;
- Candidate B local failure;
- Candidate C local failure;
- common-source blocker at early/middle/late stages;
- common-court blocker at early/middle/late stages.

Requirements:

- candidate-local failure stops only the failed candidate's remaining measured stages and continues lawful later candidates in the same source;
- source blocker propagates only within that source;
- court blocker stops that source-local block immediately and is explicitly represented as a court-level blocker;
- no blocker path may fabricate completion of unexecuted candidate work;
- the merge must treat any unresolved common authority as globally blocking P2 admissibility.

Concurrency note:

If one source hits a common-court blocker while the other source is already running on another host, the other host may finish naturally, but its resulting evidence must remain non-admissible for P2 until HQ adjudication. Do not invent cross-host process killing.

## G5 — EXACT CONTROL-RUNNER BINDING

The current shell checks the control branch name but not an exact qualified control implementation identity.

Close this fail-open surface.

Because a script cannot self-hardcode its own final commit SHA without a self-reference problem, use a lawful non-circular binding design.

Acceptable examples:

- an external HQ-provided exact expected-control-head gate plus exact tested runner hashes; or
- an immutable post-qualification control binding receipt that binds tested implementation head + launcher/driver/merge SHA-256 values, with the launcher verifying its own bytes against that receipt.

Requirements:

- wrong control branch => fail;
- unqualified control implementation => fail;
- modified launcher => fail;
- modified source-local driver => fail;
- modified merge verifier => fail for merge use;
- dirty control checkout => fail;
- exact tested protected execution remains independently bound.

Add hostile tests.

## G6 — PROTECTED REPO-LOCAL MUTABLE EVIDENCE NAMESPACE

The protected backend writes live evidence to:

`<execution checkout>/WORKER_RETURNS/EE-P2X/LOCAL_COURT`

This namespace is outside external `WORK_ROOT`.

That is a critical split boundary.

Prove source-free, statically and dynamically where feasible, that:

- S01–S16 candidate execution does not consume mutable `LOCAL_COURT` output produced by another source;
- live `LOCAL_COURT` outputs are audit/evidence outputs only;
- immutable repo reads such as `09_LOCAL_COURT_FROZEN_EXPECTATIONS.json` are clearly distinguished from mutable live `LOCAL_COURT`;
- one source block cannot alter/read another source's mutable live evidence;
- no cross-source semantic/candidate state is carried through the execution checkout.

Add a pre/post repo-local evidence inventory law for source-local execution:

- bank the baseline inventory before measured source-block entry;
- bank the post-block inventory after terminalization;
- identify created/changed live evidence paths;
- require every changed live path to be attributable to the selected source or explicitly source-neutral court administration;
- fail closed on a non-selected-source live mutation.

Do not modify the protected backend merely to relocate its governed evidence unless absolutely necessary and separately justified.

Prefer control-layer inventory/snapshot binding.

## G7 — PORTABLE SOURCE-LOCAL EVIDENCE CLOSURE

Because the two hosts have separate protected checkouts, the final merge cannot assume one shared repo-local live-evidence namespace.

After the source-local measured block is terminal, create a non-measured closure/snapshot receipt under the external work root that binds:

- source-local terminal receipt;
- stage ledger;
- every selected-source stage receipt;
- every selected-source repo-local live evidence artifact created/changed relative to baseline;
- hashes of those artifacts;
- exact control-runner identity;
- exact protected execution identity;
- exact runtime fingerprint;
- source SHA;
- candidate order;
- proof no nonlocal source evidence was included.

This post-terminal evidence packaging must occur only after measured stage timing is complete and must not contaminate candidate physical metrics.

Do not copy raw survey source bytes.

## G8 — ORCHESTRATION FAILURE RECEIPT

The RUN5 LiTS failure exited code 1 and emitted no source-local terminal.

Add a fail-closed orchestration failure receipt for any nonzero source-local measured-driver exit.

It must record at least:

- source;
- selected source SHA identity;
- execution head;
- control identity;
- runner file hashes;
- runtime;
- measured runner exit code;
- whether any candidate stage ledger entry exists;
- last terminal/partial stage address if any;
- stage ledger hash if present;
- progress JSONL hash if present;
- source-local terminal absent/present;
- explicit `PRESERVE_WORK_ROOT`;
- explicit no-retry law.

It must not misclassify a control-plane failure as candidate-local failure.

## G9 — MERGE MUST VERIFY, NOT MERELY TRUST A SELF-HASHED TERMINAL

Strengthen `FIABC_SOURCE_LOCAL_SPLIT_MERGE.py`.

For each source root, independently verify at minimum:

- terminal schema;
- terminal self-identity;
- expected exact source ID;
- expected canonical source SHA;
- exact protected execution head;
- exact execution-manifest identity consistency;
- source_local_only == true;
- six_cell_s17_executed == false;
- six_cell_completion_claimed == false;
- measured_synthesis_performed == false;
- p2_synthesis_authorized == false;
- exact candidate inventory A/B/C;
- candidate terminal addresses belong to expected source/candidate;
- candidate terminal dispositions are lawful;
- common blocker inventory is source-scoped and well-formed;
- incomplete-stage inventory is coherent with blocker status;
- stage ledger file exists;
- stage ledger hash equals terminal's `stage_ledger_sha256`;
- ledger contains no non-selected-source stage entries;
- no selected-source RUNNING stage remains;
- all required selected-source stages are terminal except lawfully incomplete stages under a common-court blocker;
- each ledger receipt path stays inside allowed roots;
- each receipt hash matches;
- portable repo-live-evidence closure/snapshot receipt verifies;
- control-runner identity is qualified;
- hardware/runtime comparison is exact under current split law;
- macOS mismatch remains recorded separately;
- absolute cross-source physical metric comparison remains forbidden.

Do not recreate or claim governed S17.

## G10 — CONTROL COMPATIBILITY BETWEEN HALVES

The merge must not silently combine arbitrary source-local terminals produced by different control implementations.

For a new court, default law should require the same qualified source-split execution-control identity for both halves.

If HQ later decides an already-completed WVS RUN5 result from control head `4f0ee6...` can be conserved across a progress-only repair, that must be handled by a separate explicit compatibility receipt proving the WVS candidate-execution semantics were unchanged.

Do NOT silently grandfather it.

This closure must produce enough evidence for HQ to decide whether a naturally completed WVS RUN5 result can be retained without rerun.

## G11 — ACTUAL-MANIFEST SOURCE-FREE INTEGRATION TESTS

The previous qualification used `FakeProgress`, which masked the observed defect.

That is no longer sufficient.

Add source-free tests using the **actual protected**:

- `StateMachine`;
- current six-cell execution manifest;
- actual `ManifestProgressPlan` or the repaired source-local progress plan;
- actual source/candidate/stage inventory.

Use fake source verification and fake backend results only where needed to prevent source access/candidate process execution.

The tests must exercise the orchestration layer for BOTH selected sources through:

- all-pass sequence;
- A failure;
- B failure;
- C failure;
- common-source blocker;
- common-court blocker;
- preserved/skip stages;
- source-terminal construction;
- verify-only path.

The purpose is to catch interface mismatches between real protected objects and the alternate control runner.

## G12 — ZERO SOURCE / ZERO CANDIDATE QUALIFICATION LAW

All closure qualification must remain:

- raw source opens = 0;
- source hash passes = 0;
- decoder calls = 0;
- candidate process launch attempts = 0;
- candidate outputs = 0;
- measured execution = false.

No LiTS/WVS source bytes may be accessed.

## G13 — CANONICAL SIX-CELL PATH MUST REMAIN UNCHANGED

Do not modify:

- protected execution branch;
- canonical six-cell launcher;
- frozen candidate owner code;
- T2 manifest;
- T3 frozen source/oracles;
- T4 accounting semantics;
- T5 current court contract.

The closure is alternate split orchestration/composition only.

## G14 — PRIOR ROOT IMMUTABILITY

Do not modify/resume/clean:

- prior RUN4 WVS measured root;
- prior blocked LiTS root;
- RUN5 LiTS failed root;
- any RUN5 WVS root/process.

If WVS RUN5 is still running, do not interact with it beyond passive status collection requested by the user.

---

# REQUIRED FORENSIC / TEST MATRIX

At minimum produce a checked-in matrix with one row per risk:

1. global first_unfinished cursor;
2. preserved stage before cursor;
3. selected-source stage universe;
4. cross-source next-stage cut;
5. candidate-local failure next edges;
6. WVS B -> C/S01 preserved-C/S00 mechanical closure;
7. common-source blocker;
8. common-court blocker;
9. full-court S17 exclusion;
10. selected-source raw path only;
11. full T3/oracle authority consumption without nonselected raw source;
12. exact runtime;
13. protected head;
14. control implementation binding;
15. dirty control checkout rejection;
16. repo-local mutable evidence read/write boundary;
17. nonlocal repo evidence mutation rejection;
18. external work-root candidate isolation;
19. source terminal completeness;
20. stage ledger hash/receipt verification;
21. portable evidence closure;
22. merge source SHA validation;
23. merge control compatibility;
24. merge hardware/runtime validation;
25. OS mismatch treatment;
26. absolute cross-source physical metric prohibition;
27. orchestration-failure receipt;
28. prior-root no-resume law.

For each row report:

- governing invariant;
- exact implementation surface;
- hostile test name;
- PASS/BLOCKED;
- evidence path.

---

# MANDATORY SECOND-PASS ADDENDUM

Before implementation or qualification is considered complete, read and execute in full:

`WORKER_COMMISSIONS/FIABC-SOURCE-SPLIT-GLOBAL-ASSUMPTION-CLOSURE-R1/01_JOINED_RUNNER_DIFFERENTIAL_PARITY_ADDENDUM.md`

The addendum is cumulative, not optional. Its joined-runner differential parity burdens apply to BOTH LiTS-I and WVS7.

No PASS terminal is lawful unless the addendum's two explicit source verdicts are both PASS.

# REQUIRED RETURN

Return under:

`WORKER_RETURNS/FIABC-SOURCE-SPLIT-GLOBAL-ASSUMPTION-CLOSURE-R1/`

Required:

- `00_RETURN.md`
- `RETURN.json`
- `01_SPLIT_ASSUMPTION_MATRIX.json`
- `02_RUN5_LITS_FAILURE_REPRODUCTION.json`
- `03_PROGRESS_SCOPE_CLOSURE.json`
- `04_TRANSITION_EQUIVALENCE.json`
- `05_REPO_LOCAL_EVIDENCE_ISOLATION.json`
- `06_PORTABLE_SOURCE_EVIDENCE_CLOSURE.json`
- `07_MERGE_HOSTILE_VALIDATION.json`
- `08_CONTROL_BINDING.json`
- `09_WVS_RUN5_COMPATIBILITY_ANALYSIS.json`
- `10_SOURCE_FREE_QUALIFICATION.json`
- test output

Terminal only if everything closes:

`PASS__SOURCE_SPLIT_GLOBAL_ASSUMPTION_HOSTILE_CLOSURE__HQ_PROMOTION_REQUIRED`

If any split assumption remains unresolved:

`BLOCKED__SOURCE_SPLIT_GLOBAL_ASSUMPTION_REMAINS`

No measured execution.
