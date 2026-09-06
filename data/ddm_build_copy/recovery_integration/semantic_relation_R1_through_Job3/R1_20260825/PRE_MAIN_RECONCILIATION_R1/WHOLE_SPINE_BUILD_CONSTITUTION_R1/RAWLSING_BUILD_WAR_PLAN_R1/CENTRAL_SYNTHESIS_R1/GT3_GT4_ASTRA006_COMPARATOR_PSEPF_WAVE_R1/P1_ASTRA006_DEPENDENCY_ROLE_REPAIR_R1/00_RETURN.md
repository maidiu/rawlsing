# GT3/GT4 P1 — ASTRA-006 AUTHENTICATED DEPENDENCY-ROLE REPAIR R1

## Terminal

`PASS__GT34_P1_ASTRA006_FIRST_POSITIVE_PATH_ROLE_AUTHENTICATION_CLOSED__LEGACY_NONCANARY_DEBT_BANKED`

This is intentionally the handoff's **bounded alternative PASS**, not the stronger claim that every historical/legacy V558 reconstruction surface has been retroactively rewritten.

## Exact execution state

- repository: `maidiu/rawlsing`
- worker branch: `agent/rabochii-gt34-p1-astra006-dependency-role-repair-r1`
- exact authorized start: `a4dbd45de0b328ef41434b3052200d425a43d99c`
- immutable instruction ref, evidence only: `bc591282b6ac618bbaa1f610774b265aa00fa637`
- final semantic candidate: `9f23cc673f771dfee1b2d19795f987b186eb1ec0`
- bounded court execution tip: `a6603745bf018ac166d18ebbe2cea46bd727f6a0`
- Actions run: `34007508494`
- Actions job: `101417322828`
- PR synthetic merge SHA used by that court: `60208f71050084d16a5be5f0596003b8e0a9a338`
- CPython: `3.12.14`
- protocol self-test: `20 passed`
- bounded hostile/regression court: `140 passed, 1 warning`
- court result: `PASS`

The warning is the existing deterministic Q69B identity-court runtime warning that emits the frozen court JSON; it is not a failure.

## O3 attack reproduced before the repaired boundary

The hostile test first reconstructs a producer with:

- identical semantic payload;
- identical producer object ref/content hash;
- one originally-declared negative dependency removed.

The existing legacy V557/V558 path accepts that reconstruction into a new checksum-valid repository because:

- the producer content hash authenticates the payload but not the role tuples;
- V557 governance and V558 producer locator bind the same producer ref;
- legacy repository material does not authenticate the producer's required/negative role declarations.

The legacy resolver then faithfully resolves the weakened repository.

That reproduces the O3-proved ASTRA-006 defect rather than merely asserting it.

## Repair class

The repair uses the handoff's identity-preserving **B/C boundary**:

1. add an independently content-addressed `DependencyRoleBinding`;
2. bind it to the exact producer object ref;
3. bind the exact normalized:
   - `required_dependency_refs`;
   - `negative_dependency_refs`;
4. require exactly one binding per repository producer in the new authenticated mode;
5. include every binding ref plus the exact authentication mode in the V558 repository semantic material;
6. thereby make the role-bound V558 repository ref the effective accepted structural identity for the future first-positive path.

New schema:

`SCR5578_V558_DEPENDENCY_ROLE_BINDING@1.0.0`

New exact mode:

`EXACT_CONTENT_ADDRESSED_ROLE_BINDINGS`

New public safe builder:

`build_role_authenticated_v558_repository_bundle(...)`

New fail-closed guard:

`require_authenticated_dependency_roles(...)`

## Why this closes the demonstrated first-positive attack

Under the authenticated boundary:

`same producer payload/ref + different required/negative roles`

necessarily produces:

`different dependency-role binding ref`

and therefore:

`different effective V558 repository ref`.

A caller cannot strip/reclassify a role and reuse the already-accepted role binding:

- dropping a negative dependency while reusing the accepted binding fails;
- required -> negative fails;
- negative -> required fails;
- stale binding hash fails;
- wrong producer ref with otherwise-shaped binding fails;
- noncanonical authentication-mode spelling fails before hashing.

A caller may construct a *different* role-complete repository from a differently-declared object, but that repository has a different exact effective identity. It cannot masquerade as the already-accepted role-bound repository.

That is the required invariant for the first-positive path.

## M5 consequence

M5 already performs deterministic exact M4 re-resolution and binds its currentness/RSC material to the exact resolution/repository evidence.

The hostile court proves:

- an accepted role-authenticated repository resolves normally;
- a weakened role-bound repository has a different exact repository/resolution identity;
- attempting to present the old accepted M4 evidence/currentness against that weakened repository fails M5 exact re-resolution.

