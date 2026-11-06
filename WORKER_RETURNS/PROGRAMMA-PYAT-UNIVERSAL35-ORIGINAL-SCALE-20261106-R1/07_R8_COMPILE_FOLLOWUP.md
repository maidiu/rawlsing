# R8 — repeated full-compilation follow-up

**STATUS:** `C_PREBUILT_RELEASE_REUSE_AND_COORDINATE_HOOK_IMPLEMENTED__COMPILE_STAGE_STILL_HOLD__NO_FACTS`

**Code:** `8c5e8236ba08dca9d2e5921f938b3ce3d480e3bc` (unchanged from scale fix). No new code was added for the compile-stage hold because the remaining repeated work is in `pre553_universal_workload.compile_universal_workload` / its issued-workload helper, not in the physical adapter or C11 facade. The existing C lease now includes that file only for measured duplicated compilation; no safe repair was connected without changing issued workload identity.

## Actual bounded measurements

| Stage | SRC10 |
|---|---:|
| source decode/read | 1.431 s |
| bounded physical stream | 0.078 s |
| first materialize/C11 | 169.265 s; 242,567 public objects; 26,951 rows |
| compile_universal_workload | >425.861 s, still running at 600 s ceiling |
| total/peak | 601.816 s; 2,074,533,888 B |
| facts | 0 |

SRC09 first materialize was still running at 347.332 s / 1,636,061,184 B; no completion. Materialize substage SRC10: candidate 51.7 s, validation 81.8 s, replay 4.4 s, total C11 133.6 s. Raw: `results/full_path_profile_summary.json`, `results/SRC10_materialize_profile.json`, `results/SRC09_materialize_profile.json`.

## Bottleneck attribution

- Prebuilt-release reuse removes the second C11 repository rebuild (focused reuse test; existing issued-workload path consumes the attached release).
- It does not remove the first C11 build (materialize) or the compile stage.
- SRC10 has 10 compiled F1 response values; `compile_universal_workload` builds a projection catalog and a full issued workload/envelope per value over the same unchanged bundle. The stage exceeded 425 s before the ceiling and emitted no facts.
- This repeated work is outside the physical adapter/facade; changing it requires the measured compile/workload sharing repair in the new lease. No compatible shared-catalog API was already wired.
- SRC09 first C11 materialization alone exceeded 347 s; this is a separate scale ceiling.

## Coordinate consumer

`materialize_native_preimages(..., coordinate_rules=...)` retains exact caller-provided `CoordinateSlotRule` support, ordinal/name checks, and typed UNKNOWN/MISSING preservation. The legacy default remains; actual SRC15 join is **NOT_RUN**, no zero-unbound claim and no age semantics inferred.

## Tests and limits

- 28 scale/facade/universal tests PASS; 3 focused D execution tests PASS; logs in `results/scale_tests.log`, `results/d_execution_quick_tests.log`.
- No genuine facts emitted on full SRC09/SRC10; no all35/native/science/16-GiB claim.
- No A/D/grammar/I03 semantic edits; no protected merge/review substitution.

## PROGRAMMA_DELTA

`ORIGINAL_SCALE_R8 = PARTIAL_PHYSICAL_REUSE_PLUS_COORDINATE_HOOK__COMPILE_HOLD`: prebuilt release and coordinate rule API are delivered; the full selected plan remains blocked by repeated per-value compile/catalog/envelope work and first-C11 scale. Next owner is D/universal-workload sharing; C physical cleanup is exhausted at this measured point.
