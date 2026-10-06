# PYAT HQ220 — F7 AUTHORITY-CHAIN FINAL HOSTILE REREVIEW — R1

**Lane:** `PYAT-HQ220-F7-AUTHORITY-CHAIN-FINAL-REREVIEW-R1`  
**Role:** Browser/GitHub independent hostile reviewer — READ-ONLY / NO REPAIR  
**Commission tip:** `c1d64e74b71043258653a8d1796d0097f0ce549e`  
**Exact candidate:** `agent/rabochii-pyat-hq219-f7-authority-chain-repair-r1 @ 9adc8cc9ba0942db974dddf809206de2a2fd231b`  
**Prior final rereview:** `1c8b8ce186682d212ceec460b7b707421b6f0d27`  
**Accepted F7 contract:** `c57a96897788108db7b194e4e51691d1ca8ab729`  
**Forward law:** HQD-216 exact control object at `e0e7ce0e596e4e5ea7ec96c265ec949b9fe801a2`

## Disposition

`F7_AUTHORITY_CHAIN_REPAIR_PARTIAL__NAMED_DEFECT`

HQ219 closes the **headline forms** of all three HQ218 defects, and it does so without adding an authority kind, a relation state, a reason family, a new source ontology, or actor/person power. It also preserves a locally productive F7 service.

It is nevertheless **not ready for HQ adoption**. Two blocking authority-chain defects remain, plus one local compatibility defect and one court-authenticity defect:

1. **F7-RR-04B — returned source-relation authority proof is discarded.** F7 now calls the real `SourceRelationResolver.require(...)`, but it does not capture the returned `RelationDecision`. The relation decision's exact `relation_ref` and, critically, its exact `authority_ref` are never cross-bound into F7's authority closure. F7 then independently resolves `request.source_equivalence_authority_ref`. A genuine relation authorized by authority **A** can therefore be accompanied by an unrelated positive SOURCE_EQUIVALENCE authority **B**; F7 accepts both and records B without proving B authorized the relation.

2. **F7-RR-03B — the identity-owning TEMPORAL_EVIDENCE authority is not source-scope-bound to the compared pair.** The temporal-evidence snapshot is resolved with no `required_universe_refs` and no identity-specific operation. Once it is positive by kind/state, custom scope keys `temporal_identity_contract_refs` and `identity_surface_jointly_satisfied` decide the identity gate. The accepted owner archaeology describes temporal identity as a source-native scoping question; a TEMPORAL_EVIDENCE snapshot outside the compared source scope must not be able to authorize sameness merely because it carries those keys.

3. **F7-RR-02C — explicit-unrestricted representation drift.** The adopted general authority law recognizes both `EXPLICIT_UNRESTRICTED` and `UNRESTRICTED_BY_THIS_AUTHORITY`. F7's three local scope helpers recognize only the first. This is fail-closed rather than fail-open, but it can reject a competent authority representation that existing authority law explicitly accepts.

4. **COURT-HQ220-01 — RR-03 targeted break is not a real targeted break.** The test first observes an unsatisfied-owner refusal, then monkeypatches only exact-ref coverage and constructs a separate **satisfied** owner registry. It never disables owner-satisfaction consultation on the same fixture. The court therefore lacks the commission-required fail-capability witness for Repair B.

These are bounded implementation/court defects. They do **not** require reopening the F7 architecture.

## RR-02B — missing governed-use scope

**SUSTAINED CLOSED at the original defect grain.**

`resolve_required_authority(... require_use_scope=True)` now fails closed when `target_use_refs` is absent. When an exact collection is present, F7 requires the complete governed-use ExactRef identity; a bare object-id token does not cover it. The path applies to both TEMPORAL_COMPARABILITY and every TARGET_USE_PERMISSION ref.

The omission-as-wildcard bug is gone.

The remaining RR-02C issue is the narrower representation mismatch: `pre553_empirical_authority._scope_contains` treats both adopted explicit-unrestricted literals as positive, while F7's local helpers only accept `EXPLICIT_UNRESTRICTED`. A local stage may be stricter than a caller, but it may not silently reinterpret an already-adopted authority representation as non-authority without adjudicating that representation obsolete.

## RR-03 — temporal identity owner resolution

### Caller self-authorization

**SUSTAINED CLOSED.**

