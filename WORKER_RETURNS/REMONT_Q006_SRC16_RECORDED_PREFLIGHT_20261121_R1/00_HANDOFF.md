# Q006 / SRC16 GSS1972 — metadata-only recorded-response preflight

## Result

**`SRC16_RACPRES_RECORDED_PREFLIGHT_EXACT_HOLD`**

Selected best-supported single-occurrence scalar marker:

`GSS:1972:racpres` — “would vote for black president”.

Why this marker:

- exact source-structure row: single-choice, answer role, source present;
- current source-config item: `governed_qsmv2_relation`,
  `GOVERNED_QSMV2_RELATION_AUTHORITY`, exact, binary contrast, signed;
- simple finite substantive domain `1/2`;
- one exact saved-stream QuestionVariableBinding match;
- exact SRC16 R2 stream/source/release/universe/replay pins available.

No response scan, original SAV read, native query, or production edit was performed.

## Exact pins

- source: `SOURCE_ARTIFACT|GSS1972.sav|e368fc0f1d141b201900185c919c48ab1de1c4c7815bccf83a6e4fb224293204`
- release: `C11_STREAM_SOURCEFREE_RELEASE|GSS_1972_SOURCE_ARTIFACT|95fbd6e611bfdc259d86d46e3d74568e04cc209f97d5ada05d45ae25483a41fb`
- universe: `EmpiricalUniverse@1.0.0|urn:rawlsing:pre553:EmpiricalUniverse:sha256:8a3e19904e95a67b63db59215eeebf47912a497e253668a0bc57943a62f657d3|8a3e19904e95a67b63db59215eeebf47912a497e253668a0bc57943a62f657d3`
- replay: `08f57630a64b281043ffb11af59f1903e80e3e0690ec68869f995048bb788da7`
- question: `NATIVE_QUESTION|urn:rawlsing:r157:source:SRC16:question_impl.phase0.29b0dec400d8150f5123|96e5d1e48d463ec0bf049a7ba4e12754e0c8942bb3238b1da20a36190177b9b1`
- R2 decision: `USER_SOURCE_DECISION|pyat-p0-two-saved-waves-r2-src16|430130866902961460d075e4cc16b775a7573403a50ddf1fb2cb52025fdc29d0`

## Source states (metadata only)

Current `SRC16.source.config.json` response slot for `racpres` distinguishes:

- substantive: 1, 2
- DK: -98
- refusal: -90
- missing: -99
- not asked: -97, -80, -70
- source-specific special: -96, -60, -40
- invalid/unresolved: -95, -94
- inapplicable: -100
- physical system missing: `None`

`source_missing_declaration` is null for this slot; no declared missing rule is
asserted. `absent` is a carrier event-absence state, not a source code, and
cannot be established from metadata without a response scan.

Routing is `row_selector=ALL`, `typed_state=ROUTING_UNKNOWN`; this is **not**
evidence that all respondents were asked.

## Contract status

Common SRC04 engineering is reusable in principle:

- `RecordedUniverseUse` / `HeldRecordedOperation` / native stream I03 are
  source-generic.
- `run_recorded_q103_private.py`, `q006_materialize.py`, and
  `proof_recorded_operation.py` hardcode SRC04/q103/owner identities and must
  not be reused as-is.

## Owner decisions still needed

1. **SRC16 source/QSM owner**: authorize `racpres` recorded-response-only scope
   and the exact allowed source states (substantive and any nonanswer states);
   asked/eligible remains held.
2. **Universe-use owner**: the stored SRC16 universe references the historical
   `R157-SRC16-SOURCE-EVIDENCE` DEFER snapshot, whose scope is
   `EXACT_COORDINATE_CANDIDATES_ONLY_NOT_ADOPTION`; the current bfa
   `RecordedUniverseUse` requires
   `EXACT_SOURCE_CODEBOOK_AND_H48_EVIDENCE_ONLY`. Provide the exact positive use
   decision/successor or a typed hold.
3. **R03/saved issuer**: supply the exact issued catalog/query/predicate for
   `racpres` after those two decisions.

No native preflight beyond metadata is warranted until those are exact.

## Boundaries

No full saved response scan, original respondent read, native run, production
edit, new architecture, fabricated routing, or cross-wave claim. No issue post.
