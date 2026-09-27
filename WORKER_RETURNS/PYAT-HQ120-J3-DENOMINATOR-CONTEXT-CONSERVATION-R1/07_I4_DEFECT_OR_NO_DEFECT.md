# J3 I4 defect adjudication

Verdict:

`ACTUAL_NARROW_ADAPTER_DEFECT_FOUND__MINIMAL_GENERIC_REPAIR_APPLIED__NO_I4_SEMANTIC_REDESIGN`

## 1. Pre-repair state

HQ120 correctly treated I4 as source-free-green for the generic composition contract.

J3 did not reopen that result broadly.

The J-shaped court asked one narrower question that the generic I4 suite had not required:

> Can caller-owned exact product-specific dependencies—especially an already-authoritative `ComponentAuthorityVectorReceipt`—enter the canonical M01→M1 dependency set without inventing a new semantic owner?

Pre-repair answer: **no public I4 path existed**.

`build_m1_bundle_from_m01` fixed `additional_dependency_refs` to only:

`(result.c11_release.release_ref,)`

and `compose_learned_world` accepted no extra exact dependency refs.

## 2. Exact failing witness

Pre-repair governed run:

- workflow run: `36334313842`
- job: `108662119360`
- existing/current tests passing before fixture setup failure: **147**
- J3 tests reaching fixture setup: **18 errors**
- common error:

`TypeError: compose_learned_world() got an unexpected keyword argument 'additional_dependency_refs'`

The failure occurred before any J3 semantic assertion could be weakened or reinterpreted.

This is an adapter interface omission, not evidence that M1/M2/B5 lose dependency refs once present.

## 3. Minimal repair

File changed:

`rawlsing_next/pre553_learned_world_composition.py`

Repair commit:

`37670bf5bb9fbdfa1ee7cec2ad742599dff80a9f`

The implementation delta is intentionally generic.

### build_m1_bundle_from_m01

Adds:

`additional_dependency_refs: Iterable[ExactRef] = ()`

Normalizes through existing exact-ref helper `_refs(...)`.

Passes:

`(result.c11_release.release_ref, *exact_additional_dependencies)`

to the already-existing M1 `additional_dependency_refs` field.

### compose_learned_world

Adds the same optional argument.

It validates exact refs once and forwards them only when:

`route == M01_M1_M2_B5`.

If nonempty additional dependencies are supplied on another route, composition fails closed rather than silently ignoring them.

## 4. What the repair does not do

It does not add:

- V550J/V551J/V552J packet fields;
- denominator fields to I4;
- component roles to I4;
- a J authority registry;
- inferred source semantics;
- inferred family-J authority;
- scalar readiness;
- automatic M1 family-rule selection;
- automatic lifecycle publication/currentness;
- Field Forge authority;
- PRE-V3 structural admission.

I4 remains an adapter/compositor.

The extra refs are semantically opaque exact dependencies. Their meaning and authority continue to belong to their existing producers.

## 5. Post-repair proof

Final semantic candidate:

`374763b1fd5ff408b8c8f5691f95c818595b1566`

Final governed execution:

- execution SHA: `ccd2bebbe9a4c83e0f6c1428cc868080088cfee2`
- workflow run: `36334688621`
- job: `108663177657`
- bounded court: **165/165 PASS**
- protocol self-test: **20/20 PASS**
- artifact ID: `10937121266`
- artifact digest: `sha256:5bfc7bf52d8368dd7ff91d06529f21992c1f55e858526d2a418e0ce3c3f96011`

The durable J3 test source is:

`WORKER_RETURNS/PYAT-HQ120-J3-DENOMINATOR-CONTEXT-CONSERVATION-R1/08_test_j3_conservation.py`.

A byte-identical temporary mirror under `rawlsing_next/tests/` was used only because the governed court protocol accepts test paths exclusively from that namespace. The mirror was deleted after qualification and the prior court spec restored.

## 6. Final holding

The defect is repaired at the smallest lawful seam.

I4 remains source-free-green, now with an exact generic path for caller-owned dependencies required by J-shaped final-consumer conservation.

No broader semantic redesign is warranted by J3.
