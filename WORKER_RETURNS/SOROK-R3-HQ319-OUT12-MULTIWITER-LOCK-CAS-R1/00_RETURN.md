# SOROK HQ319 OUT12 — Real multiwriter CAS/lock court

**VERDICT:** `MULTIWITER_CANDIDATE_IMPLEMENTED_AND_COURT_PASSES__NO_SILENT_LOSS_AT_TESTED_SCOPE__INDEPENDENT_I2_STILL_REQUIRED`
**TERMINAL:** `SOROK_HQ319_OUT12_MULTIWITER_LOCK_CAS_COURT_RETURNED__GITHUB_PUSHED`
**Branch:** `agent/rabochii-sorok-r3-hq319-out12-multiwriter-lock-cas-r1` @ `b1c0b474969b891c11da8f3a16b748568f395af5`
**Role:** bounded source-free transaction implementer — **NOT** HQ or ADP019 issuer. **One accountable agent, no helpers, no harness switch.**

## 1. Authentic source — independently re-verified
| check | value |
|---|---|
| commit | `fd58957fceca250e86ed3b1a5d06fa45ffc9ec85` |
| path | `…/SOROK-R3-HQ314-OUT9-OUT8-INDEPENDENT-R1/candidate/outbox_prototype.py` |
| **git blob** | `331840768ce0b5f6f73e5e93094ca0d217ddaebf` ✅ **matches HQ's value** |
| **sha256** | `5c994f29a8c3cf870cb8a18ce4c300fa51d9ab45c34caabc5f10a0f1973708ed` ✅ |

18 staged Python files; import path verified (`outbox_prototype`, `test_rto_hostile.legacy`).

## 2. Baseline counterexample preserved (the defect is real)
```
pytest test_sr_28_falsifier_court.py … test_out9_independent_hostile.py -q
  ->  2 failed, 270 passed
```
Both historical literal REDs remain RED (`test_s27_material_move_needs_world_owner`, `test_replay_manual_two_writers_can_lose_first_committed_event`). Court case **C0** re-executes the counterexample with **two real OS processes** on the **unmodified accepted `Journal`**: both report success, **one committed event is lost**.

## 3. The candidate — return-local, opt-in, accepted source untouched
`candidate/multiwriter_journal.py` — `MultiwriterJournal`, a wrapper that **does not modify, subclass or monkeypatch** the accepted `Journal`. Two mechanisms, both required:

1. **Interprocess transaction lock** — exclusive `fcntl.flock(LOCK_EX|LOCK_NB)` on `<journal>.lock`, held across the **entire** read-modify-write, with a bounded poll/timeout raising typed `JOURNAL_LOCK_TIMEOUT`.
2. **Versioned compare-and-swap** — a monotonically increasing `writer_version` persisted in the journal receipt; `commit(p, expected_version)` raises typed **`StaleJournalConflict`** unless the on-disk version still matches.

The added top-level `writer_version` key is **backward compatible** (accepted `recover()` validates `schema` and a digest over `state` only), so the accepted reader still loads the file — it simply ignores the version and re-exposes the original hazard, which is precisely the defect being closed. **The accepted OUT9 source was not modified and is not claimed to have been retroactively safe for multiple writers.**

## 4. Court results — all passed
```
pytest candidate/test_out12_multiwriter_court.py -q     ->  9 passed
```
| case | claim | result |
|---|---|---|
| **C0** | accepted Journal loses a committed event (2 real processes) | ✅ counterexample preserved |
| **C1** | CAS, 2 processes, **no lost committed event** | ✅ **2 events retained** |
| **C2** | CAS, 3 processes, **no lost committed event** | ✅ **3 events retained** |
| **C3** | lock serializes; each writer commits at a **distinct fresh version** | ✅ commits = {1,2} |
| **C4** | version monotonic; replaying an old version refuses | ✅ typed conflict |
| **C5** | **stale reader cannot publish**; typed `STALE_JOURNAL_CONFLICT` | ✅ |
| **C6** | revocation survives a competing transaction; **byte-for-byte cold recovery** | ✅ |
| **C7** | **real SIGKILL** at `BEFORE_RENAME` → journal **byte-identical**; cold recovery yields the pre-crash state | ✅ rc=79 |
| **C8** | cold-recovery identity: `writer_version == 3`, 3 events | ✅ |

Real OS subprocesses throughout, with a filesystem **synchronization barrier** releasing writers simultaneously; **no simulated concurrent calls**.

## 5. Two test bugs of mine — found, disclosed, corrected
My first run was **7 passed / 2 failed**, and **both failures were in my test code, not the candidate**:
- `C3` wrongly asserted that a clean race must produce a `StaleJournalConflict`. With the lock held across the whole read-modify-write, writers legitimately **serialize** — no stale snapshot can be held, so no conflict arises. I rewrote C3 to assert the true property (distinct fresh versions) and left the CAS-fires proof to **C5**, which constructs a genuine stale snapshot.
- `C6` guessed a private attribute (`Outbox._revoked`) that does not exist. I replaced it with a state-equality assertion over the public snapshot.

I record this rather than hiding it: a court whose only failures are its author's own assertions must say so.

## 6. Honest scope of the safety claim
**At the tested scope** — 2- and 3-writer races on a local filesystem, with lock-serialized CAS commits and a pre-rename `SIGKILL` window — **no acknowledged committed event was silently lost, and every conflict was typed**. This is **not** a claim of exactly-once delivery to real clients, nor of correctness on exotic/network filesystems (`flock` semantics are filesystem-dependent), nor of safety against a writer that bypasses the candidate and calls the accepted `Journal.commit` directly — that path remains last-writer-wins by construction.

## 7. Boundaries
Writes confined to `WORKER_RETURNS/SOROK-R3-HQ319-OUT12-MULTIWITER-LOCK-CAS-R1/`. Accepted OUT9 source and all original test bytes **unmodified**; both historical REDs preserved. No production ADP019 issuance, no physical effects, no client perception, no V3 operation. **Independent I2 review is required for this new candidate**, and I do not self-adopt it.

**Terminal:** `SOROK_HQ319_OUT12_MULTIWITER_LOCK_CAS_COURT_RETURNED__GITHUB_PUSHED`.
