# S01 — Q03 POSITION SEMANTIC / OCCUPANT-FACT SPLIT REPAIR R1 — RETURN

Repository: `maidiu/rawlsing`

Worker branch: `agent/rabochii-prev3-w17-s01-q03-position-occupant-split-repair-r1`

Commission tip: `01608ad5ae492c432816db3b1b91a06632a86ad0`

Authorized grain: `PREV3_Q03_OBJECTIVE_POSITION_SEMANTIC_OCCUPANT_SPLIT_REPAIR_AND_RECONTENT_ADDRESS_R1_ONLY`

Library: `NOT USED`

## Terminal

`S01_PASS__Q03_POSITION_SEMANTIC_OCCUPANT_SPLIT_REPAIRED_RECONTENT_ADDRESSED_R1`

## Holding

PASS.

The R01 type error is repaired at exactly the commissioned layer:

```text
POSITION_SEMANTIC_IDENTITY
!=
OCCUPANT_ACTOR_INDEXED_OBJECTIVE_POSITION_FACT_IDENTITY
```

The repaired Q03 semantic candidate preserves the surviving source-backed relation bundle, Wright/M10 provenance, Q73A distinctness proof, semantic-owner authority, currentness ceiling, and negative ceilings.

`EXACT_OBJECTIVE_ACTOR_OR_ENTITY_IDENTITY` has been removed from both:
- the structural-position `constitutive_requirements`; and
- the hashed `canonical_identity_material`.

It is now owned only by the separately gated later actor-indexed objective-position fact/materialization layer.

No actor/entity fact is emitted here.

## Re-content-addressed candidate

Prior blocked hash:

`e040ae101388d0c9a87befa4fcd88ab3e861424376ad00b9e864c885d5bb12f9`

Repaired content hash:

`60e0f41b8cd1e3b22f43dbfc2cb8bbf97c81aec7f1664486ec4adf92533af505`

Repaired candidate identity:

`urn:rawlsing:prev3:objective-position-admission-candidate:sha256:60e0f41b8cd1e3b22f43dbfc2cb8bbf97c81aec7f1664486ec4adf92533af505`

Canonicalization remains the Q03 law: UTF-8 JSON, lexicographically sorted object keys, compact separators, declared array order preserved, with no hash/identity field included in the canonical identity material.

The new hash is therefore caused by the repaired position-semantic constitutive material, not by an occupant identity or later fact instance.

## Preserved Q03 semantics and provenance

Preserved without widening:
- semantic class `OBJECTIVE_STRUCTURAL_POSITION`;
- canonical name `PRODUCTIVE_ASSET_SEPARATED_ACTIVE_WAGE_LABOUR_POSITION`;
- productive-asset control insufficient for independent production;
- active wage-labour sale relation;
- exact employer/counterpart identity;
- exact institutional-rule context;
- Wright/M10 source worker tip `0ebca9ff111bea63838f9b68c8e5c3cb93d9d128`;
- source-ledger blob `606de007e0f6dcb28e552bd8c959f3c4ec1fd2a7`;
- the three Q03 documentary loci;
- semantic owner `Q03_M10_M01_OBJECTIVE_POSITION_SOURCE_AUTHORITY_R1`;
- Q73A/PREV3POS distinctness;
- no employment-status, occupation, income, subjective/person-state, unemployment, manager-label, bounded-exit, or exploitation shortcut;
- no mechanism/channel/topology or causal permission;
- semantic-admission currentness is not actor-fact currentness or present-day world truth.

## Exact semantic/fact split

The reusable position-semantic identity now contains only:

```text
PRODUCTIVE_ASSET_CONTROL_INSUFFICIENT_FOR_INDEPENDENT_PRODUCTION
ACTIVE_WAGE_LABOUR_SALE_RELATION
EXACT_EMPLOYER_OR_COUNTERPART_IDENTITY
EXACT_INSTITUTIONAL_RULE_CONTEXT
```

A later separately authorized objective-position fact/materializer must instead bind:

```text
EXACT_OBJECTIVE_ACTOR_OR_ENTITY_IDENTITY
EXACT_POSITION_SEMANTIC_CANDIDATE_IDENTITY
EXACT_APPLICABILITY
EXACT_PERMISSION
EXACT_VALID_TIME_OR_CURRENTNESS
EXACT_PROVENANCE_AND_DEPENDENCY
DETERMINISTIC_FACT_REPLAY
```

Changing the occupant therefore changes a later fact identity, not this repaired semantic candidate identity.

## Replay

Replay artifact:

`02_REPLAY_Q03_POSITION_SEMANTIC_IDENTITY.py`

It deterministically recomputes SHA-256 from the exact canonical identity material and asserts:
- replayed hash equals `60e0f41b8cd1e3b22f43dbfc2cb8bbf97c81aec7f1664486ec4adf92533af505`;
- candidate ID is derived from that hash;
- repaired hash differs from the blocked Q03 hash;
- occupant identity is absent from semantic constitutive/hash material;
- occupant identity is present in the later fact-materialization requirement set;
- exact M10 source tip/blob are preserved;
- direct PREV3POS emission and actor/entity materialization remain false/forbidden.

Local replay result:

```text
PASS S01_PASS__Q03_POSITION_SEMANTIC_OCCUPANT_SPLIT_REPAIRED_RECONTENT_ADDRESSED_R1 60e0f41b8cd1e3b22f43dbfc2cb8bbf97c81aec7f1664486ec4adf92533af505 urn:rawlsing:prev3:objective-position-admission-candidate:sha256:60e0f41b8cd1e3b22f43dbfc2cb8bbf97c81aec7f1664486ec4adf92533af505
```

## Boundaries

No actor-indexed PREV3POS fact was emitted.
No real actor/entity was materialized.
No mechanism/channel rule or topology was created.
No V555/M2, V3/person state, or OBL063 semantics were used.
S02/S03 provisional output was not consumed.
Library was not used.
MAIN and PRE-MAIN were not mutated.

## Successor gate

PASS wakes only a separate independent qualification of the repaired content-addressed semantic candidate.

It does not wake actor/entity materialization directly.
