# PYAT C3-01 — REPRESENTATION REPAIR ACCEPTANCE — R1

Status:

`PASS__THREE_REPAIRS_SEPARATELY_ADJUDICATED__G01_ACCEPT__D01_ACCEPT__D02_ACCEPT`

Repository: `maidiu/rawlsing`

Assigned branch:
`agent/rabochii-pyat-hq126-c3-physical-repair-acceptance-r1`

Commission tip:
`afffba327286a3f49ce852409d520bf944efed3c`

Implementation baseline:
`b3b2fa13049513078c301a1f6574b661fcf390c5`

Orchestration authority:
`810dbfde9fa5dbe1e3625188f4c13c4c9e7ceeb7`

No raw survey file was opened, materialized, decoded or executed. No current shared decoder, facade, codec, source semantic, or governed execution branch was modified by C3-01.

## Identity re-verification

The assigned branch was exactly at the expected commission tip before C3-01 writes.

The commission-named orchestration files are not present in the commission commit tree itself. They were therefore read from the exact orchestration authority named by the commission, not from an unpinned moving branch:

- `07_C3_EXECUTION_SPEC.md` blob `7a8cb87e188dd24437b58170b3ada0b9a2d95e91`;
- `08_REVIEW_AND_INTEGRATION.md` blob `ed54e675a073c0e462581c0918f35ac2776d26af`;
- command charter blob `50a48745dfd9a156268ddce1b3fdcd04899dc731`.

The C3 binding in the commission tree is blob:
`170c335fca49f0231323ab48d7bd77f41ba10987`.

Pinned C3 implementation identities reverified:

- historical combined repair candidate: `3cefb4ebf61ccdb6a8c5a03815438bdcda021292`;
- historical candidate decoder blob: `37013eb52efb8b61ef202b0d686f729f459d79c5`;
- H125/current audited decoder: `1585b3edf1014544dfce90bbeb758a5024d69855`, blob `d2a074a41fb556a1cd5928a5fe1421ef3672a4e5`;
- implementation-baseline decoder `b3b2fa...`: same blob `d2a074a41fb556a1cd5928a5fe1421ef3672a4e5`;
- current source-backed C11 facade at H125 and `b3b2fa...`: blob `8a761119e4a8d68eb291fc4edfadb52e027f8284`;
- current R5 codec at H125 and `b3b2fa...`: blob `72f8f3c03ed065e86fea4e76bb17f8e06c2bf540`;
- historical fan-in return commit: `9bf2fd3641136c58c9e54f050864eb9f29c1a6c4`, return blob `4365bc346e7615382d0b909d09209260bbe8908d`.

## Independent law / oracle

C3-01 does not treat the historical repair branches as their own authority.

The controlling independent law is the accepted CLOSED35 representation-regime audit rooted in authoritative census head:

`b801c58c8e4d6d10e36e0a42ca62cf6908cbf25a`.

Independent acceptance-audit return blob:
`89000485e69c6716008b4199e301df8ace3e2869`.

Acceptance matrix blob:
`def6e218d79f62d4f1886c843cbd1270538f58ad`.

That court establishes the controlling distinctions:

1. physical representation law is separate from source applicability;
2. source applicability is exact-SHA / decoder/config / governed-surface bound;
3. bounded bridges do not generalize;
4. int/float arithmetic equality is not physical identity;
5. encoding admission is not text-semantic authority;
6. opaque date/time carriage is representation preservation, not date/time interpretation;
7. future variables/sources do not inherit applicability merely from family or source labels.

## Separate dispositions

### G01 — ACCEPT

Accepted only as:

`EXACT_NINE_SURFACE_SAV_NATIVE_INT_RULE_TO_FLOAT64_PHYSICAL_REPRESENTATION_SUCCESSOR`.

Historical semantic candidate:
`8ed091e1323f46335a4bcbf6ab92ac9e3f228848`.

The candidate adds a separate exact representation-authority module. It does **not** edit the decoder.

