# PYAT C1-03A — R3 FACTORY-AUTHENTICITY INDEPENDENT REREVIEW — R1

**Disposition:** `CHANGES_REQUIRED`

**Terminal:** `C1_03A_R3_INDEPENDENT_REREVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED`

Reviewed implementation return:
`767bb9139b80e774093af8e765e57ee57a19e005`

R3 commission tip:
`b885227b1b3f0ccaa8c892357dfc40251ab1d1cc`

Prior independent review:
`6bc1cb8ecd5568d6e78e83916763f125e8b888c8`

Reviewer issue tip:
`14fc5351e00f0f303f8288bdea60828a02187794`

## Bottom line

R3 successfully closes the dangerous G5 route-laundering counterexample and the named E/F/G factory-authenticity defects for empirical facts, discovery receipts, adaptive results, recursive handoffs, structural-admission evaluations, owner labels, adaptive determinant identity and recursive custody evidence.

It is **not yet acceptable at the full AT14–AT16 declared grain** because the two exact refusal factories remain caller-mintable. A caller does not need an owner execution to create either trusted refusal projection:

- `Pre553IntegrityError` is a public constructible exception class with no authenticity-bearing payload;
- `Pre553AuthorityError` is likewise publicly constructible;
- both refusal factories accept a caller-supplied `producer_ref`;
- both also accept caller-supplied `supporting_refs`;
- the trusted factory itself then injects the private trust token and mints an `OwnerStateProjection`, which becomes `ProducerStateEvidence` and enters the final envelope identity.

That is not merely a mislabeled diagnostic string. It permits caller-created `INTEGRITY_FAILURE` or `BLOCKED_REQUIRED_AUTHORITY` evidence to be bound to an unrelated exact object ref with arbitrary extra provenance refs.

This violates AT14's required receipt law to bind the **exact input** and **actual output** and contradicts the implementation's own claim that retained state is always a function of a real owner object.

No AT15 route-law repair needs reopening. No AT16 54/6 repair needs reopening. The correction is narrow: make refusal projection owner-execution-derived / owner-witness-derived rather than exception-class-plus-caller-ref-derived.

## G5 — attacked first

### Hostile

Start from a genuine negative `StructuralEmpiricalAdmission` receipt and build an exact-type `AdmissionEvaluation` around it whose envelope claims:

`decision_state="ADMITTED"`

### Result

**PASS — laundering closed.**

`RouteObligation.from_structural_admission`:

1. requires the exact `AdmissionEvaluation` type;
2. requires the exact `StructuralEmpiricalAdmission` receipt type;
3. reads authoritative decision from `receipt.admission_decision_state`;
4. reads reason from `receipt.decision_reason_code`;
5. reads target use, empirical fact ref, authority, rule material and blocker refs from the receipt;
6. compares the evaluation's duplicate decision/reason/blockers against receipt truth;
7. fails closed before constructing a `RouteObligation` when any duplicate disagrees.

Thus a negative receipt wrapped in a forged ADMITTED evaluation cannot mint positive route material.

If the envelope instead agrees with the negative receipt, the resulting obligation has `is_positive_admission == False`; `require_positive_route()` rejects it; and `assert_route_not_laundered(... DIRECT_EMPIRICAL ...)` rejects direct-route laundering.

### Other G attacks

Also **PASS**:

- positive receipt + forged negative decision → fail closed;
- positive/negative receipt + forged reason → fail closed;
- injected, dropped or caller-only blocking refs → fail closed;
- positive receipt + contradictory `requested_use` → fail closed;
- positive receipt + matching use → lawful learned/adjudicated obligation;
- nonpositive unresolved receipt preserves `UNRESOLVED_STRUCTURAL_USE` and gains no positive authority.

### Residual AdmissionEvaluation constructibility

**NONBLOCKING after R3.**

`AdmissionEvaluation` remains publicly constructible, but C1-03A no longer trusts its authority-like duplicate fields. Its other constructible fields (`m1_direct_projection`, `m1_projection_hash`, `v553_participant_projection`) are not read by `RouteObligation.from_structural_admission`.

