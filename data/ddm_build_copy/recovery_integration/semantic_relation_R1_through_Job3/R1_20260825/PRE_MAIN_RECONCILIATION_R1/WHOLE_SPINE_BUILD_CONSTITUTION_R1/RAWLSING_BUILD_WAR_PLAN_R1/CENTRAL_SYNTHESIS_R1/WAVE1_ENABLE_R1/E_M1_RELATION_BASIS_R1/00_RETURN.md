# RAWLSING WAVE 1E — M1-COMPATIBLE ADMITTED-RELATION BASIS DESIGN R1

Status:

`PASS__WAVE1E_M1_RELATION_BASIS_DESIGN_READY`

## Execution posture

Repository: `maidiu/rawlsing`

Worker branch:

`agent/rabochii-warplan-w1e-m1-relation-basis-design-r1`

Verified exact starting HEAD:

`d15f8973ddeff46dbaa15f352fe5d7e59e1fe1a3`

Immutable Wave 1 instruction/evidence ref consumed:

`3454b15ff7ef388f6e028f78fad4e229c9aa969f`

Sibling Wave 1 Enable branches were not consumed. FIELD FORGE R2 was not reopened. No physical architecture was selected. No current M1 code was modified.

## Central holding

The current M1/V554 runtime cannot lawfully consume a positively admitted FIELD FORGE relation through either of its existing basis kinds.

Current exact basis kinds are:

- `DIRECT_STRUCTURAL_EMPIRICAL_ADMISSION`;
- `V553_TEMPORAL_OBJECT`.

The first is semantically and structurally bound to `StructuralEmpiricalAdmission` identity/authority/lineage. The second is semantically and structurally bound to V553-owned temporal objects whose current projection also carries originating structural-empirical-admission lineage.

Therefore:

`ADMITTED_FIELD_FORGE_RELATION != DIRECT_STRUCTURAL_EMPIRICAL_ADMISSION`

and

`ADMITTED_FIELD_FORGE_RELATION != V553_TEMPORAL_OBJECT`.

A relation must not be made M1-compatible by copying relation IDs into fields named `structural_empirical_admission_*`, by fabricating a current `StructuralEmpiricalAdmission`, or by presenting relation material as an existing V553 object.

## Recommended compatibility design

Use a **separate relation-specific M1 ingress contract** that produces the existing downstream `M1Evaluation` / V554 `F1`, `F2`, `B1`, and direct V557-handoff shapes, while leaving the current empirical M1 evaluator and basis contract unchanged.

Proposed design identity for central reconciliation:

`M1_ADMITTED_FIELD_FORGE_RELATION_V554_INGRESS@1.0.0`

Proposed basis kind:

`ADMITTED_FIELD_FORGE_RELATION`

Proposed first/minimum signature:

`V554-SIG-004-NONTEMPORAL-ADMITTED-RELATION-EXACT`

This signature is intentionally distinct from current `V554-SIG-001-NONTEMPORAL-EXACT`. A governed use must explicitly select the relation signature; M1 must never choose between empirical-direct and relation bases by proximity, availability, chronology, or a winner heuristic.

## Why a separate ingress contract is the minimum lawful adaptation

1. It preserves current `M1_TEMPORAL_V554_INGRESS_SEAM@1.0.0` empirical semantics exactly.
2. It avoids semantic type forgery through `DIRECT_STRUCTURAL_EMPIRICAL_ADMISSION`.
3. It avoids a broad rewrite of current M1 dedup, F2/B1, publication, or V557/V558 mechanics.
4. It permits relation-specific projection/equivalence fields, especially exact relation participant role/order/cardinality and relation-admission lineage.
5. It can return the same `M1Evaluation` data type and F1/F2/B1 object shapes, minimizing downstream adaptation.
6. It makes the new semantic boundary explicit enough for the required later bounded hostile audit.

## Minimum positive input

A relation-basis candidate may be constructed only from one exact positive relation-admission result from the separately governed FIELD FORGE relation → PRE-V3 admission surface.

