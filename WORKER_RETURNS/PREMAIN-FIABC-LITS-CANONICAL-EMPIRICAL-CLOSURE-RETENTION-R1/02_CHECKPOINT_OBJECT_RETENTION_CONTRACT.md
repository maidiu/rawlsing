# Checkpoint / object-retention contract

## Purpose

Checkpoint v3 is the zero-source resume boundary for current LiTS candidate-neutral empirical truth.

Schema:

`FIABC_LITS_CURRENT_NEUTRAL_I05_MATERIALIZATION_CHECKPOINT@3.0.0`

Canonical closure:

`FIABC_LITS_CANONICAL_CURRENT_EMPIRICAL_OBJECT_CLOSURE@1.0.0`

## Canonical-current storage law

The canonical store is PRE553-native. It is not an ASTRA-shaped summary.

Each retained public object is represented by its complete canonical `as_dict()` preimage, modulo lossless content-addressed factoring of repeated large fragments. Hydration restores the exact original canonical document before the existing PRE553 constructor is invoked.

For every retained public object:

`semantic_hash(rehydrated_object.semantic_projection()) == rehydrated_object.content_hash`

and the supplied `object_id/content_hash` must be accepted by the exact public-object constructor.

## Content-addressed fragment law

A fragment reference has the form:

`{"$canonical_preimage_fragment": "<sha256>"}`

The fragment store contains the corresponding canonical value and validation requires:

`semantic_hash(fragment_value) == fragment_hash`

Only identity-preserving storage factoring occurs. No semantic interpretation, coercion, label inference, value inference or source reread is permitted during hydration.

The current factoring applies to repeated identity-bearing fact material:

- risk-set member refs;
- denominator member refs;
- complete-cell semantic projection.

## Closure law

The checkpoint must close over:

1. all 60 current empirical facts;
2. all 50 discovery result receipts;
3. every exact query and predicate referenced by the 77 frontier roles;
4. authority snapshots required by retained public objects;
5. current empirical-universe/source-relation support objects available from the sealed release;
6. LiTS representation authority material/snapshot;
7. C11 logical release and replay identity material;
8. current execution/replay/frontier/projection/exact-ref identities.

The compact FIABC comparison manifest remains a separate projection and must agree exactly with canonical discovery receipts/facts.

## Zero-source resume law

Resume from v3 must not call source-backed neutral materialization. It must have:

- source hash passes = 0;
- decoder calls = 0;
- Candidate A/B/C processes = 0;
- candidate outputs seen = 0;
- candidate-owned roots consulted = [];
- candidate-owned state reused = false.

ASTRA regression is optional on resume. Absence of an ASTRA projection is not absence of current canonical empirical truth.

## Negative law

Checkpoint v3 does not authorize or retain positive structural admission. It may not create:

- structural relations;
- `StructuralEmpiricalAdmission@1.0.0`;
- causal claims;
- population generalization;
- actor/person/V3 state.

Checkpoint v1 and v2 are rejected for complete-current-object resume because they do not satisfy this retention contract.