A hand-built evaluation can therefore add no route authority beyond the canonical receipt it contains, provided receipt authenticity itself is genuine.

## Factory authenticity E/F — PASS

The principal minting factories now use exact type identity, not duck typing and not `isinstance`:

`type(value) is expected`.

That closes:
- duck-typed fake `EmpiricalFact`;
- duck-typed fake `DiscoveryResultReceipt`;
- duck-typed fake `AdaptiveSearchResult`;
- duck-typed fake `AdmissionEvaluation`;
- caller-defined subclasses of those owner families.

The committed subclass court is imperfectly written: it defines `_AdaptiveSubclass` and `_AdmissionEvaluationSubclass` concepts only indirectly and actually passes other wrong-family subclass instances to two gates. That does **not** create an implementation gap because the governing check is literally exact type identity and therefore necessarily rejects every subclass. Static code establishes the stronger result.

Owner labels are factory-fixed. The typed projection/route factories expose no `owner=` override.

Adaptive projection no longer accepts `producer_ref`; it derives the determinant only from `AdaptiveSearchResult.determinant_state_ref` and preserves checkpoint/visited/unvisited refs.

Recursive custody no longer accepts caller supporting refs. Its identity is derived from the exact handoff, exact evaluated frontier and owner-retained scope identity. No completeness grade is stored.

## Blocking residual — refusal authenticity

### Counterexample A: caller-created integrity failure

The following public call shape is accepted by the current implementation:

`OwnerStateProjection.from_empirical_integrity_refusal(exception=Pre553IntegrityError("caller"), reason="caller", producer_ref=<caller ExactRef>)`

The factory checks only:

`type(exception) is Pre553IntegrityError`

That is satisfied by an exception the caller instantiated directly. No empirical owner operation occurred.

The factory then returns trusted material with:
- owner fixed to the empirical owner label;
- `producer_state="OWNER_REFUSED:Pre553IntegrityError"`;
- retained state `INTEGRITY_FAILURE`;
- caller-selected producer ref;
- caller-selected supporting refs.

The worker's own R3 court proves the exception is directly constructible: `test_repair_hq_f_no_factory_still_accepts_a_caller_owner_label` instantiates `Pre553IntegrityError("x")`. The call only fails there because it additionally passes the removed `owner=` keyword. Remove that keyword and the refusal factory accepts the caller-created exception.

### Counterexample B: caller-created blocked authority

Likewise:

`OwnerStateProjection.from_blocked_authority_refusal(exception=Pre553AuthorityError("caller"), reason="caller", producer_ref=<caller ExactRef>)`

is accepted.

`Pre553AuthorityError` has no authenticity-enforcing constructor; it is a public subclass of `Pre553IntegrityError`.

The factory therefore mints trusted `BLOCKED_REQUIRED_AUTHORITY` state without any discovery/authority owner execution.

### Counterexample C: genuine refusal + unrelated object

Even if the exception is assumed genuine, the caller can pair it with an unrelated `ExactRef`. Nothing in either exception carries a ref, and the factories perform no relation check between the refusal and `producer_ref`.

That false ref then survives:
`OwnerStateProjection`
→ `ProducerStateEvidence`
→ `AnalyticalStateRouteResult.identity_preimage()`.

The same is true of caller-supplied `supporting_refs`.

This is custody/provenance authority, not a harmless display field.

## Why this blocks AT14

AT14 does more than require eight distinct words. Its required receipt must bind:
- exact input;
- expected-output authority;
- implementation;
- public path;
- actual output;
- consumer identity.

The eight-state mapping remains distinct and the genuine fixture paths still demonstrate real integrity and authority refusals. But the public trusted factory can also manufacture those two retained states without those owner paths and bind them to arbitrary input refs.

Therefore the AT14 envelope is not yet authenticity-closed at its declared grain.

## AT15 — preserved

