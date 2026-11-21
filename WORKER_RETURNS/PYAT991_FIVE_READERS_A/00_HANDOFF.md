# PYAT991 S2-D — five remaining native saved readers

## Result

**`READY_FOR_RECEIVING` at `S2_SOURCEFREE_SAVED_FIXTURE`.**

The owner ACK resolved the five shared-file holds. The same accepted S2-C estate now drives all seven existing first readers:

- I03, I05
- actual `BatchExecutionRunner`
- actual `execute_issued_workload` NORMAL path
- actual `resume_joined_workloads` COMPLETED / PARTIAL / ABSENT

This is not self-acceptance and not protected merge. A distinct nonauthor G5 is required.

## Exact artifact and ownership

- Branch: `agent/pyat991-s2d-a-r1`
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat991-s2d-a`
- Startup / owner ACK delivery: `b32f215660def205762f0e9d0eafa2c3dfaa0c36`
- Qualified saved baseline: `5478210b7aeedf608a3e9754bf891d4d0262817f`
- Accepted S2-C executable/tree: `b7b697b69f0acea12174937ee824c19ac34ac284` / `dc416d1f23100d4d52b19bc2120226964bc0be43`
- Contract: `S2-D_PHASE1_USER_20261113.md@d7eaaf2363312af96e9bea02f6d85ae69a8cc47f`, SHA-256 `37d4b7e2…`
- Owner ACK: `WORKER_RETURNS/PYAT991_OWNER_HANDOFF/owner_ack.json`, status `ACK`, blob `dae76ff1…`

Shared files changed under the exact ACK:

- `rawlsing_next/pre553_batch_runner.py`
  - `BatchExecutionRunner.__init__` and only typed saved-release admission.
  - `saved_mode=True` is required for a `SavedC11Admission`; the ordinary `C11Repository` path remains unchanged. This preserves the existing guard behavior for callers that do not opt into saved mode.
- `rawlsing_next/pre553_issued_workload.py`
  - `execute_issued_workload`: optional lazy `saved_admission_factory`, called only after fresh `admit`; skips source factory, Route B source read and full C11 construction.
  - `resume_joined_workloads`: same saved path for absent/partial; completed validates saved binding after fresh current.
  - `JoinedWorkloadCheckpoint` / `capture_joined_checkpoint`: optional exact `SavedBindingReceipt`; omitted for legacy checkpoints, so legacy material/hash behavior remains unchanged.
  - Existing current resolver API, host/purpose, envelope, source SHA, expected jobs, currentness/revocation and legacy source path are unchanged.
- `rawlsing_next/pre553_saved_c11_admission.py`
  - exact release/source/replay/current properties; only previously qualified scope/semantics.
- `rawlsing_next/pre553_saved_workload_integration.py`
  - actual Batch wrapper using `BatchExecutionRunner`; actual normal/resume wrappers using the issued owner. Old no-argument probes remain only as compatibility holds; actual calls use the owner paths.
- New `rawlsing_next/tests/test_pyat991_s2d_five_readers.py`.

No S2-C writer/reader/layout/test, native scientific owner, issuer, source, or prior return was modified.

## Five actual paths

### Batch
`execute_saved_batch(admission, manifest=..., predicate_ref_by_query=...)` runs the existing `BatchExecutionRunner` with `saved_mode=True`; each unit calls the saved I03/I05 owner, current is checked before and after each unit, and existing manifest/schedule/receipt/state logic is untouched.

### NORMAL
`execute_issued_workload(..., saved_admission_factory=...)`:
- `admit` runs first;
- source factory and full C11 build are never called;
- the factory opens the saved estate only after current admission;
- existing Batch/I03/I05 owners execute;
- manifest, receipts, output refs and facts match the legacy native result.

### COMPLETED
`capture_joined_checkpoint((full,), saved_binding=...)` → fresh `resume_joined_workloads` → current rechecked → saved binding verified → existing `_completed_entry_view` serves retained results without rebuild.

### PARTIAL
`max_units=1` saved run → checkpoint PARTIAL with exact prior receipt/output prefix and binding → fresh resume executes only remaining units; final output refs match the uninterrupted result.

### ABSENT
Empty checkpoint with exact binding → fresh resume executes the intended workload against the same estate; no false ABSENT and no source/full graph.

## Fresh-process evidence

`test_saved_normal_and_completed_survive_fresh_process` runs **normal, completed, partial and absent** in child interpreters using only:

- the saved estate root/pins,
- exact release/I02 roots,
- serialized public workload/current/checkpoint material.

The child opens the saved admission lazily after current admission, never receives the source or a C11 repository, and returns exact output refs. Prior I03/I05 fresh-process tests remain in the 36-test focused suite.

## Commands and results

```text
python3 -m pytest \
  test_pre553_direct_estate_i03.py \
  test_pyat991_s2d_saved_admission.py \
  test_pyat991_s2d_b_adversarial.py \
  test_pyat991_s2d_a_counter.py \
  test_pyat991_s2d_g5_source_scope.py \
  test_pyat991_s2d_five_readers.py -q -o addopts=''
