# Vozhd Dva — W1 First-Batch Interim Adjudication Ruling

**Status:** `BINDING_W1_FIRST_BATCH_INTERIM_ADJUDICATION`  
**Date:** 2026-08-18  
**Whole-machine architecture:** `CLOSED`  
**W0 authority foundation:** `CLOSED`  
**Verdict:** `W1_FIRST_BATCH = 5_ACCEPTED__1_RETURN_FOR_FIX_ACTIVE`

## 1. Court scope

This ruling adjudicates the six dependency-satisfied first-batch W1 authority/canonicalization cells released from exact common base:

`10a8e60f171e3a70bf48336fff73d37040cc1b93`.

The court is authority-only. No production implementation is released by this ruling.

## 2. Accepted cells

| Cell | Authority | PR | Reviewed head | Merge |
|---|---|---:|---|---|
| W1-01 | ADP-002 / V555 mediation-route rule registry | #98 | `cdf93f6f9b47c46084628088bebe5e204b3bde2f` | `096c139947855e5a55abd9bc5a31eb8e6596c079` |
| W1-04 | ADP-017 / actor knowledge-belief-accessibility | #99 | `614775fa05c5d904adff4b53f353637b869e6842` | `3d8cab238eca1c1f694eb778e39566bf3aaaf03a` |
| W1-05 | ADP-021 / hybrid causal scheduler + slow cadence | #101 | `c83f0cfe2ee9039c7f8e3cf90b94941a1c186c5c` | `72fe87268296f35f7aed30330f690880569ee3f1` |
| W1-03 | ADP-010 / opportunity-encounter-exposure | #102 | `dd7720bf7201eb215e8a612cbd70952a728ca37b` | `28d504cb7d1b8e45a9f9085a465e50e41686bae6` |
| W1-02 | ADP-009 / structural-position generation + mobility | #103 | `ef7b7cc8d03c3e0ecc2f73da39632b2cb882645e` | `1e66221fec9b645ac41c28ea290f239fb83116e2` |

All five accepted PRs changed exactly the two authorized `AUTHORITY.md` / `AUTHORITY.json` files for their cell. Required historical-archive cells directly verified:

`Rawlsing_code_bundle_staging.zip`

SHA256:
`953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`.

## 3. Binding accepted results

### ADP-002 / MUST-002

`V555_MEDIATION_ROUTE_RULE_REGISTRY@1.0.0` is accepted.

First-tranche route authority is deliberately narrow:
- one exact V554 F1 per atomic V555 route;
- one exact already-governed upstream structural-channel identity may serve as the mediation locus under the accepted rule;
- absence of such exact channel identity yields `NO_GOVERNED_ROUTE_AUTHORITY` rather than invention;
- unary route effects remain `VALID_EMPTY` in tranche one;
- no numeric route semantics;
- no V556 cross-route topology;
- no actor traversal/history.

This closes ADP-002 as an authority dependency. It does not release V555 production.

### ADP-009 / MUST-009

`V3_STRUCTURAL_POSITION_GENERATION_MOBILITY_RULE@1.0.0` is accepted.

Binding law:
- structural prior != generated actor position fact;
- position facts are actor-specific `GENERATED_RUNTIME_FACT` records with append-only prospective position events;
- no geography/prevalence/demographic shortcut to actor position;
- raw prevalence is never silently converted into probability/weight;
- actor-scoped ADP-020 randomness selects only among already-lawful candidates;
- multiple lawful candidates without governed selection semantics remain unselected;
- mobility is prospective causal history and never rewrites the past;
- committed generated-position binding changes trigger prospective ContextResolver re-resolution without transferring position ownership to V558.

### ADP-010 / MUST-010

`V3_OPPORTUNITY_ENCOUNTER_EXPOSURE_REALIZATION_RULE@1.0.0` is accepted.

Binding noncollapse:

`AVAILABLE != OPPORTUNITY != ENCOUNTER != EXPOSURE`.

Co-location or co-presence is not encounter. Encounter is not exposure. Exposure is not route traversal, response, memory, belief, relationship, attractor movement or developmental change. Nonoccurrence and zero encounter/exposure counts are lawful.

### ADP-017 / MUST-017

`V3_ACTOR_KNOWLEDGE_ACCESSIBILITY_RULE@1.0.0` is accepted.

Binding noncollapse:

`objective fact != causal memory != memory accessibility != actor epistemic stance != current claim accessibility != first-person claim permission != V2 expression`.

