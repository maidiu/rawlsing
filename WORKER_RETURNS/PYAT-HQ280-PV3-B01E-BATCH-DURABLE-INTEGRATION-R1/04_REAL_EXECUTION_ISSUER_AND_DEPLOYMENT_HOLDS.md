# B01E — REAL_EXECUTION, issuer and deployment holds

## 1. Custody

| Item | Value |
|---|---|
| Sealed startup (verified before mutation) | `2fb5e8cc9971fe05899bbbeff837cd6cd049a969` |
| Branch | `agent/rabochii-pyat-hq280-pv3-b01e-batch-durable-integration-r1` |
| Inherited candidate | B01D `ef93f014a157983e0f713c118ee3a95311c16292` (B01DR positive) |
| Interpreter | Python 3.11.3 (`.pv3-venv`), macOS-13.7.8-x86_64 |
| Raw `.sav`/`.dta` in worktree | **0 files** (walked, `.git` excluded) |
| Source read / source-use grant | **none** |
| Canonical / semantic PRE-MAIN | **unmutated** |
| Self-adoption / merge | **none** |
| ZIP relay | **none** — modest text/JSON pushed to the branch |

Changed files (only): `rawlsing_next/pre553_governed_batch_checkpoint_integration_candidate.py`
+ its test + this return dir. Verified: `git diff --name-only <sealed> --
rawlsing_next/` lists exactly these two files; batch/protocol/B01D/A04T
owners byte-identical.

## 2. Safe hosted bounded resource record

Measured recorder process, real subprocesses, 3-unit manifests:

| Measure | Value |
|---|---|
| Peak RSS | **14.48 MiB** |
| User CPU | **0.104 s** |
| System CPU | **0.083 s** |
| Recorder wall | **~11.4 s** (dominated by real Route B executions) |

**Bounded development-scale numbers only — not a capacity forecast.**

## 3. Protocol truth (unchanged, still controlling)

`rabochii_execution_protocol.py` requires `WRITE_AHEAD checkpoint_state`
with `durable_checkpoint_ref` for REAL_EXECUTION. This adapter delivers
*candidate source-free compliance evidence* (durable START intents +
digest-backed checkpoint refs for every unit) and identifies the exact
accepted protocol integration owner — but **cannot and does not declare
operative REAL_EXECUTION approved**. No REAL_EXECUTION permission was
requested, granted, or constituted by any run herein.

## 4. Approval holds — what this integration does NOT establish

1. **Exactly-once external execution: NOT proven.** Proven instead: no
   duplicate externalization across kill+resume (journal stays 1), and
   unknown outcomes stay HELD under `IDEMPOTENCE_ISSUER_HOLD` (inherited,
   still open — no owner-verified idempotence credential exists).
2. **Deferred/failed retry through the adapter: PINNED, not available.**
   The B01D journal pins every COMMITTED record; the adapter reports
   `pinned_deferred` loudly rather than working around it. Retrying such
   work needs an idempotence credential (hold 1) or a fresh checkpoint
   root after fixing the underlying cause (e.g., missing executor).
3. **Selective resume past held/pinned units: NOT available.** The accepted
   runner is head-anchored with no per-unit entrypoint; the adapter stops
   at the first non-progressable unit and reports the suffix as blocked.
   An owner-level per-unit execution entrypoint is recorded as future
   work — never simulated (simulating it would mean inventing receipts).
4. **Single-host `flock` only**; NFS/distributed semantics unsupported.
5. **Crash-consistency is phase-bounded**: START / side-effect / COMMIT
   windows, torn files, lock contention, 3-unit manifests. Hardware/FS
   lies, disk exhaustion, large-manifest fsync costs: outside the envelope.
6. **Scale is bounded** (3 units). No throughput or large-manifest claims.
7. **B01 F-04/F-05/F-06 and P17** inherited unchanged, out of scope.
8. **Full repository suite not run** per commission scope; no claim made
   about it either way.

## 5. Competent-owner decisions required

| Decision | Owner |
|---|---|
| Accept/reject this candidate-only integration | HQ / competent owner |
| Issue (or decline) a verified idempotence credential | execution/authority owner |
| Provide a per-unit execution entrypoint (or accept schedule pinning) | batch owner |
| Allow journal successor-intents for DEFERRED/FAILED retries (or keep pinning) | checkpoint owner |
| REAL_EXECUTION approval, if ever sought | protocol owner |

**Terminal:** `HQ280_PV3_B01E_ACTUAL_BATCH_DURABLE_ADAPTER_SOURCEFREE_RUN_OR_PRECISE_HOLD__NO_REAL_EXECUTION_GRANT__GITHUB_PUSHED`.