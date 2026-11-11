# PYAT HQ118 I3 — B5 LEARNED-PRODUCT LIFECYCLE RUNTIME — R1

## Terminal

`PYAT_HQ118_I3_PASS__B5_LEARNED_PRODUCT_LIFECYCLE_RUNTIME_SOURCE_FREE_GREEN__OBL034_SEMANTICS_PRESERVED`

## Exact identity

- repository: `maidiu/rawlsing`
- branch: `agent/rabochii-pyat-hq118-i3-b5-lifecycle-runtime-r1`
- commission: `d85bf24aa694cfa03cd79207df64a87aec634fb1`
- exact sealed HQ118 base: `6cd63ce6cd5bf697f76ff7e62c4681f16c062832`
- governing current lifecycle authority: `PRE553_LEARNED_PRODUCT_LIFECYCLE_CANDIDATE@1.0.0`
- OBL034 inherited disposition: `CLOSED_AT_EXACT_LIFECYCLE_ECONOMICS_GRAIN`
- mode: source-free implementation + hostile qualification
- raw source access: NONE
- real-source I03/I05 execution: NONE
- Field Forge mutation: NONE
- M1 learned-empirical semantic mutation: NONE
- M2 ReleaseCore/publication-binding implementation: NONE
- source/carrier retirement: NONE
- new semantic authority created: NONE

## Result

I3 implements the already-adopted B5 learned-product lifecycle constitution as a dedicated runtime owner:

`rawlsing_next/pre553_learned_product_lifecycle.py`

Final implementation blob proved by the final I3 qualification:

`a11c9eb73abab9be118ef4f0b6e325e676059f27`

Hostile/source-free tests:

`rawlsing_next/tests/test_pre553_learned_product_lifecycle.py`

Final test blob proved by the final I3 qualification:

`d7ab66fe50aacb2d4223dca223d0d702af11270c`

The runtime does not alias Authority42 and does not wait for sibling I2/M2 implementation. It consumes only exact producer/release identity through a narrow protocol boundary.

## Core lifecycle closure

The implementation provides:

- opaque exact learned-product/release lifecycle subjects;
- explicit repository staging distinct from lifecycle registration;
- immutable B5 `PRODUCT_REGISTERED` and `PRODUCT_PUBLISHED` events;
- exact `SelectionKey` identity by family + scope + purpose + optional consumer partition;
- exact `CurrentSelectionReceipt`;
- exact `NoCurrentReceipt`;
- no latest/default/newest/semver/filesystem-order currentness;
- exact expected-prior-receipt conflict detection for concurrent/stale selection;
- B5-governed explicit `CURRENT_SUPERSEDED` transition;
- nondestructive withdrawal;
- determinant-local direct + transitive invalidation;
- explicit replacement or `NO_CURRENT` for every affected current selection during withdrawal/invalidation;
- exact authority-ref changes as neutral B5 determinant keys without importing Authority42 lifecycle ownership;
- typed rebuild eligibility/blockers;
- exact rebuild linkage;
- optional cache materialization/drop without semantic mutation;
- recomputable learned-product payload GC eligibility only after exact proof;
- hard firewall against source/carrier retirement;
- append-only exact event history;
- deterministic checkpoint/restart/replay;
- exact historical current-as-of event/checkpoint resolution.

Freeze:

`SEMANTIC_OWNER != CARRIER_OWNER != LIFECYCLE_OWNER`

`REPOSITORY_PRESENCE != PRODUCT_REGISTERED`

`PRODUCT_REGISTERED != PRODUCT_PUBLISHED`

`PRODUCT_PUBLISHED != CURRENT_SELECTED`

`CURRENT_SELECTED != CONSUMER_PERMISSION`

## B5 versus M3 reconciliation

M3 was used only where its later representation sharpened B5 without changing B5 meaning.

The controlling difference was handled explicitly:

B5 `CURRENT_SUPERSEDED` includes an exact predecessor -> successor current-selection transition.

