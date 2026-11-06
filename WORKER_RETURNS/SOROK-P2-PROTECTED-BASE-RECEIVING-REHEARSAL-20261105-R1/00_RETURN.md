# SOROK P2 PROTECTED-BASE RECEIVING REHEARSAL R1

## RESULT

`BOUNDED_ENGINEERING_RECEIVING_COMPATIBILITY_REHEARSAL__PROTECTED_BASE_8FFEC40A__PRODUCT_25D40806__GUIDE699_9_FILE_OVERLAY__COMPOSITE_TREE_3894541E__COLD_CLI_PASS__NOT_INDEPENDENT_REVIEW__NOT_SELF_ACCEPTANCE__NOT_MERGE_PERMISSION`.

This is engineering receiving evidence only. It does not accept the candidate, the fanin, or any repair; it does not authorize a protected merge or PR697 action.

## EXACT INPUTS

- Live protected starting base: `8ffec40a6924848a49f95950aa9ce28c27ee3ec1`; tree `ba895ff69255f35c8fec58c0d0b28e339def57f6`.
- P2 candidate: `25d40806d15516b7f7ffa04f47bc651022c6f2b0`; tree `57dbdca8efdbb6bcda7b64df0ac60e8fe75ddc3a`. Includes accepted `41bf4581`, lifecycle `79b90e4a`, interval repair `7a256ed4`, later-event `76fdb624`, and fanin repair refresh.
- Guide PR699 head: `5b569b130379ee012936e2f6517fc7c49ddcbdea`; tree `a6a823344bff865d8e42d68242e0a5eff98fe4b3`.
- Merge base: `8ffec40a6924848a49f95950aa9ce28c27ee3ec1`.
- Moving refs were fetched and the three exact commits verified before composition.

## SELECTED SOURCES AND COMPOSITE

- Product allowlist: exactly the `git diff 8ffec40..25d` file set, 625 files, all under the seven intended product returns plus the S45-S47 receiving commission. Paths: `evidence/product_allowlist.txt`, SHA-256 `f79ee2e94770d5579fc8bc99e0612f0f1e10dd174fe467e9f56291666e7a350b`; selection manifest `evidence/selected_manifest.json`, SHA-256 `24b8f56675e388e07450b7ce7dda4722f879dfc4d1f20efb95bd54584fd07432`.
- Guide allowlist: exactly the 9 existing `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/` files changed by PR699. The 4 guide-return evidence files were deliberately excluded. Paths: `evidence/guide_allowlist.txt`, SHA-256 `4a4dc85b318ad9347988882d8054bef4ee30624429cd21f4ea32cc3eafa68ab6`.
- Composition: full protected base tree + 625 product files + 9 guide files. Composite tree `3894541eeac3e2133a3823252c65f04252e21e93`.
- Composite diff versus protected base: exactly `634` changes = `625` additions + `9` guide modifications. No unrelated protected file changed.
- Product/guide path overlap: `0`. Product files already present in protected base: `0`. Guide files replaced: `9`. No schema/root/import incompatibility observed.
- Snapshot is checkout-local and disposable under `.local-logs/sorok-p2-protected-base-receiving-rehearsal-20261105-r1/snapshot`; it is not a protected branch or commit.

## MERGE-TREE DIAGNOSTIC

- `git merge-tree --write-tree 8ffec40 25d` → `57dbdca8efdbb6bcda7b64df0ac60e8fe75ddc3a`, exit 0, no conflicts.
- `git merge-tree --write-tree 8ffec40 5b569b` → `a6a823344bff865d8e42d68242e0a5eff98fe4b3`, exit 0, no conflicts.
- `git merge-tree --write-tree 25d 5b569b` → `b3a82908dfc50186a9f37ebe60e2bd5acf9fdfb6`, exit 0, no conflicts. This full merge tree includes the 4 excluded guide-return files; composite differs only by those 4 additions.

Evidence: `evidence/merge-tree-product.txt`, `evidence/merge-tree-guide.txt`, `evidence/merge-tree-25d-guide699.txt`, `evidence/composite_diff_vs_base.txt`, `evidence/selected_manifest.json`.

## GUIDE CANONICAL VERIFY

Composition affects the guide (9 selected guide files), so the existing canonical verifier was run against the receiving snapshot:

```text
python3 <snapshot>/CROSS_HQ_CONTROL_ROOM/PROGRAMMA/verify_canonical_programma_r1.py
# PASS canonical tree: Pyat 782/892/62/82, FF 26/16, cross 18/16, Sorok 144/38, no prototype
# exit 0
```

