# CAN-003 — V557 Runtime Publication / Use-Governance Authority

## 0. Authority identity

- **Authority ID:** `CAN-003`
- **Canonical contract ID:** `CAN_003_V557_RUNTIME_USE`
- **Canonical authority version:** `CAN-003.v1`
- **Owner:** `V557`
- **Classification:** `AUTHORITY_NEEDS_CANONICALIZATION` → canonicalized here; no new semantic authority created
- **Direct implementation consumers:** `V557-P1`, `V557-P2`, `V557-P4`, `V558-P1`
- **Downstream enforcement consumer:** V558 `StructuralPriorRepository` publication/linking boundary; query-relative permission may then be narrowed further by the V558→V3 `ContextResolver`
- **Explicitly separate authority:** temporal-proxy eligibility (`ADP-006` / RA-R00 `MUST-006`); this contract neither defines nor grants proxy eligibility
- **Production implementation:** none

`CAN-003.v1` binds the already-accepted V557 item-level runtime publication/use-governance meaning into a stable machine contract. It does not create a structural-domain semantic family, reinterpret any V553–V556 producer object, create a runtime condition, or authorize temporal proxying.

## 1. Binding source law

This canonicalization binds, without semantic deepening, the accepted law from:

1. TD-R04 V557/V558 terminal-demand result and accepted V557/V558 implementation ruling;
2. SI-R03 V556→V557 hostile seam hardening;
3. SI-R04 V557→V558 hostile seam hardening;
4. TD-R07 whole-machine architecture closure;
5. RA-R00 release synthesis classification of `CAN-003`;
6. current governance/manifest mechanics only as compatible implementation evidence.

The binding jurisdiction is:

```text
producer-owned semantic object + producer-owned meaning
+ producer permission / epistemic authority
        ↓
V557 publication admission + item-use governance
        ↓ never wider
V558 immutable producer-preserving repository
        ↓ never wider
ContextResolver query-relative permission
```

V557 owns no structural-domain semantic family. It can publish, narrow, deny, preserve, audit and prove closure. It cannot change what an upstream object means.

## 2. Canonical separation of fields

A runtime-authorized object record MUST keep these dimensions distinct.

### 2.1 Producer semantic identity

Producer-owned and immutable in V557:

- `producer_family`;
- `producer_collection_kind`;
- `producer_object_id`;
- `producer_object_hash`;
- `producer_build_id` / build hash where available;
- producer schema/compiler/rule/predicate/reference-contract versions required to interpret the object;
- exact producer semantic/negative/noncomparability/provenance references.

V557 may not re-ID or re-own the semantic object.

### 2.2 Producer permission input

Canonical field:

```text
producer_permission_input {
  authority_ref,
  authority_version,
  use_state,
  provenance_refs[]
}
```

`use_state` uses the same five-state vocabulary frozen below when the producer already serializes an equivalent permission. A compatibility adapter MAY map an older producer spelling to that vocabulary only when the mapping is one-to-one, provenance-recorded and non-widening. Ambiguous or absent permission is not guessed.

### 2.3 V557 publication admission

Canonical field:

```text
v557_publication_admission ∈ {
  ADMIT_RUNTIME_AUTHORIZED_RECORD,
  DO_NOT_ADMIT_RUNTIME_AUTHORIZED_RECORD
}
```

This is an **administrative publication decision**, not structural meaning and not causal permission.

An item with `DENY_CAUSAL_USE`, a producer negative/limit authority, a noncomparability state, or a valid-empty collection may still need a governance/manifest record preserved for V558 so that denial or absence cannot disappear. `ADMIT_RUNTIME_AUTHORIZED_RECORD` therefore never implies `ALLOW_ACTIVE_CAUSAL_CONTEXT`.

An item whose identity/hash/schema/reference integrity is not trustworthy MUST NOT be admitted as a runtime-authorized semantic object. Its integrity-failure audit record may still be preserved in the publication audit/manifest.

### 2.4 V557 item-use state

Canonical enum, copied exactly from accepted TD-R04 authority:

1. `ALLOW_ACTIVE_CAUSAL_CONTEXT`
2. `ALLOW_CONTEXT_ONLY`
3. `ALLOW_REVIEW_ONLY`
4. `DENY_CAUSAL_USE`
5. `NOT_APPLICABLE`

