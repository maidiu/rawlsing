# SOROK PROGRAMMA selective PRE-MAIN receiving candidate — repaired-source intake

**RESULT:** `SELECTIVE_PREMAIN_RECEIVING_CANDIDATE_CURRENT__SOURCE_F5D0AF85D__PROTECTED_BASE_8FFEC40A__INTERVAL_76D5_ORACLE_PASS__LATER_B716_AUTHOR_PASS__PRODUCT_25D_UNACCEPTED_REVIEW_RUNNING__PR699_PR697_UNMERGED__NOT_MERGED`.

This candidate closes the existing pending guide-integration engineering gap for the #647 guide write-through. It carries the two completed public-boundary repairs and preserves the prior selective-base proof. It is a receiving candidate only; no protected write, merge, product edit or new guide architecture was performed.

## 1. Exact bases and provenance

| Item | Exact identity |
|---|---|
| Live protected guide base | `integration/pre-main-reconciliation-r1` at `8ffec40a6924848a49f95950aa9ce28c27ee3ec1` |
| W8-R documentary source cut | `a9ebf71e62d84e5dcc599662e976eca7fcd0e623` (separate source cut; **not** an ancestor of protected base or source branch) |
| Current source guide | `codex/sorok-programma-product-intake-20261105-r1` at `f5d0af85d14285b694c7155ed7ccf5d2622a4243` |
| Prior source guide cuts | `b8c764f1279e5116d74d98ae7f5e423c5c69f7da`; `35ae6f9aeaa5437ec497b44bbd044d32f76d4b0a` |
| Source/protected merge base | `8ffec40a6924848a49f95950aa9ce28c27ee3ec1` |
| Candidate branch | `codex/sorok-programma-selective-receiving-20261105-r1`; PR699 branch head `b6d3f8d2b946a38f6336361c2b625c1260699100` before this update |
| Method | Same selective diff application from protected base; this update applies the exact 7-file currentness delta `b8c764f..f5d0af85d`; all 9 affected guide files byte-match source `f5d0af85d` |

No missing predecessor was found. W8-R remains a separate documentary source cut, not the protected branch parent.

## 2. Selective change set

This update touches only these 7 existing guide files; the prior `06` and `READ_FIRST` selective additions are retained unchanged.

| Path | SHA-256 |
|---|---|
| `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/00_HQ_WRITE_THROUGH_DECISION.md` | `845ffd945dfff51a9b07dc0416700358c392621d8ffaea00fa1f509154b11602` |
| `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/07_GITHUB_ACCESSIBLE_ASSET_LOCATOR_R1.json` | `050c138037e1c5e429d746e25ee376e4a8ff084252313869a795263e512f465f` |
| `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/08_INITIAL_EVIDENCE_GRADED_DEPENDENCY_AND_SEAM_REGISTER_R1.json` | `7dee968b85df9622d8588b42d71af39d8c0bc411ed82ec12d5f10a7a1fb5a090` |
| `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/09_INHERITED_144_FUNCTIONS_TO_WORKING_SPINE_R1.json` | `03b64e8bee27041a1ff2ef949f44185104ccfe8781924954c7f917f0eaf5ef36` |
| `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/10_RECONCILIATION_QUEUE_SOURCE_GAPS_AND_CLOSEOUT_CHECK_R1.md` | `2914d34115cb22c92afa221fea8591165d387386165d259418df74ffe7fae715` |
| `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/14_W7_RECURSIVE_PHASE_GATES_AND_WORK_PACKAGES_R1.jsonl` | `14c6c280048ce20f6d7cb698dc144f2928fd9a4030ef71f53ca1f6c4624bbfc6` |
| `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/15_W7_VERSIONED_SEAMS_AND_GATE_JOIN_CANDIDATES_R1.jsonl` | `2979c65fde3e9347c5fc4d15305a82d1cb9c8726f48e596d33c93ece44c6742e` |

Changed existing records: `07/08/09` `hq_p2_interval_later_20261105` and `hq_p2_product_fanin_20261105`; `14` 20 existing rows; `15` 8 existing seams; `00/10` repaired-source currentness. Counts preserved: 144 functions, 14 `668` rows/`83` gates, 15 `38` seams, 08 `22` seams, 07 `304` assets.

## 3. Conflict disposition

