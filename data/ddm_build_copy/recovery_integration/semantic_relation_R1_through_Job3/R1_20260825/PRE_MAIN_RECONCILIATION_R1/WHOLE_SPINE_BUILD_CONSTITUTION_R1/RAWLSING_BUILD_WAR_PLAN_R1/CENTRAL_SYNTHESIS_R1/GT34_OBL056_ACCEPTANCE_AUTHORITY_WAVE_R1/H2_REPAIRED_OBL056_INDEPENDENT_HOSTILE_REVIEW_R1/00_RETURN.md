# GT34 OBL056 H2 — REPAIRED INPUT-AUTHORITY ACCEPTANCE INDEPENDENT HOSTILE REVIEW R1 — RETURN

## Terminal

`FAIL__GT34_OBL056_CURRENT_ACCEPTED_ENTRY_IMMUTABLE_PROVENANCE_NOT_REQUIRED__REQUIRE_NONEMPTY_CURRENT_ENTRY_PROVENANCE`

State after terminal: `CLOSURE_ONLY`.

The exact repaired OBL056 candidate is **not lawful for HQ adoption consideration in its present form**.

This worker does not repair the candidate, does not adopt OBL056, and does not touch OBL055.

## Exact identities

- repository: `maidiu/rawlsing`
- worker branch: `agent/rabochii-gt34-obl056-repaired-input-authority-acceptance-hostile-audit-r1`
- exact working-ancestry start / commission: `1c5001fa281028c5ee34ed99d38f9e6406429323`
- repair worker tip: `67a3ee42cd1fd11bd68bf835e3bfa6a642bd155a`
- frozen repaired semantic candidate: `54f7a73275127d12f47fffa2a0d6b41addacfa3e`
- independent matrix freeze: `9caf9843206364e4270672b8c0d47b0e68c6ffad`
- hostile-test candidate: `839f324540082320e98f006c1c283a0581a9418f`
- governed evidence execution / exact checkout: `e41eb2e4bb2583e533b98c2bd2ddc24729bab46d`
- PR synthetic merge identity: `da88b9acd1a2406838c9cbeafebf1e82e2f34251`
- final worker tip: reported out of band after this return commit because this file cannot contain its own commit SHA without changing that SHA.

The semantic candidate, hostile-test candidate, evidence execution SHA, PR synthetic merge SHA, and final worker tip remain distinct identities.

## Independence sequencing

The fresh matrix was frozen before consuming the R2 return, governed evidence, R2 focused/inherited tests, or R2 compatibility artifact.

Frozen independent matrix:

`01_INDEPENDENT_ATTACK_MATRIX.json`

Attack-family count:

`64`

The fresh hostile test surface was independently authored after matrix freeze:

`rawlsing_next/tests/test_gt34_obl056_repaired_input_authority_acceptance_hostile_audit.py`

Hostile-test blob:

`7f6a7b318f8ba2b9b01a0de45c9ba3058099808d`

## Holding

The R2 repair successfully closes the prior H1 contact-pair constituent-validation bypass and makes future-current registry membership generally representable.

However, the candidate still violates one explicit future-current exactness requirement:

> every exact positive `CURRENT_ACCEPTED` entry must carry immutable entry provenance.

The implementation requires nonempty immutable **registry** provenance for a `CURRENT_ACCEPTED` registry snapshot, but does not require the matched `CURRENT_ACCEPTED` `AcceptanceEntry.immutable_provenance` to be nonempty.

Both `_make_registry_snapshot` and `_validate_against_registry` permit the exact matched current entry to have:

`immutable_provenance == ()`

provided the registry itself has nonempty adoption/current-selection evidence and nonempty registry provenance.

## Fresh governed reproduction

The fresh H2 test:

`test_03_ADOPTION_BLOCKER_current_entry_empty_immutable_provenance_is_accepted`

constructs an isolated nonproject `CURRENT_ACCEPTED` entry with:

- exact role;
- exact consumer and transition/use/family/subject/object scope;
- exact accepted-authority ID/version/content hash;
- exact owner/jurisdiction ref/hash;
- exact source adoption/current-selection evidence ref/hash;
- positive `ACCEPT` decision;
- deterministic exact entry ID/hash;
- `CURRENT_ACCEPTED` currentness;
- **empty entry immutable provenance**.

It then passes that entry through the candidate's own `_make_registry_snapshot` with:

- exact OBL056 acceptance-authority identity;
- exact content-addressed registry identity/hash;
- exact source-selection evidence;
- nonempty immutable registry provenance;
- exact one-entry membership.

A matching exact receipt is issued, the snapshot is installed only inside the isolated test using monkeypatch, and `validate_acceptance_receipt` returns the receipt successfully.

No project-current entry or authority is persisted or declared by the test.

Therefore the candidate accepts a future-current positive entry without one of the handoff's mandatory exact bindings.

## Smallest authority-respecting repair class

Do not widen OBL056.

The smallest lawful successor repair is inside the existing OBL056 acceptance-binding grain only:

1. require nonempty `immutable_provenance` for every `CURRENT_ACCEPTED` entry when constructing an exact current registry snapshot;
2. independently enforce the same nonempty entry-provenance condition during current receipt validation;
3. preserve exact entry/receipt equality and content-addressing;
4. add a regression proving an empty-provenance current entry fails closed.