A caller-minted identity mapping plus its matching self-computed ExactRef no longer suffices. The resolved TEMPORAL_EVIDENCE snapshot must name the exact identity-contract ref and assert joint satisfaction. Missing/wrong owner ref, missing/false joint satisfaction, and caller-owner contradiction all refuse.

The two new detected codes:

- `TEMPORAL_IDENTITY_NOT_BOUND_BY_TEMPORAL_EVIDENCE_AUTHORITY`
- `TEMPORAL_IDENTITY_OWNER_RESOLUTION_UNAVAILABLE`

map into the existing `TEMPORAL_IDENTITY_UNRESOLVED` state. The 12-state ceiling remains intact.

### Identity contract shape

**LAWFUL REUSE SHAPE; NOT AUTHORITY OVERREACH.**

The accepted contract already assigns persistent temporal identity to **TEMPORAL_EVIDENCE + exact temporal_identity_contract_ref** and explicitly says TEMPORAL_COMPARABILITY consumes identity rather than constituting it. Therefore using owner-supplied identity keys on the TEMPORAL_EVIDENCE authority envelope is a reasonable representation of the already-assigned owner, not a hidden twentieth authority kind or a new identity registry.

Crucially, HQ219 does **not** create the missing real identity instance in production. `IDENTITY_CONTRACT_INSTANCE_MISSING` therefore remains an upstream dependency / estate-occupancy gap. Under HQD-216, that absence is not itself a local F7 implementation defect if F7 can consume a competent owner-backed fixture.

### Remaining owner-scope defect

The new owner path is not fully scoped. At `pre553_temporal_comparability.py:867-872`, F7 resolves TEMPORAL_EVIDENCE without the exact compared `source_universe_refs`, even though `resolve_required_authority` already supports required-universe checking.

That is not merely “the real estate instance is missing.” It means an actual but out-of-scope TEMPORAL_EVIDENCE snapshot can be treated as the identity owner for this comparison. The repair must bind the identity owner to the exact source scope it is authorizing.

## Identity precedence

**SUSTAINED.**

Identity failure cannot fall through to a positive receipt. The existing precedence remains total:

`TEMPORAL_INSUFFICIENT_AUTHORITY` outranks identity; identity outranks all lower negative/comparability states. No thirteenth relation state and no new reason family were introduced.

## RR-04 — source-relation positive adjudication

### Original exact-lookup bypass

**SUSTAINED CLOSED.**

HQ219 correctly replaces plain `resolve_exact` lookup with the adopted owner's `require` path. With the concrete adopted resolver:

- DENIED relation refuses;
- wrong relation kind refuses;
- wrong universe pair refuses;
- wrong effective/operation scope refuses;
- wrong governed-use string refuses;
- a duck-typed non-owner stub is rejected;
- a genuine positive owner decision remains productive.

This is a real improvement.

### Remaining split authority chain

**FAIL / BLOCKING.**

The critical code is `pre553_temporal_comparability.py:977-1016`.

F7 executes:

`resolver.require(...)`

but assigns its return to nothing. The adopted owner, however, returns a contentful `RelationDecision` containing the exact authorized `relation_ref` **and** exact relation-authorizing `authority_ref`.

F7 then manufactures a local positive `AuthorityResolutionRecord` from the requested `equivalence_ref`, and independently resolves the caller-supplied `source_equivalence_authority_ref`.

So the repair now proves:

> some genuine owner decision is positive

and separately:

> some caller-supplied SOURCE_EQUIVALENCE authority snapshot is positive

but it does **not** prove:

> this exact authority snapshot is the authority that authorized this exact relation decision.

Positive + positive is not identity.

The receipt's `authority_snapshot_refs` are populated from F7's `positive_snapshots`; the actual relation owner's authority snapshot is not added through the returned decision. Thus the receipt can misstate its authority ancestry even when the underlying relation itself is genuine.

A related boundary weakness follows from the same omission: `isinstance(resolver, SourceRelationResolver)` accepts subclasses, while F7 interprets any non-raising `require()` as success. The RR-04 targeted-break test itself demonstrates that replacing `require` with a non-raising fake makes a DENIED relation positive. The adopted concrete resolver is sound; F7 simply fails to conserve the proof it returns.

This needs a bounded repair: capture the returned decision, validate its exact relation identity, and bind its exact authority identity into the F7 authority closure.

