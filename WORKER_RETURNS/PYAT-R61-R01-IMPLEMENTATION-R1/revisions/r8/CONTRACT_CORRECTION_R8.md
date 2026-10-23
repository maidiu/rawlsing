# R61 R01 R8 correction contract — semantic label binding

Status: frozen for R8 before the R8 code commit. No API/schema redesign; adds the
remaining validation required by R61AF section 3 and the R7 independent review.
Inherits the R7 contract and all R61AF/R61V decisions. TEST_ONLY sourcefree.

## Target binding

The shared create/live/restore native-context validator derives target identity
from the pinned query target refs and admitted source question inventory.
`target_label` must identify exactly one query target ref in that inventory
(exact ref or its canonical object-id/tail label). Wrong labels and query targets
that do not match the label are typed `CAMPAIGN_TARGET_LABEL_*` refusals before
planning, records or native calls.

## Condition binding

Each condition catalog `(OccurrenceKey, typed value, predicate)` must be a real
response leaf for that source question/value:

- predicate AST must be `SURVEY_RESPONSE_EVENT` leaf;
- its question ref must be in the admitted source question inventory;
- its question ref must match the occurrence key item identity (`key`/tail);
- its exact response value must equal the typed catalog value;
- create/restore use the same validator; malformed keys/values refuse.

Typed occurrence variants (option/form/repeat qualified keys) remain accepted
when they resolve to the same exact question leaf.

## Public issue refusals

`issue(condition_refs)` validates each entry before planning:

- non-`OccurrenceKey` key -> `CAMPAIGN_TYPED_OCCURRENCE_KEY_REQUIRED`;
- unsupported typed value -> `CAMPAIGN_TYPED_VALUE_REQUIRED`;
- duplicate `(occurrence, typed value)` -> `DUPLICATE_CONDITION_REF`;
- duplicate predicate refs in the planner -> `RecurrenceRefusal`.

No raw `AttributeError`/bare `ValueError` is a product refusal.

## Preserved

All R7 positives (retained owner, chronology, multiple batches, stopped head,
pre/post-activation restore, no rerun, fixed pin, native D3/minority/cold,
A1-A3) remain. No new engine, native-owner edit, scientific threshold, source
authority, R03 wake or host/service claim.
