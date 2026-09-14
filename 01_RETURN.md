# T02 — GENERIC R4 BATCH ADAPTER IMPLEMENTATION R1 — RETURN

Repository: `maidiu/rawlsing`

Worker branch: `agent/rabochii-prev3-w18-t02-generic-r4-batch-adapter-impl-r1`

Commission tip: `462d7defedc4817952e9bc916920472d03613d69`

Commission base: `190e74d0266b6bc75bd24a34ff5a139590f0ce30`

Exact grain:

`SDTF_R4_GENERIC_BATCH_ENVELOPE_ADAPTER_IMPLEMENTATION_R1_ONLY`

Library: `NOT USED`

## Terminal

**PASS**

`T02_PASS__GENERIC_R4_BATCH_ADAPTER_IMPLEMENTED__SEPARATE_INDEPENDENT_QUALIFICATION_REQUIRED`

This PASS implements the narrow S03 generic batch-row adapter. It does not independently qualify the adapter and does not issue semantic authority, select a current rule, mint a concrete mechanism rule, or materialize actor/entity/topology/person state.

## Governed inputs preserved

- S03 return tip: `a718682521fe9b5c1d3b90e6a9c9e765ed892e8a`
- frozen S03 contract blob: `0a2eb3da6d755f12197348a71cfa7d1dd97d7b4d`
- exact S03 contract ref: `SDTF_R4_GENERIC_BATCH_ENVELOPE_CONTRACT|SDTF_R4_GENERIC_BATCH_RULE_ENVELOPE_INTAKE_AND_CONSTRUCTOR_CONTRACT_R1@1.0.0|abc44b2b4ff04e164b5188e5929b0c10ca1b6e582b28207bb7e464ace698a83d`
- adopted final-envelope constructor: `SDTF_R4_MECHANISM_RULE_AUTHORITY_BINDING_R1@1.0.0`
- adopted constructor implementation blob: `c94997f5c7f2bbee9cd99c570554fd48c0f47556`

## Implementation artifact

`rawlsing_next/sdtf_r4_generic_batch_adapter.py`

Git blob:

`c1a495c7a23d4ebee086fd5410d9627f4aefb695`

The adapter freezes the exact 28 determinant ids/field paths and six S03 package partitions; validates the exact S03 contract identity, candidate row identity/generation/predecessor/provenance/status-cell grammar, batch identity and duplicate presentation; preserves all five fail-closed determinant states; quarantines same-key/same-generation hash conflicts without choosing a winner; and emits content-addressed candidate and batch receipts whose semantic identities are independent of presentation order.

Only rows whose 28 cells are all `SATISFIED_CURRENT` or conditionally lawful explicit `NOT_APPLICABLE` are projected. Projection is one-to-one into the existing adopted R4 types: `MechanismRuleIdentity`, `RuleTraceBinding`, six `AuthorityCeilingBinding` slots, `RuleValueMode`, `RuleCurrentness`, and the current/noncurrent ref tuples. The existing R4 constructor remains the final projected-envelope validator.

The adapter never supplies a candidate-specific source family, mechanism name, authority id, rule id/version/hash, value mode, rule body, currentness proof, actor/entity fact, or topology default. An explicit authority N/A cell is converted only to the corresponding generic R4 role plus the exact supplied `na_basis_ref`; no authority or evidence ref is invented.

## Test artifact

`rawlsing_next/tests/test_sdtf_r4_generic_batch_adapter.py`

Git blob:

`7b4190601757fa69352d1a990c27242c67226cae`

Deterministic test identities:

1. `test_exact_contract_identity_and_frozen_28_to_six_partition`
2. `test_wrong_or_mutable_contract_selector_is_rejected_at_batch_boundary`
3. `test_all_valid_multirow_projects_one_to_one_into_existing_r4_constructor`
4. `test_one_invalid_row_is_quarantined_without_contaminating_later_valid_row`
5. `test_deterministic_replay_and_reordering_preserve_batch_and_candidate_receipts`
6. `test_candidate_only_row_stays_governed_and_cannot_masquerade_as_current`
7. `test_silent_not_applicable_on_required_determinant_is_rejected`
8. `test_predecessor_chain_error_is_row_local_and_fails_closed`
9. `test_same_key_generation_different_hashes_are_both_quarantined_with_no_winner`
10. `test_exact_duplicate_row_refs_deduplicate_idempotently`
11. `test_row_identity_hash_excludes_free_text_diagnostics_but_not_governed_fields`
12. `test_generic_implementation_contains_no_m10_specific_semantic_path_or_default`
13. `test_adapter_does_not_invent_authority_ref_rule_body_or_currentness`
14. `test_currentness_evidence_mismatch_is_rejected_by_existing_r4_path`

Local deterministic execution result: `14 passed`.

The local runner used the exact committed implementation/test bytes (verified by Git blob hashes above) with a hermetic interface-equivalent fixture for the already-inspected PRE553/R4 imports because the execution container had no repository/network checkout. The committed test module is written against the real repository imports and is ready for the separately required independent qualification lane.

## Required-law closure

- exact frozen contract identity accepted; mutable/substitute contract selector rejected;
- exact 28-field mapping and six-package partition preserved;
- unresolved/candidate-only cells remain governed and cannot project;
- fully resolved candidate-not-current rows project into the adopted R4 constructor;
- silent N/A fails closed;
- mandatory authority, value-mode/calibration and rule-currentness/evidence laws remain delegated to or mirrored exactly around the adopted R4 constructor;
- exact duplicate row refs deduplicate idempotently;
- conflicting same-key/same-generation hashes quarantine every conflicting row and no winner is selected;
- predecessor-chain errors fail closed without contaminating unrelated rows;
- row order and duplicate presentation do not alter semantic receipt identity;
- M10-like namespaces are opaque data only; no M10/Wright/source-specific path exists in the implementation;
- no authority/ref/body/currentness is invented by the adapter.

## Boundary preservation

No concrete M10 or other mechanism rule was minted. No `CURRENT_ACCEPTED` selection was issued. No RULE_OWNER, CAUSAL_USE, measurement, estimand, identification, calibration, or other authority was issued. No source-semantic adjudication, actor-position materialization, topology, V3/person state, OBL063 semantics, Library use, MAIN mutation, or PRE-MAIN mutation occurred.

`GENERIC_BATCH_ADAPTER_IMPLEMENTED != GENERIC_BATCH_ADAPTER_INDEPENDENTLY_QUALIFIED`

PASS wakes the separately authorized independent qualification lane required by the commission.
