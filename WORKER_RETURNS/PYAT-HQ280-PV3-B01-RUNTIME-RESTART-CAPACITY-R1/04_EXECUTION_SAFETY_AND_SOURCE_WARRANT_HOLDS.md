# PYAT HQ280 PV3 B01 — Execution safety, source-warrant holds, and residual blockers

**Commission:** `WORKER_COMMISSIONS/PYAT-HQ280-PV3-B01-RUNTIME-RESTART-CAPACITY-R1/00_COMMISSION.md`
**Governing authority:** HQD-2026-10-10-280
**Sealed startup (verified exact):** `150033139132a801c0cb22cb896e70d783a3a1bc`
**Branch:** `agent/rabochii-pyat-hq280-pv3-b01-runtime-restart-capacity-r1`
**Scope:** SCOPED_NONAUTHORIZING_DEVELOPMENT_DOCUMENTARY_EXECUTION

---

## 1. Proof discipline applied

Every hostile in `03_RESTART_CANCELLATION_CACHE_TESTS.json` records the owner call that was **actually
invoked** and the outcome **actually observed**. Where an owner operation does not exist, the entry is
labelled `NOT_EXECUTED_NO_OWNER_OPERATION` rather than described as a test that failed. No anticipated
failure is reported as an executed hostile test.

Three probes initially reported FAIL. In all three cases the defect was in **my harness**, not in owner
code, and each was diagnosed, corrected and re-executed:

| Probe | Apparent failure | Actual cause | Resolution |
|---|---|---|---|
| B01-P07 | stale checkpoint "ACCEPTED" | I built two **byte-identical** manifests, so the test was vacuous | Rebuilt with genuinely distinct units → `BatchIntegrityError: receipt manifest hash mismatch` |
| B01-P08 | tamper "not detected" | `receipt_hash` is **not** a member of `projection()`, so my string replace was a no-op | Mutated a real member (`result_refs[0].content_hash`) → identity changed |
| B01-P17 | tamper "ACCEPTED" | My **expectation was wrong**: checkpoint identity is visit-order-sensitive, not work-set sensitive | Restated the safety property as *equal visited set + equal terminal state*, and recorded the identity divergence as a finding |

No owner source was modified to obtain a PASS.

## 2. Source warrant holds — observed compliance

| Hold | Status | Evidence |
|---|---|---|
| No raw SAV/DTA execution | **HONOURED** | `find` for `*.sav`/`*.dta` across the worktree returns **0 files**. Nothing to open even accidentally. |
| No raw source read grant | **NOT REQUESTED, NOT USED** | All fixtures are synthesized in-process from `sha256(label)`. |
| Private primary custody (LR-A/B/C, WGE-R) | **NOT ACCESSED** | Hashes recorded from the seal for custody reference only. Not present locally, not fetched. |
| System Python unmodified | **HONOURED** | System `python3` at start had only `pip`+`setuptools`; all work used an isolated venv interpreter. |
| No unbounded stress | **HONOURED** | Largest manifest executed was 200,000 units in an isolated process. No stress loop. |
| No worktree deletion / no git gc | **HONOURED** | Neither performed. |
| Parallel A04/C02 undisturbed | **HONOURED** | No other worktree touched; no new clone or checkout created. |
| No canonical mutation | **HONOURED** | Only this return directory was written; `rawlsing_next/` byte-identical. |

## 3. Residual blockers for governed real-source workloads

These are the exact reasons a governed real-source launch is **not yet safe** on the current runtime.

### F-01 — No durable checkpoint in the batch/Route B family (BLOCKING)

The batch owner has complete receipt machinery (`UnitExecutionReceipt`, `attempt_index`, `prior_receipts`,
`pending_units()`) but **persists nothing**. Verified by direct source inspection: zero matches for
`open(`, `write_text`, `json.dump(`, `tempfile`, `os.replace`, `.mkdir(`, `fsync` in all seven of
`pre553_batch_runner.py`, `pre553_replay_audit.py`, `pre553_c11_repository.py`, `pre553_c11_integrity.py`,
`pre553_route_b_production.py`, `bounded_empirical_runtime.py`, `pre553_discovery_adaptive.py`.

Consequence, measured: **B01-P20** shows that with no caller-supplied receipts, the runner redoes **all**
work. Recovery is caller-owned. `UnitExecutionReceipt.projection()` also emits plain dicts, so rehydration
requires the caller to rebuild every `ExactRef` explicitly — there is no owner `from_dict`.

Reference implementation exists but is not wired to this surface:
`ee_p2x_darwin_court_driver.py` — `StageLedger` (line 756), atomic fsync+`os.replace` writer (502–510),
`--resume` (1095/1192/1294), `fcntl.flock` lock (802–810), terminal re-hash (790–800).

### F-02 — The written protocol mandates a checkpoint the code does not implement (BLOCKING)

`rabochii_execution_protocol.py:300–323` **requires** a `WRITE_AHEAD` `checkpoint_state` with
`durable_checkpoint_ref` for any `REAL_EXECUTION` profile, and forbids a volatile pending result from
coexisting with that ref. A repository-wide search for `PERSIST_CHECKPOINT` / `durable_checkpoint_ref`
matches **only this validator and its own test file**. No owner code creates one.

This is a documentation-versus-implementation gap. Any real-execution claim today would run ahead of the
implemented capability.

