# V3_EMPIRICAL_POSSIBILITY_METABOLISM_AUTHORITY — SV3M CANDIDATE

**Status:** `NON_DISPOSITIVE_CANDIDATE_FOR_SCRV3`  
**Canonical proposed ID:** `V3_EMPIRICAL_POSSIBILITY_METABOLISM_AUTHORITY`  
**Proposed version:** `1.0.0`  
**Owner:** `V3_ACTOR_DEVELOPMENTAL_CAUSALITY_ENGINE`  
**Jurisdiction:** PSEPF read permission, use-class admission, operation ceilings, typed read result, causal/replay binding.  
**Not owned:** any actor-state domain semantics or population-to-person transform.

## 1. Canonical binding and hash shape

```text
V3_EMPIRICAL_POSSIBILITY_METABOLISM_AUTHORITY@1.0.0#sha256:<64-lowercase-hex>
```

Canonical `authority_core` fields, in sorted-key canonical JSON:

```text
authority_id
authority_version
owner
jurisdiction
dependency_authorities[]
read_permissions[]
operation_classes[]
typed_results[]
forbidden_operations[]
causal_replay_obligations[]
```

`authority_content_hash = sha256(UTF8(canonical_json(authority_core)))`.

Canonical JSON requirements:
- UTF-8;
- Unicode NFC;
- sorted object keys;
- arrays in explicitly governed semantic order;
- integers serialized canonically;
- no insignificant whitespace;
- no mutable locator, filename, branch name, wall clock, row order, database surrogate key, or `latest` alias in semantic identity.

The accepted SCRV3 artifact must bind the actual 64-hex digest. SV3M does not mint that accepted digest.

## 2. Permission theorem

A V3 transition may read empirical possibility iff all are true:

1. the exact `V3EmpiricalPossibilityInput` is current/admissible for the transition's actor, use class, decision context and effective time;
2. the metabolism authority ID/version/hash is present and exact;
3. the transition owner has an exact allowlist row for its authority ID/family + transition class + use class + operation class;
4. every referenced PSEPF/source component required by the operation resolves by immutable ID/hash;
5. upstream negative/source-comparison state permits the requested operation;
6. the owner has an independently lawful candidate/transition basis; PSEPF does not manufacture one;
7. if a numeric or ordering transform is used, that transform is separately owner-versioned/hash-bound and declared by the permission row;
8. the causal/replay receipt is emitted if the field was actually consulted.

Otherwise: `NO_PSEPF_TRANSITION_EFFECT`.

## 3. Allowed operation classes

### `EXACT_GEOMETRY_DEREFERENCE`
Read exact requested source-indexed unary/J-way geometry and typed states. No truncation, modal projection, marginal substitution, top-k replacement, source blending, or scalar output is implied.

### `OWNER_RULE_CONSTRAINT_TEST`
Evaluate an exact owner-declared predicate against exact field components. Output is only a typed constraint result.

### `OWNER_RULE_CANDIDATE_ANNOTATION`
Attach exact source/component support facts to already-lawful owner candidates for subsequent owner logic. Annotation is not actor state.

### `OWNER_RULE_CANDIDATE_FILTER`
Remove candidates that fail an exact owner-declared empirical constraint. The field may not add a candidate absent the owner’s independent candidate basis.

### `OWNER_RULE_CANDIDATE_WEIGHT`
Permitted only when the transition owner separately binds:
- transform ID/version/hash;
- exact source/component inputs;
- exact candidate-set identity;
- deterministic formula;
- support/uncertainty treatment;
- source conflict/noncomparability treatment;
- no direct actor-state interpretation.

The metabolism authority never supplies a default transform.

## 4. Proposed owner read permissions

Positive permissions are narrow and do not alter the owning authority's semantic jurisdiction.

- `ADP-010 / OPPORTUNITY_PROPOSAL_OR_ADMISSION`: exact geometry dereference, constraint, annotation, filter; candidate weight only with separately bound ADP-010 extension. Encounter/exposure occurrence reads are denied.
- `ADP-011 / ROUTE_REALIZATION_PROPOSAL`: exact geometry dereference, constraint, annotation, filter; candidate weight only with separately bound ADP-011 extension. Route existence/applicability cannot become lived traversal without V3 witnesses.
- `CAN-008 / RESPONSE_OR_METABOLIZATION_CANDIDATE_SELECTION`: exact geometry dereference, constraint, annotation; candidate filter/weight only with separately bound CAN-008 extension. Direct field mass/modal cell -> response is forbidden.
- `CAN-010 / NEED_EXPECTATION_STRIVING_CANDIDATE_SELECTION`: same constrained permission; no initial need/value/striving state may be created directly from the field.

