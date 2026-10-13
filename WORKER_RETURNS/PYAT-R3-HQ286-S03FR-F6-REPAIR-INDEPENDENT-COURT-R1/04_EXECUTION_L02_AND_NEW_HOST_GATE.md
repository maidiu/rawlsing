# S03FR — runtime evidence reconciliation and exact local handoff

## Distinct observed/reported evidence sources

| Provenance | Actual recorded test/result | Interpretation |
|---|---|---|
| Original S03R review \`34cc7bdb28664ecbc707528470c2b4397aa96f12\` | independent reviewer Python original pinned \`EXPECTED_SHA=68aba...\` | Frozen oracle; do not edit. |
| L02 \`d396b9b3d9bbb4f3b763bb0f00d79276b845ccfe\` | macOS 13.7.8 x86_64, Python 3.11.3 / pytest 9.1.1, *complete original* \`69a16865\` candidate root: **8 passed / 3 failed**, exit 1; failures 01, 07, 08. \`s03r_full_root.log\` real artifact. | True original candidate Python execution, NOT S03F qualification. 11 earlier errors from missing \`S03_CANDIDATE_ROOT\` were setup HOLD, not test verdict. |
| S03F \`bb739...\` author \`repro/s03f_evidence.json\` | 24 author original S03 tests passed, exit 0; **11 copied reviewer tests ERROR**, exit 1; combined 24 pass / 11 errors, exit 1 | Author's own recorded command/exit. It contradicts author prose claiming reviewer 10/11 and combined 34/1. |
| S03F prose \`00_RETURN.md\` | Claims 24+10 passes, 1 fail, combined 34 PASS/1 FAIL | **UNREPRODUCED** by committed execution records; must not be promoted. |
| Current HQ286 Browser S03FR | 13 independent versioned tests committed; **NO interpreter, pytest or local test execution** | STATIC_ONLY; projected pass/fail status is not actual runtime. |

S03F candidate Python SHA256 \`818638c937a9b1b64ac400dcb8e33337310f6c793417a1558f838edb01eb4841\`, Git blob \`b1b05e7d60f92357fb31cbea99e5b432415cc7b0\`; original fixture and accepted hash shared blob pinned in versioned test. No original source records.

## Resource-gated local executor handoff

Only if the existing qualified **secondary Mac** has available isolated sparse worktree, attested configured provider/model/endpoint, privacy-eligible local code policy, interpreter and quota can the following occur. **No new clone**, reset, broad fetch, primary Codex billing, paid overflow, Space Bunny dispatch or unauthorized local action.

1. Materialize complete **S03F candidate \`bb739fb6d60b40876566ec6320ff6eec2388e8cf\`** including \`WORKER_RETURNS/PYAT-R3-S03-F6-HETEROGENEOUS-SYNTHESIS-R1/repro/fixtures.py\`; verify code Git blob/SHA256, fixture Git blob, shared semantic_hash blob, original reviewer blob in *separate immutable directory*, and exact test-overlay git blob from S03FR review.
2. Do **not** edit the S03R test file. Overlay *only* independently versioned new \`rawlsing_next/tests/test_hq286_s03fr_f6_repair_court.py\` from reviewer commit \`21bde003bce385a88c26c1fdefbbf1fb39849703\`.
3. Set \`S03F_CANDIDATE_ROOT=<FULL_EXACT_S03F_ROOT>\` and \`PYTHONPATH=<FULL_EXACT_S03F_ROOT>\`; the first is a required self-guard. Run from worktree root (proposed **not executed**):
   \`python3.11 -m pytest -q rawlsing_next/tests/test_pre553_heterogeneous_synthesis.py rawlsing_next/tests/test_hq286_s03fr_f6_repair_court.py -rxX\`
   and separately run source-free author only and reviewer only to preserve identities.
4. Expect by static inspection **12 of the 13 S03FR strict tests may pass and test_11_original_order_contract_strict_unmet should FAIL**, but treat these only as **predictions** until evidence. Any setup error is a setup HOLD, never substituted with PASS.
5. Retain exact command, origin worktree/tree SHA, environment, Python/pytest version, stdout/stderr logs+hashes, full case statuses, exit code, xfail/xpass, changed-file/object identity and machine/model/provider/quota telemetry **actually observed**.
6. Return to HQ as **external run evidence**; S03FR reviewer itself is Browser and did not operate local Mac. No real two-family product, source permission or adopted S03F issuer may arise from a source-free green suite.

## Resource/account statement

GPT-6 model family via ChatGPT Browser connected private GitHub. Requested High effort; actual effort/account alias / remaining capacity / Go normalized pool and Codex quota **UNKNOWN** to reviewer. No paid overflow requested or authorized, and none initiated by reviewer. No local shell, Python, Mac worktree, subprocess or test exit observed **in this review session**. Only GitHub remote read/write refs, blobs, tree/commits verified. These details must not be backfilled from separate agent L02.
