# SOROK PROGRAMMA selective PRE-MAIN receiving candidate

**RESULT:** `SELECTIVE_PREMAIN_RECEIVING_CANDIDATE_PREPARED__PROTECTED_BASE_8FFEC40A__SOURCE_35AE6F9A__9_AFFECTED_GUIDE_FILES__NO_WHOLESALE_REPLACEMENT__NOT_MERGED__NOT_PROTECTED_WRITE`.

This candidate closes the existing pending guide-integration engineering gap for the already-published #647 write-through `35ae6f9aeaa5437ec497b44bbd044d32f76d4b0a`. It is a selective receiving candidate only; no protected write, merge, product edit or new guide architecture was performed.

## 1. Exact bases and provenance

| Item | Exact identity |
|---|---|
| Live protected guide base | `integration/pre-main-reconciliation-r1` at `8ffec40a6924848a49f95950aa9ce28c27ee3ec1` |
| W8-R documentary source cut | `a9ebf71e62d84e5dcc599662e976eca7fcd0e623` (separate source cut; **not** an ancestor of protected base or source branch) |
| Source branch | `codex/sorok-programma-product-intake-20261105-r1` at `35ae6f9aeaa5437ec497b44bbd044d32f76d4b0a` |
| Source/protected merge base | `8ffec40a6924848a49f95950aa9ce28c27ee3ec1` |
| Candidate branch | `codex/sorok-programma-selective-receiving-20261105-r1` branched from protected base |
| Method | Exact `git diff protected_base..source_head` for 9 affected existing guide files; `git apply --check`; `git apply`; candidate guide files byte-match the source for those paths |

No missing predecessor was found. The protected base is the exact source merge-base, so the #647 guide delta applies without conflict. W8-R is a separate documentary source cut referenced by the guide, not the protected branch parent.

## 2. Selective change set

Only these 9 existing guide files changed. No unrelated protected guide file, row or field was replaced.

| Path | SHA-256 |
|---|---|
| `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/00_HQ_WRITE_THROUGH_DECISION.md` | `974ab61cd6e62c46a886b12d74cc4724e35e81c5f353c0b8103d67403b26e7f6` |
| `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/06_WORKING_WHOLE_SOROK_ARCHITECTURAL_SPINE_R1.md` | `26d433af5a71eada33daccdec63e9a8249bbde7b3c9444e5ca70d61b66fabf0e` |
| `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/07_GITHUB_ACCESSIBLE_ASSET_LOCATOR_R1.json` | `8ef30f454a9c469ab4ad6ff24c0f33133dc859623bc83fab61823e541da04e91` |
| `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/08_INITIAL_EVIDENCE_GRADED_DEPENDENCY_AND_SEAM_REGISTER_R1.json` | `d960c0d617eb0110031a7ed62e1bbe8d5450d50d3e9b19ffe3b6c80d705b1e48` |
| `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/09_INHERITED_144_FUNCTIONS_TO_WORKING_SPINE_R1.json` | `021f1c5d809639ca8caf6c94c52159ab8675a19c67a5befcb7d51cf71e6a3a24` |
| `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/10_RECONCILIATION_QUEUE_SOURCE_GAPS_AND_CLOSEOUT_CHECK_R1.md` | `2a8cefde835614f2f9ef4505402a2e59d9d4c07d3d7fcdc053488885c179a61c` |
| `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/14_W7_RECURSIVE_PHASE_GATES_AND_WORK_PACKAGES_R1.jsonl` | `b7a89139c3a72b2a47c1424cd2f2852f521beac47a5f6054689eb8ed54f991c3` |
| `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/15_W7_VERSIONED_SEAMS_AND_GATE_JOIN_CANDIDATES_R1.jsonl` | `c853b431c6344a4777040b2a849b1349cf1dd812950a38e418d876b8bfee51c4` |
| `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/READ_FIRST.md` | `7e80a498021380a053f77645b80c2195bf56408996d2f04a07baebc7ad28569e` |

Changed records:

- `07`: `hq_647_incremental_source_reconciliation_20261105`, `hq_p2_local_lifecycle_candidate_20261105`, `hq_p2_interval_later_20261105`, `hq_p2_product_fanin_20261105`.
- `08`: `hq_647_incremental_20261105`, `hq_p2_local_lifecycle_candidate_20261105`, `hq_p2_interval_later_20261105`, `hq_p2_product_fanin_20261105`.
- `09`: same four top-level dispositions; 144 function identities unchanged.
- `14`: 25 existing records (`C4`, `O09`, `S11`, C4/C8/C9/C10/C12/O15/S8/S9/S11 local rows, `E008:LOCAL_GUIDE:TUPLE_MATRIX`, `WP-W6B-01/02/07/19/20/24/34/35/37`); 668 rows and 83 gates unchanged.
- `15`: 10 existing seams (`E004`, `E005`, `E006`, `E008`, `E011`, `E021` and child rows `C12_EPISODE_ROOT`, `M35_B_OPERATION`, `R31E_ACTION`, `B3AS_SCHEMA_READSET`); 38 seams unchanged.
- `00`/`10`: S45-S47 receiving and P2 lifecycle/interval/later-event/fan-in currentness sections.
- `06`: S45-S47 incremental candidate paragraph.
- `READ_FIRST`: #647 navigation link.

