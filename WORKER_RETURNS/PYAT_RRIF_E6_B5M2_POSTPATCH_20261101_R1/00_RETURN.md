# PYAT-RRIF-E6 — HOSTILE POST-PATCH B5/M2 FIXTURE AND FAN-IN COURT

Status: `HOLD_E5_LOCAL_SOURCEFREE_FANIN_PENDING_OWNER_AUTHORIZED_VERSIONED_M2_FIXTURE_AMENDMENT`

Role: independent I3 hostile B5/M2 local-integrity and accepted-test reviewer. This session is not E5, S06G, E2 or original M2 author, not HQ, not canonical integrator and not a source/scientific issuer.

Branch: `review/pyat-rrif-e6-b5m2-postpatch-hostile-20261101-r1`

Startup PRE-MAIN: `8e44ca9c751049d65e6def47600b5c073ee04b29`

Frozen review inputs:

| Input | Exact commit | Remote readback |
|---|---|---|
| E5 head | `96e6d49ac18274332751c5fbb87c6ed370e8fd9c` | `refs/heads/agent/pyat-rrif-e5-s06g-b5m2-compatible-hardening-20261101-r1` |
| E5 source content | `f3defd3cb84e2bab4be3df3300fd1289c6ebadfb` | ancestor of E5 head |
| E2 review head | `46a4ba7baf90d75c4941e9ddc2e372e07b4db0f4` | `refs/heads/review/pyat-rrif-e2-s06g-integrity-hostile-20261031-r1` |
| S06G reference | `0ff13995cc55db00d02b08004e62f75d4c5cb36e` | `refs/heads/agent/rabochii-pyat-r3-hq285-s06g-native-atomic-integrity-repair-r1` |
| S06FR review | `1b5b6072f855a74864c82d0f1b3923327bfb8b99` | `refs/heads/agent/reviewer-pyat-r3-hq284-s06fr-native-security-r1` |

Direct `git ls-remote` readback before review: E5 `96e6d49ac18274332751c5fbb87c6ed370e8fd9c`; E2 `46a4ba7baf90d75c4941e9ddc2e372e07b4db0f4`; S06G `0ff13995cc55db00d02b08004e62f75d4c5cb36e`; S06FR `1b5b6072f855a74864c82d0f1b3923327bfb8b99`. The final reviewer branch tip is the exact pushed 40-hex SHA reported by `git ls-remote` in the live return after this directory is committed. No production file on this reviewer branch was changed.

## Bottom line

E5 is a genuine, locally effective sourcefree hardening of B5/M2. Its production blobs are byte-identical to S06G, its public signatures and adjacent composition calls are preserved, its S06G court is stable, and its E2 court is stable. The early `RELEASE_UNAVAILABLE` refusal is a lawful tightening at the repository writer boundary, not a permissive-resolution regression; the original downstream `PUBLICATION_BINDING_MISMATCH` oracle remains reproducibly preserved after lawful foreign release import.

Fan-in is nevertheless **HOLD**:

- `test_17_binding_cannot_resolve_different_release` and `test_18_endpoint_failover_only_among_same_release` remain byte-unchanged and RED with `M2ReleaseError: RELEASE_UNAVAILABLE`.
- E5 adds new reconciled tests but does not amend or version the two accepted fixtures, and the frozen evidence contains no accepted-M2 owner permission for a versioned fixture amendment.
- The unfiltered court is therefore `179 passed, 14 failed, exit 1`, not green. The filtered `179 passed, 14 deselected` selection is a selection, not acceptance.
- No owner permission was invented. This is a named governance/contract HOLD, not a newly found source defect.

## Reproduced court