Default deny:
- ADP-007 actor initialization;
- ADP-008 developmental phase;
- ADP-009 generated structural position;
- ADP-010 encounter/exposure occurrence subtransitions;
- ADP-015 relationship/household/genealogy creation;
- ADP-016 causal memory;
- ADP-017 knowledge/belief/claim accessibility;
- ADP-019 external-event admission;
- ADP-020 causal RNG;
- ADP-021 hybrid scheduler;
- CAN-009 material/organismic/vitality;
- CAN-011 developmental middle state;
- CAN-012 rupture/metabolization;
- CAN-014 derived publication;
- V2/application.

A later positive row for a denied family requires an exact SCRV3 or higher-authority amendment and an owner-specific semantic justification. Generic inheritance is forbidden.

## 5. Direct assignment ceiling

Regardless of read permission, the following are categorically forbidden:

```text
belief_probability = field.mass
response_probability = field.mass
actor_state = modal_configuration
identity/persona = argmax(field)
memory = survey_configuration
knowledge = supported_cell
relationship = source_majority
generated_structural_position = comparator_coordinate
```

Likewise forbidden:
- hidden nearest-cohort fallback;
- source-majority voting;
- source pooling without independent composition authority;
- modal/top-k/marginal replacement of requested J-way geometry;
- hidden scalarization;
- cross-source average;
- null-to-zero coercion;
- low-support-to-certainty;
- zero-support-to-impossibility;
- comparator receipt as prior;
- ReplayReceipt as prior.

## 6. Typed read-result contract

Every attempted read returns one of:

```text
READ_NOT_REQUESTED
READ_ADMITTED
READ_DENIED
METABOLISM_AUTHORITY_MISSING
OWNER_READ_PERMISSION_MISSING
USE_CLASS_MISMATCH
INPUT_STALE_OR_REBIND_REQUIRED
UPSTREAM_REQUERY_REQUIRED
SOURCE_COMPONENT_NONCOMPARABLE
SOURCE_CONFLICT_PRESERVED
LOW_SUPPORT_PRESERVED
ZERO_SUPPORT_PRESERVED
TARGET_UNAVAILABLE_PRESERVED
UPSTREAM_NEGATIVE_PRESERVED
OWNER_CONSTRAINT_NOT_SATISFIED
OWNER_CONSTRAINT_SATISFIED
NO_PSEPF_TRANSITION_EFFECT
```

The read result is not a replacement for upstream typed states. Upstream state is included by immutable reference and preserved exactly.

## 7. Causal/replay receipt

Any transition that actually consults empirical possibility must bind:

```text
metabolism_authority_id
metabolism_authority_version
metabolism_authority_content_hash
transition_owner_authority_id
transition_owner_authority_version
transition_owner_authority_content_hash
owner_transform_id/version/hash if any
actor_id
decision_context_id
use_class
effective_time
v3_empirical_possibility_input_id/hash
psepf_ids/hashes
source_component_ids
exact_cells_or_component_paths_read
upstream_typed_states_seen
pre_candidate_set_hash
post_constraint_candidate_set_hash
pre_actor_state_hash
causal_parent_refs
rng_receipt_refs
read_operation_class
read_result
committed_transition_id or NO_TRANSITION
post_actor_state_hash
receipt_content_hash
```

If the read did not participate in a committed transition, the receipt must still distinguish diagnostic/admission read from causal effect.

## 8. Determinism and divergence

Metabolism consultation does not itself introduce randomness. If owner logic needs stochastic choice, it uses ADP-020 only after the owner has established a lawful candidate set.

ADP-020's rule remains controlling:
- randomness selects only among already-lawful candidates;
- named stream and scope;
- exact candidate-set identity;
- exact receipt;
- no ambient/global RNG;
- deterministic operations consume no gratuitous draw.

Therefore identical upstream priors can lawfully yield divergent lives because post-branch encounter, relationship, exposure, action and owner-governed RNG histories can differ. Each exact history remains deterministically replayable from its own complete receipt set.
