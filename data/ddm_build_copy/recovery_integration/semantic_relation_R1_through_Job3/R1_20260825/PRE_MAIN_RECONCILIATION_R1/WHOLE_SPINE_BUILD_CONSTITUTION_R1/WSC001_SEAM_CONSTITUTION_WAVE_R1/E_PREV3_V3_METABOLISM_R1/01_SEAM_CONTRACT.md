# WSC001E — PRE-V3 → V3 COMPARATOR / PSEPF / METABOLISM SEAM CONTRACT R1

## 1. Contract purpose

This contract defines the smallest lawful interface by which PRE-V3 learned-world empirical/structural possibility may be presented to V3 without collapsing population evidence into actor truth.

It is an interface constitution for central fan-in. It does not itself close `OBL031` or `OBL032`, accept a new transition authority, or implement V3 developmental semantics.

Contract identity:

`PREV3_V3_COMPARATOR_PSEPF_METABOLISM_SEAM@WSC001E.R1`

## 2. Semantic producers and owners

### 2.1 V3 generated-subject owner

V3 owns:

- generated-subject identity;
- generated-subject facts;
- generated position/relationship/history facts when such facts already exist under V3 authority;
- any later actor-facing causal transition.

PRE-V3 may reference exact V3-owned facts as query criteria. It may not create or revise them.

### 2.2 PRE-V3 empirical possibility owner

The PRE-V3 learned-world service owns:

- exact source universe and release identity;
- empirical coordinate/predicate identity;
- exact positioned-subject empirical possibility query;
- exact/proxy evidence distinction;
- uncertainty/support state;
- source-backed replay determinants;
- typed `VALID_EMPTY`, `NONCOMPARABLE`, `UNRESOLVED`, `FAIL_CLOSED` states.

A `PositionedSubjectEmpiricalPossibilityField` remains empirical possibility only.

### 2.3 Comparator authority owner

A competent empirical/structural authority must own the exact bridge from each V3-owned generated-subject fact to the corresponding empirical predicate/coordinate role used by the PSEPF query.

The comparator does not own the V3 fact. It certifies that an already-owned actor fact may lawfully serve as a criterion for the exact empirical predicate at the declared source/release/time/use grain.

### 2.4 V3 transition owner

A separately accepted V3 owner rule owns any positive semantic transition from learned-world possibility/context into V3 causal state.

The seam guard owns only admission/delegation. It never owns actor mutation.

## 3. Consumer

Primary consumer:

`V3_DEVELOPMENTAL_TRANSITION_OWNER`

The consumer receives either:

- a pure delegation decision naming an exact separately accepted owner rule; or
- a typed zero-effect negative/blocked/empty/noncomparable decision.

No consumer may reinterpret a negative decision as probability zero, default opportunity, default knowledge, default action or default nonoccurrence unless an independent owner explicitly defines that meaning.

## 4. Minimum input identities

A request is invalid unless it carries exact immutable identities for all material fields.

### 4.1 Generated-subject binding

Required:

- `generated_subject_ref` — exact V3-owned subject identity;
- `generated_subject_fact_refs[]` — exact V3-owned facts used as comparator/query criteria;
- `generated_subject_fact_owner_refs[]` — authority/currentness proof sufficient to establish that PRE-V3 did not invent those facts;
- `effective_time_or_interval` for every fact when time is meaning-bearing.

### 4.2 Predicate-ancestry binding

For every generated-subject fact consumed as a conditioner, require:

- `subject_fact_ref`;
- `empirical_coordinate_ref`;
- `empirical_predicate_ref` or exact predicate operand identity;
- `predicate_ancestry_ref` binding actor-fact semantic role to empirical predicate role;
- `comparability_authority_ref`;
- `source_universe_ref`;
- `release_ref`;
- `effective_time_or_interval`;
- exact target-use permission.

Forbidden comparator construction:

- lexical-name equality;
- ontology resemblance;
- nearest/fuzzy cohort selection;
- ungoverned harmonization;
- implicit cross-release or cross-source equivalence;
- a diagnostic association score used as identity proof.

### 4.3 Positioned-subject empirical possibility input

Required:

- `psepf_result_ref`;
- `psepf_result_hash`;
- `psepf_result_state`;
- `exact_disposition`;
- `source_universe_ref`;
- `release_ref`;
- `target_ref`;
- exact query ref;
- exact conditioner set;
- model-rule authority ref/hash;
- replay determinants;
- replay identity;
- explicit proxy lane and specificity-loss material if a proxy exists.

Only the exact lane can participate in a future positive delegation decision.

`EXACT_UNRESOLVED_PROXY_AVAILABLE` is not positive actor-transition evidence.

### 4.4 Optional structural context

If a concrete V3 owner rule declares structural context required, the request may also include:

- exact `ResolvedStructuralContext` ref/hash;
- exact V558 resolution/repository binding;
- structural currentness receipt;
- structural peer-use receipt;
- required-use declaration.

This material may satisfy structural-context eligibility only. It never supplies mutation authority.

### 4.5 Positive transition authority presentation

A positive delegation request must carry:

- `authority_id`;
- `authority_version`;
- `authority_content_hash`;
- `acceptance_ref`;
- `acceptance_hash`;
- `owner_rule_id`;
- `owner_rule_version`;
- `owner_rule_content_hash`;
- `transition_surface_id`;
- `operation_class`;
- allowed guarded source classes/lineage;
- exact registry binding proving the authority is separately accepted and current at this operation grain.

A caller-supplied claim of authority is insufficient.

## 5. Minimum comparator receipt identity

The seam requires, but does not presently claim to have production authority for, an exact comparator receipt with the following minimum semantics:

`ActorComparatorReceipt@WSC001E.R1`

Minimum fields:

- `receipt_id`;
- `receipt_hash`;
- `generated_subject_ref`;
- ordered/set-normalized `subject_fact_refs` as declared by the predicate contract;
- `predicate_ancestry_bindings[]`;
- `source_universe_ref`;
- `release_ref`;
- `target_ref`;
- `effective_time_or_interval`;
- `comparability_authority_refs[]`;
- `measurement_portability_authority_refs[]` when required;
- `transport_authority_refs[]` when required;
- `result_state`;
- `replay_determinants[]`;
- `authority_snapshot_refs[]`.

Comparator result states:

- `EXACT_COMPARATOR_MATCH`;
- `EXACT_COMPARATOR_NONMATCH`;
- `VALID_EMPTY`;
- `NONCOMPARABLE`;
- `BLOCKED_MISSING_PREDICATE_ANCESTRY`;
- `BLOCKED_MISSING_COMPARABILITY_AUTHORITY`;
- `BLOCKED_MISSING_MEASUREMENT_PORTABILITY`;
- `BLOCKED_MISSING_TRANSPORT_AUTHORITY`;
- `INTEGRITY_FAILURE`.

`EXACT_COMPARATOR_MATCH` means only that existing V3-owned facts lawfully instantiate the declared empirical criteria. It is not evidence that the actor believes, wants, chooses or will realize the target.

`EXACT_COMPARATOR_NONMATCH` is a typed comparator result, not a claim that the actor lacks some broader identity or trait.

## 6. Minimum output identity

Every seam evaluation returns exactly one immutable decision:

`PREV3_V3_METABOLISM_DECISION@WSC001E.R1`

Minimum fields:

- `decision_id`;
- `decision_hash`;
- `generated_subject_ref`;
- `comparator_receipt_ref_or_blocker`;
- `psepf_result_ref`;
- optional structural-context refs;
- `decision_state`;
- `reason_code`;
- `transition_surface_id`;
- `operation_class`;
- `delegated_owner_rule_ref_or_none`;
- `actor_state_effect_at_seam = ZERO`;
- `causal_ledger_appends_at_seam = 0`;
- `rng_mutations_at_seam = 0`;
- `scheduler_mutations_at_seam = 0`;
- pre-seam state fingerprint;
- post-seam state fingerprint;
- replay determinants;
- authority/currentness snapshots;
- information-loss declaration.

The pre/post state fingerprints must be identical at this seam.

## 7. Decision state machine

Decision precedence is fail-closed.

### 7.1 `INTEGRITY_FAILURE_ZERO_EFFECT`

