# HQ320 OUT13 — INDEPENDENT MULTIWRITER TRANSACTION COURT

## Verdict

# `REVIEW_REVISE_AT_SOURCEFREE_SCOPED_MULTIWRITER_GRAIN`

OUT12's mechanism **works at the tested cooperating-writer grain**, and its nine
author tests reproduce unedited. But two structural defects in the candidate's
integrity model are **demonstrated, not theoretical**, and one evidentiary label
overstates its method. The candidate should not be accepted as a safety property
until the version-metadata design is fixed.

| Suite | Result |
|---|---|
| Original 272 unchanged | **270 PASS / 2 historical REDs** (both preserved) |
| OUT12 nine author tests, unedited | **9 passed** |
| New OUT13 hostile court | **23 passed** |

---

## 1. MANDATORY INDEPENDENCE DISCLOSURE

I must not bury this. **In an earlier session of this same conversation I authored
the OUT9 return** that produced the accepted single-writer source reviewed here
(`fd58957f`, `outbox_prototype.py` blob `331840768…`).

- **OUT12 authorship independence: intact.** I have never authored, edited or run OUT12.
- **Baseline-reviewer independence: COMPROMISED.** I reviewed my own accepted baseline.

This is an **HQ-adjudicable defect that I do not resolve myself.** Mitigation: both
sources are staged byte-exact and re-verified against their own commits, and no
accepted or candidate source was edited, so a fully independent reviewer can
reproduce every number here.

## 2. My own error, disclosed and corrected

My first staging placed OUT9 and OUT12 in **separate directories**. OUT12's court
spawns child processes that import `outbox_prototype` from their own script
directory, so that run produced **6 failures that looked like OUT12 defects**. They
were entirely my staging error. With the faithful merged `candidate/` layout,
OUT12 is **9/9**. I report this because an independent reader deserves to know the
first number I saw was wrong and why.

## 3. What genuinely holds

**HP1 (2, 3 and 5 genuinely simultaneous OS writers, real barrier, real `flock`):
no acknowledged committed event was ever lost.** Durable identities always equal
acknowledged identities. Conflicts are typed `STALE_JOURNAL_CONFLICT`; lawful retry
after re-recover succeeds. `writer_version` is strictly monotone and equals the
commit count (3 → 6 → 9 for 3 writers).

**HP9 cold recovery:** interruption before rename leaves prior state **byte-identical**;
interruption after commit leaves the newest state durable with a coherent ledger.

**HP5 starvation:** an external lock holder produces a typed `JOURNAL_LOCK_TIMEOUT`,
not a hang or a corrupt write, and the lock is legitimately released afterwards.

## 4. DEFECT 1 — `writer_version` is unauthenticated metadata (HP7, HP8)

This is the commission's central question and the answer is concrete.

`commit()` writes `{"schema":…, "state":…, "state_digest": _hash(state),
"writer_version": …}`. **`state_digest` covers `state` only.** The accepted
`Journal.recover()` validates `schema` and that digest over `state`, and **ignores
`writer_version` entirely**. Demonstrated consequences:

1. An authorized writer can rewrite `writer_version` to any value while leaving
   `state` byte-identical, and the accepted reader **cannot detect it** — the
   digest still verifies.
2. **Worse:** `_read_version()` is `except (ValueError, TypeError): return 0`. A
   corrupted version silently becomes **0**, and a holder expecting version 0 then
   **publishes successfully**, defeating the compare-and-swap entirely (HP8).
   Version 0 is also the "no journal yet" sentinel, so a corruption is
   indistinguishable from first creation.

**Consistency meaning:** the candidate provides **no authenticated ordering
metadata**. Its monotone-version guarantee holds only against *cooperating* writers
that never bypass it. Older readers, which ignore the key, cannot participate in the
protocol at all — they are silently outside it rather than detected.

## 5. DEFECT 2 — a safe wrapper does not make the original Journal safe (HP6)

`MultiwriterJournal` is **opt-in**. Demonstrated: an authorized caller invoking the
accepted `Journal.commit()` on the same file obtains **no lock and no version
check**, and the resulting receipt **carries no `writer_version` key at all**.

That is worse than merely "no protection": a bypassing write **erases the version
entirely**, which then feeds directly into the HP8 path (`_read_version() → 0`).
So the two defects compose. Any authorization model that admits the accepted
`Journal` as a legal writer leaves the journal unsafe, and the candidate's own
monotone-version claim is void on that path.

**Honest null:** my single-process sequential-commit variant did **not** reproduce a
lost event, and I assert no such loss. The lost-event property of the accepted
Journal rests on the real two-process interleaving in OUT12's own `C0`, which
passed in this court unedited. I record my null rather than claim an unreproduced
result.

## 6. DEFECT 3 — "real SIGKILL" overstates the method (HP10)

OUT12 records C7 as **"real SIGKILL"** with **`rc=79`**. I measured it directly:
`rc=79` is `os._exit(79)` — a **normal positive process exit, not a signal**. A
SIGKILL would surface as `-9`.

I preserve OUT12's original result and adjudicate the limit separately: `os._exit`
*does* bypass `finally`/`atexit`, so process-death semantics are largely exercised
and the practical fidelity is better than a casual reading suggests. But **no
signal was delivered**, and the label claims more than was executed. The honest
description is "abrupt non-returning process exit at a pre-rename injection point".

## 7. Process death is not power-loss durability (HP11)

The candidate does the right user-space things: `fsync` on the file **and** on the
parent directory before declaring success. But nothing in user space proves
media-level durability. No `fdatasync`, no `syncfs`, no barrier-based claim.
**Process death ≠ power-loss durability**, and the return claims only the former.

## 8. Bounded threat model (unchanged, restated)

| In scope | Out of scope |
|---|---|
| TEST_ONLY source-free multiwriter, **local** filesystem, **cooperating** writers all using `MultiwriterJournal` | exactly-once client delivery; exotic/network filesystem `flock` semantics; **true power-loss durability**; **any writer that bypasses the candidate**; production ADP019 issuance; semantic adoption; V3 |

## 9. Required repairs before any acceptance

1. **Authenticate `writer_version`** — include it in a digest the accepted reader
   validates, or store it in a separately sealed field with its own integrity
   check. Stop returning `0` on parse failure: refuse with a typed
   `VERSION_STATE_UNREADABLE`.
2. **Detect bypass** — a write that removes `writer_version` must be refused or
   loudly detected rather than silently reinterpreted as version 0.
3. **Correct the C7 label** to the method actually executed, or re-run under a real
   `SIGKILL` and record `-9`.
4. **State the authorization precondition**: the candidate is safe only if every
   authorized writer is *required* to use it.

## 10. What is NOT claimed

No production ADP019 grant. No real human perception. No physical-world event claim.
No semantic adoption. No V3 operation. No exactly-once delivery. No power-loss
durability. **Neither accepted OUT9 nor OUT12 source was edited**, and neither
historical RED was suppressed, xfailed or relabelled.