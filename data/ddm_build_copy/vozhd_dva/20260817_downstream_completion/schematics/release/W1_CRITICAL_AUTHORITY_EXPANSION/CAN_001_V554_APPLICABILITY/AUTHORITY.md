# W1-06 — CDP-CAN-001 / V554 applicability predicate contract canonicalization

**Authority ID:** `V554_APPLICABILITY_PREDICATE_CONTRACT`  
**Authority version:** `1.0.0`  
**Canonicalization ID:** `CAN-001`  
**Worker packet:** `CDP-CAN-001`  
**Launch base:** `10a8e60f171e3a70bf48336fff73d37040cc1b93`  
**Branch:** `agent/vozhd-dva-w1-can-001-v554-applicability`  
**Verdict:** `PASS`  
**Production code modified:** `NO`  
**Historical ZIP used:** `NO — not authorized or needed`  
**New F2 semantic meaning introduced:** `NO`

## 1. Authority, dependencies, consumers, jurisdiction

CAN-001 canonicalizes only the stable machine representation of V554 F2 applicability/use conditions already created and closed by accepted `ADP-001 / V554_AFFORDANCE_RULE_REGISTRY@1.0.0` (`MUST-001`). The whole-machine architecture and W0 authority foundation remain closed.

**Exact accepted dependency consumed:** `ADP-001 / V554_AFFORDANCE_RULE_REGISTRY@1.0.0` only. `MUST-003` / V555 route-born predicate authority is explicitly not consumed. No sibling W1 result was used.

**Exact consumers of this machine contract:** V554 canonical F2 publication/implementation; ContextResolver runtime applicability evaluation; V3 genealogy only as producer of separately authorized generated-position bindings for K01; V555 only as a consumer/transporter of inherited V554 F2 identity; V558 as lossless transport/runtime boundary; V3 runtime replay/selection. None receives new semantic F2 meaning from CAN-001.

CAN-001 owns predicate IDs/versions, owner-resolution-producer-evaluator bindings, exact-ref argument serialization, legal evaluation/result/integrity states, replay/provenance requirements, and exact compatibility aliases. It does not own F2 semantic-kind existence or meaning, V555 route predicates, actor-position generation, actor history/satisfaction, interpolation/proxy policy, scalar readiness/strength/confidence, or production implementation.

The controlling relation is one-way:

`accepted ADP-001 F2 semantic kind -> CAN-001 machine predicate/evaluator contract`

There is no reverse promotion from legacy V554 seeds/readiness fields, prose, V555 route predicates, runtime observations, or actor facts.

## 2. Admissible inputs / epistemic classes

Canonical evaluation admits only exact, governed references already admissible under ADP-001 plus exact runtime bindings supplied by their separately authorized producer/evaluator:

- accepted ADP-001 F2 `condition_id` + `condition_kind_id` and its exact authority/rule/signature/target-use lineage;
- exact V552/V552J governed structural/use-authority refs carried by the F2 condition where applicable;
- exact V553 key/observation/relation/limit/negative refs where the accepted condition requires them;
- exact producer-owned denial, informational-constraint, noncomparability, gap/absence, missing-slot, unknown/conflict refs;
- exact native structural/geographic/position/stratum/scope refs;
- exact runtime generated-position binding refs for K01, and exact ContextResolver query/binding refs for K02/K03;
- exact manifest/schema/compiler/reference-contract versions and hashes required for replay.

Inadmissible as authority: legacy V554 seed/readiness/score fields; interpolated/imputed/backfilled/nearest-wave values; descriptive/fuzzy rematching; V555 route-born predicates; generated actor facts not supplied through their separately governed producer; actor history/biography/satisfaction; mutable `latest`; wall-clock or enumeration-order authority.

## 3. Closed predicate registry

ADP-001 closes tranche-one F2 at exactly nine kinds. CAN-001 binds exactly those nine and no others.

