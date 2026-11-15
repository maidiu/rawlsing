# PYAT991 S2-D — PARTIAL binding-order repair and G4 observations

## Result

**`READY_FOR_RECEIVING` after exact repair; same independent G5 delta recheck required.**

The prior all-seven G5 `REVISE_EXACT_DEFECT` was exactly:

- **COMPLETED forged binding:** refused with 0 protected restores.
- **PARTIAL forged binding:** restored 2 protected outputs before refusing.

That ordering defect is corrected. On the final code, both branches refuse the coherently rehashed forged binding with **0** `_restore_output_material` calls. A legitimate PARTIAL still resumes its exact prefix and final native outputs.

The G4 observations previously missing are now banked at the fixed fixture, including sampled process-tree aggregate RSS, bounded family object count, source/full-build/whole-table counters, observed stage peak, and one controlled SIGKILL → fresh-process resume witness.

No self-acceptance, protected merge, original35, production CURRENT, or 100k/6 GiB claim is made.

## Exact artifact

- Branch: `agent/pyat991-s2d-a-r1`
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat991-s2d-a`
- Startup / G5 delivery: `f5b9c2acdb79b0bc9fabcf8eabcffe580611b34f`
- G5 reviewed candidate: `5df0bbdf3ec4c479724e74651a80d4861ab700a1`
- Owner ACK delivery: `b32f215660def205762f0e9d0eafa2c3dfaa0c36`
- Accepted S2-C: `b7b697b69f0acea12174937ee824c19ac34ac284`
- Contract: `S2-D_PHASE1_USER_20261113.md@d7eaaf23…`, SHA-256 `37d4b7e2…`
- Owner ACK: `WORKER_RETURNS/PYAT991_OWNER_HANDOFF/owner_ack.json`, status `ACK`

Changed product/test paths:

- `rawlsing_next/pre553_issued_workload.py` — PARTIAL ordering only plus the second fresh-current check.
- `rawlsing_next/tests/test_pyat991_s2d_partial_binding_order.py` — new focused regression.
- `WORKER_RETURNS/PYAT991_PARTIAL_BINDING_REPAIR/`.

No other product code, accepted S2-C writer/reader/layout/test, prior returns, or shared owner file was modified. The known dirty `WORKER_RETURNS/PYAT991_S2D_B/a_red_b_green.json` remains unstaged.

## Exact repair

`resume_joined_workloads` PARTIAL now does:

```text
fresh CURRENT require_unchanged
exact saved admission factory
  exact type
  exact checkpoint saved_binding
  exact current source hash
fresh CURRENT require_unchanged after saved binding
_validate_entry_material
_validate_entry_outputs
_restore_receipt / _restore_output_material
```

The saved binding/type/source checks are now before any protected entry/output parse/restore, matching the COMPLETED control. Existing current checks and legacy source path are preserved. No schema, scheduler, issuer or resume-engine rewrite.

## Canonical G5 witness

Before:

```text
completed forged: 0 protected restores
partial forged:   2 protected restores
error:            JOINED_CHECKPOINT_SAVED_BINDING_MISMATCH
```

After:

```text
completed forged: 0 protected restores
partial forged:   0 protected restores
error:            JOINED_CHECKPOINT_SAVED_BINDING_MISMATCH
defect:           false
```

The canonical harness returns exit 2 when `defect=false`; that is expected and is not a product failure. Raw evidence:

- `g5_before_repair.json`
- `g5_after_repair.json`
- `forged_partial_after.out`
- `canonical_g5_forged_partial.py`

The before JSON is copied from the prior independent G5 evidence; the after JSON is produced in this repair's own proofroot.

## Focused and legacy proof

```text
python3 -m pytest \
  test_pre553_direct_estate_i03.py \
  test_pyat991_s2d_saved_admission.py \
  test_pyat991_s2d_b_adversarial.py \
  test_pyat991_s2d_a_counter.py \
  test_pyat991_s2d_g5_source_scope.py \
  test_pyat991_s2d_five_readers.py \
  test_pyat991_s2d_partial_binding_order.py -q -o addopts=''
# 38 passed in 17.31s
```

Relevant native regressions:

```text
python3 -m pytest \
  test_pre553_batch_runner.py \
  test_pyat940_s1d_current_permissions.py \
  test_pyat940_s1d_a_counter_cache_binding.py \
  test_pyat940_s1d_b_cache_custody.py -q -o addopts=''
