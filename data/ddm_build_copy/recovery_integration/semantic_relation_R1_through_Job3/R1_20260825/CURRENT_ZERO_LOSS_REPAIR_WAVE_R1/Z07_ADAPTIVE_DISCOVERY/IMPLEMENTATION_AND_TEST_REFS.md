# Z07 IMPLEMENTATION AND TEST REFS R1

## Governing inputs

- Worker launch ref used: `d247e1759eb63927afb6869824b0892e779a3c64`.
- Authority 40: `c649d57c14ca6c0f84571beab4610c007c2484f2`; authority blob `6b8a4449b4c5304d122231848b07880ac4858cf4`.
- D03 learned-world succession: `fa6ea6c957bd350b31e5adb504dbb854a0464dfa`; RESULT blob `70bd5c5877437dbc9738fa138339d897b5b83ed4`.
- D06 branch/stranding succession: `93e84b084f14db2db410cbad5555e7820507d4d9`; RESULT blob `e73b9b8df9f08ac8bcc121b1a8bf877f3f0aa629`.
- Long Memory terminal baseline: `669062e6c319f31214f403939dded91300639bde`.
- Long Memory 44-row ledger blob: `0ae29caa6b3c572b2cedf39bebfa737668ebfb5b`.
- Long Memory closure-result blob: `5312d04780c45400a6a38205c475ad6e42eeef88`.

## Preserved exact I05

- Path: `rawlsing_next/pre553_discovery_exact.py`
- Start blob: `b2b99460cc5991bc26aa2ffe5bda129b408fc197`
- Contract: `PRE553_I05_EXACT_BOUNDED_DISCOVERY@1.0.0`
- Z07 action: **none**. The file is absent from the Z07 diff.

Existing exact-mode test path remains:
- `rawlsing_next/tests/test_pre553_discovery_exact.py`
- inherited blob at launch: `308a582c012f20824bc2dceb530b1c9652395f93`.

## New production implementation

Commit:
`57193e4d1cd6476d2989323226df2cb40a6f25c3`

Path:
`rawlsing_next/pre553_discovery_adaptive.py`

Blob at implementation commit and current content before documentary returns:
`58e32770381fa8d901701d6a2c676f28261aa3e3`

Primary public surface:
- `ADAPTIVE_DISCOVERY_CONTRACT_ID`
- `ADAPTIVE_SEARCH_COMPLETENESS_CONTRACT`
- `AdaptiveExplorationUnit`
- `AdaptiveUnitOutcome`
- `AdaptiveVisit`
- `AdaptiveSearchCheckpoint`
- `AdaptiveSearchResult`
- `execute_adaptive_exploration`
- `verify_adaptive_replay`

Typed completeness states:
- `PARTIAL_BUDGET_EXHAUSTED`
- `PARTIAL_INTERRUPTED`
- `EXPLORATORY_POLICY_FRONTIER_EXHAUSTED`

Errors include:
- `AdaptiveDiscoveryError`
- `AdaptiveSearchIdentityError`
- `PartialSearchNegativeError`

## New hostile tests

Commit:
`2fc7404383c4470690f146d63fb9607fbd41e487`

Path:
`rawlsing_next/tests/test_pre553_discovery_adaptive.py`

Eight committed hostile cases cover the command-required surfaces:

1. budget truncation;
2. result-driven widening between sealed units;
3. restart + reordered initial storage + eventual exhaustive completion equivalence;
4. interruption/restart without silent candidate loss;
5. deterministic replay and typed replay divergence;
6. heuristic policy-version/content identity change;
7. partial valid-empty negative attack;
8. exact-mode noninterference / mode separation.

## Executed evidence

Isolated hostile harness:
`8 passed in 0.09s`

This was an interface-faithful isolated execution of the new service contract and is intentionally not represented as repository-native CI.

Repository-native pytest / GitHub CI:
`NOT_EXECUTED_IN_WORKER_ENVIRONMENT__NO_PASS_INFERRED`

No GitHub commit statuses were present on the committed test tip when checked.

## Exact relationship to I05 and fracture-map controller

Z07 is a scheduling/replay service around complete sealed evaluation units, not a replacement evaluator.

When a sealed unit is an exact I05 execution:

- I05 compiles its full finite candidate frontier before empirical evaluation;
- I05 evaluates every candidate under exact authority;
- Z07 cannot change that open frontier;
- only after the sealed result exists may a governed controller/proposal producer derive future exploration-unit proposals;
- those proposals bind exact parent-unit and sealed-parent-result refs;
- Z07 may then reorder/reach future units under its exploratory policy and explicit budget;
- partial/unvisited units remain unknown.

Authority-37 result→next-frontier controller therefore supplies a lawful proposal/composition role **between** sealed discovery generations/units; Z07 supplies exploratory prioritization, checkpointing, restart and replay for those future units. Neither service gains semantic truth authority from search order.
