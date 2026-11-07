# C4 reporting corrections — independent review 0def1171

Prior reviewed cut: `8986f3d4936edb1bda68f9eda55bf4be710e8642`.
Reporting-only corrections; no production, existing-test, peer, HQ, reviewer,
original-byte, native/science/actor or authority change.

| ID | Correction | Exact edits / evidence |
|---|---|---|
| C4-R1 | Disclose actual M1 registration mechanism and replace categorical no-caller label with `NONE_FOUND_IN_STATIC_SOURCE` for invocation/call-through. | `00_RETURN.md` FINDING/INTERPRETATION/ACTION; `01_CASES.jsonl` C4-J01 B/C/E/G/J and `02_CASES.tsv`; `03_TEST_RECEIPTS.md`; `04_MINIMAL_OWNER_ACTIONS.tsv`; `05_REGISTER_ANTIJOIN.tsv` O14. Evidence: `build_j_validator_registry` (`pre553_j_role_certification.py:1018-1027`) -> `FamilyValidatorRegistration.from_binding(binding, j_component_certification_validator)` -> exact `M1ValidatorRegistry`; `compose_learned_world` caller registry dispatch. Prior `logs/non_test_caller_search.txt` retained as historical incomplete narrow grep. |
| C4-R2 | Remove categorical “narrower/inadequate” implication; state different responsibility and `UNPROVED` historical equivalence. | `00_RETURN.md` F17/F19/F20/F21 comparison; C4-J01 `D_equivalent_authority` and `J_owner_action`; `02_CASES.tsv`. No actual current O14 demand requiring full dynamic historical surface is established. |
| C4-R3 | Preserve historical static pins/calls as proved, selected release `UNPROVED`, not historical absence. | `00_RETURN.md` FINDING/INTERPRETATION/limits; C4-J01/C4-J02 `historical_selection_status`, `G_equivalence_proof`, `E_first_break`; `03_TEST_RECEIPTS.md` NOT_RUN section. No equivalence/severance/absence claim. |
| C4-R4 | Keep old-version/shadow/revocation `NOT_RUN` explicit; no invented issuer/version/gate. | C4-J01/C4-J02 `G_equivalence_proof.old_version_shadow_revoked = NOT_RUN__NO_SELECTED_J_RELEASE`; `00_RETURN.md` limits; `03_TEST_RECEIPTS.md` NOT_RUN. |

## Preserved evidence

- Seven named O14 mechanism tests remain `7 passed in 2.23s`; independent reviewer also reports 7 passed in 2.69s. No tests were re-run for this reporting correction.
- Source hashes unchanged: O14 `838e123c...`, component vector `9cbe0200...`, M1 `40ce648e...`; historical six 9ba source pins unchanged.
- C2 closed; no C2 edits. No new probe/investigation, no production/test-existing/HQ/peer/protected writes.

## Evidence boundary

`NONE_FOUND_IN_STATIC_SOURCE` is limited to the stated static source search. It
does not prove absence of external/dynamic callers. Historical F17/F19/F20/F21
static callsites/source pins are preserved; selected original J release/row/
version remains `UNPROVED`. No old private cache/compiler restoration, no
mandatory original-J reinstatement, and no no-demand authority gate is created.
