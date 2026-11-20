# SOROK REMONT — R12 R2 same-event project-reorganization provenance repair

2026-11-20. **AUTHOR-TESTED RESEARCH CODE; INDEPENDENT RECEIVING PENDING.** This repair is stacked atop frozen [PR #1199](https://github.com/maidiu/rawlsing/pull/1199) exact `9db0e6f64bf568409e638ff2215af8b8a414487f`; it does not change that original branch, protected PRE-MAIN or native scientific owner contracts. The existing 71-record REMONT ledger is reconciled from latest original #1171 (`a6b5f97b9aa7e1f8c8d4063d2ab8d5869f6fefb1`) and R12 historical candidate metadata without changing any P/T/E identities or receiving statuses.

## First fault and substantive code repair

Independent [#1199 review #5999820908](https://github.com/maidiu/rawlsing/pull/1199#pullrequestreview-5999820908) established that a legitimate, runtime-issued Nadia SING trial did not license `ADD_PROJECT` but **did** allow a semantic callback to rewrite a separately acquired durable project's `object` and `motive` with `REORGANIZE_PROJECT` during the **same event**. R12 persisted `MATURE_END_FROM_THIS_TRIAL` while the possible end was nominally still provisional and the objective event chain valid. The defect is psychological historical provenance, not transaction hash integrity.

**Existing first owner changed:** `um_sorok_organism/development.py::admit` checks each issued-trial `REORGANIZE_PROJECT` for either `object` or `motive`, raising `InvalidDevelopment('CURRENT_TRIAL_NOT_MATURE_MOTIVE')` **before** recording trial history or applying any proposed psychic updates. The existing `ADD_PROJECT` and same-end `TAKE_UP_POSSIBLE_END` guards remain unchanged. No new actor authority, world inference or scientific motive law is created. **Non-purpose updates** (`priority`, `cue_terms`) during the current trial remain available. Object/motive changes on an independently experienced *nontrial* event remain available through ordinary qualified admission.

## Actual executed RED → GREEN, distinct from author assertion

1. The exact R12 ZIP recovered from REMONT Library has whole-ZIP SHA-256 `2aeb7fc0075124ce0107bf48087ed1bb2b967cb52846135a18559ac00b83b460`, and all 42 original Python Git blobs/SHA256 bytes match the frozen GitHub manifest. R12 original suite: **246/246 normal, 246/246 optimized, pytest 246 PASS + 14 subtests**.
2. Six external reviewer scenarios were behaviorally transcribed in `tests/test_r12_hostile_receiving_new.py` (not claimed byte-identical to reviewer blob `019dc15b79fccff66b142396605504cf81feab88`). On untouched R12: **5 PASS, 1 failure**—existing project rewrite silently admitted, `RED_FROZEN_R12.txt`. Independent original source remains at immutable commit `dea778ef3187994a362d88a0287029730730590b`.
3. After repair the same six scenarios **6/6 PASS**. Four additional author tests cover object-only refusal, motive-only refusal, mixed TRACE+rewrite atomic rollback, and positive non-purpose scope update in an issued trial: **4/4 PASS**.
4. Full combined **256/256 normal unittest PASS, 256/256 optimized Python -O PASS, pytest 256 PASS + 20 subtests**; exact logs here. Separate two-process cold SQLite reopen: four valid events, stable event-chain hash, actor-specific trial persists while `POSSIBLE_NOT_ACQUIRED_MOTIVE` remains intact.
5. `R12_R2_SOURCE_SHA256.json`: **44 Python files** (41 exact inherited R12, one changed development owner, two new tests), with exact byte counts, SHA-256 and Git blob identities. Source/test bytes should be independently verified against the new HEAD.

## Remaining receiving duties

A **different agent** must independently freeze the new HEAD, reproduce original R12 246 + all six *original exact reviewer* tests + four author tests, challenge other historical and durable-purpose entry routes, verify complete original 71-entry P/T/E and newer #1198 receiving conservation, and return `ACCEPT_SCOPED / REVISE_EXACT_DEFECT / HOLD`. This author return is not independent acceptance or native psychology. SR-P070/P071 separately require review by someone other than their original author. Protected PRE-MAIN and canonical PROGRAMMA/paired CURRENT_PROGRESS are unchanged; `HQ_CURRENTNESS_HOLD` on authorized receiving.
