# PRE553 P06 — StructuralEmpiricalAdmission / V553 ingress exact preflight contract

Status: `PREFLIGHT_EXACT_BINDING__HQ_ACCEPTANCE_REQUIRED`

Assignment: `PRE553_P06_ADMISSION_V553`  
Branch: `agent/vozhd-trii-pre553-w06-admission-v553-preflight`  
Exact base: `e51730e461a15b0ad20f02f2efb4bccd751c2c81`

## 1. Holding

The lawful upstream structural seam is exactly:

`EmpiricalFact -> named STRUCTURAL_EMPIRICAL_ADMISSION_AUTHORITY -> StructuralEmpiricalAdmission -> V553`

There is no generic `EmpiricalFact -> structure` promotion. There is no `EmpiricalCoordinateFact -> generated nine-stratum position` promotion. There is no `DiscoveryResultReceipt -> structure` promotion merely because a relationship scored highly. There is no population fact -> actor belief/persona/psyche promotion.

`StructuralEmpiricalAdmission` is a durable governed decision receipt whose grain is **one exact EmpiricalFact/query result x one exact structural interpretation/use target x one exact structural-admission rule decision**.

Only `ADMITTED` is positive structural evidence at this seam.

## 2. Admission rule burden

Every positive rule must bind an exact ID/version/hash and state, without inference from labels:

- allowed EmpiricalFact/query family;
- service-specific source-universe applicability authority;
- required source-relation/composition authority for any multi-universe use;
- time/geography applicability;
- exact empirical predicate/target semantics relied upon;
- exact structural target identity refs;
- focal structural proposition ref;
- interpretation/transformation meaning;
- role/direction semantics;
- target-use permissions;
- support/uncertainty admissibility;
- source disagreement/noncomparability policy;
- negative authority / forbidden conclusions;
- required external authorities;
- effective period;
- downstream structural producer/use;
- replay semantics.

For compatibility migration from V551/V551J/V552/V552J, the rule must additionally bind the legacy semantic surface, parity claim scope, parity receipt and retained structural meaning. Packet shape or historical stage name is never authority.

## 3. Receipt envelope

Every receipt carries exact immutable refs/hashes for its EmpiricalQuerySpec, EmpiricalFact and admission rule, plus all material needed by downstream structural consumers:

- source universe refs;
- native scope identity refs;
- target use and permission refs;
- focal structural proposition ref;
- structural semantic identity refs;
- exact effective-time/interval evidence required by the target use;
- estimand refs;
- measure/weight authority refs;
- support/uncertainty state and refs;
- applicable negative/denial/noncomparability refs;
- interpretation-critical authority refs;
- authority closure refs;
- producer replay root.

An `ADMITTED` receipt additionally carries the exact bounded `structural_interpretation_payload` authorized by its named rule.

Discovery receipts and legacy compatibility receipts may be preserved as provenance, but neither substitutes for the exact underlying EmpiricalFact and named structural rule.

## 4. Typed state law

Positive:

- `ADMITTED`

Nonpositive, mutually preserved:

- `MISSING_STRUCTURAL_ADMISSION_AUTHORITY`
- `ADMISSION_DENIED`
- `ADMISSION_DEFERRED`
- `EMPIRICAL_FACT_NONCOMPARABLE`
- `SOURCE_NOT_APPLICABLE_TO_STRUCTURAL_USE`
- `INSUFFICIENT_EVIDENCE_UNDER_RULE`
- `TEMPORAL_SCOPE_MISMATCH`
- `STRUCTURAL_TARGET_UNRESOLVED`
- `NEGATIVE_AUTHORITY_ONLY`
- `UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY`
- `VALID_EMPTY`
- `INTEGRITY_FAILURE`

Fail-closed precedence is:

`INTEGRITY_FAILURE > MISSING_STRUCTURAL_ADMISSION_AUTHORITY > UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY > ADMISSION_DENIED > NEGATIVE_AUTHORITY_ONLY > SOURCE_NOT_APPLICABLE_TO_STRUCTURAL_USE > EMPIRICAL_FACT_NONCOMPARABLE > TEMPORAL_SCOPE_MISMATCH > STRUCTURAL_TARGET_UNRESOLVED > INSUFFICIENT_EVIDENCE_UNDER_RULE > ADMISSION_DEFERRED > VALID_EMPTY > ADMITTED`.

All simultaneously applicable blocking refs remain preserved even when one primary state wins precedence.