Therefore I3 implements supersession as:

`EXACT_CURRENT_PREDECESSOR + EXACT_SUCCESSOR + SUPERSESSION_BASIS + SELECTION_ATTESTATION`
`-> CURRENT_SUPERSEDED`
`-> NEW EXACT CurrentSelectionReceipt`

The predecessor remains immutable history.

M3 refinements retained where compatible include:

- exact `SelectionKey`;
- explicit `NO_CURRENT`;
- selection-conflict failure state;
- exact current-as-of event/checkpoint replay;
- content-addressed lifecycle receipts;
- exact checkpoint/restart identity.

## Authority42 boundary

Authority42/A03 remains the `AuthoritySnapshot` maintenance lifecycle owner.

I3 does not import `pre553_authority_maintenance.py` and does not reuse its owner/executor classes.

Only neutral exact-identity primitives from `pre553_empirical_objects` are shared.

I3 explicitly rejects `AuthoritySnapshot` and `AuthorityReleaseReceipt` identities as learned-product release aliases.

B5 LCR-009 authority-change invalidation is implemented by projecting an exact `AuthorityRef` into a neutral content-addressed:

`B5Lifecycle:AUTHORITY_DETERMINANT`

This key participates only in learned-product determinant traversal.

It neither resolves nor promotes nor rolls back authority state.

## M2 sibling interface

I3 does not import an I2/M2 sibling runtime.

It defines only:

`LearnedProductReleaseProtocol`

which requires the exact identity/closure facts B5 must later consume.

The local `LearnedProductLifecycleSubject` is explicitly an opaque B5-side adapter view, not a second `ReleaseCore`.

HQ118 publication noncollapse is preserved:

`M2 PublicationBinding != B5 PRODUCT_PUBLISHED lifecycle state`

A release can be visible to a repository/resolver without being B5-registered, B5-published or current-selected.

## B5 rule parity

All adopted B5 rules `LCR-001` through `LCR-020` are mapped to concrete runtime surfaces and hostile evidence in:

`02_B5_RULE_TO_RUNTIME_PARITY.tsv`

All 20 return `PASS`.

Particularly:

- LCR-003 current selection is explicit and exact;
- LCR-004 supersession is explicit and nondestructive;
- LCR-006 current withdrawal/invalidation cannot silently leave or choose currentness;
- LCR-008 invalidation is determinant-local and transitive;
- LCR-009 authority changes are explicit determinants;
- LCR-010 semantic-changing rebuild requires a new upstream product identity;
- LCR-012 cache state is nonauthoritative;
- LCR-014 GC is restricted to proven recomputable product payload;
- LCR-015 source/carrier retirement is out of jurisdiction;
- LCR-016 AuthoritySnapshot lifecycle is external;
- LCR-019 history is append-only;
- LCR-020 conflicts and missing evidence fail closed.

## Hostile qualification

The I3 test file contains 38 source-free lifecycle tests.

The final repository-native narrow governed court ran:

- workflow run: `36326914249`
- workflow head: `7c181e6c05532e6d7a4308ce5077d032e61f5b75`
- exact semantic candidate pinned for the court: `700dff473978fd241fe97fb68502a295a55de63e`
- protocol self-test: `20 passed in 0.11s`
- governed bounded court: `60 passed in 0.61s`

The 60-test governed court consisted of:

- 38 I3 learned-product lifecycle tests;
- 22 existing Authority42 maintenance tests.

This simultaneously proves the new B5 runtime and bounded non-regression of the separate Authority42 lifecycle owner.

Court artifact:

- name: `rabochii-court-receipt-36326914249`
- artifact id: `10933214853`
- digest: `sha256:72d4527202693805aa9f0600935d63c686acff404cf3b1004bf693e5512f7996`

## Governed-court spec hygiene

The repository's ordinary `.rabochii/court_spec.json` was not an I3 court: it was pinned to an older semantic candidate and a legacy FIABC test surface.

