# CLOSED35-R3-ASIAN1 — Asian Barometer Wave 1 Governed Source-Specific Realization

Repository: maidiu/rawlsing

Base: agent/vozhd-closed35-l2r-r1-fanin-r1@da33eb6a8225c14eee9490633a3263388dc5536c

Branch: agent/rabochii-closed35-r3-asian1-realization-r1

Source: Asian Barometer Wave 1.sav

Canonical SHA-256: ac0b8bc1ddb2fa6b952417e35b6379ce6a2cf8596776a43282ba44f48e0ae1a2

Authority class: L1_EXECUTION_PACKET_READY__BOUNDED_UNKNOWNS_ALLOWED

## Disposition

SOURCE_SPECIFIC_REALIZATION_IMPLEMENTED

The accepted Asian Barometer Wave 1 Authority71/72 packet is represented by one candidate-neutral governed realization in:

- rawlsing_next/closed35_asian1_realization.py
- rawlsing_next/tests/test_closed35_r3_asian1_realization.py

No local or raw survey carrier was opened. No real source processing was executed. No measured P2X was run. A/B/C were not executed.

Synthetic tests were authored but browser/GitHub tooling did not execute Python:

TESTS_AUTHORED__NOT_EXECUTED

## Governing realization law

### Exact source and reader configuration

Admission is exact-source-bound to:

- Asian Barometer Wave 1.sav
- SHA-256 ac0b8bc1ddb2fa6b952417e35b6379ce6a2cf8596776a43282ba44f48e0ae1a2
- SAV_SOURCE_DECLARED_BIG5
- no source-specific compatibility override

The accepted packet freezes 12,217 rows and 217 variables under the BIG-5 source-declared reader path. Readable decoded text is physical reader evidence only. It does not become questionnaire/codebook authority, and this realization does not normalize or harmonize decoded text from later Asian Barometer waves.

### Replay identity

The hard replay identity is exactly:

(source SHA-256, zero-based source row ordinal)

idnumber, country, and country+idnumber remain source-local physical attributes. Authority71 observed idnumber as globally noninjective and country+idnumber as injective in this exact source snapshot, but neither is promoted to hard replay, cross-wave, longitudinal, or global respondent identity.

### Typed missingness

The accepted packet records:

- 284,794 user-missing cells
- 720,729 system-missing cells
- 199 variables with missing declarations
- q001 user-missing values 98/99, including a governed q001=98 witness
- q018_1 system-missing witness

Physical stored value, missing declaration, and physical missing-state classification remain separate fields. A positive/numeric user-missing code is not converted into an ordinary substantive response by magnitude; system missing is not collapsed with user missing; and no decoded label is promoted to semantic DK/refusal/not-asked authority.

The exact semantic mapping of Wave-1 response-state codes remains BOUNDED_UNKNOWN.

### Nine weights

All nine packeted carriers remain individually preserved:

w_jp, w_hk, w_kr, w_cn, w_mo, w_ph, w_tw, w_th, w_all

No carrier is selected as a default. Exact estimand, normalization, population/domain, combination rule, PSU/strata relation and variance design remain BOUNDED_UNKNOWN.

### Ranked q097

The ordered topology is preserved as:

q097_1 -> q097_2 -> q097_3

Packet ordinals 135, 136, 137 remain distinct. Flattening, reordering, deduplicating or scalarizing the ranked slots is forbidden.

### Routing and geography

Exact Wave-1 questionnaire/codebook/routing authority was not recovered by Authority71. Missingness, decoded labels, country codes and observed support therefore cannot mint routing applicability. Unresolved routing remains BOUNDED_UNKNOWN.

The raw country and level3 carriers remain source-local coordinates. No Wave-4/Wave-5 geography scheme or semantics are imported.

### Candidate neutrality

A, B and C must consume one immutable source-specific realization identity. Candidate identity may not alter:

- BIG-5 reader authority status;
- replay identity;
- typed missing-state distinctions;
- ranked q097 topology;
- the nine distinct weight carriers;
- geography scope;
- routing/weight bounded UNKNOWNs;
- decoded-text authority boundary.

Different later physical realization strategies may be qualified. Different source semantics are divergence.

## S35 / R35 binding

Applicable S35 edge classes are frozen to:

EC01; EC02; EC05; EC07; EC09; EC12; EC13; EC14

EC14 is composition only and creates no special adapter or semantic authority.

The realization binds the accepted R35 seams:

- I01 physical metadata: PRE553_PHYSICAL_METADATA@1.0.0
- I02 derivative parentage: FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0 for any non-direct raw carrier
- I03 whole-source physical scope / expectation / candidate realization / equivalence receipt schemas

Required physical dimensions include reader configuration, decoded-text evidence, physical missing states, variable order, raw storage, row replay, native-ID evidence, ordered repeated topology, weight/design carriers and source-local coordinate carriers.

This browser implementation does not materialize an R35 whole-source physical-equivalence receipt.

## Bounded UNKNOWN set preserved

- exact Wave-1 questionnaire/codebook item semantics
- exact semantic mapping of declared user-missing response codes
- exact routing/applicability rules
- exact roles/estimands/normalization/default use for all nine weights
- exact survey-design semantics
- cross-wave/instrument geography reconciliation
- native-ID fieldwork/global identity semantics beyond source-local physical evidence

## Proof boundary

This return proves only that a source-specific candidate-neutral realization and synthetic rejection court have been implemented on the requested branch.

It does not claim:

- real-source execution
- whole-source physical-equivalence PASS
- ABC execution PASS
- I05 PASS
- measured P2X
- source certification beyond accepted Authority71/72 preparation and L1 launch class

## Terminal

CLOSED35_R3_ASIAN_BAROMETER_W1_SOURCE_SPECIFIC_REALIZATION_IMPLEMENTED__READY_FOR_ABC_QUALIFICATION
