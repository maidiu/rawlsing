# D01 — FRACTURE-MAP CONTROLLER COMPOSITION DESIGN R1

Status: `DESIGN_COMPLETE__NO_PRODUCTION_IMPLEMENTATION__IMPLEMENTATION_HELD_FOR_HQ_JOIN_AND_NAMED_AUTHORITY_GAPS`

Repository: `maidiu/rawlsing`  
Worker branch: `agent/verkhovod-fracturemap-d01-controller-composition-r1`  
Verified starting HEAD: `8b016afd82f029e5430731ed182b52f70e13575c`

## 1. Dispositive design

The minimum lawful controller is **not** a new discovery engine and is **not** an adaptive version of I05.

It is a deterministic composition layer that performs one missing function:

```text
EXACT GOVERNED RESULT SET FROM GENERATION N
-> GENERATE THE ENTIRE LAWFUL FINITE FRONTIER FOR GENERATION N+1
-> CANONICALIZE + HASH-SEAL THAT FRONTIER
-> BIND IT WITH DiscoveryAuthority@1.0.0
-> HAND THE CLOSED FRONTIER TO UNCHANGED I05
```

I05 remains the exact complete-frontier evaluator:

```text
CONTROLLER_GENERATES_GOVERNED_FINITE_FRONTIER
-> I05_EVALUATES_COMPLETE_FRONTIER
```

not:

```text
CONTROLLER_REPLACES_I05
```

and never:

```text
I05_PARTIAL_RESULTS -> PRUNE/WIDEN/REORDER_CURRENT_I05_FRONTIER
```

The controller may be **result-driven between I05 invocations**. Each individual I05 invocation remains fully predeclared, evaluate-all, fail-closed and replayable.

This directly answers the G02/G05 implementation gap without weakening any proved PRE553 exactness property.

## 2. Exact root object

### Semantic root

Use the existing `EmpiricalQuerySpec@1.0.0` as the exact semantic start object. No new public `FractureMapRequest` object is needed.

The root query must identify one governed substantive response/question surface with:

- exact target question/component refs;
- exact source universe(s);
- exact risk/routing scope;
- exact response topology and response-semantic authority;
- exact measure basis;
- a full governed response domain;
- an exact condition `EmpiricalPredicate@1.0.0` that restricts scope/routing only.

The caller may choose **which question to investigate**. The caller may not supply:

- the modal answer;
- the winning predictor;
- conformer/deviant/converger/minority membership;
- the secondary splitter;
- the next branch;
- a cotravel target chosen because the caller already knows the answer.

Operationally, the controller invocation also receives the exact condition predicate object, exact sealed C11 release refs, immutable `AuthorityRegistry`, and exact controller-law authority refs. This is an argument bundle, not new public ontology.

## 3. How the response surface is generated without answer leakage

The controller first executes the full root/current-branch response distribution through existing I03 exact query execution.

From the resulting exact `EmpiricalFact` cell projection it can mechanically recover:

- every governed substantive response cell/pattern;
- exact raw support;
- governed weighted support where authorized;
- exact typed nonresponse states through separate governed state semantics;
- the exact maximal-cell set under the authorized measure.

Mechanical maxima do **not** silently become semantic `MODAL`, `MULTIMODAL`, `POLARIZED`, `STABLE_MINORITY`, or other shape labels. G05 correctly identifies the higher classification as an authority gap. If the required morphology law is missing, the controller preserves the exact distribution and stops with unresolved morphology rather than inventing M.

For multi-select surfaces the controller generates both:

1. exact response-pattern predicates;
2. response-label presence/absence predicates derived from the exact governed pattern domain.

`A+B` remains distinct from `A_ONLY`; presence marginals never substitute for pattern morphology.

## 4. How predictor candidates are enumerated

The controller derives the positional candidate catalog from existing exact PRE553 coordinate material, not a caller list.

For the exact source/release/universe scope it enumerates all lawfully conditionable coordinate/value predicates supported by:

- `EmpiricalCoordinateFact@1.0.0`;
- exact positive `COORDINATE_SEMANTICS` authority;
- exact positive predicate/operator authority;
- exact source/effective-time/risk-set scope.

The generated catalog is canonical exact-ref/hash ordered.

No candidate is removed because of:

- prevalence;
- MI/NMI/Cramer's V;
- entropy/tree/cloud score;
- a unary screen;
- top-k;
- a prior expectation of which social variable should matter.

This is missing controller code, not a missing empirical carrier.

### Predictor selection

I05 evaluates the complete generated predictor frontier. The minimum zero-loss controller then retains **every** supported predictor candidate.

