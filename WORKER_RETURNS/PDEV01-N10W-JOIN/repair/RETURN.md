# PDEV-01 — J42 receiver identity repair

**Status:** `CANDIDATE__TEST_ONLY__INDEPENDENT_REVIEW_REQUIRED`  
**Engineering:** `PASS_SCOPED_REPAIR__J42_EXACT_IDENTITY_GUARD`  
**Source science:** `HOLD`  
**Authority:** `HOLD`

Repair base: `30b04c762bc4edd5e2e672d8d76b1e6e4ff84190`  
Branch: `agent/pyat-pdev01-n10w-join-r1`  
Overlay: `WORKER_RETURNS/PDEV01-N10W-JOIN/repair/`

## Repair

`guarded_receiver.py` validates the actual J42 receipt before invoking the unchanged existing receiver:

- exact P41 schema/service;
- exact existing J42 provider identities:
  - `W41_READONLY_SOURCE_QUALIFIED_WORLD@1`
  - `E41_N10E_EMPIRICAL_POSSIBILITY_SLICE_PROVIDER_EXT@1.1.0`
  - `P41_GENERIC_POSSIBILITY_SERVICE@1`
  - `E04L_M1_M2_B5_READTHROUGH@1`
- exact `CURRENT_TEST_ONLY_SELECTION` N9 currentness;
- exact selected-clock binding between `n9_world.selection` and `j42_bindings.w41_clock`;
- recomputed P41 `content_hash` from the existing `semantic_hash` contract;
- then delegates to the actual existing `select_joined_world_view`.

No production code, provider, science rule, source, trust issuer or R05 substitution was introduced.

## Actual positive and cold replay

The guard accepted all **84 actual J42 views**, not just the selected example.

- Positive state: `SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER`
- Reason: `WORLD_SELECTED_VIEW`
- Positive view hash: `062c4c5fc59c5618582d43f9e4c917ab97a32ecfd7249d5bfba2824fe0767287`
- N10E steps: 3 `EXACT_SUPPORTED`
- N10W state: `EXACT_PROGRESSIVE_CHAIN`, 3 live consumptions
- N9/W41, N10E/E41 and N10W/P41 provider identities exact
- Source rows: `4320b3a505478c274fc756ce0e025e36685e0742e940072aae80ce11286e4c02`
- Cold receipt pair: parent `J42_RECEIPTS.json` and `J42_RECEIPTS_2.json` are byte equal (`c54b215bb03bba391571b4c51357831b14f256b7c4c6eec98d85dd9bda30eebf`)
- All 84 cold view hashes equal the first build; `all_cold_view_hashes_equal: true`

## Rejections

All five recorded mutations were rejected even after recomputing the P41 hash:

| Mutation | Guard result |
|---|---|
| wrong N9 provider version | `JOINED_PROVIDER_IDENTITY_MISMATCH` |
| wrong N10E provider version | `JOINED_PROVIDER_IDENTITY_MISMATCH` |
| wrong N10W provider version | `JOINED_PROVIDER_IDENTITY_MISMATCH` |
| revoked N9 currentness | `JOINED_N9_CURRENTNESS_INVALID` |
| mutated N9 selected clock | `JOINED_N9_SELECTION_MISMATCH` |

Additional controls:

- stale P41 hash → `JOINED_RECEIPT_CONTENT_HASH_MISMATCH`
- missing N9 provider → `JOINED_PROVIDER_IDENTITY_MISMATCH`
- missing N10E steps → `JOINED_CONSUMER_NOT_PRODUCTIVE`
- missing P41 or joined receipt → `JOINED_VIEW_NOT_FOUND`
- missing second field → `WORLD_REQUIRES_AT_LEAST_TWO_FIELDS`
- wrong source rows → `JOINED_SOURCE_ROWS_MISMATCH`
- wrong as-of → `JOINED_AS_OF_MISMATCH`
- R05 provider substitution → `JOINED_PROVIDER_IDENTITY_MISMATCH`

## Exact command

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-n10w-join
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH="WORKER_RETURNS/PDEV01-N10W-JOIN/repair:$PWD" \
python3 WORKER_RETURNS/PDEV01-N10W-JOIN/repair/run_guard_checks.py
```

The replay uses the existing parent `J42_RECEIPTS.json`, `J42_RECEIPTS_2.json`, `VERSION_AND_IDENTITY_NEGATIVES.json` and `R05_P41_TRACE.json` as read-only inputs.

## Hashes and pins

- `guarded_receiver.py`: see `PINS.json`
- `run_guard_checks.py`: see `PINS.json`
- `GUARD_WITNESS.json`: see `PINS.json`
- J42 provider source `runtime/j42_join.py`: `4bab407129b1b385585f287b948bcde4d5ffaa4affe53b78cefdf6c6c981b399`
- J42 provider source commit: `f53cb0d2bce52640268c844c398bbd8007d28edc`
- P41 runtime: `f27d1101048638bba395143a48efb7ef00bfcda4`
- W41 returned artifact: `b0a68e4ff5d5e2ca62b080376fda6b5f5431a6c2:WORKER_RETURNS/PYAT-R41-W41-OBJECTIVE-WORLD-R1/current_historical_asof_world_consumer_receipts.json`
- W41 artifact SHA-256: `09a92d6c00e867a44712b225cadd352b7d41a2038384de26de34f5c10a9185e7`
- Parent positive receipt SHA-256: `c54b215bb03bba391571b4c51357831b14f256b7c4c6eec98d85dd9bda30eebf`

## Limits

TEST_ONLY sourcefree W41/E41/P41 values and synthetic E04 rows. N9 currentness is `CURRENT_TEST_ONLY_SELECTION`, not operative N9/CURRENT. No original source/respondent read, original science, N5/N6/EE13, N9/OC05, N11/N12, actor/Sorok, CI/prod, protected merge, production edit, or authority expansion. The production receiver remains unchanged; this is an isolated candidate overlay only.

**Next:** distinct nonauthor review of this repair and its actual replay. The author does not self-accept.
