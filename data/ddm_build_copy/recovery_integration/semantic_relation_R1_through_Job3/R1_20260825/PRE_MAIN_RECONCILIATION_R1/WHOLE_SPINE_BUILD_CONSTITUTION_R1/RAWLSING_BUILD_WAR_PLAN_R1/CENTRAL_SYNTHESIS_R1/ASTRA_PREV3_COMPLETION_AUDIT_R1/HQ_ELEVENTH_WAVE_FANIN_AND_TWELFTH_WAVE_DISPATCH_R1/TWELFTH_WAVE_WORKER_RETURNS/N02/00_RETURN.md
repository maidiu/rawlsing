# N02 — LiTS-I q301 R2/R7/R27 exact record-ID materialization R2 — governed return

Status: `BLOCKED__EXACT_CARRIER_HEALTHY__ACCEPTED_PRE553_DTA_DECODER_BACKEND_UNAVAILABLE__NO_AUTHORIZED_EXTENSION_FREEZE`

Branch: `agent/rabochii-prev3-w12-n02-lits-record-id-materialization-r2`

Commission tip: `69a5dbf0492b618413d39f50d1a7fc251dfa4d34`

Exact grain:

`LITS_I_Q301_R2_R7_R27_EXACT_RECORD_ID_EXTENSION_MATERIALIZATION_R2_ONLY`

## Holding

N02 does not claim PASS and does not freeze R2/R7/R27 extensions from an ungoverned decoder.

The exact commissioned Library carrier was materialized successfully:

- file id: `file_0000000036dc81f8b8b546e356590a03`
- version: `1`
- filename: `LITS-2006-data.dta`
- bytes: `139531180`
- observed SHA-256: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- expected/diagnostically observed rows: `29002`

The frozen identity law remains unchanged:

`(exact source SHA-256, one-based source row ordinal)`

Native `id` is not promoted to a cross-release/person identity.

## Accepted decoder gate

The inherited accepted governed DTA path is:

`rawlsing_next/pre553_physical_decoder.py`

Exact inherited blob:

`13aa733b511dc23e00bfcdf288c5b920e3f09983`

For the commissioned source SHA, its exact compatibility allowlist requires `encoding="latin1"`. Its DTA execution path imports `pyreadstat` and performs raw-value decoding with `apply_value_formats=False`, `user_missing=True`, preserving one-based physical source row ordinals.

On the available execution surface:

- `import pyreadstat` fails with `ModuleNotFoundError`;
- an explicit `pip install pyreadstat` attempt cannot resolve the package index because outbound name resolution is unavailable;
- therefore no accepted `decode_dta(..., encoding="latin1")` scan completed.

This is narrower than M03's prior generic execution-surface blocker: the carrier is present and decodable, but the exact accepted PRE553 decoder backend is unavailable in this sandbox.

Terminal blocker:

`N02_BLOCK__ACCEPTED_PRE553_DTA_DECODER_BACKEND_UNAVAILABLE__NO_AUTHORIZED_R2_R7_R27_EXTENSION_FREEZE`

## Quarantined diagnostic probe — not authority

To isolate the failure from carrier corruption, N02 performed a bounded raw Stata diagnostic using the locally available `pandas.read_stata` reader against only `q301_2` and `q301_7`.

That non-authoritative probe observed:

- q301_2 states `1..5`: `24897`;
- q301_7 states `1..5`: `28325`;
- q301_2 state counts: `1=4377`, `2=6440`, `3=5226`, `4=6972`, `5=1882`, `6=1774`, `7=2327`, system-missing `4`;
- q301_7 state counts: `1=2889`, `2=6112`, `3=6511`, `4=10334`, `5=2479`, `6=224`, `7=442`, system-missing `11`;
- candidate row-ordinal intersection count for `R2 ∩ R7`: `24630`;
- same-input diagnostic replay parity: exact.

Those values are explicitly **not** frozen as Rawlsing materialization authority because they were not emitted by the accepted PRE553 decoder path. N02 therefore does not publish member-coordinate extensions, canonical roots, or a successor-consumable R27 cardinality from this probe.

Exact probe artifact:

`01_EXECUTION_ENVIRONMENT_PROBE.json`

The probe is evidence for the environment blocker only.

## Prohibitions preserved

- zero learned outcomes inspected;
- only q301_2 / q301_7 were read by the diagnostic probe;
- no ranking/discovery;
- no denominator mutation;
- no predictor-missingness rule invention;
- no new identity scheme;
- no semantic recoding beyond the commissioned K03 distinctions;
- no MAIN/PRE-MAIN mutation;
- no OBL063 revival.

## Successor gate

Do **not** treat N02 as PASS and do not wake the learned 50-candidate / 77-role workload from this return.

Re-run this exact worker grain on an execution surface where the accepted PRE553 decoder can import `pyreadstat` and decode the exact commissioned carrier. The successor must then emit exact R2/R7/R27 member-coordinate extensions, canonical content roots, exact R27 cardinality, complete 29,002-row accounting, and fresh same-input replay parity.

FOR HQ: N02 — BLOCKED: exact carrier and identity law are healthy; the remaining blocker is specifically the unavailable `pyreadstat` backend required by the accepted PRE553 DTA decoder. The pandas diagnostic is quarantined and is not materialization authority.