The commission explicitly allowed an equally ordinary narrowly modified governed court if the normal path was not fit for the bounded lane.

I3 therefore temporarily pinned the court to:

- the exact I3 semantic candidate;
- the I3 lifecycle test file;
- the current Authority42 maintenance test file.

After the green final run, the court spec was restored byte-for-byte to the exact HQ118 baseline blob:

`67eb1c668c6d03a31f678d6b09db3288bd1ef810`

Restoration commit:

`2343aa6e73fdfc0a2567693db5bf7993995f701f`

There is **no final branch delta** in `.rabochii/court_spec.json`.

## Restored legacy-court result — not an I3 regression

Restoring the old court spec triggered its broad legacy court at run:

`36326954301`

The protocol self-test remained green:

`20 passed`

The broad legacy bounded court returned:

`144 passed, 3 failed`

All three failures are stale exact-blob assertions in preexisting FIABC packaging/fanin tests over files I3 did not touch:

1. `test_fiabc_w3_i04_runtime_packaging_rebind.py`
   expected historical `ee_p2x_darwin_stage_backend.py` blob `1bb84723...`; current exact blob is `b655d8b8...`.

2. `test_fiabc_final_preflight_fanin.py::test_live_candidate_c_and_packaging_bind_final_hq_state`
   expected historical Candidate-C binder blob `47893688...`; current exact blob is `c2451b1b...`.

3. `test_fiabc_final_preflight_fanin.py::test_t5_contract_binds_final_successor_and_lits_current_law`
   repeats the same stale Candidate-C binder anchor.

Neither the Darwin backend nor Candidate-C binder is modified by this worker.

Accordingly this broad restored-spec failure is recorded as preexisting stale exact-hash debt outside I3's write scope, not hidden and not repaired here.

The commission-authorized I3 qualification remains the exact narrow governed run `36326914249`, which is green.

## Qualification correction history

An earlier narrow run found one hostile-test expectation that was weaker than the runtime:

the runtime rejected a semantic change under an existing `product_ref` during staging, before rebuild linkage could be attempted.

The test was corrected to recognize this earlier fail-closed boundary.

I3 then additionally hardened:

- reselection after explicit `NO_CURRENT`;
- withdrawn-product self-replacement rejection;
- invalidated-product self-replacement rejection;
- exact `AuthorityRef` determinant invalidation.

The final green 60-test court includes those corrections.

## Temporary PR hygiene

A temporary draft PR was used only to trigger repository-native GitHub Actions qualification:

`#458 — TEMP I3 qualification: B5 lifecycle runtime`

It targeted the exact HQ118 control base.

It was closed **unmerged** after qualification.

No integration/control branch was advanced by this worker.

## Return artifacts

- `00_RETURN.md`
- `01_CHANGED_FILES.tsv`
- `02_B5_RULE_TO_RUNTIME_PARITY.tsv`
- `03_PUBLIC_API_AND_OWNER_RECEIPT.md`
- `04_HOSTILE_TEST_LEDGER.tsv`
- `05_AUTHORITY42_REUSE_OR_NONREUSE_RECEIPT.md`
- `06_M2_INTERFACE_PROTOCOL.md`
- `07_CHECKPOINT_REPLAY_RECEIPT.md`

## Final write scope

The intended final delta is exactly:

1. `rawlsing_next/pre553_learned_product_lifecycle.py`
2. `rawlsing_next/tests/test_pre553_learned_product_lifecycle.py`
3. the eight return files above.

No raw data, source-specific runtime, Field Forge module, Authority42 module, M1/M2 sibling module, execution branch, or control-room file is modified.

Final worker HEAD is external to this self-referential return and must be resolved from the worker branch after this return commit.

## Terminal

`PYAT_HQ118_I3_PASS__B5_LEARNED_PRODUCT_LIFECYCLE_RUNTIME_SOURCE_FREE_GREEN__OBL034_SEMANTICS_PRESERVED`
