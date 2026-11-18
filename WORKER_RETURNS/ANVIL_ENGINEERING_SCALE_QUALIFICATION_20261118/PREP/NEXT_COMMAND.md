# NEXT EXECUTABLE COMMAND — SCALE QUALIFICATION PREP

**Input gate:** `FAIL_NO_100K_OR_10K_ESTATE_PHYSICALLY_AVAILABLE`  
**No execution in this prep:** no estate construction, no f4 probe, no heavy/native workload. Existing accepted G5 and prior R2–R5 data are unchanged.

## Missing artifact

- `PREP/fixture_contract_10k.json`
- `PREP/.local-data-10k/releases/<content-id>` and its immutable manifest

No 100k estate was found. The largest physically available sourcefree estate is the 128-respondent/5-question/416-event country-reuse estate; the sealed pilot is 16R/600Q/8,622 events. Neither is a 10k/100k survey-scale estate. Details: `INPUT_MANIFEST.json`.

## One bounded construction command (not authorized/run here)

```bash
SNAP=/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/anvil-scale-68aa7
rm -rf "$SNAP"; mkdir -p "$SNAP"
git -C /Users/matthewsmith/s2b-work/rawlsing archive \
  68aa7cac7cce7057fefd458ef4a06bec2dede1b2 rawlsing_next | tar -x -C "$SNAP"

python3 WORKER_RETURNS/ANVIL_ENGINEERING_SCALE_QUALIFICATION_20261118/PREP/build_10k_estate.py \
  --snapshot "$SNAP" \
  --out WORKER_RETURNS/ANVIL_ENGINEERING_SCALE_QUALIFICATION_20261118/PREP/.local-data-10k \
  --respondents 10000 --chunk-rows 512
```

Build estimate: 10,000 respondents × 5 native questions; expected 32,448 events, 50,000 routing facts, 10,000 weights; retained roughly 164 MB extrapolated from the 128R estate; expected wall 250–350 s, cap 600 s; RSS ≤6 GiB; scratch ≤4 GiB; require ≥8 GiB free. These are estimates, not measurements. This is respondent-scale only, not 600-column width.

## Exact one-run qualification (after build; not run here)

```bash
python3 WORKER_RETURNS/ANVIL_ENGINEERING_SCALE_QUALIFICATION_20261118/PREP/run_scale.py \
  --snapshot "$SNAP" \
  --contract WORKER_RETURNS/ANVIL_ENGINEERING_SCALE_QUALIFICATION_20261118/PREP/fixture_contract_10k.json \
  --out WORKER_RETURNS/ANVIL_ENGINEERING_SCALE_QUALIFICATION_20261118/PREP/EXECUTION/scale_result.json
```

The runner uses exact integrated `68aa7cac...`, one fresh process, one prepared session, and the fixed five distinct operations: `selected_weighted`, `f2_forward_raw`, `f2_reverse_raw`, `f4_three_raw`, `repeated_mr_raw`. No repetitions/matrix, no test-only adapter, no profiler, no native/100k/science/actor/CURRENT acceptance. Caps: native child 600 s, total 900 s, process-tree RSS 6 GiB, scratch 4 GiB, free ≥8 GiB; 0.25 s sampling and process-group abort. The negative/revocation contract is the already accepted G5 suite; this positive scale run does not repeat the hostile court.

## Source pins

- integrated executable `68aa7cac7cce7057fefd458ef4a06bec2dede1b2`
- integrated G5 `d74b641f8ec0c3a94da8ea90e9f5e7b5dc97a0ab`; receipt SHA-256 `cf70adfc85f2e3ff770b0dc10273b841314c204250d14a5c2d271e590c9909c7`
- product blobs: `pre553_direct_estate_i03.py` `d662fc578a1ecb42d54ec8b4bdab87fd7ecec176`; `pre553_source_postconsumer_receipts.py` `0a2e7b899ebd392761d38b8ceb175f0bf81c6378`
- fixture pins: `fixture_1006.py` `1487ad233c871d973b2a64c9649c37f100c46832`; `query_1006.py` `5a15272043246e5293a51e2390adc038bd280e47`; `court_instrumentation.py` `5f2b424b198ac2242b9a4bf0028b64afde25d6a8`

See `SOURCE_PINS.json`, `INPUT_MANIFEST.json`, `RESOURCE_GATE.json`. No production edits, no source/native/science/actor/CURRENT/protected grant.