Actor opacity is machine-enforceable. Objective truth never automatically becomes actor knowledge. Memory never automatically becomes articulation permission. `ActorAccessibleRenderEnvelope` is allowlisted and immutable; V2 may narrow but never widen it.

### ADP-021 / MUST-021

`V3_HYBRID_CAUSAL_SCHEDULER_POLICY@1.0.0` is accepted.

Binding scheduler law:
- six trigger classes remain distinct;
- explicit dependency outranks class rank;
- noncommuting same-time causal peers without governed order fail closed as `AMBIGUOUS_SAME_TIME_CAUSAL_ORDER`;
- every causal mutation reopens same-time dependency/barrier evaluation before later context-consuming work;
- no annual ontology, hidden wall clock, filler tick/event or ungoverned slow cadence;
- CAN-014 pure-derived scheduling remains separate;
- quiescence is lawful.

## 4. RETURN_FOR_FIX — CAN-001 / PR #100

PR #100 remains open/draft on:

`agent/vozhd-dva-w1-can-001-v554-applicability`

Reviewed head:
`b2359c57ec084483803a27fc206536b02f9dd3ea`.

Disposition:
`RETURN_FOR_FIX__NARROW_K01_RUNTIME_POSITION_OWNER_BINDING_PRODUCER_CANONICALIZATION`.

The result correctly canonicalizes the nine accepted ADP-001 F2 semantic kinds and introduces no new F2 meaning. The defect is limited to K01:

`V554-F2-K01-RUNTIME-POSITION-REQUIRED` is hard-coded with both `resolution_owner` and `binding_producer` equal to `V3_GENEALOGY`.

That is too narrow after accepted ADP-009. Generic actor structural-position generation/mobility is now explicitly owned by the V3 Actor Developmental Causality Engine under ADP-009. Genealogy/relationship/household generation remains a separate later authority. K01 must therefore accept the exact separately-authorized generated-position binding from its actual owning V3 authority/interface, with ADP-009 as the currently accepted generic position owner, rather than making genealogy the universal producer.

K01 semantic ownership remains V554. ContextResolver remains the downstream evaluator. CAN-001 acquires no actor-position semantics.

The exact narrow continuation instruction is recorded on PR #100 as top-level Vozhd comment `5324802520`.

## 5. Dependency consequences

The accepted results now satisfy these authority dependencies:

- ADP-002 accepted -> ADP-003 becomes dependency-satisfied when its scheduled wave opens;
- ADP-009 accepted -> ADP-007 position dependency satisfied;
- ADP-009 + ADP-010 + accepted ADP-020 -> ADP-015 dependency set satisfied;
- ADP-010 + ADP-002 satisfy two of ADP-011's three dependencies; ADP-003 remains required;
- ADP-017 accepted -> ADP-022 becomes dependency-satisfied when W2 opens;
- ADP-021 closes MUST-021 itself but V3 implementation remains gated by its other CAN/MUST/EXT authorities;
- CAN-001 remains blocking for W2 V554 semantic implementation until its narrow continuation is accepted.

Wave labels remain planning gates in addition to dependency truth; this ruling does not pull W2/W3 cells forward merely because a dependency is now satisfied.

## 6. Governing-Spirit court

All five accepted authorities pass `RAWLSING_GOVERNING_SPIRIT.md` under the binding authority hierarchy.

- ADP-002 uses minimum exact mediation machinery and lawful emptiness rather than invented route effects.
- ADP-009 preserves historically caused but non-inevitable social position and divergent lives under the same field.
- ADP-010 preserves contingent encounter/nonoccurrence rather than structural possibility becoming biography.
- ADP-017 preserves determination without transparency and actor opacity without inventing false beliefs.
- ADP-021 preserves causal history and genuine same-time ambiguity rather than imposing a convenient total timestep order.

The Governing Spirit supplied no missing semantic rule.

## 7. Next W1 capacity release

While CAN-001 is corrected, the five remaining available Rabochii slots should execute the independent W1 V3 mechanism canonicalizations:

- CAN-008 — actor response / pressure-flow / metabolism;
- CAN-009 — material / organismic / vitality;
- CAN-010 — need / expectation / striving;
- CAN-011 — framework / buffer / crack / wound / practice / infrastructure middle state;
- CAN-012 — rupture / metabolization.

All five are canonicalization, not new-authority creation. All require direct historical V3 source inspection. Historical machinery may be preserved only where it fits accepted V3 architecture; legacy fields/formulas do not become terminal ontology merely by existing.

## 8. Final token

`W1_FIRST_BATCH = 5_ACCEPTED__1_RETURN_FOR_FIX_ACTIVE`