Applicability is frozen to nine surfaces over exact sources 02, 06 and 21, exact variable names, ordinals, native integer codes, physical missing states/declarations, R5 float64 tokens, and expected physical binding keys.

Rejected interpretations remain rejected:

- no global int->float coercion;
- no arithmetic-magnitude identity;
- no Decimal equivalence;
- no other source/variable/code;
- no DTA applicability;
- no cross-wave inheritance;
- no label/display semantic authority;
- no missing-state reinterpretation.

Fresh source-free rerun on 2026-09-29:

- execution commit `a9069d0a3d3b3526bc72a9b7c9dccc02bd01f243`;
- its only delta over semantic candidate is the court-spec binding to that exact candidate;
- workflow run `35884185279`;
- fresh job `109531459446`;
- protocol self-test: **20 passed**;
- governed court: **25 passed**;
- fresh artifact `11050980609`;
- artifact digest `sha256:47d74c0474e32520d4934ad671e2e8d9b6ff299e1cf01c3e5a66e779656ecbb3`.

### D01 — ACCEPT

Accepted only as:

`EXACT_SOURCE_SHA_PLUS_DECLARED_ENCODING_PHYSICAL_DECODER_ADMISSION`.

Historical semantic candidate:
`f6613cbef8c23148c14d9464e9b6a869474a418f`.

Exact admitted declarations:

- `ac0b8bc1ddb2fa6b952417e35b6379ce6a2cf8596776a43282ba44f48e0ae1a2 -> BIG5`;
- `5b703173845c086382fd93252f1cbc91dfef74007755459adfc73785389172f2 -> WINDOWS-1252`;
- `66252a92c59bf6759b79a6b35b2be658b98a433373212a70c8ec94755d3e02ec -> WINDOWS-1252`.

The independently frozen census receipts identify those exact source SHA/encoding pairs and the pyreadstat physical lane.

The candidate keeps declared encoding separate from the older compatibility-only allowlist and fails closed on:

- wrong source SHA;
- wrong encoding for a known SHA;
- unknown SHA;
- `auto`, `guess`, or `fallback`;
- cross-source inheritance.

`encoding=None` remains unprivileged and carries no declared-encoding authority status.

The authority status explicitly says:
`SOURCE_DECLARED_EXACT_SHA_ENCODING__PHYSICAL_DECODING_ONLY`.

It therefore does not infer text meaning from successful decoding.

The decoder's physical receipt continues to record reader version, implementation, config, missingness and physical metadata; downstream applicability remains responsible for matching the frozen runtime/config evidence. D01 acceptance does not waive that requirement.

Fresh source-free rerun on 2026-09-29:

- execution commit `4a19af8bbc5d2ef602ad375873feeba96bf47eaa`;
- its only delta over semantic candidate is court-spec binding;
- workflow run `35883052865`;
- fresh job `109531476500`;
- protocol self-test: **20 passed**;
- governed court: **14 passed**;
- fresh artifact `11049874988`;
- artifact digest `sha256:d3bf6d5fa2a336aa434c641ecd30b3be50a8fe8d773a8676d1aa0b913ff0cf32`.

D01 acceptance closes decoder admission only. It does **not** change the other value-key/semantic blockers recorded for sources 08, 11 or 12.

### D02 — ACCEPT

Accepted only as:

`EXPLICIT_OPAQUE_DECODER_NATIVE_NAIVE_DATE_TIME_CARRIER__REPRESENTATION_ONLY`.

Historical semantic candidate:
`e2d7674701e1b743dc513ce3bd525ee181bfda17`.

The current codec already has an opaque typed-value lane but lacks a lawful constructor/normalizer for decoder-native date/time values. The current decoder therefore falls through `_jsonable` and convenience-stringifies otherwise unsupported objects.

D02 adds an explicit carrier for exact built-in naive:

- `datetime.datetime`;
- `datetime.date`;
- `datetime.time`.

