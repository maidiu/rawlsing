# PYAT R3 S1-C — Agent A counterattack execution and G5 handoff

**This is an execution/verification return, not a G5 ruling.**

- PR under test: https://github.com/maidiu/rawlsing/pull/975
- Agent A frozen HEAD: `779fea665829aae641a3f3d6b463f456c78f8316`
- Agent A code/test commit: `dae66cdf9f3846d237e0b1c3069cc17eb05b7746`
- B2 tested ancestor: `f011a7639c89ec07829521cff3824dcaf95b6e6e`
- Verified A census blob: `dd5bf3940083679612d73f98e6a7b7711c223fd5`
- Verified A test blob: `a19b0db5ea800af80aff86816e77e666f4acc72f`
- Runner evidence branch: `agent/pyat-r3-s1c-a-counter-runner-20261112-r1`
- Protected PRE-MAIN `6a5c12f04323d74001f9632063ec907f4fc4468e` was not touched.

## Actual execution result

Executed on an isolated local macOS 13.2.1 x86_64 runner with Python 3.11.3, in a detached worktree at `dae66cdf`, without modifying Agent A's branch.

| Suite | Result |
|---|---|
| Focused S1-C | **18 passed, 0 failed, 0 skipped** (94.53s) |
| Inherited R03/R61 | **22 passed** (107.84s) |
| Combined S1-B | **46 passed** |
| Combined S1-D | **59 passed** |
| Combined S2-F | **19 passed** |
| Combined shared C11/universal/empirical | **58 passed** |

The new test `test_s1c_a_counter_pending_severance_cannot_overissue_bounded_work` is in the collected 18 and passes. The B2 false-HELD and false-reason tests also pass unchanged.

## Pending-list attack: independently reproduced

With a genuine `budget=5` R61 frontier:

- Honest frontier: `PARTIAL`, 145 pending IDs, execution states `NOT_STARTED=164/PENDING=145`, **5 issued receipts, 11 native facts**, pending rows with receipts = 0.
- Attack: remove only `pending_operation_ids`; rows remain PENDING, budget state remains PARTIAL, and source/science/UNKNOWN/EXCLUDED/inventory-ledger census hashes remain equal.
- Direct existing R03→Batch/C11/I05 execution on the severed frontier: **150 receipts, +145 over budget**, 142 of 145 pending IDs received receipts, both native candidate and operation anti-joins remained **green**.
- Pre-repair B2 adapter: accepted the severed frontier, called the source factory once and issued 150 receipts. It also accepted a false `COMPLETE` budget state.
- Repaired Agent A adapter: refused with `PENDING_FATE_CENSUS_DRIFT` with **0 source-factory calls**; false `COMPLETE` refused with `BUDGET_STATE_FATE_DRIFT`.
- Restoration: exact checkpoint equality, frozen-census equality, operation-fate identity, 5 receipts and 11 facts.

This confirms Agent A's alleged defect and causal repair. **No runner repair was required or made.**

## Full B2 preservation

The full sourcefree fixture still executes 309 declared / 309 compiled / 309 receipt rows, with `ELIGIBLE=150`, `HELD=159`, 6 deferred records, 3 unsupported-runtime rows, **150 issued candidate receipts**, **330 native empirical facts**, 1 source-factory call and 1 bounded C11 build.

Focused run resource evidence: inner elapsed `5.465261s`, wall `95.1941s`, sampled process-tree peak RSS `189,599,744 bytes` (3199 samples).

## Authority / limitations

- Hard grade remains `TEST_ONLY_SOURCEFREE`.
- No original35 respondent source, scientific issuance, native-host CURRENT permission or protected merge was accessed.
- The two pending representations are now internally conserved. Sourcefree consistency still cannot independently certify an externally issued budget value absent from the frozen manifest.
- G5 is **NOT_RUN**; this worker is not the independent nonauthor reviewer.

## Required disposition

`S1C_A_COUNTER_REAL_RUN_PASS__SOURCEFREE_G1_G4_COMPLETE__READY_FOR_INDEPENDENT_G5`

## Next action

Hand immutable code/test commit `dae66cdf9f3846d237e0b1c3069cc17eb05b7746` and this runner evidence branch to one independent nonauthor G5 reviewer. Do not run another author contest. GitHub Actions remains billing-blocked; do not treat unstarted hosted jobs as test results.

Evidence: `WORKER_RETURNS/PYAT_R3_S1C_RUNNER_A_COUNTER/` (receipt, logs, attack evidence).
