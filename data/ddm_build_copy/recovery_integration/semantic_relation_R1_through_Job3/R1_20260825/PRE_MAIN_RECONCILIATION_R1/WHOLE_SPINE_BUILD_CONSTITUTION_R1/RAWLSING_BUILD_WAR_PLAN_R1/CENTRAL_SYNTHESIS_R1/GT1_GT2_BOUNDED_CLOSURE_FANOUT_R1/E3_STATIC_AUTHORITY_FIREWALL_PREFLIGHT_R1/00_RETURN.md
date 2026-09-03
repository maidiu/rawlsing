# GT12 FINAL E3 — STATIC AUTHORITY + FIREWALL PREFLIGHT R1

## Status

`STATIC_PREFLIGHT_BLOCKED__MATERIAL_AUTHORITY_DEFECTS_FOUND`

This is **not** the final hostile-audit verdict.

This return does **not** issue GT1/GT2 adoption.

## Identity

Repository:

`maidiu/rawlsing`

Worker branch:

`agent/rabochii-gt12-final-e3-static-authority-review-r1`

Exact starting candidate HEAD:

`820311811b3e4094aea7e0e665fd0a228520cd1a`

Integrated A-F merge base:

`42c4a1ed753071026a5186e8c1770b6359a9e48c`

Closure-D hostile-audit handoff tip consumed:

`5ce9b13285f5ac42297e01a21e8dba4026c0a5ac`

Prepared handoff:

`D_REGRESSION_HOSTILE_AUDIT_PACKET_R1/03_BOUNDED_HOSTILE_AUDIT_HANDOFF.md`

Method:

- static exact source/type/ref inspection only;
- no Library data;
- no full regression court;
- no production semantic edits;
- no final hostile-audit PASS/FAIL verdict;
- no PRE-MAIN or `main` movement.

Candidate comparison from `42c4a1...` to `820311...` is 37 commits ahead, 0 behind. The integrated changed surface relevant to this preflight includes the C->D typed bridge, D relation admission, D->E typed bridge, relation-specific M1/V554 ingress, M4/V557/V558, and inherited V3 zero-positive guard.

---

# Preflight attack disposition H01-H10

## H01 — semantic promotion

**MATERIAL DEFECT VIA H05.**

FIELD FORGE itself is correctly count-only and anti-causal:

- `field_forge_conditional_support.py:30-39`
- anti-inferences remain explicit in its semantic projection.

However the later M1->M4 bridge can mint an `ACTIVE_CAUSAL` producer permission from a caller-supplied argument without an exact upstream permission translation. See E3-01 below.

## H02 — producer reownership

**No material static defect found before blocker stop.**

Concrete safeguards inspected:

- `gt12_c_to_d_relation_bridge.py:_validate` requires the actual FIELD FORGE relation owner;
- PRE-V3 admission owner remains separate;
- `gt12_d_to_m4_typed_bridge.py:410-430` carries FIELD FORGE relation owner/ref/rule/authorities in the authority bundle;
- relation M1 F1 preserves originating FIELD FORGE relation exact refs;
- M4 producer family becomes V554 as producer-of-structural-object without rewriting the preserved FIELD FORGE relation owner lineage.

## H03 — actor leakage

**No material static defect found before blocker stop.**

- C/D/E bridge payloads create no actor/personality/biography objects.
- M4 forbids actor/V3/V2/persona/render semantic classes.
- V3 production accepted-positive registry remains empty.
- Existing V3 guard returns zero-effect unless a separately accepted positive authority is present.

## H04 — I04 / empirical-M1 coercion

**No material static defect found before blocker stop.**

- C->D bridge accepts exact `ExactConditionalSupportProfile`, not `EmpiricalFact`.
- No I04/StructuralEmpiricalAdmission call occurs on the relation path.
- D->E requires relation contract `M1_ADMITTED_FIELD_FORGE_RELATION_V554_INGRESS@1.0.0`.
- basis remains `ADMITTED_FIELD_FORGE_RELATION`.
- signature remains `V554-SIG-004-NONTEMPORAL-ADMITTED-RELATION-EXACT`.
- empirical-direct contract substitution is explicitly rejected.

## H05 — permission widening

**MATERIAL DEFECT E3-01.**

See detailed defect below.

## H06 — role/order drift

**No material static defect found before blocker stop.**

Concrete checks preserve:

- CONDITIONER = Q86B;
- TARGET = Q86A;
- ordinals [0,1];
- participant order CONDITIONER then TARGET;
- exact participant refs and role/order fingerprint.

## H07 — exact-ref/hash loss

**No material static defect found on the intended typed bridge before blocker stop.**

The intended path preserves:

- relation ExactRef kind/object-id/content-hash;
- admission ExactRef;
- relation/admission rule refs;
- AuthorityRef id/version/content-hash;
- current-selection ref;
- source/universe/risk/dependency/replay closure;
- V558 exact OBJECT_IDENTITY index and repository checksum.