The carrier stores exact type ID plus deterministic binary field material. It does not turn the value into a canonical survey date/time, infer display-format meaning, infer timezone meaning, or grant source semantics.

Negative limits verified:

- bare date/time remains rejected by `R5TypedValueCodec.encode`;
- timezone-aware datetime/time remains rejected pending separate authority;
- ordinary strings remain ordinary strings;
- int and float typed identity remains distinct;
- field/type changes alter opaque identity;
- convenience stringification is not accepted as the carrier.

The accepted CLOSED35 regime names this as a generic physical-carrier debt whose observed affected source is exact source 14. Accepting a representation carrier does not admit a new source or a new semantic date/time regime; source applicability remains separately governed.

Fresh source-free rerun on 2026-09-29:

- execution commit `76ce34c8e24db5f080a96fdca6d0c4c982215089`;
- its deltas over semantic candidate are court-spec-only;
- workflow run `35883745809`;
- fresh job `109531487944`;
- protocol self-test: **20 passed**;
- governed court: **24 passed**;
- fresh artifact `11051220376`;
- artifact digest `sha256:6da9440db3772f17e8674bfcfd48e2abde8a1814f6cfb3d00cc2fe2c80e55552`.

## Interaction / current-facade compatibility

Fresh combined historical-candidate rerun:

- semantic candidate `3cefb4ebf61ccdb6a8c5a03815438bdcda021292`;
- execution commit `3d6d45e0d97cdf9a60105e140583e043a42ccfba`;
- only delta is exact court-spec binding;
- workflow run `35887617559`;
- fresh job `109531501528`;
- protocol self-test: **20 passed**;
- combined governed interaction court: **42 passed**;
- fresh artifact `11050338899`;
- digest `sha256:4918ca1338974463428f2e6fda451b2590748612275e49de7b934596fd41f4ca`.

The source-backed C11 facade blob is exactly identical at:

- G01 candidate;
- D01 candidate;
- D02 candidate;
- combined fan-in candidate;
- H125;
- current implementation baseline.

Exact blob:
`8a761119e4a8d68eb291fc4edfadb52e027f8284`.

No facade repair is required by C3-01.

The facade already uses exact R5 typed physical material and `physical_value_binding_key`. G01 is defined against that exact function. D02's opaque values fit the facade's already-existing `R5OpaqueValue` encode lane. D01 changes decoder admission, not facade semantics.

## C3-02 integration constraint

These ACCEPT dispositions do **not** authorize C3-02 yet. HQ must freeze the minimal patch allowlist first.

C3-02 must not cherry-pick the historical decoder wholesale. The historical base decoder blob `86109c4a0b7ebd9b66e3b531b6334bfb48f03f78` differs from the current baseline decoder blob `d2a074a41fb556a1cd5928a5fe1421ef3672a4e5`.

The accepted changes must therefore be ported at exact function/constant grain onto the current decoder.

The historical D02 edit to `closed35_representation_census_harness.py` is not part of the current patch allowlist: that historical harness is absent from `b3b2fa...`.

See `08_PROPOSED_C3_02_ALLOWLIST.json`.

## Proof labels

- candidate/current identities: `STATIC_EXACT_GITHUB_INSPECTION`;
- independent law/oracle: `ACCEPTED_DOCUMENTARY_AUTHORITY_PLUS_EXACT_CENSUS_RECEIPTS`;
- G01/D01/D02 focused qualification: `SOURCE_FREE_EXECUTED_2026_09_29`;
- combined interaction qualification: `SOURCE_FREE_EXECUTED_2026_09_29`;
- raw-source positive applicability beyond committed receipts: `NOT_EXECUTED_IN_C3_01`.

Historical test counts are retained only as historical evidence. The counts cited above as decision evidence are fresh reruns.

## Terminal

`C3_01_G01_D01_D02_SEPARATE_DISPOSITIONS_READY_FOR_INDEPENDENT_REVIEW`