## 3. Conflict disposition

- No textual or semantic conflict: protected base is the exact source merge-base and the patch applied cleanly.
- Only the 9 affected guide files changed; all unrelated protected rows, fields, old cuts and source identities remain at protected base.
- The two earlier source return directories were not copied into the protected-base candidate; they remain cited by commit/path.
- No source product, vendor, projection, harness, return, PROGRAMMA architecture or protected branch file was edited.
- Conserved counts: Sorok 09 `144`; 14 `668` rows/`83` gates; 15 `38` seams; 08 `22` seams; 07 `304` assets.

## 4. Verification actually run

```text
python3 CROSS_HQ_CONTROL_ROOM/PROGRAMMA/verify_canonical_programma_r1.py
# PASS canonical tree: Pyat 782/892/62/82, FF 26/16, cross 18/16, Sorok 144/38, no prototype
# exit 0
```

JSON/JSONL parse, count validation and `git diff --check` passed. The candidate guide files byte-match source `35ae6f9a` for all 9 changed paths. No product suite was rerun.

## 5. Original owner acceptance limits and current status

- Lifecycle: `ACCEPT_SCOPED_TEST_ONLY` at review `6398888f1d28152b5d29fef816f0bb45e77dd43b`; local UI lifecycle boundary only, sidecar not security/tamperproof.
- Interval: `AUTHOR_TESTED_CANDIDATE`; independent review `sorok-p2-interval-later-independent-review-20261105-r1` is RUNNING; not accepted.
- Later-event: `AUTHOR_TESTED_CANDIDATE`; same independent review RUNNING; not accepted.
- Product fan-in: `sorok-p2-product-fanin-20261105-r1` RUNNING; not integrated/accepted; not done.
- PR #697: OPEN, READY, UNMERGED at `41bf45813fd0adeffd9b54e1306c2022abe96514`.
- This guide candidate: isolated, pending protected integration; not merged.
- Native C8/C9/C12, CAN008/CAN011, ADP, Pyat, human S11/A5 Gate4/Gate5 and current B-owned context remain unchanged/held.

## 6. NOT_RUN

- No product suite rerun.
- Interval/later-event independent review still RUNNING; no verdict.
- Product fan-in still RUNNING; no integrated/accepted result.
- No native/human/B/Pyat execution, protected merge or PR #697 action.

## 7. PR-ready title and body

**Title:** `PROGRAMMA #647: selectively receive S45-S47 and P2 guide currentness`

**Body:**

```text
Selective PRE-MAIN receiving candidate for the already-published #647 guide write-through 35ae6f9aeaa5437ec497b44bbd044d32f76d4b0a.

Base: integration/pre-main-reconciliation-r1 @ 8ffec40a6924848a49f95950aa9ce28c27ee3ec1
Source: codex/sorok-programma-product-intake-20261105-r1 @ 35ae6f9aeaa5437ec497b44bbd044d32f76d4b0a
Merge base: 8ffec40a6924848a49f95950aa9ce28c27ee3ec1; patch applies cleanly.

Changed only 9 existing guide files; no wholesale replacement, no unrelated protected rows/fields changed, no new guide/project, no product edits.
Changed records: 07/08/09 four #647/P2 dispositions each; 14 25 existing rows; 15 10 existing seams; 00/06/10/READ_FIRST currentness/navigation. Counts preserved: Sorok 144 functions, 14 668 rows/83 gates, 15 38 seams, 08 22 seams, 07 304 assets.

Canonical verifier PASS; JSON/JSONL parse and diffcheck PASS. No product suite rerun.

Status limits: lifecycle accepted scoped TEST_ONLY at review 6398888f; interval/later-event independent review RUNNING; product fan-in RUNNING and not done; PR #697 open/ready/unmerged at 41bf4581; this guide candidate is not merged. Native/human/B/Pyat rights unchanged.

HQ creates the PR through the connector; this return sends no external messages.
```

## 8. Publication

Committed and pushed normally on `codex/sorok-programma-selective-receiving-20261105-r1`. Exact published 40-hex SHA is returned in the final chat readback and verified by `git ls-remote`. No protected write or merge.
