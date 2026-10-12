# E03 — Actual call graph

Real invocations only. Synthetic world (58 respondents) is the only source.

```
build_synthetic_world()                        [fixture only: i03._build_source 58 rows, 1 risk set,
        │                                       frozen query authority, registry, pairing, model rule]
        │
        ▼ STEP 1  P(Y|A=1) ──── PRODUCTION ──────────────────────────────────────────────
_joint_predicate(A=1)   : owner i03._predicate — response leaf A==1
_producer_query(Y)      : owner i03._query → EmpiricalQuerySpec (domain {0,1}, risk R, RAW)
_consumer_query(step1)  : fx.make_multi_conditioner_consumer_query — 1 binding (A)
_witness(step1)         : fx.build_witness_for_binding — closed custody identity
        │
        ▼
provide_empirical_possibility_slice(            [owner N10E: pre553_empirical_possibility_provider]
  repository, empirical_query, predicate,
  authority_registry, release_refs,
  consumer_query, model_rule, witness)
  → provider_state = EXACT_SUPPORTED_SLICE_PRODUCED
  → composition.raw_denominator_support = 32
  → cells {0:14, 1:18}   P(Y=1) = 9/16
  → produced_evidence (possibility slice evidence, owner-generated)
        │
        ▼ CONSUMPTION (distinct invocation)
evaluate_positioned_subject_possibility(        [owner F8: source_backed_positioned_subject_possibility]
  query, model_rule, evidence=(step1.produced_evidence,))
  → EXACT_SUPPORTED / EXACT_POSITIONED_STRATUM_SUPPORTED
  → consumed ref == produced ref (verified)

        ▼ STEP 2  P(Y|A=1,B=1) ─ PRODUCTION ─────────────────────────────────────────────
_joint_predicate(A=1,B=1): owner i03._predicate — AND(leaf A==1, leaf B==1) hash-sorted
_consumer_query(step2)  : fx.make_multi_conditioner_consumer_query — 2 bindings (A,B)
_witness(step2)         : fx.build_witness_for_binding — per-conditioner custody
        │
        ▼
compose_positioned_subject_possibility(         [owner C1: pre553_analytical_composition]
  repository, empirical_query, predicate, ...)
  → producer_route DIRECT_I03_TO_POSITIONED_SUBJECT, analytical SUPPORTED
  → denominator 16, cells {0:6, 1:10}, P(Y=1) = 5/8
        │
        ▼ CONSUMPTION (distinct invocation: F8 on step2.produced_evidence)
  → EXACT_SUPPORTED

        ▼ STEP 3  P(Y|A=1,B=1,C=1) ─ PRODUCTION (same C1 owner, 3 bindings) ─────────────
  → denominator 8, cells {0:2, 1:6}, P(Y=1) = 3/4
        │
        ▼ CONSUMPTION (distinct invocation: F8 on step3.produced_evidence)
  → EXACT_SUPPORTED
```

## Owner-by-owner ledger

| call | owner module | used for | calls | logged as |
|---|---|---|---|---|
| `provide_empirical_possibility_slice` | `pre553_empirical_possibility_provider` | step 1 production (single conditioner) | 1 | `provide_empirical_possibility_slice` |
| `compose_positioned_subject_possibility` | `pre553_analytical_composition` | steps 2–3 production (multi-conditioner) + witness verification in probes | 2 (+ probes) | `compose_positioned_subject_possibility` |
| `evaluate_positioned_subject_possibility` | `source_backed_positioned_subject_possibility` | consumption of each produced evidence object | 3 standing (+ hostile probes) | `evaluate_positioned_subject_possibility` |
| `execute_empirical_query` (internal) | `pre553_empirical_query` | producer fact inside C1/N10E | owner-internal | not separately logged (owner fact) |

## What the candidate itself adds (and only this)

1. **Synthetic world** (`synthetic_world_rows`, `build_synthetic_world`) — one bounded fixture, one risk identity, `real_subject: False`.
2. **Route selection** — step 1 via N10E (single binding); steps 2–3 via C1 multi-conditioner, because N10E's `_single_binding` refusal is the exact edge (demonstrated).
3. **Joint predicate assembly** — canonical hash-sorted AND of owner response leaves.
4. **Production/consumption separation** — F8 receives the *produced object*; identity equality asserted.

## What no component claims

- N9 publication/resolution/lifecycle join — absent in repo, recorded ABSENT, not fabricated.
- N10W progressive world binding — absent in repo, recorded ABSENT, not fabricated.
- Any G0b issuance, model-use grant, B5 CURRENT selection, Field Forge, temporal/CURRENT, actor/V3 state.
- Any real CURRENT designation for the synthetic world.