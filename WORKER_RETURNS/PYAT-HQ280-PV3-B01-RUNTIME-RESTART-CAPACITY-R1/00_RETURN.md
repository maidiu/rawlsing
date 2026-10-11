# PYAT HQ280 PV3 B01 — Measured execution and restart envelope

**Agent:** independent local Python/runtime investigator
**Commission:** `WORKER_COMMISSIONS/PYAT-HQ280-PV3-B01-RUNTIME-RESTART-CAPACITY-R1/00_COMMISSION.md`
**Governing authority:** HQD-2026-10-10-280
**Sealed startup (verified exact):** `150033139132a801c0cb22cb896e70d783a3a1bc`
**Branch:** `agent/rabochii-pyat-hq280-pv3-b01-runtime-restart-capacity-r1`
**Scope:** SCOPED_NONAUTHORIZING_DEVELOPMENT_DOCUMENTARY_EXECUTION

---

## Headline

Rawlsing's existing source-free Route B / C11 / I03 / I05 / batch / replay machinery is **runnable,
fast and reproducible**, and its **recovery semantics are sound**. It is **not** launch-ready for governed
real-source work, for one structural reason: **there is no durable checkpoint** in that entire family, and
the written execution protocol mandates one that no owner code implements.

I ran real bounded workloads and real hostile probes. Everything below was executed and observed; nothing
is an anticipated failure dressed up as a test.

## Measured envelope

| Scope | Result | Wall | Peak RSS |
|---|---|---|---|
| Source-free core owner suite (Route B, C11, I03, I05, batch, bounded runtime) | **178 passed, 0 failed** | 4.44 s | 32.78 MiB |
| Whole `rawlsing_next/tests` tree | 3216 passed / 58 failed / 15 errors | 18m08s | 1.49 GiB |
| B01 hostile harness (24 probes) | **20 PASS, 0 FAIL**, 4 typed non-pass | 2.15 s | 69.3 MiB |

**Scaling (batch orchestration, synthetic executor):** ~145–149 µs/unit, flat across a 64× size range, and
~6.2 KB/unit resident, verified to 200,000 units (1.17 GiB, ~48 s). Linear in both time and memory.
This bounds *orchestration* cost only — **no 35-wave forecast is made or implied.**

## The two blocking findings

**F-01 — no durable checkpoint.** `pre553_batch_runner.py` has complete receipt machinery
(`UnitExecutionReceipt`, `attempt_index`, `prior_receipts`) but persists nothing: zero file-write
operations across all seven owner modules in that family. Measured consequence: with no caller-supplied
receipts, a fresh runner redoes **all** work (B01-P20). Recovery is entirely caller-owned, and
`projection()` emits plain dicts, so the caller must rebuild every `ExactRef` by hand — there is no owner
`from_dict`. A working pattern already exists at `ee_p2x_darwin_court_driver.py` (`StageLedger`, atomic
fsync+`os.replace`, `--resume`, `fcntl.flock`) but is coupled to the EE-P2X court.

**F-02 — the protocol mandates what the code lacks.** `rabochii_execution_protocol.py:300–323` requires a
`WRITE_AHEAD` `checkpoint_state` with `durable_checkpoint_ref` for any `REAL_EXECUTION` profile. A
repo-wide search finds those tokens **only in that validator and its own test**. Any real-execution claim
today would run ahead of the implemented capability.

## What held up well

Under genuine interruption, deferral, retry, **real two-process loss**, byte tampering, stale-manifest
replay, cache priming and concurrent runners, the owners never skipped work, never double-counted a unit,
and never forged completion. Duplicate publication is prevented structurally: completed units are not
retryable, attempt indices must be contiguous, and the runner has **no cache parameter at all**, so a cache
cannot be laundered into a receipt. The I05 adaptive checkpoint survives a real disk round-trip with a
stable identity — the strongest restart-grade result I measured.

One honest identity caveat (B01-P17): a rewritten adaptive checkpoint re-executes an *equal* work set and
reaches the *equal* terminal state, but yields a **different checkpoint ref** because checkpoint identity
is sensitive to visit *order*. Safety holds; identity determinism does not converge, and `from_dict`
does not itself reject the tampered dict.

## Operational and repo defects found

- **F-03** — the worktree must be byte-clean for part of the suite; `require_clean_worktree` fails on any
  `git status --porcelain` output. Proven by A/B re-run (1 failed → **15 passed**), not assumed. Two
  aggravating facts: `.gitignore` does not cover `.venv*`, and **4 `.pyc` files are tracked in git**.
  *(I removed those tracked files by mistake mid-run and restored them with `git checkout -- .`; the
  worktree is verified byte-clean and nothing tracked was altered.)*
- **F-04** — 17 tests exceed 60 s; the real-material C11 path is the worst and drives suite cost.
- **F-05** — three modules cannot be collected at all: two import files that **do not exist in the repo**.
- **F-06** — 19 failures are **not** explained by custody/HEAD/dependency/clean-tree causes. I did not
  adjudicate them and make **no** claim that they are benign.

## Custody and holds

Python 3.11.3 in an **isolated venv placed deliberately outside the worktree**; system Python untouched
(it had no pytest). pytest 8.3.4 + pandas/pyarrow/pytest-timeout recorded exactly in
`01_ENV_CODE_DEPS_CUSTODY.json`. **Zero `.sav`/`.dta` files exist in this worktree** — the source-free
posture is structurally guaranteed, not merely asserted. No raw source opened, no source-use grant
requested or claimed, no unbounded stress, no worktree deletion, no git gc, no canonical mutation, no
parallel worktree disturbed.

## Recommendation

Resolve **F-01** and **F-02** at their owners before any governed real-source launch. Apply the
host-specific tripwires in `04_...HOLDS.md` §5 in the meantime. Do not treat the 15
`HEAD_RELATIVE_IDENTITY` or 15 `MISSING_HISTORICAL_ARTIFACT_CUSTODY` failures as evidence that the
underlying logic is correct — they are environment and custody states.

## Return contents

| File | Contents |
|---|---|
| `00_RETURN.md` | this summary |
| `01_ENV_CODE_DEPS_CUSTODY.json` | interpreter, venv, exact dependency install, owner blob SHAs, custody |
| `02_ACTUAL_RUN_AND_RESOURCE_MEASURES.json` | every run, command, wall/CPU/RSS, failure taxonomy, scaling |
| `03_RESTART_CANCELLATION_CACHE_TESTS.json` | 24 probes with the owner call actually invoked |
| `04_EXECUTION_SAFETY_AND_SOURCE_WARRANT_HOLDS.md` | holds, blockers F-01..F-06, tripwires |
| `05_MANIFEST.json` | byte-hash receipts for every returned file |
| `repro/b01_harness.py` | the hostile harness (no owner source modified) |
| `repro/b01_memory_bench.py` | isolated per-size peak-RSS benchmark |
| `repro/harness_results.json` | machine-readable probe results |
| `repro/logs/*.txt` | raw pytest and harness logs |

**Terminal:** `HQ280_PV3_B01_MEASURED_EXECUTION_AND_RESTART_ENVELOPE_PUSHED__NO_RAW_SOURCE_RUN`