The state is item-level. A global build/readiness/status field cannot substitute for it and cannot override it.

### 2.5 Epistemic class

Canonical enum, copied exactly from accepted TD-R04 authority:

1. `SOURCE_EVIDENCE`
2. `DERIVED_STRUCTURAL_PRIOR`
3. `NEGATIVE_OR_LIMIT_AUTHORITY`
4. `RESOLVER_DERIVED_CONTEXT`
5. `GENERATED_RUNTIME_FACT`
6. `RENDERED_EXPRESSION`

The epistemic class says what kind of authority/material an item is. It is not a permission ranking. V557 may preserve the producer class but may not transform one class into another.

Within the accepted structural-prior publication path, producer-owned source/structural/negative objects are expected. `RESOLVER_DERIVED_CONTEXT`, `GENERATED_RUNTIME_FACT` and `RENDERED_EXPRESSION` remain distinct downstream classes and cannot be laundered into producer structural authority merely because the enum can represent them.

## 3. Use-state behavior

| V557 item-use state | Runtime causal structural use | Structural/context visibility | Review/audit visibility | Meaning |
|---|---:|---:|---:|---|
| `ALLOW_ACTIVE_CAUSAL_CONTEXT` | allowed, subject to all preserved producer conditions and later resolver narrowing | allowed | allowed | maximum V557 use permission already permitted by producer authority |
| `ALLOW_CONTEXT_ONLY` | forbidden as active causal structural prior | allowed as context/constraint/metadata according to producer meaning | allowed | context may survive without becoming actor-causal authority |
| `ALLOW_REVIEW_ONLY` | forbidden | forbidden from ordinary runtime context | allowed | audit/review only |
| `DENY_CAUSAL_USE` | forbidden | no positive causal/context promotion; denial/negative governance may still be preserved as authoritative restriction | allowed | explicit item-level denial; never overridden by global readiness |
| `NOT_APPLICABLE` | forbidden for the relevant governed use | not active for that governed use | allowed where needed for replay/audit | non-applicability is not missing authority and not integrity failure |

`ALLOW_ACTIVE_CAUSAL_CONTEXT` never bypasses producer predicates, actor-history requirements, native scope, negative authority, or ContextResolver query-relative selection. It means only that CAN-003 itself has not narrowed the producer below active-causal eligibility.

## 4. Monotone narrowing invariant

The binding invariant is:

```text
producer permission ≥ V557 publication/use permission ≥ resolver query-relative permission
```

For machine validation, the permission order is represented as the following allowed-use sets:

```text
ALLOW_ACTIVE_CAUSAL_CONTEXT = {REVIEW, CONTEXT, ACTIVE_CAUSAL}
ALLOW_CONTEXT_ONLY          = {REVIEW, CONTEXT}
ALLOW_REVIEW_ONLY           = {REVIEW}
DENY_CAUSAL_USE             = {}
NOT_APPLICABLE              = {}
```

`DENY_CAUSAL_USE` and `NOT_APPLICABLE` intentionally have the same empty allowed-use set but remain distinct states because denial and non-applicability are different accepted governance meanings.

For every item:

```text
allowed_uses(v557_use_state) ⊆ allowed_uses(producer_use_state)
```

and later:

```text
allowed_uses(resolver_query_relative_state) ⊆ allowed_uses(v557_use_state)
```

Any attempted widening is a governance integrity failure and fails closed. A compatibility alias cannot widen permission either.

This set representation is serialization/validation machinery for the already-accepted monotonicity law. It does not add a new structural semantic category.

## 5. Per-item precedence

Evaluation is per item. The following precedence is binding and cannot be superseded by stage/build readiness.

1. **Integrity first.** If required object identity, hash, schema/version, reference-contract, or indispensable transitive reference closure is corrupt/unverifiable, the semantic object is not runtime-admissible. Record `INTEGRITY_FAILURE`; do not turn the failure into a producer negative or missing-authority fact.
2. **Producer denial ceiling.** Explicit producer denial yields no V557 permission wider than `DENY_CAUSAL_USE`.
3. **V557 denial/narrowing.** A matching canonical V557 governance rule may preserve or narrow producer permission; never widen it.
4. **Producer epistemic/authority state remains producer meaning.** Negative/limit authority, missing authority, noncomparability and valid-empty status are preserved exactly and never translated into one another.
5. **Item state beats globals.** A global `READY`, readiness score, successful artifact write, healthy build, collection health flag or diagnostic status cannot override item denial, missing authority, noncomparability, negative/limit authority or integrity failure.
6. **Resolver only narrows further.** Query-time applicability/selection is downstream. CAN-003 does not pre-decide ContextResolver temporal selection, generated-position binding, or proxy eligibility.

