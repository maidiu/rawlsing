# All twelve hostile tests with exact exits

**Successor implementation:** `SOURCEFREE_CANDIDATE_AND_VERSIONED_API/owner_bound_successor.py`
blob `08f0bea429a8f35223db8acf757ef7b714805603`; hostile court
`SOURCEFREE_CANDIDATE_AND_VERSIONED_API/tests/test_twelve_hostile_attacks.py`
blob `37ad5b63ed2be6fa6b87ee4e93483e51de5b2865`.

**Session:** OpenCode `1.18.34`, agent `build`,
`opencode-go/deepseek-v4.1-flash`, variant `max`, session
`ses_e6f557010ffeVc8ejV937G5Ii9`, PID `28096`.

**Source cuts:** startup `d0342290...`; current PRE-MAIN
`8e44ca9c751049d65e6def47600b5c073ee04b29`; predecessor overlay
`9c030bf4c239d2e14f2b5a8a02ff7b44906cd0c7`; hostile predecessor report
`33b5363a20d44cfb42b3d1e86fdb9615710adb23`; original PE
`e61a26ce24f023a53d6b116bb9eca2fb7b6f8e65`.

## Successor command and exit

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/PYAT-PE-SC0-OWNER-BOUND-SUCCESSOR/SOURCEFREE_CANDIDATE_AND_VERSIONED_API/tests/test_twelve_hostile_attacks.py
# 14 passed in 5.43s, exit 0
```

The file contains the twelve commissioned attacks plus two additional oracles
(zero/null geometry treatment and narrow issuer version/time/operation scope).
All fourteen pass because every attack is refused and every allowed treatment is
exact. Raw log:
`SOURCEFREE_CANDIDATE_AND_VERSIONED_API/evidence/candidate_hostile_12.log`;
JUnit:
`SOURCEFREE_CANDIDATE_AND_VERSIONED_API/evidence/candidate_hostile_12.junit.xml`.

## Predecessor reproduction

```bash
HQ297_EXACT_PE_ROOT=$PWD PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 \
  python3 -m pytest -q -p no:cacheprovider \
  /tmp/opencode/pe-hostile-review/hostile_pe_tests.py
