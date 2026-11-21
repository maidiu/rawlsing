# SOROK REMONT R17 — independent bounded P018 sourcefree engineering receiving

**Receiving date:** 2026-11-21. **Verdict:** `ACCEPT_SCOPED_SOURCEFREE_P018_HISTORICAL_INTEGRITY_PREFLIGHT__NATIVE_AND_PROTECTED_RECEIVING_HELD`.

## Frozen source / independent qualification

- **Reviewed PR:** REMONT [#1230](https://github.com/maidiu/rawlsing/pull/1230), exact current **HEAD** `28bf7fc48264d433ecf172bd0846744a3476222e`, parent R16 #1222 `7a8a18c153ee5a36e1c52eca15f4e5e8862296be`. Draft, unmerged. This reviewer did **not** author the R17 P018 repair, so this is a different-agent execution/review of the bounded work. The connected GitHub account remains the PR author's credential, however; this **is not** an independently credentialed GitHub approval or G5 authorization.
- Source frozen against actual GitHub PR diff. Starting from the exact R16 Library runnable archive `SOROK_REMONT_R16_R12_LOCAL_FIXES_280_TESTS.zip`, independently reconstructed only the **three** R17 Python changes: `um_sorok_organism/storage.py` blob `75087ed57c3a39d82b9ded5ebf8123f949e54c21`, `tests/test_remontathon_r4.py` blob `47d2d88b85ee573d313fd18a2346c2931b639664`, and new `tests/test_r17_source_preflight.py` blob `b25f93b2fd81fa814bfeee9be843d7279cf0b31b`. All three match the **exact Git object hashes, SHA-256 and lengths** in the frozen R17 source manifest.
- **All 48/48 inherited R17 Python files** verified through a two-part source identity proof: 45 untouched R16 files matched the R16 frozen source manifest locally; the three R17 changed/new blobs matched independent exact GitHub reads. The published R17 manifest matches the R17 GitHub tree for **48/48** paths; no out-of-manifest Python files. Reconstructed source was executed, not merely inspected.
- The newer SORACLE×REMONT first-consumer #1234, current `8d1ff8bbb75b359cc7bd3044b385323600c70b88`, carries the **identical** R17 `storage.py` and R17 test Git blobs. That code-identity check is not a new full-suite execution at the joined HEAD.

## Actually executed sourcefree court — CPython 3.13.5

| Test basis | Normal | Optimized `-O` | Pytest |
|---|---:|---:|---:|
| **Frozen R17 suite, unchanged** | **289/289 PASS** | **289/289 PASS** | **289 PASS +32 subtests** |
| Original **six** R15 independent reviewer tests, unchanged | **6/6 PASS** | **6/6 PASS** | included in combined |
| **Eight newly authored** P018 adversarial source/append tests | **8/8 PASS** | **8/8 PASS** | included in combined |
| **Joined independent acceptance court** | **303/303 PASS** | **303/303 PASS** | **303 PASS +96 subtests** |

**Additional attacks** directly tampered persisted `source_seals` canonical bytes, injected an unauthorized source row, inserted an unauthorized seal map in an ordinary event while **recalculating that event's own hash**, altered an event header, wrote malformed JSON into prior history, inserted unanchored constraints, and inserted an uncommitted second world. Every attack was refused at ordinary source read, including a request for a nonexistent source, and at event/source append; failure did not add events or late source rows. Valid late sealing, subsequent ordinary append, `verify_chain()`, and cold SQLite reopen also passed.

The six inherited independent R15 tests include the *64-graph* independent acyclic inhibitor oracle supporting P012. P012 acceptance is not being expanded by this P018 decision.

**Python 3.11 distinction:** This review environment has only Python **3.13.5** installed (`uv python list --only-installed`). The R17 PR already contains source-pinned author/other-machine **Python 3.11.3** receipts: **289/289 normal**, **289/289 optimized**, **289 pytest +32 subtests** at the same exact R17 HEAD. Those receipts were inspected for scope but are **not** represented as tests independently executed by this review agent. The independent functional outcome here is on Python 3.13.5.

## Accepted exact engineering boundary

`storage.ResearchLedger` now runs the complete `verify_chain()` preflight via `_require_valid_history_locked()` **before** returning `source(sid)` and **inside the transaction before** `commit()` or `seal_source()` appends. It preserves P045/P046 specific conflict diagnostics while mapping malformed historical envelopes, illegal source-seal maps, mismatched anchors, invalid chain headers and noncanonical historic bytes to a typed `Conflict`. The 5 original R15 P018 hostile cases, the full R17 target module, and the new sourcefree falsifiers pass at the exact reviewed source.

**This warrants `ACCEPT_SCOPED_SOURCEFREE_ENGINEERING` of the historical-source integrity and operational preflight first fault only.** It does not independently attest that source content is true, cryptographically signed by an external issuer, protected from a fully privileged database administrator who can rewrite and rehash the entire history, or confidential under native P009/P018 disclosure law. The continuing P018 production-defect identity must remain **PARTIAL**, not globally CLOSED. The earlier R15 `REVISE_EXACT_DEFECT` was valid on frozen #1220 and is superseded **only for this bounded repair**, not retrospectively erased.

## Authority and follow-through

- **No code patch required** for the reviewed R17 first fault. The R17 branch is unchanged; no protected merge or scientific/native rights granted.
- Record this as **an independent (different-agent) scoped engineering receiving decision** on #1230 and in the existing SOROK REMONT `OPEN_DEFECTS.md` and `.json` receiving record, without changing the historical P queue identity or treating older #1171's 71-entry branch as the current 73-entry R17 queue.
- **Credential-independent GitHub approval, authorized owner acceptance, native security/privacy science, protected-base no-drop transplant, and paired PROGRAMMA/CURRENT_PROGRESS receiving remain separate.** Protected branch `integration/pre-main-reconciliation-r1` was observed at `80e60385f6b6fa8cbaded730d7ab877d5fcaad78`, but no protected state was altered.

**Final:** `P018_R17_ACCEPT_SCOPED_SOURCEFREE__R15_OLD_RED_SUPERSEDED_BY_LATER_VERIFIED_CODE__NATIVE_PRIVACY_AND_PROTECTED_RECEIVING_NOT_GRANTED`.
