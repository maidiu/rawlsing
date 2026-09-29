# C3-01 D02 review — ACCEPT

## Exact historical candidate

Historical base:
`9d2958eeb8f0f8a02e9ed4be80909c97a306db3e`.

D02 semantic candidate:
`e2d7674701e1b743dc513ce3bd525ee181bfda17`.

Historical candidate delta:

- `rawlsing_next/pre553_r5_codec.py`: +49;
- `rawlsing_next/pre553_physical_decoder.py`: +18/-1;
- historical census harness: +9/-4;
- new D02 hostile test: +92.

Candidate codec blob:
`064484a7ddbc754f52df7a4a4a87e8b7a028ea86`.

Candidate decoder blob:
`1d848d2506430006883555aba9c9c2d8426fad15`.

D02 test blob:
`7dac3d259f30fe3f3e2d6e7d7df66dca549b81ed`.

## Competent authority / independent oracle

The independent CLOSED35 census records exact source 14 / EVS 2008 as blocked by:

`R5CodecError: date/time meaning may not be invented by the R5 codec; use an explicit opaque decoder value`.

The accepted representation-regime audit classifies D02 as generic **physical carrier** debt:

preserve decoder date/time objects without inventing date/time semantics or convenience-string normalization.

That is the oracle.

## Current defect relation

The current R5 codec already has the generic `R5OpaqueValue(type_id, payload)` lane and exact opaque encode/decode support.

Current R5 codec blob:
`72f8f3c03ed065e86fea4e76bb17f8e06c2bf540`.

But it has no explicit date/time carrier constructor or decoder normalizer.

The current decoder blob:
`d2a074a41fb556a1cd5928a5fe1421ef3672a4e5`

has no `_physical_value` date/time route. Its cell path currently calls `_jsonable(value)`; unsupported objects fall through to `str(value)`.

D02 therefore closes an actual physical-preservation gap rather than creating date/time semantics.

## Candidate law

D02 adds:

- `opaque_decoder_value`;
- `normalize_decoder_physical_value`;
- decoder `_physical_value` routing.

Accepted exact built-in naive physical types:

- `datetime.datetime`;
- `datetime.date`;
- `datetime.time`.

The payload is deterministic field material and carries an explicit type ID.

This is representation of a decoder-native Python object. It is not a survey-semantic date/time value.

## Positive fixtures

The executed fixture covers:

- date;
- time with microseconds/fold;
- datetime with microseconds/fold;
- nested metadata containers;
- exact R5 opaque round-trip;
- decoder route returning `R5OpaqueValue` instead of string.

## Hostile fixtures

The D02 court proves:

- bare date/time passed directly to `R5TypedValueCodec.encode` still fails;
- timezone-aware datetime/time fail pending separate authority;
- different microseconds create different exact identity;
- date and datetime are type-distinct;
- ordinary string `"2008-04-05"` remains a string;
- unrelated int/float lanes do not change;
- int and float remain R5-distinct.

Therefore no semantic date/time promotion occurs.

## Source applicability ceiling

The observed affected source is exact source 14. The carrier itself is a generic representation primitive, not source admission.

A future source does not become admissible merely because its decoder emits a Python date/time object. The separate future-source applicability contract still governs source/variable/config authority.

## Current facade compatibility

The current facade's exact physical material and binding-key paths use `R5TypedValueCodec.encode`.

That codec already knows how to encode `R5OpaqueValue`.

The facade blob is byte-identical between the D02 candidate and current baseline:
`8a761119e4a8d68eb291fc4edfadb52e027f8284`.

No facade change is required.

## Historical harness exclusion

D02 historically modified `closed35_representation_census_harness.py` so its metadata fingerprinting could consume the new carrier.

That file is absent from the current implementation baseline.

It is therefore **not** part of the current C3-02 patch allowlist and must not be resurrected merely to reproduce the old candidate shape.

## Fresh execution

2026-09-29 source-free rerun:

- semantic candidate `e2d767...`;
- execution commit `76ce34c...`; all commits above the candidate are court-spec-only;
- fresh job `109531487944`;
- 20/20 protocol self-test;
- 24/24 governed tests;
- artifact digest `sha256:6da9440db3772f17e8674bfcfd48e2abde8a1814f6cfb3d00cc2fe2c80e55552`.

## Disposition

`ACCEPT`

Only as explicit opaque representation of decoder-native naive date/time objects. Any semantic interpretation or timezone-aware extension requires separate authority.
