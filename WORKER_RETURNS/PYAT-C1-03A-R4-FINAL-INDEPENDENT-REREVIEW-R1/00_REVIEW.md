# PYAT C1-03A — R4 FINAL INDEPENDENT REREVIEW — R1

**Disposition:** `CHANGES_REQUIRED`

**Terminal:** `C1_03A_R4_FINAL_INDEPENDENT_REREVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED`

Reviewed implementation return:
`b46fcf2b951d3ecbc7d17be45a36b37ff7c2f494`

R4 refusal-authenticity return:
`3bd481163ac1b2b1e30817b2704e89341099a960`

Prior independent rereview:
`3ebde6d268abcb005a48e42eb6d0b52ec4a3c025`

Reviewer issue tip:
`be9194ff86abfb89dd9b3b185d019815aadcb52c`

## Bottom line

R4 materially improves refusal authenticity and preserves the accepted G5/AT15/AT16 work. The final-SHA callability cleanup is also correct.

However, the primary refusal-authenticity boundary is still not closed.

The blocking issue is now narrower and different from R3:

`C1-03A-R4-FINAL-REVIEW-BLOCK-EMPIRICAL-CAPTURE-OWNER-FAMILY-001`

`capture_empirical_integrity_refusal()` does not require the exact competent empirical owner family it claims to certify. Its admission gate is only:

`isinstance(original_object, CanonicalSemanticObject)`

and it then executes:

`type(original_object)(**kwargs)`.

That means any canonical semantic-object family can be driven through this capture. If its constructor rejects a tampered stale-identity body with `Pre553IntegrityError`, the capture mints a token-guarded witness with:

- `refusal_kind = EMPIRICAL_INTEGRITY_REFUSAL`;
- `owner_label = rawlsing_next.pre553_empirical_query.execute_empirical_query`;
- `refused_ref = original_object.ref`;
- supporting refs from that object's own closure.

This is cross-owner refusal laundering. A constructor refusal by a different canonical family becomes an attestation that the empirical-query owner refused.

The R4 fixture itself exposes the mismatch: `integrity_failure_fixture()` correctly records its actual owner as the `CanonicalSemanticObject` constructor, while the resulting projection is asserted to carry the empirical-query owner label.

The final commission explicitly requires the capture wrapper not be drivable by caller-shaped inputs into certifying a refusal that the claimed competent owner did not produce. This boundary is therefore still blocking.

I do **not** rely on access to the module-private trust token for this disposition. The counterexample survives even if the project's private-token convention is treated as a trusted internal capability.

## Refusal authenticity attack

### What R4 fixed

R4 correctly removed the prior public minting path:
- no bare `Pre553IntegrityError` parameter;
- no bare `Pre553AuthorityError` parameter;
- no caller `producer_ref`;
- no caller `supporting_refs`;
- no caller reason;
- projection factories accept a witness only;
- witness construction is token-guarded;
- wrong refusal-kind replay is rejected;
- owner acceptance produces no refusal witness.

The discovery refusal path is materially stronger: `capture_required_authority_refusal()` imports and invokes the actual `execute_exact_bounded_discovery` owner and binds the grammar/release context. No caller-supplied owner function is accepted.

### Blocking empirical counterexample

The empirical capture's stated law is stronger than its actual gate.

It says the class comes from “a genuine owner-produced object.” Source does not establish that. It establishes only membership in the broad base class `CanonicalSemanticObject`.

There are two concrete ways this matters.

#### 1. Cross-family canonical object

A genuine canonical object from another family can be supplied as `original_object`.

The capture:
1. accepts it because it is a `CanonicalSemanticObject`;
2. copies its exact sealed body;
3. applies a semantic override while retaining its old `object_id`/`content_hash`;
4. calls that object's own class constructor;
5. catches the resulting `Pre553IntegrityError`;
6. emits an `EMPIRICAL_INTEGRITY_REFUSAL` witness labeled as `execute_empirical_query`.

The actual refusing code path is the canonical object constructor of the supplied family, not `execute_empirical_query`.

No exact empirical family check, governed-release membership check, or empirical-query-output check exists at the capture boundary.

#### 2. Caller-defined CanonicalSemanticObject subclass

The use of `isinstance` also admits caller-defined subclasses.

Because the invoked operation is `type(original_object)(**kwargs)`, a caller-defined subclass controls the constructor that the capture treats as the “real owner.” Such a subclass can deliberately raise `Pre553IntegrityError` and thereby cause the wrapper to mint a trusted witness from caller-controlled object identity/closure material.

This is precisely why the earlier R3 factory-authenticity work used exact type identity rather than `isinstance` at trusted owner boundaries.

### False owner attribution

The inconsistency is visible without constructing a hostile subclass.

The committed fixture says:

`owner = rawlsing_next.pre553_empirical_objects.CanonicalSemanticObject constructor`

but `capture_empirical_integrity_refusal()` hard-codes:

`owner_label = rawlsing_next.pre553_empirical_query.execute_empirical_query`.

That label is then copied unchanged into the trusted `OwnerStateProjection`.

Thus the final envelope can claim an owner different from the code that actually generated the refusal.

## Required correction

Do not reopen G5, AT15, AT16 or C1-02.

Close only the empirical refusal capture boundary.

A lawful correction must make the witness prove the exact competent owner/family it claims. Acceptable narrow shapes include:

1. resolve the original empirical object through the governed repository/release path and bind its exact membership before invoking the canonical integrity constructor; or
2. introduce an exact finite family/owner gate plus truthful owner attribution, if that is sufficient under the governing AT14 contract.

