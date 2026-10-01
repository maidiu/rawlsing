# PYAT C5/N5 — RETAINED CURRENT GT2 STRUCTURAL CONTEXT — R1

Status: `PASS_C5_N5_SOURCE_FREE_CURRENT_PRODUCT__INDEPENDENT_REVIEW_REQUIRED`

Branch: `agent/opencode-pyat-hq149-c5-n5-current-structural-context-r1`
Base: `f69ad91f594219cb3ab0fadc9694af86dee188f7`
Commission tip: `71cd049bed3fe921e639af9c3e5921d6e0ebcb51`

## What was built

| File | Role |
|---|---|
| `rawlsing_next/current_gt2_structural_context.py` | The service: `evaluate_current_gt2_structural_context()` |
| `rawlsing_next/tests/test_current_gt2_structural_context.py` | 30 courts across AT22/AT23/AT24 |

The service takes **no caller arguments** and composes six already-retained
owners, each through its single public API:

1. `pre553_repo_native_seal.load_current_gt2_query_fact()`
2. `field_forge_conditional_support.produce_exact_conditional_support_profile`
3. `gt12_c_to_d_relation_bridge.admit_gt12_c_relation`
4. `gt12_d_to_m4_typed_bridge.evaluate_typed_d_to_e_at_v554`
5. `gt12_d_to_m4_typed_bridge.publish_and_resolve_relation_v554_at_current_m4`
6. `gt12_e2b_publication_governance_binding.load_current_gt12_e2b_publication_governance_binding()`

It returns the owners' own objects and refs, untranslated, so a caller can audit
them.

## Retained floor: verified live, not assumed

All eight values matched exactly on first execution:

| Value | Observed |
|---|---|
| query hash | `e4ec3998…d0d0` ✓ |
| fact hash | `540236d5…1f46` ✓ |
| replay hash | `c0c23ca2…884f` ✓ |
| risk-set hash | `0484fa5c…1313b` ✓ |
| state / denominator | `SUPPORTED` / `19,210` ✓ |
| conditioner → target | `Q86B → Q86A`, arity 2, SEMANTIC_ORDERED ✓ |
| relation identity | `1ffdfe53…d19` ✓ |
| admission identity | `a445e43d…b08d` ✓ |

Admission came back exactly `ADMITTED` with reason
`EXACT_GT2_RELATION_ADMITTED_FOR_STRUCTURAL_MEDIATION_INPUT`, permission ceiling
exactly `("STRUCTURAL_MEDIATION_INPUT",)`, and no applicable
negative/denial/noncomparability refs.

## AT22 — retained input, support, topology, provenance

8 courts. Two independent service calls produce identical relation, admission,
publication and resolution identities. The strongest assertion is
`test_at22_service_returns_owner_objects_without_recomputation`, which
independently re-runs the FIELD FORGE producer and proves the relayed relation is
**byte-identical** to the owner's own output (`as_dict()` equality), not a
reconstruction. A separate court scans the service source to confirm it authors
no cell projection, probability, fraction or profile material.

## AT23 — structural authority and admission

14 courts covering all nine commissioned hostile themes: wrong source identity,
wrong risk set, non-SUPPORTED state, wrong denominator, reversed conditioner/target
role, wrong target use, missing target-use permission, nonpositive admission, and
permission widening.

Notably, **permission widening is rejected by the producer owner itself**
(`FieldForgePermissionWideningError`) when the relation ceiling is widened beyond
the producer's — the service never gets the chance to launder it.

The service explicitly claims no causal, mechanism, or actor semantics. The owner
constants themselves carry `CONDITIONER != CAUSE`.

## AT24 — objective consumption

8 courts. Observed end state:

- M1 `ELIGIBLE` over `ADMITTED_FIELD_FORGE_RELATION` under contract
  `M1_ADMITTED_FIELD_FORGE_RELATION_V554_INGRESS@1.0.0`
- bridge preparation `RELATION_BASIS_READY`; only descent `V554_TO_V557_DIRECT`
- publication entry: `semantic_class=F1`, `producer_family=V554`,
  `source_stage=M1_RELATION_V554_TO_V557`, `producer_allowed_uses=("CONTEXT",)`
- V557 `ALLOW_CONTEXT_ONLY` with uses `("CONTEXT",)`; V558 requested `("CONTEXT",)`
- resolution selection `SELECTED` / `ELIGIBLE` with a matching resolution key
- `resolved_structural_context is None` — no actor state, no V3 effect
- no `REVIEW`, no `ACTIVE_CAUSAL`, no V553/V555/V556 substitute basis

## Test obligations

| Court | Tests |
|---|---|
| new C5 court | 30 |
| `test_field_forge_conditional_support.py` | 11 |
| `test_wave1_ff_prev3_relation_admission.py` | 35 |
| `test_m1_admitted_field_forge_relation_v554_ingress.py` | 14 |
| `test_gt12_e2b_actual_object_consumer_harness.py` | 14 |
| `test_pre553_repo_native_current_rehydration.py` | 16 |
| **total** | **120 passed, 0 failed** |

No existing owner was modified, so no existing owner can have regressed; all five
owner courts were re-run green anyway.

## Two things worth flagging

**I did not need the C4 work described in your note.** The commission's dependency
law is explicit that C4 is not required for this selected C5 scope, and that it
does not generalize beyond the frozen GT2 canary. I built only the C5/N5 product.

**My first draft asserted the wrong thing about the M1 decision state.** I compared
`str(M1DecisionState.ELIGIBLE) == "ELIGIBLE"`, which fails because `str()` on an
enum includes the class name. The service now compares the enum *name*, which is
the correct identity check. Worth knowing the guard is real rather than decorative.

## Scope ceiling

Valid only for the frozen GT2 canary. The service asserts no conditioner=CAUSE,
target=EFFECT, support=mechanism, or population=actor identity, and carries no
pressure/hegemony/capital semantics. None of that is claimed here because none of
it is authorized.

## Return inventory

`00_RETURN.md`, `01_INPUT_AND_OWNER_BINDING.json`,
`02_AT22_AT24_ACCEPTANCE_MATRIX.json`, `03_EXECUTION_RECEIPT.json`,
`04_FINAL_DISPOSITION.json`.

## Terminal

`C5_N5_STRUCTURAL_ADMISSION_RETURNED__HQ_ADJUDICATION_REQUIRED`