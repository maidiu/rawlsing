# SOROK HQ317 C07P — crash fate matrix, invariants and threat outcomes

All rows below are **observed from real runs**, not predicted. Process A is killed by a real,
uncatchable `SIGKILL` delivered *in place* inside the write protocol — no unwinding, no flush, no
`atexit`. Exit status observed: `137` (`-SIGKILL`) at every crash point.

## 1. Write protocol actually used

```
write tmp = <journal>.tmp        (whole new content)
flush
fsync  tmp                        observed: SUPPORTED
   ---- CRASH POINT 1 ----
os.replace(tmp, journal)          observed: atomic on the same directory
   ---- CRASH POINT 2 ----
fsync  containing directory       observed: SUPPORTED
   ---- CRASH POINT 3 ----
```

Platform observed: `macOS-13.7.8-x86_64`, Python `3.11.3`. Journal directory is a local APFS-backed
temp path. **This is a local file, not an institutional vault.**

## 2. Crash fate matrix — observed

| Crash point | Kill | Journal on disk | Temp file | Restore | Committed capsules | Verdict vs prereg |
|---|---|---|---|---|---|---|
| 1 — after tmp fsync, before `os.replace` | SIGKILL | 2 records, unchanged | **present** (orphaned) | succeeds | `['cap-A']` | `CLEAN_ROLLBACK` as preregistered |
| 2 — after `os.replace`, before dir fsync | SIGKILL | 3 records | absent | succeeds | `['cap-A','cap-C']` | `NOT_SETTLED` as preregistered |
| 3 — after dir fsync | SIGKILL | 3 records | absent | succeeds | `['cap-A','cap-C']` | `COMMITTED` as preregistered |

At **every** crash point the journal parsed cleanly, the hash chain verified, and
`verify_ledger_integrity()` was `True`. **No torn or partial record was ever produced.**

### 2.1 Crash point 2 is NOT a durability proof — and this is preregistered

Prereg §4.2 predicted exactly this and it held. A `SIGKILL` kills the *process*; the kernel page cache
survives, so post-`os.replace` bytes stay visible whether or not the directory entry was fsynced.
This experiment therefore **cannot** distinguish "durably renamed" from "renamed but not yet made
durable", because doing so needs an actual power cut or a separate filesystem. Neither is authorised
here.

**Crash point 2 remains permanently `NOT_SETTLED` by construction of this experiment.** Any future
document that treats it as proven durability is wrong.

## 3. Invariants proven across a real process boundary

Measured by comparing process A's fingerprint against a fresh process B's.

| # | Invariant | Result |
|---|---|---|
| I1 | distinct OS processes and distinct PIDs | proven |
| I2 | fresh interpreter and fresh import of the pinned blob in B | proven — `4c185c18…`, sha256 `ca85b844…` in both |
| I3 | all **18** capsule fields survive; commitment bit-identical | proven, and each field individually re-proven to change the commitment |
| I4 | `committed`, `unblinded`, `released`, `holder_roles`, exposure rows identical | proven |
| I5 | ledger op sequence and seq numbering identical | proven |
| I6 | `verify_ledger_integrity()` true in B after restore | proven |
| I7 | B can safely **continue** the lifecycle (second capsule) and integrity holds | proven |
| I8 | escrow **event timestamps** survive | **NOT preserved** — see hold below |

### 3.1 `C07_DEPENDENCY_TS` — open typed hold

`unblind()` and `record_exposure()` stamp `time.time()` internally and expose **no timestamp
parameter**. A journal replay therefore re-stamps escrow event times. The journal itself is faithful
(original `unblinded_at` / `exposure_ts` are stored and verifiable), but the reconstructed
`EscrowState` is not time-identical.

This was **not** worked around. Mutating `state.ledger` after the fact, or `object.__setattr__` on the
reconstructed state, would forge the very authority the experiment is meant to test.

**Minimal owner API request:** an optional `at: Optional[float]` parameter on `unblind` and
`record_exposure`, or an explicit `replay_event(record, at=...)` entrypoint.

