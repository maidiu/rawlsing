# Q006 SRC16 racpres operator preparation

## Result

**`SRC16_OPERATOR_READY_PENDING_EXACT_OWNER_AND_CURRENT_USE`**

The reusable SRC16 materializer/driver wiring is ready for a separately
supplied exact owner decision, current-use successor and closure. No real
authority was created, no saved estate was opened by the author run, and no
native SRC16 run was started.

- Base: `8ca2ce37e39a4775b41627000ac9567ab9543540`
- Branch: `agent/remont-q006-saved-issuer-20261121-r1`
- Marker: `GSS:1972:racpres`
- Source: `SRC16`
- Operation: `SRC16-RACPRES-RECORDED-RESPONSE-ONLY`
- Historical grade: `EXACT_COORDINATE_CANDIDATES_ONLY_NOT_ADOPTION`

## Product change

`RecordedUniverseUse` no longer hardcodes only the SRC04 historical scope.

It accepts exactly two known historical grades:

- `EXACT_SOURCE_CODEBOOK_AND_H48_EVIDENCE_ONLY` (SRC04 default, unchanged)
- `EXACT_COORDINATE_CANDIDATES_ONLY_NOT_ADOPTION` (SRC16)

For the non-default grade, the positive current owner decision must bind both:

- the exact historical scope grade, and
- the exact full historical `AuthoritySnapshot` ref.

Unknown grades and generic DEFER acceptance are refused. SRC04 behavior is
unchanged because its constructor uses the default grade.

## Operator files

- `src16_operator.py`
  - materializes the SRC16 operation artifact from the exact owner decision;
  - does not issue authority or open the estate;
  - builds the full structured owner scope:
    `host`, `scope`, `question_id`, `questionnaire_sha256`, `denominator`.
- `run_recorded_src16_private.py`
  - reads owner, operation, R2, use/closure inputs;
  - validates exact SRC16 source/release/universe/replay/question/operation/risk;
  - validates current positive ALLOW authorization, structured scope, raw-domain
    shape, interpretation, historical grade/ref and closure;
  - performs those checks **before** `VerifiedAnvilStreamEstate`/cold index;
  - then uses the existing `HeldRecordedOperation` and native I03 issuance path.

Required current-use shape:

```text
owner_decision_sha256
operation_document_sha256
historical_scope_grade
historical_snapshot_ref   (full AuthoritySnapshot ref)
scope                     (exact structured mapping)
operation
recorded_raw_codes
```

The operation document is materialized with private mode `0600`; driver output
is also written `0600`.

## Nonresponse dependency

The existing recorded transform emits only `SUBSTANTIVE_RESPONSE` cells. An
owner interpretation using `DK`, `REFUSAL`, `SOURCE_SPECIFIC_SPECIAL` or any
unknown state is not silently promoted or dropped. It returns:

```text
SRC16_NONRESPONSE_CLASSIFICATION_REQUIRED
```

Example exact dependency:

```json
{"dependency":"SRC16_NONRESPONSE_CLASSIFICATION_REQUIRED","detail":"code=-98 state=DK cannot be emitted by the existing recorded substantive-only transform","status":"EXACT_HOLD"}
```

The exact SRC16 source-domain metadata from the committed preflight includes
nonresponse codes. If the owner authorizes any of them, the R03/denominator
classification is a separate exact dependency; this operator does not guess it.

## Sourcefree proof

The SRC16-shaped persisted fixture uses only the existing sourcefree candidate,
with:

- `source_id=SRC16`;
- structured nested owner scope;
- exact SRC16 historical grade and full historical snapshot ref;
- saved `SCALAR` topology (translated by the already-tested exact scalar path);
- substantive codes `1/2`, one system-missing event and one absent event.

Observed native result: `SUPPORTED`, denominator `4`, cells `1/2`, system
missing `1`, absent `1`, exact replay equality and both authority identities.

The unchanged SRC04 persisted fixture remains green. Mismatch, unknown-grade,
stale-use and revoked-current paths refuse.

## Test results

```text
SRC16 operator + native fixture: 5 passed
SRC04 persisted regression:      1 passed
SRC04 scalar regression:         2 passed
native I03 suite:                8 passed
driver preflight test:           1 passed (1 deselected)
```

## Remaining external inputs

1. Exact SRC16 `racpres` source/owner decision with an explicitly authorized
   substantive and nonresponse set, or a typed hold.
2. The genuine current-use successor binding the exact historical grade/ref.
3. If any nonresponse code is authorized, the exact R03/denominator
   classification dependency must be resolved without promoting or dropping
   that code.

## Boundaries

No original SRC16/source bytes, respondent bodies, private evidence, saved
native estate or production authority were read/created. No real SRC16 native
query was executed, no issue was posted, and no historical DEFER snapshot was
rewritten.
