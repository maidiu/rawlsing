# PYAT HQ118 I3 — M2 Interface Protocol

## Purpose

I2/M2 is a sibling lane and is not imported by I3.

I3 therefore defines a narrow structural protocol only:

`LearnedProductReleaseProtocol`

It states the exact product/release identity and closure material B5 must consume once an M2 release exists. It does **not** define an M2 `ReleaseCore`, `PublicationBinding`, resolver, publication registry, or release-construction algorithm.

## Required protocol fields

A conforming M2 adapter supplies:

- `release_ref`
- `product_ref`
- `product_family_ref`
- `producer_owner_ref`
- `producer_contract_ref`
- `semantic_projection_hash`
- `authority_snapshot_refs`
- `direct_dependency_refs`
- `determinant_refs`
- `determinant_set_hash`
- `replay_root_ref`
- `selection_scope_ref`
- `build_or_release_receipt_refs`
- `producer_permission_ceiling_ref`

I3 then constructs a local:

`LearnedProductLifecycleSubject`

This local object is explicitly a **B5-side opaque lifecycle view**, not a second release schema.

## Ownership direction

The intended future binding is:

`M2 exact release identity / ReleaseCore`
`-> narrow adapter`
`-> LearnedProductReleaseProtocol`
`-> B5 lifecycle registration/publication/currentness`

I3 never calls back into M2 to mutate release identity.

B5 lifecycle events reference exact release/product identities already supplied by the producer/M2 side.

## Publication collision resolved

HQ118 freezes:

`B5 PUBLISHED = lifecycle publication state/event`

`M2 PublicationBinding = exact locator/resolution binding`

Therefore:

`M2_PUBLICATION_BINDING_EXISTS != B5_PRODUCT_PUBLISHED`

`B5_PRODUCT_PUBLISHED != M2_PUBLICATION_BINDING_EXISTS`

A repository/resolver can see an exact release without B5 having lifecycle-registered or lifecycle-published it.

I3 proves this separation with:

- `stage_release` — repository/adapter presence only;
- `register_product` — explicit B5 `PRODUCT_REGISTERED`;
- `publish_product` — explicit B5 `PRODUCT_PUBLISHED`.

## Semantic ownership firewall

The adapter cannot let I3 rewrite:

- product semantic meaning;
- validation/adjudication state;
- product family anatomy;
- authority closure;
- dependency identity;
- semantic projection hash;
- producer permission ceiling.

If the same exact `product_ref` arrives under a different semantic projection hash, I3 fails closed before registration.

Semantic-changing rebuild must therefore mint a new exact product identity upstream.

## Currentness handoff

M2 does not provide implicit currentness to I3.

I3 current selection operates on exact B5 `SelectionKey` plus an exact release ref.

A release can be:

- staged but unregistered;
- registered but unpublished;
- published but not current;
- published and current for one SelectionKey;
- current for one purpose but not another;
- historical and resolvable but no longer current;
- explicitly NO_CURRENT at a key.

No M2 creation/publication timestamp can select any of these states.

## Permission handoff

`producer_permission_ceiling_ref` is conserved as a ceiling input.

I3 does not turn that ceiling into a consumer grant.

Downstream target-use permission remains a separate authority after M2 resolution and B5 current selection.

## Source-free sibling independence

No I2 file, module, branch, schema, or runtime was imported.

The hostile protocol test uses a fake object satisfying only the declared protocol and verifies:

- I3 can stage it;
- staging does not register it;
- no M2 release construction is performed.

Test:

`test_m2_interface_is_narrow_protocol_not_release_core_reimplementation`

## Future I2 integration gate

When I2 returns, integration should add the thinnest adapter that can prove:

1. I2 exact release identity maps without loss to the B5 protocol;
2. I2 producer/dependency/determinant/replay refs are unchanged;
3. M2 `PublicationBinding` remains resolver-only;
4. B5 `PRODUCT_PUBLISHED` remains lifecycle-only;
5. no latest/default/currentness enters through M2 resolution;
6. consumer permission remains outside both.

No I3 semantic change should be needed if I2 conforms to the HQ118-adopted M2 constitution.

## Terminal

`I3_M2_INTERFACE = NARROW_EXACT_REF_PROTOCOL__SIBLING_INDEPENDENT__NO_RELEASECORE_REIMPLEMENTATION__NO_PUBLICATIONBINDING_COLLAPSE`
