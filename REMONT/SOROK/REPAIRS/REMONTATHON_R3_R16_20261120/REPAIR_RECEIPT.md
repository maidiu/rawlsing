# R16 REMONT repair receipt — source-reconciled R12 local-machine work

## Source genealogy

- Frozen R15 sourcefree parent [#1220](https://github.com/maidiu/rawlsing/pull/1220), `6075792420e1d87b30036ebe6f352815783e47c2`: 276/276 Python 3.13.5 author court, source-seal and inhibitor fixes already present.
- Separate, independently run local-machine R12 correction [#1199](https://github.com/maidiu/rawlsing/pull/1199), `943b52c08d6b0fa9cdfdff9f7b751ab2eafcccb6`: reported 248/248 Python 3.11.3 and seed-stable demo. Exact GitHub compare reviewed: one commit after its original 246-test R12.
- Cross-branch distinction: R13–R15 already block current-trial `REORGANIZE_PROJECT` (different diagnostic string); no cherry-pick of duplicate repair or rewriting earlier review.

## Actual remaining defects reproduced on frozen R15

1. **P070 typed snapshot errors:** `verify_chain()` accepted canonical JSON *non-objects* long enough to throw untyped `AttributeError` on actor rows or generic hash mismatch on world rows. New regression tests assert fail-closed `WORLD_SNAPSHOT_NOT_OBJECT` / `ACTOR_SNAPSHOT_NOT_OBJECT` for canonical `[]`, `null`, scalar and boolean data, with positive rollback/unchanged-chain assertions. Original canonical byte matching, unique world roster, actor roster and P018 source custody all retained.
2. **Deterministic actor recruitment:** in R15, final joint-link/motif recruitment is a `set`; iterating that set into `active` determined candidate `basis` order and actor-facing `Situated.recruited` by `PYTHONHASHSEED`. Sort the already acquired/qualified `actual` form IDs before building the dict. The cue, motives, actions and actor permissions are unchanged. New 17-form test reproduces unordered result on frozen source; after repair both `recruited` and candidate `basis` are ordered.
3. **Cross-end premature TAKE_UP:** R15 correctly refused same-event uptake of the **selected** trial end but allowed an LLM to take up a distinct preexisting end into a durable project in the same event. A two-end actor and valid issued current ticket showed actual mutation on frozen R15. R16 refuses *all* `TAKE_UP_POSSIBLE_END` proposals when an issuer-qualified trial exists; separate genuinely later nontrial uptake remains supported by inherited tests. This is a conservative sourcefree guard, not a universal learning theory.

## Evidence and bounds

- First-red evidence: `R16_RED_ON_FROZEN_R15.txt`, test methods 4, original 5 actor errors + 5 world mismatches + 2 other failures. 
- Repaired author court: **280/280 unittest normal**, **280/280 `python -O`**, **pytest 280 passed +32 subtests** on Python 3.13.5. `R16_FOCUSED_GREEN.txt` and complete suite transcripts retained.
- Sourcefree demo (two different PYTHONHASHSEED values) yielded **byte-identical outputs** and same nine-event `bc47d6102f9cf402193131bd196cb697aa47930e53ff53cc6329ef3efed5b363`, valid cold reopen.
- Original 73 production records, 53 scoped first-fault independent reviews, 8 open/8 partial and 4 P070–P073 author repairs awaiting separate review; 0 T and 6 E holds are not amended. The #1199 Python 3.11.3 proof is NOT imputed to this R16 code; a new 3.11 test and independent hostile receiving at exact HEAD remain.
- No protected PRE-MAIN merge, canonical PROGRAMMA or paired CURRENT_PROGRESS write, native source/secret owner rights, genuine science calibration, or claim of a completed person.
