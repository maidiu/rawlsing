# I2 M2 — PUBLICATION BOUNDARY RECEIPT

## HQ118 governing split

Frozen and implemented:

`B5_LIFECYCLE_PUBLICATION_EVENT != M2_RELEASE_CORE != M2_PUBLICATION_BINDING`

## What PublicationBinding means

M2 PublicationBinding means only:

> this exact release is resolvable through this exact resolution mode, exact resolver/locator ref and exact representation-integrity ref.

It is immutable and content-addressed.

It does not state that the release is lifecycle-published.

## Mechanical absence of lifecycle semantics

ReleaseCore has no:
- `published`;
- `current`;
- `latest`;
- supersession;
- withdrawal;
- lifecycle event;
- consumer permission.

PublicationBinding has no:
- `published`;
- `current`;
- lifecycle status;
- consumer permission.

ResolutionReceipt carries explicit false effects:
- `lifecycle_publication_effect=False`;
- `current_selection_effect=False`;
- `consumer_permission_effect=False`.

## Governed hostile evidence

- no lifecycle PUBLISHED minting: PASS;
- no current-selection minting: PASS;
- no consumer-permission minting: PASS;
- no latest/default/fuzzy/nearest/semver fallback: PASS;
- binding cannot resolve different release: PASS;
- endpoint failover only within exact same release: PASS.

Workflow run:

`36326255638` — `success`.

## B5 handoff

A later B5 runtime may cite exact M2 release/binding refs under B5's own current lifecycle authority.

M2 exposes exact identities only. It does not perform the B5 event.

Disposition:

`HQ118_PUBLICATION_COLLISION_RESOLVED_IN_CODE__M2_BINDING_IS_NOT_B5_PUBLICATION`
