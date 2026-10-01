# LAUNCH IN: OpenCode — Space Bunny Free
# ROLE: PYAT C1-03A — FACTORY AUTHENTICITY CORRECTION — R3
# REPOSITORY: maidiu/rawlsing

Branch:
`agent/opencode-pyat-hq153-c1-03a-factory-authenticity-correction-r3`

Exact base:
`ad67be387fd9da350f07858b41729309e1c2e67f`

Prior R2 disposition:
`PASS_C1_03A_TRUST_BOUNDARY_CORRECTED__INDEPENDENT_REREVIEW_REQUIRED`

HQ intake found that R2 closed direct-construction escapes, but several public factories still accept caller-shaped inputs or caller-substitutable provenance. This is the final bounded factory-authenticity correction before independent rereview.

Do not reopen the semantic design. Preserve all R1/R2 valid work.

## HQ blocker E — typed factories still accept duck-typed caller objects

The following R2 factories accept `Any` and inspect attributes:
- `OwnerStateProjection.from_empirical_fact`
- `OwnerStateProjection.from_discovery_receipt`
- `OwnerStateProjection.from_adaptive_result`
- `RouteObligation.from_structural_admission`

A caller can therefore construct an arbitrary object with the expected attributes and ask the trusted factory to mint governed projection/route material.

### Required correction

Require the exact competent current owner object family at each boundary:
- empirical fact -> `rawlsing_next.pre553_empirical_objects.EmpiricalFact`
- discovery receipt -> `rawlsing_next.pre553_empirical_objects.DiscoveryResultReceipt`
- adaptive result -> `rawlsing_next.pre553_discovery_adaptive.AdaptiveSearchResult`
- structural route -> `rawlsing_next.pre553_structural_admission.AdmissionEvaluation`

Use the narrowest fail-closed type check consistent with current owner law. Do not accept arbitrary duck-typed objects.

Add hostiles using fake objects with plausible fields and exact-looking refs; they must not mint trusted material.

## HQ blocker F — caller can still rewrite owner/provenance identity

R2 factory methods retain caller-overridable `owner=` labels.

`from_adaptive_result(... producer_ref=...)` also lets the caller replace the owner's exact determinant ref even though the R2 return claims the factory carries the owner's own refs.

`RecursiveCoverageCustody.from_handoff(... required_supporting_refs=...)` lets callers add arbitrary supporting refs into the trusted custody identity even though the exact frontier is already owner-derived.

### Required correction

For typed factories, owner labels are fixed by the factory and must not be caller-overridable.

Remove caller owner-label parameters from:
- empirical fact projection;
- discovery receipt projection;
- adaptive projection;
- recursive handoff projection;
- structural-admission route obligation;
- exact refusal projection factories.

For adaptive projection:
- remove caller `producer_ref`;
- derive the producer/determinant ref only from `AdaptiveSearchResult.determinant_state_ref`;
- preserve the exact owner checkpoint, visited and unvisited refs.

For recursive custody:
- remove caller-supplied `required_supporting_refs` unless every such ref is independently derivable from the handoff itself;
- the custody already binds the exact handoff ref and exact evaluated frontier and should not acquire arbitrary caller evidence.

Add hostiles proving these override keywords are rejected or otherwise cannot change identity.

## HQ blocker G — AdmissionEvaluation is itself constructible; receipt truth must dominate

Even after an exact type check, `AdmissionEvaluation` is a plain dataclass and can be manually instantiated around a real receipt with forged:
- `decision_state`;
- `reason_code`;
- `blocking_refs`.

Therefore `RouteObligation.from_structural_admission` must not treat those evaluation fields as independent semantic authority.

### Required correction

The obligation must derive authoritative route facts from the exact canonical `StructuralEmpiricalAdmission` receipt:
- decision from `receipt.admission_decision_state`;
- reason from `receipt.decision_reason_code`;
- target use from `receipt.target_use`;
- empirical fact ref from the receipt;
- admission authority from the receipt;
- rule hash from the positive structural interpretation payload;
- blocking refs from the receipt's exact applicable negative/denial/noncomparability refs.

The surrounding `AdmissionEvaluation` may be used as an execution envelope only if its duplicate fields exactly agree with the receipt. A manually constructed inconsistent evaluation must fail closed.

For `ADMITTED`:
- the caller's `requested_use` must exactly equal the receipt-declared target use;
- contradictory requested-use metadata must be rejected, not merely stored alongside the receipt truth.

For a nonpositive receipt whose target use is `UNRESOLVED_STRUCTURAL_USE`:
- preserve that receipt target exactly;
- `requested_use` may record the attempted requested use but must not be represented as granted authority.

Add hostiles:
- real positive receipt + forged evaluation decision -> fail;
- real positive receipt + forged reason -> fail;
- forged blocking refs inconsistent with receipt -> fail;
- positive receipt + contradictory requested_use -> fail;
- real positive evaluation + matching requested_use -> pass;
- real negative unresolved evaluation preserves receipt target and does not gain positive route authority.

## Preserve

Do not regress:
- R2 direct-construction guards;
- no generic derive/derive_fn;
- exact refusal-type distinction (`Pre553AuthorityError` subclass trap stays covered);
- learned route requires owner-derived obligation;
- recursive custody has no invented completeness grade;
- AT16 54/6 is SUPPORTED;
- all eight negative states remain distinct;
- real adaptive UNVISITED;
- genuine ADMITTED positive route;
- DENY/failed no-laundering;
- real positive handoff exact custody;
- producer -> C1 composition -> named consumer;
- C1-02 untouched.

## Write terrain

Modify only:
- `rawlsing_next/pre553_analytical_state_and_route.py`
- `rawlsing_next/tests/test_pre553_analytical_state_and_route.py`
- `rawlsing_next/tests/c1_at14_at16_fixture.py`
- `WORKER_RETURNS/PYAT-C1-03A-FACTORY-AUTHENTICITY-CORRECTION-R3/**`

No C1-02. No AT17. No C1-03R. No C5/C7. No raw sources. No V3.

## Required court

Run the same ten-file court used by R2 plus the new factory-authenticity hostiles.

Record exact counts and exact files. Do not claim a broader sweep.

## Return

Write:
`WORKER_RETURNS/PYAT-C1-03A-FACTORY-AUTHENTICITY-CORRECTION-R3/**`

Required:
- `00_RETURN.md`
- `01_HQ_BLOCKER_DISPOSITION.json`
- `02_FACTORY_AUTHENTICITY_RECEIPT.json`
- `03_EXECUTION_RECEIPT.json`
- `04_FINAL_DISPOSITION.json`

Allowed dispositions:
- `PASS_C1_03A_FACTORY_AUTHENTICITY_CORRECTED__INDEPENDENT_REREVIEW_REQUIRED`
- `EXISTING_OWNER_OR_AUTHORITY_GAP__HQ_ADJUDICATION_REQUIRED`
- `ARCHITECTURE_WARRANT`

No merge/self-adoption.

Terminal:
`C1_03A_FACTORY_AUTHENTICITY_CORRECTION_RETURNED__HQ_ADJUDICATION_REQUIRED`
