# T01 — REPAIRED Q03 OBJECTIVE-POSITION INDEPENDENT HOSTILE QUALIFICATION R1 — RETURN

Repository: `maidiu/rawlsing`

Worker branch: `agent/rabochii-prev3-w18-t01-repaired-position-hostile-qualification-r1`

Commission tip: `7f06a1408b94dc33eccafc6185392954f296c363`

Authorized grain: `PREV3_REPAIRED_Q03_OBJECTIVE_POSITION_INDEPENDENT_HOSTILE_QUALIFICATION_R1_ONLY`

Library: `NOT USED`

## Terminal

`T01_PASS__REPAIRED_Q03_OBJECTIVE_POSITION_INDEPENDENTLY_QUALIFIED__ACTOR_FACT_MATERIALIZATION_REMAINS_SEPARATELY_GATED`

## Adjudication

PASS.

The repaired S01 candidate independently survives qualification at the semantic-position ceiling. The R01 type error is actually removed rather than renamed:

```text
POSITION_SEMANTIC_IDENTITY
!=
OCCUPANT_ACTOR_INDEXED_OBJECTIVE_POSITION_FACT_IDENTITY
```

The qualified semantic candidate remains:

`urn:rawlsing:prev3:objective-position-admission-candidate:sha256:60e0f41b8cd1e3b22f43dbfc2cb8bbf97c81aec7f1664486ec4adf92533af505`

with canonical content hash:

`60e0f41b8cd1e3b22f43dbfc2cb8bbf97c81aec7f1664486ec4adf92533af505`

No real actor/entity fact is emitted or implied by this PASS.

## Hostile qualification matrix

### 1. Actor-independent semantic identity — PASS

`EXACT_OBJECTIVE_ACTOR_OR_ENTITY_IDENTITY` is absent from both the structural-position constitutive requirements and the canonical identity material.

The repaired semantic identity hashes only the reusable position proof shape plus exact source/provenance, authority, baseline-distinctness and use-ceiling material. A different occupant therefore belongs to a later fact identity rather than changing this semantic candidate.

The definition's phrase `objective actor/entity structural position` identifies the domain of possible occupancy; it does not bind any concrete occupant.

The requirements `EXACT_EMPLOYER_OR_COUNTERPART_IDENTITY` and `EXACT_INSTITUTIONAL_RULE_CONTEXT` also do not repeat the R01 error. They are requirement kinds in the semantic proof shape. No concrete employer/counterpart identifier or concrete institutional-rule instance is present in the hashed semantic candidate.

### 2. Objective-world semantics / no person-state leakage — PASS

Every positive constitutive requirement is objective:

```text
PRODUCTIVE_ASSET_CONTROL_INSUFFICIENT_FOR_INDEPENDENT_PRODUCTION
ACTIVE_WAGE_LABOUR_SALE_RELATION
EXACT_EMPLOYER_OR_COUNTERPART_IDENTITY
EXACT_INSTITUTIONAL_RULE_CONTEXT
```

Self-report, belief, preference, appraisal, motivation, disposition, biography and person-state are explicitly forbidden as constitutive shortcuts.

### 3. Exact source / claim provenance closure — PASS

The repaired candidate preserves the exact frozen M10/Wright provenance:

- source worker tip `0ebca9ff111bea63838f9b68c8e5c3cb93d9d128`;
- source-ledger blob `606de007e0f6dcb28e552bd8c959f3c4ec1fd2a7`;
- Wright *Classes* Ch. 3 supplied loci `857-909`, `951-959`, and `978-996`.

Those source claims support productive-asset/property relations, exchange/work strategies, the active wage-labour counterpart relation, and institutional-rule context. The frozen extraction separately preserves the structural-position / incumbent distinction.

The source extraction remains documentary evidence only. It does not self-issue project semantic authority or current actor-fact truth.

### 4. Distinctness from Q73A / PREV3POS — PASS

The semantic axes remain distinct.

Q73A owns `ACTIVE_POSITION__FISCAL_INCORPORATION_OR_OBLIGATION_POSITION`, with baseline fact:

