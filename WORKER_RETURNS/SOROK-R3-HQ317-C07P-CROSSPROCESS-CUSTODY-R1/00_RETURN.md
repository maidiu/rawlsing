# SOROK HQ317 C07P — cross-process custody durability experiment

## VERDICT: `SOURCEFREE_C07_CROSSPROCESS_CANDIDATE_REQUIRES_I2`

**C07 moves from `NOT_REACHED` to genuinely executed** — with two typed dependency holds and an
explicit, demonstrated anti-tamper failure ceiling. **This is an experiment, not an acceptance.**

| | |
|---|---|
| **Role** | Bounded source-free custody implementation experimenter. **NOT** HQ, **NOT** an external escrow institution, **NOT** the OC7 accepting reviewer, **NOT** a semantic issuer, **NOT** a production actor. |
| **Branch** | `agent/rabochii-sorok-r3-hq317-c07p-crossprocess-custody-r1` |
| **Sealed startup** | `64f32aab9c0e2edc35e6b9120aca09fa9a7d0aff`, verified against direct remote HEAD |
| **Native source** | OC6 `c6cb15d7417595c359571e4525dd0f0fd6c59d1f`, blob `4c185c18dbee57603038e97886da8fc4aa834082`, SHA256 `ca85b844…` — **never edited** |
| **Accepted boundary** | OC7 `6e7d85d28f82729a06ede32d0440b63d0452a634` |
| **Preregistration** | `01_PREREGISTERED_PROTOCOL_R1.md`, frozen at `82ba75680f7cf296918c6236ef7c0e8df1756dde` **before any adapter existed** |
| **Environment** | New isolated local sparse worktree, real Python 3.11.3 / pytest 9.1.1 / Git 2.39.1, real subprocesses |
| **Model / editor** | Step 5 Preview in OpenCode (owner-selected). One agent, no helpers, no switches. |

---

## 1. What was actually built

A **return-local** adapter, `repro/c07_journal.py`. It does not wrap, patch or replace the pinned
custody source — it imports it and persists an authorised escrow event stream to a filesystem journal,
restoring it by **replaying the public `EscrowState` API only**. No internal dictionary is ever
assigned, no object is pickled, no authority is forged.

Journal: UTF-8 JSON Lines, one canonical record per line, `seq` contiguous, `prev`-chained, each
record sealed with an unkeyed SHA-256 `rec`. Capsules are stored as plain JSON of their 18 declared
fields and re-validated through the native `capsule_envelope_commitment` on restore.

Write protocol: temp file → `fsync` → `os.replace` → `fsync` directory. Both fsyncs observed
`SUPPORTED`; rename observed atomic on the same directory.

## 2. The headline result: a real cross-process handoff

| Step | Observed |
|---|---|
| Process A builds escrow through the public API | `['COMMIT','UNBLIND','RELEASE','EXPOSURE']`, `verify_ledger_integrity() == True` |
| Process A **exits** | journal on disk: 6 records, chain verifies |
| **Process B** — fresh interpreter, fresh import | **distinct PID**, module blob `4c185c18…`, sha256 `ca85b844…` |
| Process B restores via public API replay | `applied=6`, chain `ok`, `verify_ledger_integrity() == True` |
| Fingerprint A vs B | **identical** — committed, unblinded, holders, released, exposures, ledger ops, ledger seq |
| All 18 capsule fields | commitment **bit-identical** across the process boundary |
| Process B continues the lifecycle | second capsule committed, unblinded, released; integrity still `True` |

This is the first time C07 has been **executed** rather than described. OC7's `NOT_REACHED` was
accurate; it is no longer accurate for the narrow claim "escrow state survives an interpreter restart".

## 3. Crash injection — real `SIGKILL`, real filesystem state

Every crash role delivers an **uncatchable `SIGKILL` in place** inside the write protocol — no
unwinding, no flush, no `atexit`. Observed exit `137` at every point.

