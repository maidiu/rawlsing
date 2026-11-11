# Harness method repair

## Before

```text
project_c11_candidate_from_physical_cells
 -> validate_c11_source_release
 -> _compact_public_objects
 -> C11Repository
```

This skipped `build_source_backed_c11_repository`'s actual streaming-cold + governed-cache path. `cache_hit` was `ParquetC11Carrier.reopen`, not the derived accelerator.

## After

```text
ExactPhysicalCellStream
 -> build_source_backed_c11_repository(..., current_authorities=...)
 -> normal streaming cold
 -> actual I02/C11 validation + seal
 -> attach_governed_cache(policy, key, envelope)
 -> derived c11-events-*.parquet
 -> real CarrierNeutralResearchExecutor I03/I05
```

Canonical path is separate:

```text
ParquetC11Carrier.persist / reopen -> releases/<source>/<release>/<semantic>/*.parquet
```

Derived file and canonical release files are never conflated.

## Instrumentation boundary

- `profile_setup`, lazy `cells`, `normal_current_cold_build` and `cold_combined` are measured with process RSS/wall/CPU.
- The current public normal caller does not expose separate public boundaries for projection/object construction/canonical hash/I02 validation/seal/compact. Those are explicitly marked `COMBINED_INSIDE_NORMAL_CURRENT_COLD_BUILD__NO_PUBLIC_SEPARABLE_BOUNDARY`; no invented zero-cost or missing peak claim.
- `decode` is explicitly `NOT_APPLICABLE__EXACT_PHYSICAL_CELL_STREAM__NO_SOURCE_DECODE`, not a fake measured cost.
- `canonical_persist`, `canonical_reopen`, `derived_cache`, and `firstconsumer` are separately recorded.
- `method_overhead_seconds` records policy/root setup.
- Observational wrappers do not change return values or production semantics.

## Preserved prior evidence

`c44cf09f` remains the prior preintegration benchmark return. Its 100000 narrow result (current 46b 5,923,426,304 B vs protected 4f3413 5,240,467,456 B, +13.0% RSS; 777.53 s vs 997.04 s) is retained as **diagnostic RED**, not overwritten or relabeled as candidate proof.
