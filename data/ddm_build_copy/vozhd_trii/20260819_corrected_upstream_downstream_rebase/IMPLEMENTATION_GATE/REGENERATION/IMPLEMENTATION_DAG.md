# VOZHD TRII — IMPLEMENTATION DAG

Status: `PREPARATORY_ONLY__SEMANTIC_DEPENDENCY_IS_NOT_BLANKET_SCHEDULING_DEPENDENCY`

Production baseline: `0777a34e50221bde6801dbaca26c058a7350c9e8`  
Frozen reclosure: `c4a3524fc21a90940701b2b5421cf53fee047781`

## Semantic DAG

```text
IG-M1  ──> IG-M2 ──> IG-M3 ──┐
  │         │         │        │
  └─────────┴─────────┴──────> IG-M4 ──> IG-M5 ──> IG-M6 ──┐
                                                             ├──> IG-INTEGRATION
IG-PSEPF ────────────────────────────────────────────────────┘
```

### Edge meanings

- `IG-M1 -> IG-M2`: V555 consumes exact accepted V554 F1/admission semantics; M2 may not redefine M1.
- `IG-M2 -> IG-M3`: V556 participants are exact canonical V555 route identities; M3 may not re-ID M2 output.
- `IG-M1/M2/M3 -> IG-M4`: V557 publication governance may receive directly authorized producer objects from the lawful producer stage. M4 must preserve producer-specific typed state, permission ceiling, identity and interpretation-critical closure.
- `IG-M4 -> IG-M5`: Context resolution consumes exact immutable V558 repository closure; M5 may not collapse V557 publication authority into V558 repository identity.
- `IG-M5 -> IG-M6`: V3/V2 receptor behavior consumes an actual runtime resolved structural peer where required; it may not fabricate one or substitute persistence evidence.
- `IG-PSEPF -> IG-INTEGRATION`: the current zero-positive actor-transition registry is an independent noncollapse proof obligation. It is not a causal bridge from structural/empirical truth to actor state.
- `IG-M6 -> IG-INTEGRATION`: final integration can accept only after current actor-safe claim/envelope ingress and actor-accessible separation have passed.

## Parallelism law

Launch dependency is not final adjudication dependency. The following work may proceed in parallel after explicit activation if exact repository write surfaces do not overlap:

- seam-local negative fixture construction for M1–M6;
- replay fixture construction for already frozen upstream identities;
- IG-PSEPF zero-positive enforcement and tests;
- M4 standalone-carrier fixtures that use frozen producer fixtures rather than unmerged production output;
- M5 no-fabrication/persistence-nonsemantic fixtures using frozen V558/RSC fixture contracts;
- M6 actor-accessible/noncollapse fixtures using frozen actor-safe entry/envelope contracts.

Positive implementation that consumes another seam's runtime output must wait for that upstream seam's accepted implementation interface. This does not require all unrelated packages to serialize.

## Merge / integration barriers

### B1 — M1 acceptance before M2 runtime binding

Accept only if temporal-negative laundering, duplicate path multiplication, unknown duplicate authority, no-double-entry, typed-state and direct V554→V557 fixtures pass.

### B2 — M2 acceptance before M3 runtime binding

Accept only if exact seven-field route identity, B1/F2 exclusion, nonpositive route-state rejection, route locator nonidentity, and direct V555→V557 no-filler fixtures pass.

### B3 — M3 acceptance before producer-complete M4 integration

Accept only if 2..n participant binding, distinct-route floor, same-route reuse, exact composition authority, typed outcomes and ZERO_V556_OBJECTS fixtures pass.

### B4 — M4 acceptance before live M5 resolver integration

Accept only if V557/V558 states and replay identities remain distinct, standalone closure is immutable and exact, permission cannot widen by repository presence, and locator/index IDs remain nonsemantic.

### B5 — M5 acceptance before live M6 receptor integration

Accept only if an actual runtime RSC is required where declared, absence/invalidity fails explicitly, no RSC is fabricated, persistence is nonsemantic, peer currentness is independent, and historical receipts preserve historical peer identity.

### B6 — M6 + IG-PSEPF before whole-machine acceptance

Accept only if VP__FSV tuple/selector semantics, current actor-safe entry/envelope ingress, stale/deny/defer/integrity zero-positive behavior, monotone no-join projection, actor-accessible/phenomenology/utterance separation, and PSEPF zero-positive actor transition all pass.

### B7 — final hostile reclosure

Run all twenty frozen composition families plus deterministic replay and integrated noncollapse. No seam may be repaired by changing another seam's frozen semantic contract.

## Failure containment / rollback

Every package has a seam-local branch and rollback boundary. A failed package is withheld or reverted as a unit. Downstream packages may continue fixture-only work against frozen contracts but may not merge positive runtime binding to the failed seam. Unrelated accepted seams and IG-PSEPF are not rolled back merely because another seam fails. If a conflict requires semantic redesign, implementation stops and returns to explicit authority adjudication rather than silently widening the implementation contract.

## Path binding gate

This DAG names semantic owners, not repository file paths. The current regeneration assignment grants no production writes, and the bounded baseline audit did not independently establish exact production owner paths. Therefore `PRODUCTION_WRITE_ALLOWLIST.json` intentionally has no activated may-touch production paths. Explicit activation adjudication must bind exact paths/functions to these nodes before any production commit.
