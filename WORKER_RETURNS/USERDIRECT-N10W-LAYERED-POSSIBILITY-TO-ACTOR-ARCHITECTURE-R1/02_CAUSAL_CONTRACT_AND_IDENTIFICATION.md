# Six-grain causal ports, clocks, units, identification and falsifiable DAG

This is a **nonbinding architecture**. No new accepted schema, actor rule, source permission or model policy.

## Time-indexed causal graph (not a mandatory one-event scheduler)

```text
W_t (public historical rule, material world, institutional other actors)
   |                  R_i,t (witnessed objective position/resources)
   +-----> O_i,t <----+   (feasible, unaffordable, blocked, unknown)
                |                       H_i,<t (authenticated living history)
channel/event --> E_i,t (actual exposure) <-- prior acquired social access
                |                                |
                v                                v
       M_i,t = actor-local situated recruitment/interpretation
                ^       (can be plural, opaque, conflicting, unknown)
                |               / 
          O_i,t / H_i,<t / relation & counterpart history
                |
    (O,E,M,H,capacity,actor-local policy, RNG, noaction)
                v
       A_i,t proposed attempt/refusal/nonaction
                |
           CAN/occurrence owner admission + independently selected K_j,t
                v
      V_t realized effect / rejected / unknown / no-effect
                |
        external owner response --> W_(t+1) or explicit unchanged
                |
        authorized V3/relation/epoch owners --> H_i,<=t+1 or explicit unchanged
```

No arrow W→private knowledge without contact/witness; no demographic prior→personal memory; no psyche→W mutation; no actor decision→guaranteed success; no renderer→past rewriting. Social reproduction and continuous activity span intervals and need their own typed input, not synthetic zero-duration occurrences. The K (counterparty) clock must be fixed *per claim*: pre-action commitment to rules/resources differs from post-attempt acceptance/rejection and may be independent of focal actor.

## Contract by causal grain

| Port | Physical/temporal unit | Proposed input → typed output | Owner candidate, clock and required proof | Identification/negative |
|---|---|---|---|---|
| P0 institutional | jurisdiction/site × rule × valid interval × selected as-of | M4/E05R selected exact rule refs, governance/currentness → tri-valued permitted/blocked/unknown, explicit fee/sanction, evidence readset | Pyat competent structural/N9/N10W; effective, publisher release, selection clock; revocation and read scope | TEST_ONLY currently; missing/unpublished/revoked ≠ false |
| P1 material positioned | person objective location/resources/capacities/care/time/other agents × situation/interval | P0 + independently witnessed position/costs → practicum set and opportunity constraints, UNKNOWN on missing budget | SDTF/positioned role owner and Pyat read boundary, source of objective facts, epoch proof | can be set-valued or bounded; a lawfully open route can be unaffordable or informally excluded |
| P2 exposure | particular agent×channel×event×earliest receipt time | opportunity plus communication/participation witness → encountered/no documented contact/unknown, with disclosure owner | CAN/occurrence-epistemic/V3 receiver; actor knowledge clock and access membrane | public existence **does not imply** actor knows; absence of witness ≠ proved absent encounter |
| P3 formation | actor lineage + accepted activities, care/learning/relations over actual event/condition times | admitted genealogy/history/memory/access states → stable-but-revisable capacities and history refs | Sorok V3 ADP (15,16,17,20,21) and relation owners; independent actor histories | initial cohort demographic prior is *not* mature actual person; unknown histories remain unknown |
| P4 situated meaning | actor×concrete encounter×counterpart/practical activity×event clock | P1,P2,P3 plus actor-local concerns and accepted CAN008 rule → actor-local conflicting possible recruitments, partial or unknown consciousness | Sorok CAN008 and exact actor-bound issuer; no direct actor-to-actor private reading | presently NO positive issuer proven; no first-person omniscience |
| P5 attempt/nonaction | actor×candidate action×present constrained slot + counterpart plans | exact admissible alternatives (including wait/refuse/illegal attempt when physically possible), actual formed actor and authorized rule+RNG → *candidate* act or none | Sorok V3/CAN/V2 proposal vs occurrence admission; own stochastic source/seed | simulation frequency ≠ empirically calibrated human probability; illegality may impose risk but not automatic zero |
| P6 consequence & development | admitted occurrence × independent other-agent event × affected exact objects/epochs | admitted actor/world target, counterparty acts → accepted/rejected/partial/nochange; owner-authorized history update or immutable past | SDTF world response, world/relation/V3 durable owners; event commit, source/actor clocks, idempotent cold replay | neither attempted action nor story guarantees outcome; no world rewrite by model |

Each output needs `{type, owner_ref, rule_or_model_ref, exact_producer_refs, source_scope, target_scope, claim_ceiling, effective_at, published_at, requested_asof, actor_access_at_or_null, revocation_epoch, disposition, uncertainty_kind, replay_ref}`. A valid `UNKNOWN` is distinguishable from `FALSE`, `OBSERVED_ZERO`, `VALID_EMPTY`, `UNREACHED`, `REFUSED` and `PARTIAL_ONLY`.

## Separately estimable empirical objects

1. `P(empirical encounter within Δ | actually eligible group, location, reachable communication channels)`: requires joint source-side exposure evidence and all eligible denominator, not public rule existence.
2. `P(attempt by Δ | admitted prior encounter, observed resources, developed-history *measurements*)`: needs longitudinal joint actor-exposure-attempt data, realized attempts, explicit observation/censoring, accessible target sample, time support, external validity. Not identified by separate survey marginals.
3. `P(success | attempted, institution/counterpart state)`: observed attempts including rejection and competing risks, not only recorded successful enrollments.
4. `P(history change | realized event, pre-state, practices, follow-up)`: hard to measure, requires event-causal process and non-event comparison / confounding treatment.
5. `π_sim(candidate action | H,O,E,M,K,rule,seed)`: internally generated probability or rule **only after competent owner issue**; it may be tested without joint real-world fit but must carry `UNVALIDATED_SIMULATION_HYPOTHESIS`. No equating this to 1–4.

**Identified vs unidentifiable:** missing joint actor-route outcome means sharp model-free empirical individual route identification often [0,1]; not 0.5, not average population propensity. F6M structural target submass `q_y` and unknown `u` yield marginal identified interval `[q_y,q_y+u]`. For q=1/8,u=1/2, cell `[1/8,5/8]`. Individual cell upper extrema are generally not jointly attainable across multiple cells. The N10WM source-local `26/31` relates to a different declared conditional target; not route choice. A ratio `attempts/exposed` and `attempts/eligible` answer different, selection-affected questions; neither implies individual future probability. Causality requires exchangeability (or bounded confounding), consistency, positivity, interference/counterpart account, observation and transport assumptions, none supplied by this commission.

## Empirical calibration upgrade, only if possible

First collect independently source/actor-authorized longitudinal eligibility, contact, resource, attempt, refusal, realization, and censoring receipts across diverse positions. Define target estimand and denominator *before* fitting; stratify minorities/unknown and model source missingness. Separate in-sample simulation fit from out-of-sample calibration (temporal holdouts, reliability curves, interval coverage, subgroup validity, cross-world shifts, selective observation); audit counterparty interference. If no qualified sample or transport law, keep null/interval and simulation policy distinct.
