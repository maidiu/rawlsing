# CLOSED35-R2-ARAB2 — Arab Barometer Wave 2 Governed Source-Specific Realization

Repository: maidiu/rawlsing

Base: agent/vozhd-closed35-l2r-r1-fanin-r1 at da33eb6a8225c14eee9490633a3263388dc5536c

Worker branch: agent/rabochii-closed35-r2-arab2-realization-r1

Canonical source: Arab Barometer Wave 2.sav

Canonical SHA-256: 6529841b97bd56463490d810ad24ceaa4866066d12e4651a7081682d413606a1

Authority class: L1_EXECUTION_PACKET_READY__BOUNDED_UNKNOWNS_ALLOWED

## Disposition

PASS at SOURCE_SPECIFIC_REALIZATION_IMPLEMENTED grain.

The governed Arab Barometer Wave 2 law is represented by:

- rawlsing_next/closed35_arab2_realization.py
- rawlsing_next/tests/test_closed35_r2_arab2_realization.py
- the return packet in this directory.

TESTS_AUTHORED__NOT_EXECUTED.

This browser worker did not open Arab Barometer Wave 2.sav, execute source processing, execute Candidates A/B/C, run I05, run whole-source physical equivalence, or run measured P2X.

## Governing source law

The realization pins the exact canonical source SHA and keeps hard replay identity at SOURCE_SHA256+ROW_ORDINAL.

QID remains the questionnaire ID concept documented by the Wave 2 instrument. Neither QID nor the empirically injective COUNTRY+QID combination is promoted to hard replay identity.

The source stays SAV_NATIVE_GOVERNED with source-reported UTF-8. No compatibility-decoding exception is invented.

## Q2062 missing-state separation

The realization explicitly models two distinct physical states already accepted by Authority71/72 evidence:

- true SYSTEM_MISSING;
- ordinary stored numeric 0 carrying the source dictionary label "0. missing".

The ordinary zero remains an ordinary stored value. The source dictionary label is preserved as metadata but is not promoted into documentary semantic authority.

The exact semantic refinement of Q2062 code 0 remains BOUNDED_UNKNOWN.

This is deliberate closure, not a blocker.

## Documentary code authority

Only exact source-native documentary mappings are admitted.

The current owner recognizes the explicit Wave 2 questionnaire meanings for:

- Q101 code 8: I don't know;
- Q101 code 9: Declined to answer;
- Q2062 code 99998: I don't know;
- Q2062 code 99999: Declined to answer.

Q101 code 0 and Q2062 code 0 remain BOUNDED_UNKNOWN. No same-question, same-family, or same-label analogy fills them.

## Ranked challenge and routing topology

Q2061 and Q2062 remain two ordered slots:

1. Q2061 — most important challenge;
2. Q2062 — second most important challenge.

The owner rejects flattening, reordering, or deduplication.

The accepted questionnaire rule that Lebanon recorded only the first challenge is represented as documentary routing authority for the second slot.

Missingness itself never supplies routing authority. Other country/module applicability remains BOUNDED_UNKNOWN until an exact documentary rule is joined.

## WT and SAMP

WT is preserved as a source carrier.

Its estimand, normalization, relation to SAMP, and any default analytical use remain BOUNDED_UNKNOWN. No default weight is selected.

SAMP retains the documentary Main sample versus Additional sample distinction. That fact does not establish a WT estimand or replay identity.

## S35 / R35 binding

Applicable S35 edge classes are exactly:

- EC01 FORMAT_FAMILY_SAV_DTA
- EC05 PHYSICAL_MISSINGNESS_MULTICLASS
- EC09 ORDERED_REPEATED_SLOT_TOPOLOGY
- EC10 FORM_MODULE_SKIP_ROUTING_CARRIERS
- EC12 WEIGHT_DESIGN_MULTIPLICITY_AND_DOMAIN
- EC14 COMPOUND_EDGE_INTERACTION_COURT

The realization binds the accepted R35 metadata, derivative-parentage, and whole-source physical-equivalence receipt schemas without claiming that those receipts have been executed for Arab2.

No Arab2-only physical adapter is created.

## Candidate-neutral owner

A, B, and C must consume one source-specific semantic owner:

ARAB2_SEMANTIC_OWNER_V1

Candidate physical representation may differ later. Source root, missing-state separation, ranked topology, documentary routing jurisdiction, bounded unknowns, replay identity, weight nonselection, and downstream semantic ownership may not differ.

## Synthetic hostile court authored

The synthetic test suite rejects:

- ordinary 0 == SYSTEM_MISSING;
- a source dictionary "missing" label becoming invented code-0 semantics;
- ranked-slot flattening/reordering/deduplication;
- routing inferred from missingness;
- undocumented WT estimand/default selection;
- QID or COUNTRY+QID replacing row-ordinal replay identity;
- source SHA drift;
- Candidate A/B/C semantic-owner divergence;
- S35/R35 scope drift.

Because this worker was restricted to GitHub/browser work, these Python tests were authored but not executed.

## Claim boundary

This PASS does not claim:

- real source bytes executed;
- whole-source physical equivalence passed;
- Candidate A/B/C executed;
- I05 passed;
- source certified beyond accepted authority;
- measured P2X occurred.

## Terminal

CLOSED35_R2_ARAB_BAROMETER_W2_SOURCE_SPECIFIC_REALIZATION_IMPLEMENTED__READY_FOR_ABC_QUALIFICATION
