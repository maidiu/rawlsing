# D15 — AUTONOMOUS DISCOVERY ARCHITECTURE

## 1. Selection

D15 selects a single `DiscoveryService` with two execution modes over one explicit `DiscoveryAuthority` contract:

- `EXACT_BOUNDED`
- `ADAPTIVE_EXPLORATORY`

The authority contract is canonical. The execution strategy is replaceable only if its declared coverage/replay semantics remain true.

`DISCOVERY AUTHORITY != DISCOVERY RESULT != MATERIALIZATION AUTHORITY != CACHE POLICY`.

## 2. Authority contract — fixed before search

Every DiscoveryAuthority must declare:

1. discovery family/service identity;
2. eligible target questions/components;
3. eligible empirical coordinates and exact source-native/canonical semantic authority;
4. lawful response/value/topology states;
5. allowed atomic predicate grammar;
6. allowed conjunction/composition grammar;
7. maximum/governed conditioner depth/arity `K`;
8. maximum/governed response target arity `J`;
9. allowed recursive branch depth/expansion grammar;
10. source/respondent-universe scope;
11. time/wave scope and comparability rules;
12. routing/applicability/risk-set law;
13. raw/governed weighting/measure law;
14. minimum feasibility/support rules and their typed result semantics;
15. uncertainty/validation method authority or typed unquantified state;
16. candidate scoring/ranking rule if ranking exists;
17. pruning law;
18. exact coverage claim;
19. deterministic tie/order rules;
20. algorithm/version/replay identity.

Authority may bound a large class without individually naming the winning relationship.

## 3. Candidate families

Within an authority that includes them, the service can construct candidates for:

- unary demographic/social forks;
- response × empirical-coordinate conditionals;
- arbitrary bounded coordinate conjunctions;
- response × coordinate conjunctions;
- pair response cotravel;
- bounded k-way response configurations;
- conditional reversals/Simpson structures;
- minority/nonmodal departures;
- recursive subgroup forks;
- branch-conditioned distributions;
- branch-conditioned cotravel;
- temporal change;
- source-indexed cross-universe disagreement.

These are candidate **classes**, not mandatory separate algorithms or permanent tables.

## 4. `EXACT_BOUNDED` mode

### Contract

Given an exact finite/finitely constructible authority frontier `F`, this mode evaluates every candidate in `F`, or uses a computation proven mathematically equivalent to evaluating every candidate, and validates outputs through exact EmpiricalQueryEngine facts.

### Coverage claim

`COMPLETE_FOR_EXACT_DECLARED_FRONTIER`

Nothing outside the declared frontier is claimed.

### Required properties

- Candidate enumeration is deterministic/order-independent under the same authority snapshot.
- No unary-signal prerequisite exists unless the authority deliberately excludes zero-unary-signal interactions from its coverage; therefore XOR can be covered when conjunction arity includes it.
- Support feasibility pruning is allowed only when the authority defines the boundary before search and the resulting state remains typed.
- Every evaluated candidate can be replayed from C11 + query spec + authority + algorithm identity.
- Discovery may return `VALID_EMPTY` when no candidate passes validation. This does not mean no relationship exists outside the declared frontier.

### Cost contract

The authority's `F` is a semantic cost axis. Implementation may share scans, factor exact calculations, parallelize or index C11, but may not skip a candidate while retaining a complete-for-F claim without a safe coverage theorem.

## 5. `ADAPTIVE_EXPLORATORY` mode

### Contract

Construct the same lawful candidate universe, then use a governed proposal/traversal strategy such as beam, priority, recursive expansion or screening to choose `F_eval ⊂ F`.

Every emitted relationship is exact-validated through the EmpiricalQueryEngine.

### Coverage claim

`EXACT_RESULTS__NONEXHAUSTIVE_FRONTIER_COVERAGE`

The receipt records:

- full authorized frontier definition;
- evaluated candidate set or reproducible evaluated-set rule;
- pruned/discarded states required by replay;
- stopping rule;
- validation rule;
- explicit classes for which no completeness is claimed.