Where the existing authority does not define a lawful widening from an exceptional state, CAN-003 does not invent one. The item remains at the producer ceiling or is narrowed/fails closed.

## 6. Authority / failure-state separation

Canonical governance-state enum:

- `NO_EXCEPTION_STATE`
- `NEGATIVE_AUTHORITY`
- `MISSING_AUTHORITY`
- `NONCOMPARABLE`
- `VALID_EMPTY`
- `INTEGRITY_FAILURE`

This enum is governance serialization. Exact producer subtype/reason/reference MUST also be retained; the enum may not erase producer distinctions.

### `NEGATIVE_AUTHORITY`

A producer-owned known negative/limit/absence/prohibition authority. It is **authority**, not missingness. Preserve the exact negative-authority object/ref and its producer meaning. It cannot be coerced to zero, neutral, positive evidence or missing authority.

### `MISSING_AUTHORITY`

The authority needed to make the proposed governed use is absent/unavailable. Missing authority is not a negative claim that the underlying world state is absent. It cannot be imputed from a neighboring object, global readiness or heuristic fallback.

### `NONCOMPARABLE`

The producer states that the relevant objects/bases cannot be lawfully compared under the governed operation. It is not contradiction, missingness, zero, negative authority or integrity failure.

### `VALID_EMPTY`

A governed collection/object family is lawfully empty under its producer rule or because no eligible authorized basis exists. Valid-empty is a successful semantic state, not a build failure and not evidence that the world contains no relation/topology beyond the governed authority.

Exact producer collection subtypes such as `VALID_EMPTY_NO_GOVERNED_RULE` and `VALID_EMPTY_NO_ELIGIBLE_AUTHORIZED_BASIS` remain preserved when supplied; CAN-003 does not merge them into one producer meaning.

### `INTEGRITY_FAILURE`

Schema/hash/reference/version/transport/build corruption or unverifiable indispensable closure. It is not a semantic fact about the represented domain and cannot be relabeled as structural blockage, negative authority, noncomparability or valid-empty.

## 7. Runtime-use governance rule identity

Every V557 permission decision MUST be replayable and versioned.

Canonical rule reference:

```text
v557_runtime_use_rule_ref {
  authority_id: "CAN-003",
  authority_version: "CAN-003.v1",
  rule_id,
  rule_version,
  decision_basis_refs[],
  decision_reason_code
}
```

This contract binds the schema and invariant. It does **not** invent domain-specific item eligibility predicates. A `rule_id` may only identify a rule already derived from accepted producer/V557 governance authority. If a future implementation needs a new semantic condition to decide use, that condition is outside CAN-003 and requires separate authority adjudication.

## 8. Canonical `RUNTIME_AUTHORIZED_OBJECT_RECORD` governance projection

The V557 runtime-authorized object record MUST expose at least:

```text
RUNTIME_AUTHORIZED_OBJECT_RECORD {
  governance_record_id,
  canonical_authority_id,
  canonical_authority_version,

  producer_family,
  producer_collection_kind,
  producer_object_id,
  producer_object_hash,
  producer_build_id,
  producer_schema_version,
  producer_compiler_version,
  producer_rule_refs[],
  producer_predicate_refs[],
  producer_reference_contract_versions[],

  epistemic_class,
  producer_permission_input,
  v557_publication_admission,
  v557_use_state,
  governance_exception_state,
  producer_exception_subtype,
  negative_or_limit_refs[],
  noncomparability_refs[],
  uncertainty_refs[],

  transitive_closure_audit_ref,
  provenance_refs[],
  v557_runtime_use_rule_ref,
  compatibility_aliases[],
  governance_record_hash
}
```

`governance_record_id` is a V557 governance/audit identity. It never replaces `producer_object_id` as the semantic object identity.

