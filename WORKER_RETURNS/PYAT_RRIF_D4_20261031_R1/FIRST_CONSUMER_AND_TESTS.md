# First consumers and tests

**Rule applied:** a static import is not an actual consumer. A production module that has no production caller is not a live service consumer. Test imports are test-only.

**PRE-MAIN:** `8e44ca9c751049d65e6def47600b5c073ee04b29`

## Static consumer graph

### F6 heterogeneous synthesis

- `rawlsing_next/pre553_heterogeneous_synthesis.py` is absent.
- No current import of the F6 module exists.
- The RRIF-C `TEST_IMPORT` at `rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py:15` imports `pre553_n9_n10w_progressive_candidate`, not F6. It is not an F6 receiver.
- F6M/F6P is a branch-only sourcefree consumer chain: F6P consumes F6M; R40 accepted it at TEST_ONLY grain. It is not current.
- **Status: UNKNOWN.**

### F7 P07 native stage B

- `rawlsing_next/_p07_native_owner_stage_a.c` and `_p07_native_owner_stage_b.c` are absent.
- No current native import, caller or receiver exists.
- The current Python P07 owner is `rawlsing_next/pre553_source_relations.py`; it does not import or call native stage A/B.
- **Status: UNKNOWN.** No native test was run; native execution/TCB/refcount authority is HELD.

### F7 source relations

- `rawlsing_next/fiabc_succession_producer.py:59` maps `"F008"` to the path string `"rawlsing_next/pre553_source_relations.py"`. This is a path map used to build evidence references, not an import or call.
- No production import of `pre553_source_relations` was found.
- `rawlsing_next/tests/test_pre553_source_relations.py` imports and executes it.
- **Status: UNKNOWN.** The only execution is test-only; no production consumer.

### F7 temporal comparability

- `rawlsing_next/pre553_temporal_comparability.py` and `rawlsing_next/s04_temporal_policy.py` are absent.
- `rawlsing_next/_pre553_query_common.py:27` imports `pre553_empirical_authority`; this is not the historical temporal module and is not a comparability consumer.
- Current `pre553_empirical_authority.py:42` defines `TEMPORAL_EVIDENCE`, an exact source-native time binding. `pre553_structural_admission.py:281-282` requires `TEMPORAL_EVIDENCE` for time-scoped rules. That is not a trend, interpolation or cohort-comparability owner.
- **Status: UNKNOWN** for the historical temporal candidate; no current consumer.

### F8 service source scope

- `rawlsing_next/pre553_ee14_c1_owner_authenticated_ingress.py:90` imports the binder as `B`.
- The same module calls `B.evaluate_bound_positioned_subject_possibility` at line 659 and constructs/uses the binding request at lines 879 and 895.
- EE14 ingress itself has no production caller; only tests import it. `KEEP_EE14_T1_HOLD` remains in force.
- `rawlsing_next/tests/test_pre553_f8_receipt_permission_identity_hq254.py`, the three F8 binding courts, the applicability court and the EE14 tests exercise the binder.
- **Status: static production import/call in a module with no production caller. Actual service consumer: UNKNOWN.**

### Learned world product

- `rawlsing_next/pre553_learned_world_composition.py:33` imports `pre553_learned_product_lifecycle`.
- `rawlsing_next/pre553_learned_world_composition.py:40` imports `pre553_learned_product_release`.
- The composition module has no production caller; only `rawlsing_next/tests/test_pre553_learned_world_composition.py` imports it. `rawlsing_next/tests/test_pre553_ee14_selected_current_asof_hq260.py` imports the lifecycle module directly, also test-only.
- **Status: static production import inside a module with no production caller. Actual consumer: UNKNOWN.**

## Tests actually executed

All tests were executed in the isolated D4 worktree with the current PRE-MAIN source, sourcefree, without native extension execution, raw survey data, protected source or network access.

Environment: macOS, Python `3.11.3`, pytest `9.0.2`, `PYTHONDONTWRITEBYTECODE=1`, `-p no:cacheprovider`.

### Batch A — F8 and applicability

```sh
python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_f8_receipt_permission_identity_hq254.py \
  rawlsing_next/tests/test_pre553_service_f8_source_scope_binding_court.py \
  rawlsing_next/tests/test_pre553_service_f8_source_scope_binding_repair_court.py \
  rawlsing_next/tests/test_pre553_service_f8_binding_authentication_court.py \
  rawlsing_next/tests/test_pre553_service_source_applicability_court.py
```

Result: **215 passed, 0 failed** in 2.06s. This matches the HQ258 combined figure.

### Batch B — learned world and source relations

```sh
python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_learned_product_lifecycle.py \
  rawlsing_next/tests/test_pre553_learned_product_release.py \
  rawlsing_next/tests/test_pre553_learned_world_composition.py \
  rawlsing_next/tests/test_pre553_source_relations.py
```

Result: **121 passed, 0 failed** in 12.82s.

### Batch C — EE14, empirical query and progressive candidate

```sh
python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_ee14_c1_owner_authenticated_ingress_hq262.py \
  rawlsing_next/tests/test_pre553_ee14_selected_current_asof_hq260.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py
```

Result: **161 passed, 0 failed** in 9.89s.

### Total

**497 passed, 0 failed.** No test file was modified. No test data was written inside the worktree.

## What was not executed, and why

- **P07 native stage A/B:** native execution, TCB, refcount and leak probes are under authority hold. No native code was imported or run.
- **F6 S03/S03F/S03FO and F6M/F6P:** historical candidates were not re-staged or re-run. Their committed evidence is cited; current F6 is absent.
- **S04 temporal policy:** historical module was not re-staged. Its 17/17 technical result and S04R's missing runnable suite are cited from HQ285 L02.
- **Learned-world S06G:** not independently re-run; its local 187/14 result and S06FR's 12 defect findings are cited. Current HQ118 tests were run.
- **No raw survey, native P07, Field Forge, actor, model-use or source execution.**

## Consumer conclusions

| Lineage | Static import | Actual production consumer | Test-only receiver |
|---|---|---|---|
| F6 | none | UNKNOWN | F6P branch-only (not current) |
| P07 native stage B | none | UNKNOWN | none for native |
| F7 source relations | string path map only | UNKNOWN | `test_pre553_source_relations.py` |
| F7 temporal comparability | none for historical module | UNKNOWN | none current |
| F8 service source scope | EE14 ingress import/call | UNKNOWN (EE14 has no production caller; T1 HOLD) | five F8/EE14 courts |
| Learned world product | composition imports lifecycle/release | UNKNOWN (composition has no production caller) | lifecycle/release/composition tests |

Exact blob identity and static imports do not prove a live consumer or behavioral equivalence.