| Crash point | Journal | Temp | Restore | Committed | Preregistered verdict |
|---|---|---|---|---|---|
| 1 — after tmp fsync, before rename | 2 records (unchanged) | **orphaned** | succeeds | `['cap-A']` | `CLEAN_ROLLBACK` ✔ |
| 2 — after rename, before dir fsync | 3 records | absent | succeeds | `['cap-A','cap-C']` | `NOT_SETTLED` ✔ |
| 3 — after dir fsync | 3 records | absent | succeeds | `['cap-A','cap-C']` | `COMMITTED` ✔ |

**No torn or partial record was produced at any crash point.** Every journal parsed cleanly and the
hash chain verified after every kill.

### 3.1 Crash point 2 stays `NOT_SETTLED`, permanently

This was preregistered and it held. `SIGKILL` kills the *process*; the kernel page cache survives, so
post-rename bytes remain visible whether or not the directory entry was fsynced. Settling this needs
an actual power cut or a separate filesystem, neither of which is authorised here.

**Any future document treating crash point 2 as proven durability is wrong.**

## 4. The explicit anti-tamper failure ceiling

This is the most important thing in this return.

**Detected** (all refused with a specific typed error): tampered payload, deleted middle record,
reordered records, duplicated record, forged capsule substitution, uncommitted-capsule unblind or
exposure, ghost commitment, unauthorised holder, forged purpose, truncated trailing line.

**NOT detected — demonstrated deliberately:**

- **T5, whole-journal rollback.** The journal was rewound to the cap-A-only prefix and **re-sealed so
  it is fully self-consistent**. Restore succeeds, native integrity returns `True`, and `cap-B` is
  **silently lost with no error whatsoever**. Every prefix of a hash chain is itself a valid chain, so
  a prefix is indistinguishable from the truth without an external monotone counter.
- **An attacker who controls both state and digest.** `rec` is unkeyed SHA-256. Anyone with write
  access to the journal directory can alter a payload and recompute the whole downstream chain. These
  are **integrity checks against corruption and naive tampering, not authentication**. The same
  attacker can delete the journal outright.

What would actually close this: an **external append-only anchor**, a **key held outside the
journal's trust domain** (HSM, remote custody, threshold-signed log), or an **OS-protected store the
local process cannot recompute**. None exists here and none may be invented by a worker. That is
precisely the real institutional custody C07P is forbidden from faking.

**An unkeyed hash and an ordinary local file do not establish an external trust anchor.**

## 5. Two open typed dependency holds

Both derived from a **measured** API audit before implementation, both left open rather than worked
around.

| Hold | Missing interface | Consequence |
|---|---|---|
| `C07_DEPENDENCY_TS` | an optional `at: Optional[float]` on `unblind`/`record_exposure`, or a `replay_event(record, at=…)` entrypoint | `unblind` and `record_exposure` stamp `time.time()` internally with no parameter. The **journal** is time-faithful; the **reconstructed escrow re-stamps** escrow event times. Not fixed by rewriting the ledger afterwards — that would forge the authority under test. |
| `C07_DEPENDENCY_REVOKE` | a public `revoke_holder(person_id)` | `EscrowState` has `authorize_holder` but **no revocation counterpart**. A revoked custodian is not expressible through the public API at all, so it cannot be persisted or restored. `test_N16` proves the *absence* of the interface rather than pretending to test revocation. |

These narrow the result but do not block the core A/B demonstration, which is why the verdict is a
candidate with holds rather than a bare `C07_EXECUTION_HOLD`.

## 6. Hostile-suite integrity, including my own errors

The suite implements the preregistered P1–P10, N1–N12, C1–C4 and T1–T14. First execution gave
**6 failed / 24 passed**. Those 6 are **preserved** in `observations/c07p_suite_v1.{xml,log}` and
adjudicated individually in `04_TEST_CORRECTION_LEDGER.json`. **All 6 were defects in my own tests** —
not in the adapter, not in the pinned source. The most instructive: `isinstance(False, int)` is
`True` in Python, so my per-field perturbation turned a lifecycle bool into the integer `1` and
tripped native validation before reaching the assertion. Corrected v2: **30 passed / 0 failed**.

