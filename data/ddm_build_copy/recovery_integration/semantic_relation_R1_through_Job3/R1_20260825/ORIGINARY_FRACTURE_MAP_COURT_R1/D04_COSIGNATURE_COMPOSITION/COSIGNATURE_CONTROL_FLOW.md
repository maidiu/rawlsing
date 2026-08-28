# D04 Co-Signature Control Flow R1

Design only. This file specifies controller composition; it is not executable production code.

## Invariants

1. Exact discovered branch identity enters by ref/replay, never by private respondent-list reconstruction.
2. Eligible substantive targets are enumerated from governed finite metadata/authority before co-signature outcomes are inspected.
3. Demographic/position coordinates can condition a branch but cannot become attitude/co-signature target nodes.
4. Current target arity ceiling is `J=2`.
5. Same-respondent exact joint evidence is evaluated directly; pairwise marginals never prove 3+ topology.
6. Authority refs, ancestry/dependency refs, denominators, weights, missing/special states, uncertainty and replay remain separately addressable.
7. Returned co-signature material is empirical learned-branch context only.

## Control flow

```text
INPUT: exact discovered branch handoff
  |
  |-- branch EmpiricalPredicate exact ref
  |-- immediate parent exact ref
  |-- full ancestry exact refs
  |-- branch replay/member-set binding exact ref
  |-- source/universe exact refs
  |-- risk/routing exact refs
  |-- measure/weight exact refs
  v
[1] EXACT BRANCH RESOLUTION
  |
  | require exact ref identity
  | require exact replay/member-set closure
  | reject caller respondent list as substitute
  v
[2] GOVERNED TARGET-CATALOG RESOLUTION
  |
  | resolve authority-frozen finite catalog
  | include substantive response/question surfaces only
  | exclude demographic/position coordinates
  | exclude actor/persona/belief/causal derived labels
  | preserve source/routing/response topology authority
  v
[3] CANONICAL TARGET ENUMERATION
  |
  | dedupe by exact ref
  | canonical sort by exact ref key/hash
  | generate all unordered distinct pairs i<j
  | no ranking/top-k/semantic relevance/manual nomination controls reachability
  v
[4] EXACT J=2 QUERY COMPOSITION
  |
  | condition_predicate_ref := exact branch ref
  | target_refs := exact canonical pair
  | target_arity_and_topology := authorized same-respondent J=2 topology
  | bind exact universe/risk/scope/measure/query authority refs
  | preserve branch/target dependencies + replay
  v
[5] AUTHORITY/FIXED-FRONTIER CLOSURE
  |
  | candidate grammar/DiscoveryAuthority freezes complete pair frontier
  | frontier membership fixed before empirical evaluation
  | typed failure if exact target/query/authority closure cannot be built
  v
[6] DELEGATE TO EXISTING EXACT EXECUTORS
  |
  | I03 exact query for marginals/joint cells as governed
  | I05 exact bounded discovery/validation as governed
  | D04 controller adds no private statistical evaluator
  v
[7] CONSERVE DISTINCT DENOMINATORS/STATES
  |
  | source/risk denominator
  | branch denominator
  | target-question denominator per target
  | joint/pattern denominator per pair
  | joint-cell numerator/support
  | RAW vs GOVERNED_WEIGHTED projections
  | missing/special/valid-empty/low-support/underpowered/noncomparable/uncertainty
  v
[8] EXACT RESULT COLLECTION
  |
  | EmpiricalFact exact refs
  | DiscoveryResultReceipt exact refs
  | execution/replay refs
  | immediate parent + full ancestry retained
  v
[9] REF-ONLY TOPOLOGY CLOSURE
  |
  | prove target catalog identity
  | prove number of eligible targets
  | prove complete expected pair count = n*(n-1)/2 minus explicit authority exclusions
  | prove every authorized pair has exact terminal coverage
  | bind exact authority/dependency/replay refs
  v
[10] RETURN TO FRACTURE-MAP CONTROLLER
      |
      +--> branch_ref
      +--> topology_closure_receipt_ref
      +--> exact result/fact refs
      +--> typed coverage/uncertainty state

      NO direct edge to:
      X actor belief
      X personality/persona
      X causal explanation
      X named semantic relation without separate admission
```

## Pair evidence schedule

For each exact pair `(T_i,T_j)` inside branch `B`:

1. resolve target-specific evaluability/routing for `T_i`;
2. resolve target-specific evaluability/routing for `T_j`;
3. compute/resolve branch-conditioned marginals under their own target denominators;
4. compute/resolve exact same-respondent joint denominator for respondents evaluable on both targets;
5. evaluate the exact authorized joint cells/patterns;
6. preserve joint support and any branch-conditioned dependence/cotravel validation;
7. emit exact facts/receipts including typed negative states.

Marginals and joint cells are intentionally separate facts. Equal marginals with different joint structure remain detectable because the joint is executed rather than inferred.

## Two-target XOR / equal-marginal / stable-minority cases

### Two-target XOR / exactly-one

With two authorized binary/presence targets, exact joint cells can represent `(1,0)` and `(0,1)` support and distinguish them from `(0,0)` and `(1,1)`. If a governed XOR/exactly-one validator is used, its candidate/query identity must be frozen before evaluation. This does not authorize 3+ target XOR.

### Equal marginals, different joint

Execute both exact marginals and the exact J=2 joint. Do not derive the joint from marginals. A changed joint with unchanged marginals is therefore representable and replayable.

### Stable minority

Do not top-k or prevalence-prune declared pair cells. Preserve supported nonmodal cells and their exact raw/weighted support and uncertainty state. “Minority” describes empirical support configuration only.

## Failure closure

Fail closed before evaluation if any of the following holds:

- branch exact ref or replay identity is unavailable;
- target catalog is not positively governed and finite;
- target eligibility depends on reading co-signature outcomes;
- a demographic/position field would enter the substantive target graph;
- routing/response topology authority for a target is unresolved;
- a target pair cannot be bound to exact J=2 query semantics;
- caller requests target arity greater than two under current authority;
- source/risk/measure identities cannot be preserved exactly.

## J=3+ guard

```text
requested target tuple arity > 2
  |
  v
current maximum_target_arity_J == 2
  |
  X DO NOT DECOMPOSE INTO PAIRS AND CALL IT HIGHER-ORDER
  |
  v
FAIL CLOSED
  |
  +--> require new/versioned topology authority
       + exact tuple enumeration
       + query/topology semantics
       + denominator/support law
       + validators
       + replay/completion law
```

## Completion criterion for current J=2

For branch `B` and governed eligible target set `T`:

`expected_pair_count = |{ unordered distinct pairs from T allowed by exact authority }|`

A topology closure is complete only when every expected pair has exactly one exact terminal-coverage result binding and the receipt seals the exact target catalog, branch, authority, result refs and replay identity.
