# PYAT C3-03 — CODEX SOURCE-FREE EXECUTION FALLBACK — R1

Status: `PASS_SOURCE_FREE_QUALIFICATION`

Commission branch: `agent/codex-pyat-hq126-c3-03-source-free-execution-r1`

Exact tested detached commit: `283d2c5d2b187c4e62ae1aecb236a0b51ddeffb1`

Semantic candidate: `901e3e77f905847d3ef8d86b458280d8fe422dd0`

## Execution

The user explicitly authorized execution on the Mac after the off-Mac GitHub runner again failed before assignment on attempt 5 (`runner_id=0`, no steps). A sparse, detached checkout of the exact execution commit was used. CPython 3.11.3, pytest 9.1.1, and pandas 2.3.3 were installed in an isolated environment. The sorted `pip freeze --all` SHA-256 was recorded before test collection: `9cde8e5ab9abba46a9e98826100ed084a0943a77fee7bc232a3c7643334da2eb`.

Protocol self-test: **20 passed, 0 failed, 0 errors, 0 skipped**.

Court-spec validation: **PASS**.

Final six-file bounded court: **55 passed, 0 failed, 0 errors, 0 skipped**. The exact generated receipt is `03_COURT_RECEIPT.json`; SHA-256: `716bb59b228ff448a60a7c77155f068d7dc98066b4e5a9f781ad4368979a3487`. The court receipt binds execution SHA `283d2c5d2b187c4e62ae1aecb236a0b51ddeffb1` and semantic candidate `901e3e77f905847d3ef8d86b458280d8fe422dd0` and has no synthetic PR merge SHA.

Two preceding court attempts were incomplete because the sparse checkout omitted tracked fixture files. Their failure counts and hashes are preserved in `04_SCOPE_AND_INTEGRITY.json`; they are not semantic qualification results. The final court used the same frozen commit, spec, code, tests, and pinned environment with only the required tracked fixtures added to the sparse checkout.

The tested tracked tree was unchanged throughout. It was clean before the final court and clean afterward once generated Python bytecode caches were removed. No raw survey source file was present or opened, materialized, or decoded. The source-free court read its frozen structural derivative fixture. Candidate A/B/C, measured P2X, and real-source C11 materialization were not run. No code, test, workflow, or court-spec file was edited.

The active Codex session was GPT-6; the earlier 5.6 preference could not be selected within this running task.

This return is qualification evidence only. HQ adjudication is required before any adoption or integration.

Terminal:

`C3_03_CODEX_SOURCE_FREE_EXECUTION_FALLBACK_COMPLETE__HQ_ADJUDICATION_REQUIRED`
