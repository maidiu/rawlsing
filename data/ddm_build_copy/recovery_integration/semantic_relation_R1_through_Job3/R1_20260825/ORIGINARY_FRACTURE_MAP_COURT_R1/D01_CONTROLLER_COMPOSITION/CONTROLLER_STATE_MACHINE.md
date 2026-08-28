# D01 — FRACTURE-MAP CONTROLLER STATE MACHINE R1

Status: `DESIGN_ONLY__NO_PRODUCTION_IMPLEMENTATION`

## 0. Governing composition theorem

```text
CONTROLLER_GENERATES_GOVERNED_FINITE_FRONTIER
-> FRONTIER_IS_CANONICALIZED_AND_HASH_SEALED
-> DiscoveryAuthority@1.0.0 BINDS THAT EXACT FRONTIER
-> I05 COMPILES THE WHOLE DECLARED FRONTIER BEFORE ITS FIRST I03 QUERY
-> I05 EVALUATES EVERY CANDIDATE
-> CONTROLLER CONSUMES THE COMPLETE RECEIPT SET
-> NEXT GENERATION MAY BE GENERATED FROM THOSE EXACT RESULTS
```

Never:

```text
I05 result -> widen/prune/reorder the frontier currently being evaluated
```

Result-driven generation is lawful only **between complete I05 invocations**. I05 remains `PRE553_I05_EXACT_BOUNDED_DISCOVERY@1.0.0` with `COMPLETE_FOR_EXACT_DECLARED_FRONTIER`, `NONE_EXACT_EVALUATE_ALL`, canonical candidate-hash order, no score/top-k/unary screen/adaptive stop, and no RNG-controlled reachability.

## 1. Exact run seed

### Public semantic root

No new public request family is needed.

The semantic start object is one existing `EmpiricalQuerySpec@1.0.0`, used in the role `ROOT_RESPONSE_SURFACE_QUERY`. It must:

- name the focal substantive question/component by exact `target_refs`;
- bind exact source universe(s), risk set, routing semantics, measure basis, response topology and response-semantic authority;
- expose the full governed target domain rather than one answer cell;
- bind an exact root `EmpiricalPredicate@1.0.0` whose role is scope/routing/parent-cohort restriction only;
- carry no caller-chosen modal answer, predictor, branch membership, next branch, secondary splitter, or cotravel winner.

Operational invocation additionally supplies the exact predicate object matching `condition_predicate_ref`, exact sealed C11 release refs, the immutable `AuthorityRegistry`, and exact controller-law authority refs. That invocation bundle is an execution argument, **not** a new public semantic object.

### Anti-cheat seed check

Fail closed if the root condition predicate contains a focal-response-value leaf that preselects the answer whose morphology is supposed to be discovered. The caller may choose the research surface; the caller may not choose its empirical answer.

## 2. Controller/I03/I05/MX01R2 boundaries

```text
CALLER
  |
  | exact focal EmpiricalQuerySpec + exact scope predicate + releases + authority refs
  v
[C00 CONTROLLER] validate root identity, authority, full response domain, no answer leakage
  |
  v
[C10 CONTROLLER -> I03] execute exact full response distribution for current parent cohort
  |
  v
[I03] EmpiricalFact(s): complete cell projection, raw/weighted support, typed states, replay
  |
  v
[C20 CONTROLLER] derive exact response-cell inventory / maximal-cell set / presence-pattern catalog
  |
  +--> [AUTHORITY GATE] semantic modal/multimodal/shape classification
  |         missing law -> preserve facts + stop typed unresolved; do not invent M
  |
  v
[C30 CONTROLLER] exhaustively enumerate lawful positional coordinate/value predicate atoms
  |
  v
[C40 CONTROLLER] build canonical per-node predictor grammar
  |                 hash candidate_universe_definition
  |                 instantiate exact DiscoveryAuthority bound to frozen snapshots
  |                 SEAL FRONTIER
  v
=================== I05 EXACT FRONTIER BOUNDARY ===================
[I05] compile every candidate before first query; evaluate every candidate; emit one receipt per candidate
==================================================================
  |
  v
[C50 CONTROLLER] consume complete predictor receipt set
  |                 retain every supported candidate absent explicit selection law
  |                 optional PRIMARY/SECONDARY annotation only under frozen selection authority
  v
[C60 CONTROLLER] construct exact branch-role predicates from governed M and each retained P
  |
  v
[C70 CONTROLLER] build/seal RECURSIVE_SUBGROUP_FORK realization frontier for all branch roles
  v
=================== I05 EXACT FRONTIER BOUNDARY ===================
[I05] evaluate every branch candidate; supported/empty/underpowered/noncomparable/etc. receipts
==================================================================
  |
  +--> supported recursive receipts -> accepted MX01R2 -> exact persisted handoff / replayable parent
  |
  +--> typed nonpositive branch states retained; never silently dropped
  |
  v
[C80 CONTROLLER] enumerate all governed other substantive question surfaces for this exact branch
  |                 no demographic targets; no correlation/topic/prevalence prefilter
  |                 detailed pair/joint composition remains D04 join authority
  v
[C90 CONTROLLER] build/seal branch-cosignature frontier(s)
  v
=================== I05 EXACT FRONTIER BOUNDARY ===================
[I05] evaluate complete declared cosignature frontier
==================================================================
  |
  v
[C100 CONTROLLER] apply frozen continuation/retention/stop law
  |                 missing law -> preserve branch + exact unresolved stop
  |
  +--> STOP: retain exact terminal state/reason
  |
  +--> CONTINUE: consume MX01R2 parent atom and generate N+1 finite frontier
  |                then loop to C10 for that actual discovered branch
  v
[C110 CONTROLLER] close whole-map topology / replay receipt if and only if public map-receipt law exists
```

