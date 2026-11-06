# PROGRAMMA PYAT — Universal35 D r15: qualified coordinate caller wiring + R14 binding defects

**STATUS:** `D_R15_COORDINATE_RULE_FACTORY_WIRED__C_HOOK_DEPENDENCY_EXPLICIT_UNACCEPTED__R14_LABEL_AND_UNHASHABLE_REFUSALS_REPAIRED__ACTUAL_SRC15_WAIT`
**BRANCH:** `codex/pyat-universal35-coordinate-caller-20261106-r1`
**D INPUT:** `a1d1ec379656d4e46841060004423931eed4b262` / code `ab7a6b606f15bd47c29d962da8c8c9db542710de`
**A DEPENDENCY:** production `bc84799edbeaefd7785e178a0aaacc94f76260fe`; tests `c84ea32de832f83656005f6e531cf837d1a58282`
**C HOOK DEPENDENCY:** candidate `8c5e8236ba08dca9d2e5921f938b3ce3d480e3bc`, unaccepted; G `e05ff071aa282c339e8237e308767ec57beed464` found prebuilt-release/foreign-source coordinate defects. Exact files received only for isolated caller wiring, not adopted.
**F R14 REVIEW:** `c5efdb9b75dd6174e70b3fd0247abbe2d2cb4ade` — REVISE label/binding and unhashable value.

## 1. FINDING | INTERPRETATION | ACTION | OWNER

| FINDING | INTERPRETATION | ACTION | OWNER |
|---|---|---|---|
| **R15-1. Exact A coordinate factory is now called at the actual materialization seam.** `execute_native_compiler_source` calls `source_configuration.factory.build_coordinate_slot_rules(config)`, selects exactly one rule for the chosen source coordinate, and passes the tuple into `materialize_native_preimages(..., coordinate_rules=...)`. Missing/multiple matching rules typed refuse; no permissive fallback in D. | The caller no longer drops A's source-qualified coordinate rules on the floor. Actual SRC15 join still waits for C's repaired hook and independent qualification. | Preserve formula; C repair independent. | D + A + C |
| **R15-2. C hook candidate is an explicit unaccepted dependency.** Exact C candidate `8c5e8236…` files were composed only in this isolated author branch to make the caller test executable. | No C acceptance or adoption is claimed. G's prebuilt-release/foreign-source defects remain; C author is repairing. | Exact SRC15 join `NOT_RUN`. | C + G |
| **R15-3. R14 label adversarial defect repaired.** Cold consumer now exposes `conditioner_label` / `target_label` as `OPAQUE_SOURCE_LABEL_NOT_ROLE_IDENTITY`; authoritative role identity is derived from decoded query target refs. | Changing old item-ID labels with recomputed request binding no longer changes authoritative role/result; selected result material records `role_identity_source=DECODED_QUERY_TARGET_REFS`. | Preserve label/ref distinction. | D + F |
| **R15-4. Unsupported canonical value now typed refuses, not TypeError.** Non-scalar/list/dict conditioner values return `REQUESTED_CONDITIONER_VALUE_UNSUPPORTED`; `None` returns `REQUESTED_CONDITIONER_VALUE_NONCANONICAL`. | No uncaught unhashable failure or zero-selection OK. | Preserve. | D + F |

## 2. TESTS / EVIDENCE

```text
PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q rawlsing_next/tests/test_pre553_original35_execution.py::test_factory_coordinate_rules_and_typed_omission \
  rawlsing_next/tests/test_pre553_original35_execution.py::test_existing_joint_engine_exact_requested_conditional_direction \
  -p no:cacheprovider --tb=short
2 passed in 4.63s
```

- Factory rules from exact SRC15 config are returned with exact slot/native/authority identity; empty/missing/wrong coordinate rules refuse.
- Existing asymmetric cold matrix retained: B|A 0=6/0, 1=2/4; A|B 8/4; changed cell/restore.
- Tampered refs, fake backing refs, empty/None/unknown/list values, missing permission/replay all refuse.
- Label tamper remains OK only as opaque label; authoritative role refs and result stay from decoded query.

## 3. LIMITS / DEPENDENCY

- Actual SRC15 full join is **NOT_RUN**: C hook candidate is unaccepted and has open G defects; no raw original read/fact claimed.
- Sourcefree caller proof is a prerequisite, not full35 or native/science completion.
- Original empirical facts remain zero; no protected/native/S3/science authority.
- No A production edits; A/C files were received exactly as dependency cuts only.

## 4. PROGRAMMA_DELTA

```text
PROGRAMMA_DELTA — Universal35 D r15 coordinate caller
- Identity: codex/pyat-universal35-coordinate-caller-20261106-r1@<returned-commit>; D input a1d1ec379; A bc84799ed; C candidate 8c5e8236b unaccepted.
- Function: exact bound config -> A build_coordinate_slot_rules -> matching typed rule -> actual materialize_native_preimages caller; plus R14 cold label/ref and unsupported-value repairs.
- Evidence: sourcefree factory/refusal tests; joint/cold matrix preserved; actual SRC15 NOT_RUN pending C repair/qualification.
- Limits: no original facts/native/science/protected acceptance; C defects remain.
```

## 5. BOUNDARY

Author evidence only; no C adoption, A production edit, protected merge, self-review, native/S3/science grant or source raw read. G/F focused review remains independent.
