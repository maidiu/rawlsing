# SEMANTIC PATCH AND ABI

## Source identity

| Surface | Current PRE-MAIN `8e44ca9c` | E5 patched |
|---|---|---|
| Lifecycle | `rawlsing_next/pre553_learned_product_lifecycle.py` blob `a11c9eb73abab9be118ef4f0b6e325e676059f27` | blob `dadf2362f3195c28ebaf97655e28cdba72c04fb3` |
| Release | `rawlsing_next/pre553_learned_product_release.py` blob `f76c390665f06ef126968ccf1a6b2d816f43ae92` | blob `1cb7692399aad8fb272c8c9ce956719527829007` |
| S06G test | absent | `rawlsing_next/tests/test_pre553_s06g_atomic_integrity.py` blob `9964464cd86c077ff5b9a99cea6fb0a41e516c80` |
| Fixtures | absent | `rawlsing_next/tests/s06g_fixtures.py` blob `f3040bb40a246e7b0bdea243060458d2045ab43b` |
| S06F helper shim | absent | `rawlsing_next/tests/test_pre553_s06f_native_owner_security.py` blob `6974f7d5e2f4ed66bb36b6160ce2ced08574d5b5` |
| E2 independent court | absent | `rawlsing_next/tests/test_pre553_e5_s06g_independent_hostile.py` blob `9a469ad0940216e02967c94159db943d2979154a` |

Production diff vs current PRE-MAIN:

- lifecycle: **+545 / −4**
- release: **+155 / −10**

The four lifecycle deletions are exactly the pre-hardening payload assignment, shallow projection copy, direct checkpoint `_append_events` and unchecked checkpoint pair extraction. The ten release deletions are exactly the static `_insert`, unguarded writer/read methods and non-checking representation/binding insertion. No unrelated S06F owner branch is merged.

## Semantic changes

1. **Recursive event immutability.** `LearnedProductLifecycleEvent.__post_init__` freezes payload recursively into `MappingProxyType`/tuples. `semantic_projection` uses `canonicalize` and exports detached JSON-safe material. Public `events`/`release_history` can no longer mutate internal identity.
2. **Checkpoint semantic replay.** `from_checkpoint` parses detached caller copies, opens an owner transaction, appends the event chain, calls `_verify_native_checkpoint_history` and `_verify_native_checkpoint_semantics`, and compares regenerated events/receipts/indexes/state. Rehashed publication fields, cross-release receipts and inconsistent checkpoint state are refused.
3. **Rollback atomicity.** All 17 B5 mutators use `_atomic_mutation`/`_mutation_transaction` with a reentrant owner lock and snapshot rollback on any `BaseException`. The 5 M2 writers use `_repository_mutation` with five-store rollback.
4. **Concurrency serialization.** B5 selection validation+commit and M2 check/insert are under the owner lock. Readers use `_locked_read`.
5. **Saved-helper refusal.** `_append_events`, `_commit_selection_transition_receipts` and M2 `_insert` require an active owner transaction; `_insert` is now an instance method with store/type/index checks. The in-body preflight also runs.
6. **M2 collision protection.** Public writer registration now checks release/subject/representation/binding integrity and inserts under the same repository transaction. `register_representation`/`register_binding` call `release_exact`; an unregistered foreign release raises `RELEASE_UNAVAILABLE` before the later oracle.
7. **LOCAL_UNAUTHENTICATED only.** `native_security_mode` is fixed to `LOCAL_UNAUTHENTICATED`; `require_external_issuer` raises `EXTERNAL_ISSUER_HOLD`. No caller flag/token elevates the owner.
8. **S06F support functions retained only as required:** `native_security_mode`, `require_external_issuer`, `_native_mutation_preflight`, `_verify_native_checkpoint_history`, and `verify_m2_release_subject_exact`. The last is needed by the frozen S06FR `test_actual_m2_release_to_subject_route_and_b5_crosscheck`; it is a source-free identity cross-check, not an issuer. No S06F acceptance test module is copied.

## ABI / callsite compatibility

Public B5/M2 signatures used by `pre553_learned_world_composition.py` are unchanged:

- B5: `stage_release`, `register_product`, `publish_product`, `selection_key`, `select_current`, `events`, `audit_replay`, `export_checkpoint`, `from_checkpoint`.
- M2: `register_representation`, `register_binding`, `release_exact`, `resolve_release_exact`, `publish_binding`, repository properties.

The adjacent integration courts pass **45/45** (`test_pre553_ee14_selected_current_asof_hq260.py` 15, `test_pre553_learned_world_composition.py` 30). The accepted B5 court passes **39/39**.

Behavioral ABI deltas, not signature breaks:

- `M2Repository._insert` changes from `@staticmethod` to an instance method; it is a private helper. Direct calls must use `repo._insert(...)` and require a native writer transaction.
- `register_representation`/`register_binding` now require an exact registered release; foreign release refs raise `RELEASE_UNAVAILABLE` earlier than before.
- Event payload mutation and rehashed checkpoint substitutions now raise typed errors instead of being accepted.

The two accepted M2 tests that fail are exactly the tests whose setup depends on inserting an unregistered foreign release. They are not edited. The new reconciled S06G tests assert early refusal, then lawfully register the foreign release/representation/binding and preserve the original `PUBLICATION_BINDING_MISMATCH` oracle.

## Test helper strategy

Current PRE-MAIN lacks `test_pre553_s06f_native_owner_security.py`. E5 adds:

- `s06g_fixtures.py`: standalone fixture helpers extracted from the historical S06F helper (no S06F tests).
- `test_pre553_s06f_native_owner_security.py`: a compatibility shim exposing only those helpers so the frozen S06FR overlay can import its original fixture names.
- The S06G test imports `s06g_fixtures`, not the S06F test module.

No S06F acceptance test is imported or executed. No test was edited to make a failure pass.
