# E5 SOURCE AND HUNKS

## Exact identity

| Surface | PRE-MAIN `8e44ca9c` | E5 `96e6d49a` | S06G `0ff13995` |
|---|---|---|---|
| Lifecycle | blob `a11c9eb73abab9be118ef4f0b6e325e676059f27` | blob `dadf2362f3195c28ebaf97655e28cdba72c04fb3` | same as E5 |
| Release | blob `f76c390665f06ef126968ccf1a6b2d816f43ae92` | blob `1cb7692399aad8fb272c8c9ce956719527829007` | same as E5 |
| S06G test | absent | blob `9964464cd86c077ff5b9a99cea6fb0a41e516c80` | blob `23aaf95d315980ea7587373e30188c7f36cb2b73` |
| Fixtures | absent | blob `f3040bb40a246e7b0bdea243060458d2045ab43b` | absent (S06F helper module used) |
| Helper shim | absent | blob `6974f7d5e2f4ed66bb36b6160ce2ced08574d5b5` | full S06F test module |
| E2 court | absent | blob `9a469ad0940216e02967c94159db943d2979154a` | absent |

Parent chain: `8e44ca9c` -> `f3defd3cb84e2bab4be3df3300fd1289c6ebadfb` (source hardening) -> `96e6d49ac18274332751c5fbb87c6ed370e8fd9c` (return artifacts only). `8e44ca9c` is an ancestor of E5 head. No merge or PRE-MAIN mutation occurred.

Exact numstat from current PRE-MAIN to E5 source content:

| File | Added | Deleted |
|---|---:|---:|
| `rawlsing_next/pre553_learned_product_lifecycle.py` | 545 | 4 |
| `rawlsing_next/pre553_learned_product_release.py` | 155 | 10 |

The E5 production files are byte-identical to the S06G reference blobs. The E5 base is current PRE-MAIN, not the S06G parent; the independent courts and adjacent composition tests demonstrate that the full-file identity applies cleanly here.

## Per-hunk merit

| Hunk | Change | Merit | Finding |
|---|---|---|---|
| B5 payload | Recursive `_freeze_payload`, frozen event payload, canonical detached `as_dict` | HIGH | Nested mutation refused; exported data cannot mutate internal identity; tested. |
| B5 transaction | `_copy_state_containers`, `_atomic_mutation`, `_locked_read`, `_mutation_transaction` | HIGH | One reentrant lock spans validation, append and projection; owner containers restore on `BaseException`; readers wait. |
| B5 checkpoint history | `_verify_native_checkpoint_history` replays typed event chain into projections | HIGH | Detects rehashed publication fields, arbitrary receipt rewrites, dropped receipts, selection/event inconsistency. Local consistency only. |
| B5 checkpoint semantics | `_verify_native_checkpoint_semantics` re-executes native operations and compares complete events, receipts and state | HIGH | Rejects coherent-looking but semantically forged checkpoints; catches malformed replay inside typed conflict. |
| B5 restore | `canonicalize` caller checkpoint, schema checks, transaction-scoped append, verifier calls | HIGH | Caller containers detached; cold restore preserves checkpoint hash and canonical semantics. |
| B5 saved helpers | `_append_events`, `_commit_selection_transition_receipts` require active transaction; in-body preflight in public mutators | MEDIUM-HIGH | Ordinary saved-helper and `__wrapped__` bypasses refuse. Same-process arbitrary code can still open private transactions/replace callables. |
| M2 transaction | `_repository_mutation`, `_repository_read`, five-store snapshot/rollback, instance `_insert` | HIGH | Serializes check/insert and rolls back all five stores; store/type/index identity checked. Private `_insert` ABI changed. |
| M2 writer validation | `register_release`, `register_representation`, `register_binding` validate local exact release, subject/closure and representation/binding consistency | HIGH at boundary; CONFLICT at two accepted fixtures | Public M2 functions already required `release_exact`; the patch closes the direct-method bypass. Two accepted tests used the bypass as setup and now fail early. |
| Security mode | `LOCAL_UNAUTHENTICATED` property, `require_external_issuer` hold, native preflight | HIGH | No caller flag/token can elect protected custody; external issuer remains held. |
| Test support | `s06g_fixtures.py` and S06F-named helper shim | TEST-ONLY | Five helpers AST-identical to historical S06F helper functions; shim has zero test functions; no S06F acceptance test transplanted. |

## Fixture and test identity proofs

- `rawlsing_next/tests/test_pre553_s06g_atomic_integrity.py` at E5 differs from S06G only at the import line: `rawlsing_next.tests.s06g_fixtures` replaces the missing S06F helper module. The 42-case court is otherwise exact S06G bytes.
- `rawlsing_next/tests/test_pre553_e5_s06g_independent_hostile.py` has blob `9a469ad0940216e02967c94159db943d2979154a`, equal to E2's `reviewer_tests/test_e2_independent_hostile.py` at E2 head `46a4ba7b`.
- `s06g_fixtures.py` functions `ref`, `subject`, `register`, `checkpoint_with_publication` and `m2_fixture` are AST-identical to the historical S06F helper functions.
- `test_pre553_s06f_native_owner_security.py` at E5 contains only five imports from `s06g_fixtures`. It defines no fixture and no test. It exists solely so the frozen S06FR overlay imports unchanged.
- The frozen S06FR overlay blob is `a25cf5a5ecec4b473ccceaec8a032747d804da7d` (SHA-256 `fea7cb29f6056996fd999cf50ddc227671024946e32af313f7954b1d30eecf30`); E5 did not edit it.

## Public ABI and callsites

An inspected signature comparison over 21 B5 methods/properties and 10 M2 methods/properties returned equal before/after for all public entries, including `stage_release`, `register_product`, `publish_product`, `selection_key`, `select_current`, `events`, `audit_replay`, `export_checkpoint`, `from_checkpoint`, `register_representation`, `register_binding`, `release_exact` and `releases`.

Private deltas:

- `M2Repository._insert` is now an instance method, not a static method, and requires an owner transaction.
- `register_representation` and `register_binding` perform local exact-release checks earlier.
- Event payloads are recursively frozen; closure metadata is recursively frozen.
- Direct private/direct-method writes outside a native writer transaction refuse.

Only `rawlsing_next/pre553_learned_world_composition.py:33/40` imports B5/M2 outside tests. That composition module has no non-test importer. No live production caller, protected CURRENT, external issuer or V3 source path is present at this cut.

## Limits

- The locks and rollback are in-memory and same-process only. They are not durable storage, OS-kill recovery, multiprocess custody or a Python principal boundary.
- A same-process caller can still set private attributes, open a private transaction context, replace callables or mutate private dictionaries. Saved-helper refusal reduces accidental bypass only.
- Checkpoint replay proves local semantic consistency. A coherent alternate history remains restorable as `LOCAL_UNAUTHENTICATED`; it is not authenticated completeness.
- A JSON roundtrip of an exported checkpoint preserves the checkpoint hash and canonical semantics, but canonical pair rows return as tuples rather than the original lists; strict Python container equality is therefore false. This is representational, not semantic.
- The two accepted M2 fixtures remain RED. That is the fan-in blocker addressed in `ACCEPTED_M2_TWO_FIXTURE_VERDICT.md`.
