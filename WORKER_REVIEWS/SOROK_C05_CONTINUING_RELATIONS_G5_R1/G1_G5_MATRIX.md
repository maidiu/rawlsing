# C05 independent G5 — G1–G5 matrix

**Verdict:** `REVISE_EXACT_DEFECT`
**Candidate:** `9cf13763b0061400e2c936eaf1d0a2f4b76a03f7`
**Report:** `bc45f699a22708aae3df7e34b1ba3b272a362565`
**Start:** `ee82397a979e52eab83f2bd4ea48ed9c28ea7ab9`
**Reviewer:** `ses_e2186e745ffecK1Ilg4cw26pVu`

| Gate | Status | Evidence | Limit |
|---|---|---|---|
| G1 source/owner/custody | `PASS_SCOPED_SOURCEFREE` | exact HEAD/branch; implementation and report commits; product blobs `98cb4ce...`, `343cf08...`, test `4741264...`; implementation-to-report product diff empty; start-to-implementation product delta is one allowlist line plus the new module/test; product read-only; reviewer writes only this return and `.local-logs/sorok-c05-independent-g5/` | sourcefree grade only; no native ADP-015/C4 owner |
| G2 build/actual first consumer | `PASS_SOURCEFREE_NORMAL` | 34/34 listed tests exit 0; independent 89/89 probe; real P2Owner `ADMIT_EVENT` at clocks 228/234/240; separate parent/neighbor/Nadia contexts; depth 1 vs 2 normal reader difference; fresh-process cold exact; chronological retry `UNCHANGED` | event content is inherited sourcefree P2/S45/S39, not G2/G4 authored language |
| G3 falsification | `FAIL_REVISE_EXACT_DEFECT` | repeated depth-2 promotion with a new operation ID commits a change+head, raises `RELATION_CUSTODY_SEVERED` instead of `RELATION_PROMOTION_NOT_DEEPER`, and permanently severs the relation scope; coherent append-only relation change/head is accepted as caller input; unexposed/present and exposed/absent contexts behave as documented | exposure is caller-supplied; self-hash chain is not owner authentication; no native actor truth claimed |
| G4 boundaries/preservation | `PARTIAL_PASS_PRESERVATION__RELATION_DEPTH_STATE_MACHINE_FAILS` | C01 6, C04 identity 6, C04 custody 12, P2 owner 5 pass; change-primary and change-head sever give custody HOLD with event access intact and world/events/perceptions/checkpoints unchanged; restore exact; cold exact with no duplicates; the defect write changes only relation episodes and leaves world/events/perceptions/checkpoints unchanged | concurrent same-operation uniqueness and branch-fork replay `UNOBSERVED`; no concurrency campaign |
| G5 independent receiving | `REVISE_EXACT_DEFECT` | one exact reproducible in-scope public-writer defect, shortest runnable witness `newprobes/c05_defect_probe.py`; product unpatched | no `ACCEPT_SCOPED`; no self-G5 |

## Defect disposition

`C05_REPEAT_DEPTH2_PROMOTION_COMMITS_SELF_SEVERING_EPISODE`

- before: `QUALIFIED`, 2 changes / 2 heads / 49 episodes, C12 verify ok
- second depth-2 promotion, new operation `defect:promote:2`: raises
  `RELATION_CUSTODY_SEVERED`, but commits 1 change + 1 head (51 episodes)
- after: `HOLD_CUSTODY_SEVERED`, 3 changes / 3 heads, C12 verify still ok,
  world_events/perceptions/checkpoints unchanged
- exact retry of the first promotion now also `RELATION_CUSTODY_SEVERED`
- minimum correction: include prior `PROMOTE` in the pre-write depth check,
  refuse `RELATION_PROMOTION_NOT_DEEPER`, and verify inside the transaction

## Boundary (not the defect)

Caller-supplied `exposed_actor_ids` is explicit sourcefree fixture input. The
reader exposes only `DATED_EXPOSURE_ONLY` relation visibility and never labels
relation knowledge `PERCEIVED`; a present unexposed Nadia is relation-held, and
an absent never-participant observer becomes relation-qualified only when the
caller adds it to a later exposure. A coherent append-only change/head is
accepted as caller-authorized history; the self-hash pair does not prove an
owner operation. This is not native relation authority, perception proof,
psychology, G2 or J1.
