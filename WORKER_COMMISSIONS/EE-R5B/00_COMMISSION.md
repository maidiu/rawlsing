# EE-R5B — A/B/C 27-CELL PHYSICAL ADAPTER REQUALIFICATION

Repository: `maidiu/rawlsing`

Exact grain:
`REQUALIFY_THE_EXACT_3_CANDIDATE_X_9_OPERATION_PHYSICAL_ADAPTER_SURFACE_USING_THE_R4B_EXECUTABLE_OWNER_REGISTRY_AND_ALREADY_READY_COMMON_OPERATION_PROFILES_ONLY`

Library: `NO`.

## Binding inputs

Read current canonical HQ authority from `HQ_HANDOFF/LATEST.json`, then consume exactly:
- EE-R4B exact owner registry return at `e5012ff2d9116e65850402b4432899de4937ed5e`;
- EE-W4 harness and EE-R2E independent harness qualification;
- EE-R3E OP020-OP022 lifecycle profiles at `dd218b1182b29259a19837c89222cbc47024b2ec`;
- EE-R3F common premise freeze at `9082b85d0963c6505e2b9dc9b417cfb881b8cb1b`;
- EE-R3B exact LiTS roots/replay and all current HQ-adopted exact source identities named by current checkpoint.

The exact candidate owners/configurations recovered by R4B are binding. Do not search for alternate A/B/C implementations and do not reconstruct candidate genealogy.

## Exact work surface

Exactly 27 cells:
`{A,B,C} × {OP001,OP002,OP003,OP004,OP005,OP006,OP020,OP021,OP022}`.

For each cell classify exactly one:
- `ADAPTER_READY` — accepted candidate owner already satisfies the EE-W4 harness contract for this operation;
- `BOUNDED_ADAPTER_IMPLEMENTED` — underlying accepted physical capability exists and only mechanical harness translation was missing; implement/test that bridge;
- `PHYSICAL_IMPLEMENTATION_GAP` — satisfying the operation would require new candidate physical architecture or capability rather than mechanical translation;
- `COMMON_PREMISE_BLOCKED` — only if no already-ready exact common premise exists for exercising the operation at all.

## Anti-serialization law

Do not wait on EE-R5A merely to qualify candidate physical capability for OP003-OP006. The LiTS exact OP001-OP006 proving premises are already ready and may exercise the shared candidate-operation transport/capability contract. WVS7 OP001-OP002 are separately ready. OP020-OP022 have exact WVS7 and LiTS lifecycle profiles.

EE-R5A is required for the final WVS real-source OP003-OP006 bakeoff cells, not for proving whether A/B/C can physically execute the operation class.

## Code ceiling

Implement code only when the accepted underlying candidate capability already exists and the missing work is mechanical request/response/config translation into the independently qualified EE-W4 harness.

If satisfying a cell requires a new storage strategy, query engine, semantic rule, persistence model, lifecycle system, accelerator class, or candidate redesign, classify `PHYSICAL_IMPLEMENTATION_GAP` and stop that cell.

Candidate C may use only the exact R4B-permitted CACC1 and CACC2 accelerator surfaces. No extra cache/index surface may be introduced.

## Search ceiling

Start from the exact R4B owner commit:path/blob and immediate dependencies. Historical references may be followed only when the current owner explicitly pins them and only for the cell being classified.

Do not prove absence repository-wide. After inspecting the bound owner, its immediate declared dependencies, and the current harness integration surface, an absent capability may be returned as `PHYSICAL_IMPLEMENTATION_GAP` with searched surfaces named.

## Stop rule

Stop when all 27 cells have one authorized disposition with exact refs and all bounded adapters, if any, have tests. Do not continue exploration for a better architectural understanding.

## Deliverables

- `WORKER_RETURNS/EE-R5B/00_RETURN.md`
- `01_27_CELL_PHYSICAL_READINESS_MATRIX.json`
- `02_ADAPTER_REGISTRY.json`
- `03_TEST_AND_QUALIFICATION_RECEIPT.json`
- bounded adapter/test code only if authorized by code ceiling
- `04_REMAINING_PHYSICAL_GAPS.json`

## Boundaries

Do not run the final equal-work A/B/C bakeoff.
Do not rank or recommend A/B/C.
Do not invent common semantic authority.
Do not weaken the 24-operation denominator or 18-cell selection floor.
Do not modify MAIN or semantic PRE-MAIN.
Do not create a replacement branch.
Do not rebase.

Work through PASS or the smallest exact proved blocker, commit the governed return, and report final branch tip.