### 3.2 `C07_DEPENDENCY_REVOKE` — open typed hold

`EscrowState` exposes `authorize_holder` but **no** revocation counterpart. A revoked custodian
therefore cannot be expressed through the public API at all, and consequently cannot be persisted and
restored. The suite proves the *absence* of the interface (`test_N16`) rather than pretending to test
revocation.

**Minimal owner API request:** a public `revoke_holder(person_id)` that removes the grant and appends
a journal-visible event.

## 4. Threat outcomes — measured

### 4.1 Detected

| # | Threat | Detecting layer | Observed |
|---|---|---|---|
| T1 | payload tampered | per-record unkeyed SHA-256 | refused: `digest mismatch` |
| T2 | middle record deleted | seq contiguity | refused: `record N: seq is …` |
| T3 | records reordered | seq + prev chain | refused |
| T4 | record duplicated | seq contiguity | refused |
| T6 | capsule fields substituted in a COMMIT | recomputed vs recorded commitment | refused: `forged capsule` |
| T7 | forged signature / uncommitted capsule unblinded | native escrow | refused: `IdentityMismatchError` |
| T8 | unauthorised purpose | native `verify_purpose` | refused: `PurposeViolationError` |
| T9 | ghost commitment / uncommitted exposure | native `_validate_capsule` | refused |
| T10 | exposure or unblind before any COMMIT | replay order + native escrow | refused |
| T12 | inconsistent materialised unblind | native `verify_ledger_integrity` | refused |
| T13 | truncated trailing line | strict parse | refused |
| T14 | stale snapshot replayed over newer journal | re-sealed prefix is still self-consistent, so it restores — see T5 | ceiling below |

### 4.2 NOT detected — the explicit bounded failure ceiling

**T5 — whole-journal rollback to a valid earlier prefix.** Demonstrated deliberately in
`test_N12_T5_whole_journal_rollback_is_a_demonstrated_ceiling`: the journal is rewound to the
cap-A-only prefix and **re-sealed so it is fully self-consistent**. Restore succeeds, native
integrity returns `True`, and `cap-B` has been **silently lost with no error at all**.

This is not a bug in the implementation. It is a property of any local unkeyed journal: every prefix
of a hash chain is itself a valid chain, so a prefix is indistinguishable from the truth without an
external monotone counter.

**The attacker who can rewrite both the state and the digest.** `rec` is unkeyed SHA-256. Anyone with
write access to the journal directory can alter a payload and recompute the entire downstream chain,
so T1, T6 and the rest are **integrity checks against accidental corruption and naive tampering, not
authentication**. The same attacker can simply delete the journal or replay a valid old prefix.

### 4.3 What would actually close this gap

None of these exist here and none may be invented by a worker:

1. An **external append-only anchor** (a monotone counter or a notary the writer cannot rewind).
2. A **key held outside the journal's trust domain** — an HSM, a remote custody service, a
   threshold-signed log. This is precisely the "real institutional custody" that C07P must not fake.
3. An OS-level protected store (a keychain, a TPM-sealed key) that the same local process cannot
   recompute.

Until one of those exists, this journal is a **durable local event log**, and saying otherwise would
be false.

## 5. Preservation of the accepted boundary

The additive adapter lives only in this return folder. Re-running the complete accepted closure
against the pinned OC6 source:

| Court | Cases | PASS | RED |
|---|---:|---:|---:|
| inherited 131 (OC1/OCR1/OC2/OC3) | 131 | 121 | **10** |
| OC4 author controls | 36 | 36 | 0 |
| OC5 prior predictions | 23 | 23 | 0 |
| OC5E native hostiles | 159 | 148 | **11** |
| OC6 author controls | 273 | 273 | 0 |
| OC7 independent v2 | 276 | 276 | 0 |
| **total** | **898** | **877** | **21** |

**Exactly the same 21 literal REDs OC7 adjudicated** — the 10 historical contract REDs and the 11
superseded/malformed witnesses. **Zero skips, zero errors.** The lexical and Unicode leakage gate was
not widened; no accepted test was edited, xfailed or suppressed.
