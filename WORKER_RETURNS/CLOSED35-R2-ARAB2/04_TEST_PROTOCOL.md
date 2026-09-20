# CLOSED35-R2-ARAB2 — Synthetic Qualification Test Protocol

Status:

TESTS_AUTHORED__NOT_EXECUTED

This protocol defines source-independent hostile tests for the Arab Barometer Wave 2 realization. The Python tests are checked in under rawlsing_next/tests/test_closed35_r2_arab2_realization.py.

No canonical SAV bytes are opened by these tests as authored.

## T01 — ordinary zero must not equal SYSTEM_MISSING

Construct two synthetic Q2062 observations:

- physical SYSTEM_MISSING;
- ordinary stored numeric 0.

Expected:

- distinct physical states;
- ordinary zero retains raw value 0;
- ordinary zero retains source dictionary metadata "0. missing";
- ordinary zero semantic refinement remains BOUNDED_UNKNOWN.

Reject any normalization in which 0 == SYSTEM_MISSING.

## T02 — dictionary wording cannot invent code-0 semantics

Supply Q2062 ordinary 0 with source dictionary label "0. missing".

Expected:

source label preserved as metadata;

documentary semantic label absent;

semantic status BOUNDED_UNKNOWN.

Reject promotion of source dictionary wording into an exact semantic reason.

## T03 — exact documentary codes do not generalize

Synthetic code-resolution requests:

- Q101 / 8;
- Q101 / 9;
- Q101 / 0;
- Q2062 / 99999.

Expected:

8/9 and the admitted Q2062 special codes resolve only at their exact variable+code joins.

Q101 / 0 remains BOUNDED_UNKNOWN.

Reject family-wide or same-number code inference.

## T04 — ranked challenge topology survives

Expected ordered slots:

Q2061 rank 1 MOST_IMPORTANT_CHALLENGE

Q2062 rank 2 SECOND_MOST_IMPORTANT_CHALLENGE

Reject:

- flattening to an unordered set;
- reversing ranks;
- deduplicating to one challenge slot;
- treating the pair as a native SPSS MR-set merely because it is repeated topology.

## T05 — routing cannot come from absent values

Synthetic unresolved country-module target with SYSTEM_MISSING but no exact documentary route.

Expected:

routing/applicability = BOUNDED_UNKNOWN.

Reject SYSTEM_MISSING -> NOT_ASKED or inapplicable.

Then supply the exact admitted Lebanon Q2062 documentary rule.

Expected:

SECOND_RANK_NOT_RECORDED_BY_INSTRUMENT independent of observed missingness.

## T06 — WT carrier does not authorize an estimand

Expected current owner state:

carrier = WT

carrier preservation = required

estimand = BOUNDED_UNKNOWN

normalization = BOUNDED_UNKNOWN

default use authorized = false

Any request for current weighted use fails closed.

Reject automatic WT selection from field name, completeness, magnitude, or presence.

## T07 — QID cannot become replay identity

Expected hard replay key:

SOURCE_SHA256+ROW_ORDINAL

QID remains a questionnaire ID concept.

COUNTRY+QID empirical injectivity remains evidence only.

Reject either native key as hard replay identity.

## T08 — source SHA drift fails closed

Exact canonical SHA is required.

Expected:

correct SHA admits only a source binding with physical_equivalence_claimed=false.

Wrong SHA fails.

This test must not manufacture a physical-equivalence PASS.

## T09 — A/B/C share one semantic owner

A, B, and C must carry the same:

- exact source SHA;
- source-specific realization identity;
- missing-state law;
- ranked topology;
- documentary routing law;
- bounded unknowns;
- replay identity;
- weight nonselection law.

Reject any candidate-specific semantic divergence.

## T10 — S35/R35 scope is frozen

Expected exact edge set:

EC01, EC05, EC09, EC10, EC12, EC14.

Expected R35 hooks:

PRE553_PHYSICAL_METADATA@1.0.0

FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0 for non-direct paths

FIABC_R35_I03 source-scope / expectation / candidate / whole-source receipt schemas

All hooks remain physical/provenance-only.

Reject an Arab2-only adapter that weakens the common edge laws.

## Later execution ordering

Future real qualification should proceed:

canonical source identity

-> common ARAB2_SEMANTIC_OWNER_V1 freeze

-> independent physical candidate realization

-> exact R35 physical receipt

-> T01-T10 semantic/negative court

-> common A/B/C terminal comparison.

A semantic PASS cannot repair failed physical equivalence.

A physical PASS cannot authorize unknown code-0 semantics or WT estimand.

## Current boundary

TESTS_AUTHORED__NOT_EXECUTED.

No source bytes were opened.

No source processing was run.

No A/B/C execution occurred.

No I05 occurred.

No measured P2X occurred.