| ADP-001 kind | Canonical predicate@version | semantic_owner | resolution_owner | binding_producer | evaluator_owner / evaluator@version | effect |
|---|---|---|---|---|---|---|
| `V554-F2-K01-RUNTIME-POSITION-REQUIRED` | `V554-PRED-K01-RUNTIME-POSITION-REQUIRED@1.0.0` | `V554` | `V3_GENEALOGY` | `V3_GENEALOGY` | `CONTEXT_RESOLVER / V554-EVAL-K01-RUNTIME-POSITION@1.0.0` | `DEFER_UNTIL_RUNTIME_BINDING` |
| `V554-F2-K02-RUNTIME-TEMPORAL-RESOLUTION-REQUIRED` | `V554-PRED-K02-RUNTIME-TEMPORAL-RESOLUTION-REQUIRED@1.0.0` | `V554` | `CONTEXT_RESOLVER` | `CONTEXT_RESOLVER` | `CONTEXT_RESOLVER / V554-EVAL-K02-RUNTIME-TEMPORAL-RESOLUTION@1.0.0` | `DEFER_UNTIL_RUNTIME_BINDING` |
| `V554-F2-K03-RUNTIME-NATIVE-SCOPE-EVALUATION-REQUIRED` | `V554-PRED-K03-RUNTIME-NATIVE-SCOPE-EVALUATION-REQUIRED@1.0.0` | `V554` | `CONTEXT_RESOLVER` | `CONTEXT_RESOLVER` | `CONTEXT_RESOLVER / V554-EVAL-K03-RUNTIME-NATIVE-SCOPE@1.0.0` | `DEFER_UNTIL_RUNTIME_BINDING` |
| `V554-F2-K04-INHERITED-INFORMATIONAL-CONSTRAINT` | `V554-PRED-K04-INHERITED-INFORMATIONAL-CONSTRAINT@1.0.0` | `V554_TARGET_USE_EFFECT_ONLY__SOURCE_MEANING_PRODUCER_OWNED` | `NONE` | `NONE` | `NONE / NONE@NONE` | `INFORMATIONAL_CONSTRAINT` |
| `V554-F2-K05-INHERITED-EXPLICIT-USE-DENIAL` | `V554-PRED-K05-INHERITED-EXPLICIT-USE-DENIAL@1.0.0` | `V554_TARGET_USE_EFFECT_ONLY__SOURCE_DENIAL_PRODUCER_OWNED` | `NONE` | `NONE` | `NONE / NONE@NONE` | `HARD_USE_BLOCK` |
| `V554-F2-K06-REQUIRED-STATIC-AUTHORITY-MISSING` | `V554-PRED-K06-REQUIRED-STATIC-AUTHORITY-MISSING@1.0.0` | `V554` | `UPSTREAM_REPAIR` | `UPSTREAM_REPAIR` | `NONE / NONE@NONE` | `UNRESOLVED_AUTHORITY` |
| `V554-F2-K07-REQUIRED-STATIC-AUTHORITY-UNKNOWN-OR-CONFLICTING` | `V554-PRED-K07-REQUIRED-STATIC-AUTHORITY-UNKNOWN-OR-CONFLICTING@1.0.0` | `V554` | `UPSTREAM_REPAIR` | `UPSTREAM_REPAIR` | `NONE / NONE@NONE` | `UNRESOLVED_AUTHORITY` |
| `V554-F2-K08-REQUIRED-TEMPORAL-SUPPORT-NONCOMPARABLE` | `V554-PRED-K08-REQUIRED-TEMPORAL-SUPPORT-NONCOMPARABLE@1.0.0` | `V554_TARGET_USE_EFFECT_ONLY__SOURCE_NEGATIVE_PRODUCER_OWNED` | `NONE` | `NONE` | `NONE / NONE@NONE` | `HARD_USE_BLOCK` |
| `V554-F2-K09-REQUIRED-TEMPORAL-SUPPORT-ABSENT-OR-GAPPED` | `V554-PRED-K09-REQUIRED-TEMPORAL-SUPPORT-ABSENT-OR-GAPPED@1.0.0` | `V554_TARGET_USE_EFFECT_ONLY__SOURCE_NEGATIVE_PRODUCER_OWNED` | `NONE` | `NONE` | `NONE / NONE@NONE` | `HARD_USE_BLOCK` |

The ADP-001 `condition_kind_id` remains semantic identity; CAN-001's `predicate_id` is only its stable machine evaluation-contract identity. The kind/predicate/version/owner/evaluator tuple must match one registry row exactly.

