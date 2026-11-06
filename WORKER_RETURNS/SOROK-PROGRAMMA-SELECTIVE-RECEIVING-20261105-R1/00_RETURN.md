# SOROK PROGRAMMA selective PRE-MAIN receiving candidate — currentness corrected

**RESULT:** `SELECTIVE_PREMAIN_RECEIVING_CANDIDATE_PREPARED__SOURCE_174658ADB__PROTECTED_BASE_8FFEC40A__FANIN_RETURNED_NOT_ACCEPTED__INTERVAL_REPAIR_RUNNING__LATER_REVIEW_RUNNING__LIFECYCLE_ACCEPTED_SCOPED__NOT_MERGED`.

This candidate closes the existing pending guide-integration engineering gap for the #647 guide write-through. It is a selective receiving candidate only; no protected write, merge, product edit or new guide architecture was performed.

## 1. Exact bases and provenance

| Item | Exact identity |
|---|---|
| Live protected guide base | `integration/pre-main-reconciliation-r1` at `8ffec40a6924848a49f95950aa9ce28c27ee3ec1` |
| W8-R documentary source cut | `a9ebf71e62d84e5dcc599662e976eca7fcd0e623` (separate source cut; **not** an ancestor of protected base or source branch) |
| Current source branch | `codex/sorok-programma-product-intake-20261105-r1` at `174658adb67905aa3f295189119f50fef41f84ee` |
| Prior source cut | `35ae6f9aeaa5437ec497b44bbd044d32f76d4b0a` (preserved as the base of the selectivity proof) |
| Source/protected merge base | `8ffec40a6924848a49f95950aa9ce28c27ee3ec1` |
| Candidate branch | `codex/sorok-programma-selective-receiving-20261105-r1` branched from protected base |
| Method | Exact `git diff protected_base..source_head` for the 9 affected existing guide files; `git apply --check`; `git apply`; candidate guide files byte-match source `174658adb` for those paths |

No missing predecessor was found. W8-R remains a separate documentary source cut, not the protected branch parent.

## 2. Selective change set

Only these 9 existing guide files changed. No unrelated protected guide file, row or field was replaced.

| Path | SHA-256 |
|---|---|
| `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/00_HQ_WRITE_THROUGH_DECISION.md` | `16cc473dc2e8d17bf4b56bd3260fd1c5f3b5489b6cb948e8056479c5aed36856` |
| `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/06_WORKING_WHOLE_SOROK_ARCHITECTURAL_SPINE_R1.md` | `26d433af5a71eada33daccdec63e9a8249bbde7b3c9444e5ca70d61b66fabf0e` |
| `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/07_GITHUB_ACCESSIBLE_ASSET_LOCATOR_R1.json` | `fb770c14f2eb764376768ced4ab0960508395fecae605a8fc99f9aadaca7205c` |
| `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/08_INITIAL_EVIDENCE_GRADED_DEPENDENCY_AND_SEAM_REGISTER_R1.json` | `51dada4553bf6d4ea1ff8505e4a206659b8ab7bc99d168227ecf7e0be87a6fdb` |
| `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/09_INHERITED_144_FUNCTIONS_TO_WORKING_SPINE_R1.json` | `f53715038e2e1696c8f60bedfde166b58f80c60d3f86e0731024ddce605be93c` |
| `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/10_RECONCILIATION_QUEUE_SOURCE_GAPS_AND_CLOSEOUT_CHECK_R1.md` | `dfb473470f7712f64e59d9a12cf561bf5dbccc484e7985beddb8f0979b34d151` |
| `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/14_W7_RECURSIVE_PHASE_GATES_AND_WORK_PACKAGES_R1.jsonl` | `31b4157e5a136a70ddcb3f68b49cc7259afba39ca2c4acd67ac42601ee56250f` |
| `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/15_W7_VERSIONED_SEAMS_AND_GATE_JOIN_CANDIDATES_R1.jsonl` | `0bc420496ee9254852b650c51bf5e9f80af77c8a0128f424e3c847e4859612a0` |
| `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/READ_FIRST.md` | `7e80a498021380a053f77645b80c2195bf56408996d2f04a07baebc7ad28569e` |

Changed records:

- `07`: `hq_647_incremental_source_reconciliation_20261105`, `hq_p2_local_lifecycle_candidate_20261105`, `hq_p2_interval_later_20261105`, `hq_p2_product_fanin_20261105`.
- `08`: `hq_647_incremental_20261105`, `hq_p2_local_lifecycle_candidate_20261105`, `hq_p2_interval_later_20261105`, `hq_p2_product_fanin_20261105`.
- `09`: same four top-level dispositions; 144 function identities unchanged.
- `14`: 25 existing records; 668 rows/83 gates unchanged.
- `15`: 10 existing seams; 38 seams unchanged.
- `00`/`10`: P2 currentness corrected. `06` and `READ_FIRST` retain the prior #647 S45-S47 receiving additions.

## 3. Conflict disposition