`OBSERVED_ZERO` is not missing and may be admitted if the exact rule permits that measured state. `ZERO_SUPPORT` is never actor or structural impossibility. `LOW_SUPPORT` may pass only under an explicit support/uncertainty clause and remains low-support. `UNCERTAINTY_UNQUANTIFIED` must remain unquantified. `VALID_EMPTY` is not converted into missing authority, denial or zero.

## 5. Identity and replay

Admission identity is content-derived:

`SEA:PRE553_V1:<sha256(canonical_semantic_identity_material)>`.

Semantic identity binds the exact empirical query/fact refs, exact structural-admission rule, decision state, target use, target permissions, focal structural proposition, structural semantic identities, admitted interpretation payload where positive, source universes and any required source-relation authorities, native scope, effective-time evidence, estimand, measure/weight authority, support/uncertainty state, negative/noncomparability refs and interpretation-critical authority closure.

Wall clock, filesystem order, session/run ID, cache state, latest/readiness/probe state, diagnostic ranking score and human-label similarity are excluded.

A later rule version creates a different admission identity. It never rewrites a historical receipt. Exact hash mismatch is `INTEGRITY_FAILURE`.

## 6. V553 jurisdiction is unchanged

V553's semantic input remains `STRUCTURAL_EMPIRICAL_ADMISSION`. Direct `EmpiricalFact`, `DiscoveryResultReceipt`, raw C11 incidence and diagnostic scores are forbidden inputs.

P06 supplies an exact immutable admission ref and the admission-owned structural/source/scope/authority/replay material needed to resolve it. P06 does **not** decide:

- `V553_REQUIRED` vs `V553_NOT_REQUIRED_FOR_THIS_USE`;
- required temporal operations;
- temporal-operation rule refs;
- canonical temporal keys;
- time harmonization;
- cross-time/cross-source comparability;
- temporal observation/relation/limit identity.

Those remain SCR553 and separately named compatibility-authority jurisdiction.

P06 may carry exact source/wave/time evidence and may reject an empirical fact that lies outside the *admission rule's own* effective time/geography. It may not convert that evidence into persistence, drift, reversal, sequence, canonical interval, baseline or other V553-owned temporal meaning.

A nonpositive admission may be referenced so its blocking state is replayable, but it can never become positive V553 output.

An earlier governed use that needed no new V553 meaning does not exempt any later governed use.

## 7. Direct M1 projection

For an `ADMITTED` receipt only, P06 defines a lossless direct-admission projection with the exact consumer slots already present in accepted M1:

- `structural_empirical_admission_id`
- `structural_empirical_admission_content_hash`
- `admission_authority_id`
- `admission_authority_version`
- `admission_authority_hash`
- `admission_decision_state`
- `focal_structural_proposition_ref`
- `structural_semantic_identity_refs`
- `native_scope_identity_refs`
- `target_use_permission_refs`
- `effective_time_or_interval_refs_required_by_target_use`
- `source_universe_refs`
- `estimand_refs`
- `measure_and_weight_authority_refs`
- `applicable_negative_denial_noncomparability_refs`
- `interpretation_critical_authority_refs`
- `producer_replay_locator_or_reference_root`

The projection is a deterministic view, not a new semantic object. Its projection hash is SHA-256 over canonical JSON.

P06 does not decide whether that projection is a lawful direct V554 basis for a particular governed use. The same-use SCR553 decision is independent. SCR554/M1 continues to own signature selection, temporal completeness, equivalence-key construction, duplicate precedence, canonical F1/F2/B1 identity and any direct V554->V557 publication authorization.

A nonpositive admission MUST NOT be emitted as a `DIRECT_STRUCTURAL_EMPIRICAL_ADMISSION` basis candidate. It remains typed negative/reference context only.

## 8. Source plurality

Distinct empirical universes remain distinct by default. Same labels, aliases, harmonized fields or provenance do not authorize equivalence, linkage, pooling, backfill or composition.

A multi-universe EmpiricalFact/admission requires exact externally owned applicability/relation/composition authority. If sources disagree, preserve separate admissions when the named structural rule permits plural evidence; otherwise return typed conflict/noncomparability. Never average by default.

## 9. Explicitly refused claims

This contract does not establish:

- an EmpiricalFact/query engine contract beyond the exact refs P06 consumes;
- source-universe equivalence/linkage/pooling/composition semantics;
- a generated actor position mapper;
- a general demographic-to-stratum map;
- a diagnostic-score-to-structure rule;
- V553 temporal rules;
- V554 dedup/equivalence rules;
- source retirement;
- cutover;
- any downstream interface change.

Accepted downstream head `e51730e461a15b0ad20f02f2efb4bccd751c2c81` remains unchanged.