Do not change:

- the four exact roles;
- consumer/scope/currentness law;
- synthetic/current separation;
- contact occurrence vs independence identity/receipt separation;
- underlying semantic ownership;
- OBL055.

## D2 contact-pair disposition

The repaired public contact-pair path survived the fresh constituent-first attacks.

Fresh hostile cases rejected:

- forged occurrence + valid independence;
- valid occurrence + forged independence;
- both forged but pairwise distinct;
- integrity-invalid receipt identity/hash;
- wrong issuer/registry;
- nonmember receipt;
- wrong role;
- wrong consumer;
- wrong scope;
- wrong owner/jurisdiction evidence;
- wrong source adoption/current-selection evidence;
- wrong currentness;
- nonpositive decision;
- synthetic/current masquerade.

After individual validation, same accepted authority remains rejected. A same receipt identity/hash cannot independently validate for both exact contact roles without violating receipt integrity/role binding.

No D2 adoption blocker was found.

## Other preserved protections

Fresh hostile proof also preserves/reconfirms:

- installed candidate current-positive registry remains empty and fails closed;
- no latest/default/fuzzy/positive fallback exists;
- arbitrary caller receipt without exact membership fails;
- accepted-authority ID/version/hash mutation fails;
- role substitution/cross-role reuse fails;
- exact consumer/scope/currentness binding remains enforced;
- issuer/registry substitution fails;
- absent/ambiguous membership fails closed;
- body mutation plus attacker rehash cannot create membership;
- synthetic/current separation remains strict;
- canonicalization/NFC is deterministic;
- replay/idempotence remains deterministic;
- authority ceiling remains intact.

## Independent identity / compatibility checks

Repaired authority hash independently recomputed exactly:

`6c9ab99a7d89835e7fdf405511abd7d6d66ced54b6e2fd8ef1863be842f39123`

Repaired empty-registry hash independently recomputed exactly:

`ca633451bfe56f86e1b463243bf721772a9ff582227411ed5137a346491b957e`

Exact repaired relevant blobs verified by the fresh court:

- implementation: `1bbc83f66f85ab46f4e1732fb43a158c0737dd6d`
- inherited R2/A1 regression: `454407f251c4146a2c0db8780afd7ea2e0b0a10c`
- R2 repair regression: `c86896aa20224695f92ec9b89c27f9d2bb3d7a78`
- repaired registry artifact: `7d9b2f4c4972c8bdcc7d9f958d136bb60532a1d6`
- repaired receipt-contract artifact: `7200514716f568356f6075b3decae29c247b169a`
- forbidden W2 executor: `54d9acba40f0eb1db8bb03aec3c1bb900f849588`

Candidate `54f7a732...` is an ancestor of H2 evidence execution. The exact H2 commission-to-evidence delta is only:

1. fresh frozen H2 matrix;
2. fresh H2 hostile test;
3. transient `.rabochii/court_spec.json`.

No repaired candidate file was modified by H2.

## Governed hostile court

Workflow:

`Rabochii Governed Bounded Court`

Exact evidence:

- run: `34143396854`
- job: `101810113479`
- exact checkout: `e41eb2e4bb2583e533b98c2bd2ddc24729bab46d`
- Python: `3.12.14` / CPython
- determinism: `EXACT`
- protocol self-test: `20 passed in 0.05s`
- court-spec validation: `PASS`
- fresh hostile court: `57 passed in 0.18s`
- court receipt result: `PASS`
- court receipt exit code: `0`
- court receipt spec SHA-256: `3c2904c0d2bb768897af50375a662007a70af147b1da855f202318c9dee118bd`
- artifact ID: `10026747756`
- artifact name: `rabochii-court-receipt-34143396854`
- artifact size: `618` bytes
- artifact ZIP SHA-256: `84a96e25f38bc0cc139d933cc770e31091045e26169ae0e03a98021f34d902dc`

The green court is hostile evidence, not candidate PASS. One green hostile assertion deliberately proves the adoption blocker by reproducing successful validation with empty current-entry provenance.

Execution-only draft PR `#246` was closed unmerged after evidence capture. The transient root court spec was removed afterward.

## Authority ceiling / non-actions

The candidate still creates none of:

- subject identity/classification;
- causal-use semantic truth;
- applicability semantic truth;
- contact occurrence;
- contact-independence fact;
- encounter/exposure;
- external-event admission;
- comparator;
- PSEPF;
- metabolism;
- CAN-008;
- V2;
- positive-V3 actor mutation;
- generic project-wide authority admission.

This worker performed no candidate repair, no OBL056 adoption, no OBL055 work, no W2 executor modification, no current first-canary OEE, and no central/PRE-MAIN/main/SUB-VOZHD movement.

## Return to SUB-VOZHD A

Do **not** prepare the OBL056 HQ adoption packet from repaired candidate `54f7a732...` in its present form.

Return exact terminal:

`FAIL__GT34_OBL056_CURRENT_ACCEPTED_ENTRY_IMMUTABLE_PROVENANCE_NOT_REQUIRED__REQUIRE_NONEMPTY_CURRENT_ENTRY_PROVENANCE`
