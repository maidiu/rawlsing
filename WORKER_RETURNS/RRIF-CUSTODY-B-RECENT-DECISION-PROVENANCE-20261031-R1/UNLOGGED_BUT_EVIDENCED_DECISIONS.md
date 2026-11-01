# Unlogged but evidenced decisions

"Unlogged" means **not appended to `HQ_HANDOFF/DECISION_LEDGER.jsonl` in the branch-scoped form required to recover the branch estate**. It does not mean the decision is invalid. Every item below has an exact Git source.

## PR merges absent from the central ledger

| PR | Merge commit | Head commit | Evidenced decision | Limits |
|---|---|---|---|---|
| #525 | `99951b87d3f1d65180ecd5f1b419958c7b045e49` | `a0a4e6b0184b5c5de1f723913103bc34a833b9f6` | Sourcefree progressive N10E/C1→F8 consumer recovered into PRE-MAIN; 18/18 current-sourcefree tests; exact denominator mutation witness | `TEST_ONLY`; no N9/N10W live world, source science or N11/N12 |
| #526 | `750548ddbb9b4392a16ce93097b856f349e16182` | `6a38ef25057e577b7b546449844a8b33fc647a82` | R61 finite universal workload and source-byte custody recovered into PRE-MAIN; 105/105 universal-workload tests; three mutation faults detected | No original35 empirical grant, structural F5-F8, model-use, N11/N12 or actor claim |
| #563 | `8e44ca9c751049d65e6def47600b5c073ee04b29` | `91a854a9123ad33e84e5b847d8f4aecd60508046` | S7FIX 1885 identities / 3135 IDs accepted as inert Git data; PE overlay RED preserved; V2K historical interface RETIRE scoped; original item anti-join HOLD | Compact HQ intake; no production import or scientific grant |

These merge commits are in PRE-MAIN. Their PR descriptions, review comments and issue threads are not in the local Git evidence cut and the API is `403`. The merge bodies are the authoritative surviving decision text.

## Branch-local HQ adoptions

Nine `integration/pyat-hq*-accepted-r1` branches carry their own adoption evidence. Some are also named by ledger rows; the branch-local `00_HQ_ADOPTION.md`/`00_INTEGRATION_RECEIPT.md` is still outside the central append-only ledger procedure.

| Branch | Decision | Integration tip / accepted commit | Exact retention at current PRE-MAIN |
|---|---|---|---|
| `integration/pyat-hq130-c3-source-free-accepted-r1` | `HQD-2026-09-30-131` | `30686b185d4ceb2c94f61815ef70d8c8e76255d6` | `NO_CODE_BLOB_IN_PREMAIN` |
| `integration/pyat-hq139-c1-01-source-free-accepted-r1` | `HQD-2026-09-30-139` | `5fafb499d53dddadaf8a7b4fd46506e91a09d270` | `NO_CODE_BLOB_IN_PREMAIN` |
| `integration/pyat-hq145-c1-02-source-free-accepted-r1` | `HQD-2026-10-01-145` | `bc661188b51e995d9f5d74e55c4e37d2ba358a17` | `ALL_CODE_BLOBS_EXACT_IN_PREMAIN` |
| `integration/pyat-hq147-n10e-at17-source-free-accepted-r1` | `HQD-2026-10-01-147` | `52e41a41e8bc3b77390016a049095b5aea1721d0` | `PARTIAL_CODE_BLOBS_EXACT_IN_PREMAIN` |
| `integration/pyat-hq151-c5-n5-source-free-accepted-r1` | `HQD-2026-10-01-151` | `151d39260a803635f622323b14e42d96c7976d25` | `NO_CODE_BLOB_IN_PREMAIN` |
| `integration/pyat-hq159-c1-03r-source-free-accepted-r1` | `HQD-2026-10-01-159` | `9ec7eaff2646c1effd5192002967407a5c66bbef` | `ALL_CODE_BLOBS_EXACT_IN_PREMAIN` |
| `integration/pyat-hq162-c1-03a-source-free-accepted-r1` | `HQD-2026-10-01-162` | `26976201b3cf14f4cf89a45a909c780591f54bcb` | `ALL_CODE_BLOBS_EXACT_IN_PREMAIN` |
| `integration/pyat-hq166-at07-successor-spine-accepted-r1` | `HQD-2026-10-01-166` | `069ac61b5c90486e5b7bb633135b4743dfbd55df` | `NO_CODE_DELTA` |
| `integration/pyat-hq168-c1-03-successor-join-accepted-r1` | `HQD-2026-10-01-168` | `149c3d2636160d8de9b5a8be0c8b87195158077d` | `ALL_CODE_BLOBS_EXACT_IN_PREMAIN` |

