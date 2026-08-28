# Z07 — ADAPTIVE EXPLORATORY DISCOVERY RUNTIME / REPLAY R1 — RESULT

Status:

`IMPLEMENTED_CANDIDATE__ADAPTIVE_PARTIAL_SEARCH_RUNTIME_AND_REPLAY_PRESENT__EXACT_I05_UNCHANGED__REPOSITORY_NATIVE_CI_STILL_REQUIRED_FOR_FINAL_HQ_ACCEPTANCE`

Repository: `maidiu/rawlsing`

Worker branch: `agent/verkhovod-z07-adaptive-discovery-r1`

Governing launch ref: `d247e1759eb63927afb6869824b0892e779a3c64`

The checked-in worker command itself names parent Authority-40 HEAD `c649d57c14ca6c0f84571beab4610c007c2484f2`; the user-specified launch ref `d247e175...` is the exact branch tip that added the Z07 command and is the base used by this worker.

## 1. Disposition

Z07 implemented the inherited Long Memory second discovery mode as a **separate adaptive exploratory scheduling/replay service**.

It did **not** make exact I05 adaptive.

`rawlsing_next/pre553_discovery_exact.py` remains unchanged from launch blob:

`b2b99460cc5991bc26aa2ffe5bda129b408fc197`

The new production implementation is:

`rawlsing_next/pre553_discovery_adaptive.py`

implementation commit:

`57193e4d1cd6476d2989323226df2cb40a6f25c3`

production blob:

`58e32770381fa8d901701d6a2c676f28261aa3e3`

The new hostile test surface is:

`rawlsing_next/tests/test_pre553_discovery_adaptive.py`

test commit:

`2fc7404383c4470690f146d63fb9607fbd41e487`

## 2. Inherited function closed by the candidate

Long Memory `LMX-027` requires:

- exact exhaustive authoritative discovery; **and separately**
- deterministic replayable adaptive partial discovery with typed search-completeness state.

D03 classified adaptive exploration as `CURRENTLY_OPEN_FUNCTIONAL_GAP` while exact sealed-frontier I05 was already current-proved.

D06 proved Authority-37 V1 had narrowed away the adaptive-partial mode without any retirement/equivalence proof.

Authority 40 therefore explicitly authorized Z07 as an independent repair.

The new service supplies the missing function candidate without altering the exact mode.

## 3. Adaptive execution model

Contract:

`PRE553_ADAPTIVE_EXPLORATORY_DISCOVERY@1.0.0`

Coverage:

`EXACT_RESULTS__NONEXHAUSTIVE_FRONTIER_COVERAGE`

A run begins from one or more exact root `AdaptiveExplorationUnit`s. A unit is an opaque request whose empirical semantics are owned by its underlying exact evaluator/authority path.

The scheduler:

1. verifies an exact `ADAPTIVE_EXPLORATORY_AUTHORIZED` DiscoveryAuthority;
2. binds a content-hashed search-policy object and exact determinant-state ref;
3. deterministically orders known unvisited units by declared heuristic rank then exact unit ref;
4. executes one unit to a **complete sealed outcome**;
5. only then accepts result-driven proposals for future units;
6. binds every child to its exact parent unit and exact sealed parent-result ref;
7. checkpoints exact visited/unvisited identity;
8. stops with an explicit typed completeness state;
9. can resume from the canonical checkpoint without silently losing known work.

There is no within-unit/adaptive mutation of an open exact I05 frontier.

## 4. Typed search completeness

The service exposes:

- `PARTIAL_BUDGET_EXHAUSTED`
- `PARTIAL_INTERRUPTED`
- `EXPLORATORY_POLICY_FRONTIER_EXHAUSTED`

The first two require explicit known-unvisited territory.

The third means only:

> every unit reachable under this frozen exploratory policy and determinant lineage has been visited.

It does **not** mean:

- no relation exists;
- all lawful exact candidates globally were tested;
- empirical absence is proved;
- a complete authoritative I05 frontier was replaced.

`PARTIAL_SEARCH_NEGATIVE = FORBIDDEN`

The runtime rejects attempts to set a global negative on adaptive outcomes/checkpoints/results.

## 5. Replay and restart

`AdaptiveSearchCheckpoint` canonically carries:

- exact discovery-authority ref;
- exact search-policy ref;
- exact determinant-state ref;
- exact root-unit refs;
- all known unit definitions;
- ordered visit history;
- sealed outcome/proposal material;
- explicit visited and unvisited unit refs;
- typed completeness and stop reason.

Resume fails closed on changes to authority, search policy, determinant state, root universe, or root scheduling material.

`verify_adaptive_replay` re-executes one run and emits public `ReplayReceipt@1.0.0`:

- `REPLAY_VERIFIED` for exact replay;
- `NONDETERMINISTIC_REPLAY` when result/checkpoint/replay identity diverges.

## 6. Search-policy ceiling

