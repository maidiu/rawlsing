# JOIN-V final-cut adjudication — JOIN-E c367777

**STATUS:** `FINAL_CUT_REVISE__c367777__PERSISTENCE_ROOT_BRANCH_C12_SOURCE_NOT_PROVEN__AWAIT_NEXT_REPAIR_SHA`
**CANDIDATE:** `c367777f83367240352c267a2d3750abb7f09397` (read-only detached worktree)
**FROZEN CANDIDATE:** `13dfd6bad54ec19b4bdf31159e54fb6052d5440d`; original frozen test hashes unchanged
**BRANCH:** `codex/sorok-join-v-20261022`
**CONTINUATION:** `141b5fe1e393621862791281e980c450715bbb9a:.../continuations/02_JOIN_V_FINAL_CUT.md`; HQ intake `00_HQ_INTAKE.md`
**WRITE SCOPE:** own return only. No candidate edit.

## Short verdict

The c367777 repair is real and materially narrows the preliminary failures. It repairs four frozen hostile counterexamples, adds a real read-only cold reopen, a legitimate lawful fork, explicit J-first import closure, and a typed no-target HOLD. The candidate's own suite is 10/10 and inherited J/E/R30A suites are 8/8, 15/15, 10/10.

It still does not establish the persistence contract HQ requires. `open()` compares mutable meta `j_source` to mutable sidecar `r31j_source`, but the persisted C12 `GM01_SOURCE` is not the authority. It accepts a foreign product root containing the same source, and it accepts a metadata-only branch selection. Missing/orphan roots are still raw failures. These are direct counterexamples to "reject donor/root/source substitution" and "material source bound to persisted C12."

**Final-cut engineering verdict: REVISE.** The next repair SHA must be tested with the same frozen test files, the new targeted file, and the preserved positives.

## Repaired on c367777

| Preliminary failure | c367777 result | Basis |
|---|---|---|
| Different product root with a different source | PASS (refused) | `open()` now rejects `product.source != meta.j_source`; frozen hostile `test_different_product_root_is_refused` passes. |
| Plain R29P donor root, empty J source, donor mutation | PASS (refused, donor unchanged) | `ReadOnlyR31JProduct` suppresses sidecar writes; `open()` refuses source mismatch; frozen hostile `test_r29p_product_root_is_refused_without_mutating_donor` passes. |
| Single-sidecar `r31j_source` tamper | PASS (refused) | `open()` compares product source to meta `j_source`; frozen hostile `test_tampered_r31j_source_is_refused_or_bound_to_c12_episode` passes. |
| Moved session root | PASS (typed refusal) | `open()` wraps reopen failure as `SessionRefusal(COLD_REOPEN_REFUSED, ...)`; frozen hostile `test_relocated_session_root_is_refused_or_rebound` passes. |
| Lawful `fork_alt` continuation | PASS | New targeted `test_lawful_fork_alt_continuation_is_supported` passes; cold reopen of the alt meta and branch C12 verify. |
| E-first contamination | Intentionally refused | Frozen positive `test_warm_and_cold_import_order_preserve_result` now fails only because `JoinedSession.start` raises `IMPORT_CLOSURE_INVALID` for E-first. New targeted closure test confirms J-first passes and E-first is refused with `WRONG_CLOSURE` evidence. This is an explicit import-contract change, not a silent rebaseline; the frozen test remains unchanged. |

The c367777 closure audit is legitimate: `r31j.build/product/...`, `bp2p4`, `bp4`, `r29p`, `r26e`, and `historical_actor_producer` must resolve under J; `r30a`/`r31e` under E; M6 under live. The E-first frozen positive is retained as evidence of the old contract and superseded by the targeted guard.

## Still failing / newly exposed on c367777

