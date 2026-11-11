# EE-R3G — A/B/C candidate adapter readiness

You are **EE-R3G — A/B/C CANDIDATE ADAPTER READINESS**.

Repository: `maidiu/rawlsing`
Library: `NO`.

Exact grain: `MAP_AND_QUALIFY_THE_EXISTING_A_B_C_PHYSICAL_CANDIDATE_IMPLEMENTATIONS_AGAINST_THE_QUALIFIED_HARNESS_INTERFACE_FOR_THE_NINE_SELECTION_CRITICAL_OPERATIONS_ONLY`.

Read current canonical HQ authority from `HQ_HANDOFF/LATEST.json`, then this commission.

Binding inputs:
- EE-R2A selection-critical operation set `6b9b39ddc089033bb5779806a9d08e56be320107`;
- independently qualified EE-W4 harness via EE-R2E `7f7f716ae9cd26bbb1fe5adc7a5ff1024955e285`;
- the exact **current** Route A / Route B / Route C implementation surfaces named by current HQ/common-harness authority;
- common contract and equal-work laws under `PREV3_EMPIRICAL_ENGINE_COMMON_CONTRACT_R1`.

## Finite work unit

The commissioned classification surface is exactly:

`3 candidates × 9 operations = 27 cells`.

Candidates: `A`, `B`, `C`.

Operations: `OP001`, `OP002`, `OP003`, `OP004`, `OP005`, `OP006`, `OP020`, `OP021`, `OP022`.

Every cell must receive exactly one of:
- `ADAPTER_READY` — existing implementation can satisfy the harness request/response/telemetry contract without semantic changes;
- `BOUNDED_ADAPTER_NEEDED` — the physical capability exists and only mechanical harness translation/transport glue is missing;
- `PHYSICAL_IMPLEMENTATION_GAP` — the candidate does not currently implement the required physical capability;
- `WAITING_ON_COMMON_PREMISE` — candidate-independent semantic/oracle input is not yet frozen.

## Search ceiling

Start from the exact current candidate implementation surfaces and the qualified EE-W4/common-harness surfaces named by current authority.

You may follow an additional repository reference **only** when one of these is true:
1. a current candidate implementation explicitly imports, invokes, names, or depends on it;
2. a current authority/receipt explicitly identifies it as the implementation owner for one of the nine operations;
3. the evidence is needed to classify one of the 27 cells and cannot be obtained from the current implementation plus its immediate declared dependencies.

Historical artifacts may be inspected only as bounded evidence for a specific cell. There is **no commission to reconstruct Route A/B/C genealogy**, survey historical architectures, or produce a complete lineage narrative.

Do not broaden from a named implementation into neighboring campaigns merely because their names appear related.

## No proof-of-absence expedition

You are **not** required to prove repository-wide nonexistence of a capability.

For a candidate/operation cell, after inspecting:
- the current candidate implementation surface;
- its immediate declared dependencies;
- the current common-harness/authority refs that claim ownership for that operation;

if no implementation is found, classify `PHYSICAL_IMPLEMENTATION_GAP` and record the exact surfaces searched. **Stop searching that cell.**

Do not recursively search historical branches, superseded campaigns, old packet trees, or semantically adjacent modules in hope that an implementation may exist somewhere else.

## Code ceiling

Implement adapter code only when all of the following are already true:
1. the underlying candidate physical capability exists;
2. the operation's semantic meaning and oracle are already common/frozen or the cell is otherwise ready on common premises;
3. the missing work is only mechanical harness-facing translation, argument plumbing, transport, telemetry normalization, or bounded state-root wiring;
4. the adapter does not change storage strategy, query semantics, persistence policy, invalidation law, source semantics, routing semantics, or candidate architecture.

If satisfying a cell would require a new storage strategy, new query engine, new lifecycle subsystem, new semantic rule, new persistence policy, or redesign of the candidate, classify `PHYSICAL_IMPLEMENTATION_GAP` and stop. Do not build it here.

## Execution rules

For A, B, and C separately, map existing executable components to OP001–OP006 and OP020–OP022.

Where a `BOUNDED_ADAPTER_NEEDED` cell satisfies the code ceiling, implement and test the smallest adapter necessary.

Require identical harness-facing request meaning and telemetry fields across candidates. Candidate-specific optimizations are allowed only behind the same semantic contract; there may be no candidate-specific workload omission, weakened oracle, or semantic shortcut.

Do not implement missing semantic work.
Do not alter the common workload.
Do not run the final A/B/C comparison.
Do not rank candidates.
Do not redesign A, B, or C.
Do not create a replacement branch.
Do not rebase.
Do not modify MAIN or semantic PRE-MAIN.

## Stop rule

**Stop immediately when all 27 cells have one authorized disposition with exact supporting refs, and every lawfully bounded adapter selected under the code ceiling has its tests/receipt.**

Do not continue searching for a deeper understanding, fuller genealogy, more elegant architecture, alternate candidate formulation, or additional optimization after the 27-cell matrix is complete.

Return:
1. the exact 27-cell readiness matrix;
2. exact evidence refs and searched surfaces for each cell;
3. bounded adapter artifacts/tests where implemented;
4. the smallest remaining physical implementation gaps;
5. no architecture ranking or recommendation.

Terminal PASS means the 27-cell readiness question is completely answered at this exact grain. It does **not** mean the final A/B/C bakeoff has run or that a production carrier has been selected.