# 69 passed in 61.07s
```

New PARTIAL regression proves:

- coherently rehashed forged PARTIAL binding → 0 protected restores before refusal;
- COMPLETED forged control → 0 restores;
- legitimate PARTIAL → exact prefix/final output conservation;
- revoked CURRENT → no factory/restore.

## G4 observations — final fixed code

Probe: `resource_recovery_probe.py` on the S1-D/S3 synthetic 4 respondents × 2 occasions fixture; not 100k.

| Observable | Observed |
|---|---:|
| Retained disk | `320,484` B |
| Peak root tree | `320,484` B |
| Observed stage peak | `555,487` B |
| Stage sampler | 1 ms, 66 samples |
| Normal | `0.1322043` s |
| Partial | `0.0715802` s |
| Completed resume | `0.0357226` s |
| Partial resume | `0.1014868` s |
| Absent resume | `0.1253911` s |
| Parent peak RSS | `121,479,168` B |
| Parent-root process-tree aggregate sampled peak | `184,696,832` B |
| RSS sampling | 2 ms `ps` parent-root tree including live children; 91 samples |
| Bounded family objects yielded | `15` |
| Source-factory calls | `0` |
| Full C11 builds | `0` |
| Whole-table `pq.read_table` fallbacks | `0` |
| Orphan child PIDs | none |
| SIGKILL child return | `-9` |
| Fresh PARTIAL resume after SIGKILL | return `0`, exact output match |
| 100k / 6 GiB | `NOT_RUN` |

The checkpoint is the existing caller-owned immutable material; no new persistent store, journal, or crash policy was added. The crash witness kills only the exact owned child before resume, then a fresh process opens the same durable fixture checkpoint under a fresh current resolver.

Evidence:

- `final_g4_observations.json`
- `g4_run.out`

Limits: the process-tree aggregate is sampled, not an exact hardware maximum; one controlled SIGKILL is not a universal failpoint matrix; child lifecycle interleaving may miss a peak; no 100k or production claim.

## Seven-reader status

| Reader | Status |
|---|---|
| I03 | **PASS_SCOPED_ACTUAL_COLD** |
| I05 | **PASS_SCOPED_ACTUAL_COLD** |
| Batch | **PASS_SCOPED_ACTUAL_NATIVE_SCHEDULER** |
| NORMAL | **PASS_SCOPED_ACTUAL_ISSUED_PATH** |
| COMPLETED | **PASS_SCOPED_ACTUAL_RESUME__FORGED_REFUSAL_0_RESTORE** |
| PARTIAL | **PASS_SCOPED_ACTUAL_RESUME__ORDERING_REPAIRED__0_RESTORE** |
| ABSENT | **PASS_SCOPED_ACTUAL_RESUME** |

## G1–G4

- **G1 PASS_SCOPED:** all seven actual owner paths, exact estate/release/source, owner ACK respected, legacy path preserved.
- **G2 PASS_SCOPED:** actual normal/completed/partial/absent + I03/I05; fresh process; exact prefix/final parity and changed/restore.
- **G3 PASS_SCOPED:** exact G5 forged PARTIAL ordering defect repaired; zero protected restores; forged COMPLETED control, revoked CURRENT, wrong source/root/body, missing/foreign binding all refuse.
- **G4 PASS_SCOPED_FIXTURE:** all required local observables above; 100k/6 GiB remains NOT_RUN.
- **G5:** `READY_FOR_SAME_G5_DELTA_RECHECK`; no self-acceptance; same reviewer `ses_e30c25800ffeT8XbyTuHekRCme`.

## Self-critique

- The G4 process-tree number is a sampled aggregate, not an exact maximum.
- The crash witness is one controlled SIGKILL, not universal host/failpoint isolation.
- The checkpoint storage is caller-owned test custody, not a new production durability service.
- The saved path remains TEST_ONLY current; production issuer/current and original35 remain external HOLDs.
- The test-only fresh capsule and Duck projection transport remain test instrumentation, not a production source-stream handoff.
- No Linux run of the repaired modules.
- No integrated 100k/6 GiB or protected merge claim.

## Stop

The exact G5 PARTIAL ordering defect is corrected and the missing G4 observations are banked on the fixed code. Same nonauthor G5 recheck next. No new A/B round, no optional hardening, no protected merge.
