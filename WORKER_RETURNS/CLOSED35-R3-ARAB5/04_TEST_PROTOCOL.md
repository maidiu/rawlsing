# CLOSED35-R3-ARAB5 — Hostile Test Protocol

Status:

`TESTS_AUTHORED__NOT_EXECUTED`

Python test file:

`rawlsing_next/tests/test_closed35_r3_arab5_realization.py`

The tests are synthetic realization-law tests. They do not open the canonical SAV and do not substitute for real-source physical equivalence.

## T01 — native ID cannot become replay identity

Assert:

- ID is noninjective;
- COUNTRY+ID also remains noninjective in accepted evidence;
- hard replay identity is source SHA + zero-based source row ordinal.

Reject ID-based or composite-native-key replay invention.

## T02 — missing WT/PSU cannot invent design semantics or row exclusion

Construct SYSTEM_MISSING WT and PSU projections.

Assert:

- physical state remains SYSTEM_MISSING;
- semantic design role remains `BOUNDED_UNKNOWN`;
- source row retention remains required;
- default analytical use remains unauthorized.

Reject automatic row dropping, PSU reconstruction, or weight selection.

## T03 — Q101 dictionary may not be pruned

Require the complete accepted dictionary set:

`-9,-8,1,2,3,4,97,98,99`

Remove `-9/-8/97` and require fail-closed.

This protects source metadata even where accepted incidence records those extra codes as unobserved.

## T04 — Q101 dictionary membership is not semantic applicability

For each extra dictionary code `-9/-8/97` assert:

- source dictionary member = true;
- observed in accepted snapshot = false;
- exact current semantic role = `BOUNDED_UNKNOWN`.

Reject semantic promotion from dictionary presence.

## T05 — Unicode text is exact, not normalized

Round-trip the accepted E2001B literal witness and a synthetic decomposed Unicode string through the realization text-preservation function.

Assert exact string/UTF-8 preservation.

Reject normalization that changes source identity.

## T06 — ranked Q2061 topology cannot flatten

Require exact ordered slots:

- Q2061A rank 1;
- Q2061B rank 2.

Reject reverse order, one-slot collapse, or unordered-set treatment.

## T07 — split carriers are distinct and routing-neutral by themselves

Assert:

- SPLITA assignment domain 1/2;
- SPLITB assignment domain 1/2/3;
- item routing remains bounded UNKNOWN absent exact documentary join.

Reject carrier aliasing or split-value-to-item-applicability invention.

## T08 — missingness cannot create routing authority

Supply SYSTEM_MISSING to an unresolved target with no documentary rule.

Expected route state:

`BOUNDED_UNKNOWN`

Then supply a synthetic explicit documentary join and require route resolution from that join rather than from observed physical state.

## T09 — exact source SHA is mandatory

Admit only the canonical SHA:

`6a5cbad637ce1546833a1d4812ba6d1e8d75f85b5b199b0cf3ec5cf456068dbc`

Assert that admission does not claim physical equivalence.

Reject wrong SHA.

## T10 — Candidate A/B/C share one semantic owner

Require the exact candidate set A/B/C to share:

- canonical source SHA;
- source-specific realization identity;
- identity law;
- Q101 dictionary law;
- ranked/split topology;
- routing noninference law;
- design bounded UNKNOWNs;
- cross-wave noninheritance.

Reject candidate-specific semantic divergence.

## T11 — S35 and R35 scope is frozen

Require exact S35 set:

`EC01, EC05, EC07, EC09, EC10, EC11, EC12`

Require R35 hooks:

- `PRE553_PHYSICAL_METADATA@1.0.0`;
- `FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0` where applicable;
- I03 source-scope / expectation / candidate / whole-source receipt schemas.

Reject an Arab5-only adapter or any physical hook treated as semantic authority.

## Rejection coverage requested by commission

The authored suite directly covers:

- respondent ID as global replay identity;
- WT/PSU survey-design invention;
- dictionary-code pruning;
- Unicode normalization that changes source identity;
- ranked-slot flattening;
- routing from missingness;
- undocumented semantic interpretation of Q101 extra codes;
- candidate-specific semantic divergence.

## T12 — cross-wave semantic leakage is forbidden

Inspect the source-specific realization payload.

Assert:

- family semantic imports are disabled;
- Wave-2 semantics are not inherited;
- Wave-8 semantics are not inherited.

Reject any source-local realization that fills Wave-5 bounded UNKNOWNs from another Arab Barometer release.

The authored Python suite contains this dedicated assertion.

## Later real qualification order

canonical source identity

-> `ARAB5_SEMANTIC_OWNER_V1` freeze

-> independent Candidate A/B/C physical realization

-> R35 whole-source physical-equivalence receipts

-> T01-T12 realization court

-> common A/B/C comparison

-> later I05/P2X only under their own authority.

## Current proof boundary

`TESTS_AUTHORED__NOT_EXECUTED`

No source bytes opened.

No source processing run.

No real-source execution.

No whole-source physical-equivalence PASS.

No A/B/C execution PASS.

No I05.

No measured P2X.
