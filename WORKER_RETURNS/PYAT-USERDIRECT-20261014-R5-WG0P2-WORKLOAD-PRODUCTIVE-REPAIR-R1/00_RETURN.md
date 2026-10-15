# PYAT R5 WG0P2 — source-true workload productive repair

**Terminal: WG0P2_SOURCE_TRUE_REPAIR_EXECUTED__15_OF_15_REDS_FIXED__29_OF_29_PASS__NO_FABRICATION__NO_ALL35__NO_V3.**

## 1. Commission and custody

- Direct commission in the launch message (this message is the commission).
- Branch `agent/userdirect-pyat-20261014-r5-wg0p2-source-true-workload-repair-r1`, sealed startup `0d551d36ff19dc9806e0ad490ff33a1e4c25e381` (verified before writes).
- WG0I independent return read in full at `e1cc3016280d3714c485bf6ec7cecb360e4df3bc`; WG0P candidate read in full at `e19099460eed10a4d3da31a917af539aef87e485`.
- Role: bounded repair implementer, not WG0/WG0P author, HQ, adopter, or model actor.
- Write terrain: `WORKER_RETURNS/PYAT-USERDIRECT-20261014-R5-WG0P2-WORKLOAD-PRODUCTIVE-REPAIR-R1/` only. No production, canonical, CURRENT or protected-branch edits.

## 2. What was repaired (all 15 WG0I failures, same test names where behavior is required)

| WG0I failure | Repair | Test |
|---|---|---|
| 1/2 fallback on missing payload | No fallback exists; unknown op raises `KeyError` | `test_red_missing_operation_payload_must_fail_closed` |
| Negative numerator accepted | Native admission gate rejects out-of-domain values (`ValueError`) before ingest | `test_red_invalid_negative_observation_must_fail_closed` |
| Manual `object()` C11 injection | Real `ingest_c11_source_release` into one shared append-only repository; all 3 releases resolve as `C11LogicalRelease` | `test_red_no_c11_release_without_validated_c11logicalrelease` |
| Same-unit conditional without joint evidence | Same-grain pairs → `HELD JOINT_RISK_SET_UNPROVED`; a separate joint-risk-set proof produces real joint cells | `test_red_no_condition_without_joined_respondent_risk_set` + `test_repair_joint_respondent_risk_set_produces_real_conditional` |
| WITHHELD marked PRODUCED | Closed grant list: only `GRANTED_FIXTURE` permits; all other tokens HELD | `test_red_unknown_source_rights_must_hold` |
| `NO_SOURCE_ISSUER_OR_LICENSE` as permission | Same closed grant list | `test_red_arbitrary_grant_token_must_not_be_permission` |
| Freeze ignores options | Freeze hashes every native field | `test_red_freeze_must_bind_original_native_options` |
| Freeze ignores grant | Same | `test_red_freeze_must_bind_source_permission_status` |
| Withdrawn pairs dropped (8) | Retained as `HELD` with grant reasons | `test_red_withdrawn_conditioning_pair_must_retained_as_held` |
| Unrouteable pairs dropped (2) | Retained as `HELD` with route reasons | `test_red_routed_unknown_pair_must_retain_as_held` |
| Conflicting carrier silently dropped | `CONFLICTING_NATIVE_ITEM_IDENTITY` on same narrow identity with differing fields | `test_red_conflicting_source_same_canonical_identity_not_silently_dropped` |
| Conflicting op id overwrites map | `build_executable_plan` raises `ValueError` | `test_red_duplicate_op_id_with_conflicting_semantics_refused` |
| No-drop ledger absent | `ExecutablePlan.frontier_receipts` carries all 25 ops with dispositions | `test_red_no_drop_full_frontier_in_execution_plan` |
| Option mutation invisible to units | Item refs bind full native material; `unit_ref` differs | `test_red_original_native_category_mutation_propagates_source_value` |
| No issuer grant on plan | `ExecutablePlan.source_issuer_grant` carries the fixture grant, issuer and scope | `test_red_original_publisher_custody_hold_must_block_result` |

Repaired inventory: 5 marginals (3 PRODUCED + 2 HELD) + 20 directed conditionals (10 HELD + 10 INADMISSIBLE) = **25 ops, 0 PRODUCED conditionals** (frozen in `01_FULL_OPPORTUNITY_AND_DISPOSITION_LEDGER.json` before tests ran).

## 3. Actual executed proof (record → value → receipt → consumer)

- Real I02 ingest of 3 synthetic releases (10 + 4 + 3 native respondents; ordinal, routed and binary-indicator MR carriers; explicit risk sets incl. a real joint risk set).
- Real I03 marginals: 01 → `{0:1,1:2,2:2,3:1,9:0}/6`; 05 → `{0:0,1:2,2:1,3:1,9:0}/4`; 02 → joint household profiles (denominator 4) with derived option totals. Missing cell `9:0` is the owner's `OBSERVED_ZERO_IN_SUPPORTED_RISK_SET`, never a fabricated zero.
- Real batch run: 3 COMPLETED receipts, `FULL_MANIFEST_COVERAGE`; the owner's own summary reports `populated_data_execution_claim=False` (recorded, not overridden).
- Consumer effects derive exclusively from the plan fact registry populated by real executions (uncomputed refs raise `KeyError`).
- Changes propagate (mutated row changes 01, leaves 02/05 cell-identical); revocation supersedes 04's receipt (retained, W1 stable); resume reproduces full-run receipts; empty risk set yields typed `ZERO_SUPPORT`; small-n cohorts report exact counts.

## 4. Execution record

```
$ cd .../R1/repro
$ PYTHONPATH=/Users/matthewsmith/Desktop/Rawlsing:$PWD python3 -m pytest test_wg0p2_repair.py -q -p no:cacheprovider --junitxml=pytest_wg0p2.xml
29 passed in 3.14s   (exit 0)
```

Host Python 3.11.3, pytest 9.1.1. JUnit: `repro/pytest_wg0p2.xml`. Frozen oracles preserved (WG0P's return and code untouched in git history; this return adds repaired artifacts only). Pinned owner blobs verified against HEAD (batch `2d291600…`, objects `a61365b9…`, c11_repository `67c6eb64…`, ingest `37cd35fa…`, integrity `7c59aa13…`, query `03facecf…`, authority `ca65a7fd4…`).

## 5. Files

- `00_RETURN.md` (this file)
- `01_FULL_OPPORTUNITY_AND_DISPOSITION_LEDGER.json` (frozen 25-op frontier + expected values)
- `02_ACTUAL_C11_I03_BATCH_EXECUTION_OR_EXACT_HOLD.md` (owner entry points, commands, computed receipts)
- `03_INDEPENDENT_HOSTILES_AND_MUTATIONS.json` (15 hostiles + 5 mutations, all PASS)
- `04_ALL35_SOURCE_PERMISSION_AND_ADOPTION_CEILING.md` (non-claims and remaining owner work)
- `repro/wg0p2_workload.py` (sha256 `b168f032…`), `repro/test_wg0p2_repair.py` (sha256 `5acc64a2…`), `repro/pytest_wg0p2.xml`

Remote SHA verified by direct `git ls-remote` after push; reported below (a commit cannot self-reference its own future SHA). No self-adoption.
