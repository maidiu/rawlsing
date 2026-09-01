# FFIF006 — CLAIM NORMALIZATION AND SPLITTING RULES

## 1. Finite normalization grammar

Every prose question must normalize to one or more atomic assertion slots:

```text
SLOT_TYPE(
  operands;
  empirical_unit;
  risk_set;
  population_and_context;
  temporal_scope;
  estimand;
  quantifier;
  conditioning_set;
  baseline;
  scale_or_value_domain;
  target_invariant
)
```

Admitted first-order slot types:

- `EXACT_STATE_EXISTENCE`
- `STATE_PREVALENCE`
- `EXACT_CONFIGURATION_EXISTENCE`
- `CONFIGURATION_MASS`
- `CONDITIONAL_DISTRIBUTION`
- `CONDITIONAL_CONTRAST`
- `ORDER_RELATION`
- `NEIGHBORHOOD_RELATION`
- `TOPOLOGY_RELATION`
- `HIGHER_ORDER_COOCCURRENCE`
- `RECONSTRUCTION_FIDELITY`
- `PREDICTIVE_ADEQUACY_FOR_TARGET`
- `COMPRESSION_AT_FROZEN_FIDELITY`
- `TRANSPORT_RECURRENCE_OF_INVARIANT`

New slot types require schema versioning. They may not be invented by a view producer at runtime.

## 2. Split before comparison

One prose question must split whenever answering it requires different:

- empirical units or risk sets;
- populations, contexts, or times;
- estimands or weight targets;
- quantifiers;
- conditioning sets or baselines;
- scales/value domains;
- semantic-input/TTAR manifests;
- PRA role assignments;
- invariants;
- descriptive, predictive, transport, or causal inferential classes.

`Is there separation?` therefore does not normalize to one slot. It may generate separately:

- `EXACT_CONFIGURATION_EXISTENCE` or `CONFIGURATION_MASS` for exact-state separation;
- `CONDITIONAL_CONTRAST` for redistribution;
- `NEIGHBORHOOD_RELATION` for local ordering;
- `TOPOLOGY_RELATION` for connectedness.

They remain different claims unless an independently authorized bundle requires them together.

## 3. No silent completion

`Does education matter?` must specify:

- exact education measurement/state and TTAR ancestry;
- exact PRA role;
- destination/outcome;
- population/context/risk set;
- conditioning set and baseline;
- estimand and weight target;
- quantifier;
- scale;
- inferential class.

The normalizer may suggest missing coordinates. It may not choose them. Missing constitutive coordinates return:

`CLAIM_UNDERSPECIFIED { missing_fields[]; candidate_splits[]; forbidden_default }`.

## 4. Quantifier law

At minimum distinguish:

- `EXISTS`
- `FOR_ALL_IN_SCOPE`
- `PREVALENCE_AT_LEAST(t)`
- `AVERAGE_OVER(risk_set)`
- `CONDITIONAL_FOR_EACH(group_set)`
- `LOCAL_AROUND(anchor_set)`
- `RECURRENT_ACROSS(context_set)`

Existence never silently becomes prevalence; average never becomes universal; local never becomes global.

## 5. Scale and inferential-class law

Ordinal evidence may support an `ORDER_RELATION`; it does not support a cardinal distance claim. A descriptive association does not normalize to a causal mechanism claim. Predictive adequacy is its own target-indexed claim, not evidence of general representational truth.

## 6. Canonicalization

Normalization is deterministic only after semantic adjudication supplies every constitutive coordinate. Canonical payloads use immutable refs, sorted set-valued operands, declared order where order is semantic, explicit `NONE`, and the same hashing law as the common semantic input manifest.

Two claims compare as:

- `SAME_PROPOSITION_SAME_COMPARISON_CONTRACT`;
- `SAME_PROPOSITION_DIFFERENT_COMPARISON_CONTRACT`;
- `SAME_BROAD_QUESTION_DIFFERENT_INVARIANT`;
- `DIFFERENT_CLAIM`;
- `CLAIM_UNDERSPECIFIED`.

Only the first enters direct materiality adjudication.

## 7. Mutation and supersession

Any post-freeze change to a constitutive coordinate creates a new claim version and proposition hash. Any change only to support/uncertainty or tolerance creates a new comparison version and comparison hash. The prior object remains replayable; it is never overwritten.

## 8. Bundle prohibition

The normalizer may emit atomic claims and a proposed bundle candidate. It may not declare them co-required. Bundle authority is governed separately by `12_CLAIM_BUNDLE_AUTHORITY.md`.