It does not need to pick a heuristic winner. If HQ later requires the semantic label `PRIMARY` or a priority ordering, that needs the separate predictor/branch-selection law identified by G05 and assigned to D02 recovery. Until then, no supported predictor is discarded merely because another looks stronger.

## 5. Per-node frontier generation and sealing

For every root or discovered branch node the controller builds a finite canonical I05 grammar from:

- the exact current parent predicate;
- the complete governed positional predicate catalog;
- the focal full-response query template;
- exact source/risk/topology/measure scope;
- exact support and validation law;
- authority-declared K/J or other bounds.

Before I05 starts:

1. the complete `candidate_universe_definition` is canonicalized;
2. its content hash becomes the exact `candidate_grammar_ref`;
3. a `DiscoveryAuthority@1.0.0` is instantiated from pre-existing positive authority snapshots;
4. coverage remains `COMPLETE_FOR_EXACT_DECLARED_FRONTIER`;
5. pruning remains `NONE_EXACT_EVALUATE_ALL`;
6. algorithm identity remains current I05;
7. tie order remains canonical candidate-hash order;
8. RNG-controlled reachability remains forbidden;
9. predicate and query-template catalogs are frozen;
10. only then is I05 called.

The controller **instantiates authority-bound semantic objects**; it does not mint governance from empirical results.

## 6. Modal/predictor branch construction

Once a semantic modal pattern M and predictor predicate P are positively governed, Authority35 already supplies the four role relations.

The branch constructor must avoid two semantic leaks.

### Predictor complement must exclude missing coordinates

A bare `NOT P` is too broad because it can absorb respondents whose predictor coordinate is missing/unknown/unconditionable.

Let `CR(P)` mean the exact predicate restricting the branch to respondents with a lawfully resolved conditionable value for P's coordinate.

### Nonmodal complement must exclude nonresponses

A bare `NOT M` is too broad because it can absorb DK/refusal/missing/not-applicable states.

Let `NM` be an explicit `IN` predicate over the exact other **substantive** response patterns for the focal surface.

With B as current parent:

```text
CONFORMER     = B AND CR(P) AND P     AND M
DEVIANT_EXIT  = B AND CR(P) AND P     AND NM
ALT_CONVERGER = B AND CR(P) AND NOT P AND M
ALT_MINORITY  = B AND CR(P) AND NOT P AND NM
```

A substantive `NONE_OF_THESE` pattern remains a real pattern inside NM and may be retained separately. Calling it `CATEGORY_FAILURE` requires separate positive law; D01 does not fabricate that interpretation.

## 7. How branches become exact N+1 parents

D01 reuses accepted MX01R2 exactly; it does not design another handoff.

Accepted exact ref:

`1773c9a12b3f60489635c562ff60f7190e99a2f5`

MX01R2 proves:

```text
supported RECURSIVE_SUBGROUP_FORK receipt
-> exact winning branch predicate
-> persisted DiscoveryBranchReplayBinding
-> exact membership replay after process exit
-> role-bearing N+1 parent atom
```

The controller therefore generates a **branch-realization frontier** containing all Authority35 role predicates as `RECURSIVE_SUBGROUP_FORK` candidates and seals that frontier before I05.

For the ordinary unique-pattern modal fracture case, existing `DISTRIBUTION_DIFFERS_FROM_BASELINE` is sufficient without changing I05: a nonempty M-restricted or substantive-NM-restricted branch differs from a parent distribution that contains the fracture. Empty, underpowered, noncomparable or authority-limited roles remain typed nonpositive receipts.

If the morphology law returns a genuinely multimodal/split state for which a single M/NM partition is not authorized, the controller must **not** force the four-quadrant representation. It stops at the morphology authority gate until the lawful split representation is frozen.

Only supported recursive receipts pass into MX01R2. The caller never supplies respondent membership.

### N+1 generation

For every branch whose continuation law says continue:

1. load the exact MX01R2 handoff;
2. use its exact `recursive_parent_atom(...)` as the next baseline atom;
3. enumerate the full lawful positional catalog again inside that exact parent;
4. generate and seal the complete next finite grammar;
5. call unchanged I05;
6. repeat.

Thus the missing edge is closed conceptually as:

```text
I05_N_COMPLETE_RECEIPTS
-> GOVERNED_CONTROLLER_COMPOSITION
-> MX01R2_EXACT_PARENT
-> SEALED_I05_N+1_FRONTIER
```

## 8. Secondary predictors inside every branch

