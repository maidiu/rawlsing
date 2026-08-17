# Wave 0 Intake / Synchronization Ledger

**Owner:** Vozhd Dva  
**Status:** CLOSED_TO_MAIN  
**Canonical closeout commit:** `1bbfb62791a583ab9ab7d21f5a0d76b4617b8f89`

## Worker intake table

| Worker | Branch | PR | Final Vozhd disposition | Integration state |
|---|---|---:|---|---|
| R0-01 | `agent/vozhd-dva-r0-01-v553-v554` | #39 | `ACCEPT` after narrow fail-closed correction | merged to Wave-0 integration, then main |
| R0-02 | `agent/vozhd-dva-r0-02-v555` | #35 | `ACCEPT_WITH_FOLLOWUP` | merged to Wave-0 integration, then main |
| R0-03 | `agent/vozhd-dva-r0-03-v556-attractor` | #36 | `ACCEPT_WITH_FOLLOWUP` | merged to Wave-0 integration, then main |
| R0-04 | `agent/vozhd-dva-r0-04-runtime-contract` | #38 | `ACCEPT_WITH_FOLLOWUP` | merged to Wave-0 integration, then main |
| R0-05 | `agent/vozhd-dva-r0-05-vertical-harness` | #37 | `ACCEPT` | merged to Wave-0 integration, then main |

## R0-01 / POSTG5-004 closeout

`POSTG5-004` is closed on the V553 consumer side. V553 now consumes and verifies the current canonical V552J publication rather than depending on the obsolete structural handoff packet. The boundary distinguishes valid-present, valid-empty, missing, unreadable/corrupt, schema-invalid, and integrity-invalid states and fails closed before V553 temporalization on invalid publication.

## Accepted Wave-0 evidence

### W0-E01 — mediation starvation begins around V554→V555
R0-02 and R0-05 independently show that current V555 does not preserve enough temporal/pressure/contradiction/provenance identity or express typed mediation effects needed by V556.

**Ruling:** accepted as evidence; replacement grain deferred to schematic S02.

### W0-E02 — V556 pressure-flow/attractor semantics are scaffold-grade
R0-03 and R0-05 show that generic route/candidate surfaces do not yet provide stable provenance-bearing pressure-flow and attractor-prerequisite identity.

**Ruling:** accepted as evidence; exact topology deferred to S03. Actor-specific route realization and Enneagram-like attractor formation remain V3 jurisdiction.

### W0-E03 — V557/V558 preserve governance better than causal content
R0-04 and R0-05 show that the current renderer/runtime boundary can enforce separation rules while still starving future V3 of lawful structural-prior semantics.

**Ruling:** accepted as evidence; S04–S06 determine the serial preservation/normalization contract.

### W0-E04 — vertical semantic court is accepted
R0-05 added the deterministic five-slice continuity harness with worker-reported `12 passed, 5 xfailed`. The XFAILs are declared current production gaps, not relaxed acceptance.

**Ruling:** accepted as standing test authority; its reference packets are not production ontology.

## Unresolved grains handed to schematics

Wave 0 intentionally does not freeze:
- exact V552J→V553 semantic intake/output grain beyond the corrected trust boundary;
- exact V553→V554 affordance handoff;
- exact V554→V555 mediation grain;
- exact V555→V556 pressure-flow topology grain;
- exact V556→V558 runtime-prior preservation shape;
- exact V558→V3 bundle/API grain.

These are adjudicated serially by S00 through S07.

## Promotion law

Wave-0 worker findings are evidence inputs to `schematics/`; they are not direct implementation specifications. One seam is active at a time. Independent perspectives may run concurrently inside that seam, and only the Vozhd synthesis of that seam becomes input law for the next.
