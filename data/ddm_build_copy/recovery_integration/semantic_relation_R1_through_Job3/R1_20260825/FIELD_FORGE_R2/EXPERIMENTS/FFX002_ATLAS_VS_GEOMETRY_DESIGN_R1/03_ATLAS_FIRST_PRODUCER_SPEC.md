# FFX002 — ATLAS-FIRST PRODUCER SPEC

Status: `EXPLORATORY_PRODUCER_DESIGN__NOT_CURRENT_ARCHITECTURE`

## 1. Purpose

Construct the strongest non-geometric, loss-preserving representation of the exact common respondent surface without degenerating into an unbounded dump of every possible cross-tab.

The atlas preserves empirical conjunction, conditional redistribution, higher-order co-occurrence, support, uncertainty posture, and provenance. It does **not** define distance, neighborhoods, axes, latent classes, fields, or social dimensions.

## 2. Required outputs

### 2.1 `ATLAS_RESPONDENT_FACT`

One exact fact per governed respondent containing only lawfully exposed/observed position and disposition states plus typed non-substantive response states.

Fields include:

- respondent_id_ref
- risk_set_ref
- position_state_refs[]
- disposition_state_refs[]
- exact exposure refs[]
- raw/design weight refs
- source/instrument ancestry refs[]
- partition state
- provenance hash

This is the lossless empirical floor. It is not itself a social object.

### 2.2 `POSITIONAL_CONFIGURATION_FACT`

A conjunction of authority-admitted position states over an exact respondent risk set.

Fields:

- configuration_id
- member_state_refs[]
- order_k
- support_n
- support_weight
- kish_effective_n where weighted
- support_tier
- exact respondent-set hash or replay query
- lower-order parent refs[]
- provenance

No configuration receives a similarity score or coordinate.

### 2.3 `DISPOSITION_COMPLEX_FACT`

An exact same-respondent joint state over a lawful coexposure/J subset.

Fields mirror the positional configuration fact and additionally preserve:

- disposition_measurement_subset_ref
- source_structure / coadministration refs
- response-state semantics

A complex may be contradictory or minority-valued. No coherence requirement exists.

### 2.4 `CONFIGURATION_DEPENDENCE_FACT`

Neutral relation between one position configuration and one disposition outcome/complex:

- joint support
- `P(D | C)`
- comparison baseline ref
- absolute probability difference
- risk ratio/odds ratio only where well-defined
- conditional mutual information contribution where applicable
- support/uncertainty posture
- held-out replay statistics
- provenance

It is association/redistribution evidence, not mechanism.

### 2.5 `CONDITIONAL_REDISTRIBUTION_PROFILE`

A bounded collection of `CONFIGURATION_DEPENDENCE_FACT` objects answering a preregistered query family. It preserves the full destination distribution, including minority alternatives, rather than only a winning category or scalar effect.

### 2.6 `EMPIRICAL_MOTIF`

Optional compressed higher-order recurring pattern admitted only when all motif-generation gates below are met. A motif is a stable empirical interaction signature, not a semantic ideology/field/class label.

## 3. Candidate generation without ontology assumption

### 3.1 Mandatory low-order floor

Always compute and preserve:

- all 1-way marginals for admitted states;
- all lawful 2-way joint tables among active position variables;
- all lawful 2-way joint tables among disposition items within their exact coexposure risk sets;
- all preregistered position -> disposition query tables.

These are indexed facts, not a claim that pairwise structure is sufficient.

### 3.2 Higher-order position configurations

Generate candidates by deterministic Apriori-style hierarchical expansion from supported lower-order conjunctions. Expansion stops when:

- support falls below the preregistered `SUPPORTED` threshold for generalization;
- all children are redundant under exact support closure;
- maximum order `K_position` frozen from the design surface is reached.

Recommended canary `K_position <= 5`, with the exact cap frozen before final holdout evaluation.

Low-support observed conjunctions that arise in the respondent facts are retained in the exact floor even when they are not expanded as generalizable candidates.

### 3.3 Higher-order disposition motifs

Generate candidates only inside lawful coexposure components and only from exact J-authorized subsets. Use hierarchical closure and require evidence that the candidate adds information beyond all immediate lower-order parents.

