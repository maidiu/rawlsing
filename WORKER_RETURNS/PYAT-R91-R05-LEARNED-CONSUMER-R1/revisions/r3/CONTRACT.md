# R91 R05 R3 actual graph validation contract

Startup `d9e809094a2398d20273605afada8ad9b81a3dda`; same OpenCode author.
Settled in-scope R05V R2 repair; no new science/architecture.

## Graph validation

`NativeProductGraph` candidates must be actual `AnalyticalCompositionResult`
objects. The consumer now derives an authoritative graph from native component
fields and rejects/refuses inconsistencies:

- joint component count/order must equal the component target topology arity,
  component count and order semantics;
- direct route must carry no discovery/recursive labels;
- discovery route must carry receipt + frontier and no recursive labels;
- recursive route must carry handoff + lineage;
- duplicate component hashes refuse;
- graph values returned are derived from the authoritative component fields,
  not copied caller metadata.

E41 extension input must be the actual
`EmpiricalPossibilitySliceExtensionResult`, its composition must belong to the
graph, its route must be one of the accepted E41 routes, and its consumer result
hash must equal the graph component consumer hash. Fake objects/routes refuse.

## Status jointness

Exact support requires `producer_fact_state == SUPPORTED` AND
`analytical_state == SUPPORTED` AND denominator equal to evidence raw support.
Disagreement or inconsistent denominator returns a typed state from the actual
analytical state (ZERO_SUPPORT/VALID_EMPTY/UNKNOWN etc.), preserving denominator,
cells, Z16 and `z_unresolved`; never false exact support.

## Other requirements

- Remove duplicate/shadowed consumer definitions; one active implementation.
- Preserve actual M01->M1->M2->C1->N10E positive, E41 direct, typed statuses,
  author 36 tests, R05V R1/R2 probes, provider/C1 regressions where material is
  available.
- Add actual multi-component graph test (two distinct actual composition
  results) and duplicate/forged/fake E41/mixed-state refusals.
- No owner/evaluator/R03/R08 edit, no R04 dependency, no full R06 service.

## Limits

No original source/science, F6/F7, CI/prod, N11/N12, Sorok, J52/W52 authority.
Full live J42/P41/E04 NOT_REACHED. Author candidate only; distinct review follows.