The same predictor enumerator runs against every supported branch authorized for continuation: conformer, deviant, alternative-route converger, alternative/minority, residual/none, and any other role later authorized by morphology law.

No branch is privileged merely because it is modal. No branch is ignored merely because it is small but supported.

The controller may leave logically redundant candidates in the frontier; I05 can return valid-empty or unsupported outcomes. D01 does not design economics or theorem-pruning.

## 9. Branch-conditioned co-signature target enumeration

The controller must not ask the caller which other question is interesting.

For each discovered branch it enumerates the candidate response-surface catalog from exact governed source/C11 material:

- all lawfully queryable substantive question/component refs in the same exact universe/scope;
- exact topology and response-semantic authority;
- exact routing/risk-set semantics;
- canonical exact-ref order;
- demographic coordinate surfaces excluded from attitude/cotravel targets;
- focal anchor excluded where the co-signature law requires an "other question".

No topic similarity, pairwise association, prevalence, cloud score or global correlation may prefilter the catalog.

That complete catalog is passed to the D04 branch-cosignature composition seam, which owns the detailed pair/joint/higher-order frontier law. D01 does not consume or anticipate a D04 return.

## 10. Continuation, retention and stop

This is the main place D01 deliberately refuses to invent semantics.

I05 already has exact terminal states for **one finite frontier**. Those states do not determine the whole fracture-map traversal policy.

G05 correctly identifies residual continuation/stop as missing authority, and Authority36A assigns D03 to recover it.

Therefore:

```text
SUPPORTED_BRANCH + NO POSITIVE CONTINUATION LAW
-> PRESERVE EXACT BRANCH / FACT / RECEIPT / REPLAY IDENTITY
-> STOP DESCENT AS UNRESOLVED
```

A later law must say what permits:

- continuing a supported residual;
- descending a stable minority;
- retaining multiple parallel branches;
- stopping a supported branch;
- depth termination;
- treatment of split/multimodal branches.

Budget exhaustion or a convenient depth may never be recoded as empirical absence.

## 11. Existing authority vs code gaps vs new HQ law

### Existing authority/capability; controller code/composition missing

- root exact query execution;
- full exact response-cell facts;
- multi-label topology/pattern representation;
- coordinate predicate representation;
- exhaustive positional candidate enumeration from exact coordinate authority;
- per-node grammar canonicalization/hash sealing using existing DiscoveryAuthority/I05 contract;
- exact evaluate-all predictor validation;
- four logical branch-role predicates once M and P are governed;
- exact recursive branch evaluation;
- branch-conditioned I03/I05 facts;
- exhaustive substantive-question target enumeration;
- source plurality/nonpooling guards;
- actor/V3 noncollapse.

### Accepted exact-ref capability not materialized at D01 starting tree

- MX01R2 discovered-child handoff at `1773c9a12b3f60489635c562ff60f7190e99a2f5`.

### Requires new/frozen HQ semantic law before production implementation

1. modal/multimodal/branch-shape classification beyond exact mechanical cell facts;
2. predictor/branch priority or `PRIMARY` selection if the system is to prioritize rather than preserve all supported candidates;
3. continuation/retention/residual stop law;
4. `CATEGORY_FAILURE` interpretation beyond preserving an exact substantive residual response;
5. role-specific determinicity semantic product/metric if more than grouped exact receipt sets is required;
6. whole-map public semantic receipt family and its replay fields if HQ requires one canonical reusable fracture-map identity.

The first three match the authority gaps already identified by G05. D01 does not preempt D02/D03.

## 12. Minimum public object/receipt delta

### Reuse

Keep using:

- `EmpiricalQuerySpec@1.0.0`;
- `EmpiricalPredicate@1.0.0`;
- `EmpiricalFact@1.0.0`;
- `DiscoveryAuthority@1.0.0`;
- `DiscoveryResultReceipt@1.0.0`;
- `ReplayReceipt@1.0.0`;
- accepted MX01R2 `DiscoveryBranchReplayBinding` operational handoff.

### Do not create

No public:

- `FractureMapRequest`;
- `FractureMapNode`;
- `BranchObject`;
- `FrontierBundle`;
- per-stage courier receipt;
- warehouse/table ontology.

### One irreducible public aggregate, pending HQ law

The current public ontology has no object that gives the **whole branch-role topology** one semantic identity. Scattered I05 receipts prove individual candidates, not their governed role composition as a fracture map.

If HQ requires the complete map to be downstream-referenceable/replayable, the minimum new family is one aggregate receipt:

`EmpiricalFractureMapReceipt@1.0.0` — **proposal only, not authorized or implemented here**.