## H08 — typed-negative laundering

**MATERIAL DEFECT E3-02.**

See detailed defect below.

## H09 — V553/V555/V556 fabrication

**No material static defect found before blocker stop.**

The relation M1 contract is explicitly non-temporal SIG-004. The D->M4 helper publishes only producer family V554 and source stage `M1_RELATION_V554_TO_V557`. No V553/V555/V556 constructor is called by the successful relation helper.

## H10 — positive V3 authority fabrication / firewall compatibility

**Existing V3 guard remains statically fail-closed, but it does not cure E3-01.**

`v3_psepf_zero_positive_guard.py` retains an immutable empty production accepted-positive registry and produces `DENY_ZERO_EFFECT` with zero actor-state, ledger, cursor, RNG, and scheduler effects absent separately accepted authority.

A structural M4 permission widening before V3 remains material even if V3 later denies actor mutation.

---

# E3-01 — M1->M4 producer permission is re-minted from caller input

## Exact defect surface

### Upstream admission is narrowly authorized

`rawlsing_next/gt12_d_to_m4_typed_bridge.py:131-157`

`_require_positive_admission(...)` requires:

- target use exactly `STRUCTURAL_MEDIATION_INPUT`;
- target-use permission present;
- target-use permissions subset of relation permission ceiling.

### Authority is not carried into an M4 permission ceiling

`rawlsing_next/gt12_d_to_m4_typed_bridge.py:476-505`

`publish_and_resolve_relation_v554_at_current_m4(...)` accepts a fresh caller argument:

`producer_allowed_uses: Sequence[str]`

and passes it directly to:

`structural_objects_from_accepted_m1(...)`.

`rawlsing_next/m4_m1_evaluation_binding.py:115-124`

The relation M1 object is constructed with:

`producer_allowed_uses=producer_allowed_uses`

without proving that those M4 permission atoms derive from the admitted relation permission/target-use authority.

### Publication authority does not close this gap

`rawlsing_next/m1_temporal_v554_admission_dedup.py:196-199`

The publication authority carries producer/publisher/use/rule/decision/object-family fields, but no M4 permission ceiling or exact translation from `STRUCTURAL_MEDIATION_INPUT`.

`rawlsing_next/m1_temporal_v554_admission_dedup.py:270-281`

The direct V554->V557 handoff preserves only publication authority id/version/hash and object refs; it does not bind producer allowed-use atoms.

### Downstream checks are only relative to the newly supplied ceiling

`rawlsing_next/m4_v557_v558_publication_repository.py:503-520`

V557 checks only:

`v557_allowed_uses <= obj.producer_allowed_uses`

and the V557 state ceiling.

`rawlsing_next/m4_v557_v558_publication_repository.py:1229-1254`

V558 checks only:

`requested_uses <= producer_allowed_uses`

and:

`requested_uses <= v557_allowed_uses`.

Thus an unauthorized producer ceiling becomes self-validating downstream.

## Violated governing law

- H01 semantic-promotion prohibition;
- H05 permission widening;
- admission permission must remain an exact subset of FIELD FORGE relation permission;
- downstream V554/V557/V558 permission must never widen upstream permission;
- raw conditional-support counts may not acquire causal/mechanism authority.

## Minimal counterexample

Start from any lawful positive relation-specific `M1Evaluation` produced from a D admission whose only admitted target use is:

`STRUCTURAL_MEDIATION_INPUT`.

Then invoke:

```python
publish_and_resolve_relation_v554_at_current_m4(
    evaluation,
    producer_allowed_uses=("ACTIVE_CAUSAL",),
    v557_allowed_uses=("ACTIVE_CAUSAL",),
    requested_resolution_uses=("ACTIVE_CAUSAL",),
    v557_authority_ref=<exact M4 AuthorityRef>,
    v557_decision_state=V557DecisionState.ALLOW_ACTIVE_CAUSAL_CONTEXT,
)
```

Static control flow:

1. `m4_m1_evaluation_binding.py` stores `ACTIVE_CAUSAL` as producer permission.
2. `govern_v557` accepts it because V557 permission equals producer permission and the selected governance state allows `ACTIVE_CAUSAL`.
3. `resolve_v558` accepts it because requested permission is a subset of both newly supplied ceilings.
4. No comparison is made to D's `STRUCTURAL_MEDIATION_INPUT` permission or relation permission ceiling.

The existing hostile test at:

`tests/test_gt12_d_to_m4_typed_bridge.py:392-402`

tests only V557 widening **relative to the caller-created producer ceiling** (`REVIEW -> CONTEXT`). It does not attack producer-ceiling widening relative to D/FIELD FORGE authority.

## Smallest bounded repair recommendation

Do not let the relation-specific M4 helper mint `producer_allowed_uses` from an unconstrained caller sequence.

Instead, require an exact content-addressed relation-publication permission binding that:

1. names the admitted D target use and exact admission/relation authority refs;
2. supplies the authorized M4 permission atom ceiling or an already-governed exact translation;
3. is included in the relation M1 direct handoff identity/replay;
4. is verified before constructing V554 `StructuralObject` values;
5. requires:
   `producer_allowed_uses <= exact translated upstream ceiling`;
6. continues the existing V557/V558 subset checks after that upstream check.

If no competent frozen mapping from `STRUCTURAL_MEDIATION_INPUT` to M4 permission atoms already exists, fail closed rather than inventing one in integration glue.

Explicit hostile regression required:

- `ACTIVE_CAUSAL` injected as producer permission from the GT2 relation path must fail before V557;
- any requested M4 use absent from the exact upstream translation must fail.

## Downstream-worker impact

**YES — blocks authority-valid real downstream M4/V558 acceptance.**

A mechanical positive run may complete when supplied a convenient permission set, but the resulting producer permission is not currently proven to descend from the relation/admission authority. The real downstream execution worker should not treat such a terminal as authority-valid until this seam is repaired.

---

# E3-02 — OBSERVED_ZERO can become ADMITTED if blocker ref is removed

## Exact defect surface

FIELD FORGE explicitly classifies `OBSERVED_ZERO` as nonpositive:

`rawlsing_next/field_forge_conditional_support.py:41-54`

Specifically:

`NONPOSITIVE_PRODUCER_STATES` contains `OBSERVED_ZERO`.

PRE-V3 instead declares:

`rawlsing_next/wave1_ff_prev3_relation_admission.py:50`

```python
POSITIVE_RELATION_STATES = frozenset({"SUPPORTED", "OBSERVED_ZERO"})
```

During admission:

`rawlsing_next/wave1_ff_prev3_relation_admission.py:585-599`

1. `_upstream_decision(...)` permits `OBSERVED_ZERO` because it is in the allowed positive set;
2. the only later nonpositive protection is whether `relation_negative_or_limit_refs` is nonempty;
3. if that tuple is empty, the receipt becomes `ADMITTED`.

## Violated governing law

- H08 typed-negative laundering;
- FIELD FORGE nonpositive state must not become positive PRE-V3 admission;
- typed negative preservation may not depend solely on an optional/removable blocker reference when the typed state itself is already nonpositive.

## Minimal counterexample

Take the lawful bridge-generated `FieldForgeRelationEvidence` for an `OBSERVED_ZERO` relation and mutate only:

```python
replace(evidence, relation_negative_or_limit_refs=())
```

Keep unchanged:

- relation exact ref/hash;
- relation typed state = `OBSERVED_ZERO`;
- source/risk/universe refs;
- participants;
- relation owner/rule;
- relation authorities/current selection;
- relation permission ceiling including `STRUCTURAL_MEDIATION_INPUT`.

Then call:

```python
evaluate_gt2_relation_admission(RelationAdmissionRequest(tampered), rule)
```

Static control flow reaches the final `ADMITTED` return because `OBSERVED_ZERO` itself is treated as a positive allowed state and the stripped blocker tuple is empty.

The existing test:

`tests/test_gt12_closure_b_c_to_d_bridge.py:151-159`

proves only that the normal C->D bridge supplies a blocker for `OBSERVED_ZERO`. It does not attack removal of that blocker before the PRE-V3 admission evaluator.

## Smallest bounded repair recommendation

Make the PRE-V3 positive relation-state set exactly the genuinely positive FIELD FORGE state(s); under the current producer contract that means do not classify `OBSERVED_ZERO` as positive.

At minimum:

- remove `OBSERVED_ZERO` from `POSITIVE_RELATION_STATES`;
- give it an explicit nonpositive admission disposition under governing typed-negative law;
- if no exact disposition is already authorized, fail closed rather than inferring one;
- retain blocker-ref validation as additional closure evidence, not as the sole protection.

Add one hostile regression that strips the blocker ref while preserving `relation_typed_state="OBSERVED_ZERO"` and requires a nonpositive admission decision.

## Downstream-worker impact

**NO for the lawful real `SUPPORTED` positive path itself.**

**YES for final hostile-audit/adoption readiness.**

The real positive GT2 relation can still traverse D, but the candidate cannot pass the required typed-negative hostile boundary while this laundering path exists.

---

# Final E3 disposition

Material defects were found, therefore E3 does **not** return:

`PASS__GT12_FINAL_E3_STATIC_AUTHORITY_PREFLIGHT_CLEAR`

and does **not** claim:

`HOSTILE_AUDIT_PASS`.

No production semantic file was modified by this review worker.

No GT1/GT2 adoption was issued.

Recommended central ordering:

1. repair E3-01 first because it blocks authority-valid real downstream M4/V558 acceptance;
2. repair E3-02 before final hostile audit;
3. rerun only the bounded affected regression/hostile surfaces;
4. then proceed to the final hostile audit.