## Reviewer verdicts

There are **72** explicit reviewer verdicts in the fate ledger: **36 REVISE**, **23 ACCEPT**, **7 HOLD**, **3 PASS**, **1 REJECT**, **2 FAIL**. Only a subset is quoted in a central-ledger row. The verdicts live in branch-local `00_RETURN.md`, `00_REVIEW.md`, manifests and disposition JSON files.

Examples:

- `agent/opencode-pyat-r109-r06-progressive-independent-review-r1` — `REVISE`; `e38a6a8c07ea6535a0d4de38053c15e4278934d7`; `e38a6a8c07ea6535a0d4de38053c15e4278934d7:WORKER_RETURNS/PYAT-R109-R06-PROGRESSIVE-INDEPENDENT-REVIEW-R1/00_REVIEW.md`
- `agent/opencode-pyat-r111-r06-binding-repair-review-r1` — `REVISE`; `ab578a9dc1c788847d0328976fe418948a44e7ac`; `ab578a9dc1c788847d0328976fe418948a44e7ac:WORKER_RETURNS/PYAT-R111-R06-BINDING-REPAIR-REVIEW-R1/00_REVIEW.md`
- `agent/opencode-pyat-r116-r06-combined-world-consumer-review-r1` — `REVISE`; `4069198e658bc05951d0792db210385ba777c80f`; `4069198e658bc05951d0792db210385ba777c80f:WORKER_RETURNS/PYAT-R116-R06-COMBINED-WORLD-CONSUMER-REVIEW-R1/00_REVIEW.md`
- `agent/opencode-pyat-r136-production-binding-review-r1` — `REVISE`; `28b29b5c7919f85989b03b40654ebb7caa0bc9c5`; `28b29b5c7919f85989b03b40654ebb7caa0bc9c5:WORKER_RETURNS/PYAT-R136-PRODUCTION-BINDING-REVIEW-R1/00_REVIEW.md`
- `agent/opencode-pyat-r138-production-repair-review-r1` — `REVISE`; `3f35210eadd9891100b6aae2ac01bb9b05d3406a`; `3f35210eadd9891100b6aae2ac01bb9b05d3406a:WORKER_RETURNS/PYAT-R138-PRODUCTION-REPAIR-REVIEW-R1/00_REVIEW.md`
- `agent/opencode-pyat-r152-native-scientific-binding-review-r1` — `REVISE`; `6476b82cedec3133ec1ac8df553acb1c243d0f0d`; `6476b82cedec3133ec1ac8df553acb1c243d0f0d:WORKER_RETURNS/PYAT-R152-NATIVE-SCIENTIFIC-BINDING-REVIEW-R1/00_REVIEW.md`
- `agent/opencode-pyat-r61-r01v-independent-review-r1` — `REVISE`; `b310c5469bb628a583d6e106946cddd08025ddc1`; `b310c5469bb628a583d6e106946cddd08025ddc1:WORKER_RETURNS/PYAT-R61-R01-INDEPENDENT-REVIEW-R1/00_RETURN.md`
- `agent/opencode-pyat-r61-r01v-r2-independent-review-r1` — `REVISE`; `3ac1e498a08648950d31df0bf52750f9335d24fa`; `3ac1e498a08648950d31df0bf52750f9335d24fa:WORKER_RETURNS/PYAT-R61-R01-INDEPENDENT-REVIEW-R1/revisions/r2/00_RETURN.md`

## Checkpoint dispositions

Nine branch-level checkpoint decisions were promoted as decisions; **114** further branches have a checkpoint disposition/grade snippet but not an explicit HQ decision at the branch's final state. Those remain in `DECISIONLESS_OR_CONTRADICTORY_CASES.md` rather than being promoted. The distinction matters: `AUTHOR_CUSTODY_VERIFIED`, `BANKED_CODE_OBSERVED`, `INTERRUPTED_UNQUALIFIED_PARTIAL` and `AUTHOR_CANDIDATE` are custody states, not acceptance.

## What is not evidence of adoption

- A worker `PASS` or `ACCEPTED` line in its own return.
- A green author test count.
- A branch name containing `accepted`.
- An E8 family `ALREADY_CURRENT` or `CURRENT_DIFFERENT` row.
- A staging branch containing the commit without an HQ decision.
- A reviewer `ACCEPT` at a bounded local scope, without an HQ fan-in decision.