## Governed-use contract change

Requiring the source relation to be adjudicated for the **downstream governed use**, rather than for the relation object's own ref, is semantically correct. Reverting to self-authorization would be wrong.

There is, however, an integration-grain mismatch: F7's governed use is an ExactRef, while the adopted source-relation owner currently keys `target_use` as a non-empty string. HQ219 projects the governed use to `governed_use_id.object_id`. That is stronger than the old relation-self fixture, but it is not complete ExactRef identity.

The candidate establishes a competent fixture for the new local contract; it does not establish a real production producer already occupying that exact contract. Under HQD-216, that is an **integration/producer occupancy gap**, not a license to call the local F7 stage defective merely because the estate is unfilled. HQ should keep this gap visible rather than pretending HQ219 populated it.

## Productive adequacy

The source and court preserve the intended service shapes:

- same-universe comparable pair -> positive comparable receipt;
- exact zero -> `NO_AUTHORIZED_CHANGE`;
- positive nonzero -> `INCREASE`;
- negative nonzero -> `DECREASE`;
- cross-universe pair with a genuine positive source-relation owner decision -> positive temporal receipt.

The repair therefore did not “solve” the authority defects by closing production.

That does not override the blocking proof-chain defects above: productive arithmetic plus an inexact authority ancestry is not an acceptable positive service.

## Court authenticity

Static reconstruction from the exact committed court supports HQ219's corrected collection accounting:

- F7: 93 test functions; prior 96 collected plus 14 new functions and 4 parametrization expansions -> **114**;
- M1: 24 test functions plus one four-case parametrization -> **27**;
- aggregate -> **141**.

This reviewer did not execute a local runtime because the commissioned lane is Browser/GitHub-only.

The worker's 14 negative-control failures against the pre-repair binder are source-consistent; no exact contradiction to that count was found. The worker also correctly discloses that two new witnesses are not pre-repair discriminators: the lawful positive cross-universe case and the wrong-kind construction guard.

The RR-02B targeted break is genuinely discriminating. The RR-04 targeted break proves the owner call is load-bearing, while simultaneously exposing the return-validation gap described above.

The RR-03 targeted break does **not** satisfy the commission's targeted fail-capability requirement. It changes from an unsatisfied owner to a separate satisfied owner rather than breaking the owner-consultation mechanism on the same fixture.

The reported 146 pre-existing regression failures/errors are not charged to F7: HQ219 reports identical before/after identities, and this review found no exact tie from those identities into the F7/M1 courts.

## Environment / workflow

The candidate's environment statement is assessed in `03_PRODUCTIVE_PATH_PRECEDENCE_AND_NONCOLLAPSE.json`. This review does not rewrite or resolve HQ214's historical version conflict. No GitHub workflow run is associated with candidate commit `9adc8cc9ba0942db974dddf809206de2a2fd231b`.

## Sustained noncollapse

HQ219 preserves the accepted noncollapse ceiling: exactly 12 temporal relation states, exactly 19 authority kinds, exact-zero arithmetic with no deadband/tolerance/rounding, 3+ anchor refusal, prior-F7 mapping, negative receipt => NOT_COMPARABLE, live frozen backfill guard, and no F8 consumption, source ranking, interpolation, trajectory, causation, currentness authority, scalar temporal pressure, pooling, equivalence creation, or actor/person power.

## Bounded repair set

1. Capture the `RelationDecision` returned by the source-relation owner and conserve its exact `relation_ref` and `authority_ref`; do not replace the returned proof with a locally fabricated positive record.
2. Cross-bind the actual relation-authorizing authority into F7's authority snapshot closure. If `request.source_equivalence_authority_ref` remains, it must be the exact authority that authorized the returned relation decision, not merely another positive snapshot.
3. Bind the identity-owning TEMPORAL_EVIDENCE authority to the exact compared source scope.
4. Reconcile F7's explicit-unrestricted helper with the already-adopted authority representation set.
5. Replace the RR-03 targeted-break witness with a same-fixture mechanism break that demonstrably reopens the identity authorization path.

No new authority kind, state family, relation kind, source ontology, or architecture reopen is required.

`HQ220_F7_AUTHORITY_CHAIN_FINAL_REREVIEW_RETURNED__HQ_DECISION_REQUIRED`
