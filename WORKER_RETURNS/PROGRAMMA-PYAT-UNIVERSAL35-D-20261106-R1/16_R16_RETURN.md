# PROGRAMMA PYAT — Universal35 D r16: expected-rule caller contract and exact F corrections

**STATUS:** `D_R16_EXPECTED_RULE_FORWARDED_WITH_OPERATIONAL_RULES__A_RESTORED_TESTS_RECEIVED__C_CANDIDATE_UNACCEPTED__SRC15_STILL_PENDING`
**BRANCH:** `codex/pyat-universal35-coordinate-caller-20261106-r1`
**D INPUT:** `4b1d2ec8bec0166fcec7857a3a11fb3642b46109` / code `223e8bbc9624431ef8bae52e0767ae92357340d3`
**A:** production `bc84799edbeaefd7785e178a0aaacc94f76260fe`; restored test file `c84ea32de832f83656005f6e531cf837d1a58282` received exactly.
**C CANDIDATE:** `511856ac5daa0c6b38b449f3bc7b2a6734403638` / code `10e228129ce744a0627a52bb446ffac6815fa08c`; composed exact facade/native-adapter/test deps only; **UNACCEPTED**, pending independent C review.
**F R14 CLOSURE:** `ca679db10a569adfb02410474b60478aba1d13f6` — cold label/role/value matrix PASS; requested caller/source-mismatch proof remains.

## 1. FINDING | INTERPRETATION | ACTION | OWNER

| FINDING | INTERPRETATION | ACTION | OWNER |
|---|---|---|---|
| **R16-1. Caller passes both exact coordinate objects.** `qualified_coordinate_rules` derives `(rules, expected)` from A's source-SHA/config-bound factory. The real call is `materialize_native_preimages(..., coordinate_rules=rules, expected_coordinate_rule=expected)`. | Expected is never derived from the operational rule or names/tokens; it is the factory object itself. Existing incidence SHA/config binding remains. | Preserve both-object forwarding. | D + A + C |
| **R16-2. Operational-rule substitution is refused at the adapter seam.** A foreign rule with the same name/ordinal but changed native ref/content hash is compared against the independently derived expected object and refuses `COORDINATE_RULE_EXPECTED_BINDING_MISMATCH`. | No silent right-name/right-ordinal substitution. | C/A independent review. | C + G |
| **R16-3. Restored A test file is now present.** Exact `rawlsing_next/tests/test_source_configuration_corrections.py` from `c84ea32d…` received unchanged; its complete 13-test set passes with the two D caller/cold tests. | Prior “cited test absent” correction is closed without A production edit. | Preserve exact file. | A + D |
| **R16-4. R14 cold-label and unhashable defects remain repaired.** Opaque labels are not role identity; authoritative roles derive from decoded query refs. List/dict/unsupported values typed refuse; no TypeError/zero-selection OK. | F cold PASS retained. | Preserve. | D + F |
| **R16-5. Actual SRC15 full join remains pending.** C candidate is unaccepted and its source-rule/release authority does not yet pass independent qualification; synthetic valid-rule materialization still hits exact historical authority failure. | Do not force original join through failing authority or claim sourcefree synthetic as original. | Wait for C qualified hook/release; no 650s rerun. | C + G + D |

## 2. TESTS

```text
PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q rawlsing_next/tests/test_source_configuration_corrections.py \
  rawlsing_next/tests/test_pre553_original35_execution.py::test_factory_coordinate_rules_and_expected_binding_reach_adapter \
  rawlsing_next/tests/test_pre553_original35_execution.py::test_existing_joint_engine_exact_requested_conditional_direction \
  -p no:cacheprovider --tb=short
15 passed in 31.38s
```

Observed:
- exact SRC15 factory rule object identity returned;
- foreign operational rule → `COORDINATE_RULE_EXPECTED_BINDING_MISMATCH`;
- empty/missing/wrong coordinate rule typed refuse;
- cold asymmetric 6/0, 2/4, reverse 8/4, changed/restore and label/ref/value refusals preserved.

## 3. LIMITS / DEPENDENCIES

- C `10e228129ce744a0627a52bb446ffac6815fa08c` is unaccepted and only composed for this author-branch caller wiring; no adoption/PR promotion.
- Actual SRC15 original join and original empirical facts remain `NOT_RUN`; no native/S3/science/protected acceptance.
- Sourcefree caller proof is a prerequisite, not full35 completion.
- No A production edit, C semantic edit, guide/controller change, raw source read or 650s rerun.

## 4. PROGRAMMA_DELTA

```text
PROGRAMMA_DELTA — Universal35 D r16 expected-rule caller
- Identity: codex/pyat-universal35-coordinate-caller-20261106-r1@0f3a22f3d40d9cf2543c3300a8e6163142e64cf8; D input 4b1d2ec8b; A bc84799ed + test c84ea32d; C candidate 10e228129 unaccepted.
- Function: exact config factory -> (rules, expected) -> both forwarded to current materialize_native_preimages; foreign operational rule refused; cold label/ref/value repairs retained.
- Evidence: 13 A tests + 2 D caller/cold tests = 15 passed.
- Limits: actual SRC15 NOT_RUN until C qualified; original facts/native/science/protected authority unchanged.
```

## 5. BOUNDARY

Author evidence only; no C/A adoption, protected merge, self-review, native/S3/science grant or source raw read. C independent review remains external.