| Court | Result | Verdict |
|---|---:|---|
| Unfiltered E5 court | 179 passed, 14 failed, exit 1; 0 skip/error | RED, honestly reported |
| Same court, 14 deselected | 179 passed, 14 deselected, exit 0 | selection only |
| Accepted B5 | 39/39 | PASS |
| Accepted M2 | 26/28 | FAIL at two unchanged fixtures |
| S06G repair court | 42/42, stable over 6 runs | PASS |
| E2 independent court on E5 | 10/10, stable over 12 runs | PASS |
| Adjacent EE14 + world composition | 45/45 | PASS |
| Frozen S06FR overlay on E5 | 17 passed, 12 historical `OBSERVED` failures | expected historical RED |
| E6 reviewer-owned adversarial court | 11/11 | PASS |
| PRE-MAIN accepted B5 + M2 | 39/39 + 28/28 | baseline comparison |
| E2 court on PRE-MAIN baseline | 9-10 failures; race case nondeterministic | differential caveat |

## Source and fixture integrity

- Lifecycle blob `dadf2362f3195c28ebaf97655e28cdba72c04fb3` equals S06G.
- Release blob `1cb7692399aad8fb272c8c9ce956719527829007` equals S06G.
- S06G test blob `9964464cd86c077ff5b9a99cea6fb0a41e516c80` differs from S06G's `23aaf95d315980ea7587373e30188c7f36cb2b73` only at the fixture import line.
- E2 test blob `9a469ad0940216e02967c94159db943d2979154a` is byte-identical to E2's reviewer test.
- The S06F-named file is a helper-only shim; its five helpers are AST-identical to the historical S06F helper functions and it contains no test function. No S06F acceptance program was transplanted.
- Both accepted test files are byte-unchanged: M2 `d45b54190815b4c6af506579962a9aac8a7074c2`, B5 `d7ab66fe50aacb2d4223dca223d0d702af11270c`.

## ABI and caller reality

Public B5/M2 signatures used by `rawlsing_next/pre553_learned_world_composition.py` are unchanged; an inspected signature comparison was equal. `M2Repository._insert` changed from private static method to private instance method. The only production importer of B5/M2 is `pre553_learned_world_composition.py:33/40`, and that composition module has no non-test importer. No live production caller exists at this cut.

## Boundary honesty

The patch is local in-memory exception atomicity, serialization and semantic checkpoint replay only. It provides no durable commit, OS-kill recovery after unsaved transactions, multiprocess or fork/pickle custody, authenticated issuer, revocation/as-of source, protected CURRENT or external custody. `native_security_mode` remains `LOCAL_UNAUTHENTICATED`; `require_external_issuer` holds. No original survey, source-native, actor, N11/N12 or source-right execution was performed.

## Grades

- ENGINEERING: `POSITIVE_LOCAL_SOURCEFREE_REPAIR_MERIT__NOT_FANIN_READY_BECAUSE_TWO_ACCEPTED_M2_FIXTURES_REMAIN_RED`
- SCIENTIFIC: `HOLD__NO_SOURCE_NATIVE_OR_EXTERNAL_VALIDATION`
- AUTHORITY: `HOLD__NO_EXTERNAL_ISSUER_OS_KILL_MULTIPROCESS_OR_PROTECTED_CUSTODY`

## Required next action

The accepted-M2 owner must issue an explicit versioned fixture amendment that either authorizes lawful foreign-release registration in the two accepted scenarios while preserving `PUBLICATION_BINDING_MISMATCH`, or formally supersedes those fixtures. Do not weaken `release_exact`, do not edit accepted tests in place without owner authority, and do not treat the 14-deselected selection as green. A distinct reviewer must re-check the exact resulting SHA. No adoption, merge or self-review is claimed here.

## Artifacts

- `E5_SOURCE_AND_HUNKS.md`
- `ACCEPTED_M2_TWO_FIXTURE_VERDICT.md`
- `INDEPENDENT_TEST_AND_FAULT_RECEIPTS.md`
- `FINITE_FANIN_OR_HOLD_DECISION.md`
- `reviewer_tests/test_e6_independent_review.py`
- `test_receipts/`
