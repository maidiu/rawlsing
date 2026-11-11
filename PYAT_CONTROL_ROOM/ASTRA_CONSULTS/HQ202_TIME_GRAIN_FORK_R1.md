# ASTRA CONSULT — HQ202 TIME-GRAIN-FORK — R1

Role: Omega / reserved architecture-theory adjudicator

Repository:
maidiu/rawlsing

This is a NARROW reserved question. Do not reopen all of F6/F7.

Current HQ state:
- HQD-125 governs PRE-V3 F6/F7.
- HQ201 ontology conservation return: d3f0619429a400552c2f3c397be57cdfbadb2f54
- HQ202 adjudication: 329a37455151f479886bd3cbb40d4d98d016fb13

## Exact question

For PRE-V3 cross-family temporal comparison, what temporal anchor grain should current authority adopt when survey fieldwork intervals are nonaligned?

Candidate answers include:
A. point-year is the primary identity/comparison grain;
B. fieldwork interval is the primary grain;
C. fieldwork interval is primary, with point-year permitted only as a derived/secondary anchor under explicit conditions;
D. another bounded typed structure.

Do not choose based on implementation convenience.

## Binding constraints

Any answer must preserve:

1. SAME_LABEL != SAME_TEMPORAL_OBJECT.
2. TWO_WAVES_EXIST != TEMPORAL_DIRECTIONALITY_AUTHORITY.
3. no implicit wave-ordinal-to-calendar-year coercion.
4. no silent midpoint-year coercion.
5. same-survey F7 must remain independently realizable.
6. cross-source F6 coexistence must not depend on temporal comparability.
7. nonoverlap and partial overlap must produce typed comparability/noncomparability outcomes, not fabricated coincidence.
8. INTERPOLATION != OBSERVATION; interpolation remains absent unless separately authorized.
9. STRUCTURAL_WORLD_TIME != ACTOR_MEMORY.
10. temporal coincidence does not create causal authority.
11. provenance must preserve actual fieldwork/anchor evidence.
12. F6 + F7 must not become a synthetic panel.

## Evidence to read

Current binding law:
- PYAT_CONTROL_ROOM/24_HQD125_DDM_FUNCTIONAL_CONSERVATION_AND_PREV3_ACCEPTANCE_LAW.md
- PYAT_CONTROL_ROOM/25_HQD125_DDM_FUNCTIONAL_CONSERVATION_CROSSWALK.md

HQ201 conservation packet at:
d3f0619429a400552c2f3c397be57cdfbadb2f54

Especially:
- 05_TEMPORAL_IDENTITY_AND_COMPARABILITY_CONSTITUTION.md
- 06_CROSS_SOURCE_COMPOSITION_CONSTITUTION.md
- 07_F6_F7_COMPOSITION_CASES.json
- 09_MULTI_SOURCE_TEMPORAL_WORLD_OBJECT.md
- 12_ARCHITECTURE_REOPEN_AND_ASTRA_TEST.json
- 13_IMPLEMENTATION_SEQUENCE.md
- 14_FINAL_DISPOSITION.json

Historical functional capital, as needed:
- data/ddm_build_copy/ddm_v553_temporal_identity.py
- data/ddm_build_copy/ddm_v553_temporal_pressure.py
- data/ddm_build_copy/ddm_v553_schema.py
- relevant V551J/V552J cross-wave comparability work

Current ingress:
- rawlsing_next/m1_temporal_v554_admission_dedup.py
- rawlsing_next/pre553_structural_admission.py

## Required analysis

Answer separately:

1. What is the PRIMARY temporal identity anchor for cross-family comparison?
2. May a point year exist as a derived convenience/display/index value? Under what authority and with what non-substitution rule?
3. How should a fieldwork interval be represented: closed interval, bounded interval with uncertainty, another type?
4. What relation is lawful when two intervals:
   - overlap substantially;
   - overlap partially;
   - are adjacent but nonoverlapping;
   - are materially separated;
   - have one unknown endpoint;
   - are known only by year?
5. Does overlap establish comparability, or only temporal co-presence eligibility pending semantic/estimand comparability?
6. What exact typed refusal/noncomparability should result when temporal grain cannot be aligned?
7. Can same-survey F7 continue using its established point-year anchor where the underlying same-family authority supports it, while cross-family composition uses a richer interval grain?
8. Does your answer require architecture reopening, or only a typed anchor/interval owner under the present DAG?
9. What is the smallest current law HQ should freeze now, without overdesigning future temporal ontology?

## Non-goals

Do not:
- design actor memory;
- create interpolation authority;
- create causal-event authority;
- mandate a persistent world container;
- decide unrelated cross-source relation vocabulary;
- reopen the entire DDM architecture.

## Required disposition

Choose exactly one:

- FIELDWORK_INTERVAL_PRIMARY__POINT_YEAR_DERIVED_ONLY
- POINT_YEAR_PRIMARY__INTERVAL_METADATA_SUFFICIENT
- TYPED_DUAL_GRAIN_CONTRACT_REQUIRED
- TIME_GRAIN_FORK_REQUIRES_ARCHITECTURE_REOPEN
- INSUFFICIENT_AUTHORITY__HQ_MUST_PRESERVE_TYPED_NONCOMPARABILITY

Then give:
- the minimal law HQ may freeze;
- what remains intentionally unbound;
- exact implications for composition case C;
- exact implications for same-survey F7;
- whether any new owner is needed and at what grain.

Do not infer authority from historical implementation merely because it exists.
