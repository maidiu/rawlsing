# C3-01 D01 review — ACCEPT

## Exact historical candidate

Historical base:
`9d2958eeb8f0f8a02e9ed4be80909c97a306db3e`.

D01 semantic candidate:
`f6613cbef8c23148c14d9464e9b6a869474a418f`.

Candidate delta:

- `rawlsing_next/pre553_physical_decoder.py`: +19/-3;
- new `rawlsing_next/tests/test_closed35_d01_declared_encoding_admission.py`.

Candidate decoder blob:
`4af3a8502ee99aa262bb5086404ca9f8a8892807`.

D01 test blob:
`8fc05965386055a208e5b3988112e67a2e6333e2`.

## Competent authority / independent oracle

The accepted CLOSED35 representation regime identifies one generic physical decoder-admission debt over exactly three committed source identities:

- Asian Barometer Wave 1:
  `ac0b8bc1ddb2fa6b952417e35b6379ce6a2cf8596776a43282ba44f48e0ae1a2` / BIG5;
- EVS 1981:
  `5b703173845c086382fd93252f1cbc91dfef74007755459adfc73785389172f2` / WINDOWS-1252;
- EVS 1990:
  `66252a92c59bf6759b79a6b35b2be658b98a433373212a70c8ec94755d3e02ec` / WINDOWS-1252.

The authoritative census receipts independently record those exact SHA/encoding/reader facts and classify generic decoder admission as GAP.

The oracle is therefore:

`ALLOW iff exact SHA is one of those three AND supplied declared encoding is that SHA's exact declared encoding; otherwise fail closed.`

Successful physical decoding is not text-semantic authority.

## Candidate law

D01 introduces a declared-encoding allowlist separate from the pre-existing compatibility-only allowlist.

`_compatibility_config` semantics:

- `auto|guess|fallback` -> reject;
- `None` -> no override, no declared-encoding authority;
- exact old compatibility SHA/config -> unchanged compatibility-only state;
- exact declared SHA + exact declared encoding -> declared physical-decoding-only state;
- everything else -> reject.

The exact authority-status string is:

`SOURCE_DECLARED_EXACT_SHA_ENCODING__PHYSICAL_DECODING_ONLY`.

The resulting decoder receipt continues to carry:

- reader;
- actual pyreadstat version;
- decoder implementation;
- physical metadata contract;
- user_missing/apply_value_formats;
- explicit encoding;
- authority status.

Thus a later current-source applicability court can still require the frozen decoder/version/config witness. C3-01 does not convert the D01 status into a runtime-version waiver.

## Positive fixtures

Positive exact pairs are the three rows above.

The old exact-SHA compatibility lane is also a conservation fixture: a previously admitted compatibility source retains `COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY`.

## Hostile fixtures

Executed D01 hostiles include:

- BIG5 supplied to a WINDOWS-1252 source;
- WINDOWS-1252 supplied to the BIG5 source;
- correct encoding with unknown all-zero/all-f SHA;
- automatic `auto`, `guess`, `fallback`;
- cross-source inheritance;
- no encoding override acquiring authority.

All fail or remain unprivileged exactly as required.

## Current implementation relation

Current decoder at `b3b2fa...` is blob:
`d2a074a41fb556a1cd5928a5fe1421ef3672a4e5`.

It contains only the older exact-SHA compatibility lane and does not contain D01's declared-encoding allowlist/status.

The historical base decoder was blob:
`86109c4a0b7ebd9b66e3b531b6334bfb48f03f78`.

Therefore the historical file cannot be wholesale cherry-picked. C3-02 must port only D01's exact constants/export and narrow `_compatibility_config` branch onto the current decoder.

No facade edit is needed.

## Scope ceiling

D01 does not cure the independently recorded value-key/semantic blockers on sources 08, 11, or 12. It admits only the exact physical decoder encoding lane.

It does not authorize:

- guessed encoding;
- source-family inheritance;
- label/value interpretation;
- canonical text normalization;
- semantic equality of decoded strings.

## Fresh execution

2026-09-29 source-free rerun:

- semantic candidate `f6613c...`;
- execution commit `4a19af8...`, court-spec-only one commit above candidate;
- fresh job `109531476500`;
- 20/20 protocol self-test;
- 14/14 governed tests;
- artifact digest `sha256:d3bf6d5fa2a336aa434c641ecd30b3be50a8fe8d773a8676d1aa0b913ff0cf32`.

## Disposition

`ACCEPT`

At exact SHA + exact declared encoding + physical-decoding-only grain.
