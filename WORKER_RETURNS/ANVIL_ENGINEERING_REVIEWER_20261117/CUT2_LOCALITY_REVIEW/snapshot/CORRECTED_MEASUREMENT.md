# CUT2 CORRECTED MEASUREMENT TABLE (new canonical)

**Status:** `CANONICAL_CORRECTED_TABLE_SUPERSEDES_STALE_FIELDS`  
**Source:** independent `CUT2_MEASUREMENT_AUDIT/RETURN.md` + `REVIEW_VERDICT.json`; R2 raw frozen at `495796e`.  
**No rerun/product edit/new pair.**

## Aligned positive phases

| Phase | Baseline | Prepared aligned positive | Saving |
|---|---:|---:|---:|
| Wall | **80.624402665 s** | **63.244547212 s** | **17.379855453 s** |
| S index build | **14.377979227 s** | **2.726060945 s** | **11.651918282 s** |
| Q native evaluator | **65.403850167 s** | **60.176479731 s** | **5.227370436 s** |
| O export serialization | 0.019123635 s | 0.017339703 s | 0.001783932 s |
| H admission (outside wall) | 0.272613543 s | 0.287418883 s | -0.014805340 s |

Prepared aligned positive wall = `78.047217121 - 14.802669909 = 63.244547212 s`.  
Prepared aligned positive S = `5.497834365 - 2.771773420 = 2.726060945 s`.  
Q is 95.15% of prepared aligned positive wall; S is 4.31%. This is still one pair, not a qualified speedup.

## Corrected build/scratch and mixed fields

| Field | Corrected value |
|---|---:|
| Producer build external wall | 33.866987348 s |
| Build process-tree RSS peak sampled | 199,135,232 B |
| Build scratch peak sampled | 100,068,948 B |
| External scratch peak (baseline/prepared) | 30,368,896 B / 30,368,896 B |
| Internal session-component peak | 23,269,376 B (not total scratch) |
| Total staging peak | NOT SEPARATELY MEASURED |
| Combined wall | 194.575780673 s |

Do not use prepared aggregate CPU/RSS/row-group reads as matched positive cost: they include the negative/restore phase and have no aligned values. Baseline as-run CPU/RSS are not a phase-aligned substitute.

## Explicit supersessions

- Wall: `80.624 vs 78.047` → `80.624402665 vs 63.244547212`.
- S saving: `8.9 s` → `11.651918282 s`.
- Build: `33.18 / 193,429,504 / 99,941,972` → `33.866987348 / 199,135,232 / 100,068,948`.
- Scratch: `23,269,376 total` → `30,368,896 external sampled; 23,269,376 internal component only`.
- Prepared CPU/RSS/reads: no matched positive comparison.
- Combined wall: top-level null → `194.575780673 s`.

R2 raw and old report remain immutable. Machine table: `CORRECTED_MEASUREMENT.json`.