No M5 semantic widening was required.

## Opaque lineage remains opaque

The new role binding authenticates only the producer's explicit:

- required dependency tuple; and
- negative dependency tuple.

It does **not** inspect arbitrary payload/provenance refs and does not infer dependency role from ref presence.

A hostile fixture places an opaque lineage ref inside producer payload while declaring no dependencies. The authenticated binding remains exactly empty and no reference edge is created.

Therefore:

`OPAQUE_LINEAGE != REQUIRED_DEPENDENCY`

remains preserved.

## Negative dependencies remain negative

The repair does not convert negative refs into positive facts.

The role binding keeps required-positive and negative tuples separately typed and separately serialized. The authenticated mode also rejects one exact dependency appearing simultaneously in both roles.

Therefore:

`NEGATIVE_DEPENDENCY != POSITIVE_FACT`

remains preserved.

## Itemwise permission is unchanged

The hostile court constructs:

- a CONTEXT-capable root;
- a required dependency that permits REVIEW only.

The role-authenticated V558 resolver still denies CONTEXT because dependency permission is checked itemwise. Role authentication grants no new use and does not cause root permission to flow into a dependency.

## Legacy identity preservation

This worker does **not** add role-binding fields to legacy repository semantic material.

Default/legacy mode remains:

`LEGACY_UNAUTHENTICATED_ROLE_DECLARATIONS`

with:

- no role binding refs in the repository semantic projection;
- no new material keys;
- the old repository hash formula byte/semantics-equivalent.

The hostile court directly recomputes a legacy repository hash from the pre-repair material shape and proves equality.

This is why the worker does not silently rewrite accepted GT1/GT2 V558 identities.

## Identity / regression court

The 140-test governed court includes:

- the new ASTRA-006 hostile role-authentication court;
- M4 V557/V558 publication/repository tests;
- M5 runtime RSC peer-prior tests;
- GT12 D->M4 typed bridge tests;
- real/current GT12 E2B actual-object consumer harness tests;
- PRE553 repo-native current rehydration tests;
- Q69B conditioner projection/identity tests;
- typed-negative conservation tests.

All passed.

The Q69B identity court emitted unchanged current values including:

- release semantic hash: `2343023560ea963b6b290575d93361256825897a7c32ff31519e3d2425b595ec`;
- source-release-manifest hash: `15b39da2a58bdb0716e8e84dd63b215e2fc5b6abdc3bc6edf8c282cf4813dbc4`;
- repaired coordinate authority hash: `cb84cf0962f5d11e7713912bc80d2078c89635ac09d7a24e39b7586591b4135c`;
- replay hash: `8ec8450d41524015c8e6b2716c00f622a9792334d2b952cac585b3b2971cb539`;
- transport semantic hash: `c90ef7eaeea4b1536d3153beb344ce22156bf15bf835a3182c1b5784b8f238c5`;
- transport gzip hash: `bbf256e01beef96d29a0a00517348d983ebfa718a320acc16787a9a3c59ab719`;
- exact current GT2 respondent subset match: `19,210`.

No PRE553/Q69B production surface was modified by P1.

## Why the terminal is bounded rather than global

The old legacy builder remains available because changing its semantic material would change already-accepted repository identities.

Therefore historical/noncanary callers that deliberately continue using legacy mode retain the old ASTRA-006 debt.

The **first positive V3 path must not use legacy mode**.

Its exact structural V558 prerequisite is now:

1. build through `build_role_authenticated_v558_repository_bundle`;
2. freeze the resulting exact repository ref as part of the accepted first-positive structural evidence;
3. call `require_authenticated_dependency_roles` at the first-positive consumer boundary;
4. carry that exact repository/resolution/currentness identity into downstream invocation evidence.

Any future attempt to authorize a positive path through legacy unauthenticated V558 is outside this PASS and must fail review.

## Authority ceiling

P1 changes only dependency-role authentication / effective V558 reconstruction identity.

It does not:

- promote provenance into dependencies;
- change dependency semantics;
- change V557 permission;
- change Q69B;
- change GT1/GT2 empirical identity;
- create comparator authority;
- create PSEPF;
- create metabolism authority;
- create a CAN-008 rule;
- mutate V3;
- authorize V2.

## Final holding

The O3 attack remains reproducible on the explicitly-bankable legacy path, which preserves historical identities.

It is closed for the future first-positive path by a versioned, content-addressed role-bound V558 identity.

Therefore the exact terminal is:

`PASS__GT34_P1_ASTRA006_FIRST_POSITIVE_PATH_ROLE_AUTHENTICATION_CLOSED__LEGACY_NONCANARY_DEBT_BANKED`
