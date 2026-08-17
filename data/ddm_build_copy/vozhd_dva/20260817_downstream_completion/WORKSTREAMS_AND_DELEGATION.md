# Workstreams and Delegation

## Coordination model

Vozhd Dva owns cross-stage semantics, integration order, gate decisions, and worker partitioning. Rabochiis receive bounded write domains and explicit acceptance criteria. Workers do not independently redefine neighboring stage contracts.

Parallelism is encouraged where dependencies are clear. Shared interfaces are coordinated centrally before conflicting implementations are launched.

## Prong 1 — Cross-stage requirements / vertical capability map

Purpose: define only the information needed to prevent downstream starvation and rework.

Outputs:
- capability matrix;
- V553→V558 stage responsibility assignments;
- V558→V3 consumer requirements;
- V3→V2 boundary requirements;
- five acceptance slices.

Good Rabochii task: inspect specific stages and report producer fields, transformations, losses, and downstream requirements. Primary write authority remains Vozhd Dva until shared contracts are frozen.

## Prong 2 — V553 entry repair and temporal semantics

Immediate known defect: activate `POSTG5-004` and repair V553 to consume canonical V552J outputs rather than the obsolete structural handoff packet.

Then inspect temporal semantics needed by all five vertical slices: comparability, persistence, drift, rupture, absence over time, uncertainty, structural dimensions, and provenance.

Can run concurrently with Prong 3 requirements analysis, but implementation must obey the cross-stage matrix.

## Prong 3 — V554–V556 semantic deepening

Purpose: turn current bounded scaffolds into useful structural-prior transformations without instantiating biography or psyche.

Subdomains may be delegated separately once interfaces are clear:
- V554 structural/seed affordance semantics;
- V555 mediation topology and conditions;
- V556 pressure-flow / attractor topology and requirements.

Workers must preserve explicit source/provenance/uncertainty lineage and cannot generate actor-specific facts.

## Prong 4 — V557–V558 boundary completion

Purpose: convert deepened structural priors into a controlled runtime-consumption boundary.

Work includes:
- lawful representation of prior information;
- forbidden-inference enforcement;
- source/generated separation;
- runtime input normalization;
- V3 consumer contract tests.

This prong can begin against mocks/reference packets before upstream semantic completion, then bind to real upstream outputs during integration.

## Prong 5 — Vertical fixtures and test harness

Purpose: make cross-stage continuity executable rather than documentary.

Build a small finite test set covering:
1. temporal persistence/drift/rupture;
2. contradictory inter-strata pressure;
3. mediation plus buffering/amplification;
4. pressure-flow plus attractor prerequisites;
5. uncertainty/absence/noncomparability/forbidden inference.

This prong should begin early and can be delegated independently because tests expose what implementation prongs must satisfy.

## Prong 6 — Horizontal source qualification

Begins only after representative vertical slices work. Workers can then own source-family/wave qualification shards and report concrete common-model failures rather than redesigning stages independently.

## Prong 7 — V3 runtime rebuild

Can begin in parallel only after the V558 information contract is stable enough to mock. Early work should focus on runtime state/event architecture and causally attributable transitions, not binding to unfinished V5 schemas.

## Prong 8 — Genealogy / household runtime

Can overlap late V3 work once actor state and temporal event interfaces exist. Owns Parent 1 / encounter / Parent 2 / relationship / household / child orchestration.

## Prong 9 — V2 and app/demo

V2 contract/design may proceed against mocked V3 state while V3 is implemented. Full integration waits for stable event/state APIs. App/demo work should prioritize a polished demonstrable vertical path over broad feature expansion.

## Worker launch rules

Every Rabochii launch must specify:
- base branch and target integration branch;
- exact write domain;
- exact issue/capability IDs;
- upstream contracts that bind;
- downstream requirements that must remain satisfied;
- tests/acceptance evidence required;
- explicit out-of-scope areas;
- required machine-readable report.

Workers encountering a cross-cutting ambiguity must return a proposed ruling or `PARTIAL_AWAITING_CROSS_HOOK`; they must not invent downstream semantics to make their local task green.