## 3. C10 — baseline response surface without answer leakage

The controller invokes current I03 directly for the full governed distribution. I03 already returns exact `EmpiricalFact` cell projections and typed support under exact universe/risk/routing/measure/topology authority.

The controller may mechanically compute a deterministic set of maximal supported response cells from exact counts under the authorized measure. That mechanical set is **not yet** a semantic `MODAL`, `MULTIMODAL`, `POLARIZED`, `STABLE_MINORITY`, or other morphology label. Semantic morphology waits for positive controller law.

For multi-select items, the full exact response-pattern domain remains primary. Presence predicates are derived from that domain without replacing it. Equal presence marginals cannot collapse distinct pattern morphologies.

## 4. C20 — multi-label presence and pattern generation

Given exact multi-select topology and response-semantic authority:

- generate one exact pattern predicate for every governed substantive response pattern;
- generate response-label presence predicates as `IN` over every governed exact pattern containing that label;
- generate absence as the exact substantive-pattern complement, not as a bare negation that could absorb missing/refused/not-applicable states;
- keep a substantive `NONE_OF_THESE`/equivalent pattern as an ordinary exact response pattern when source semantics says it is substantive;
- keep DK/refusal/missing/not-applicable/unknown in their existing typed response-state lane.

`PRESENCE_MORPHOLOGY != PATTERN_MORPHOLOGY`.

## 5. C30 — exhaustive predictor candidate enumeration

For the current exact universe/release scope, enumerate all lawfully conditionable positional coordinate/value predicates from existing `EmpiricalCoordinateFact@1.0.0` plus positive coordinate/predicate authority.

Canonical inventory key is the exact semantic material needed to reproduce a predicate: coordinate semantic ref, authorized value/typed state, exact source/universe/effective-time scope where required, operator semantics, risk-set scope and authority refs.

Rules:

1. no caller predicate list;
2. no association score, prevalence, top-k, MI/NMI/Cramer's V/tree score or unary screen may decide reachability;
3. exact observed authorized coordinate values may be enumerated from the sealed governed release; missing/unknown/not-lawfully-conditionable states remain typed audit material rather than silently becoming social predictor values;
4. source universes remain separate absent explicit composition authority;
5. canonical exact-ref/hash order only.

The controller may preserve logically redundant or eventually empty candidates. Economics and safe theorem pruning are not D01 jurisdiction.

## 6. C40 — per-node predictor frontier sealing

For root node, baseline atom is the root scope predicate. For N+1, baseline atom is the accepted MX01R2 `recursive_parent_atom(...)` derived from the actual discovered branch handoff.

The controller generates a finite I05 grammar from **all** lawful predictor atoms and the focal full-distribution query template, using existing exact families/forms such as `RESPONSE_X_EMPIRICAL_COORDINATE`, `RECURSIVE_SUBGROUP_FORK`, `SINGLE_ATOM`, `AND_CARTESIAN_GROUPS` and `DISTRIBUTION_DIFFERS_FROM_BASELINE` only where their current contract applies.

Then, before I05 receives anything:

1. canonicalize the complete candidate-universe definition;
2. content-hash it into `candidate_grammar_ref`;
3. instantiate `DiscoveryAuthority@1.0.0` with exact source/risk/topology/measure/support/validation/coverage/pruning/algorithm/tie/RNG fields;
4. require exact positive `DISCOVERY_FRONTIER` authority closure for the operation;
5. freeze predicate and query-template catalogs;
6. only then call I05.

The controller does not create governance. It instantiates an authority-bound object from pre-existing frozen snapshots. Missing positive law is terminal.

## 7. C50 — supported predictor retention without arbitrary winner selection

I05 returns a receipt for every declared candidate. The minimal zero-loss controller does **not** need a heuristic winner.

Absent an explicit predictor-selection law:

- retain every `DISCOVERED_RESULT_SUPPORTED` predictor candidate;
- retain every typed negative/nonpositive receipt;
- do not label one supported predictor `PRIMARY` merely because it has a larger diagnostic score;
- do not discard lower-prevalence supported predictors.

If HQ later freezes a lawful primary/secondary selection relation, the controller may add that semantic annotation. Selection may never change the fact that all supported candidates remain preserved.