| Finding | Observed counterexample | Required |
|---|---|---|
| **F1. Same-source foreign root is accepted.** | Copy A's product tree to a donor path, repoint A's `session.json` `product_root` to the donor, open A. Result: `opened=true`, `source_equal=true`, `verify=true`; product root is the donor, not `state_root/product`. Frozen `test_different_product_root_is_refused` does not cover this because the donor source differs there; new targeted `test_foreign_product_root_with_same_source_is_refused` fails. | Bind `product_root` to canonical `state_root/product` or a root receipt; source equality alone is not root identity. |
| **F2. Metadata-only branch substitution is accepted.** | Start `first_session`, call lawful `fork_alt("alt")`, then edit only `session.json` `branch_id` to `root`; open succeeds, `verify=true`, branch `root`. The original frozen alt substitution also still succeeds (`branch_id="alt"`, `verify=true`, help accepted). New targeted `test_metadata_only_branch_substitution_to_root_is_refused` fails. | Require a branch/fork receipt tying `meta.branch_id` to an authorized fork, or open only the recorded branch; do not infer authorization from a valid C12 branch. |
| **F3. Double sidecar+meta source tamper is accepted; source is not C12-bound.** | Edit both `session.json` `j_source` and `product/bp2_join.json` `r31j_source` to the same foreign `REFUSE_TOOL` source. Open succeeds, `verify=true`, help accepted, while the C12 `GM01_SOURCE` episode still says `SHARE_TOOL`/quantity 1. New targeted `test_double_sidecar_and_meta_source_tamper_is_refused_or_c12_bound` fails. | Compare the J source and actor mapping against the persisted C12 `GM01_SOURCE`/committed lineage; meta-to-sidecar equality is insufficient. |
| **F4. Missing session still raises raw `FileNotFoundError`.** | `JoinedSession.open` on a directory with no `session.json`. Frozen hostile `test_missing_session_is_typed_refusal` fails. | Typed `SessionRefusal(SESSION_NOT_FOUND)`. |
| **F5. Orphan product root after session loss still raises raw `RuntimeError`.** | Delete `session.json` from a valid root and call `start`; result `R31J_PREC9_REFUSED:c8_exclusive_append:C8_OCCURRENCE_NOT_ADMITTED`. Frozen hostile `test_orphan_product_root_start_is_typed_refusal` fails. | Typed `SESSION_EXISTS__NO_AUTOMATIC_REROLL`/`ORPHAN_PRODUCT_ROOT`; no automatic reroll. |

F1 and F3 are the material counterexamples to HQ intake item 3. F2 is the counterexample to HQ intake item 1. F4/F5 are the remaining missing/orphan typed-refusal gaps from item 4. The moved root is now safely refused (item 4 partially satisfied).

## B-source witness and E's mutation proof

E's `evidence/proof_witness.json` targets `test_material_omission_vs_e2_changes_help_without_patch`: the fault forces inspection in the omission branch and the test fails by assertion. This is an **A action/omission** witness. It is bounded and mechanically useful, but it is not an upstream B-source witness.

The independent witness on c367777 is new targeted `test_b_refusal_and_b_share_with_same_a_omission`:

- B `REFUSE_TOOL`: `b_performed=true`, `b_operation=REFUSE_TOOL`, quantity 0, `material_feasible_after=false`, A tool 0; E help refused.
- B `SHARE_TOOL`: `b_performed=true`, `b_operation=SHARE_TOOL`, quantity 1, `material_feasible_after=true`, A tool 1; E help accepted.
- Both use the same A omission action; the difference is the B source and the resulting material state.
- A newly built share-source donor restores the green consumer after the refusal donor; the targeted test covers that restore.
- `JoinedSession.probe_refusal` gives `target_id=""`, C9 `target_branch=NO_CHANGE`, `target_reason=NO_PROPOSAL`; no target is fabricated.

This witness **preserves the lawful no-tool refusal**. It does not adopt DEV-R's ungrounded "B refusal must lead to help accept" expectation. The B-refusal path remains a typed HOLD/owner-contract item; no E user session is manufactured without a target. The witness is source-derived and discriminating at the consumer, but it does not repair the persistence/canonical-source findings above.

## Exact frozen / targeted results

Frozen test hashes were checked before running and match `FROZEN_ORACLES.json` for all four frozen files. No frozen test file was edited.

| Suite | Result |
|---|---|
| Frozen positives against c367777 | **9 passed, 1 failed** |
| Frozen hostile against c367777 | **4 passed, 3 failed** |
| Targeted final-cut file against c367777 | **3 passed, 3 failed** |
| Candidate own suite | **10/10 passed** |
| Inherited J / E / R30A | **8/8, 15/15, 10/10 passed** |
| Source manifest | **444/444 verified**, 0 missing, 0 mismatched |

Frozen positive failure: `test_warm_and_cold_import_order_preserve_result` — E-first import is refused with `IMPORT_CLOSURE_INVALID` and `WRONG_CLOSURE` (J-first targeted guard passes).

Frozen hostile failures:

- `test_tampered_branch_id_is_refused` — alt accepted.
- `test_missing_session_is_typed_refusal` — raw `FileNotFoundError`.
- `test_orphan_product_root_start_is_typed_refusal` — raw `RuntimeError`.

Targeted failures:

- `test_metadata_only_branch_substitution_to_root_is_refused` — root accepted.
- `test_foreign_product_root_with_same_source_is_refused` — donor root accepted.
- `test_double_sidecar_and_meta_source_tamper_is_refused_or_c12_bound` — foreign source accepted; C12 episode disagrees.

Targeted passes:

- `test_lawful_fork_alt_continuation_is_supported`
- `test_b_refusal_and_b_share_with_same_a_omission`
- `test_import_closure_refuses_e_first_and_accepts_j_first`

Evidence: `evidence/final_cut/results.json`, `evidence/final_cut/source.json`, and JUnit files under `evidence/final_cut/`.

## Exact commands

```text
cd WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1
SOROK_JOIN_CANDIDATE_ROOT=<c367777 worktree>/WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1 \
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_join_v_positive.py -p no:cacheprovider
SOROK_JOIN_CANDIDATE_ROOT=... PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_join_v_hostile.py -p no:cacheprovider --tb=short
SOROK_JOIN_CANDIDATE_ROOT=... PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_join_v_final_cut.py -p no:cacheprovider --tb=short
SOROK_JOIN_CANDIDATE_ROOT=... PYTHONDONTWRITEBYTECODE=1 python3 -B tools/collect_final_cut.py
```

`collect_final_cut.py` also runs the candidate's own `tests` and the isolated inherited J/E/R30A suites and records the exact JUnit summaries.

## Candidate source hashes

- Candidate commit: `c367777f83367240352c267a2d3750abb7f09397`.
- `joined/session.py`: `1c1276a047d116a6787824bdb48e2f9d24b28947fdb84778990639203dbf480a`.
- `joined/readonly.py`: `93e1885e35d078879228b38c716ac5ed0b14b91367433b19d19bf7d4535d2371`.
- `joined/closure.py`: `d4c5e46d64e03201c5379eba4a1f2aaa2ec53744ceb22e78395fef05f6e74ff4`.
- `joined/assertion.py`: `ec9a313b271cafc089eeb6353b11a2c74b4b3bac33431b53c830410ae98b9878`.
- `tests/test_join.py`: `87cc0ae9378be0375de1a6b35bd200a0cf158b425557ba8a7703927fc110ef7b`.
- `SOURCE_MANIFEST.json`: `7cfcb4679e36b522e83cc7120dbc166ce61dd220099c2aca8f5c9ddb5252c126`; 444/444 verified.
- New targeted test `tests/test_join_v_final_cut.py`: `6e2f87d773090235a4a5f3567430737f30f16698397c852f799585ff73280de1`.
- New collector `tools/collect_final_cut.py`: `fc9d3bed87c6eeade8292e90d6470128816cf27e9b6ee1a0886af2eaa3b41ac8`.

The original `FROZEN_ORACLES.json` and all four frozen test hashes are unchanged.

## Courts

| Court | Final-cut verdict | Ceiling |
|---|---|---|
| **ENGINEERING** | `REVISE` | c367777 repairs four preliminary failures and retains the positive encounter/fork/attention/import closure, but same-source foreign roots, metadata-only branch selection, double sidecar+meta source tampering, and missing/orphan raw failures remain. |
| **SCIENTIFIC** | `HOLD__NO_ISSUANCE` | B-source witness is a lawful sourcefree material/consumer contrast; no B-refusal=>help-accept claim, no acquired practice, psychology, personhood or A5. |
| **AUTHORITY** | `HOLD` | No native CAN/ADP/C8/C12/Pyat/C11/C5, protected keys, external provider or human A5; no production security claim. |

## Next

Await the next repair SHA from human/HQ. Continue this same review lane with the frozen tests unchanged and the targeted final-cut tests. The next repair should:

1. bind `open()` to canonical `state_root/product` or a root receipt, not merely source equality;
2. store and verify an authorized branch/fork receipt, rejecting metadata-only branch selection while preserving lawful `fork_alt`;
3. compare J source and actor mapping to the persisted C12 `GM01_SOURCE`/committed lineage, not just meta-to-sidecar equality;
4. add typed missing-session and orphan-root refusals;
5. rerun all frozen positives and hostiles plus targeted tests; preserve the c367777 positives.

No polling, no additional worker, no candidate edit, no native grant.