A broad `CanonicalSemanticObject` `isinstance` gate is insufficient.

If the intended owner for this state is actually the canonical object constructor rather than `execute_empirical_query`, record that owner truthfully and prove the AT14 contract accepts that owner. Do not relabel one owner as another.

Add hostiles for:
- a different genuine canonical object family;
- a caller-defined `CanonicalSemanticObject` subclass;
- owner-label equality with the operation that actually refused.

## Final-SHA method shape — PASS

The final implementation has exactly one `@classmethod` on:
- `from_empirical_integrity_refusal`;
- `from_blocked_authority_refusal`.

No refusal factory contains a nested `classmethod`.

Both are directly callable through normal class attribute access with genuine current witnesses.

The HQ156 correction is accurately characterized: the duplicate decorator was a real structural defect; the earlier predicted normal-call `TypeError` was not established and should not be repeated as a live failure.

The final correction from returned R4 is exactly:
- one production-line deletion in `pre553_analytical_state_and_route.py`;
- four added final-SHA callability courts;
- final-SHA return/commission artifacts.

No refusal semantics changed in that correction.

## G5 preservation — PASS

The route-authority section is byte-identical from accepted R3 return `767bb913...` to final R4 `b46fcf2b...`.

`RouteObligation.from_structural_admission` still:
- requires exact `AdmissionEvaluation`;
- requires exact `StructuralEmpiricalAdmission`;
- treats the receipt as sole route authority;
- requires evaluation decision/reason/blockers to agree with receipt truth;
- rejects contradictory positive `requested_use`;
- keeps nonpositive receipt obligations nonpositive.

Thus negative-receipt → forged-positive evaluation remains closed.

## AT15 preservation — PASS

The `RouteObligation` implementation, route guards, and AT15 courts are byte-identical between R3 and final R4.

Still preserved:
- genuine ADMITTED learned/adjudicated route;
- exact admission receipt;
- exact admission authority;
- exact rule hash;
- exact target use;
- failed/DENY route cannot proceed;
- failed learned claim cannot be relabeled direct;
- route obligation cannot be caller-constructed into legitimacy.

No R4 regression found.

## AT16 preservation — PASS

The 54/6 positive AT16 court is byte-identical from R3 to final R4.

It still proves:
- real producer output;
- accepted C1 composition;
- 54 support / 6 oppose;
- denominator 60;
- composition state `SUPPORTED`;
- retained state `SUPPORTED`, not observed-zero;
- exact generated evidence;
- named positioned-subject consumer;
- exact composed result identity retained in the final envelope.

Negative non-invocation courts remain present.

No AT16 regression found.

## Other accepted R3 work — preserved

No concrete regression found in:
- exact owner-family gates on the previously accepted typed factories;
- fixed owner labels there;
- adaptive determinant provenance;
- recursive owner-derived custody;
- no invented completeness grade;
- eight mandatory AT14 states remaining distinct;
- real adaptive UNVISITED;
- canonical admission receipt dominance;
- requested-use equality.

The stale `coverage_custody.completeness_state` reference was removed without changing the lawful handoff path.

## Owner-module preservation

The following blobs are unchanged between R3 and final R4:

- `pre553_empirical_query.py`: `03facecf70890bfd13b80418620d274cbcd69d02`
- `pre553_discovery_exact.py`: `905f24d114419dbdd93879ad2bee5b59dd2f23af`
- `pre553_empirical_objects.py`: `a61365b994e5c3c50de0f598fcf40e90abf757b6`
- `pre553_empirical_authority.py`: `ca65a7fd4d52f0c44447434559b1d09412e7aa39`
- `pre553_analytical_composition.py`: `604c8d591d4cc2b646e9b149cdb233fc9d69cf6b`

The R3→R4 diff changes only the C1-03A module, its C1-03A fixture/tests and R4 documentary terrain. C1-02 is untouched.

## Execution / provenance

The final recorded ten-file court is internally consistent:

- C1-03A state/route: 75
- higher-order composition: 35
- empirical query: 32
- structural admission: 17
- discovery exact: 14
- analytical composition: 13
- positioned-subject possibility: 13
- adaptive discovery: 8
- adaptive admission: 3
- recursive handoff: 2

Total: **212 passed, 0 failed, 0 errors, 0 skipped**.

Static source inventory independently reconciles those counts:
- state/route: 75 functions;
- empirical query: 30 functions plus a 3-case parametrized court = 32;
- structural admission: 13 functions plus a 5-case parametrized court = 17;
- analytical composition: 12 functions plus a 2-case parametrized court = 13;
- remaining suites match direct function counts.

No fresh runtime was available in this Browser/GitHub lane. Proof grade:
- execution result: reconciled worker execution evidence;
- blocking refusal counterexample: exact committed-source proof, independent of runtime timing/environment.

## Scope

No implementation mutation.
No merge/self-adoption.
No C1-03 join.
No raw source access.
No C4/C7.
No C1-R.
No V3.

## Final

The 212-pass court is valid evidence for what it tests. G5, AT15 and AT16 remain accepted.

But the final refusal-authenticity requirement is not yet satisfied because the empirical capture still allows the wrong canonical owner family—or a caller-defined canonical subclass—to be certified under the empirical-query owner label.

**Disposition:** `CHANGES_REQUIRED`

**Terminal:** `C1_03A_R4_FINAL_INDEPENDENT_REREVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED`
