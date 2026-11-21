# REMONT Q006 / SRC04 q103 — Lane 1 R2 evidence cut

## Result

**`Q103_RAW_CODE_RECOVERABLE__TYPED_STATE_CONFLICT__ASKED_RISK_IRREDUCIBLE_HOLD`**

Exact unchanged SRC04 carrier verified under the current R2 scoped analytical
decision. Private targeted q103 inspection found:

- q103 events are present.
- The original raw physical values are retained in the versioned R5 typed
  carrier (exact float bits + schema/codec identity), and all observed raw codes
  are within the questionnaire set `1,2,3,4,97,98,99` or explicit none/missing.
- Raw-code recoverability is **total within observed q103 codes**.
- The current source-config typed states conflict with the questionnaire:
  `97` and `98` both `DK`; `99` `SUBSTANTIVE_RESPONSE`.
- Later/response provenance: producer replay locator and response topology are
  present; `value_transform_authority_ref` and
  `canonical_response_value_if_authorized` are absent.
- Actual q103 RoutingEligibilityFact rows are present but `ROUTING_UNKNOWN`.
  Asked membership is therefore **not proven**.

No native I03, issuer, scientific policy, source rebuild, or estate write was
performed.

## Questionnaire authority

Actual local questionnaire SHA-256
`0814f77bcfdad3c78d5e46f49012437f25ddcbfe8bea3e565d7a26874bab4118`
gives q103: `1 Very Good`, `2 Good`, `3 Bad`, `4 Very Bad`, `97 Not clear`,
`98 Can't Choose/Don't know`, `99 Decline to Answer`.

QSR q103 is exact, source-present, single-choice, general-scope; it has no typed
state map. Current q103 source-config item supplies
`GOVERNED_QSMV2_RELATION_AUTHORITY` and an exact semantic role, but its response
state map is not compatible with the questionnaire.

## One-item owner decision

`Q103_OWNER_DECISION_CANDIDATE.json` is a draft, **not issued**:

- signable from evidence: q103 identity; raw-code total recoverability; source
  labels; carrier raw/provenance shape; item semantic role.
- proposed typed map requiring owner signature:
  `1-4 substantive`, `97 SOURCE_SPECIFIC_SPECIAL`, `98 DK`,
  `99 REFUSAL`, physical system missing `MISSING`.
- irreducible hold: asked/eligible risk. `ALL` and routing facts do not prove
  administration.
- recorded-response-only candidate: physically possible from the retained raw
  events, but **not authorized by existing evidence** and must not be labeled
  asked. Exact owner attestation remains.

## Asked route trace

Actual instrument/form/source references checked:

- questionnaire: q103 general item, no form/skip rule; only country context.
- QSR: q103 `scope=general`, answer role, no routing.
- R157 config: `SINGLE_SAV_FILE_NO_FORM_VARIABLE_EVIDENCE`; q103
  `row_selector=ALL`, `typed_state=ROUTING_UNKNOWN`, risk set
  `urn:rawlsing:r157:original:SRC04:q103:unresolved`.
- saved carrier: q103 routing facts present, all observed state
  `ROUTING_UNKNOWN`.

No exact asked/eligible record exists. Full asked distribution is held.

## Smallest next input

SRC04 QSM/source/risk owner signs the q103 state map and either exact asked/
eligible form/country/risk or a distinct `RECORDED_Q103_RESPONSE_ONLY` scope.
R03/saved-release owner then supplies an authentic catalog/query/predicate.

**Positive witness:** actual I03 returns q103 RAW categories 1-4/97/98/99 plus
system missing with the signed denominator and exact replay.
**Negative witness:** treating `ROUTING_UNKNOWN` as asked, collapsing 97/98/99,
or accepting the current 99=substantive mapping must refuse.

## Boundaries

No original SAV, private rows/body/identifiers, counts in public, C11 admission
rerun as substitute, GSS rerun, issuer implementation, protected edits, or issue
comments.
