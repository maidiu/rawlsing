# PYAT991 S2-D — ALL-SEVEN G5 RECEIVING

## 1. Verdict

**`REVISE_EXACT_DEFECT`**

The five-owner integration is real and substantially works: actual saved Batch, actual
`execute_issued_workload` NORMAL, and actual `resume_joined_workloads`
COMPLETED/PARTIAL/ABSENT all run on the accepted S2-C estate. The prior I03/I05
subresult and the closed source-scope finding are preserved.

A genuine PARTIAL checkpoint safety counterexample remains, so the full seven-reader
packet is **not accepted**:

> A coherently rehashed **forged saved binding** on a **PARTIAL** checkpoint is refused
> only **after** two protected retained-output restores. The COMPLETED branch correctly
> refuses with zero restores.

This violates the original requirement that forged checkpoint material be refused
before protected restore/serve. The defect is an ordering bug, not a missing test only.

No reviewer product code was edited. No new A/B round, no protected merge.

## 2. Exact artifact and authority

- Base / owner-ACK delivery: `b32f215660def205762f0e9d0eafa2c3dfaa0c36`
- Tested candidate: **`5df0bbdf3ec4c479724e74651a80d4861ab700a1`**
- Prior G5 return: `eccc0ad4980261bdf7e77d4e18569f334089d7df`
- Prior qualified saved cut: `5478210b7aeedf608a3e9754bf891d4d0262817f`
- Accepted S2-C: `b7b697b69f0acea12174937ee824c19ac34ac284` / tree `dc416d1f23100d4d52b19bc2120226964bc0be43`
- Contract SHA-256: `37d4b7e22035f97ec39bf72c57fbe944be215b3a7273a284a30fbafdf6a87da5`
- Branch/worktree: `agent/pyat991-s2d-g5-r1` / `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat991-s2d-g5`
- Reviewer: `ses_e30c25800ffeT8XbyTuHekRCme`; model `opencode-go/deepseek-v4.1-flash#max`
- Write allowlist: `WORKER_RETURNS/PYAT991_ALL_SEVEN_G5/` only.

**Owner ACK verified:** `WORKER_RETURNS/PYAT991_OWNER_HANDOFF/owner_ack.json`,
blob `dae76ff13b096efe67df9ec526b9d8b99ce28b25`, status `ACK`. The serial lease covers
`BatchExecutionRunner.__init__`/identity lookup and the issued-workload
execute/resume/checkpoint/capture helpers; the existing S2-D new-module surface continues.
The ACK explicitly records an inherited functional/controller allocation, not personal
R16 Batch authorship. The 13-path delta stays inside that lease and the existing S2-D
module surface; no new owner permission was manufactured.

Product path blobs at the tested cut:

- `pre553_batch_runner.py`: `49e3974c658d66a270815d9faa3798b40d4488b1`
- `pre553_issued_workload.py`: `c50be4a54433d429e92bd2232f56e735d11375b2`
- `pre553_saved_c11_admission.py`: `22749addc1fca5f0b90e12728847c390aafa7a84`
- `pre553_saved_workload_integration.py`: `cc8aa32512378261406d765f0b049c748cb3e11f`
- `test_pyat991_s2d_five_readers.py`: `38e339b70eb1ca8f607b75a8a259523504ede731`

The accepted S2-C writer/layout/I03 session/tests and all prior returns are unchanged.

## 3. Decisive defect

- **ID:** `G5-S2D-PARTIAL-FORGED-BINDING-BEFORE-RESTORE`
- **File:** `rawlsing_next/pre553_issued_workload.py`
- **Function:** `resume_joined_workloads`
- **Lines at cut:** 1568–1582
- **Witness:** `forged_partial_binding.py`
- **Raw:** `evidence/forged_partial_binding.json`

Actual partial sequence:

1. `require_unchanged(... BEFORE_RESTORE ...)`
2. `_validate_entry_material(entry)`
3. `_validate_entry_outputs(entry, workload=...)`
4. `_restore_receipt(...)`
5. `_restore_output_material(...)` ×2
6. only then `saved_admission_factory()`, binding comparison and
   `JOINED_CHECKPOINT_SAVED_BINDING_MISMATCH`

Measured result:

```text
COMPLETED forged control: restore_output_calls_before_refusal = 0; refused
PARTIAL forged witness:   restore_output_calls_before_refusal = 2; refused
                          WorkloadAdmissionError: JOINED_CHECKPOINT_SAVED_BINDING_MISMATCH
```

Expected: the exact saved admission/type/binding/source check must run after fresh
CURRENT and **before** any protected entry/output material parse or restore in the
PARTIAL branch, as it already does for COMPLETED. The author regression
`test_saved_forged_checkpoint_binding_refused_before_restore` only constructs a
COMPLETED checkpoint, so it does not cover this branch.

The defect is reproducible on the exact cut and is material in-scope. HQ/owner
adjudication is required before any repair; this reviewer did not patch it.

## 4. Commands and observed results

| Check | Actual |
|---|---|
| Focused 36 (prior 29 + new 7) | **36 passed in 18.19 s** |
| Native 69 (Batch/S1-D current/checkpoint) | **69 passed in 67.17 s** |
| Full normal/partial/absent material parity (S3) | equal |
| Completed S3 facts/receipts/refs | equal; retained view has `summary=None` and different output-ref order |
| Integrated I03+I05 NORMAL (discovery) | final outputs/refs/receipts/summary equal |
| Integrated I05 route results | saved 0 vs normal 1; direct saved I05 intentionally bypasses Route B source |
| Fresh Batch child | 2 COMPLETED; manifest exact; result refs equal |
| Fresh normal/completed/partial/absent child | all return 0 in independent resource probe |
| Forged PARTIAL binding | defect reproduced (2 protected restores) |
| Forged COMPLETED binding | control refused with 0 protected restores |