All material prior AT15 repairs remain sound:

- route obligation is owner/receipt-derived;
- a bare learned-route label cannot establish legitimacy;
- genuine ADMITTED route exists;
- failed and DENY evaluations cannot proceed;
- failed learned evidence cannot be relabelled direct;
- positive route binds receipt, authority, rule hash, target use and empirical fact identity;
- G5 receipt dominance now closes the constructible-evaluation attack.

No AT15 implementation change is required by this rereview.

## AT16 — preserved

The corrected positive witness remains real:

- actual producer output;
- accepted C1 composition;
- named possibility consumer;
- 54 support / 6 oppose;
- denominator 60;
- analytical state `SUPPORTED`;
- retained state `SUPPORTED`, never `OBSERVED_ZERO`;
- exact evidence ref and consumer result;
- composed-result identity retained.

Negative fixture courts still record explicit non-invocation.

The refusal-authenticity blocker does not invalidate the real AT16 positive witness; it prevents full C1-03A acceptance because AT14 remains forgeable.

## Earlier laws preserved

Confirmed in source/courts:

- eight mandatory negative states remain distinct;
- real adaptive UNVISITED is still produced by the adaptive owner with visited/unvisited refs and no global negative;
- positive recursive handoff requires owner-derived custody;
- missing or mismatched handoff custody fails;
- custody carries no invented completeness grade;
- genuine ADMITTED learned route exists;
- failed/DENY cannot launder to direct;
- direct competent empirical output remains unwrapped;
- C1-02 is untouched by the R3 diff.

The two rewritten courts are genuine strengthening, not weakening:
1. observed-zero/no-cell hostile now uses an exact real `EmpiricalFact`, so it reaches the intended cell-projection gate rather than dying at the new type gate;
2. recursive-custody court now proves custody is a pure owner-derived function and the removed supporting-ref widening channel raises `TypeError`.

## Diff / provenance

`b885227b1b3f0ccaa8c892357dfc40251ab1d1cc -> 767bb9139b80e774093af8e765e57ee57a19e005`

is one commit ahead, zero behind.

Changed terrain is confined to:
- `rawlsing_next/pre553_analytical_state_and_route.py`;
- `rawlsing_next/tests/test_pre553_analytical_state_and_route.py`;
- `rawlsing_next/tests/c1_at14_at16_fixture.py`;
- `WORKER_RETURNS/PYAT-C1-03A-FACTORY-AUTHENTICITY-CORRECTION-R3/**`.

No C1-02 implementation/test file is touched.

## Execution evidence

The worker records one exact ten-file court:

**199 passed, 0 failed, 0 errors, 0 skipped.**

Independent static inventory reconciles exactly:
- C1-03A state/route: 62;
- analytical composition: 13;
- higher-order composition: 35;
- positioned-subject possibility: 13;
- empirical query: 32;
- discovery exact: 14;
- adaptive discovery: 8;
- adaptive admission: 3;
- recursive handoff: 2;
- structural admission: 17.

Total: **199**.

No fresh runtime execution was available in this Browser/GitHub review lane. The blocking refusal counterexample is nevertheless source-complete: it follows directly from public exception constructors and the refusal-factory bodies, and does not depend on timing, environment or fixture values.

## Smallest correction

Do not reopen R3 G5, AT15, AT16 or C1-02.

Repair only the refusal minting boundary.

A lawful correction must ensure the factory cannot mint a refusal projection from:
- a caller-instantiated bare exception;
- an unrelated caller-chosen producer ref;
- arbitrary caller supporting refs.

The strongest narrow shape is to derive the refusal witness and its object/context identity from the competent owner execution itself (or from an already-existing canonical owner-produced refusal receipt if one exists), rather than accepting exception-class + ref as sufficient authority.

If a wrapper must perform the owner call and catch the exception internally, that is preferable to treating a freely constructible exception instance as proof of provenance.

**Terminal:** `C1_03A_R3_INDEPENDENT_REREVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED`
