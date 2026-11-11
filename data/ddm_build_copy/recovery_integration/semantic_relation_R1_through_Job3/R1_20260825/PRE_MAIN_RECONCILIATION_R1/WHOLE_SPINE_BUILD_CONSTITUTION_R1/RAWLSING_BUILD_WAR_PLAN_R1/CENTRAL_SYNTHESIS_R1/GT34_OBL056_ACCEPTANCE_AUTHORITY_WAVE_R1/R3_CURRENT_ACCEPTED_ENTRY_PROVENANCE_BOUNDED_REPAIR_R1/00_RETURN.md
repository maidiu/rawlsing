# GT34 OBL056 R3 — CURRENT-ACCEPTED ENTRY PROVENANCE BOUNDED REPAIR R1 — RETURN

## Terminal

`PASS__GT34_OBL056_CURRENT_ACCEPTED_ENTRY_IMMUTABLE_PROVENANCE_BOUNDED_REPAIR_GREEN__NO_ADOPTION`

State after terminal: `CLOSURE_ONLY`.

This PASS means only that the exact repaired candidate is ready for one fresh independent hostile review. It does not adopt OBL056.

## Exact identities

- repository: `maidiu/rawlsing`
- worker branch: `agent/rabochii-gt34-obl056-current-entry-provenance-bounded-repair-r1`
- exact commission / working-ancestry start: `75897ab89df5fd58c27f7c996e9a818bc8561549`
- frozen predecessor semantic candidate: `54f7a73275127d12f47fffa2a0d6b41addacfa3e`
- H2 hostile tip: `53172d2fe1dba091b1cbaf663c75a4c4e6bcf750`
- H2 terminal: `FAIL__GT34_OBL056_CURRENT_ACCEPTED_ENTRY_IMMUTABLE_PROVENANCE_NOT_REQUIRED__REQUIRE_NONEMPTY_CURRENT_ENTRY_PROVENANCE`
- repaired semantic candidate: `442a8c16cea45620374c5a73e406483ff59122d8`
- governed evidence execution / exact checkout: `90a6ba5ff7ca30f40a9450c22eed7889b4721f88`
- PR synthetic merge identity: `a950017f103624e2fc413fe55004c4dc59508906`
- final worker tip: reported out of band after this return commit because this file cannot contain its own commit SHA without changing that SHA.

## Bounded repair

The repair changes only the exact H2 entry-provenance defect.

For `CURRENT_ACCEPTED`:

1. `_make_registry_snapshot` now rejects any positive entry whose `immutable_provenance` is empty;
2. `_validate_against_registry` independently rejects the exact matched current entry when its `immutable_provenance` is empty;
3. runtime contract artifacts explicitly expose that immutable current-entry provenance is required.

The repair does not allow immutable registry provenance to substitute for immutable entry provenance.

Implementation blob:

- predecessor: `1bbc83f66f85ab46f4e1732fb43a158c0737dd6d`
- repaired: `49538b9c36e58e19a6dc293ecac5bc2dff58eebe`

## Preserved identity / authority law

The R2 contract already required immutable entry provenance; R3 closes the implementation enforcement gap and therefore does not mint or widen authority material.

The exact content addresses remain:

- authority: `6c9ab99a7d89835e7fdf405511abd7d6d66ced54b6e2fd8ef1863be842f39123`
- presently-empty registry: `ca633451bfe56f86e1b463243bf721772a9ff582227411ed5137a346491b957e`

Installed candidate current-positive entry count remains `0`.

The exact four roles, exact consumer/scope/currentness law, synthetic/current separation, registry adoption/current-selection evidence requirement, immutable registry provenance requirement, exact membership/content addressing, contact constituent-first validation, contact authority/receipt distinctness, no-fallback law, and authority ceiling remain unchanged.

## Regression proof

Fresh focused regression:

`rawlsing_next/tests/test_gt34_obl056_current_entry_provenance_bounded_repair.py`

blob:

`fe4c67ab66d574b577be03b7f8848ca79c227310`

It proves:

- a lawful isolated future-current entry with nonempty entry provenance remains representable and validates;
- an otherwise-exact current entry with `immutable_provenance == ()` fails snapshot construction;
- a handcrafted, internally content-addressed malformed current snapshot containing that entry independently fails again during receipt validation;
- the installed candidate registry remains empty and current-positive use fails closed today;
- authority and empty-registry hashes remain exact;
- the prior contact-pair repair remains operative;
- the W2 executor remains blob `54d9acba40f0eb1db8bb03aec3c1bb900f849588`.

H2 source tests were not modified. The compatibility wrapper excludes only two assertions that are definitionally predecessor-specific:

- the historical assertion that empty entry provenance is accepted;
- the assertion pinning the predecessor implementation blob.

All remaining applicable H2 hostile cases are green (`55`).

## Governed proof

Workflow: `Rabochii Governed Bounded Court`

Final evidence:

- run: `34151115277`
- job: `101833429369`
- exact checkout: `90a6ba5ff7ca30f40a9450c22eed7889b4721f88`
- semantic candidate: `442a8c16cea45620374c5a73e406483ff59122d8`
- Python: `3.12.14` / CPython
- determinism: `EXACT`
- protocol self-test: `20 passed in 0.13s`
- court-spec validation: `PASS`
- bounded court: `51 passed in 0.65s`
- court receipt result: `PASS`
- artifact ID: `10029378313`
- artifact name: `rabochii-court-receipt-34151115277`
- artifact size: `678` bytes
- artifact ZIP SHA-256: `1e4b83f3308b1489a85cb3a4c2a2101b8b246aca5c15c7288fe19f44b324dba9`

Execution-only draft PR `#249` was closed unmerged after evidence capture. Its synthetic merge identity is `a950017f103624e2fc413fe55004c4dc59508906`. The transient root court spec was removed afterward.

A prior diagnostic governed run `34150916201 / 101832832985` failed only because the compatibility wrapper still included the H2 assertion that hard-pinned the predecessor implementation blob. That diagnostic showed `55` other H2 cases green and was superseded without changing the bounded candidate repair. PR `#248` was closed unmerged.

## Mutation / non-action audit

This worker:

- repaired only OBL056 current-entry immutable-provenance enforcement;
- did not modify OBL055;
- did not adopt OBL056;
- did not create a project-current positive authority or registry entry;
- did not execute current first-canary OEE;
- did not modify the W2 executor;
- did not move central, PRE-MAIN, main, or SUB-VOZHD branches.

## Return to SUB-VOZHD A

The exact repaired candidate may proceed only to one fresh independent hostile review.

Return exact terminal:

`PASS__GT34_OBL056_CURRENT_ACCEPTED_ENTRY_IMMUTABLE_PROVENANCE_BOUNDED_REPAIR_GREEN__NO_ADOPTION`