- No textual or semantic conflict: protected base is the exact source merge-base and the patch applies cleanly.
- Only the 9 affected guide files changed; all unrelated protected rows, fields, old cuts and source identities remain at protected base.
- Prior source cut `35ae6f9a` remains the selectivity proof base; the new source `174658adb` carries only the two currentness corrections.
- The earlier source return directories were not copied into the protected-base candidate; they remain cited by commit/path.
- No source product, vendor, projection, harness, PROGRAMMA architecture or protected branch file was edited.
- Conserved counts: Sorok 09 `144`; 14 `668` rows/`83` gates; 15 `38` seams; 08 `22` seams; 07 `304` assets.

## 4. Verification actually run

```text
python3 CROSS_HQ_CONTROL_ROOM/PROGRAMMA/verify_canonical_programma_r1.py
# PASS canonical tree: Pyat 782/892/62/82, FF 26/16, cross 18/16, Sorok 144/38, no prototype
# exit 0
```

JSON/JSONL parse, count validation and `git diff --check` passed. Candidate guide files byte-match source `174658adb` for all 9 changed paths. No product suite was rerun.

## 5. Reconciled material facts and owner limits

- Lifecycle: `ACCEPT_SCOPED_TEST_ONLY` at review `6398888f1d28152b5d29fef816f0bb45e77dd43b`; local UI lifecycle boundary only, sidecar not security/tamperproof.
- Interval `bdadbc57`: still `AUTHOR_TESTED_CANDIDATE`, not accepted; independent review RUNNING. Defect recorded: standalone interval `admit_continuation` auto-calls `adapter.do_help`, mixing observation with a user attempt. Repair branch `sorok-p2-interval-attempt-boundary-repair-20261105-r1` RUNNING; no repair SHA/acceptance.
- Later-event `76fdb624`: still author-tested candidate, independent review RUNNING; fanin observes the later opportunity without auto DO_HELP but that is not acceptance.
- Product fanin RETURNED `579afc5fe63ff305ec49d4c8d42abc8475acf8bb`; remote verified, 6 author tests `58.22s`, one S47 root, lifecycle + explicit interval + later-event opportunity, encounters `0` until explicit `DO_HELP` yields `1`; independent fanin review NOT_RUN, not accepted/integrated. `evidence/upstream_interval_auto_do_help.json` records the bypassed defect.
- PR #697 remains open, ready and unmerged at `41bf45813fd0adeffd9b54e1306c2022abe96514`.
- This guide candidate: isolated, pending protected integration; no dependent READY.
- Native C8/C9/C12, CAN008/CAN011, ADP, Pyat, human S11/A5 Gate4/Gate5 and current B-owned context remain unchanged/held.

## 6. NOT_RUN

- No product suite rerun.
- Fanin independent review NOT_RUN; interval repair no published SHA/acceptance; interval/later review still RUNNING.
- No native/human/B/Pyat execution, protected merge or PR #697 action.

## 7. PR-ready title and body

**Title:** `PROGRAMMA #647: selectively receive S45-S47 and P2 guide currentness`

**Body:**

```text
Selective PRE-MAIN receiving candidate for the #647 guide write-through, currentness-corrected after the P2 fanin return and interval attempt-boundary defect.

Base: integration/pre-main-reconciliation-r1 @ 8ffec40a6924848a49f95950aa9ce28c27ee3ec1
Source: codex/sorok-programma-product-intake-20261105-r1 @ 174658adb67905aa3f295189119f50fef41f84ee
Prior selectivity base: 35ae6f9aeaa5437ec497b44bbd044d32f76d4b0a
Merge base: 8ffec40a6924848a49f95950aa9ce28c27ee3ec1; patch applies cleanly.

Changed only 9 existing guide files; no wholesale replacement, no unrelated protected rows/fields, no new guide/project, no product edits.
Counts preserved: Sorok 144 functions, 14 668 rows/83 gates, 15 38 seams, 08 22 seams, 07 304 assets.
Canonical verifier PASS; JSON/JSONL parse and diffcheck PASS. No product suite rerun.

Currentness: lifecycle accepted scoped TEST_ONLY at review 6398888f. Interval bdadbc57 is author-tested candidate with repair RUNNING (standalone admit_continuation auto-DO_HELP defect); later-event 76fdb624 review RUNNING; both not accepted. Fanin 579afc5 returned author-tested, 6 tests 58.22s, one S47 root, encounters 0 until explicit DO_HELP 1; independent fanin review NOT_RUN, not accepted. PR697 open/ready/unmerged at 41bf4581; this guide candidate is not merged. Native/human/B/Pyat rights unchanged.

HQ creates the PR through the connector; this return sends no external messages.
```

## 8. Publication

Committed and pushed normally on `codex/sorok-programma-selective-receiving-20261105-r1`. Exact source-branch and receiving-branch 40-hex SHAs are returned in the final chat readback and verified by `git ls-remote`. No protected write or merge.