# 36 passed in 15.65s
```

Relevant native owner regressions:

```text
python3 -m pytest \
  test_pre553_batch_runner.py \
  test_pyat940_s1d_current_permissions.py \
  test_pyat940_s1d_a_counter_cache_binding.py \
  test_pyat940_s1d_b_cache_custody.py -q -o addopts=''
# 69 passed in 60.67s
```

Logs: `focused-36.txt`, `native-69.txt`.

## Resource evidence

Five-reader probe on the S1-D/S3 sourcefree fixture (4 respondents / 2 occasions; not 100k):

| Measure | Value |
|---|---:|
| Retained disk | `320,656` B |
| Peak root tree | `320,656` B |
| Peak staging | not separately captured |
| Normal | `0.1357` s |
| Partial | `0.0693` s |
| Completed resume | `0.0360` s |
| Partial resume | `0.0939` s |
| Absent resume | `0.1170` s |
| Parent peak RSS | `119,582,720` B |
| Child process peak RSS | not captured by this probe; prior independent G5 child `52,043,776` B |
| Source opens | `0` |
| Full C11 builds | `0` |
| Whole-table fallbacks | `0` |
| 100k / 6 GiB | `NOT_RUN` |

The fresh-process test proves exact child outputs; the probe reports parent RSS and does not claim a multi-process tree benchmark.

## Seven-reader matrix

| Reader | Status |
|---|---|
| I03 | **PASS_SCOPED_ACTUAL_COLD** |
| I05 | **PASS_SCOPED_ACTUAL_COLD** |
| Batch | **PASS_SCOPED_ACTUAL_NATIVE_SCHEDULER** |
| NORMAL | **PASS_SCOPED_ACTUAL_ISSUED_PATH** |
| COMPLETED | **PASS_SCOPED_ACTUAL_RESUME** |
| PARTIAL | **PASS_SCOPED_ACTUAL_RESUME** |
| ABSENT | **PASS_SCOPED_ACTUAL_RESUME** |

## Negative and preservation evidence

New five-reader coverage includes:

- revoked current before admission factory;
- source-factory tripwire never called on saved normal;
- missing checkpoint binding;
- checkpoint with binding but no saved admission;
- coherently rehashed forged checkpoint binding refused before restore;
- source/universe/release scope positives/foreign negatives from the prior 29 tests;
- I05 zero/valid-empty/mixed frontier and current revocation from B/A evidence;
- legacy native batch/issued/current/checkpoint regressions 69 pass.

The old 36 focused tests (including the two-reader scope corrections) remain green.

## Grades and holds

- Engineering: `S2_SOURCEFREE_SAVED_ALL_SEVEN_FIXTURE_ACTUAL__PENDING_G5`.
- Scientific: `NONE_VERIFIED`; TEST_ONLY sourcefree only.
- Authority: `TEST_ONLY_SOURCEFREE`; production current/issuer and original35 remain HOLD.
- G1–G4: **PASS_SCOPED** at the saved fixture grade.
- G5: **NOT_RUN**; distinct nonauthor receiver required.
- Integration: **UNMERGED**.
- Production CURRENT, original35 source/science, Q2/S1-E body-sink/fate join, S2-B G5-R1, integrated 100k/6 GiB and protected merge remain external holds.

## Self-critique

- The fresh-process capsule uses a test-only lightweight projection transport because the full test projection is not JSON-serializable; the saved estate, current admission, actual issued/Batch/resume owners and output identity are genuine, but this is not a production source-stream handoff.
- The owner ACK is limited to the two named files; no broader shared edit was made.
- `BatchExecutionRunner` requires explicit `saved_mode=True`; the old C11 guard behavior is preserved intentionally.
- The old no-argument integration probes remain for compatibility (they raise typed holds); actual calls with arguments execute the owner paths.
- Child RSS is not captured by the five-reader probe; prior independent G5 child evidence is cited separately.
- No Linux run of the new five-reader modules; no integrated 100k/6 GiB.
- An unrelated historical test outside the relevant S1-D suite has a pre-existing missing-resolver call; it is not counted as this packet's evidence.

## Stop

All seven actual readers are implemented at the sourcefree saved fixture grade and ready for distinct nonauthor G5 review. No new A/B round, no self-acceptance, no protected merge.
