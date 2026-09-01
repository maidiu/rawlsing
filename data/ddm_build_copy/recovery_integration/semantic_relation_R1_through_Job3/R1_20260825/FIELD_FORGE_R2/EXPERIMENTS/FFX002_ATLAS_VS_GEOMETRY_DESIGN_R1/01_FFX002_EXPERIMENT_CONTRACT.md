# FFX002 — EXPERIMENT CONTRACT

Status: `DESIGN_ONLY__PENDING_LAWFUL_BINDINGS`

## 1. Identified question

Using one identical, governed respondent-level survey surface, determine which of the following empirical states is supported:

- geometry preserves stable/downstream-useful relational information that a loss-preserving atlas cannot preserve economically enough;
- geometry mostly imposes an unstable low-dimensional representation on facts better preserved by configuration/dependence objects;
- the two representations preserve different non-substitutable invariants;
- both representation families fail;
- or the comparison itself is invalid because common respondent/exposure/estimand authority cannot be established.

No winner is preferred ex ante.

## 2. Experimental unit

The experimental unit is one `FFX002_CANARY_BUILD` defined by the tuple:

`{respondent_universe, governed_respondent_id, exact_exposure_topology, exact_scope, frozen_position_role_surface, frozen_disposition_surface, estimand, weight_contract, source/instrument ancestry, frozen_train_holdout_manifest}`.

Both representations consume exactly this tuple. Any divergence in respondent rows, exposure rules, category semantics, scope, weight target, or holdout membership invalidates the duel.

## 3. Preregistration phases

### Phase 0 — authority bind

Bind all placeholders in `02_COMMON_INPUT_AND_CANARY_ADMISSION_CONTRACT.md`. Fail closed if any hard dependency is unresolved.

### Phase 1 — semantic freeze

Before outcome inspection:

- freeze exact position-role dispositions;
- freeze position/disposition active ancestry separation;
- freeze source/instrument and analytic-role block manifests;
- freeze admissible category states and lawful alternate encodings;
- freeze estimand and weight use;
- freeze hostile perturbations and metric thresholds.

### Phase 2 — partition freeze

Create deterministic design/holdout partitions from governed respondent IDs under the declared risk/design strata. Store seed, algorithm, and partition hash. No candidate pruning, dimension selection, motif selection, or tuning may inspect the final holdout.

### Phase 3 — independent production

Run `ATLAS_FIRST` and `GEOMETRY_FIRST` independently from the common input. Neither producer may consume the other's learned output.

### Phase 4 — hostile perturbation court

Execute all applicable fixtures in `05_HOSTILE_PERTURBATION_MATRIX.tsv`. A fixture that cannot be instantiated because the lawful canary lacks its required variable/block is typed `NOT_INSTANTIABLE_ON_THIS_CANARY`, not silently skipped. Exposure/risk-set, ancestry, estimand, and leakage tests are mandatory on every canary.

### Phase 5 — frozen query/metric court

Evaluate the representations using `06_COMPARISON_METRIC_REGISTRY.tsv` and the downstream ablation contract. Do not aggregate metrics into a master score.

### Phase 6 — decision state

Apply `10_DECISION_RULE.md` mechanically after hard-invalidity checks.

## 4. Common empirical query battery

Before either producer is fitted, construct a frozen query manifest from the common input schema, not from discovered geometry or atlas motifs. It must contain at least:

1. high-support exact position configurations -> disposition marginal/joint distributions;
2. bounded minority position configurations -> disposition distributions;
3. disposition complex prevalence conditional on position configurations;
4. pairwise and selected higher-order J relations on lawfully coexposed disposition items;
5. counterpattern queries: common position configuration with empirically minority disposition alternatives;
6. sparse/walkback queries whose exact high-order configuration has inadequate support;
7. source/instrument-block conditioned checks;
8. holdout respondent likelihood/reconstruction targets.

Query candidates are generated deterministically from the design partition subject to preregistered support rules. Final metric evaluation is on holdout respondents and on synthetic hostile fixtures.

## 5. Support law

Support is descriptive evidence quality, not existence ontology.

For unweighted cells, `n >= 25` is the minimum `SUPPORTED_FOR_CONDITIONAL_ESTIMATION` canary tier because the worst-case Bernoulli standard error is <= 0.10 under an iid descriptive approximation. `n < 25` remains an exact observed branch but is `LOW_SUPPORT_FOR_GENERALIZATION`.

For weighted cells use Kish effective sample size for the same canary screening threshold while separately preserving raw n and total weight. If the source provides design-based variance authority, that authority supersedes the iid screening approximation for inferential uncertainty.

No low-support branch is deleted merely to improve either representation.

## 6. Information ancestry firewall

Position and disposition representations are constructed independently.

Hard rule for the claim-scoped cross-space comparison:

`intersection(position_active_measurement_ancestry, disposition_active_measurement_ancestry) = empty`.

Shared respondent identity, source/scope refs, risk-set refs, and weight refs are linkage/provenance, not active measurement ancestry.

Any direct or derived active overlap yields `EXPERIMENT_INVALID__ANCESTRY_CONTAMINATION` until resolved by exclusion or supplementary treatment.

## 7. Interpretation firewall

Neither producer emits `CLASS`, `FIELD`, `CAPITAL`, `HEGEMONY`, `HOMOLOGY`, `PRESSURE_PATHWAY`, or actor psychology as empirical facts.

The geometric producer emits unlabeled dimensions/subspaces and diagnostics. The atlas producer emits neutral configuration/dependence/motif facts. Downstream testing asks information preservation and usefulness, not sociological storytelling.

## 8. Replay contract

Every build emits:

- exact input artifact refs + hashes;
- code/version ref;
- frozen semantic authority refs;
- partition manifest + seed/hash;
- parameter/specification manifest;
- hostile fixture manifest;
- output hashes;
- deterministic/non-deterministic operation inventory.

Repeated execution with identical inputs/specification must reproduce deterministic artifacts byte-for-byte, modulo explicitly versioned floating-point tolerance for numeric decompositions.

## 9. Hard invalidation conditions

The experiment cannot proceed or cannot be interpreted if any of these occurs:

- respondent identity is ungoverned;
- exposure is inferred from missingness or source co-presence;
- atlas and geometry use different respondent/risk sets;
- estimands or weights differ except inside an explicit weight perturbation;
- position/disposition active ancestry overlaps;
- holdout information leaks into candidate generation/tuning;
- disconnected measurement components are forced into a common geometry;
- a representation silently changes semantic categories;
- a mandatory nuisance/null fixture cannot be replayed from provenance.

## 10. What would count as geometry earning anything

Geometry earns no role merely by existing, explaining inertia, or offering visually interpretable axes. It must produce stable relational or compression/downstream value under nuisance perturbation and holdout while remaining within tolerances for exact/minority/higher-order information loss.

## 11. What would count as atlas earning anything

Atlas-first earns no role merely by being lossless. It must avoid combinatorial explosion, preregister its pruning/compression law, survive resampling, preserve rare facts without laundering them through pooling, and support downstream queries at acceptable complexity.
