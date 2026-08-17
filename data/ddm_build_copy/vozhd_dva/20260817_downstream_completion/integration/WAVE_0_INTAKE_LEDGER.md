# Wave 0 Intake / Synchronization Ledger

**Owner:** Vozhd Dva  
**Purpose:** track worker returns, accepted findings, cross-hooks, collisions, and merge state without letting worker-local conclusions silently become system law.

## Worker intake table

| Worker | Branch | PR | Worker status | Vozhd disposition | Integration state | Blocking cross-hook |
|---|---|---:|---|---|---|---|
| R0-01 | `agent/vozhd-dva-r0-01-v553-v554` | #39 | COMPLETE_WITH_FINDINGS / fix pending | `RETURN_FOR_FIX` | NOT_MERGED | fail-closed canonical artifact integrity |
| R0-02 | `agent/vozhd-dva-r0-02-v555` | #35 | COMPLETE_WITH_FINDINGS | `ACCEPT_WITH_FOLLOWUP` | MERGED `ba593a838554e485e159c462fac8c625baf3eda4` | object grain deferred to S02 |
| R0-03 | `agent/vozhd-dva-r0-03-v556-attractor` | #36 | COMPLETE_WITH_FINDINGS | `ACCEPT_WITH_FOLLOWUP` | MERGED `d17d066495095332bbcc014bd81e23fba828bbaa` | object grain deferred to S03 |
| R0-04 | `agent/vozhd-dva-r0-04-runtime-contract` | #38 | COMPLETE_WITH_FINDINGS | `ACCEPT_WITH_FOLLOWUP` | MERGED `741dd2e50051f8bef7dc65e97494a2f60a38fed6` | boundary grain deferred to S04–S06 |
| R0-05 | `agent/vozhd-dva-r0-05-vertical-harness` | #37 | COMPLETE_WITH_FINDINGS | `ACCEPT` | MERGED `71035e360efeea033addcc317d23b9a7f21de02e` | five production-gap XFAILs remain |

Individual review authority lives under `reviews/WAVE_0/`.

## R0-01 closeout — INT-W0-001

- **Producer:** canonical V552J
- **Consumer:** V553
- **Law:** repair obsolete V553 consumer expectation on V553 side; do not recreate legacy V552J packet.
- **Accepted direction:** consume canonical V552J input/handoff surfaces and preserve upstream governed identity.
- **Outstanding defect:** canonical artifact reads must distinguish missing, unreadable/corrupt, schema-invalid, and valid-empty states and fail closed on integrity failure. Path existence alone cannot establish a valid consumer surface.
- **Status:** RETURNED_TO_R0_01; S00 waits for closeout.

## Accepted Wave-0 evidence

### W0-E01 — mediation starvation begins around V554→V555

R0-02 and R0-05 independently show that current V555 does not preserve enough temporal/pressure/contradiction/provenance identity or express typed mediation effects needed by V556.

**Ruling:** accepted as evidence of a seam problem; exact replacement object grain is deferred to serial schematic session S02.

### W0-E02 — V556 pressure-flow/attractor semantics are scaffold-grade

R0-03 and R0-05 independently show that generic `route_axis_*`/candidate surfaces do not yet provide stable, provenance-bearing pressure-flow and attractor-prerequisite identity for downstream use.

**Ruling:** accepted as evidence; exact topology/object grain is deferred to S03. Actor-specific route realization and Enneagram-like attractor formation remain V3 jurisdiction.

### W0-E03 — V557/V558 preserve governance better than causal content

R0-04 and R0-05 show that the current renderer/runtime boundary can enforce separation rules while still starving future V3 of lawful structural-prior semantics.

**Ruling:** accepted as evidence; S04–S06 must determine the serial preservation/normalization contract.

### W0-E04 — vertical semantic court is accepted

R0-05 added a deterministic five-slice continuity harness with worker-reported `12 passed, 5 xfailed`. The XFAILs represent declared current production gaps rather than test weakening.

**Ruling:** accepted as standing acceptance evidence. Reference packets are test authority only, not production ontology.

## Interface collisions / unresolved grains

Wave 0 intentionally did not freeze the following:
- exact V554→V555 mediation object grain;
- exact V555→V556 pressure-flow graph/topology grain;
- exact V556→V558 runtime-prior preservation shape;
- exact V558→V3 bundle/API grain.

These are now adjudicated by the schematic transformation layer, serially from S00 through S07.

## Schematic handoff law

Wave-0 findings are evidence inputs to `schematics/`; they are not direct implementation specifications.

Progression:
`R0-01 integrity closeout → S00 breakout/synthesis → S01 breakout/synthesis → ... → S07 breakout/synthesis`

Only one seam is active at a time. Independent forward/backward/critic workers may run concurrently inside the active seam. The accepted output of each seam becomes the frozen upstream input law for the next.

## Implementation promotion rule

No Wave-0 proposed object grain becomes production authority merely because its report PR was merged. Implementation packets are created only after the relevant schematic seam has been synthesized by Vozhd Dva.