It should contain refs, not copied empirical payloads:

- root query/predicate refs;
- source release refs;
- controller authority refs;
- canonical node identities derived from branch predicate + parent refs;
- exact branch-role labels under positive law;
- node baseline fact refs;
- generated DiscoveryAuthority/frontier refs;
- complete predictor/branch/cosignature receipt refs;
- parent/child topology by exact predicate refs;
- typed continuation/stop states and authority refs;
- unresolved shape/determinicity fields where authority is absent;
- final replay ref and closure state.

No separate public node or branch family is needed.

Until HQ authorizes this family, a controller prototype can only return a nonsemantic operational envelope of exact refs and may not claim canonical public map closure.

## 13. Why this is the minimum lawful composition

It adds no new empirical substrate, no new query algebra, no new candidate validator, no new weighting method, no new recursive carrier, no adaptive pruning algorithm and no actor/V3 semantics.

It composes already-proved capabilities around the one missing control edge:

```text
RESULT -> NEXT GOVERNED QUESTION FRONTIER
```

while preserving the exactness theorem:

```text
EVERY GENERATED FRONTIER IS CLOSED BEFORE I05
AND I05 EVALUATES EVERY CANDIDATE IN THAT CLOSED FRONTIER
```

That is sufficient to distinguish a real autonomous fracture-map controller from the current anti-cheat failure mode where fixtures/callers pre-author the correct splitter, branch, grandchild and cotravel target.

## 14. Frozen oracle compatibility

The design can in principle be tested against G04's already-frozen hostile oracle without leaking its answer into the seed:

- target surface only, not `A+B`;
- coordinate catalog only, not `P`/`Q`/`R`/`S` selected as winners;
- no predeclared four quadrants;
- no grandchild path;
- no preselected `C1/C2` because their branch cotravel is known;
- no caller-supplied respondent membership.

A future implementation acceptance test must reproduce the expected structure through controller generation, not by placing the oracle's answers in candidate grammar fixtures.

## 15. Evidence floor / exact refs

- Authority35 at D01 start, blob `1679d011b8034a49a7a77dc95cda15e7c05e7417`.
- Authority36A at D01 start, blob `808d686287e8feef42d5f8eab1f1da4bd817c1b5`.
- G02 accepted branch tip `191eaaad58d81fb440c8b55964028fcce27c6ad7`; RESULT blob `34ac440a4332c3bfe578e8ef62fecae2351df4af`.
- G05 accepted branch tip `21b4bfbe4f609aeca7a5850a738eff7f663f3ba4`; RESULT blob `f0667321ffc54f3726faacf9ec1576437b74221a`; minimum-delta blob `eb76a4fafd18cdb607f6d99b90fe076e2629563a`.
- G04 accepted branch tip `8620265b95f5b3bf8c210674a7735e0ce8dac88c`; RESULT blob `992a152526acc90caf30c975790923878ed4b15a`; fracture-map oracle blob `8f17d399b46f4ccef0614fbbadf59dab3a089bde`; cosignature oracle blob `fb1c87ac1fb8064d91298678717d697258311ddf`.
- Accepted MX01R2 tip `1773c9a12b3f60489635c562ff60f7190e99a2f5`; RESULT blob `93d957f8926ec73d9603b345794a1421012f66ac`; accepted runtime handoff blob `868f43bf9869af5501fd67c3de7a2703ba4cb1b4`.
- Current D01-start I05 `rawlsing_next/pre553_discovery_exact.py`, blob `b2b99460cc5991bc26aa2ffe5bda129b408fc197`.
- Current public empirical objects, blob `91974c52ce8c0acafa939be0d7d83f4a5c8085b7`.
- Current authority module, blob `6714340facfe186c6cc521884cc85ab6340ad989`.
- Current I03 query module, blob `d81e4ebebaf314ad39b4c56452f9331811c7e3a0`.
- Current predicate evaluator, blob `524043996f21110b25a05f0f08bce056e0fa357e`.

## 16. Noninterference / negative ceiling

This return:

- does not implement production code;
- does not modify I05, I03, C11, MX01R2, V3 or downstream architecture;
- does not select a physical seam or A/B/C carrier;
- does not set thresholds, depth limits, scoring metrics or a selection algorithm;
- does not consume still-running L02/L03 real-data findings;
- does not consume D02/D03/D04 design returns;
- does not call a proposed public object authorized merely because it is designed here;
- does not treat a demographic predictor as attitude, cause, personality or actor belief.

Success token:

`D01_FRACTURE_MAP_CONTROLLER_COMPOSITION_R1_COMPLETE`