Logs: `evidence/focused_36.txt`, `evidence/native_69.txt`,
`evidence/independent_parity.out`, `evidence/discovery_parity.out`,
`evidence/fresh_batch.out`, `evidence/forged_partial_binding.out`,
`evidence/resource_independent.out`, `evidence/diffs.txt`.

The normal saved path was also compared field-by-field, not by counts: manifest,
receipts, native outputs, output refs, summary, routes, envelope, decision, scope,
source SHA and outputs-by-unit all matched the normal source-backed owner on the S3
workload. The new author test's two-query workload has `discoveries=()`, so its
NORMAL test does not exercise I05; the independent discovery workload above does.

## 5. Seven-reader matrix

| Reader | Status |
|---|---|
| I03 | **PASS_SCOPED_ACTUAL_COLD** — prior 29 preserved |
| I05 | **PASS_SCOPED_ACTUAL_COLD** — prior 29 preserved; integrated final parity |
| Batch | **PASS_SCOPED_ACTUAL_NATIVE_SCHEDULER** — actual runner, fresh child |
| NORMAL | **PASS_SCOPED_ACTUAL_ISSUED_PATH** — full material parity; integrated I05 final parity |
| COMPLETED | **PASS_SCOPED_ACTUAL_RESUME** — facts/receipts/refs retained; retained-view note |
| PARTIAL | **FAIL_SCOPED** — forged binding restores protected outputs before refusal |
| ABSENT | **PASS_SCOPED_ACTUAL_RESUME** — full parity |

`PARTIAL` positive execution itself works; it is the G3 negative ordering that fails.
The packet is therefore not `ACCEPT_SCOPED@S2_SOURCEFREE_SAVED_NATIVE_ALL_READERS`.

## 6. G1–G5

- **G1 PASS_SCOPED:** owner-integrated five paths, exact saved estate/release/source,
  actual native owners, ordinary C11 path and legacy source path preserved.
- **G2 PASS_SCOPED:** actual cold normal/completed/partial/absent, fresh child,
  changed/restored facts/receipts/replays; I03+I05 final parity.
- **G3 FAIL_SCOPED:** forged PARTIAL binding restores two protected outputs before
  refusal. Other tested current/source/release/scope/foreign-source/missing-body and
  forged-COMPLETED negatives pass.
- **G4 PARTIAL_HOLD_EXTERNAL:** independent 4x2 probe measured retained `320,740 B`,
  observed peak staging `555,743 B` (1 ms sampler), parent RSS `122,609,664 B`,
  max single-child RSS `66,641,920 B`, source/build calls `0`, no orphan PIDs,
  normal `0.1124 s`, partial `0.0710 s`, resumes `0.0361/0.1010/0.1257 s`.
  Process-tree aggregate RSS, bounded object count and SIGKILL crash injection were
  **not captured**; 100k/6 GiB **NOT_RUN**. No 6 GiB production claim.
- **G5 REVISE_EXACT_DEFECT:** one runnable first-reader counterexample; completed
  control clean.

The author resource probe reported parent RSS only and `peak_staging: null`; it did
not measure the new five-reader child RSS or the actual `.s2c-stage-*` peak. The
author handoff correctly discloses child RSS as missing, but `G4 PASS_SCOPED` is not
fully supported by that probe. Our independent probe supplies bounded fields above,
not a process-tree aggregate.

## 7. Preservation / no-loss

- Batch diff is only the typed `__init__` guard; `run`, schedule, receipt/state and
  science behavior unchanged. Native Batch regressions pass.
- Issued-workload current resolver API, host/purpose, envelope/source/expected jobs,
  currentness/revocation and legacy `source_factory` path unchanged. Native 69 pass.
- Saved checkpoint binding is optional; legacy checkpoint hashes remain unchanged.
- Accepted S2-C code/tree/layout/tests unchanged; prior 29 source-scope and negative
  tests pass.
- Source-scope finding `G5-S2D-SCOPE-WHITELIST` remains **CLOSED_CORRECTED** and was
  not reopened.
- The five old ownership holds are **resolved** by the actual ACK; they are not carried
  forward as missing authority. The blocking item is the reproduced new defect.

## 8. Self-critique and limits

- The decisive finding is a protected-read ordering defect, not a positive fact leak;
  no forged output is served by the current code. It is still material because the
  original contract requires refusal before protected restore/serve.
- The discovery saved path intentionally returns `route_results=()` because it bypasses
  Route B source. Final I05 facts/receipts/refs match; full route-object parity is not
  claimed.
- COMPLETED retained discovery output uses the existing `RetainedDiscoveryResultView`
  (refs rather than executed objects) and `summary=None`; facts/receipts/refs match.
- Author fresh child covers normal/completed/partial/absent, not Batch; our fresh Batch
  witness covers Batch. Author forged-binding coverage is COMPLETED-only; our PARTIAL
  witness is the defect.
- Resource evidence is fixture-scale; process-tree aggregate, object count, SIGKILL
  recovery and 100k/6 GiB remain unproven. New modules were not run on Linux.
- No original35 source/respondent, production CURRENT, science, Q2/S1-E fate join,
  S2-B G5-R1 or protected merge is accepted or claimed.
- Integration remains **UNMERGED**.

## 9. Next actor

HQ/owner adjudicates the exact PARTIAL binding-order defect. The only bounded correction
would be to move the exact saved binding/type/source checks before the PARTIAL
`_validate_entry_*`/restore calls and add a PARTIAL forged-binding regression, then
freeze and have this distinct G5 re-receive. No new A/B round, optional hardening,
reviewer patch or protected merge. Stop finite.

Return: `WORKER_RETURNS/PYAT991_ALL_SEVEN_G5/`.
