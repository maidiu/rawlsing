# HQ280 WVF — reusable (non-authorizing) data-only source-authority binding pattern, and exact holds

This pattern is **data-only and non-authorizing**. It binds WGC/WGD operation *candidate* keys to a competent current source-specific original-work issuer and to already-existing C11/I05/T3 owner outputs. It **does not** hardcode universal Q291 semantics, **does not** issue eligibility for other waves/sources, and **does not** create a scheduler.

## 1. The pattern (six slots, each explicitly resolved or typed-unknown)

```json
{
  "pattern": "HQ280_SOURCE_OPERATION_BINDING_CANDIDATE@1",
  "candidate_operation_key": "<WGC/WGD operation-candidate key — input, never authority>",
  "original_item": {
    "source_family":      "<WVS|Afrobarometer|GSS|...>",
    "wave":               "<exact>",
    "instrument_item_id": "<SOURCE-NATIVE item identity>            [REQUIRED, issuer: original-instrument owner]",
    "wording_ref":        "<exact questionnaire wording ref>         [REQUIRED]",
    "native_codes_ref":   "<exact code list incl. DK/refusal/missing>[REQUIRED]",
    "routing_ref":        "<asked/eligible exposure rule>            [REQUIRED]",
    "respondent_unit":    "<person|household|dyad|occurrence>        [REQUIRED]",
    "weight_design_role": "<weight|none|design-limited>              [REQUIRED, default none]"
  },
  "source_authority": {
    "grant_ref":          "<exact source-use/permission ref>         [REQUIRED, issuer: competent source owner]",
    "measure_ceiling":    "<RAW|...>",
    "target_use_ref":     "<exact target-use ref>"
  },
  "operation": {
    "roles":              ["CONDITIONER","TARGET"] | ["BASE"],
    "grammar_ref":        "<finite permitted-operation grammar>      [REQUIRED]",
    "validation_kind":    "<TARGET_CELL_SUPPORTED|DISTRIBUTION_DIFFERS_FROM_BASELINE|JOINT_NOT_PRODUCT_OF_MARGINALS|...>",
    "resolved_by_owner":  "<existing C11/I05/T3 owner>               [REQUIRED]"
  },
  "owner_outputs": {
    "c11_release_ref":    "<existing release identity or null>",
    "i05_frontier_ref":   "<existing evaluated frontier identity or null>",
    "oracle_ref":         "<existing oracle identity or null>",
    "t3_consumed_ref":    "<existing T3 consumed identity or null>"
  },
  "status": "BOUND | UNRESOLVED | COVERAGE_LIMITED | HELD",
  "unresolved_field": "<exact field name> @ <responsible_owner>"
}
```

### Rules

1. **`candidate_operation_key` is an input, never authority.** A candidate key that appears in WGC/WGD is not evidence of eligibility.
2. **Every `[REQUIRED]` field is either exactly bound or the record is `UNRESOLVED` with the field named and the responsible owner named.** No field is defaulted from a variable name.
3. **Chronology is explicit.** An expected set may be pre-execution; a truth payload assembled after execution is labelled `POST_EXECUTION_EVALUATION` and may never be presented as a pre-registered oracle. (This is the exact defect the WVS7 chain exhibits — see `03`/`04`.)
4. **Typed negatives are preserved**, never collapsed: physical vs semantic missing; `VALID_EMPTY`; `NOT_ASKED` vs `NOT_ELIGIBLE` vs `INAPPLICABLE`; `UNAVAILABLE` vs `COVERAGE_LIMITED`; governance-blocked is not empirical data.
5. **No-drop is measured at a declared grain** (`expected_n`, `covered_n`, `additions`, `drops`, order equality, replay equality) and explicitly not extended beyond it.
6. **One record = one operation.** No pattern-level default and no whole-scheduler behaviour: the pattern produces a per-operation binding record only.

## 2. Concrete instantiation for the WVS7 Q291 chain (worked example)

| slot | value | status |
|---|---|---|
| `candidate_operation_key` | the 46 ordered candidate hashes (`03_46_CANDIDATE_REPLAY_CONSERVATION.json`) | BOUND |
| `source_family` / `wave` | WVS7 / (wave not bound in receipts) | PARTIAL |
| `instrument_item_id` | — | **UNRESOLVED** |
| `wording_ref` / `native_codes_ref` / `routing_ref` | — | **UNRESOLVED** |
| `respondent_unit` | — | **UNRESOLVED** |
| `weight_design_role` | none claimed | BOUND (as *no claim*) |
| `source_authority.grant_ref` | semantic authority closure `b9be2091…` (+ 6 `AuthoritySnapshot` refs) | PARTIAL |
| `operation.grammar_ref` | `a94bd2ed…` | BOUND |
| `operation.validation_kind` | 3 kinds across 46 | BOUND |
| `owner_outputs.c11_release_ref` | `e6881e9a…` | BOUND |
| `owner_outputs.i05_frontier_ref` | `b2c3c50b…` | BOUND |
| `owner_outputs.oracle_ref` | R1M `3694b8bd…`, T3 `e546c155…` | BOUND |
| `status` | `COVERAGE_LIMITED` ×46 with `unresolved_field = original_item.*` | — |

## 3. Exact holds (each with its responsible owner)

| id | hold | field | responsible owner | smallest packet needed |
|---|---|---|---|---|
| H1 | `HOLD__ORIGINAL_INSTRUMENT_ITEM_FIELD_UNBOUND` | `original_item.instrument_item_id / wording_ref / native_codes_ref / routing_ref` | WVS original-instrument / source-semantics owner | WVS7 Q291 questionnaire or codebook entry + native code list + asked/routing rule |
| H2 | `HOLD__RESPONDENT_UNIT_AND_WEIGHT_DESIGN_UNBOUND` | `original_item.respondent_unit`, `weight_design_role` | WVS sampling/design owner | source-native respondent-unit statement + weight/design designation for this wave |
| H3 | `HOLD__SOURCE_USE_GRANT_NOT_ISSUED_FOR_PROMOTION` | `source_authority.grant_ref` for *promoting* an evaluated fact to an eligible operation | competent source-use issuer (not this worker, not HQ-by-implication) | explicit per-operation source-use grant at declared scope |
| H4 | `HOLD__PRE_I05_TRUTH_ORACLE_NOT_ESTABLISHED` | chronology label on the 46 truth outcomes | chain author + HQ | a pre-I05 sealed truth oracle, or accept the honest `POST_EXECUTION_EVALUATION` label |
| H5 | `HOLD__T3_GRAIN_SCOPE_CONFIRMATION` | whether the T3 46 `COVERAGE_LIMITED` are the same 46 as R1M's | T3 acceptance owner | per-record identity join (currently established only at digest level) |

## 4. What this pattern must NOT be used for

- Not to grant eligibility to other WVS waves, other sources, or the 78,037 WGC annotations.
- Not to convert `COVERAGE_LIMITED` into supported.
- Not to select an ABC candidate or a world release.
- Not to authorize raw source execution or a new I05 run.
- Not to stand in for the missing original-instrument authority (H1/H2).
