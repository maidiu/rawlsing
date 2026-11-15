# Open questions and finite uninspected territory

## Exact missing / uninspected sources

- Historical run logs, shard manifests, row counts, wall times, RSS, I/O: **not found in this
  pass**, not requested broadly. `HISTORICAL_RUNTIME_UNKNOWN`.
- Original output parquet/csv rows were not read (raw governed respondent bytes prohibited).
  No old product row was verified to exist for any inspected producer.
- V551J packet/certification internals, V552J join semantics beyond the handoff call site, and
  any real V553 reader: `NOT_INSPECTED`.
- V550J association registries, thresholds, lane overrides, full family compiler beyond the
  inspected counting/MI block: `NOT_INSPECTED`.
- V549 `v547`/`v548` upstream tree genesis and whether real trees ever used blanked demographic
  predictors: `NOT_INSPECTED`; the code-path defect is proven, executed effect is not.
- `build_determinicity_repository_v550.py` `_question_rows` fallback SQL details and
  `_harmonize_question_frame` semantics: partially inspected only.
- Modern merged #684/#686/#707, S2-C/D D13 families, `_pre553_query_eval.py` at `3e0ed...`,
  W05/P03 cost court, #1006 R2 logs: `NOT_INSPECTED`. The 543.026→294.087 s claim is intake only.
- Other investigator's checkout/runtime and VOSKRES branch: deliberately not read.

## Claims that remain inference, not observation

- V552 unused conditional-determinicity parameter: proven in this file; another caller may
  post-process the index elsewhere.
- V549 blank-demographic masks: code-path inference; no tree was executed.
- Pooled distribution labelled country: latent when a multi-country frame reaches the function;
  actual shard country scoping was not traced end-to-end.
- V550J "MI" mislabel: proven for the inspected association branch; other lanes may differ.
- Modern `pre553_diagnostics` is diagnostic-only by its own guard (`:606`); this does not prove
  whether any current consumer uses it scientifically.

## Questions for bounded reconciliation

1. Did V551J actually read `conditional_determinicity_index`, or was it always a terminal
   side-product? Which exact V551J artifact/row field would consume it?
2. Did any V552/V552J path consume old `recursive_branch_nodes` or `secondary_indicator_summary`
   outside the bridge lane classification? Which artifact?
3. What were the actual V550 historical wall times/resource metrics and per-question checkpoint
   counts? Are any logs present under a different historical path?
4. Does the current grouped I03 core preserve ordered same-person components and multiple
   denominators end-to-end to a real consumer, or only in test scope?
5. Which modern owner, if any, is required to receive the conditional determinicity function:
   diagnostics, S04, or an explicit retired status?
6. Are old V549/V549b branch summaries evidence of real scientific splits, or artifacts of blank
   predictors? Needs v548 tree predictor inventory and one non-governed synthetic check only if
   authorized in a later tract.
