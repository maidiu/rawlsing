# PYAT HQ224 — F7 FINAL AUTHORITY CLOSURE HOSTILE REREVIEW — R1

**DISPOSITION:** `F7_FINAL_AUTHORITY_CLOSURE_PARTIAL__NAMED_DEFECT`  
**ROLE:** Browser/GitHub independent hostile reviewer — read-only review; no production repair; no self-adoption  
**COMMISSION:** `83ff750647dcd3e5a91218cca232ef894f1359ef`  
**CANDIDATE:** `agent/rabochii-pyat-hq222-f7-final-authority-closure-r1 @ a190988b58ae1fe5d6a714e0691b19f84eb4e00e`  
**PRIOR REVIEW:** `acb8602e3968bc2e9fcde63223294aa92e0ddce2`  
**ACCEPTED F7 CONTRACT:** `c57a96897788108db7b194e4e51691d1ca8ab729`  
**FORWARD LAW:** HQD-216 at `e0e7ce0e596e4e5ea7ec96c265ec949b9fe801a2:PYAT_CONTROL_ROOM/26_HQD216_PRODUCTIVE_ADEQUACY_AND_PREV3_EMPIRICAL_GATE_LAW.md`

## Decision

HQ222 closes the four exact HQ220 findings at their direct defect grain, and it preserves the lawful positive F7 service. It is nevertheless **not ready for HQ adoption** because the commission-mandated hostile resolver-subclass attack exposes one exact local authority-boundary defect.

### F7-RR-04C — hostile `SourceRelationResolver` subclass can counterfeit owner adjudication

`TemporalComparisonRequest.source_relation_resolver` remains `Any`. F7 rejects a duck-typed non-owner, but accepts any object satisfying `isinstance(resolver, SourceRelationResolver)`. Python subclasses therefore cross the gate.

After that gate F7 calls the virtual `resolver.require(...)` and validates only the returned decision's presented fields. `_relation_decision_defect` checks authorized state, relation kind, relation-ref identity, non-null authority ref, source-universe pair, target-use string and operation scope. It does **not** establish that the concrete base resolver's own relation registry/authority registry produced that decision; it does not resolve the relation independently; and it does not bind the decision's replay identity back to a base-owner adjudication.

A hostile subclass can therefore call the lawful base constructor with **zero relations**, override `require`, and return a real `RelationDecision` whose fields echo F7's request while naming the caller's independently genuine positive SOURCE_EQUIVALENCE authority B. The outer `isinstance` passes. `_relation_decision_defect` passes. The separately supplied B snapshot resolves positive. HQ222's A/B check then compares forged-B to real-B and passes. Given otherwise competent fixtures, no relation need exist in the base resolver at all and the path can reach `TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED`.

This is not hypothetical duck typing; it is a direct consequence of the current dispatch boundary. The adopted owner implementation is sound when its concrete `decide/require` machinery executes, but F7 has not proved that the call it trusts is that machinery. The candidate itself disclosed this residual; HQ224 explicitly commissioned the hostile-subclass attack and forbade waiving it as outside HQ222's write list.

**Required bounded repair:** bind F7 to a non-overridable adopted-owner adjudication boundary. Rejecting subclasses is the minimum obvious boundary, but HQ should prefer a proof that the base owner's adjudication/constructor provenance—not a caller-overridable virtual method—is what produced the consumed decision. No new relation kind, authority kind, state family, or architecture reopen is required.

## HQ220 findings

- **F7-RR-04B direct A/B split:** closed for the concrete adopted resolver. The returned decision is captured; its relation ref and relation-authorizing authority are conserved; unrelated positive B refuses. The new F7-RR-04C defect is the trust boundary *before* that cross-binding.
- **F7-RR-03B TEMPORAL_EVIDENCE source scope:** closed. The identity-owning TEMPORAL_EVIDENCE slot now resolves against the exact compared source universes; unrelated, one-sided and stale universe coverage is refused.
- **F7-RR-02C unrestricted representations:** closed. F7's blanket set is exactly `EXPLICIT_UNRESTRICTED` and `UNRESTRICTED_BY_THIS_AUTHORITY`; omission and third literals remain non-blanket.
- **COURT-HQ220-01 fail capability:** closed at source/court grain. RR-03 now keeps one unsatisfied-owner fixture and falsifies only owner satisfaction consultation; restoring the seam restores the refusal. RR-04 now falsifies a real returned RelationDecision rather than demanding acceptance of a contentless fake.

## Productive adequacy and ceilings

HQD-216's positive-service requirement remains satisfied at local fixture grain according to the candidate court and is source-consistent: same-universe comparison, exact zero, increase, decrease, and a genuine owner-backed cross-universe comparison remain reachable. The hostile-subclass defect is therefore not a refuse-everything issue; it is a positive-authority authenticity issue.

The candidate preserves the declared ceilings: 12 relation states, 19 authority kinds, exact-zero/no tolerance, 3+ anchor refusal, total precedence, exact measure binding, complete F7 ExactRef use-scope checks, and no F8/ranking/selection/interpolation/trajectory/causation/currentness authority/pooling/equivalence creation/actor power.

## Court authenticity

This Browser/GitHub lane did not execute a local runtime. Static inspection reconstructs the HQ222 addition as 9 named `test_hq222_*` functions collecting to 21 cases: four RR-03B cases, two unrestricted-token cases, twelve bad/omitted-token cases, one adopted-law agreement case, and two RR-04B cases. That is consistent with the worker's 114→135 F7 collection delta. The worker reports 135/135 F7, 27/27 M1, and an unchanged 62-entry pre-existing failure set; no source-level contradiction was found.

The reported `20 of 21` pre-repair discrimination is also structurally plausible: the one lawful source-scope control is expected to remain positive, while the three bad identity-scope cases, the representation-drift cases (whose new constant/assertions are absent pre-repair), and the two RR-04B cases distinguish the repair. The revised RR-03 same-fixture targeted break is a modified existing witness, not one of the 21 newly collected cases, and the worker truthfully discloses that its new seam does not exist in pre-repair production.

The worker's execution environment is explicitly non-governed (`Python 3.11.3`, pre-existing pytest venv). This review treats those numbers as reproduced worker evidence, not governed certification.

## Known integration gaps

Under HQD-216, the governed-use `ExactRef` → source-relation string `target_use` projection remains an **integration/producer occupancy gap**, not this local F7 defect: the local competent fixture exercises the accepted path, while no real producer occupancy is proved. Likewise `IDENTITY_CONTRACT_INSTANCE_MISSING` remains an **upstream estate-occupancy gap**; F7 consumes competent owner-backed identity fixtures but does not own production of the real instance.

## Final

`F7_FINAL_AUTHORITY_CLOSURE_PARTIAL__NAMED_DEFECT`

Named blocker: `F7-RR-04C__HOSTILE_SOURCE_RELATION_RESOLVER_SUBCLASS_CAN_FORGE_OWNER_DECISION`.

`HQ224_F7_FINAL_AUTHORITY_CLOSURE_REREVIEW_RETURNED__BOUNDED_RESOLVER_TRUST_REPAIR_REQUIRED`