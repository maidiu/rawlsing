# PYAT HQ280 PV3 B01C — Source-free durable WRITE_AHEAD checkpoint/recovery CANDIDATE

**TERMINAL:** `HQ280_PV3_B01C_SOURCEFREE_DURABLE_CHECKPOINT_CANDIDATE_RETURNED__NO_REAL_SOURCE_ADOPTION__GITHUB_PUSHED`
**RESULT:** `PASS__CANDIDATE_ONLY__DURABLE_CHECKPOINT_WORKS_AGAINST_REAL_ACCEPTED_RUNNER__35_TESTS_PASS__19_OF_19_CASES_MET__5_REAL_SIGKILL_SCENARIOS_EXECUTED__EXACTLY_ONCE_NOT_CLAIMED__UNKNOWN_OUTCOME_HELD__SOURCEFREE_ONLY__NON_ISSUING`

**Branch:** `agent/rabochii-pyat-hq280-pv3-b01c-durable-checkpoint-candidate-r1`
**Sealed startup (verified exact before mutation):** `923e2c1d0ff27961233c52c385f672bbd1a4f23c`
**Grounded in B01 measured return:** `agent/rabochii-pyat-hq280-pv3-b01-runtime-restart-capacity-r1 @ 2e317aa5fbabac8a8fa78bf85069ab30f69d3db7`
**Authority:** HQD-2026-10-10-280; canonical `a70a069fa948e0f3c041b389edcc732b6b948a4f`; semantic PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390` (**unmutated**); HQ seal intake `e10a785af0fc86799588000331349b1f0ec82bdf`.

## 1. Headline

The two B01 blockers were re-verified independently, and a **standalone candidate** now supplies the missing capability without touching a single accepted owner:

- **F-01 re-verified:** `pre553_batch_runner.py` contains **zero** file-write operations. Receipts exist (`UnitExecutionReceipt`, `attempt_index`, `prior_receipts`) but nothing is persisted. Independently confirmed: `grep -c "open(" pre553_batch_runner.py` → `0`.
- **F-02 re-verified:** `rabochii_execution_protocol.py` requires `checkpoint_state.mode == "WRITE_AHEAD"` plus a `durable_checkpoint_ref` for `REAL_EXECUTION`. The candidate supplies exactly that vocabulary and a real digest-backed ref — **without relaxing the validator**.

**A further real defect was found in the existing pattern:** the proven EE-P2X `StageLedger` atomic writer (`ee_p2x_darwin_court_driver.py:501-508`) does `write → fsync(file) → os.replace` but **never fsyncs the parent directory**. After `os.replace` the rename is not durable until the directory entry is synced. The candidate closes this gap (`_fsync_dir`).

## 2. What was built

Two NEW files plus the return packet. **No accepted owner modified** — `git diff --name-only 923e2c1d… -- rawlsing_next/` is **empty**.

| File | Role |
|---|---|
| `rawlsing_next/pre553_batch_durable_checkpoint_candidate.py` | the durable checkpoint adapter candidate |
| `rawlsing_next/tests/test_pre553_batch_durable_checkpoint_candidate.py` | 35 tests |
| `WORKER_RETURNS/…/repro/b01c_worker.py` | real subprocess worker, genuinely SIGKILLable |
| `WORKER_RETURNS/…/repro/b01c_evidence_recorder.py` | real kill/restart + hostile recorder |

It is an **adapter around the accepted runner**, not a replacement scheduler: it emits `UnitExecutionReceipt` values and hands them back through `BatchExecutionRunner(prior_receipts=…)`.

## 3. Real process kill / restart — actually executed

Not parsed JSON: real temp dirs, real files, real signals.

| # | Scenario | Observed |
|---|---|---|
| 1 | Real **SIGKILL** after durable intent | returncode **-9**, 1 durable `START_INTENT_WRITTEN` on disk, `recovery_safe=False`, **held=1, rerunnable=0** |
| 2 | Partial run then **fresh-process restart** | 2 committed → restart → **4 committed**, prior work preserved, 0 held |
| 3 | Restart attempt on an already-committed unit | returncode 1, **`already committed` refused** |
| 4 | Second real writer while lock held | **`REFUSED`** |
| 5 | Real on-disk truncation then real probe | **probe refused** |

Scenario 1 is the decisive one: after a genuine `SIGKILL`, the candidate classifies the unit as **UNKNOWN_OUTCOME and HELD**. It does **not** silently rerun.

## 4. The exactly-once hazard — stated plainly

**A write-ahead intent alone does NOT prove exactly-once external execution.** After a crash between an owner side effect and the durable COMMITTED record, the true outcome is genuinely unknown. The candidate encodes this rather than papering over it:

| Recovery state | Disposition |
|---|---|
| durable COMMIT + receipt rehydrates | `ALREADY_COMMITTED` |
| START intent, **no** idempotence proof | **`UNKNOWN_OUTCOME` → HELD** |
| START intent, explicit idempotence proof | `RERUN_SAFE` |
| never started | `NEVER_STARTED` |

`write_ahead_intent_alone_is_NOT_exactly_once` is an **expected-false** case and it passed as such. `checkpoint_effect_flags()` includes `claims_exactly_once_external_execution: False`.

**This source-free PASS is NOT REAL_EXECUTION protocol approval.** That remains a competent owner's act.

## 5. Durability and tamper — 19/19 cases met expectation

Atomic write (`tmp → fsync(file) → os.replace → fsync(dir)`) with no `.tmp` residue and byte-stable repeat writes; torn/truncated refused; sequence tamper refused; foreign manifest refused; foreign release refused; forged receipt digest refused; foreign unit smuggling refused; completed unit not restartable; commit-without-intent refused; committed receipts admitted to the accepted runner with `batch_state == COMPLETED`.

## 6. Governance

`git diff --name-only 923e2c1d… -- rawlsing_next/` → **empty**. The accepted batch runner and the execution protocol are untouched; the candidate imports neither the protocol module nor any validation surface, and performs no monkeypatching. `find . -name '*.sav' -o -name '*.dta'` → **0 files**, so the source-free posture is structural, not merely asserted.

**Tests:** 35 B01C pass; **69** pass across B01C + accepted batch runner + accepted execution protocol; **102** pass including Route B, I05 exact and I05 adaptive. No `.pyc` or test residue committed.

## 7. Limits and holds

- **Exactly-once external execution is NOT proven** — only the safe HOLD behaviour is proven.
- Bounded scale only: 4 units, 4-row manifest. Peak RSS 25.9 MiB, ~0.25 s user CPU. **No capacity or 35-wave forecast.**
- `RERUN_SAFE` depends on a **caller-supplied** idempotence proof; the candidate cannot verify idempotence of an arbitrary owner itself.
- Recovery assumes a **single writer** enforced by `flock`; it does not provide distributed consensus.
- B01's P17 identity caveat (adaptive `checkpoint_ref` sensitive to visit order) is **inherited unchanged** — safety holds, identity determinism does not converge. This candidate does not alter adaptive checkpoint semantics.

## 8. Required follow-up before any real launch

A competent owner must (a) accept or reject this candidate, (b) supply per-executor idempotence proofs or accept permanent HOLD for non-idempotent work, (c) decide whether REAL_EXECUTION protocol approval is warranted, and (d) resolve B01's F-04/F-05/F-06 separately. **No self-adoption, no canonical mutation, no ZIP relay.**

**Terminal:** `HQ280_PV3_B01C_SOURCEFREE_DURABLE_CHECKPOINT_CANDIDATE_RETURNED__NO_REAL_SOURCE_ADOPTION__GITHUB_PUSHED`.