The exact sibling W1D field names are intentionally not presumed in this independent lane. Central fan-in must verify a lossless mapping from W1D's admitted-relation object into the following semantic requirements:

- exact relation-admission decision ref/hash;
- exact relation-admission authority ref/hash;
- exact `ADMITTED` positive state;
- exact originating `FIELD_FORGE_EXACT_RELATION` ref/hash;
- exact relation semantic identity;
- exact participant identities and claim-constitutive role/order/cardinality identity;
- exact focal structural proposition ref for the governed V554 use;
- exact native scope identity;
- exact target-use permission including `STRUCTURAL_MEDIATION_INPUT`;
- exact effective-time/interval material required by that use;
- exact source-universe identity;
- exact estimand identity where claim-constitutive;
- exact measure/weight authority identity where claim-constitutive;
- exact comparability/transport authority refs where actually required;
- exact applicable negative/denial/noncomparability refs;
- exact interpretation-critical semantic authority refs;
- exact producer/replay root and authority snapshots;
- exact information-loss declaration.

No field above transfers semantic ownership to M1/V554.

## Minimum relation-basis candidate

The compatibility layer should emit a typed candidate equivalent to:

`M1AdmittedRelationBasisCandidate@1`

with:

- `basis_kind = ADMITTED_FIELD_FORGE_RELATION`;
- exact `basis_ref` to the relation-basis projection object;
- immutable projection + projection hash;
- relation-specific equivalence key;
- exact selected rule-relevant basis semantics;
- exact upstream relation-admission and relation provenance;
- no actor data or actor permission.

Only a positive ready candidate enters the relation-specific M1 evaluator. Nonpositive upstream admission states remain typed outside the positive candidate path and must not be collapsed to an empty positive candidate list.

## Relation-specific equivalence law

The relation path should preserve the current M1 dedup philosophy but not reuse the empirical-direct equivalence schema verbatim.

At minimum the relation equivalence key must bind:

- focal structural proposition ref;
- target use;
- V554 rule ID/version/hash;
- basis semantic class = `ADMITTED_FIELD_FORGE_RELATION`;
- rule-relevant structural semantic identity fingerprint;
- relation participant/role/order/cardinality fingerprint;
- native scope fingerprint;
- rule-relevant effective-time semantics fingerprint;
- originating admitted-relation lineage fingerprint;
- source-universe fingerprint;
- estimand fingerprint;
- measure/weight-authority fingerprint;
- source-relation/comparability authority fingerprint where required;
- interpretation-critical semantic-authority fingerprint.

This means an empirical-direct basis and an admitted-relation basis do **not** deduplicate across basis classes merely because they point at a similar proposition.

## Dedup / conflict behavior

For `SIG-004`:

- identical relation-basis candidates with the same exact relation equivalence key and identical selected rule-relevant semantics may collapse to one support with provenance aliases;
- different relation equivalence keys must never be winner-selected;
- conflicting selected rule-relevant semantics for one purported equivalent group must fail `EQUIVALENCE_UNKNOWN`;
- empirical-direct and V553 candidates are reference-only/noncounting for the relation signature;
- missing equivalence components fail closed;
- candidate/invocation binding mismatch is integrity failure.

The current M1 output distinctions should be reused where semantically exact: `ELIGIBLE`, `VALID_EMPTY`, `INTEGRITY_FAILURE`, explicit denial, negative temporal authority, missing authority, unknown/conflicting authority, temporal-signature ineligibility, and `EQUIVALENCE_UNKNOWN`.

## Temporal law

This first relation ingress should support **only** a relation whose exact governed V554 use requires no new V553-owned temporal meaning.

A positive direct relation route therefore requires:

- an exact W1D relation admission;
- exact target-use temporal sufficiency for this use;
- `V553_NOT_REQUIRED_FOR_THIS_USE` or its lawfully reconciled equivalent;
- zero required new V553 temporal operations.

