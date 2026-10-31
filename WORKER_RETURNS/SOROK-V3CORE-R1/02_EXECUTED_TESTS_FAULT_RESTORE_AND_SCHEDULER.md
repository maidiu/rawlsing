# SOROK V3CORE-R1 — executed tests, fault/restore and scheduler

## Runtime and pins

| Binding | Value |
|---|---|
| Repository | `maidiu/rawlsing` (private) |
| Branch | `agent/sorok-v3core-r1-sourcefree-activity-time-adapter-20261030` |
| Base | `750548ddbb9b4392a16ce93097b856f349e16182` |
| Inputs | RCF-A `e66dc53a…`; R5 `aebb2452…`; O1 `501ea1f5…`; I1 `7d44e300…` |
| Host | `oldMac`, macOS 13.7.8, x86_64 |
| Python | 3.11.3 |
| pytest | 9.1.1 |
| Historical archive | `/Users/matthewsmith/Desktop/Rawlsing/Rawlsing_code_bundle_staging.zip` |
| Archive SHA-256 | `3f2c5ed9…` observed; TD-R05 expects `953c9149…`; container mismatch preserved |
| Candidate | `candidate/` in this return |

All commands below ran in `candidate/`. `PYTHONPATH` always included the
candidate root, `candidate/vendor` (historical V3/V2 source), and
`candidate/vendor/py3deps` (PyYAML 6.0.3 only; no source edit).

## Court results

| Court | Command | Result |
|---|---|---|
| Unchanged V3 source tests | `python3 -m pytest -o addopts='' -q -p no:cacheprovider vendor/v3/tests/test_architecture_invariants.py vendor/v3/tests/test_step_logic.py vendor/v3/tests/test_v5_pressure_flow.py vendor/v3/tests/test_v5_pressureflow_golden_run.py` | **40 passed** in 1.77 s |
| V3CORE adapter tests | `python3 -m pytest -o addopts='' -q -p no:cacheprovider tests` | **46 passed** in 6.31 s |
| I1 unchanged consumer tests | `cd vendor/i1 && PYTHONPATH=$PWD python3 -m pytest -o addopts='' -q -p no:cacheprovider tests/test_i1_guarded_consumer.py` | **8 passed** in 6.25 s |
| 19-step mutation | copy `vendor/v3` to temp, move `render_layer` before `field_update`, run unchanged `test_step_order_immutable` | **1 failed as expected** in 0.18 s |

Evidence:

- `candidate/evidence/court_results.json` SHA-256 `6f2b1378961549cfa7b5ff17ca4505959f86b8d277d7e5627bc2db38cbb0e3aa`.
- `candidate/evidence/unchanged_v3_source_junit.xml` SHA-256 `71738a0d442eeeaab957b9450e0e8ee6d75163b5d045b838972b829f1e3875f6`.
- `candidate/evidence/v3core_adapter_junit.xml` SHA-256 `3715c9b54ce946070803e38b89526840e775d9081790b7262c595f32d0e9f156`.
- `candidate/evidence/i1_unchanged_junit.xml` SHA-256 `e58c6b28e3992be29ac74b5573ad507a0f54521c0c455638e6db31254c43af34`.
- `candidate/evidence/mutated_19_step_order.stdout.txt` SHA-256 `b587e7753d7d953d51fe71df60a820c7c824ebb8cdba19fe567aeeed9def49f3`.

The unchanged 40-test set is exactly the RCF-A selected V3 court, including
`test_step_order_immutable`, `test_llm_no_backbone_mutation`,
`test_events_cannot_write_domains_or_peak_routing`,
`test_no_derived_fields_in_backbone_state`, `test_run_one_year_advances_and_derived_valid`,
the 24 pressure-flow tests and the golden-run evidence test. The mutation court
is the original unchanged test; its failure message is:

```
AssertionError: Core step id 'render_layer' missing or out of order in steps...
```

## Scheduler

The scheduler loads the exact historical
`vendor/v3/v3_yearly_step_order.yaml` through the historical
`v3.core.config_loader`. `validate_step_order` requires:

1. `core_steps` equals the exact 19 IDs in `ANNUAL_STEP_IDS`;
2. the 19 IDs appear in order as a subsequence of `steps`;
3. append-only extensions appear after the last core step;
4. each step's `derived_compute` set equals the schedule's
   `compute_after_step` set.

Admitted adapters:

| Step | Adapter | Status |
|---|---|---|
| `event_sampling` | actual event ingress; never samples | `APPLIED_TEST_ONLY_SOURCEFREE` |
| `capacity_update` | recorded material accounting only | `APPLIED_TEST_ONLY_SOURCEFREE` |
| `render_layer` | exact `render_year`, nonmutation court | `DERIVED_EVALUATED_SCOPED` |
| other 16 steps | no issued transition rule | `HELD_MISSING_ISSUED_RULE` |
| post-year pressure flow | conserved-charge model not issued | `HELD_CONSERVED_CHARGE_MODEL` |

A year with an actual source event therefore records 19 step outcomes plus one
post-year flow hold. A year without an actual source event cannot become a
developmental occurrence: `HELD_NO_EVENT_SOURCE`; removing a bound event yields
`HELD_SOURCE_EVENT_WITHDRAWN`. Neither path samples or fabricates an event.

## Fault matrix

