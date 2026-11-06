# UNIVERSAL35 C — original selected-package scale and coordinate consumer

**STATUS:** `C_PREBUILT_RELEASE_REUSE_IMPLEMENTED__COORDINATE_RULE_CONSUMER_API_ADDED__FULL_SRC09_10_PLAN_STILL_COMPILE_BOUND__NO_FACTS`

**FINDING:** The actual current D full-plan path is dominated by C11 construction and then by `compile_universal_workload`, not by source decoding or cell projection. On genuine SRC10: decode 1.43 s, bounded stream 0.08 s, `materialize_native_preimages` 169.26 s (first C11 build peak ~1.34 GB), then `compile_universal_workload` was still running at the 600 s ceiling (425.86 s observed in that stage) with **0 facts**. Pre-fix D r7 recorded >650 s/no facts. SRC09 first C11 materialization was still running at 347 s/1.64 GB; not completed.

**INTERPRETATION:** The prebuilt-release reuse is real and connected: the validated release is attached to the selected physical stream, and the existing issued-workload repository build reuses it instead of repeating C11 projection/validation (focused test proves the validation function is not called). It removes the second C11 build, but it does not remove the first C11 build or the compile-stage repeated full projection/catalog envelope work. Those remaining costs are outside this C write lease (`pre553_universal_workload.py`/D consumer) and are a precise residual hold, not a fact-producing success.

**ACTION:** D should pass a shared/prebuilt catalog or batch the F1 workload compilation rather than constructing a fresh full-projection/envelope workload per response value. That is a D/universal-workload change, not a second C engine. C added the coordinate rule consumer hook; D should pass the exact A `build_coordinate_slot_rules(config)` entries once received/qualified. No SRC15 zero-unbound claim is made until that actual join is run.

**OWNER:** D for compile/workload batching; A for coordinate rule producer; C for physical stream/prebuilt release/consumer parameter; independent reviewer for the new consequential scale claim.

## Exact code identity

- Branch: `codex/pyat-universal35-original-scale-20261106-r1`
- Base: D `f295f90f2dc2202055ddf21b575776621260b118`
- Code commit: `8c5e8236ba08dca9d2e5921f938b3ce3d480e3bc`
- Production changes only:
  - `rawlsing_next/pre553_source_backed_c11_facade.py` — prebuilt-release binding/reuse with exact source SHA + projection identity checks.
  - `rawlsing_next/pre553_source_native_preimage_adapter.py` — attach prebuilt release; optional typed `coordinate_rules`.
  - `rawlsing_next/tests/test_pre553_original35_scale.py` — focused tests.
- No A/D/*execution/grammar/kernel/guide/protected edits. No global config/provider/permission change.

## Actual stage receipts

| Stage | SRC10 |
|---|---:|
| source read/decode | 1.431 s |
| bounded physical stream | 0.078 s |
| materialize (first C11) | 169.265 s; 242,567 public objects; 26,951 rows |
| compile_universal_workload | >425.861 s, still running at 601.8 s ceiling |
| peak RSS | 2,074,533,888 bytes |
| actual facts | 0 |

Materialize substage on SRC10: project candidate 51.7 s, validate 81.8 s, replay manifest 4.4 s, total C11 133.6 s. SRC09 materialize hit 347 s / 1.64 GB without completing. Raw trace: `results/full_path_profile_summary.json`, `results/SRC10_materialize_profile.json`, `results/SRC09_materialize_profile.json`.

## Tests

- 28 scale/facade/universal-workload tests passed (`results/scale_tests.log`).
- 3 focused D execution tests passed (`results/d_execution_quick_tests.log`).
- New tests prove prebuilt-release repository reuse without C11 revalidation and exact caller coordinate-rule consumption with typed UNKNOWN states.

## Coordinate consumer

`materialize_native_preimages(..., coordinate_rules=...)` now accepts exact caller-provided `CoordinateSlotRule` values, requires exactly one rule for the selected coordinate, checks the physical ordinal, and uses it instead of the legacy permissive `copy_observed_raw` fallback. Default behavior is unchanged for existing callers; D glue must pass A's qualified rules for SRC15/other coordinates. Actual SRC15 C-adapter join: **NOT_RUN**, no zero-unbound claim.

## Limits

- No genuine native facts emitted; full selected SRC09/SRC10 plan remains `NOT_RUN` after the partial scale fix.
- Full C11/native/science/actor/all35/16-GiB claims remain separate and NOT_RUN.
- No raw respondent rows, native keys or source bytes in Git.
- Independent review required for the consequential scale/coordinate claims; no self-review or protected merge.

## PROGRAMMA_DELTA

`ORIGINAL_SCALE_R3 = PARTIAL_REUSE_ACCEPTED_SCOPED; FULL_PLAN_HOLD`: prebuilt release/repository reuse and coordinate-rule consumer API are implemented; SRC10 600 s path remains compile-bound with no facts; SRC09 materialize >347 s; D must batch/share the compile catalog/envelope and pass exact A coordinate rules. Physical stream remains correct; no probability/denominator/state/provenance/replay change is claimed.
