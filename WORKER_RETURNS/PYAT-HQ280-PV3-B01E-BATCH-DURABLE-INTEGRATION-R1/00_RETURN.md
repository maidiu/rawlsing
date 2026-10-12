# PYAT HQ280 PV3 B01E — Actual batch durable-checkpoint integration

**TERMINAL:** `HQ280_PV3_B01E_ACTUAL_BATCH_DURABLE_ADAPTER_SOURCEFREE_RUN_OR_PRECISE_HOLD__NO_REAL_EXECUTION_GRANT__GITHUB_PUSHED`
**RESULT:** `PASS__ADAPTER_JOINS_REAL_RUNNER_TO_DURABLE_JOURNAL__29_TESTS_PASS__3_REAL_SIGKILLS_MEASURED__7_OF_7_HOSTILES_DETECTED__B01D_FAIL_CLOSED_INHERITED__SOURCEFREE_ONLY__NON_ISSUING`

**Branch:** `agent/rabochii-pyat-hq280-pv3-b01e-batch-durable-integration-r1`
**Sealed startup (verified exact before mutation):** `2fb5e8cc9971fe05899bbbeff837cd6cd049a969`
**Inherited candidate:** B01D `ef93f014a157983e0f713c118ee3a95311c16292` (fail-closed repair, B01DR positive review `621607282bd13f23ab7bbf0d93f64b431d8f95ec`)
**Authority:** HQD-2026-10-10-280; canonical `a70a069fa948e0f3c041b389edcc732b6b948a4f`; semantic PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390` (**unmutated**).

## 1. Why a new adapter (proven, not assumed)

The commission allowed demonstrating that an existing owner already supplies
the integration. It does not, by measurement:

| piece | capability | gap (measured) |
|---|---|---|
| Accepted `BatchExecutionRunner` | real execution, prior receipts, contiguity law | **0 file-write ops** — persists nothing (B01 F-01, re-verified: `grep -c "open("` → `0`) |
| B01D durable candidate | atomic START/COMMIT journal, fail-closed recovery | **never invokes the real chain** — zero references to Route B/I03/I05 anywhere in its module or worker |
| Accepted owners collectively | each step exists | **no owner binds** manifest → durable journal → fresh-process resume → manifest reconciliation in one governed flow |

The new bounded adapter `pre553_governed_batch_checkpoint_integration_candidate.py`
(contracts `PYAT_HQ280_B01E_GOVERNED_BATCH_CHECKPOINT@1.0.0`) supplies exactly
that join: per unit, durable START → REAL owner call → durable side-effect
journal append → durable COMMIT of the owner's REAL receipt; on recovery,
rehydrated receipts into a fresh accepted runner plus outer-join manifest
reconciliation. It invents no scheduler, no receipt shape, no authority.

## 2. What was built (new files only — zero owner edits)

| File | Blob | Role |
|---|---|---|
| `rawlsing_next/pre553_governed_batch_checkpoint_integration_candidate.py` | `44807c6a287145507d7332138c944cd61da363bf` | the adapter |
| `rawlsing_next/tests/test_pre553_governed_batch_checkpoint_integration_candidate.py` | `2b362b04cfc01fd297768990209829b4fca4a83e` | 29 tests |
| `WORKER_RETURNS/…/repro/b01e_worker.py` | (return dir) | real-process worker, SIGKILLable at exact windows |
| `WORKER_RETURNS/…/repro/b01e_evidence_recorder.py` | (return dir) | evidence recorder |

`git diff --name-only <sealed> -- rawlsing_next/` lists **exactly these two
files**. B01D candidate, batch/protocol owners, A04T owners: byte-identical.

## 3. Genuine positive run (actual measured output)

Real source-free chain — accepted `_fixture` → `execute_route_b_production`
→ real C11 release → manifest of 2 QUERY + 1 DISCOVERY units bound to real
query/discovery/predicate refs → adapter drives the REAL
`CarrierNeutralResearchExecutor` through the ACCEPTED runner:

- manifest hash `7a9c5224b35e441366b5492784b2f8be42319719b4a3e23322c9b1e33a843908`
- batch `COMPLETED`, 3/3 executed (attempt 1, all `COMPLETED`), checkpoint
  sequence 6, side-effect journal 3 entries, reconciliation ok, pending empty
- Rehydrated receipts reproduce recorded digests byte-identically (saved).

**Command:** `PYTHONPATH=. python3 repro/b01e_evidence_recorder.py`

## 4. Real kills — three windows, all with genuine SIGKILL (exit -9/137)

| window | observed | resume |
|---|---|---|
| After START, before any effect | HELD, journal 0 (absence unprovable → still HELD) | 0 executed, 1 skipped-held, 2 blocked |
| After side effect, before COMMIT | HELD, journal **1** | 0 executed, journal **stays 1** — no duplicate externalization |
| After COMMIT (2 units) | 2 committed, safe | 1 executed → `COMPLETED`, reconciliation ok, journal 3 |

Partial-then-resume (no kill) completes without redo. Crash-after-COMMIT
recovery reuses receipts; committed units are never re-executed (redo is a
no-op, journal unchanged).

## 5. The schedule-pinning finding (measured consequence)

The accepted runner executes **head-anchored** (`run()` always takes the
first pending unit; no per-unit selection exists). A held-but-pending unit
therefore cannot be skipped over — any `run()` call would execute it — and
fabricating a skip receipt is forbidden. The adapter **stops at the first
held unit** (checked invariant: pending head must equal the intended unit,
else refuse loudly) and reports the suffix explicitly as
`blocked_behind_held`: never executed, never hidden, never omitted.

The same pinning forced a second, deeper finding: the B01D journal pins
**every** COMMITTED record, including DEFERRED/FAILED receipts, so a
deferred unit cannot be journaled for retry even though the raw runner would
permit one. The adapter therefore pins deferred/failed units too
(`pinned_deferred`, batch ends DEFERRED, never FULL) instead of silently
retrying possibly-effectful work. Both pinnnings are reported loudly; a
per-unit owner execution entrypoint that would allow selective resume does
not exist and is recorded as future work — **not** simulated around.

## 6. Hostile battery — 7/7 detected, all executed

Foreign manifest/release (probe refused) · torn file (load refused) ·
single-byte digest flip (load refused) · malicious serialization shapes
(wrong-schema → Foreign, array/non-JSON → Torn) · lock contention (second
real writer refused; lock released after holder SIGKILL) · forged caller
proofs incl. empty string (all HELD; B01D W6 regression at integration
level) · redo of committed batch (no-op, journal unchanged) · plus, in the
29-test suite: attempt-index substitution refused, stale-release promotion
refused, corrupt-receipt rehydration refused, saved-vs-simulated
distinction (intent-chain required), incomplete recovery executes nothing,
UNAVAILABLE conserved through kill/resume (missing-weight), no fabricated
nulls, concurrency, owner-integrity and posture checks.

## 7. Tests

- Integration suite: **29 passed** (real subprocesses throughout).
- Widest targeted run (integration + B01D 48 + batch + Route B + I05
  exact/adaptive + protocol + empirical query + carrier): **180 passed**.
- Resources (bounded, development scale — **not** a capacity forecast):
  peak RSS 14.48 MiB, user CPU 0.104 s, recorder wall ~11.4 s.

## 8. Ceilings and holds

Source-free only (0 `.sav`/`.dta`). No raw source read, no new source-use
permission, **no REAL_EXECUTION permission** (protocol unmodified and still
controlling), no exactly-once claim (only the safe HOLD and the demonstrated
no-duplicate-externalization), no self-adoption, no canonical/PRE-MAIN
mutation, no merge, no ZIP relay, no NFS/distributed claim. Unknown outcomes
stay HELD under `IDEMPOTENCE_ISSUER_HOLD` (inherited, still open); deferred
retries and per-unit selective resume are pinned/held as documented above.
A source-free PASS here is explicitly **not** protocol approval.

**Terminal:** `HQ280_PV3_B01E_ACTUAL_BATCH_DURABLE_ADAPTER_SOURCEFREE_RUN_OR_PRECISE_HOLD__NO_REAL_EXECUTION_GRANT__GITHUB_PUSHED`.