| Fault | Expected terminal | Test |
|---|---|---|
| Foreign actor | `HELD_FOREIGN_ACTOR` | `test_foreign_actor_is_held_without_mutation` |
| Sorok Neo N11 event clock | `HELD_CLOCK_MISMATCH` | `test_sorok_n11_clock_is_not_an_m25_year_event` |
| Pyat N11 objective-world clock | `HELD_CLOCK_MISMATCH` | `test_pyat_n11_objective_world_clock_is_not_an_m25_year_event` |
| Wrong annual binding | `HELD_CLOCK_BINDING_MISMATCH` | `test_wrong_annual_binding_is_held` |
| Missing actor perception | `HELD_MISSING_PERCEPTION` | `test_missing_actor_perception_is_held` |
| Missing actor response | `HELD_MISSING_RESPONSE` | `test_missing_actor_response_is_held` |
| No competent transition rule | `HELD_MISSING_RULE` | `test_missing_transition_rule_is_held_and_distinct_from_no_change` |
| Unissued scientific rule | `HELD_RULE_NOT_ISSUED` | `test_unissued_scientific_rule_is_held` |
| Evaluated test-only zero | `NO_CHANGE_EVALUATED` (committed, no material delta) | `test_evaluated_test_only_zero_is_no_change_not_missing_rule` |
| Source event removed | `HELD_SOURCE_EVENT_WITHDRAWN` | `test_source_event_removal_cannot_become_an_annual_occurrence` |
| Empty year, no source event | `HELD_NO_EVENT_SOURCE` | `test_empty_year_without_source_event_is_held` |
| Duplicate event | `HELD_DUPLICATE_EVENT` | `test_duplicate_event_is_not_reapplied` |
| Unowned event | `HELD_ACCOUNTING_MISMATCH` | `test_unowned_event_is_held_as_accounting_mismatch` |
| Forbidden default injection | `HELD_FORBIDDEN_DEFAULT` | `test_injected_default_blocks_the_year_without_commit` |
| Renderer mutates backbone | `HELD_RENDERER_MUTATION` | `test_malicious_renderer_mutation_is_rolled_back` |
| Derived mutation of live state | held/blocked | `test_derivation_is_scoped_and_does_not_mutate_live_state` |
| Transaction save failure | `HELD_TRANSACTION_ABORTED`, old ledger unchanged | `test_failed_commit_leaves_existing_ledger_unchanged` |
| Cold reload | identical state hash, material facts and year count | `test_cold_process_reloads_identical_material_projection` |
| Restored positive | `APPLIED_TEST_ONLY_SOURCEFREE`, material index +0.3 | `test_source_event_removal_then_restored_positive` |

## First current consumer

`project_actual_market_event` drives I1's actual `wait(30)` and consumes the
actual B `OFFSCREEN_REPAIR` C12 world event. It does not write to I1's C12
database and does not create a rival C9 store.

| Reading | Actual value |
|---|---|
| Event | `TEST_ONLY_BP4_WORLD_EVT_3da61c63ecdb310fb4f1962e636594992b8b34d1b2099624594cfdb79bf7c93c` |
| Source clock | `40` in `CURRENT_C12_ACTOR_WORLD_CLOCK` |
| Cash | `54 -> 56` |
| Completed units | `3 -> 4` |
| Position | `workshop -> market` |
| Material capacity index | `11.3 -> 11.6` (`+0.3`) |
| Durable state hash | `1a42e424… -> 5255a469…` |
| Projection ledger SHA-256 | `056ff04d2d756a649308352e9507a5cac6cb99c8ce0467ded608c395bd220ab1` |
| Cold reloaded hash | `59ecb508…` (equal) |
| C12 counts before/after | `checkpoint 2, episode 3, perception 4, world_event 3` (equal) |
| C12 authenticity | `OWNER_ANCHOR_REQUIRED` |
| Canonical C9 claimed / rival store | `false / false` |

Evidence: `candidate/evidence/first_consumer_probe.json` SHA-256
`d075f2c5fd6017b3980762239c6d46c9290b3bc14e56ee92fe8777772214e2a4`.
The I1 fixture's observed world artifact hash is retained in
`projection.source_metadata`; because that fixture artifact varies between
runs, it is not part of the durable state hash. The adapter's state hash is
deterministic across repeated actual-event runs.

The difference is a recorded material fact and a read-only material-scope
derived index. No class, identity, ethnicity, religion, Enneagram or typographic
value is read or written.

## Cold reload and restored positive

- Cold subprocess `tools/cold_probe.py` reloads the ledger with the same state
  hash, cash, material facts, year count and empty forbidden-default reason list.
- A simulated save failure leaves the previous ledger byte-identical and rolls
  the in-memory projection back.
- Removing the actual event yields `HELD_SOURCE_EVENT_WITHDRAWN`; restoring the
  same actual event yields `APPLIED_TEST_ONLY_SOURCEFREE` and the `+0.3`
  material-index difference.
- A second actual event (`EV2`, annual year 2) continues the durable projection
  to cash `58` with two year records, then reloads cold.

## NOT_RUN

- The TD-R05 reported **80-test aggregate** as one current suite; only the
  RCF-A selected 40 unchanged tests were run.
- Full historical V3/V2 suite.
- Native source/respondent data, CAN/ADP/SCI05 issuance, native person.
- I1 durable C9 handoff, external C12 anchor, native A5 person.
- Pyat N11/N12 native world acceptance and production/PRE-MAIN integration.
- Any claim that the material-scope index is a full psychological person metric.

## Engineering verdict

**PASS SCOPED (local candidate).** 40 unchanged source tests, 46 adapter tests
and 8 unchanged I1 consumer tests pass; the original 19-step mutation test
fails as expected. The first consumer demonstrates a real I1-originated durable
material difference and cold reload. This is not scientific issuance, native
personhood or owner adoption.