## 8. C60/C70 — four role quadrants with missingness-safe complements

Once a response pattern `M` and a predictor predicate `P` are positively governed, Authority35 fixes the logical roles. Branch construction must use resolved-domain complements, not naked boolean negation.

Let:

- `B` = exact current parent branch/scope predicate;
- `CR(P)` = exact predicate restricting to respondents with a lawfully resolved/conditionable value for P's coordinate;
- `M` = governed modal response-pattern predicate;
- `NM` = explicit `IN` over all other governed **substantive** response patterns for the focal surface.

Construct:

```text
CONFORMER        = B AND CR(P) AND P     AND M
DEVIANT_EXIT     = B AND CR(P) AND P     AND NM
ALT_CONVERGER    = B AND CR(P) AND NOT P AND M
ALT_MINORITY     = B AND CR(P) AND NOT P AND NM
```

Thus `NOT P` does not swallow missing coordinate data, and `NM` does not swallow DK/refusal/not-applicable/missing responses.

A substantive `NONE` pattern remains inside `NM` and may also be retained as its own exact response-pattern branch. Calling it `CATEGORY_FAILURE` requires separate positive semantic law.

### Branch realization through unchanged I05

Generate one finite `RECURSIVE_SUBGROUP_FORK` frontier containing every role predicate. Use the current `DISTRIBUTION_DIFFERS_FROM_BASELINE` validator against parent B. Because each nonempty role branch is restricted to M or the substantive nonmodal domain while B contains the response fracture that made P supportable, the role branch is evaluated by current I05 without a new validator. Valid-empty, underpowered, noncomparable and authority-limited branches remain explicit receipts.

Only supported `RECURSIVE_SUBGROUP_FORK` receipts are handed to accepted MX01R2. No exact member list is ever supplied by the caller or controller.

## 9. C80/C90 — branch-conditioned other-question enumeration

For each exact branch, enumerate the candidate target catalog from governed source/C11 response surfaces, not caller hints:

1. exact question/component refs queryable in the same source/universe scope;
2. positive response-topology and response-semantic authority;
3. substantive response surface present/lawfully queryable under exact routing/risk-set semantics;
4. exclude the focal anchor surface where the composition law requires another question;
5. exclude demographic/coordinate facts from attitude/cotravel targets;
6. canonical exact-ref ordering;
7. no topic similarity, pairwise score, global correlation, prevalence or prior positive result may prefilter the catalog.

The complete catalog becomes input to the D04 branch-cosignature composition contract. Pair/joint/higher-order frontiers must be sealed before I05 exactly as above. D01 does not preempt D04's detailed topology law.

## 10. C100 — continuation/retention/stop gate

D01 does not invent the D03/HQ continuation law.

Existing I05 terminal coverage states remain binding for one finite frontier. They are not by themselves a complete fracture-map traversal policy.

The controller therefore requires a positive exact law before deciding whether a supported conformer, deviant, converger, minority, residual, stable-minority or split branch is descended, retained terminally, or both.

Until that law exists:

```text
SUPPORTED_BRANCH + MISSING_CONTINUATION_AUTHORITY
-> PRESERVE BRANCH IDENTITY AND RECEIPTS
-> STOP CONTROLLER DESCENT AS UNRESOLVED
```

Never convert budget exhaustion, maximum depth chosen for convenience, underpoweredness, or valid-empty into empirical absence.

## 11. What MX01R2 contributes exactly

Accepted ref: `1773c9a12b3f60489635c562ff60f7190e99a2f5`.

It already proves:

```text
supported RECURSIVE_SUBGROUP_FORK receipt
-> exact winning predicate
-> persisted DiscoveryBranchReplayBinding
-> fresh-process exact membership replay
-> role-bearing N+1 parent atom
```

D01 adds no replacement handoff. The controller merely supplies the missing generation edge:

```text
complete N receipt set
-> governed branch construction/retention decision
-> supported branch handoff
-> generated and sealed N+1 grammar
```

The D01 starting branch does not itself contain `pre553_recursive_handoff.py`; implementation must consume the accepted exact-ref capability under a later authorized integration court rather than pretending the file is already present.

## 12. Whole-map closure

Existing `EmpiricalFact`, `DiscoveryResultReceipt`, `DiscoveryAuthority`, `EmpiricalPredicate`, `ReplayReceipt` and MX01R2 handoff refs preserve the components. They do not currently give the complete branch-role topology one public semantic identity.

The minimum public-output delta, if HQ requires a reusable complete fracture-map product, is one new aggregate receipt family, proposed only for later authority review:

`EmpiricalFractureMapReceipt@1.0.0`.

It should reference existing exact objects rather than copy their empirical payloads. No separate public `ControllerRequest`, `Node`, `Branch`, `FrontierBundle`, `StageReceipt`, or warehouse family is needed.

Until HQ authorizes that family and its branch-role/stop fields, a design/prototype may return only a nonsemantic operational envelope of exact refs and may not claim canonical public whole-map closure.
