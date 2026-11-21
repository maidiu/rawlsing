# Q006 SRC16 racpres actual-shape operator proof

## Result

**`SRC16_ACTUAL_BINARY_STORED_CODE_OPERATOR_READY`**

The actual saved topology and stored-code semantics are now covered by the
sourcefree SRC16 fixture and exercised through the private driver result writer
and the actual native I03 issuer/evaluator.

- Base: `4866043e3ef550dbdc485a21f012c2c096241669`
- Branch: `agent/remont-q006-saved-issuer-20261121-r1`
- Marker: `GSS:1972:racpres`
- Source: `SRC16`
- Operation: `SRC16-RACPRES-RECORDED-RESPONSE-ONLY`
- Historical grade: `EXACT_COORDINATE_CANDIDATES_ONLY_NOT_ADOPTION`
- Owner scope: `OBSERVED_STORED_CODE_FREQUENCIES`

## Actual saved topology

The exact sole saved shape reported by the targeted local inventory is:

```json
{"index":0,"kind":"BINARY_CONTRAST_SINGLE","source_manual_topology":"binary_contrast"}
```

The recorded projection accepts that exact three-field shape only, with
`index=0` and `source_manual_topology=binary_contrast`, and translates it to
`SCALAR_SINGULAR` for the existing strict native target. It preserves the
remaining topology fields, original event dependency, and the recorded
transform replay identity.

No generic topology alias is implemented. Ordered, repeated, unknown,
malformed, extra-field and non-zero-index envelopes are left unchanged and
refused, or rejected before the native path.

## Stored-code state bins

The actual saved code categories are explicit, owner-supplied states. The
fixture uses synthetic codes matching the documented signed code types:

```text
1    -> SUBSTANTIVE_RESPONSE
2    -> SUBSTANTIVE_RESPONSE
-98  -> DK
-99  -> MISSING
-100 -> INAPPLICABLE
None -> physical system missing, separate
absent respondent -> absent, separate
```

The state-bearing projection:

- keeps every authorized non-null code distinguishable;
- rejects duplicate/non-distinguishable non-substantive bins;
- preserves the raw code in operation interpretation and driver evidence;
- emits signed integer cells for substantive codes and explicit state-bearing
  bins for DK/MISSING/INAPPLICABLE;
- reports `scope_kind=OBSERVED_STORED_CODE_FREQUENCIES`,
  `asked_eligibility=HELD_NOT_PROVEN`, and
  `substantive_vote_denominator=false`;
- does not treat stored codes as an asked, eligible, population or substantive
  vote denominator, and does not reclassify them as substantive responses.

The driver output includes `stored_code_bins` mapping each raw code to its state
and emitted cell, plus the exact state-bearing native cells.

## Historical DEFER field

The exact saved SRC16 historical envelope has these keys:

```text
evidence_bundle_sha256
grade
not_source_scientific_authority
p2_authority_status
source_id
source_sha256
wave
```

The SRC16 `RecordedUniverseUse` path reads only `scope_envelope["grade"]`.
SRC04 retains `scope_envelope["semantic_scope"]`. There is no fallback, no
cross-field alias, and unknown/wrong fields or refs refuse. The historical
snapshot remains immutable DEFER.

The tiny persisted fixture was changed to the actual SRC16 envelope keys before
the repair; it failed with `historical snapshot scope grade mismatch`, then
passed after the field-specific repair. `HISTORICAL_FIELD_RED.out` preserves
the pre-repair failure.

## Preflight / currentness

Before any cold estate/index open, the private driver validates:

- exact owner/R2/operation/source/release/universe/replay/question/risk roots;
- positive current ALLOW owner/use authorization;
- exact structured owner scope;
- exact raw-code domain, signed code representation and state interpretation;
- exact historical grade and full historical snapshot ref;
- exact operation/use/closure hashes and current-use binding;
- state-bearing flag and approved non-substantive state set.

The driver then uses the existing `HeldRecordedOperation`, recorded routing plan,
`issue_and_execute_stream_i03`, and native `execute_anvil_stream_i03`; no test
substitute issuer/evaluator is used. The CLI/result writer is exercised and
writes a private `0600` JSON result.

## Test proof

```text
SRC16 operator + actual-shape fixture: 7 passed
SRC04 persisted regression:            1 passed
SRC04 scalar regression:               2 passed
native I03 suite:                      8 passed
driver result-writer test:             1 passed (1 deselected)
```

The actual-shape fixture produces a `SUPPORTED` native fact with stored-code
denominator `6`, five distinguishable cells (`1`, `2`, DK, MISSING,
INAPPLICABLE), one separate physical-null/system-missing member, one separate
absent member, and repeated replay equality.

Negatives covered:

- wrong saved BINARY_CONTRAST_SINGLE shape/index/manual topology;
- extra rank/multiplicity fields;
- ordered/unknown topology left unaliased;
- unknown raw code;
- non-distinguishable state bins / unknown state dependency;
- stale operation/use currentness before estate construction;
- revoked current verifier;
- SRC04 default historical grade regression.

## Exact dependency for unknown states

The actual owner categories are supported. If an owner supplies a state outside
the exact recorded response-state family, the operator returns:

```json
{"dependency":"SRC16_CODE_STATE_CLASSIFICATION_REQUIRED","detail":"code=-98 state=NOT_A_RECORDED_STATE is not an exact recorded state","status":"EXACT_HOLD"}
```

## Remaining external inputs

The exact SRC16 owner decision and genuine current-use successor are still
controller-supplied. No actual SRC16 authority creation, raw source read,
private evidence read, estate mutation or real native query was performed.
