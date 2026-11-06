# R11 — physical C11 construction cost reduction

**STATUS:** `PHYSICAL_EVENT_IDENTITY_HASH_REUSED__SRC10_FIRST_MATERIALIZE_REDUCED__FULL_PLAN_HOLD`

**Code:** `3aceba5d6e76a94095507c357d4b4ce38afddaf9` on `codex/pyat-universal35-physical-cost-20261106-r1`; parent `511856ac…` / code `10e22812…`.

## Measured hot path

Existing cProfile of one unchanged SRC10 native package showed `project_c11_candidate_from_physical_cells` at ~51.7 s, dominated by `canonicalize`/`semantic_hash`: 242,603 object initializations, 629,058 semantic hashes, 26.5M canonicalize calls, 854,689 canonical_json calls. Event material is JSON-shaped and was canonicalized three times per event for group ID, event ID, and replay root.

## Smallest physical repair

`pre553_source_backed_c11_facade.py` now hashes the JSON-shaped event material directly (`_fast_json_hash`) for event group/event/replay identity, avoiding repeated semantic dataclass/typing walks. The equivalence test checks the fast material hash against `semantic_hash`; all 29 scale/facade/universal tests pass. No event fields, refs, authorities, topology, states, validation, or release identity semantics changed. Validation still runs fully and no validator/authority check is bypassed.

## Before/after SRC10 first materialization

| Stage | Before | After |
|---|---:|---:|
| first materialization | 169.265 s | 145.998 s |
| project candidate | 51.7 s | 44.503 s |
| validate release | 81.8 s | 73.892 s |
| replay manifest | 4.4 s | 4.313 s |
| total C11 build | 133.6 s | 118.467 s |
| public objects | 242,567 | 242,567 |
| peak RSS | ~1.37 GB | 1.473 GB |

The same SRC10 full path remains compile-bound: prior post-fix run was >425.861 s at the 601.8 s ceiling with 0 facts; no 600 s rerun and no full-scale fact/scale claim. SRC09 first materialize >347 s remains unchanged in status.

## Coordinate/release guardrails retained

- R10 exact expected coordinate rule binding (no regex/name heuristic) and release/replay/authority/closure binding remain.
- A UNKNOWN/MISSING/DEFER states are preserved; actual SRC15 join remains NOT_RUN.
- No A/D/compiler/native-workload/issued/grammar/I03 semantic edits; G owns those files.

## Tests

- 29 scale/facade/universal tests pass (`results/physical_cost_tests.log`).
- Valid release reuse, wrong source/projection, tampered semantic release hash, foreign coordinate ref, and exact UNKNOWN rule cases retained.
- No native/all35/16-GiB/science claim.

## PROGRAMMA_DELTA

`C_PHYSICAL_COST_R11 = EVENT_IDENTITY_FAST_HASH_ACCEPTED_SCOPED__FULL_PLAN_HOLD`: SRC10 first materialization reduced from 169.265 s to 145.998 s with exact validation retained; compile-stage >425.9 s/0 facts remains a separate D/universal-workload dependency.
