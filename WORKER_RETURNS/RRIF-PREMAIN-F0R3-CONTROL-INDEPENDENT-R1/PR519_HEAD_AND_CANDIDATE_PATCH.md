# PR #519 live head and F0R3 candidate patch

## Exact live identities

- PR #519 head: `59c9a7a4a4fae60d809c1ef545ff4e48906d0dd0`.
- PR #519 merge ref: `7abc24f2ec3884702d0bc41248ae13d7a367a6ae`; parents `299f41e97a43c67be9cc76a79fa49b48f4e12e54` and `59c9a7a4`.
- Current PRE-MAIN: `8e44ca9c751049d65e6def47600b5c073ee04b29`.
- Current PRE-MAIN does **not** contain `CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/**`; the reviewed control change is still only on PR #519.
- F4 `9fb7caebc266f1e3a8315d87ff446d5db1634cc5` is not an ancestor of current PRE-MAIN.

## Exact source blobs at PR #519 head

| Path | Git blob |
|---|---|
| `CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/00_FROZEN_INITIAL_SEED.json` | `4ffe5f95b84505431a928f7ef6d0e7b5931f63d8` |
| `CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/01_RETURN_EVENT_LOG.json` | `60fd8e26b3d8c4bd66f27900b82c9359cf4ad652` |
| `CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/02_FLIGHT_AND_PR_REGISTER.json` | `9306df304a8f12029c8daacb2eb97c9fcb58df56` |
| `CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/verify_branch_fanin.py` | `6fa0ce132e68f1fea7d67321129a2af2627a5d94` |
| `.github/workflows/pre-main-branch-fanin-receipts.yml` | `ce1ef40b5f2568c52a44d1ddc01a98647f3bf322` |

The event log has 32 events; the flight register has 32 workers and 5 PR rows. The F0R3 `current_head_59c9a7a4` data blobs match these exact values.

## Candidate patch

- Candidate validator: `WORKER_RETURNS/PREMAIN-F0R3-POSTSEED-AUTHORITY-LOG-REPAIR-R1/candidate/verify_branch_fanin.py`
- Blob: `2fc1c3c7ae6113d12b70abb655ff123a6ae9c895`
- SHA-256: `ab26b3a014a16d5ec0f1c3edb5cfbbe284440b9a7a6580e4bd3631b971af1abb`
- Patch blob: `424d87370b0e5fdfad13705335558eff37be9257`
- Patch SHA-256: `4fb4f8401e0f73c5b2b39044a5b14c10e848df6f271f4ad76bfb828f23ce3c74`
- Tests blob: `80eaf4feaaa34760129c7efe3a4019f67465052a`
- Reproduction harness blob: `d5ce55cbfbecf8f8da264977e9c365cd15d4f388`

`git apply --check` exits 0 against the live PR #519 validator; the patch changes only that validator (90 insertions, 7 deletions). It does not change the seed, event log, flight register, workflow, PR #519, PRE-MAIN or any source/science file.

## Executed result

- Original validator on current 32/32 data: exits 0 with **13 witnesses**, legal candidate accepted; it **admits N1–N4, N6, N7**.
- Candidate validator on current 32/32 data: exits 0 with **20 witnesses**, N1–N7 rejected, legal `OWNER_ADOPTION_CANDIDATE` accepted with `adoption=false`.
- Candidate unittest: 12 tests OK; witness count 20.
- F0R3 reproduction on current data: N1 `UNVERIFIED_SOURCE_AUTHORITY`, N2 `SCIENCE_NONISSUER`, N3 `REVIEWER_TARGET_RETURNED_ONLY`, N4 `PR_REMOTE_STATE_UNVERIFIED_519`, N5 append-reuse rejected by candidate (original also rejects via a different log mismatch), N6 `PR_APPEND_ORDER_513`, N7 `AUTHORITY_NONISSUER`.
- The old 13-witness green is not treated as a pass for the new bytes; the current 32/32 corpus was used.

## Currentness boundary

The candidate applies to the PR #519 validator, but the PR's merge ref is still based on `299f41e9`, while current PRE-MAIN is `8e44ca9c`. A merge of the stale PR cannot be treated as a current canonical fan-in. The owner must rebase/merge-forward, re-lock the exact head, and rerun the same exact tests before any merge.

The PR #519 workflow is `PRE-MAIN Branch Fan-in Receipt Integrity (sourcefree)`, job `receipt-contract`. It is path-filtered to `CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/**` and the workflow file, with `pull_request` and push-to-PRE-MAIN triggers. It has no `workflow_dispatch`; no candidate-branch CI was available. The exact Python tests were run locally.