A candidate motif enters the compact atlas only if:

1. design-set support tier is `SUPPORTED`;
2. conditional/multi-information increment exceeds the 95th percentile of the topology-preserving within-item permutation null;
3. it is selected in >=80% of design-set bootstrap resamples;
4. its held-out direction/order pattern is not reversed beyond the preregistered tolerance.

The raw joint fact remains available even if motif admission fails.

## 4. Redundancy control

The compact atlas uses **closed conjunctions + minimal generators**:

- if a higher-order conjunction has exactly the same respondent support as a lower-order conjunction, store the closed set once and link the minimal generators;
- identical conditional-distribution payloads within numerical tolerance are content-addressed and referenced rather than duplicated;
- ancestry-equivalent synthetic clones are deduplicated at the substantive-fact layer while their fixture/source provenance remains preserved.

This is compression by exact logical redundancy, not by semantic similarity.

Forbidden shortcut:

`distance(config_A, config_B)` introduced to cluster configurations. That would smuggle geometry into the atlas and must be separately named/compared rather than hidden inside pruning.

## 5. Sparse-cell treatment

Sparse empirical branches are never converted to absence or noise.

States:

- `SUPPORTED_FOR_DIRECT_CONDITIONAL_ESTIMATION`
- `LOW_SUPPORT__FACT_PRESERVED__NO_STABLE_GENERALIZATION`
- `ZERO_OBSERVED_IN_EXACT_RISK_SET`
- `NOT_COMPOSABLE_OR_NOT_EXPOSED`

No frequency-only category merge is permitted.

For downstream prediction only, the atlas may expose a **secondary pooled decoder** that backs off hierarchically to lower-order parent configurations. The pooled estimate must reference the exact raw branch and identify the amount of shrinkage/backoff. It may never replace the raw empirical fact.

## 6. Uncertainty

Always preserve:

- raw n;
- weighted mass where authorized;
- Kish effective n for weighted screening;
- design/holdout frequency;
- bootstrap stability for discovered motifs/configuration-selection decisions.

Do not fabricate design-based confidence intervals without design variance authority. Where only descriptive resampling is available, label it `DESCRIPTIVE_RESAMPLING_UNCERTAINTY`.

## 7. Evidence levels

- `E0_EXACT_RESPONDENT_FACT`
- `E1_EXACT_MARGINAL_OR_JOINT_FACT`
- `E2_SUPPORTED_CONDITIONAL_FACT`
- `E3_RESAMPLE_STABLE_HIGHER_ORDER_MOTIF`
- `E4_HELD_OUT_REPLICATED_MOTIF_OR_REDISTRIBUTION`

These levels concern empirical representation strength. They do not license causal or strong sociological interpretation.

## 8. Admissible compression

The producer must emit both:

1. a lossless indexed fact store sufficient to replay every emitted compact object; and
2. a compact atlas manifest containing nonredundant supported objects.

Compression cost is measured explicitly as bytes, object count, and query latency. No loss is acceptable merely because a configuration is inconvenient.

## 9. What the atlas refuses to infer

The producer never infers:

- metric distance or neighborhood;
- axes/dimensions;
- latent class membership;
- semantic equivalence across categories;
- missing exposure from response blankness;
- population target from weight availability;
- actor belief/personality;
- field, capital, class, hegemony, homology, or mechanism.

## 10. Hostile self-tests

The atlas fails if:

- substantive fact count increases under a byte-identical questionnaire-block clone with shared ancestry;
- low-support factual branches disappear after pruning;
- pruning decisions use holdout data;
- a hidden distance/similarity metric determines motif or configuration equivalence;
- partial pooling overwrites exact facts;
- motif admission is unstable under resampling/nulls;
- storage/query complexity grows superlinearly without bounded pruning gains on the canary;
- exact replay cannot reconstruct compact objects from respondent facts and manifests.

## 11. Replay

All IDs are content-addressed from canonicalized member refs + exact risk set + estimand + producer version. Candidate generation order is deterministic. Bootstrap/permutation seeds are stored. The output must regenerate byte-identically except for explicitly documented floating-point summaries.