Unevaluated candidates are not negative evidence.

### Screens

A screen may support a broader completeness claim only when a separately accepted no-false-negative theorem applies to that exact discovery class and input semantics.

A unary-signal screen has no generic no-false-negative theorem for XOR; therefore it may not claim general interaction completeness.

## 6. Recursive social-fork discovery

Recursive discovery is a mode over `DiscoveryResultReceipt` branch predicates, not a permanent historical-tree ontology.

For each reached branch:

1. replay exact branch predicate/membership;
2. construct the branch-local authorized candidate frontier;
3. execute `EXACT_BOUNDED` or `ADAPTIVE_EXPLORATORY` under its coverage contract;
4. create child branch receipt only after exact validation;
5. preserve ancestry, predicate identity, support/uncertainty and replay provenance.

A branch member table is optional cache. The canonical requirement is exact membership replay.

## 7. Minority law

Supported configurations remain reachable unless the authority explicitly places them outside the discovery frontier for a governed reason.

`LOW_SUPPORT != ABSENT`.

Support thresholds may declare a candidate statistically/epistemically non-admissible while still recording that the supported configuration exists and why it was not promoted. Cost-driven top-k truncation cannot turn supported minority into semantic absence.

## 8. Conditional reversal law

Reversal/interaction discovery compares exact pooled and conditioned EmpiricalFacts under compatible risk-set/measure semantics. A scalar association score is never sufficient evidence by itself.

Where pooled and conditioned risk sets are not comparable, return `NONCOMPARABLE`, not a reversal claim.

## 9. Cotravel law

Same-respondent cotravel uses exact pair or J-way contingency, not E3 modal cells or E4 scores.

Branch-conditioned cotravel first resolves exact branch membership, then constructs the joint within that cohort.

## 10. Cross-universe discovery

Respondent-bound candidate evaluation happens within one EmpiricalUniverse unless exact linkage authority exists.

Cross-universe discovery compares source-indexed EmpiricalFacts. It does not create synthetic same-person cotravel across independent samples.

Disagreement/noncomparability may itself become a discovered source-indexed relationship under authority.

## 11. Materialization

Discovery does not require permanent materialization of all candidates.

Persist canonically only:

- DiscoveryAuthority;
- DiscoveryResultReceipt when a discovered relationship/branch must survive as an identified historical result;
- ReplayReceipt where historical reproducibility requires it.

Optional caches:

- evaluated exact E1/E2 facts;
- branch member sets;
- candidate score tables;
- E3/E4 diagnostics.

None becomes authority.

## 12. Replay

A historical discovery replay binds:

- C11 content identity;
- EmpiricalUniverse identities;
- DiscoveryAuthority version/hash;
- candidate grammar/frontier;
- query engine semantics;
- algorithm implementation/version;
- coverage/pruning/stopping contract;
- deterministic tie/order rules;
- RNG state only if lawful randomness is part of proposal order.

Replay must reproduce the same evaluated frontier and result/typed-empty outcome for deterministic mode, or the same lawful seeded trajectory where randomness is authorized.

## 13. What this replaces

Target capability replaces the semantic roles, not exact algorithms, of:

- V547 exhaustive-pair determinicity search;
- V548 recursive breakage materialization;
- V549 branch cotravel discovery;
- current primary-star secondary summaries;
- current top-two recursive tree.

Historical implementations remain genealogy/reference. Their valid information needs are subsumed by exact queries + governed discovery receipts.

## 14. Explicit completeness statement

Rawlsing does **not** claim universal exhaustive discovery over every mathematically imaginable relation.

It claims:

- `EXACT_BOUNDED`: exhaustive and exact for the finite/finitely constructible frontier explicitly named by a DiscoveryAuthority;
- `ADAPTIVE_EXPLORATORY`: exact for emitted results, non-exhaustive for unevaluated candidates unless a separately proven safe-pruning theorem applies.

This is the strongest honest coverage contract compatible with D12 autonomy and D14 cost law.
