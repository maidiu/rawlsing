# SOROK REMONTATHON R17 — P018 full source/chain preflight

## Genealogy and scope

- Frozen parent: R16 draft #1222 exact `7a8a18c153ee5a36e1c52eca15f4e5e8862296be`.
- R16 inherited R15's incomplete P018 fast preflight: `source()` and `commit()` could read or append to a ledger whose full `verify_chain()` already rejected the history.
- R17 changes only the source/chain admission boundary in `um_sorok_organism/storage.py`; it does not change world/actor psychology, P012 recruitment, P070 snapshot typing, trial authority, native rights or protected status.

## First fault reproduced on R16

Seven independent cases were RED on R16 under normal and `-O`:

1. modified historical source anchor, source read returned content;
2. modified historical source anchor, append succeeded;
3. unauthorized source map on an ordinary event, source read returned content;
4. same unauthorized map, append succeeded;
5. noncanonical late `SOURCE_SEAL` payload, source read returned content;
6. noncanonical initialization payload, source read returned content;
7. noncanonical ordinary-event payload, source read returned content.

Full `verify_chain()` rejected all seven on R16; the defect was that `source()` and append preflight did not enforce the same result.

## Correction

`storage.ResearchLedger` now calls the existing complete `verify_chain()` under its lock/transaction from:

- `source()` before returning any source row;
- `commit()` before appending any new event;
- `seal_source()` before appending a late source seal.

The existing specific preflight runs first (`_verify_current_anchor_locked`) so inherited P045/P046 diagnostics remain stable; the full verifier then catches noncanonical bytes, bad event identity/hash, unauthorized source maps and historical source-anchor changes. Failures raise `Conflict('SOURCE_HISTORY_INVALID: …')`.

Two inherited R4 assertions that previously called `source()` on an already-tampered ledger and expected `None` now inspect the `source_seals` table directly. Their intent—no late source row was created—is preserved; the old assertion would have masked the invalid history that P018 now refuses.

## Court

- New R17 test module: 9/9 PASS normal and `-O` (the eight hostile cases plus a valid read/append continuation).
- Imported R15 P018 test module: 6/6 PASS normal and `-O`.
- Two new reviewer P018 cases: 2/2 PASS normal and `-O`.
- Full suite: **288/288 normal**, **288/288 `-O`**, pytest **288 passed + 32 subtests** on Python 3.11.3.
- Demo: two distinct `PYTHONHASHSEED` values, byte-identical, 9 events, last hash `bc47d6102f9cf402193131bd196cb697aa47930e53ff53cc6329ef3efed5b363`, cold reopen valid, SQLite integrity `ok`.

## Boundaries

R17 is a sourcefree local repair candidate, not independent acceptance, native P018 source disclosure authority, scientific accreditation or protected receiving. P070–P073 remain author-repaired pending distinct review; the 73 P records and six E holds are unchanged.


## Addendum — malformed envelope and joined #1234 evidence

An integration probe on #1234 exposed that `source()` could surface a raw `KeyError` when a historical envelope lacked required keys, because the preflight wrapped only `AssertionError`. R17 now rejects malformed envelopes as `EVENT_ENVELOPE_MALFORMED` in `verify_chain()` and maps `KeyError`/`TypeError`/`ValueError`/`StopIteration` to `Conflict(SOURCE_HISTORY_INVALID: …)`. The focused R17 module is now 9/9. R17 remains a sourcefree repair candidate; #1234 still carries the older storage blob and needs a new integration after this fix.
