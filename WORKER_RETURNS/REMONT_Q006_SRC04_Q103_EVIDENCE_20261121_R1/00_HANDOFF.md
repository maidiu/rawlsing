# REMONT Q006 / SRC04 q103 — Lane 1 bounded evidence return

## Exact result

**`Q103_SOURCE_DECISION_CANDIDATE__ASKED_RISK_IRREDUCIBLE_HOLD`**

The task materially advances the prior q103 trace:

- The actual local questionnaire is available and confirms q103 exactly:
  `1=Very Good`, `2=Good`, `3=Bad`, `4=Very Bad`, `97=Not clear`,
  `98=Can't Choose/Don't know`, `99=Decline to Answer`.
- The actual saved SRC04 carrier has one exact q103 question binding.
- The saved carrier retains the raw response value and provenance fields
  (`raw_typed`, `field_raw_response_value_json`, `field_response_state`,
  `field_value_transform_authority_ref`, `producer_replay_locator_json`);
  this is structural retention evidence, not an interpretation.
- The QSR q103 row is exact but supplies no typed code-state mapping and reports
  `final_driver_id=hierarchy`; the current q103 source-config item supplies a
  `GOVERNED_QSMV2_RELATION_AUTHORITY` semantic role, not a selected response-code
  state map.
- The current source config's response-state map is not compatible with the
  questionnaire: `97` and `98` are both `DK`; `99` is `SUBSTANTIVE_RESPONSE`.
- q103 routing remains `row_selector=ALL`, `typed_state=ROUTING_UNKNOWN`, with
  risk set `urn:rawlsing:r157:original:SRC04:q103:unresolved`. `ALL` is not a
  proof that everyone was asked.

No query, native I03, scientific policy, or source authority was issued.

## The one-item decision

`Q103_SOURCE_DECISION_CANDIDATE.json` is a **draft owner decision, not issued**.
It identifies which fields are signable from existing evidence and which remain
irreducible holds.

## Distinction

- **Source fact / source authority:** categories 97/98/99 and asked risk.
- **Code absence:** no competent real saved-stream issuer/catalog/query exists;
  #1084 public is TEST_ONLY and #1205 is policy/fixture code.
- **Permissible narrower scope:** recorded-response-only is a different estimand;
  no existing competent authority covers it and it must never be labeled
  asked-eligible.

## Shortest next owner input

SRC04 QSM/source/risk owner signs the q103 decision fields; R03/saved-release
issuer then supplies an authentic catalog/query/predicate. Only then can the
MainMac worker run actual I03 and replay.

## Boundaries

No original SAV read, estate reconstruction/write, responder values, GSS rerun,
C11 admission rerun, issuer implementation, protected refs, or issue comments.
