# R10 — exact coordinate binding, no authority-name heuristic

**STATUS:** `COORDINATE_NAME_HEURISTIC_REMOVED__EXACT_EXPECTED_RULE_BINDING_IMPLEMENTED__TESTS_PASS`

**Code:** `10e228129ce744a0627a52bb446ffac6815fa08c` (prior `68980922…`).

## Change

`materialize_native_preimages` now has this caller contract for explicit coordinate rules:

```python
materialize_native_preimages(
    package=...,
    incidence=...,
    coordinate_rules=(exact_rule,),
    expected_coordinate_rule=exact_rule,  # independently derived by caller from accepted factory/config
)
```

The regex/token/source-ID substring heuristic is removed. When either side is supplied without the other, or the operational rule is not exactly equal to the expected rule (including native coordinate ref, unit taxonomy ref, effective time, authority/provenance, value rules), the call refuses. A foreign coordinate ref with correct slot/ordinal therefore cannot pass via a matching token in its name; a legitimate differently named exact rule passes because equality is on the accepted factory object, not on text.

D must pass `expected_coordinate_rule` from the accepted `build_coordinate_slot_rules(config)` result (A production `bc84799e…`, restored tests `c84ea32d…`). No A/D file was edited; the API change is the exact minimal caller requirement. UNKNOWN/MISSING/DEFER values remain typed; no age meaning is inferred.

## Evidence

- `results/g_repair_tests.log`: 28 scale/facade/universal tests PASS after the exact-binding rewrite.
- Adverse tests: missing expected binding REFUSED; foreign rule vs expected rule REFUSED with `COORDINATE_RULE_EXPECTED_BINDING_MISMATCH`; tampered prebuilt release semantic hash remains REFUSED; valid explicit UNKNOWN rule and exact release reuse PASS.
- Full-scale negatives unchanged: SRC10 first materialize 169.3 s, compile >425.9 s at ceiling, 0 facts; SRC09 materialize >347 s. No 600 s rerun and no full-scale/native/all35 claim.

## Limits

Release reuse verification remains the existing binding/replay/authority/closure check from `68980922`; no full candidate validator rerun was claimed. Actual SRC15 join and D glue are NOT_RUN until D passes the exact expected rule. No protected merge/self-review.
