# G1–G5 review matrix — automatic currentness R1

**Overall:** `REVISE_EXACT_DEFECT`; **accept_scoped:** `false`; **full original:** `NOT_ESTABLISHED`.
**Source:** `ac09ac7f26fa2db8950f563e8f1decb0c32f5af5`; **runtime:** `6164e595...`; **test:** `6cf53b66...`.

| Gate | Required result | Observed result | Status |
|---|---|---|---|
| G1 Source identity and preserved boundaries | exact source identity | runtime blob 6164e595... / test blob 6cf53b66...; frozen #1095 verifier/workflow/task/GMT blobs match; seven protected foundations and historical scoped pins preserved | `PASS_SOURCE_IDENTITY_ONLY` |
| G2 Authenticated live GitHub currentness | authenticated live GitHub or expiring authenticated connector observation with fetch/expiry/missing-change-unavailable semantics | no network/GitHub client primitive; local baseline only; 2020 mtime read as 2026 as_of; simulated local head change accepted with zero items; stale unchanged baseline also no item | `FAIL` |
| G3 Mechanism review intake and restart | mechanism dispatch before task lookup; real supervised review job/immutable evidence/competent intake role | intake-review task_id=AUTOMATIC_CURRENTNESS_R1 exit 1 SOROK_CURRENTNESS_RUNTIME_RED: TASK_UNKNOWN: AUTOMATIC_CURRENTNESS_R1; _task_by_id before mechanism branch; fabricated C05 review accepted with arbitrary trust/session strings | `FAIL` |
| G4 STOP/RESUME/reconciliation authority | competent operator/HQ role/scope/evidence; arbitrary local events and resolve text rejected | USER_STOP/USER_RESUME with source.trust=ARBITRARY_LOCAL_TEST_STRING accepted; stop cleared; B02 became CANDIDATE; arbitrary resolve text cleared AUTHENTICATED_GITHUB_INTAKE_UNAVAILABLE | `FAIL` |
| G5 End-to-end cold/restart demonstration | after correction, one focused end-to-end sourcefree demonstration and real review receipt intake | not run because G2/G3/G4 fail first; author 17 tests/full crash matrix/canonical validator not rerun; no full success claimed | `NOT_RUN_BLOCKED` |

## Interpretation

- G1 only establishes that the reviewed source/blobs and historical boundaries are exact; it does not grant authority.
- G2 fails the core mission: currentness is a local snapshot read, not an authenticated live GitHub since-checkpoint observation.
- G3 fails the required independent mechanism transition: the runtime rejects its own mechanism task as `TASK_UNKNOWN`, while accepting a fabricated ordinary task review.
- G4 fails control authority: arbitrary local STOP/RESUME and resolve text are accepted.
- G5 is not run because the mission-critical gates fail first; no full success is claimed. The author’s 17-test result is author evidence only.

**Correction target:** one bounded source correction for real live GitHub freshness, mechanism review dispatch/job binding, and competent control/resolve authority; then one focused rereceiving of the exact fixed source. **STOP.**