K01 deliberately separates producer and evaluator: V3 genealogy produces a separately authorized generated-position binding; ContextResolver evaluates the immutable V554 predicate against it. V554 never asserts `ACTOR_HAS_POSITION`. K02/K03 grant ContextResolver no interpolation/proxy/scope-relabel authority; any such policy must come from separate authority.

## 4. Owner/evaluator namespaces

Accepted `semantic_owner` values:

- `V554`
- `V554_TARGET_USE_EFFECT_ONLY__SOURCE_MEANING_PRODUCER_OWNED`
- `V554_TARGET_USE_EFFECT_ONLY__SOURCE_DENIAL_PRODUCER_OWNED`
- `V554_TARGET_USE_EFFECT_ONLY__SOURCE_NEGATIVE_PRODUCER_OWNED`

Accepted `resolution_owner` / `binding_producer`: `V3_GENEALOGY`, `CONTEXT_RESOLVER`, `UPSTREAM_REPAIR`, `NONE`.

Accepted `evaluator_owner`: `CONTEXT_RESOLVER`, `NONE`.

K01-K03 require exact nonempty evaluator IDs and versions. K04-K09 require the explicit `NONE/NONE` evaluator sentinel; omission is not equivalent. `V555` is not a CAN-001 evaluator/resolution namespace: route-born predicate meaning remains `MUST-003`-separate.

## 5. Argument contract

**Schema:** `V554_F2_PREDICATE_ARGUMENT_ENVELOPE@1.0.0`.

Exact-ref groups:

- `required_binding_refs[]`
- `authority_basis_refs[]`
- `negative_authority_refs[]`
- `required_authority_slots[]`
- `conflict_or_unknown_refs[]`
- `affected_structural_refs[]`
- `v553_temporal_refs[]`
- `native_scope_refs[]`
- `runtime_binding_refs[]`

UTF-8 canonical JSON is used for hashing. Object keys are sorted. Ref arrays preserve governed producer order when order is semantic; otherwise they are exact-deduplicated and bytewise sorted. Optional absent groups serialize as empty arrays; missing required groups are integrity failure. Free-text/fuzzy matching and manufactured defaults are forbidden.

Per-kind minimum groups: K01 `required_binding_refs`; K02 `v553_temporal_refs`; K03 `native_scope_refs`; K04 `authority_basis_refs`; K05 `negative_authority_refs`; K06 `required_authority_slots`; K07 `conflict_or_unknown_refs`; K08/K09 `negative_authority_refs` + `v553_temporal_refs`.

## 6. Evaluation request/result contract

**Request schema:** `V554_F2_PREDICATE_EVALUATION_REQUEST@1.0.0`.

Required fields: `condition_id`, `condition_kind_id`, `predicate_id`, `predicate_version`, `semantic_owner`, `resolution_owner`, `binding_producer`, `evaluator_owner`, `evaluator_id`, `evaluator_version`, `argument_schema_id`, `arguments`, `authority_snapshot_refs`, `query_context_refs`.

**Result schema:** `V554_F2_PREDICATE_EVALUATION_RESULT@1.0.0`.

Canonical `result_state` values are exactly:

- `SATISFIED`
- `NOT_SATISFIED`
- `DEFERRED`
- `INFORMATIONAL_CONSTRAINT`
- `HARD_USE_BLOCK`
- `UNRESOLVED_AUTHORITY`
- `INTEGRITY_FAILURE`

State law:

- K01-K03 only: `SATISFIED | NOT_SATISFIED | DEFERRED` after exact runtime binding/evaluation;
- K04 only: `INFORMATIONAL_CONSTRAINT`;
- K05/K08/K09 only: `HARD_USE_BLOCK`;
- K06/K07 only: `UNRESOLVED_AUTHORITY`;
- every kind: presemantic `INTEGRITY_FAILURE` on machine-contract failure.

`DEFERRED` is not missing static authority. `NOT_SATISFIED` is a context-local runtime evaluation and is not producer-owned denial. Observed zero is not gap/absence. Integrity failure is not a semantic F2 negative. Runtime evaluation is not actor satisfaction history, biography, or mutation of F1/F2.

## 7. Fail-closed law

