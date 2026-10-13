# RFA-06C — controlled three-model screen and Opus comparability constitution

**Existing Opus generation contract:** sealed RFA-06B R2 commit `4ce795413c2e77be04657a260cbda586610f4756`. The official fixture source is RFA-05B `a406e1d289faac31fd51cca8b36a4bb47af93852`. The present correction is **post-generation only**.

## Exact request parity proof

`screen_common.request_for_new(run,c,r2c,transport)` calls **the frozen R2 `court_common_r2.request_for()` directly**, deep-copies its result and changes one scalar: `req["model"]`. It restores that field to the R2 Opus model and asserts byte-identical canonical JSON request equality, including the R2 `required_fixture_id` envelope, fixed transport instruction, entire original semantic `model_payload`, output schema, fixture const, and role-message structure. Both source files' Git blob SHA-1 IDs are pinned against the exact sealed R2 startup. No new referent guidance is included in a model request; the corrected `referent_admission` code runs only after receiving model output.

| Invariant | Resolution |
| --- | --- |
| RFA-05B twenty packets / both arm contents | Original Git blob and compact payload hashes enforced; no edits |
| Current event, world facts, Nadia/relationship context | Inherited packet unchanged |
| Renderer instructions / output semantics | Inherited R2 request bit-equivalent except model ID |
| `required_fixture_id` and transport instruction | Inherited, exactly unchanged |
| Request-specific `fixture_id.const` | Inherited, case binding unchanged |
| Effort, max tokens, system and generation sampling | `high`, 16384, no system, sampling knobs absent |
| Actor/world admission law and RFA-05 scoring rubric | No modification |
| Corrected referent classification | Post-generation only, applies to all three models |

**Comparability disposition:** `EXISTING_OPUS_COMPARABILITY = PASS__NO_OPUS_RERUN_REQUIRED`, contingent on local hash checks succeeding. This does not imply the previously reported Opus substantive scores were independently reproduced in this GitHub-only commission.

## Opus primary and secondary sets

`OPUS_EXISTING_SAMPLE_SELECTION_R1.json` selects **exactly replicate ordinal 1** from each of the ten cases × N/WP conditions, using only the sealed R2 private execution manifest. The selection was made without consulting content, schema validity, scorer ratings, tokens, latency or outcome. The twenty precommitted source `R2RUN-XXXX` IDs form the Opus primary comparison set. Replicates 2 and 3 (forty outcomes) remain a separately labeled secondary replication set, never additional primary weight.

## New screening court

`EXECUTION_MANIFEST_PRIVATE_R1.json`: exactly 20 Sonnet 5.5 calls and 20 Haiku 5.5 calls, one for each of ten cases × two conditions, interleaved across model, case and condition by xorshift32/Fisher–Yates seed `0x5A0C4020`. This seed does not control provider generation. Execution uses `CMRUN-0001` to `CMRUN-0040`. Each model first passes a distinct RF001_N smoke without counting that output in primary estimates.

`BLIND_MAPPING_PRIVATE_R1.json`: independently shuffled with seed `0x5A0C5001`, mapping every selected Opus and new Sonnet/Haiku observation to `BLIND-CM-0001` through `BLIND-CM-0060`. It is private operator custody only. The scorer-visible manifest and output bundles omit model identity, arm, replicate, provider usage, latency, original R2 source ID, and execution order. RF case ID is allowed for exact case-specific substantive review.

## Required offline review and interpretation

The operator must supply the original **60 R2 Opus raw response records locally**, not merely status totals. The build step independently re-evaluates all sixty with the corrected referent contract, writes a private old-vs-corrected diagnostic record, and selects only the predetermined twenty for the balanced blind bundle. The existing R1 diagnostic court is neither read nor included.

After collecting the forty new candidates, build the exact sixty-observation blind bundle and obtain complete 15-dimension RFA-05 rubric scores. Freeze all sixty scores by SHA-256. Only the separate explicit `--unblind` command, after successful hash verification, opens the model×arm mapping and produces model/condition pass rates, failures, rubric distributions, and token/latency receipts. The secondary Opus forty are summarized separately for stochastic stability. No significance claim is made from a 20-per-model screen.

## Claim boundary

The test asks whether a model tier can realize a specific objective Nadia occurrence **conditional on hand-constructed actor/world inputs**. It does not establish future V3, CAN-008/PFF, redesigned V2, full Rawlsing, durable continuity, or personalized phenomenal rendering. A post-generation correction does not demonstrate better model performance; it changes only the mechanical evaluation of references.
