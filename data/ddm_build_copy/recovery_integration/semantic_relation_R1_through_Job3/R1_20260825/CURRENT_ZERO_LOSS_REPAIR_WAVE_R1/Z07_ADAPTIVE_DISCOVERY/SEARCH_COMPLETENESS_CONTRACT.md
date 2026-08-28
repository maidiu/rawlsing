# Z07 ADAPTIVE EXPLORATORY SEARCH COMPLETENESS CONTRACT R1

Status: `IMPLEMENTED_CANDIDATE__TYPED_PARTIAL_SEARCH_AND_REPLAY_CONTRACT_FROZEN`

## 1. Separate discovery modes

The current PRE553 machine now has two deliberately non-equivalent discovery execution contracts:

1. `PRE553_I05_EXACT_BOUNDED_DISCOVERY@1.0.0`
   - authoritative exact-bounded mode;
   - complete declared frontier;
   - frontier fixed before the first empirical query;
   - every candidate evaluated;
   - no adaptive traversal;
   - unchanged by Z07.

2. `PRE553_ADAPTIVE_EXPLORATORY_DISCOVERY@1.0.0`
   - exploratory service mode;
   - explicitly nonexhaustive frontier coverage while partial;
   - result-driven proposal/prioritization allowed only **between complete sealed evaluation units**;
   - search policy affects exploration order/reachability only;
   - never an empirical/structural truth authority.

`EXACT_BOUNDED != ADAPTIVE_EXPLORATORY`

`PARTIAL_SEARCH_NEGATIVE = FORBIDDEN`

## 2. Typed completeness states

The adaptive service returns exactly one of:

- `PARTIAL_BUDGET_EXHAUSTED`
  - the run budget ended while known units remain unvisited;
  - unvisited unit refs remain explicit in the checkpoint;
  - no absence/negative/completeness inference is licensed.

- `PARTIAL_INTERRUPTED`
  - interruption occurred only after a complete sealed unit;
  - every known but unvisited unit remains explicit;
  - restart resumes from the exact checkpoint and cannot skip one silently.

- `EXPLORATORY_POLICY_FRONTIER_EXHAUSTED`
  - every unit reachable under the **frozen exploratory policy and determinant history actually generated in this run lineage** has been visited;
  - this is an exploratory-policy exhaustion state, not an authoritative global empirical-negative claim.

There is intentionally no `GLOBAL_NEGATIVE`, `NO_RELATION_EXISTS`, or equivalent adaptive terminal state.

## 3. Sealed evaluation-unit law

An `AdaptiveExplorationUnit` is an opaque exact request whose empirical semantics are owned by its underlying exact evaluator/authority path.

An `AdaptiveUnitOutcome` is accepted only when:

- it belongs to the exact visited unit;
- its `sealed_unit_coverage` is `COMPLETE_SEALED_EVALUATION_UNIT`;
- any proposed child binds the exact parent unit;
- the child generation is parent generation + 1;
- the child determinant set binds the frozen adaptive determinant state and the exact sealed parent-result ref;
- the proposal rule is explicitly within the adaptive authority's allowed proposal-rule set;
- `global_negative_claim = false`;
- `semantic_truth_effect = false`;
- `actor_v3_effect = false`.

Therefore adaptive result-driven reachability may change only after the prior empirical evaluation unit has closed.

## 4. Search policy and identity

The adaptive authority pins:

- `ADAPTIVE_EXPLORATORY_AUTHORIZED`;
- coverage claim `EXACT_RESULTS__NONEXHAUSTIVE_FRONTIER_COVERAGE`;
- algorithm identity `PRE553_ADAPTIVE_EXPLORATORY_DISCOVERY@1.0.0`;
- deterministic tie law `HEURISTIC_RANK_DESC_THEN_UNIT_REF`;
- no RNG in this minimum service;
- pruning/search contract `ADAPTIVE_PARTIAL_SEARCH_BETWEEN_SEALED_UNITS`;
- unvisited state `UNKNOWN_UNVISITED`;
- a content-hashed `adaptive_search_policy` object;
- exact allowed proposal-rule refs;
- maximum generation and maximum frontier size.

The current hostile fixture includes explicit `policy_id` and `policy_version`; the entire policy mapping is content-addressed, so changing policy/version/heuristic material changes `search_policy_ref` and invalidates replay/resume identity. The runtime does not elevate those labels or any historical numeric coefficient into empirical authority.

## 5. Deterministic scheduling

Within one frozen policy/determinant state:

1. known unvisited units are ordered by declared exact integer `heuristic_rank` descending;
2. ties are broken by exact `unit_ref.key`;
3. input storage/list order is irrelevant;
4. each unit is visited at most once;
5. proposals are merged by exact unit ref and conflicting same-ref scheduling material fails closed;
6. visited order and unvisited frontier are checkpointed exactly.

No historical coefficient, top-k constant, tree score, NMI threshold, or old heuristic is canonized by Z07.

## 6. Replay / restart identity

`AdaptiveSearchCheckpoint` binds:

- exact DiscoveryAuthority ref;
- exact content-hashed search-policy ref;
- exact determinant-state ref;
- exact root-unit refs;
- all known unit definitions;
- ordered visit history;
- exact sealed result/proposal outcome for every visited unit;
- explicit visited and unvisited unit refs;
- typed completeness state and stop reason.

Resume fails closed if authority, policy, determinant, root universe, or root scheduling material changes.

`verify_adaptive_replay` re-executes the exact run and returns public `ReplayReceipt@1.0.0` with:

- `REPLAY_VERIFIED` when result/checkpoint/replay identity is exact;
- `NONDETERMINISTIC_REPLAY` when re-execution diverges.

## 7. Negative and promotion ceiling

The adaptive scheduler itself creates no `EmpiricalFact`, structural fact, actor fact, or global absence claim.

A supported result discovered inside a sealed unit remains governed by the ordinary exact empirical validation and authority path. Search rank never promotes it.

`SEARCH_PRIORITY != EMPIRICAL_SUPPORT`

`EXPLORATORY_EXHAUSTION != GLOBAL_NEGATIVE`

`ADAPTIVE_OUTCOME != STRUCTURAL_ADMISSION`

`PRE553_EXPLORATION != ACTOR_V3_STATE`

## 8. Relationship to Authority-37 fracture-map controller

The Authority-37 result→next-frontier controller and Z07 are complementary rather than competing owners:

- a complete sealed exact generation/result may be consumed by a governed controller/proposal producer;
- that producer may return exact future exploration units with parent/result determinant refs;
- Z07 deterministically prioritizes and checkpoints which future sealed units are explored under the frozen exploratory policy/budget;
- when one such unit is an exact I05 invocation, its internal I05 frontier remains fully fixed/evaluate-all;
- Z07 never adds/removes/reorders candidates **inside** that I05 invocation.

Thus:

`RESULT_DRIVEN_BETWEEN_UNITS = ALLOWED_IN_ADAPTIVE_SERVICE`

`RESULT_DRIVEN_INSIDE_OPEN_I05_FRONTIER = FORBIDDEN`