Use when identity, hash, replay, authority binding or required reference closure is invalid.

Permission: none.

### 7.2 `NONCOMPARABLE_ZERO_EFFECT`

Use when exact comparator/PSEPF evidence is noncomparable at the declared use grain.

Permission: preserve noncomparability; no proxy rescue into actor transition.

### 7.3 `VALID_EMPTY_ZERO_EFFECT`

Use when the exact positioned stratum/query frontier is valid-empty.

Permission: preserve valid emptiness; no walkback to fabricate positive actor evidence.

### 7.4 `BLOCKED_COMPARATOR_ANCESTRY_ZERO_EFFECT`

Use when exact predicate ancestry or exact comparator authority is missing.

Permission: none.

This is the current `OBL031` gate.

### 7.5 `BLOCKED_MEASUREMENT_OR_TRANSPORT_ZERO_EFFECT`

Use only when the concrete transition/comparator actually crosses a measurement or transport boundary and the independently governed premise is missing.

Measurement portability is not inferred from source equivalence or shared labels.

### 7.6 `UNRESOLVED_OR_PROXY_ZERO_EFFECT`

Use for:

- exact stratum absent;
- exact stratum underpowered/unresolved;
- explicit lower-specificity proxy available;
- source/release mismatch;
- model/source universe outside scope.

A proxy may remain useful to learned-world analysis but cannot support positive actor transition.

### 7.7 `ZERO_EMPIRICAL_OR_COMPARATOR_EFFECT`

Use when an exact upstream typed zero/nonmatch is lawfully bound to the exact comparator grain.

This state must preserve the specific zero kind, such as `OBSERVED_ZERO`, `ZERO_SUPPORT`, `ZERO_OVERLAP` or `EXACT_COMPARATOR_NONMATCH`; these are not interchangeable.

Actor effect remains zero. An empirical zero does not prove actor impossibility, actor rejection or actor nonoccurrence.

### 7.8 `BLOCKED_POSITIVE_TRANSITION_AUTHORITY_ZERO_EFFECT`

Use when exact supported PSEPF + exact comparator prerequisites exist but no separately accepted V3 positive transition authority is present.

This is the current production posture of `v3_psepf_zero_positive_guard.py` because the active registry is empty.

### 7.9 `POSITIVE_DELEGATE_TO_ACCEPTED_V3_OWNER`

This state is permitted only when all of the following hold:

1. PSEPF exact lane is positively supported at the exact source/release/target/conditioner grain;
2. no proxy substitutes for exact support;
3. comparator result is `EXACT_COMPARATOR_MATCH`;
4. every required predicate ancestry/comparability authority is exact and current;
5. every operation-specific measurement/transport premise required by the owner rule is positively authorized;
6. the presented positive transition authority matches one separately accepted current registry entry exactly;
7. the registry entry authorizes every guarded source class in the request lineage;
8. transition surface and operation class match exactly;
9. replay/provenance closure is complete.

Effect of this seam: **still zero**.

Permission granted: call the named V3 owner rule with the exact decision and inputs.

Any V3 mutation, event creation, causal parentage, effective-time semantics, route realization, response or persistent change is owned by that V3 rule and must be returned as a separate V3 receipt.

## 8. Permissions

The seam may:

- verify exact identities/currentness/replay;
- compare already-owned generated-subject facts to exact empirical predicate criteria under explicit authority;
- preserve exact PSEPF positive/negative/empty/noncomparable/unresolved states;
- preserve structural peer context as context only;
- deny with zero actor effect;
- delegate to a separately accepted exact V3 transition owner.

The seam may not:

- create actor facts;
- infer belief, personality, identity, desire, knowledge, memory, action, response, opportunity or realization from empirical prevalence/probability/geometry;
- infer route realization from route existence/applicability;
- convert proxy evidence into exact evidence;
- infer individual prediction from population evidence;
- infer measurement portability from source equivalence;
- infer transport authority from structural comparability;
- self-register positive transition authority;
- mutate V3 state directly.

## 9. Replay/provenance burden

A seam decision is replay-complete only if replay can reconstruct the same semantic decision from:

- exact generated-subject/fact refs as they existed at the declared effective time;
- exact predicate ancestry/comparator bindings;
- exact source universe/release/query/model-rule identity;
- exact PSEPF result/replay identity;
- structural-context identity/currentness when used;
- exact authority snapshots and acceptance bindings;
- exact decision precedence/version;
- all typed negative states encountered.

Mutable selectors such as `latest`, `default`, `nearest`, `fuzzy` or `*` are forbidden in meaning-bearing replay inputs.

Historical authority pinning is part of semantic replay. Re-running against whatever authority is current later is not equivalent replay.

## 10. Information-loss declaration

Every result must explicitly state whether information was lost before the seam.

At minimum:

- exact PSEPF lane: `NO_ADDITIONAL_SEAM_COMPRESSION`;
- explicit proxy lane: record dropped conditioner identities and loss count/fraction;
- scalar/model summaries: name the compression/model semantics explicitly;
- blocked/empty/noncomparable states: `NO_DEFAULT_VALUE_SUBSTITUTION`.

No loss declaration can promote compressed/proxy evidence to actor truth.

## 11. Existing reusable implementation/tests

Reuse map is authoritative only as implementation capital, not as obligation closure. See `02_EXISTING_ASSET_REUSE.tsv`.

Core reuse:

- `source_backed_positioned_subject_possibility.py` — exact conditioned query, explicit proxy lane, specificity loss, source/release closure and deterministic replay;
- `test_source_backed_positioned_subject_possibility.py` — exact supported, unresolved/proxy, valid-empty, noncomparable, cross-source/release fail-closed and replay coverage;
- `test_a05_z08_positioned_admission.py` — explicit actor/prediction rejection and no smoothing/nearest/extrapolation;
- `v3_psepf_zero_positive_guard.py` — zero-positive default and exact external delegation boundary;
- `test_psepf_zero_positive_guard.py` — zero-effect invariants, unaccepted authority denial and exact delegation-only behavior;
- `pre553_empirical_objects.py` — exact public empirical identity/state vocabulary and deferred actor-comparator/PSEPF/V3-input separation;
- `pre553_structural_admission.py` — structural admission is separate and cannot create actor position/belief/etc.;
- `m5_runtime_rsc_peer_prior.py` — structural context eligibility is not V3 mutation authority.

## 12. Exact open gates

See `03_OPEN_GATES.tsv`.

Primary gates:

- `OBL031` comparator/predicate ancestry — OPEN;
- `OBL032` production PSEPF metabolism — OPEN / strong return required;
- `OBL012` measurement portability — conditional dependency when the concrete comparator/transition requires measurement transfer;
- operation-specific structural transport/comparability authority — `OPEN_GATE` when actually required;
- exact positive V3 transition owner/registry binding — absent in current production registry.

## 13. Minimal GT0-compatible seam path

Current-lawful path:

`EXACT PRE-V3 PSEPF RESULT`

→ verify source/release/query/replay identity

→ require exact V3-owned generated-subject fact refs

→ require exact predicate ancestry/comparator authority

→ if absent: `BLOCKED_COMPARATOR_ANCESTRY_ZERO_EFFECT`

→ if exact comparator exists, evaluate exact PSEPF state

→ `VALID_EMPTY` / `NONCOMPARABLE` / unresolved/proxy / typed zero: preserve corresponding zero-effect state

→ if exact supported: require exact separately accepted V3 transition-owner registry binding

→ current registry absent: `BLOCKED_POSITIVE_TRANSITION_AUTHORITY_ZERO_EFFECT`

→ future accepted binding only: `POSITIVE_DELEGATE_TO_ACCEPTED_V3_OWNER`

At no point does this seam infer actor belief, personality, identity or action.

## 14. Central fan-in recommendation

Adopt this seam as the negative/permission constitution between learned-world evidence and V3. Do **not** mark `OBL031/032` closed merely because the interface is now specified.

The implementation program after central fan-in should first realize an exact comparator/predicate-ancestry receipt and then, only under competent authority, bind the smallest concrete V3 transition owner required by Golden Thread 0.

Terminal:

`PASS__WSC001E_PREV3_V3_METABOLISM_CONTRACT_CONSTITUTED__READY_FOR_CENTRAL_FANIN`