- No conflict: protected base is the exact source merge-base; the 7-file delta applies cleanly and all 9 selective guide files byte-match source `f5d0af85d`.
- Prior selective-base proof `8ffec40a` is preserved; prior source cuts `b8c764f` and `35ae6f9a` remain historical references.
- No unrelated protected row/field, product, vendor, projection, harness or protected-branch file changed.
- Source return directories were not copied into the protected-base candidate; they remain cited by commit/path.

## 4. Reconciled repaired sources and exact readiness

- Interval original `bdadbc57`: original `REVISE` `f1a287` retained. Primary repair `7a256ed4`: primary no-auto-help independently PASS at closure `89b334`; closure still `REVISE`d public keys and pyc census. Final correction `76d5a3d13e`: 6 author tests `78.34s` plus original privacy/receipt oracle PASS; keys `admission_status`/`c9_public`; 29 actual receipt files, no `.pyc`; final key/census fix author-only.
- Later original `76fdb624`: original `REVISE` `f1a287` retained. Final repair `b71624f2` (code `4bdba46c`): 8 author tests, 0 public privacy hits, observation encounters `0→0`, explicit help `0→1`; original primitive/source/cut/cold positives preserved; final repair independent review NOT_RUN.
- Product current `25d40806` remains independently unaccepted: exact `25d408` review RUNNING retry2; `76d5` import RUNNING `sorok-p2-final-interval-import-20261105-r1`; later `b716` not imported yet.
- Receiving engineering `bf574e5a` PASS remains engineering evidence only, not independent acceptance or merge.
- PR699 (`b6d3f8d2`) and PR697 (`41bf4581`) remain unmerged. Lifecycle scoped acceptance `6398888f` and accepted `41bf` preserved.
- No automatic dependent READY/native/human/B/protected promotion.

## 5. Verification actually run

```text
python3 CROSS_HQ_CONTROL_ROOM/PROGRAMMA/verify_canonical_programma_r1.py
# PASS canonical tree: Pyat 782/892/62/82, FF 26/16, cross 18/16, Sorok 144/38, no prototype
# exit 0
```

JSON/JSONL parse, count validation and `git diff --check` passed. No product suite rerun; no running worker polled or invented.

## 6. NOT_RUN

- Exact `25d408` independent review RUNNING retry2; `76d5` import RUNNING; later `b716` not imported.
- Final interval key/census fix and final later repair are author-tested only; no acceptance promotion.
- No product suite rerun, no native/human/B/Pyat rights, no protected merge.
- No dependent READY.

## 7. PR-ready title and body delta

**Title:** `PROGRAMMA #647: selectively receive S45-S47 and repaired P2 guide currentness`

**Body delta:**

```text
Reconcile the two public-boundary repairs into the selective PROGRAMMA #647 candidate:
- interval 76d5a3d13e: 6 author tests 78.34s + original privacy/receipt oracle PASS; admission_status/c9_public; 29 actual receipt files, no pyc; primary no-auto-help PASS at 89b334 preserved; final key/census fix author-only.
- later b71624f21: 8 author tests; 0 public privacy hits; observation encounters 0->0, explicit help 0->1; original primitive/source/cut/cold positives preserved; final repair independent review NOT_RUN.
- original cuts bdadbc57/76fdb624 REVISE f1a287 preserved.
- product 25d408 remains unaccepted: exact 25d review RUNNING retry2, 76d5 import RUNNING sorok-p2-final-interval-import-20261105-r1, b716 not imported.
- receiving engineering bf574e5a PASS is not independent acceptance/merge; PR699 and PR697 remain unmerged.
- lifecycle scoped acceptance 6398888f and accepted 41bf preserved; no automatic dependent READY/native/human/B/protected promotion.
- no product, guide-schema, registry or protected edits.

Base: integration/pre-main-reconciliation-r1 @ 8ffec40a6924848a49f95950aa9ce28c27ee3ec1
Source: codex/sorok-programma-product-intake-20261105-r1 @ f5d0af85d14285b694c7155ed7ccf5d2622a4243
Changed existing guide files only; canonical verifier PASS; no product suite rerun.
HQ creates the PR through the connector; this return sends no external messages.
```

## 8. Publication

Committed and pushed normally on `codex/sorok-programma-selective-receiving-20261105-r1`. Exact source-branch and receiving-branch SHAs are returned in the final chat readback and verified by `git ls-remote`. No protected write or merge.
