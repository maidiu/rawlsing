# SOROK REMONTATHON R3 R2 — hostile ledger integrity follow-on

## Identity and scope

Research/sourcefree only. Parent live GitHub candidate #1171 exact R1 
`a4d4f54b825b69c5b2f7ff66e8450babafda6404`, itself built on ORACLE R3 #1167 `3dba91136870ab5e766ca14faacd847531dea075`. Protected integration remains separate and unmodified. All old R1 84-test source/history kept immutable.

## Actual reproduced bugs before patch

- **SR-P040: event metadata tamper without failing verification.** SQLite events have columns `world_id`, `clock`, `actor_id`, `kind` alongside the JSON event envelope. Old `events()` read and `verify_chain()` only checked the envelope, so a direct UPDATE of the `kind='FORGED_LIFE'` and `actor_id='ghost'` columns yielded an apparently valid chain. Now the event reader exposes the columns and `verify_chain()` checks *exact row-header/envelope agreement* before claiming a valid event.
- **SR-P041: `python -O` disables all hash-chain checks based on `assert`.** The research ledger used `assert` to verify ancestry, event id, chain hash, source anchors, and actor roster. In an optimized Python interpreter these checks were compiled away. A standalone `python -O` subprocess reproduced acceptance of a forged `previous_hash`. Replaced integrity asserts with explicit `raise AssertionError`, and the adversarial optimized-interpreter test now rejects altered ancestry.
- **SR-P018 extra exact-source violation:** the hash of a source seal was calculated from JSON meaning, allowing whitespace mutations of the original raw source bytes without detection. A sealed raw JSON blob is now required to equal its canonical serialization byte-for-byte; valid initial and late source seals continue to reopen/cold verify. This remains a research seal, not native source-chain authorization.
- **SR-P039 extra clock violation:** a `True` boolean qualified as an integer clock in the old `isinstance(bool,int)` check. Require exact integer type; no floating/boolean pseudo-clock.

## Executed proof

- Original pre-repair R3 baseline: 62 local tests passed.
- Prior R1 REMONTATHON: 84 tests passed, including 22 new tests; immutable GitHub parent R1 evidence.
- **Current R2 integrated sourcefree run:** `python -m unittest discover -s tests -v` -> **88 PASS / 0 FAIL**, four newly added independent adversarial tests (source whitespace mutation, forged SQLite header, optimized-interpreter ancestry, boolean clock). Tests ran against the full prior R1 code, not an isolated artificial test-only adapter.
- Full executable source package and exact Git-object/SHA-256 file identity ledger are present in the R2 Library package. The suite also includes 120 sequential actor/world transitions and cold SQLite reopen with source anchoring, and a multi-effect invalid provider rollback.

## Open constraints

SR-P012 and SR-P018 remain **partially repaired**, not native-scientifically solved. SR-P005 remains partial despite wage due/paid/unpaid accounting. Earlier P022/P023 organismic genesis and historically generated motives still open; sourcefree LLM backfill, native PYAT input, actor secrecy, empirical POP/DEV/TRANS and independent receiving unproved. This is no basis for protected PROGRAMMA or paired CURRENT_PROGRESS mutation. New SR-P040/041 are local author-tested candidate fixes pending nonauthor review.