# 12 passed in 1.26s, exit 0
```

In the predecessor court, "passed" means the attack **succeeded** against the
overlay. That is hostile evidence, not predecessor acceptance. Receipt:
`SOURCEFREE_CANDIDATE_AND_VERSIONED_API/evidence/hostile_predecessor_12.log`.

## Attack-by-attack

| # | Attack | Successor test node | Successor result | Refusal / exact binding |
|---|---|---|---|---|
| 1 | Altered absolute horizon/sanctions with unchanged selection digest | `test_hostile_01_altered_horizon_and_sanctions_with_unchanged_digest` | PASS | `WORLD_VALUES_TAMPERED_REFUSED`; no receipt/world/geometry |
| 2 | Cells sum to 2 with denominator 100 | `test_hostile_02_cells_sum_two_with_denominator_one_hundred` | PASS | `GEOMETRY_CELL_SUM_MISMATCH_REFUSED` |
| 3 | Fake refresh receipts from provider whose refresh methods fail | `test_hostile_03_fake_refresh_receipts_from_failing_provider` | PASS | raising methods -> `REFRESH_CHANNEL_FAULT_REFUSED`; unaudited receipts -> `REFRESH_AUDIT_MISSING_REFUSED` |
| 4 | Enriched receipt mutation absent from result hash | `test_hostile_04_enriched_receipt_mutation_changes_result_identity` | PASS | formula equality proves the result hash covers the receipt hash; mutated receipt/result hashes differ |
| 5 | Source-promotion flag TRUE from a faulty producer | `test_hostile_05_source_promotion_from_faulty_producer_is_refused` | PASS | `SOURCE_PROMOTION_REFUSED` for echo true and upstream authorship true; test-only grant cannot issue `SOURCE_PROMOTION` |
| 6 | HELD_AUTHORITY with missing scope | `test_hostile_06_held_authority_missing_scope_is_refused` | PASS | `NEGATIVE_STATUS_SCOPE_REFUSED` for null scope or missing risk ref |
| 7 | Unrestricted ALL_TIME reversal grant for unauthorized target/risk | `test_hostile_07_all_time_grant_does_not_erase_target_or_risk_scope` | PASS | `ISSUER_TARGET_REFUSED` / `ISSUER_RISK_REFUSED`; ALL_TIME removes only expiry |
| 8 | Automatic import/monkeypatch through PYTHONPATH | `test_hostile_08_no_sitecustomize_or_pythonpath_monkeypatch` | PASS | no `sitecustomize.py`; imported provider identity unchanged; subprocess prints `False` and `rawlsing_next.pre553_empirical_possibility_provider` |
| 9 | Stale clock/revision and invalidated current | `test_hostile_09_stale_clock_revision_and_invalidated_current` | PASS | `WORLD_REVISION_MISMATCH_REFUSED`, `STALE_CURRENT_REFUSED` (publication or currentness), `INVALIDATED_CURRENT_REFUSED` |
| 10 | Wrong target/condition role direction | `test_hostile_10_wrong_target_condition_role_direction` | PASS | producer direction mismatch -> `ROLE_DIRECTION_REFUSED`; swapped refs -> typed refusal (`ISSUER_TARGET_REFUSED` or `ROLE_DIRECTION_REFUSED`) |
| 11 | Missing producer or severed consumer | `test_hostile_11_missing_producer_or_severed_consumer` | PASS | `PRODUCER_MISSING_REFUSED`, `PRODUCER_FAULT_REFUSED`, `CONSUMER_SEVERED_REFUSED`, `WORLD_PROVIDER_MISSING_REFUSED` |
| 12 | Wrong replay/as-of or changed world owner | `test_hostile_12_wrong_replay_asof_or_changed_world_owner` | PASS | exact replay succeeds; changed as-of raises `OwnerBoundReplayError`; changed owner -> `WORLD_OWNER_MISMATCH_REFUSED`; changed revision -> `WORLD_REVISION_MISMATCH_REFUSED` |
| + | Zero/null geometry treatment | `test_geometry_zero_cell_is_exact_and_zero_or_null_is_refused` | PASS | zero cell exact at denominator 62; null numerator -> `GEOMETRY_REFUSED`; zero denominator -> `GEOMETRY_ZERO_DENOMINATOR_REFUSED` |
| + | Narrow issuer version/time/operation | `test_issuer_version_time_and_operation_are_narrow` | PASS | wrong version/fake hash -> issuer missing; future/expired -> `ISSUER_TIME_SCOPE_REFUSED`; wrong operation -> `ISSUER_OPERATION_REFUSED` |

## Why each attack now fails closed

The predecessor trusted presence and shape. The successor checks the semantic
preimage and the actual operation:

- World values are recomputed into the selection digest, so changing a value
  while retaining the old digest is detected.
- Geometry is checked for exact cell conservation, not just a plausible first
  numerator.
- Refresh receipts come only from actual provider methods, are audited by
  invocation counters, and carry an invocation token and recomputed successor
  digest.
- The result identity is computed over the full enriched receipt, not the
  original pinned receipt.
- A contradictory source-promotion flag is refused, not overwritten.
- Negative-status rows require source/scope and exact risk scope.
- The exact issuer grant has target, risk, world, operation and time scopes;
  `ALL_TIME` is not a scope wildcard.
- The candidate has no `sitecustomize.py` and never replaces an upstream module
  symbol.
- Currentness and revision are exact; invalidated or stale worlds cannot serve.
- Producer role direction and target/condition refs are cross-checked.
- Missing/failing producers and consumers produce typed refusals with no
  receipt.
- Replay is deterministic and world-owner/as-of changes cannot reproduce the
  original identity.

## Explicit NOT_RUN / UNKNOWN

- The predecessor's P41/E04L or #536 worker suites were not run; only the exact
  hostile predecessor court and the published overlay courts were run.
- No production receiver or production issuer exists for the successor, so no
  production-adopter test is claimed.
- No original survey/actor/N9/model-use/N11/N12/Sorok operation was executed.

## Verdicts

**ENGINEERING:** `ACCEPT_AT_TEST_ONLY_SOURCEFREE_SCOPE__ALL_TWELVE_ATTACKS_FAIL_CLOSED__TWO_ADDITIONAL_ORACLES_GREEN__PREDECESSOR_ATTACKS_REPRODUCED_AS_HOSTILE_EVIDENCE`.

**SCIENTIFIC:** `HOLD__SYNTHETIC_C1_N10E_GEOMETRY_ONLY__NO_ORIGINAL_RESPONDENT_SOURCE`.

**AUTHORITY:** `HOLD__TEST_ONLY_SOURCEFREE_ISSUER_ONLY__NO_COMPETENT_SOURCE_N9_WORLD_OR_PRODUCTION_GRANT`.
