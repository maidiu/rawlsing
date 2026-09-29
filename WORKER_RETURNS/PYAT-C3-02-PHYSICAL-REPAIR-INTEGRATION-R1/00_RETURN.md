# PYAT C3-02 — current-baseline physical repair integration — R1

Status:

`PASS__CURRENT_BASELINE_G01_D01_D02_PORT__SOURCE_FREE_QUALIFIED`

Repository: `maidiu/rawlsing`

Assigned branch:
`agent/rabochii-pyat-hq126-c3-02-physical-repair-integration-r1`

Commission tip:
`e1420435591d727f48b7a4d5964709f87fcf5a4f`

Exact implementation base:
`b3b2fa13049513078c301a1f6574b661fcf390c5`

Accepted C3-01 return:
`d9462674d45f228b5985a5ce3158723b87ca6fa6`

Independent approval / frozen allowlist:
`f8f152c60747a6146e92539a36af76ddc97a8d23`

## Final identities

Semantic candidate:

`31fd2f4b7c7c2cdf72bed295b7cb5ca94528349f`

Execution-only qualification commit:

`a26279dfad85ddc2a37f7cb396094da308bc58e4`

The final candidate differs from the commission tip only in the six frozen semantic/test paths. The execution commit differs from that candidate only in:

`.rabochii/court_spec.json`

The current source-backed C11 facade remains byte-identical:

`8a761119e4a8d68eb291fc4edfadb52e027f8284`

The historical CLOSED35 census harness and qualified-census receipt tree were not resurrected.

## Ported repairs

### G01

Ported only:

`EXACT_NINE_SURFACE_SAV_NATIVE_INT_RULE_TO_FLOAT64_PHYSICAL_REPRESENTATION_SUCCESSOR`

The accepted authority module blob is:

`31a9afd7d91ed4cb2fb1c1aab3ef86a5fdda1f85`

The current-port test freezes the already-accepted nine-surface oracle directly and does not import historical receipt infrastructure.

No generic int/float equivalence was introduced.

### D01

Ported only:

`EXACT_SOURCE_SHA_PLUS_DECLARED_ENCODING_PHYSICAL_DECODER_ADMISSION`

The current decoder moved from:

`d2a074a41fb556a1cd5928a5fe1421ef3672a4e5`

to:

`5a21bdbf314f240a8718fe64b6db734e839a8581`

Only the three accepted SHA/encoding pairs were added. Existing compatibility behavior and fail-closed guessing remain.

### D02

Ported only:

`EXPLICIT_OPAQUE_DECODER_NATIVE_NAIVE_DATE_TIME_CARRIER__REPRESENTATION_ONLY`

The R5 codec moved from:

`72f8f3c03ed065e86fea4e76bb17f8e06c2bf540`

to:

`6000a1704d713f65e07610d81e9b3fd8bdd515ca`

Only exact built-in naive `date`, `datetime` and `time` obtain the explicit opaque carrier. Bare R5 date/time remains rejected and timezone-aware values remain rejected.

## Current-port diff

From commission tip `e142043...` to semantic candidate `31fd2f4b7c7c2cdf72bed295b7cb5ca94528349f`:

- 6 net changed files;
- no forbidden path changed;
- no facade edit;
- no historical census harness;
- no historical receipt-tree integration;
- no raw source access.

The decoder was transplanted at exact function/constant grain onto the current baseline. It was **not** replaced with historical blob `37013eb52efb8b61ef202b0d686f729f459d79c5`.

## Source-free qualification

Final governed run:

- workflow: `Rabochii Governed Bounded Court`;
- run: `36615231777`;
- job: `109566427495`;
- attempt: `1`;
- head/execution SHA: `a26279dfad85ddc2a37f7cb396094da308bc58e4`;
- runtime: CPython `3.11.16` on `ubuntu-latest`;
- protocol self-test: **20 passed, 0 failed, 0 errors, 0 skipped**;
- required six-file court: **53 passed, 0 failed, 0 errors, 0 skipped**;
- artifact: `11055435060`;
- artifact digest: `sha256:e823e3fcc269357584fce20d03676f05f9a6e605617d0101e205e721d37a68fe`.

The six files ran together:

1. `test_closed35_g01_sav_numeric_representation_authority.py`
2. `test_closed35_d01_declared_encoding_admission.py`
3. `test_closed35_d02_opaque_datetime_carrier.py`
4. `test_fiabc_lm2_r1j_sav_representation_authority.py`
5. `test_r35_i01_physical_metadata.py`
6. `test_pre553_source_backed_c11_facade.py`

This includes explicit current-decoder D01×D02 composition, all required G01/D01/D02 hostile boundaries, and unchanged facade compatibility.

## Preserved failed execution evidence

The first exact six-file court was **not** rewritten as a repair failure or erased.

- semantic candidate: `42ddc284f7a959797d864e6f8e656fbd94d82348`;
- execution SHA: `9a158eea3ff450292486b2d40ae8f19d21fc9f12`;
- run: `36614460693`;
- job: `109563805093`;
- protocol: **20 passed**;
- governed collection: **1 error before C3 test execution**;
- exact error: `ModuleNotFoundError: No module named 'pandas'`;
- failed artifact: `11054548103`;
- digest: `sha256:b4cc555128c59d7456ffbae0fc77ee734f65d8932a4ca3805dacdf548808c9b5`.

The generic bounded-court workflow installs only pytest. Because the mandated unchanged facade regression imports pandas, the final current-port D02 qualification test bootstraps pandas only when absent before facade collection. This is test-only execution routing; production blobs and semantic authority are unchanged by it.

## Source-access declaration

- raw survey files opened: **0**
- raw survey files materialized: **0**
- raw survey files decoded: **0**
- Candidate A/B/C: **not run**
- measured P2X: **not run**
- CLOSED35 real-source rerun: **not run**

## Review state

Evidence PR #475 was closed unmerged after the green qualification. No control branch, semantic PRE-MAIN branch or shared facade was promoted or mutated.

C3-02 is ready for independent review, not self-adoption.

## Terminal

`C3_02_CURRENT_BASELINE_REPAIRS_INTEGRATED_AND_SOURCE_FREE_QUALIFIED__READY_FOR_INDEPENDENT_REVIEW`
