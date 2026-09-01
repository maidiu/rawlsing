# FFIF003 — NULL AND FALSIFICATION CONTRACT

Status: design contract only. No respondent-level test is executed by this court.

## 1. Principle

A cross-context signature is informative only if the claimed recurrence is **harder to obtain under lawful alternatives than under the registered transport map**.

Therefore the null target is not only “no association.” It also includes “the same apparent recurrence is obtainable by arbitrary semantic correspondence, representation choice, or block composition.”

## 2. Required null/control families

### N1 — LOCAL_ASSOCIATION_NULL

Preserve local univariate/marginal distributions and source/risk-set structure while breaking the cross-variable/respondent association relevant to the local invariant.

Purpose: test whether the transported shape/motif is carried by real local dependence rather than marginals/instrument structure.

Future execution must preserve exact exposure/design strata where required; missingness may not stand in for exposure.

### N2 — SEMANTIC_CORRESPONDENCE_PERMUTATION

Permute candidate endpoint mappings among semantically admissible alternatives.

Purpose: determine whether the chosen mapping is uniquely/discriminatively supported or merely one of many ways to obtain the same recurrence.

### N3 — TYPE_CONSTRAINED_CATEGORY_MAPPING_RANDOMIZATION

Randomize category correspondence only within the declared admissible type/order constraints.

Purpose: avoid straw nulls that violate obvious semantics while measuring residual researcher freedom.

### N4 — UNRELATED_BLOCK_NEGATIVE_CONTROL

Apply the same transport machinery to structurally unrelated item/measurement blocks matched as closely as practical for size, support, and source topology.

Purpose: detect generic pattern-finding machinery.

### N5 — CONTEXT_HOLDOUT

Choose/freeze the transport rule without one context; test the held-out context without retuning the map/signature.

Purpose: test whether a purported recurrent structure generalizes beyond pairwise fitting.

### N6 — BLOCK_COMPOSITION_SWAP

Change the measurement-block composition within a declared hostile perturbation while preserving the substantive claim where possible.

Purpose: detect signatures driven by battery length, duplicated/counterfeit items, questionnaire topology, or one dominant block.

### N7 — LOCAL_REPRESENTATION_PERTURBATION

Recompute the relevant local object across lawful specification alternatives: thresholds, admissible category handling, active/supplementary choices, graph construction, geometry family, etc.

Purpose: distinguish transport of a structural invariant from transport of a representation artifact.

### N8 — ALTERNATIVE_MAP_MULTIPLICITY

Enumerate/sample the admissible map family `H_q` and measure how many materially different maps satisfy the preservation predicate.

Purpose: identify non-identifiable transport. A signature matched by almost any map contains little cross-context information.

### N9 — SIGNATURE_COMPONENT_ABLATION

Remove one signature component at a time and recompute discriminativeness.

Purpose: detect decorative components and identify whether one weak/universal feature carries the match.

### N10 — RISK_SET_ESTIMAND_SENSITIVITY

Within only separately lawful alternatives, vary local risk-set/weight/estimand choices and record whether the recurrence classification changes.

Purpose: expose composition-driven recurrence or hidden estimand substitution. This does not authorize new estimands.

### N11 — CROSS_REPRESENTATION_DISCORDANCE

Where more than one local representation is independently lawful for the same claim, test whether the transport result survives or becomes typed representation-dependent.

Purpose: prevent representation-shopping.

## 3. Decision outputs

A future executable court should not return only a p-value or similarity score. It should classify:

- `SURVIVES_REGISTERED_NULLS`;
- `MAP_NONIDENTIFIABLE`;
- `REPRESENTATION_DEPENDENT`;
- `RISK_SET_ESTIMAND_SENSITIVE`;
- `INSUFFICIENT_SUPPORT`;
- `SEMANTIC_AUTHORITY_FAILURE`;
- `REVERSAL`;
- `PARTIAL_RECURRENCE`;
- `NO_TRANSPORT`.

## 4. Falsification by transport family

| transport | minimum hostile controls |
|---|---|
| exact semantic | version drift + near-semantic negative controls + routing contract audit |
| order | type-constrained map permutations + tie/order perturbation |
| rank/quantile | denominator/weight/tie sensitivity + pooled-vs-local denominator audit |
| topology | threshold/edge-construction perturbation + node-map permutations |
| conditional shape | association null + configuration decomposition + scale/link sensitivity |
| motif | role-map permutations + unrelated-block motif controls + representation perturbation |
| signature | all applicable component controls + map multiplicity + ablation + holdout |

## 5. Downgrade law

A failed higher-order transport does not automatically imply complete incomparability. Downgrade only if a narrower claim has its own independent authority and passes its own tests:

`SIGNATURE -> MOTIF / CONDITIONAL / TOPOLOGY / RANK / ORDER / EXACT -> NO_TRANSPORT`

The reverse is forbidden: passing a weaker transport never upgrades the claim automatically.

## 6. Anti-arbitrariness law

`RECURRENCE UNDER ARBITRARY MAPPINGS IS EVIDENCE AGAINST THE SIGNATURE`.

This is the core falsification principle of FFIF003. If a claimed “deep structure” survives because it is too generic to fail, it is not strong evidence of cross-context recurrence.
