# ACCEPTED M2 TWO FIXTURE VERDICT

## Exact unchanged tests

Both accepted tests are in `rawlsing_next/tests/test_pre553_learned_product_release.py`, blob `d45b54190815b4c6af506579962a9aac8a7074c2` at both PRE-MAIN `8e44ca9c` and E5 `96e6d49a`.

| Test | E5 result | Exception |
|---|---|---|
| `test_17_binding_cannot_resolve_different_release` | FAIL | `M2ReleaseError: RELEASE_UNAVAILABLE: requested exact release is unavailable` |
| `test_18_endpoint_failover_only_among_same_release` | FAIL | `M2ReleaseError: RELEASE_UNAVAILABLE: requested exact release is unavailable` |

Failure locations:

- test 17 calls `repo1.register_representation(RepresentationRecord(...))` directly with a release created only in a second repository. E5 refuses at `pre553_learned_product_release.py:606`.
- test 18 calls `repo.register_binding(other_binding)` directly with a binding created only in a second repository. E5 refuses at `pre553_learned_product_release.py:632`.

Neither test was edited, skipped or xfailed. The accepted M2 court is 26/28, not 28/28.

## What the original M2 owner contract says

The adopted M2 public surface is the module-level operations listed by the HQ118 I2 owner receipt:

`register_producer_subject(...)`, `constitute_closure(...)`, `constitute_release(...)`, `register_representation(...)`, `publish_binding(...)`, `resolve_release_exact(...)`, `resolve_subject_exact(...)`, `explain_release(...)`, `affected_release_refs(...)`.

The original public functions already required a locally registered exact release:

- `register_representation(...)` begins `release = repository.release_exact(release_ref)`.
- `publish_binding(...)` begins `release = repository.release_exact(release_ref)` and then resolves the exact representation.
- `resolve_release_exact(...)` verifies every supplied binding targets the requested release before failover.

The owner receipt describes `M2Repository` as an exact-index in-memory runtime used as a storage-neutral reference realization, and states the resolution law: failover is explicit and ordered by exact binding refs, and every binding is verified to target the requested exact release before failover begins.

The accepted tests do not use the published owner operations for their hostile setup. They call the class storage methods directly:

- test 17 comment: a foreign representation exact ref is inserted intentionally, while copying the foreign producer/closures/release is "intentionally avoided".
- test 18 comment: the foreign binding is registered "solely to attack the failover list".

Those setups exercise a low-level insertion path that the public owner operations already refused. They are attack-fixture construction, not evidence that foreign release registration was a supported owner operation.

## Verdict on the early refusal

`RELEASE_UNAVAILABLE` on an unregistered foreign release is a **lawful tighter sourcefree boundary at the repository writer**, not a permissive-resolution regression and not an uncontrolled failure.

Reasons:

1. The published M2 operations already required `release_exact` before representation or binding creation.
2. The original resolution oracle remains: if the foreign release, subject, closures and representation are lawfully imported, `PUBLICATION_BINDING_MISMATCH` still fires for the cross-release binding/failover attack.
3. No source meaning, release identity, lifecycle publication, currentness, consumer permission or external authority was changed.
4. The refusal is typed `M2ReleaseError` with code `RELEASE_UNAVAILABLE`; stores remain unchanged.

The two accepted tests nevertheless encode a lower-level setup contract that no longer accepts the attack fixture. That is a real compatibility change at the accepted-test contract grain. It cannot be waved through merely because the runtime behavior is stronger.

## Reconciled oracle proof

E5 adds:

- `test_reconciled_m2_17_early_refusal_and_lawful_downstream_mismatch`
- `test_reconciled_m2_18_early_refusal_and_lawful_failover_mismatch`

Both pass. Each first asserts `RELEASE_UNAVAILABLE`, then lawfully registers the foreign subject, closures and release, registers the representation/binding, and preserves `PUBLICATION_BINDING_MISMATCH`.

E6 independently re-derived both scenarios without importing the E5 reconciled test bodies. The reviewer-owned court confirms:

- early refusal is atomic; the five M2 stores are unchanged;
- lawful import of the foreign subject, five closures and release succeeds;
- representation and binding registration then succeed;
- `publish_binding(repo, first_release, foreign_locator, foreign_integrity)` raises `PUBLICATION_BINDING_MISMATCH`;
- cross-release failover with the imported foreign binding raises `PUBLICATION_BINDING_MISMATCH`;
- same-release failover still selects the second valid binding.

The original `PUBLICATION_BINDING_MISMATCH` oracle is therefore preserved, not replaced by the earlier refusal.

## Owner permission

The frozen evidence contains no accepted-M2 owner permission for a versioned fixture amendment:

- E5 `ACCEPTED_TEST_CONFLICT_AND_NEGATIVES.md` states "Owner choice: decide whether the two accepted fixtures are invalid setups ... authorize a new fixture-update review ... do not weaken `release_exact` or edit the accepted tests in place."
- E5 `EXACT_FANIN_MANIFEST.json` records the same owner choice.
- E2 `CONDITIONAL_REPAIR_OR_REJECTION.md` requires an owner decision and a separate fixture-update review.

No document in the frozen basis authorizes E5 or this reviewer to amend the accepted fixtures. Under the E6 launch, that permission cannot be invented.

## Binary consequence

- If the owner determines the two accepted fixtures are invalid under the stricter public-boundary contract and issues a versioned amendment, the M2 writer hardening has merit and the downstream oracle is preserved. The source patch can proceed to a distinct receiving review.
- If the owner determines direct foreign-record registration is a supported lower-level contract, the M2 `register_representation`/`register_binding` early-refusal hunks must be rejected; the remaining B5/M2 transaction, immutability and replay hunks are separable.
- Until one of those owner decisions exists, E5 is not fan-in ready and the accepted M2 court remains RED.

Named hold: `HOLD_E5_LOCAL_SOURCEFREE_FANIN_PENDING_OWNER_AUTHORIZED_VERSIONED_M2_FIXTURE_AMENDMENT`.
