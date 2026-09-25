# FIABC SPLIT R2 — WORKER C — T5 / PROCESS LIFECYCLE / FAILURE-PATH PARITY — RETURN

## Terminal

`BLOCKED__PREEXISTING_JOINED_T5_FAILURE_PATH_DEFECT`

This is not a split-only defect and must not be patched in alternate split control. The dedicated fan-in commission explicitly requires fan-in to stop if Worker C proves this class.

## Provenance

- Worker branch: `agent/rabochii-fiabc-split-r2-c-t5-process-failure-parity-r1`
- Commission commit: `48a201ee846294a56618f520f166eafa4282b1a3`
- Exact common base: `e1b82095c83dd15a64b409dba0e4ae7d4f4460c6`
- Protected execution: `agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1`
- Protected head: `3d8f2ad62600b6777dcb23a28404a067502e77a0`
- Protected execution modified: **NO**
- Alternate split-control code modified by Worker C: **NO**

Relevant protected blobs are byte-identical at the protected head and split common base:
- `ee_p2x_candidate_process_envelope.py`: `e8b653991887855ac7dee730bb19706219332422`
- `ee_p2x_darwin_court_driver.py`: `33605355d9f2b6236d20fa207fbca59d357823e0`
- `fiabc_live_terminal_control.py`: `95739544dceea60298a6e90a87a9062b4fed6df1`
- `fiabc_live_accounting_binding.py`: `31aaf0dadffad260bb77ef65c530188a560b32a1`
- exact T2 manifest: `49692c1c8527680c97af073039b36125edd7e56d`

## Decisive defect proof

1. Protected `ProcessIsolationController.run_stage()` correctly stops the main candidate process whenever a backend stage returns non-PASS. It also forbids cross-cell reuse and permits same-cell retention only under an authorized adjacent lifecycle token.
2. The joined driver then correctly applies `_candidate_stop()`: after a candidate-local failure, the failed candidate's remaining stages are terminalized as `CANDIDATE_LOCAL_FAILURE`, and control proceeds to the later candidate named by the manifest.
3. T5 observation files are materialized by `admit_post_i05_oracle_match()`, and that function is invoked by `_backend_terminal()` only when S05 returned `PASS`.
4. Therefore A or B failing before or at S05 has **no** `fiabc_t5_candidate_observation.json`.
5. When C reaches a passing S05, `admit_post_i05_oracle_match()` unconditionally loops A/B/C and loads each observation from `cells/<same source>/<candidate>/receipts/fiabc_t5_candidate_observation.json`.
6. `_load()` hard-raises `LiveTerminalControlError` when any required receipt/document is absent.
7. In the joined driver, only `backend.run_stage()` is inside the typed candidate/common-blocker try/except. The subsequent `_backend_terminal()` call is outside it. The missing A/B observation therefore becomes an **untyped orchestration failure at C/S05**, not a lawful candidate-local failure or common blocker.
8. The split runner has the same post-backend `base._backend_terminal()` exception surface. Because the governing T5/process blobs are identical, this is a pre-existing joined-runner defect, not a split regression.

The exact trigger class exists for **both LiTS-I and WVS7**:
- A fails before S05;
- A fails at S05;
- B fails before S05;
- B fails at S05.

That is eight source×candidate×position cases. A/B failures after S05 do not trigger this specific defect because their observations already exist. C failures before/at S05 do not invoke the C three-way gate. C failures after S05 and S16 failures occur after the three-way observation set has already been materialized.

## Process lifecycle differential

The protected process policy itself is sound for the requested parity questions:

- one active main candidate process maximum;
- active process refuses a different cell key;
- same-cell retention requires an explicit adjacent-stage authorization token;
- any candidate-local/common-source/common-court non-PASS stage stops the process before returning;
- A→B and B→C cell-terminal edges stop;
- LiTS→WVS source boundary stops;
- no foreign-candidate warm-state inheritance path was found;
- S15 launches a **new Python replay child**, binds the same source/candidate in its replay plan, and records the parent cell token plus replay token.

One subtlety matters: on a **passing C/S05**, the controller lawfully retains C's main process for S06. The fatal missing-observation exception happens afterward in outer T5 terminal control. The process will ultimately be aborted on controller close/atexit, but the court has already lost typed failure semantics and no lawful source/court terminal is produced.

See `12_PROCESS_LIFECYCLE_DIFFERENTIAL.json`.

## Exact T5 dependency graph before S17

For **each source independently**:

- A/S05 = A observation + that source's frozen oracle.
- B/S05 = B observation + that source's frozen oracle.
- C/S05 = C observation + that source's frozen oracle + A/B/C observations for that **same source**.
- Each S16 = current-cell observation + current-cell oracle match + current-source freeze + current manifest + current-cell T4 accounting/journal + current-cell S15 lifecycle receipt + current S16 backend replay projection.
- Cross-source live output is first required by full-court S17/final composition, which iterates both sources and all six cells.

Thus:
- `LITS_I` T5 does not require live WVS output before S17.
- `WVS7` T5 does not require live LiTS output before S17.

See `13_T5_SOURCE_LOCAL_DEPENDENCY_AND_FAILURE_PATHS.json`.

## WVS RUN5 semantic conservation

Worker C's answer is **conditional yes for semantic evidence, separate from physical admissibility**.

If WVS RUN5 reached a natural source terminal and its existing WVS observation/match/three-way/S16 terminal artifacts are still byte-identical and independently revalidatable, its WVS semantic evidence can be conserved without LiTS live output. The defect proved here would have prevented natural terminalization if A or B had failed before/at S05; it does not silently alter a successfully terminal WVS semantic result.

This is **not** a physical-metric admission. Split-only immutable/owner deployment cost, work-root prestate, cache/host history, and related physical-equivalence burdens remain independent and may still void physical comparison.

See `14_WVS_RUN5_SEMANTIC_CONSERVATION.json`.

## Source-free forensic qualification

Authenticated exact-ref GitHub reads plus deterministic structural/manifest assertions produced **16/16 PASS**:
- protected process stop/retention/cross-cell laws;
- S15 fresh child attribution;
- exact C/S05 same-source A/B/C dependency;
- hard missing-document behavior;
- joined and split post-backend exception placement;
- S16 source/cell locality;
- S17 first cross-source live composition;
- exact eight-case failure trigger matrix;
- exact protected/common-base blob identity.

Zero-access/zero-execution accounting:
- raw source opens: **0**
- source hash passes: **0**
- decoder calls: **0**
- candidate process launch attempts: **0**
- candidate outputs: **0**
- measured execution: **false**

See `15_SOURCE_FREE_FORENSIC_HARNESS.json`.

## Required next action

A protected-code T5 failure-semantics repair/adjudication is required before either the joined court or the split court can truthfully claim that A/B candidate-local failures before S05 allow lawful continuation through C/S05. The repair must decide the lawful meaning of C three-way parity when an earlier candidate lacks a passing S05 observation and must return a typed governed terminal rather than an orchestration crash.

Worker C does **not** patch protected execution.

## Fan-in instruction

Per the fan-in commission: **STOP fan-in on this blocker. Do not paper over it in alternate source-split control.**

`BLOCKED__PREEXISTING_JOINED_T5_FAILURE_PATH_DEFECT`