`transitive_closure_audit_ref` records compliance with SI-R03/SI-R04 handoff law. It is not an item-use category and does not create semantic permission.

## 9. Collection and handoff requirements

`RUNTIME_AUTHORIZED_COLLECTION_MANIFEST` MUST state, independently of global readiness:

- producer collection identity/build/schema/hash;
- exact object count;
- governed collection state (`VALID_NONEMPTY`, exact producer valid-empty subtype, denied/missing-authority/integrity state where applicable);
- count of items with complete CAN-003 governance records;
- count by V557 item-use state;
- count by epistemic class;
- count by governance exception state;
- referential-closure audit status/ref;
- CAN-003 authority ID/version and rule-registry version(s);
- manifest hash.

`V557_V558_RUNTIME_PUBLICATION_HANDOFF` MUST carry the immutable publication bundle identity, object/collection manifest hashes, CAN-003 authority/version, exact governance rule/registry versions, transitive-closure audit refs, and publication content hash.

Per-root transitive semantic closure is mandatory SI-R03/SI-R04 implementation/handoff law. It is **not** a new use state, epistemic class, or semantic condition in CAN-003.

## 10. Exact consumers and release effect

Direct consumers frozen by RA-R00:

- `V557-P1` — admission / collection-manifest implementation;
- `V557-P2` — item-governance implementation;
- `V557-P4` — immutable V557→V558 handoff implementation;
- `V558-P1` — immutable linker / repository ingress.

The V558 repository preserves the CAN-003 decision and producer authority. The V558→V3 ContextResolver then computes **query-relative** permission by further narrowing only.

CAN-003 does **not** release these consumers by itself. Their other authority and production gates remain independently binding.

## 11. Explicit separation from ADP-006 temporal-proxy eligibility

Temporal-proxy eligibility is outside this authority.

CAN-003 MUST NOT define:

- whether latest-prior proxy is allowed;
- whether earliest-post/future proxy is allowed;
- maximum lag;
- eligible query phase/purpose for proxying;
- temporal-anchor precedence;
- proxy tie-breaking;
- `DIRECT_TEMPORAL_SUPPORT`, `LATEST_PRIOR_OBSERVATION_PROXY`, `EARLIEST_POST_QUERY_PROXY`, or `EARLIEST_POST_BIRTH_ANCHOR` eligibility.

Those belong to the separately versioned ADP-006/MUST-006 authority and downstream resolver law.

A physical implementation may carry both authorities in one registry only if namespaces, schemas and versions remain logically distinct. CAN-003 may carry an opaque `temporal_proxy_authority_ref` for provenance/linkage but MUST NOT evaluate or synthesize it.

## 12. Compatibility law

Compatibility aliases are allowed only for mechanical migration from superseded terrain.

Each alias MUST include:

```text
compatibility_alias {
  legacy_field_or_value,
  canonical_field_or_value,
  mapping_kind: EXACT_ONE_TO_ONE,
  source_version,
  sunset_consumer,
  audit_ref
}
```

Forbidden compatibility behavior:

- treating a global readiness/status boolean as item permission;
- mapping a scalar readiness score to a use state;
- treating `ready_for_runtime_consumption=true` as permission for every item;
- mapping renderer/prompt status to structural causal authority;
- converting `missing` to `DENY` without preserving missing-authority state;
- converting noncomparability to negative authority;
- converting valid-empty to integrity failure;
- merging CAN-003 runtime-use governance with temporal-proxy eligibility;
- widening permission during alias normalization.

## 13. Hostile fixture court

A CAN-003 implementation is insufficient unless all hostile fixtures pass.

### H01 — global-ready cannot override item denial

Producer item is explicitly denied; stage/build is globally `READY`.

**Required:** V557 item remains `DENY_CAUSAL_USE`. Publication/readiness cannot widen it.

### H02 — context-only cannot become causal

Producer ceiling is `ALLOW_CONTEXT_ONLY`; V557 rule attempts `ALLOW_ACTIVE_CAUSAL_CONTEXT`.

**Required:** fail closed as forbidden widening; causal permission is not granted.

### H03 — review-only cannot become context

Producer ceiling is `ALLOW_REVIEW_ONLY`; adapter maps it to `ALLOW_CONTEXT_ONLY`.