The service does not canonize historical V547–V549 coefficients, thresholds or top-k rules.

The minimum implementation uses only:

- an authority-supplied exact integer heuristic rank for search order;
- exact unit-ref tie ordering;
- an exact content-hashed policy mapping;
- explicit maximum generation/frontier-size safety bounds;
- no RNG.

Search rank is not an EmpiricalFact or structural fact and has no downstream actor/V3 effect.

The committed hostile fixture carries explicit `policy_id` and `policy_version`; the entire policy content is identity-bearing, so changing policy/version/heuristic material changes `search_policy_ref` and an old checkpoint cannot lawfully resume. Z07 does not elevate the labels themselves into authority.

## 7. Promotion / semantic-truth ceiling

`AdaptiveUnitOutcome` is a scheduling input only.

It is forced to:

- `global_negative_claim = false`
- `semantic_truth_effect = false`
- `actor_v3_effect = false`

The adaptive scheduler itself creates no empirical fact, structural fact, actor fact, or V3 state.

Any learned result proposed for real use still requires the normal exact empirical validation/authority/promotion path.

`SEARCH_PRIORITY != EMPIRICAL_SUPPORT`

`EXPLORATION != STRUCTURAL_ADMISSION`

`PRE553_DISCOVERY != ACTOR_STATE`

## 8. Relationship to exact I05

Exact I05 remains:

`PRE553_I05_EXACT_BOUNDED_DISCOVERY@1.0.0`

with:

`COMPLETE_FOR_EXACT_DECLARED_FRONTIER`.

Its candidate enumeration is precompiled before the first empirical query and every candidate is terminally covered.

Z07 never imports private I05 frontier/compiler internals and never mutates the exact I05 module.

A lawful integration can use one complete exact I05 invocation as an adaptive **sealed evaluation unit**. After it closes, the exact result can contribute determinant/proposal material for a future unit. Z07 can schedule the future unit; it cannot edit the completed or currently-open I05 frontier.

Thus:

`EXACT_I05_NONINTERFERENCE = PRESERVED`

## 9. Relationship to Authority-37 fracture-map controller

The two functions compose at a process boundary:

```text
SEALED EXACT UNIT / COMPLETE GENERATION
        -> exact result refs
        -> governed result-to-next-frontier / fracture-map proposal logic
        -> exact future AdaptiveExplorationUnit proposals
        -> Z07 deterministic priority/budget/checkpoint/replay
        -> next complete sealed exact unit
```

The Authority-37 controller can therefore originate future lawful work from completed results. Z07 provides the separate inherited exploratory policy/replay layer that decides which future units are visited under a bounded exploratory run.

Neither changes candidate reachability inside an open I05 invocation.

## 10. Hostile test coverage

Committed pytest cases cover all command-required attacks:

1. **budget truncation** — partial state + explicit unvisited refs;
2. **restart** — canonical serialized checkpoint resumes without skip;
3. **reordered storage input** — canonical scheduling is input-order invariant;
4. **partial negative attack** — attempted global negative raises `PartialSearchNegativeError`;
5. **heuristic change/version identity** — search-policy identity changes and old checkpoint resume fails;
6. **exact-mode noninterference** — exact authority is rejected by the adaptive service and exact/adaptive contract IDs remain distinct;
7. **eventual exhaustive completion equivalence** — one-shot and interrupted/budgeted+resumed execution reach the same final visited order/checkpoint/result for a bounded deterministic fixture;
8. additional replay hostility — deliberately unstable evaluator produces typed `NONDETERMINISTIC_REPLAY`.

## 11. Executed evidence and ceiling

An isolated interface-faithful hostile harness for the new service executed:

`8 passed in 0.09s`

That proves the new control logic under the same public shape used by the committed test file, but it is **not** represented as repository-native pytest.

No GitHub commit-status/CI run was available on the test commit when checked. Therefore:

`REPOSITORY_NATIVE_PYTEST = NOT_EXECUTED_IN_WORKER_ENVIRONMENT__NO_PASS_INFERRED`

HQ must run the committed pytest surface in an environment with the repository/runtime available before promoting this implementation candidate to final accepted current successor.

## 12. Mutation audit

Z07 production mutation is bounded to the new adaptive service and its test.

No modification to:

- `rawlsing_next/pre553_discovery_exact.py`;
- existing exact I05 tests;
- C11/source data/database state;
- V553+;
- V3/V2;
- architecture ranking/selection.

Documentary return artifacts live only under the authorized Z07 command directory.

## 13. Final worker holding

`LMX027_ADAPTIVE_PARTIAL_SEARCH_FUNCTION_IMPLEMENTED_AS_SEPARATE_REPLAYABLE_CANDIDATE__EXACT_I05_PRESERVED__FINAL_HQ_ACCEPTANCE_REQUIRES_REPOSITORY_NATIVE_TEST_EXECUTION`