### F-03 — The worktree must be byte-clean to run parts of the suite (OPERATIONAL)

`fiabc_succession_producer.require_clean_worktree` (line 148) fails on **any** `git status --porcelain`
output, including untracked files. An isolated venv created *inside* the worktree, plus `__pycache__`,
made this test fail. Proven by A/B re-run, not assumed:

- with untracked venv + bytecode → `1 failed, 14 passed`
- venv moved outside the worktree, untracked bytecode cleared, `PYTHONDONTWRITEBYTECODE=1` → **`15 passed`**

Two aggravating repo facts, both confirmed:
- `.gitignore` does **not** cover `.venv*`.
- **4 `.pyc` files are tracked in git** (under `WORKER_RETURNS/PREMAIN-FIABC-...`). These are byte-code
  in version control; running the suite can dirty tracked files and trip the same clean-tree check.
  *(During this commission I removed these by mistake and restored them with `git checkout -- .`; the
  worktree is verified byte-clean and nothing tracked was altered.)*

### F-04 — Slow real-material path dominates cost (CAPACITY)

17 tests exceed 60 s. Worst observed:
`test_fiabc_lm2_r1h_real_material_c11.py::test_r15_real_candidate_neutral_common_c11`, which drives
`RoutingEligibilityFact` construction inside a WVS7 projection materializer and did not finish in 60 s.
Full suite: **18m08s wall / 1.49 GiB peak RSS**. Note wall (65.24 s) vastly exceeded user CPU (4.09 s)
during collection — import/collection cost, not compute.

### F-05 — Three source-free test modules cannot be collected at all (REPO DEFECT)

- `test_objective_consumer_bounded_evidence_d07.py` imports `rawlsing_next.tests.d07_bounded_loss_harness`
  — **that module does not exist in the repository.**
- `test_subv_e_obl059_positive_applicability_r13_independent_review_r1_corrected.py` loads a sibling test
  file that **does not exist**.
- `test_pre553_sr06_decoder_carrier.py` needs `pyreadstat`, which was deliberately **not** installed
  because it would write SAV/DTA files.

These are missing-artifact defects in the repo, not environment gaps.

### F-06 — Unadjudicated pre-existing failures (OPEN, NOT CLAIMED BENIGN)

Of the 58 failures, 12 (`OEEIntegrityError: reconstructed CAUSAL_USE_PERMISSION source does not match
exact stored OBL056 binding`) and 7 (`representation authority variable identity/ordinal mismatch`) are
**not** explained by custody, HEAD-pinning, dependency or clean-tree causes. This commission did **not**
adjudicate them and makes **no** claim that they are benign.

15 further failures are `HEAD_RELATIVE_IDENTITY` (frozen git-blob pins such as
`FAILURE__QUALIFIED_DRIVER_BLOB_DRIFT`) and 15 are `MISSING_HISTORICAL_ARTIFACT_CUSTODY` (governed
evidence JSON absent from this worktree). Both are environment/custody states, **not** proof that the
underlying logic is correct.

## 4. What is genuinely qualified

- **Source-free core suite: 178/178 passed, 4.44 s, 32.78 MiB** — reproducible and fast.
- **Batch orchestration scales linearly**: ~145–149 µs/unit (flat over a 64× range) and ~6.2 KB/unit
  resident, verified to 200,000 units (1.17 GiB, ~48 s). This bounds *orchestration* cost only and is
  **not** a 35-wave forecast.
- **Semantic safety of restart held under real execution**: no skipped work, no duplicated unit, no forged
  completion, across interruption, deferral, retry, process loss, tampering and cache priming.
- **I05 adaptive checkpoint survives a real disk round-trip with stable identity** (B01-P16) — the strongest
  restart-grade result measured here.
- **Cache is structurally non-authoritative**: `BatchExecutionRunner` has no cache parameter at all.

## 5. Recommended tripwires (evidence-based, host-specific)

Set on **this host only**, from measurements — not universal thresholds:

| Tripwire | Measured basis |
|---|---|
| manifest ≤ 200,000 units per process | largest size verified; beyond that is unmeasured |
| peak RSS ≤ 1.5 GiB per batch process | 1.17 GiB at 200k units; suite already peaked at 1.49 GiB |
| per-test wall ≤ 60 s, else investigate | 17 tests breach it |
| worktree byte-clean before any clean-tree-governed run | F-03, proven by A/B |
| never claim FULL_MANIFEST_COVERAGE without `actual_execution_receipts` | owner already enforces this |

## 6. Exact disposition

Runtime readiness of the source-free Route B / C11 / I03 / I05 / batch / replay machinery is
**measured and qualified at the orchestration and recovery-semantics level**, with **two blocking gaps**
(F-01 no durable checkpoint, F-02 protocol mandates an unimplemented write-ahead checkpoint) and
**operational/repo defects** (F-03 clean-tree coupling, F-05 uncollectable modules).

**No governed real-source launch is recommended** until F-01 and F-02 are resolved at their owners.
No raw SAV/DTA source was executed, no source-use grant is claimed, and no scientific, semantic,
model/use, G0b, EE12, actor/world or publishing authority arises from this commission.

**Terminal:** `HQ280_PV3_B01_MEASURED_EXECUTION_AND_RESTART_ENVELOPE_PUSHED__NO_RAW_SOURCE_RUN`