**Required:** reject mapping as widening.

### H04 — denial survives publication

A denied item/negative restriction is required for V558 enforcement.

**Required:** governance/manifest record can be published while `v557_use_state` remains denied. Publication admission is not causal permission.

### H05 — negative authority is not missing

Producer supplies exact negative/limit authority ref.

**Required:** `governance_exception_state=NEGATIVE_AUTHORITY`; preserve ref; never recode as missing/zero/neutral.

### H06 — missing authority is not negative authority

Required use authority is absent.

**Required:** preserve `MISSING_AUTHORITY`; no invented denial fact or heuristic replacement; no causal widening.

### H07 — noncomparability is independent

Producer says two bases are noncomparable.

**Required:** preserve `NONCOMPARABLE`; do not turn it into contradiction, negative authority, zero or integrity failure.

### H08 — valid-empty is healthy

Producer collection is `VALID_EMPTY_NO_GOVERNED_RULE` or `VALID_EMPTY_NO_ELIGIBLE_AUTHORIZED_BASIS`.

**Required:** publication manifests preserve valid-empty as a successful semantic state; do not fabricate object rows and do not classify as failure.

### H09 — integrity failure is not semantic absence

Producer object hash/reference closure is corrupt.

**Required:** `INTEGRITY_FAILURE`; semantic object not admitted as runtime-authorized; audit record survives; no recoding as negative/missing/noncomparable.

### H10 — closure is not permission

An object has perfect transitive semantic closure but producer use state is denied.

**Required:** remains denied. Closure proof cannot grant permission.

### H11 — permission is not closure

An object has active-causal producer permission but an indispensable interpretation dependency is missing.

**Required:** integrity failure / no runtime admission. Permission cannot repair closure.

### H12 — resolver cannot widen

V557 state is `ALLOW_CONTEXT_ONLY`; query-relative resolver attempts active-causal use.

**Required:** reject/fail closed; resolver may narrow only.

### H13 — ADP-006 isolation

An item has active-causal CAN-003 permission but lacks temporal-proxy authority for the proposed proxy mode.

**Required:** CAN-003 remains unchanged; proxy use is not authorized. No proxy permission is inferred from runtime-use permission.

### H14 — legacy global flag laundering

Legacy packet has `ready_for_runtime_consumption=true` but no item permission record.

**Required:** no item causal permission is synthesized. Compatibility layer reports missing canonical item governance or fails closed.

### H15 — epistemic laundering

A `RENDERED_EXPRESSION` or `GENERATED_RUNTIME_FACT` is presented as if it were a producer `DERIVED_STRUCTURAL_PRIOR` without producer authority.

**Required:** reject/fail closed; V557 cannot change epistemic class to create structural authority.

### H16 — duplicate semantic re-ID

A V557 governance record invents a new semantic ID and drops the producer object ID.

**Required:** reject. Governance record identity is audit identity only; producer semantic ID/hash remain authoritative.

## 14. Canonicalization sufficiency

`CONSUMER_RELEASE_SUFFICIENCY = SUFFICIENT`

Reason: CAN-003 now supplies a stable authority/version, exact accepted use-state and epistemic enums, producer-permission input contract, separate publication admission, machine-checkable monotonicity invariant, per-item precedence, typed fail-closed governance states, exact V558-facing consumers, provenance/versioning, compatibility constraints and hostile fixtures. No unresolved semantic decision inside **runtime publication/use governance** remains for the named consumers.

This does not release V557/V558 implementation. Separate dependencies—including canonical producer publications, CAN-004/CAN-005 where applicable, ADP-006 temporal-proxy eligibility, and external production gates—remain outside this cell.

## 15. No-new-meaning attestation

This canonicalization introduced **no new structural-domain semantic family, condition, causal fact, proxy rule, resolver rule, structural predicate or actor-state meaning**.

New strings introduced here (`CAN-003.v1`, serialization field names, administrative publication-admission values, governance exception umbrella values, allowed-use validation atoms, fixture IDs) are schema/audit/validation machinery permitted by W0 canonicalization law. They bind already-accepted distinctions and do not alter producer meaning.

`CAN_003_V557_RUNTIME_USE_CANONICALIZATION = PASS`