Integrity codes include `UNKNOWN_CONDITION_KIND`, `UNKNOWN_PREDICATE_ID`, `PREDICATE_KIND_MISMATCH`, `UNSUPPORTED_PREDICATE_VERSION`, unknown semantic/resolution/binding/evaluator owner, `UNKNOWN_EVALUATOR_ID`, `MISSING_EVALUATOR_VERSION`, `EVALUATOR_BINDING_MISMATCH`, `ARGUMENT_SCHEMA_INVALID`, `REQUIRED_ARGUMENT_GROUP_MISSING`, `PROVENANCE_INCOMPLETE`, `REPLAY_INPUT_UNAVAILABLE_OR_CHANGED`, `UNKNOWN_RESULT_STATE`, `RESULT_STATE_ILLEGAL_FOR_PREDICATE`, `V555_ROUTE_PREDICATE_MASQUERADE`, and `FORBIDDEN_LEGACY_AUTHORITY_INPUT`.

Any unknown/mismatched predicate, version, owner, evaluator, state, required argument or replay identity yields `INTEGRITY_FAILURE`: current use stops, no semantic F2 is fabricated, no closest match is selected, no missing version becomes `latest`, and no legacy score/interpolation/proxy/prose alias repairs the record. Integrity failure is never coerced to denial, unresolved authority, defer, or runtime non-satisfaction.

## 8. Version/provenance/replay law

Every evaluation/result preserves immutable condition/kind/predicate/version; semantic/resolution/binding/evaluator identities and versions; argument schema + canonical argument SHA-256; exact authority-snapshot/query-context/runtime-binding refs; result state; `V554_AFFORDANCE_RULE_REGISTRY@1.0.0`; `V554_APPLICABILITY_PREDICATE_CONTRACT@1.0.0`; inherited rule/signature/target-use refs; and producer manifest/schema/compiler/reference-contract versions/hashes.

`evaluation_record_id = "v554_f2_eval__" + sha256(canonical exact evaluation identity JSON)`.

Same exact identities/refs reproduce the same result. Changed upstream/predicate/evaluator/runtime-binding identity creates a new evaluation identity. Unavailable/changed exact replay input fails integrity rather than rematching descriptions, interpolating, choosing a proxy or consulting legacy scores. Processing time may be metadata but is excluded from semantic identity. Evaluation records remain immutable and never become actor history.

## 9. Compatibility aliases

One-way exact parse aliases only:

- `REQUIRES_RUNTIME_POSITION` -> K01 / `V554-PRED-K01-RUNTIME-POSITION-REQUIRED`;
- `REQUIRES_EXACT_WAVE_OR_PROXY` -> K02 / `V554-PRED-K02-RUNTIME-TEMPORAL-RESOLUTION-REQUIRED`; the spelling grants **zero** proxy-selection authority;
- `REQUIRE_BEFORE_USE` -> context-qualified effect alias for `DEFER_UNTIL_RUNTIME_BINDING`, valid only when K01-K03 identity is already known.

Canonical effect spellings remain canonical. Unknown aliases fail closed. No fuzzy/prose matching.

Not aliases and never authority inputs: `seed_strength_score`, `seed_confidence_score`, `seed_specificity_score`, `seed_certifiability_score`, `seed_readiness_status`, `seed_use_permission`, `interpolation_status`, `readiness_score`, `harmonization_score`, or V555 route-condition/predicate IDs.

## 10. Hostile fixtures

- **CAN001-HF-01 SAME_CONDITION_TWO_DIFFERENT_OWNERS:** wrong second owner/evaluator tuple -> `INTEGRITY_FAILURE`; no owner guessing.
- **CAN001-HF-02 MISSING_EVALUATOR_VERSION:** K01-K03 without exact evaluator version -> `INTEGRITY_FAILURE`; no latest-version default.
- **CAN001-HF-03 UNRESOLVED_GENERATED_POSITION:** K01 with exact requirement but no generated binding -> `DEFERRED`; no actor position/history invented.
- **CAN001-HF-04 TEMPORAL_NONCOMPARABILITY:** K08 exact negative ref -> `HARD_USE_BLOCK`; no interpolation, proxy, fallback or signature downgrade.
- **CAN001-HF-05 V555_ROUTE_PREDICATE_MASQUERADE:** V555 route-born predicate presented as inherited V554 F2 -> `INTEGRITY_FAILURE`; `MUST-003` remains separate.
- **CAN001-HF-06 RUNTIME_EVALUATION_OMITTED_FROM_ACTOR_HISTORY:** evaluation is complete without actor-history mutation; history/biographical satisfaction fields are schema-invalid.

