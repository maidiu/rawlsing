# FFX002 R2 — MULTI-VIEW ABLATION / INVARIANT-LOSS EXPERIMENT CONTRACT

Status: `DESIGN_ONLY__PENDING_EXISTING_AUTHORITY_BINDINGS`

## 1. Question

For one frozen claim and one identical lawful empirical substrate:

> Which empirically relevant invariants does each admissible representation preserve, approximate, lose, distort, or uniquely expose; what incremental downstream value does it add over weaker views; and does the bounded empirical result materially depend on lawful representation choice?

This is not a search for a master representation.

## 2. Experimental unit

One `FFX002_R2_CANARY` is identified by:

`{current_execution_sha, common_semantic_input_manifest_hash, claim_scope_ref, respondent_risk_set_ref, estimand, weight_design_contract, holdout_manifest}`

All representation arms consume the same unit. A different common manifest is a different canary variant, not another arm.

## 3. Mandatory first-canary arms

### Core A — exact configuration set view

Claim role: exact same-unit conjunction, minority alternatives, contradiction, and lawful higher-order configuration/J preservation without implicit distance.

### Core B — local geometric view

Claim role: local order/neighborhood/opposition/compression relations under explicit metric/decomposition choices. No global world-space and no axis-to-sociology promotion.

### Core C — direct conditional / redistribution view

Claim role: claim-direct `P(D|C)` or equivalent bounded redistribution summaries with explicit support/backoff, risk set, estimand, and uncertainty. This is the weakest mandatory analytical baseline.

Optional arms are admitted only under `03_REPRESENTATION_ARM_ADMISSION_MATRIX.tsv`.

## 3A. First-canary empirical admission floor

The representation redesign does not weaken the original canary's empirical adequacy requirements.

A candidate canary must provide, after lawful authority exclusions:

### Respondent/exposure
- governed respondent identity;
- positive actual exposure/coexposure authority for every active measurement;
- exact form/ballot/module/split/country/prior-answer predicates where relevant;
- no response-missingness proxy for exposure.

### Position surface
Minimum original canary guidance retained:
- at least 4 variables admitted `ACTIVE_POSITION`;
- those variables span at least 3 independently authorized analytic-role families if the source lawfully supplies three;
- no single source/instrument block is the sole source of position heterogeneity;
- at least one additional position candidate can be supplementary/conditioning/excluded so removal sensitivity is testable.

Preferred, not hard universal ontology:
- at least 6 active variables across at least 4 role families;
- at least one lawful ordered/continuous or bounded multi-role candidate for sensitivity testing.

### Disposition surface
Minimum original canary guidance retained:
- at least 8 separately respondent-facing disposition measurements;
- actual coexposure authority for the risk set;
- at least 2 source/instrument blocks or batteries;
- at least one lawful order>=3 higher-order J/configuration subset with adequate design-set support.

A multiple-response answer-slot set does not satisfy the repeated-item requirement merely because it has many coded members.

### Estimand/holdout
- explicit sample-descriptive or governed weighted/design estimand;
- feasible frozen holdout without destroying the lawful risk set;
- sufficient support to run the common query battery with honest abstention where needed.

If no current governed canary meets this floor, return a typed canary-rejection state. Do not relax the law or acquire data inside FFX002.

## 4. Pre-fork common semantic freeze

Before any view method runs:

1. bind the governed observation/provenance substrate;
2. bind respondent identity and actual exposure/risk-set authority;
3. bind source-native measurement/structure and response/special-state semantics;
4. execute only already-authorized TTAR transformations in a frozen order;
5. bind exact post-transform state identities;
6. bind claim scope, estimand, weight/design authority;
7. bind PRA and all other analytic-role authority;
8. bind unresolved/noncomparable states and cumulative loss;
9. canonicalize and hash the manifest;
10. require every arm to attest to that exact hash.

If an arm requires a semantic alteration, either:
- register a separate pre-fork common-input variant applied identically to every arm; or
- declare the arm inadmissible for the canary.

## 5. Representation-local method freedom

After the semantic freeze, each arm may choose only method operations that do not change the frozen ontology.

Examples:
- geometry: dimensionality, declared metric/decomposition family, regularization, nonsemantic display rotation, local compression;
- configuration: bounded order-k selection, indexing, support/pruning of compact summaries while source facts remain recoverable, exact-vs-backoff query strategy;
- conditional: estimator family, smoothing/pooling within already frozen semantic states, declared link scale, uncertainty estimator;
- graph/hypergraph: algorithm/layout over exact admitted relation semantics;
- latent/model: preregistered model family/class count.

Every method choice is recorded. No method may hide a semantic transform inside "preprocessing."

## 6. Phase order

### Phase 0 — authority bind
All hard dependencies in `10_POSITION_ROLE_AND_RESPONDENT_BINDING_DEPENDENCIES.tsv` must be exact. Otherwise stop.

### Phase 1 — common semantic manifest freeze
Construct `COMMON_SEMANTIC_INPUT_MANIFEST`; run canonical validation and hash attestation.

### Phase 2 — holdout / replay freeze
Freeze design/holdout partition, seeds, software/version refs, tolerances, and query manifest without final-holdout leakage.

### Phase 3 — independent view production
Produce A/B/C independently. No arm may consume another arm's learned output.

### Phase 4 — view-specific adequacy tests
Apply the preservation/loss registry and view-specific hostile tests.

### Phase 5 — common query battery
Run only queries for which a view is admitted; record `DOES_NOT_REPRESENT` rather than forcing a translation.

### Phase 6 — ablation / incremental value
Run weaker-baseline, target-added, target-removed, and multi-view comparisons under `05_VIEW_ABLATION_CONTRACT.md`.

### Phase 7 — PRE-V3 downstream ablation
Test actor-independent possibility information only.

### Phase 8 — typed representation-dependence result
Emit the narrow decision-state payload in `13_DECISION_STATE_PLACEHOLDER.md`. No winner-take-all ontology claim.

## 7. Hard invalidation conditions

Any of the following invalidates the experiment rather than a view:

- arm semantic-manifest hashes differ;
- respondent identity is ungoverned;
- exposure is inferred from response missingness or source co-presence;
- risk set or estimand silently differs across arms;
- ungoverned category merge/rebin/order/special-state mapping occurs after fork;
- PRA/analytic role differs across arms except in an explicitly separate pre-fork claim variant;
- holdout leakage occurs;
- active position/disposition ancestry overlaps;
- source-native ancestry becomes unrecoverable;
- a mandatory hostile fixture cannot be replayed from provenance;
- a disconnected component is forced into a relation the representation cannot lawfully define.

## 8. No master score

There is no scalar `architecture_quality`. Results are vectors of:
- invariant preservation/loss;
- hostile-test behavior;
- query adequacy;
- uncertainty/support posture;
- instability;
- storage/latency/compression;
- incremental downstream value;
- representation dependence.

A view can add value and still be barred from a claim because it destroys a critical invariant.

## 9. Claim ceiling

FFX002 R2 may establish only bounded representation adequacy, information loss, incremental utility, and representation dependence.

It may not establish:
- class/field/capital/hegemony;
- homology;
- causal mechanism;
- actor psychology;
- realized V3 personality;
- cross-context recurrence in the first canary.

## 10. Replay

Every output must bind:
- exact common manifest hash;
- arm method manifest;
- code/version ref;
- seed/partition manifest;
- query manifest;
- hostile fixture refs;
- loss manifest;
- output hashes;
- deterministic/non-deterministic operation inventory.

Deterministic artifacts must replay byte-identically; numeric methods use explicitly versioned tolerances.
