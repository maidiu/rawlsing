# CLOSED35-R3-ARAB8 — Synthetic Qualification Test Protocol

Status:

TESTS_AUTHORED__NOT_EXECUTED

This protocol defines source-independent hostile tests for the Arab Barometer Wave 8 realization.

The Python tests are checked in under:

rawlsing_next/tests/test_closed35_r3_arab8_realization.py

No canonical SAV bytes are opened by these tests as authored.

## T01 — ID=0 is ordinary source state, not missing identity

Construct a synthetic ID value 0.

Expected:

- physical state ORDINARY_STORED_VALUE;
- raw value exactly 0;
- documentary role RESPONDENT_ID_NUMBER;
- hard replay authority false;
- hard replay identity remains SOURCE_SHA256+ROW_ORDINAL.

Reject ID=0 row deletion, respondent merge, missing-identity coercion, or deduplication.

## T02 — native ID cannot replace replay identity

Expected:

ID hard replay authority = false.

COUNTRY+ID hard replay authority = false.

Hard replay key = source SHA + zero-based row ordinal.

Reject any candidate that rekeys on native respondent ID.

## T03 — blank BLOCK_ID is not SYSTEM_MISSING

Construct BLOCK_ID raw value "".

Expected:

- raw value exact empty string;
- physical state ORDINARY_STORED_VALUE;
- semantic state BOUNDED_UNKNOWN.

Reject conversion to null, SYSTEM_MISSING, NOT_ASKED, or inferred design block.

## T04 — Q1/STRATUM vector equality does not create alias authority

Construct a realization assertion with vectors_equal=true.

Expected:

- Q1 identity remains Q1;
- Q1 documentary role remains Governorate / first administrative division;
- STRATUM remains a distinct variable;
- STRATUM design semantics remain BOUNDED_UNKNOWN.

Reject semantic_alias_requested=true.

## T05 — Q1A_PAL routing is documentary, not empirical

Resolve Q1A_PAL at COUNTRY==15.

Expected:

DOCUMENTARY_ROUTING_RESOLVED.

Resolve the same target at another country while providing SYSTEM_MISSING as observed physical state.

Expected:

BOUNDED_UNKNOWN, not NOT_ASKED or inapplicable by inference.

## T06 — Q622C_IRQ routing/topology survives without MR invention

Resolve Q622C_IRQ_* at COUNTRY==7 + SPLIT A.

Expected:

- documentary routing resolved;
- topology SELECT_ALL_THAT_APPLY;
- native SPSS MR metadata false;
- option-like member variables remain distinct.

Reject scalar flattening of the module.

Reject inventing a native SPSS MR set.

## T07 — WT/PSU/STRATUM preservation does not authorize analytic design

Expected:

WT, PSU, STRATUM all preserved as source carriers.

PSU may retain its exact source-native "sampling variable" documentary role.

WT estimand/default use remains BOUNDED_UNKNOWN.

STRATUM design semantics remain BOUNDED_UNKNOWN.

PSU analytic design use beyond the documentary carrier statement remains BOUNDED_UNKNOWN.

Requests for current analytic/design use fail closed.

## T08 — cross-wave semantic leakage fails

Wave 8 authority scope is admitted.

Wave 5 and Wave 2 authority scope requests fail.

Reject reuse of another Arab Barometer wave's code meanings, ID law, routing, weight semantics, or typography as Wave 8 source authority.

## T09 — source SHA drift fails closed

Exact canonical SHA:

a5e83a953f03dd890e076a51da473051f1cfd1ca2e8ab93c2172eeb2517af998

Expected:

correct SHA can create only a source binding with physical_equivalence_claimed=false.

Wrong SHA fails.

This test must not manufacture a physical-equivalence PASS.

## T10 — A/B/C share one semantic owner

A, B, and C must carry the same:

- exact source SHA;
- source-specific realization identity;
- ID/replay law;
- BLOCK_ID physical/semantic law;
- Q1/STRATUM nonalias;
- documentary routing law;
- Q622C topology law;
- bounded UNKNOWNs;
- weight/design nonselection.

Reject any candidate-specific semantic divergence.

## T11 — S35 / R35 scope is frozen

Expected exact edge set:

EC01, EC05, EC07, EC10, EC12, EC14.

Expected R35 hooks:

PRE553_PHYSICAL_METADATA@1.0.0

FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0 for non-direct paths

FIABC_R35_I03 source-scope / expectation / candidate / whole-source receipt schemas.

All hooks remain physical/provenance-only.

Reject an Arab8-only adapter that weakens common edge laws.

## Later execution ordering

Future real qualification should proceed:

canonical source identity

-> ARAB8_SEMANTIC_OWNER_V1 freeze

-> independent Candidate A/B/C physical realization

-> exact R35 physical receipt

-> T01-T11 semantic/negative court

-> common A/B/C terminal comparison.

A semantic PASS cannot repair failed physical equivalence.

A physical PASS cannot authorize unknown BLOCK_ID, WT, STRATUM, PSU, or unjoined routing semantics.

## Current boundary

TESTS_AUTHORED__NOT_EXECUTED.

No source bytes were opened.

No source processing was run.

No A/B/C execution occurred.

No whole-source physical equivalence occurred.

No I05 occurred.

No measured P2X occurred.