Log: `logs/guide_canonical_verify.log`.

## ACTUAL COLD FIRST-CONSUMER SEQUENCE

Executed from the receiving snapshot, not the author checkout, with `python3 -I -B` and fresh processes:

`new -> interval ACTUAL -> later-event -> opportunity -> verify (zero encounters) -> explicit do-help -> exit -> cold blocked say -> local return -> say UNKNOWN -> verify`.

Observed:

- `new`: `SOROK_WP19_ENCOUNTER_VIEW@1`.
- Explicit ACTUAL interval: `OK`, `PARTIAL`, coverage `[[222,223]]`, material `0`, `do_help_executed=false`.
- Later-event: `event_status=OK`, C9 `c9_material_eligible=false`, S43 `language_status=ACCEPTED`, `do_help_executed=false`, `user_attempt=false`.
- Opportunity read: same observation-only contract; `do_help_executed=false`.
- Verify before attempt: `encounter_count=0`, `event_count=2`, `ok=true`.
- Explicit DO_HELP: `REFUSED`, `attempted=true`, `performed=false`, `refusal=true`.
- Local exit: `LOCAL_EXIT_ONLY`, mode `OUTSIDE`.
- Cold blocked SAY: `LOCAL_OUTSIDE_MODE_BLOCKED`, `actor_response=null`, `world_event_created=false`, `clock_changed=false`.
- Local return: `LOCAL_RETURN_ONLY`, mode `PORTAL`, no world event/clock change.
- Typed UNKNOWN SAY: `status=UNKNOWN`, `actor_response=null`.
- Final verify: `ok=true`, `encounter_count=2`, `event_count=4`.

Evidence: `evidence/cli/` (11 command receipts plus `summary.json`, SHA-256 `da18dd2b5def693cb174a6f4debc45adb1c34b46d6b802839641cbce3bb99dec`), `evidence/receiving_rehearsal.json` SHA-256 `1c78ec28b57178a60bd1dde4d19573c20c256992f042ad9a65e26ab82069c452`.

## IMPORT ORIGIN AND PRIVACY

- Import-origin check loaded `sorok_s45_s47.bootstrap`, `s45.session`, `s47.session`, `s45_projection.adapter`, lifecycle, interval repair, later-event, and fanin from the receiving snapshot. `all_under_snapshot=true`. Evidence: `evidence/import_origin_check.json`.
- Privacy walker over `new`, later-event, opportunity, and final verify found no `root_hash`, `root_id`, private keys or forbidden source markers; all `root_hash_present=false`. Evidence: `evidence/privacy_check.json`.
- Typed UNKNOWN, local access boundary, observation-only later event, and explicit single DO_HELP action were preserved.

## STATUS AT DECLARED CUT — NO POLLING

- Later repair: `RUNNING_AT_DECLARED_CUT`.
- Independent interval closure: `RUNNING_AT_DECLARED_CUT`.
- Later-event `76fdb624` original independent verdict: `REVISE`; original public-CLI limits preserved.
- This rehearsal: `ENGINEERING_RECEIVING_EVIDENCE_ONLY_NOT_ACCEPTANCE_NOT_MERGE_PERMISSION`.

No job statuses were polled after the declared cut.

## NOT RUN

- No full inherited 13-test state suite.
- No new broad review or independent acceptance.
- No protected merge, PR697 action, source-branch drift, product/guide modification or native/science/human/B grant.
- No actual elapsed life, absence activity, delivery or world-return producer.

## SMALLEST REMAINING RECEIVING STEP

After the running interval-repair/later-boundary reviews close, a competent PRE-MAIN owner can decide whether to receive the exact candidate `25d40806` plus the 9-file guide699 overlay using this allowlist and composite tree. No further engineering step is added by this rehearsal; this receipt is not permission to merge.

## REPOSITORY AND PUBLICATION

- Branch: `codex/sorok-p2-protected-base-receiving-rehearsal-20261105-r1`.
- Only `WORKER_RETURNS/SOROK-P2-PROTECTED-BASE-RECEIVING-REHEARSAL-20261105-R1/` is written/committed.
- Candidate parent: `25d40806d15516b7f7ffa04f47bc651022c6f2b0`.
- Rehearsal commit is this branch head; exact SHA is returned in the final chat readback. No protected write or merge.

## PROGRAMMA_DELTA

See `PROGRAMMA_DELTA.md`: engineering receiving rehearsal and evidence only; no canonical PROGRAMMA guide/product adoption, no protected merge and no acceptance.