**Hostile fixture verdict:** `PASS_BY_CONTRACT_INSPECTION`.

## 11. Present terrain

Current `ddm_v554_seed_contract.py` is legacy `V554_SCHEMA_VERSION="v0.1"` seed machinery containing bounded score/readiness/interpolation surfaces. They are implementation-terrain evidence only and are inadmissible as canonical semantic authority under accepted ADP-001. The Wave-0 vertical continuity fixture likewise supplies implementation-continuity/forbidden-persona evidence, not new F2 semantics. No production code or tests are modified.

## 12. Evidence inspected

All evidence was inspected at the exact launch base or while the branch was byte-identical to it. No historical ZIP and no sibling W1 result were used.

- `schematics/release/W1_CRITICAL_AUTHORITY_EXPANSION/LAUNCH_REGISTER.md`
- `state/CURRENT_STATE.md`
- `RAWLSING_GOVERNING_SPIRIT.md`
- `integration/WHOLE_MACHINE_ARCHITECTURE_CLOSURE_RULING.md`
- `integration/IMPLEMENTATION_RELEASE_SYNTHESIS_RULING.md`
- `integration/W0_AUTHORITY_FOUNDATION_CLOSURE_RULING.md`
- `integration/V554_COMPLETION_IMPLEMENTATION_RULING.md`
- `schematics/recalibration/TD_R01_V554/RESULT.md`
- `schematics/seam_integrity/SI_R00_V553_V554/RESULT.md`
- `schematics/seam_integrity/SI_R01_V554_V555/RESULT.md`
- `schematics/release/W0_AUTHORITY_FOUNDATION/ADP_001_V554_AFFORDANCE/AUTHORITY.md`
- `schematics/release/W0_AUTHORITY_FOUNDATION/ADP_001_V554_AFFORDANCE/AUTHORITY.json`
- `schematics/release/RA_R00_RULE_AUTHORITY_IMPLEMENTATION_RELEASE/RESULT.md`
- `schematics/release/RA_R00_RULE_AUTHORITY_IMPLEMENTATION_RELEASE/RESULT.json`
- `data/ddm_build_copy/ddm_v554_seed_contract.py`
- `data/ddm_build_copy/tests/vozhd_dva_wave0/vertical_continuity.py`

## 13. GOVERNING_SPIRIT_CHECK

`GOVERNING_SPIRIT_CHECK = NOT_APPLICABLE__HARD_AUTHORITY_UNIQUE`

`RAWLSING_GOVERNING_SPIRIT.md` was read and obeyed. Hard authority uniquely determines the semantic boundary and the necessary representational distinctions here; no lawful semantic ambiguity remained for it to decide. It created no condition kind, predicate meaning, owner, permission, evaluator behavior, coefficient or use-right.

## 14. CONSUMER_RELEASE_SUFFICIENCY

`CONSUMER_RELEASE_SUFFICIENCY = PASS_AFTER_VOZHD_ADJUDICATION`

The contract leaves no material machine boundary to prose inference: V554 has exact kind->predicate/version records; ContextResolver has K01-K03 evaluator/version/argument contracts without proxy authority; V3 genealogy has only K01 generated-binding production responsibility; V555 can preserve inherited F2 while route-born predicate meaning stays separate; V558 can transport identity/results/provenance losslessly; V3 runtime replay has exact versioned replay identity; unknown values fail integrity closed.

## 15. Scope confirmation

Exactly two authority files only. No implementation. No production-code change. No new F2 semantic condition kind. `ADP-001/MUST-001` remains semantic authority. `MUST-003` remains separate. Runtime evaluation is not actor history/satisfaction. V554 infers no generated actor position. No scalar readiness/strength/confidence. No interpolation or temporal proxy-selection authority. No sibling W1 result used.

**Tests:** `NOT_RUN__AUTHORITY_ONLY_NO_PRODUCTION_CODE`

`CAN_001_V554_APPLICABILITY_CANONICALIZATION = PASS`