**An honest note on discrimination.** Unlike OC7, this suite does **not** discriminate the OC4 and
OC6 custody blobs — it exercises the additive adapter plus the native public API, which both blobs
expose (OC4 scores 28/30). Claiming blob-contrast discrimination here would be false. The correct
control for this suite is **adapter mutation**, which was run instead:

| Mutant | Change | Killed by | Result |
|---|---|---|---|
| A | neuter the per-record digest comparison | `test_N1_T1_tampered_payload_is_refused` | 1 failed / 29 passed |
| B | neuter the capsule-commitment re-check on restore | `test_N5_T6_forged_capsule_substitution_is_refused` | 1 failed / 29 passed |
| C | replace `os.replace` with a non-atomic plain write | `test_C3_crash_after_dir_fsync_is_committed` | 1 failed / 29 passed |

Each defence is independently load-bearing and killed by exactly its intended test.

## 7. Preservation of the accepted boundary

The adapter is purely additive and lives only in this return folder. Re-running the **complete**
accepted closure against the pinned OC6 source, 12/12 objects blob-verified from the true binary
preimage (two `.tar.xz` members extracted, not transcribed):

| Court | Cases | PASS | RED |
|---|---:|---:|---:|
| inherited 131 (OC1/OCR1/OC2/OC3) | 131 | 121 | **10** |
| OC4 author controls | 36 | 36 | 0 |
| OC5 prior predictions | 23 | 23 | 0 |
| OC5E native hostiles | 159 | 148 | **11** |
| OC6 author controls | 273 | 273 | 0 |
| OC7 independent v2 | 276 | 276 | 0 |
| **total** | **898** | **877** | **21** |

**Exactly the 21 literal REDs OC7 adjudicated** — the 10 historical contract REDs and the 11
superseded/malformed witnesses. **Zero skips, zero errors.** The lexical and Unicode leakage gate was
not widened. No accepted test was edited, xfailed or suppressed. The pinned source bytes are untouched.

## 8. What is explicitly NOT claimed

- No real third-party or institutional escrow, no external custody service.
- No cryptographically protected or externally anchored remote journal.
- No anti-tamper against an attacker who can rewrite both the state and the digest.
- No production durability — crash point 2 is `NOT_SETTLED`.
- No real signer, protected holdout, original respondent source or human perception.
- No semantic adoption, and no widening of the lexical/Unicode leakage gate.
- No production, V3, N12, CURRENT or PRE-MAIN admission.
- **No adoption.** A **distinct future independent review is mandatory**, and the author does not
  accept this work.

## 9. Artifact map

| Path | Purpose |
|---|---|
| `01_PREREGISTERED_PROTOCOL_R1.md` | protocol, threat model, crash matrix, P1–P10 / N1–N12, holds — frozen at `82ba75680` **before any adapter existed** |
| `freezes/01_PREREG_FREEZE.json` | freeze binding + expectation index |
| `02_CROSS_PROCESS_EVIDENCE_R1.md` | process A/B traces and restore comparison |
| `03_CRASH_FATE_MATRIX_AND_THREAT_OUTCOMES_R1.md` | observed crash fates, invariants, threat outcomes, failure ceiling |
| `04_TEST_CORRECTION_LEDGER.json` | the 6 corrections to my own suite + mutation controls |
| `05_OWNER_API_REQUEST_R1.md` | minimal owner API request for the two holds |
| `environment_passport_delta.json` | `SOROK_WARM_ENVIRONMENT_PASSPORT_R1` |
| `repro/c07_journal.py` | the adapter |
| `repro/c07_worker.py` | real process A / B / crash roles |
| `repro/c07p_stage_closure.py` | blob-authenticated closure staging |
| `repro/source/` | pinned OC6 source + unrepaired OC4 contrast |
| `tests/test_c07p_crossprocess.py` | v1 suite, preserved unmodified |
| `tests/test_c07p_crossprocess_v2.py` | v2 suite |
| `observations/` | JUnit + stdout for every court, preservation re-run, staging ledger |
| `observations/mutation/` | the three mutants and their kill evidence |