`PREV3POS:c823a816ce6f71431c99b1a466c7313f3766e5d1e7832fc36b6a31f15835dd02`

The repaired candidate is instead constituted by productive-asset noncontrol plus an active wage-labour counterpart relation under exact institutional rules. Neither identity entails the other.

### 5. Constitutive closure / no hidden inferred element — PASS

The position cannot be admitted from a bare employment-status code, occupation, industry, sector, job title, income level, unemployment/exclusion, manager label, subjective state, bounded-exit restriction, or exploitation classification.

All four objective predicates must be separately evidenced at the asserted source/context grain. In particular, exploitation is not inferred from the position identity alone.

### 6. Negative ceilings — PASS

The candidate remains semantic-only. It does not authorize or emit:

```text
DIRECT_PREV3POS_FACT_EMISSION
ACTOR_OR_ENTITY_OCCUPANCY_ASSERTION
MECHANISM_OR_CHANNEL_RULE
TOPOLOGY_OR_SOURCE_RECEIVER_EDGE
EXPLOITATION_FACT_FROM_POSITION_ALONE
CAUSAL_EFFECT_OR_PERSON_UPTAKE
V555_OR_M2_USE
V3_OR_PERSON_STATE
OBL063_DRIVER_TYPE_OR_PERSON_TERMINAL_SEMANTICS
```

Semantic-admission currentness is not actor-fact currentness or present-day world truth.

### 7. Deterministic replay / change sensitivity — PASS

Independent replay of the exact canonical identity material reproduces:

`60e0f41b8cd1e3b22f43dbfc2cb8bbf97c81aec7f1664486ec4adf92533af505`

The T01 replay additionally proves change sensitivity across sixteen mutations spanning semantic name/definition, every constitutive predicate, source tip/blob/locus, semantic authority, commission/HQ authority, Q73A baseline distinctness, and use ceiling. Every governed semantic mutation produces a different SHA-256 identity.

Two different hypothetical occupant labels held outside the semantic canonical material leave the semantic candidate identity unchanged. That is the exact property R01 required.

### 8. Suitability for a later actor-fact materializer — PASS

The repaired candidate now supplies a stable semantic candidate identity and exact constitutive proof shape without claiming any instance truth.

A later, separately authorized fact/materialization lane must still bind:

```text
EXACT_OBJECTIVE_ACTOR_OR_ENTITY_IDENTITY
EXACT_POSITION_SEMANTIC_CANDIDATE_IDENTITY
EXACT_APPLICABILITY
EXACT_PERMISSION
EXACT_VALID_TIME_OR_CURRENTNESS
EXACT_PROVENANCE_AND_DEPENDENCY
DETERMINISTIC_FACT_REPLAY
```

T01 does not satisfy, infer, waive, or pre-authorize any of those actor-fact gates.

## Replay artifact

`02_REPLAY_T01_REPAIRED_POSITION_QUALIFICATION.py`

Local replay result:

```text
PASS T01_PASS__REPAIRED_Q03_OBJECTIVE_POSITION_INDEPENDENTLY_QUALIFIED__ACTOR_FACT_MATERIALIZATION_REMAINS_SEPARATELY_GATED 60e0f41b8cd1e3b22f43dbfc2cb8bbf97c81aec7f1664486ec4adf92533af505 urn:rawlsing:prev3:objective-position-admission-candidate:sha256:60e0f41b8cd1e3b22f43dbfc2cb8bbf97c81aec7f1664486ec4adf92533af505 change_sensitivity_mutations=16
```

## Preserved boundaries

No actor-indexed PREV3POS fact was emitted.

No real actor/entity was materialized.

No mechanism, channel, topology or source-to-receiver edge was created.

No V555/M2, V3/person state or OBL063 semantics were used.

T02/T03 provisional output was not consumed.

Library was not used.

MAIN and PRE-MAIN were not mutated.

## Successor gate

T01 PASS wakes only a separate materialization-source/applicability lane for the qualified semantic candidate.

It does not wake direct actor/entity fact emission and does not establish that any real actor/entity currently occupies the position.
