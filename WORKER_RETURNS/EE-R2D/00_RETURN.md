# EE-R2D — ROUTING AUTHORITY BATCH REGISTRY — GOVERNED RETURN

Status: `PASS`

Terminal:
`PASS__EE_R2D_EXACT_159_ACCOUNTED__2_READY_SOURCE_OWNER_UNITS_74_IDS__85_TRUE_UNRESOLVED_NO_OWNER__ZERO_COERCION`

Repository: `maidiu/rawlsing`

Branch: `agent/rabochii-prev3-ee-r2d-routing-authority-batch-registry-r1`

Commission tip verified before execution: `e6e7c8cf5d24a76814d04f63fe9ae6c1d4e6a993`

Exact grain:
`PARTITION_EXACT_159_CLASS_D_ROUTING_RESIDUALS_INTO_FINITE_SOURCE_RULE_AUTHORITY_UNITS_AND_FREEZE_DISPATCH_REGISTRY_ONLY`

Library: `NO__NOT_USED`.

## HQ authority

Read `HQ_HANDOFF/LATEST.json` and followed its immutable checkpoint pointer to:
- checkpoint `20260916T0219-0400`
- handoff commit `d3d96e0c753707ee8615cc25c77d2fcb45adb950`
- semantic PRE-MAIN `1dcd2a79dd6d4208738f655ab7fe4e71c219e354`

The checkpoint explicitly keeps EE-W3's response-semantics/routing closure lane parallel to the Empirical Engine critical path and preserves the law that missing authority is not candidate failure.

## Exact input and partition

The accepted N04-R4B input is exactly **159** unique current routing/applicability residual IDs, all in state `UNRESOLVED_ROUTING_APPLICABILITY_AUTHORITY`.

Input sorted-ID stream SHA-256:
`dfe518e369047eff7978e0a9b1161989cf97c1254ac577479e5c7c38b3671a12`

This registry partitions that exact set without semantic inference:

- **55 GSS IDs** -> `EE-R2D-B01-GSS-B03-SOURCE-SUBSTRATE` -> `READY_FOR_ROUTING_AUTHORITY_COURT`
- **19 WVS IDs** -> `EE-R2D-B02-WVS-B03-W07` -> `READY_FOR_ROUTING_AUTHORITY_COURT`
- **85 exact IDs** -> `TRUE_UNRESOLVED_NO_OWNER` -> held, not dispatched
- `CONFLICTED_OWNER`: **0**
- `OUTSIDE_ROUTING_JURISDICTION`: **0**

Thus `159 = 55 + 19 + 85`, with zero missing and zero duplicate IDs.

## Why the two units are ready

B03 Authority-44 rebinding proves exact source-substrate matches over the complete current GSS/EVS/WVS family slice. Its pinned owner ledger identifies W01 and W02 as GSS source-substrate returns and W07 as the WVS source-substrate return.

N02-R2's one-authority-code-per-current-row ledger independently freezes:
- GSS: `B03-W01 = 3,101` plus `B03-W02 = 2,920`, exactly **6,021**, the full current GSS family;
- WVS: `B03-W07 = 1,219`, exactly the full current WVS family.

Therefore the exact selected GSS and WVS intersections have recoverable competent source-owner sets for a bounded routing-authority court.

This does **not** assert a shared routing predicate inside either batch. GSS W01/W02 is a pinned owner set only. Every court must resolve the exact listed `question_implementation_id` to its exact source-return row and may preserve unresolved.

## Why 85 rows remain true residuals

No competent current source-rule owner is recovered for the other 85 exact selected IDs within the accepted source-authority superseder set:

- B03 is exactly bounded to GSS/EVS/WVS; the selected set contains no EVS rows.
- The exact 11 B04 Authority-44 retained current findings have **zero** ID intersection with the selected 159.
- B05 retained **61** current findings and all are LiTS; the selected 159 contains **zero LiTS** rows.

`TRUE_UNRESOLVED_NO_OWNER` is deliberately narrow: it means no exact competent source routing-document/rule owner is recovered in the accepted current inputs used by this commission. It does not claim that no source document exists anywhere.

## Dispatch graph

The GSS and WVS courts may run in parallel under `NO_ALL_LANES_BARRIER`. The 85-row true residual does not block them and remains held until exact owner recovery.

Any later positive/known ruling may flow to EE-W3's existing generic routing objectizer only after the competent court emits an exact qid-bound ruling. This registry does not objectize rows or create routing semantics.

## Anti-expansion law

- Exact listed IDs only.
- Grouping is not authority.
- Source-owner coverage is not a shared routing rule.
- No borrowing by variable numbering, labels, missingness, adjacency, data, statistics, wave proximity, or family resemblance.
- No unresolved row is converted to applicable, absent/nonapplicable, or outside-jurisdiction by registry construction.
- No MAIN or semantic PRE-MAIN mutation.

## Artifacts

- `01_EXACT_159_ROUTING_ACCOUNTING.jsonl.zlib.b64` — lossless exact 159-row accounting; decoded JSONL SHA-256 `097250444ebea8ee7e5de5926daec4edf2cc1d90a952beb810f3378feb828983`; encoded SHA-256 `c8894dd920dc4a9bfbdf069ce25013c27a3079098b1259790a6e6833183e9cfb`
- `02_SOURCE_RULE_BATCH_REGISTRY.json` — finite batch/authority-unit registry; SHA-256 `3b6a52d5afdf5a6f606c4c7e2baf693d15f85ed5ad10d065378abed50b6bcaa5`
- `03_VALIDATION_RECEIPT.json` — deterministic partition and authority-boundary checks; SHA-256 `f7666856e279d7ef0f5c189de64ce2c6f3f078dc8b739a7a02a4b8d837d4d9fb`
- `04_PARALLEL_DISPATCH_GRAPH.json` — bounded parallel court graph; SHA-256 `40eb5f35baad4ed0e69e1d94fd25d6bd863114cde27aac44c0950b921fb32fa3`

PASS.