If the selected relation requires new temporal observation/relation semantics, this lane does not coerce it into the direct relation signature and does not reuse current V553 projection fields that are hard-bound to structural-empirical-admission lineage.

Return the exact typed temporal blocker and require a separately relation-aware V553 intake/lineage adaptation before a temporal relation can reach M1.

This preserves:

`RELATION_TEMPORAL_MEANING_REQUIRED -> V553_OWNER_REQUIRED`.

## V554 ownership and output reuse

Once the relation-specific M1 ingress returns `ELIGIBLE`, V554 may reuse the current F1/F2/B1 semantics:

- one canonical basis semantic identity;
- exact V554 rule/signature/target-use binding;
- F2 condition records with existing K01-K09 disposition law where applicable;
- B1 permission gate for V555 use;
- direct V554→V557 handoff only under exact publication authority.

V554 owns only its affordance/applicability/basis-selection result. FIELD FORGE retains relation meaning; the relation-admission owner retains admission meaning; empirical/source owners retain empirical/source meaning.

## Downstream M4 compatibility

Current `m4_v557_v558_publication_repository.py` requires an exact `M1Evaluation` and current M1 contract identity before adapting F1/F2/B1 into V557 objects.

The future minimum integration change is therefore mechanical and explicit:

- preserve the current accepted M1 contract ID for empirical M1 evaluations;
- add the new relation-ingress contract ID to the exact accepted M1-evaluation contract set for `structural_objects_from_m1(...)`;
- preserve the same F1/F2/B1 hash validation, producer family `V554`, and direct-handoff validation;
- do not widen allowed producer families or permissions.

Do not silently change the current empirical M1 contract ID merely to make the relation path fit.

## Typed nonpositive relation-basis preparation states

Before positive M1 invocation, the compatibility adapter should preserve at least:

- `RELATION_BASIS_READY`;
- `VALID_EMPTY`;
- `DENIED`;
- `DEFERRED_MISSING_AUTHORITY`;
- `UNRESOLVED`;
- `NONCOMPARABLE`;
- `TARGET_USE_NOT_PERMITTED`;
- `TEMPORALIZATION_REQUIRED`;
- `INTEGRITY_FAILURE`.

Only `RELATION_BASIS_READY` emits `M1AdmittedRelationBasisCandidate@1`.

No nonpositive state may be converted into a placeholder candidate, default relation, zero-valued relation, or empirical-direct basis.

## No actor inference

This entire path remains PRE-V3 actor-independent structural world construction.

Forbidden:

- relation → actor belief;
- relation → actor knowledge;
- relation → actor encounter/opportunity;
- relation → actor route realization;
- relation → actor preference/identity;
- V554 F1/B1 → actor state;
- publication/resolution → actor state.

`PRE_V3_STRUCTURAL_OBJECT != V3_REALIZED_PERSON`.

## Implementation disposition

No production code change is authorized by this lane.

For the later narrow implementation wave, the smallest expected delta is:

1. add relation-specific candidate/projection/equivalence parser and evaluator without modifying current empirical evaluator behavior;
2. reuse the existing `M1Evaluation`, M1 decision vocabulary, F2/B1 construction and V554→V557 handoff shapes;
3. add exact relation-signature/dedup/negative tests;
4. minimally update M4's accepted M1 contract-ID binding for the relation evaluator;
5. run current M1/M4 inherited regressions plus relation-specific hostile cases.

## Central fan-in recommendation

Reconcile W1D's independently constituted relation-admission output against this lane at semantic-field grain, not by field-name resemblance.

If the selected W1C relation is non-temporal for the exact first V554 target use, use the relation-specific direct M1 signature above.

If the selected relation needs new V553 temporal meaning, do not widen this design: return the exact temporalization gate and either choose a cheaper non-temporal first relation or commission the minimum relation-aware V553 extension.

Terminal:

`PASS__WAVE1E_M1_RELATION_BASIS_DESIGN_READY`
