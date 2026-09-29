# PYAT C3-02 — CURRENT-BASELINE PHYSICAL REPAIR INTEGRATION — R1

Status: ISSUED__USER_MEDIATED_BROWSER_SOL_HIGH_LAUNCH_REQUIRED

Role: Browser GPT-5.6 Sol High sole physical integrator

Branch:
`agent/rabochii-pyat-hq126-c3-02-physical-repair-integration-r1`

Exact implementation base:
`b3b2fa13049513078c301a1f6574b661fcf390c5`

Accepted C3-01 return:
`d9462674d45f228b5985a5ce3158723b87ca6fa6`

Independent approval:
`f8f152c60747a6146e92539a36af76ddc97a8d23`

Overall independent disposition:
`APPROVE_AT_DECLARED_GRAIN`

## Mission

Port only the independently accepted G01, D01 and D02 repairs onto the exact current baseline.

Do not replace the current decoder with a historical snapshot.
Do not use raw survey sources.
Do not widen source applicability or semantic authority.
Do not edit the source-backed C11 facade.
Do not resurrect historical census harness/receipt infrastructure.

## Frozen semantic grains

G01:
`EXACT_NINE_SURFACE_SAV_NATIVE_INT_RULE_TO_FLOAT64_PHYSICAL_REPRESENTATION_SUCCESSOR`

D01:
`EXACT_SOURCE_SHA_PLUS_DECLARED_ENCODING_PHYSICAL_DECODER_ADMISSION`

D02:
`EXPLICIT_OPAQUE_DECODER_NATIVE_NAIVE_DATE_TIME_CARRIER__REPRESENTATION_ONLY`

## Exact semantic implementation allowlist

### ADD
`rawlsing_next/closed35_g01_sav_numeric_representation_authority.py`

Only the accepted finite nine-surface G01 authority at semantic-equivalent content grain.

### MODIFY
`rawlsing_next/pre553_physical_decoder.py`

D01 only:
- add `SOURCE_DECLARED_ENCODING_ONLY` physical-only status;
- add exactly these three SHA→encoding declarations:
  - `ac0b8bc1ddb2fa6b952417e35b6379ce6a2cf8596776a43282ba44f48e0ae1a2 -> BIG5`
  - `5b703173845c086382fd93252f1cbc91dfef74007755459adfc73785389172f2 -> WINDOWS-1252`
  - `66252a92c59bf6759b79a6b35b2be658b98a433373212a70c8ec94755d3e02ec -> WINDOWS-1252`
- extend the current compatibility-config path with that exact declared SHA+encoding branch;
- preserve existing compatibility behavior and fail-closed guessing;
- export only required constants.

D02 only:
- import `normalize_decoder_physical_value`;
- add narrow `_physical_value` handling for exact naive built-in `date`, `datetime`, `time`, including item()-unwrapped exact native types;
- route physical-cell raw-value capture through `_physical_value`;
- preserve all intervening current decoder behavior.

### MODIFY
`rawlsing_next/pre553_r5_codec.py`

D02 only:
- import datetime support;
- add `opaque_decoder_value` for exact built-in naive date/datetime/time;
- add recursive `normalize_decoder_physical_value`;
- export only required helpers.

## Exact test allowlist

### ADD current-baseline port
`rawlsing_next/tests/test_closed35_g01_sav_numeric_representation_authority.py`

Do not import/copy absent historical receipt trees. Encode the already-frozen independent nine-surface oracle in current-baseline fixtures/references and retain all hostile noncoercion cases.

### ADD
`rawlsing_next/tests/test_closed35_d01_declared_encoding_admission.py`

Exact accepted D01 hostiles only; no extra source/encoding ALLOW.

### ADD current-baseline port
`rawlsing_next/tests/test_closed35_d02_opaque_datetime_carrier.py`

Do not import or restore `closed35_representation_census_harness.py`.
Retain:
- exact type/field identity;
- bare-R5 rejection;
- timezone-aware rejection;
- string-masquerade rejection;
- decoder-route hostile cases;
- direct compatibility assertion that the unchanged facade can bind the resulting `R5OpaqueValue`.

## Explicitly forbidden edits

- `rawlsing_next/pre553_source_backed_c11_facade.py`
- `rawlsing_next/closed35_representation_census_harness.py`
- historical CLOSED35 qualified-census receipt trees
- raw source files/payloads
- source/question/structural semantic authority
- generic int/float canonicalization
- encoding guessing/fallback
- date/time semantic interpretation

## Required source-free qualification

On the exact current-baseline-derived semantic candidate, run together:

1. the three C3-02 current-ported repair tests;
2. `rawlsing_next/tests/test_fiabc_lm2_r1j_sav_representation_authority.py`;
3. `rawlsing_next/tests/test_r35_i01_physical_metadata.py`;
4. `rawlsing_next/tests/test_pre553_source_backed_c11_facade.py`.

Also explicitly prove:
- D01×D02 shared-decoder composition on the current decoder;
- G01 wrong type/source/variable/ordinal/code rejects;
- D01 wrong SHA/wrong encoding/unknown SHA/guess/fallback/None-no-authority behavior;
- D02 bare date-time/tz-aware/string masquerade/type-field collision rejects;
- unchanged facade compatibility.

Preferred execution route is the repository's PR-triggered Rabochii Governed Bounded Court if needed.

If using that governed court, keep the semantic candidate SHA separate from any execution-only commit whose only permitted delta is:
`.rabochii/court_spec.json`.

Do not call unexecuted cases PASS.

## Return terrain

Production/test writes only to the frozen allowlist above.

Documentary return:
`WORKER_RETURNS/PYAT-C3-02-PHYSICAL-REPAIR-INTEGRATION-R1/**`

Return:
- `00_RETURN.md`
- `01_IMPLEMENTATION_MANIFEST.json`
- `02_CURRENT_PORT_DIFF.json`
- `03_QUALIFICATION_RECEIPT.json`
- `04_HOSTILE_CASES.json`
- `05_REMAINING_OBLIGATIONS.md`

Report exact:
- semantic candidate SHA;
- changed blobs;
- execution SHA if distinct;
- runtime/workflow/job/attempt;
- commands/tests;
- pass/fail/error/skip counts;
- source-access declaration;
- unchanged facade blob identity.

Terminal target:
`C3_02_CURRENT_BASELINE_REPAIRS_INTEGRATED_AND_SOURCE_FREE_QUALIFIED__READY_FOR_INDEPENDENT_REVIEW`
