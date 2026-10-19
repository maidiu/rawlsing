# E41 empirical slice provider contract — v1.1 extension over the accepted N10E seam

**Status:** CANDIDATE / SOURCEFREE / TEST_ONLY. Not a scientific adoption, source right,
model-use grant, N11 issue or production permission.

## What is served

| Layer | Owner | Contract |
| --- | --- | --- |
| Direct scalar route | `rawlsing_next.pre553_empirical_possibility_provider.provide_empirical_possibility_slice` (accepted, unchanged) | `N10E_EMPIRICAL_POSSIBILITY_SLICE_PROVIDER@1.0.0` |
| Multi-conditioner / discovery / recursive routes | `e41_provider_extension.provide_empirical_possibility_slice_ext` (NEW, this return) | `N10E_EMPIRICAL_POSSIBILITY_SLICE_PROVIDER_EXT@1.1.0` |
| Accepted composition owner | `rawlsing_next.pre553_analytical_composition.compose_positioned_subject_possibility` (accepted, unchanged) | C1-01/C1-02 analytical composition |
| Public consumer | `rawlsing_next.source_backed_positioned_subject_possibility.evaluate_positioned_subject_possibility` (accepted, unchanged) | `SOURCE_BACKED_POSITIONED_SUBJECT_POSSIBILITY@1.0.0` |
| Original E04 client | vendored byte-identical `product.nonparent.consume` (TEST_ONLY, provenance in `vendor/__init__.py`) | `NONPARENT_OPTIONS` |

The extension does not compute geometry. It carries exact caller-owned determinants
into the accepted owners and returns the accepted objects plus a v1.1 receipt.

## Routes

* `DIRECT_VIA_ACCEPTED_PROVIDER_FUNCTION` — exactly one conditioner binding; the extension
  calls the accepted provider function itself. The extension result carries
  `base_result_or_null` with the accepted provider's exact receipt/result objects
  (object identity asserted by the courts).
* `DIRECT_MULTI_CONDITIONER_VIA_ACCEPTED_COMPOSITION` — more than one conditioner
  binding; the accepted N10E R1 provider is scalar-grain by its own contract, so the
  extension calls the accepted composition owner directly with the same request fields.
* `I05_EXACT_BOUNDED_VIA_ACCEPTED_COMPOSITION` — exact-bounded discovery material
  (`discovery_result` + its exact `discovery_receipt_ref`).
* `MX01R2_RECURSIVE_VIA_ACCEPTED_COMPOSITION` — persisted recursive handoff
  (`recursive_handoff`) with lineage validation by the accepted owner.

## Request shape (v1.1)

Exactly the accepted provider request fields plus optional
`discovery_result` / `discovery_receipt_ref` / `recursive_handoff`. There is **no**
evidence/geometry/probability input channel; the signature is asserted by
`test_extension_exposes_no_precomputed_geometry_channel` and the module guard
`assert_extension_delegates_to_inherited_c1()`.

## Result states

* `EXACT_SUPPORTED_SLICE_PRODUCED` — accepted-owner generated evidence exists and is
  the composition's own evidence object; consumer result is the composition's own
  consumer result. Both object-identity assertions are enforced in `__post_init__`.
* `TYPED_REFUSAL` — producer fact state not `SUPPORTED` or no evidence; carries
  `refusal_state ∈ {SLICE_NOT_SUPPORTED_UNDER_EXACT_MODEL_LAW, OWNER_TYPED_REFUSAL}`,
  no geometry, no consumer result. Owner typed errors propagate unchanged (never
  laundered into a synthetic slice).

## Receipt (`N10E_EMPIRICAL_SLICE_PROVIDER_RECEIPT@1.1`)

Carries: extension contract id, producer route, provider state, producer
query/predicate/fact refs and fact state, source universe and release refs, consumer
query ref, binding fingerprint, witness ref/hash, model rule hash, generated evidence
ref + producer-derived flag, consumer result state/hash, composed result identity
hash, coverage state, joint component count/order semantics, discovery receipt refs,
discovery frontier ref, recursive handoff refs, recursive lineage refs, base receipt
ref (direct route) and refusal state. Receipt material is canonically hashed.

## Provenance and evidence law

* Every emitted slice in this campaign is produced by an accepted owner from
  accepted fixture/source material; no caller-supplied probabilities enter.
* `artifacts/computed_slice_evidence.json` records, per operation, the exact
  generated evidence ref, composed identity and coverage state.
* `artifacts/slice_consumer_receipt.json` records the actual consumer result state
  and identity per operation, including the original E04 `NONPARENT_OPTIONS`
  client receipt (`OPTIONS_AND_SOURCE_SUPPORT_PRODUCED`, route probability null).

## Ceilings

Provider receipt ≠ adoption; computed slice ≠ source right; positioned-subject
possibility ≠ individual prediction; E04 TEST_ONLY receipt ≠ production permission.
Original-35 occupancy remains HELD (see `artifacts/f1f4_coverage_ledger.json`
`held_original_scope`).
