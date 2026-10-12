# PYAT HQ282 P04 — Dependency and Authority

## Existing owners used (all executed, nothing simulated)

| owner | contract ID | function | role in P04 |
|---|---|---|---|
| N10E | `N10E_EMPIRICAL_POSSIBILITY_SLICE_PROVIDER@1.0.0` | `provide_empirical_possibility_slice` | step 1: P(Y\|A=1) single-conditioner provider |
| C1 | `ANALYTICAL_COMPOSITION@1.0.0` | `compose_positioned_subject_possibility` | steps 2-3: P(Y\|A,B), P(Y\|A,B,C) multi-conditioner composition |
| F8 | `SOURCE_BACKED_POSITIONED_SUBJECT_POSSIBILITY@1.0.0` | `evaluate_positioned_subject_possibility` | consumption: evaluates each step's produced evidence |

## Missing owners (typed HOLDs)

| owner | E01 status | what it would provide |
|---|---|---|
| N9 | `implemented: false` | publication/resolution/lifecycle world-serving; real selected-world join |
| N10W | `implemented: false` | progressive multi-condition world binding |
| G0b | UNISSUED | model-use grant from EE14 competent issuer |
| B5 CURRENT | not selected | CURRENT selection |

## Authority preservation

- No canonical/accepted owner edited
- No self-adoption
- No G0b fabrication
- No B5 CURRENT selection
- No Field Forge
- No temporal/CURRENT
- No actor/V3 state
- No raw SAV/DTA read
- No respondent row leakage

## Immutable references

- canonical: `a70a069fa948e0f3c041b389edcc732b6b948a4f`
- semantic PRE-MAIN: `1f47063c3205a45888b3c55e81e7485943ed1390`
- HQD: `HQD-2026-10-10-280`
