# CURRENT CALLSITE AND API DELTA

## Source identity

| Surface | Current PRE-MAIN `8e44ca9c` | S06G candidate `0ff13995` |
|---|---|---|
| Lifecycle | `rawlsing_next/pre553_learned_product_lifecycle.py` blob `a11c9eb73abab9be118ef4f0b6e325e676059f27` | blob `dadf2362f3195c28ebaf97655e28cdba72c04fb3` |
| Release | `rawlsing_next/pre553_learned_product_release.py` blob `f76c390665f06ef126968ccf1a6b2d816f43ae92` | blob `1cb7692399aad8fb272c8c9ce956719527829007` |
| S06G test | absent | blob `23aaf95d315980ea7587373e30188c7f36cb2b73` |
| S06FR overlay | absent in current | blob `a25cf5a5ecec4b473ccceaec8a032747d804da7d` (equals historic S06FR test) |

Current → S06G production diff: **lifecycle +545/−4**, **release +155/−10**. The four lifecycle deletions replace direct payload assignment/serialization/torn append/helper read with recursive freeze, detached projection, transaction append and a guarded read. The ten release deletions replace the static `_insert`, unguarded writers/readers and non-checking representation/binding registration with guarded instance methods.

## Real callsites

### B5/M2 production importers

Only one current production module imports the B5/M2 owners:

- `rawlsing_next/pre553_learned_world_composition.py:33` imports lifecycle symbols;
- `rawlsing_next/pre553_learned_world_composition.py:40` imports M2 symbols.

That composition module has **no production importer**. A tree-wide search for `pre553_learned_world_composition` outside tests returns no non-test import. Therefore:

- The B5/M2 stack is a **local/test-only runtime** at this cut, not a live production service.
- The absence of a production consumer does **not** make the local integrity defects irrelevant: the current accepted tests and local APIs exhibit them. It only bounds present business impact.
- The S06G patch does not create a new production consumer and cannot claim production/protected-current/external custody.

### Calls actually used by the composition

The composition uses:

- `LearnedProductLifecycleExecutor.stage_release`
- `register_product`
- `publish_product`
- `selection_key`
- `select_current`
- `events`
- `audit_replay`

The S06G overlay preserves these public signatures. The adjacent integration suites pass **45/45** under both current and the S06G overlay (`test_pre553_ee14_selected_current_asof_hq260.py` 15 + `test_pre553_learned_world_composition.py` 30). The composition does not use the saved private helpers, checkpoint export/restore or M2 foreign-binding registration in its normal path. The strict M2 `register_binding` change is what breaks the two accepted release tests, not the composition callsite.

## API delta and compatibility

| Change | Current | S06G | Compatibility consequence |
|---|---|---|---|
| Event payload | `payload` normalized to mutable dict; `as_dict` copies shallowly | Recursive freeze (`MappingProxyType`/tuples), detached export | Public payload mutation now refused; old S06FR defect test fails as obsolete. Composition unaffected. |
| Mutation transaction | No owner lock/rollback; `_append_events` callable directly | Reentrant lock + snapshot rollback across validation/append/projections; saved helpers require transaction | Direct helper bypass refused; accepted B5 tests pass; composition passes. |
| Native preflight | No `native_security_mode`/`require_external_issuer` | `LOCAL_UNAUTHENTICATED` only; external/protected/token modes hold | Pretended external custody now fails closed; old OBSERVED append/insert tests fail with `EXTERNAL_ISSUER_HOLD`. |
| Checkpoint restore | Hash + structural checks then `_append_events` | Native event replay + receipt/state semantic comparison; rejects rehashed semantic substitution | Old checkpoint field/rebuild OBSERVED assertions fail as obsolete; cold restore positive passes. |
| Selection | Validation and commit not serialized | Lock spans check/append/projection; one winner/one conflict | Old concurrent stale-predecessor probe fails as obsolete; new 12-trial race passes. |
| M2 writers | Static `_insert`; writers not serialized | Instance `_insert` with transaction, store/type/index checks, read/write lock, rollback | Saved `_insert` direct call refused; M2 public writers serialized. |
| `register_representation`/`register_binding` | Does not require the release to be registered first | Calls `release_exact`; foreign release raises `RELEASE_UNAVAILABLE` | **Two accepted M2 tests fail at setup**; new reconciled tests assert early refusal then lawfully register and preserve later mismatch. |
| Checkpoint/test helper dependency | No S06F native-owner test module | S06G test imports `test_pre553_s06f_native_owner_security` helpers | Current cannot run S06G test unmodified; a separate engineer must port/rewrite the helper. |

## The two accepted-M2 failures are a test-contract compatibility regression

- `test_17_binding_cannot_resolve_different_release` and
  `test_18_endpoint_failover_only_among_same_release` construct a foreign
  representation/binding from a second repository and insert it into the first
  repository to attack a later resolution/failover path.
- Current permits the unregistered foreign record and reaches the later oracle.
- S06G’s `register_binding`/`register_representation` calls `release_exact` and
  refuses `RELEASE_UNAVAILABLE` before insertion.
- The new S06G reconciled cases (17/18) first assert the early refusal, then
  lawfully import the foreign release and its representation, register the
  binding, and preserve the original `PUBLICATION_BINDING_MISMATCH` oracle.
- This is a **real compatibility change at the accepted test fixture grain**,
  not a permissive resolution regression and not a security defect. The
  accepted tests were not edited. An owner must decide whether to update the
  fixture/test contract; the reviewer does not.

## D3 is not S06G

`LIN-S06_TRUSTED_RELEASE_REPLAY` (D3, `a897ad3d`) is a **standalone
caller-trusted S06 wrapper** with a caller-supplied boolean/token. It is not the
B5/M2 owner hardening in S06G. S06G does not repair or accept that wrapper, and
the wrapper does not repair or supersede S06G. D3’s `SUPERSEDED_PROVED` label is
scope-limited to the standalone wrapper only.

## Patch shape

- A full-file overlay of S06G lifecycle/release onto current is functionally
  compatible at the tested scope: 187/14 with current modules and 45/45
  adjacent integration tests.
- A Git cherry-pick of the S06G commit is **not** clean: S06G is based on S06F
  parent `6187d0a2`, whose merge base with current is `7f29aec3`, not current
  `8e44ca9c`. The practical patch is the **semantic diff** of the two owner
  files, not a wholesale branch merge.
- The S06G test module requires a missing S06F test helper. A separate engineer
  should add/rewrite the helper or provide a standalone test module; do not
  drop the S06G test file into current and assume it collects.
