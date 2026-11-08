# C16 — EXACT C15 CORRECTION RETURN

**Issue:** #777, bounded author-HQ correction of C15 findings.
**Branch:** `agent/pyat-hq-pre-forge-to-prev3-authority-severance-functional-adequacy-20261107-r1`.
**Original prepared-branch base:** `e2fdd975f618228ecc4e146840cb0eed2091a20f`.
**C14 intake base:** `46104b8ddf44db4d5a32e603ca9332cebbbb1f94`.
**C15 correction base:** `ad28344350af30861681f50f5b5d908157354223`.
**HQ head at C16 correction:** `9651352a846da9ed85d4e64562b7d2b07b90fb07` (HQ-owned control-room changes in that commit are not C16 writes).
**C15 review content:** `9195d25b67fd99a101e1208b30517a79148d8158`; **C15 review metadata:** `c4f68989788a0a0b27a3b65be610502cb4a824db`; verdict `REVISE`.
**C8 historical snapshot:** content `55fca441d1c674c256473c264cabda48f2df0e52`; 51 cases; `03` SHA-256 `cc4275628286f31ba3695d92910f52d639a3f2d54ca7d43852bbd9d12b614251`; review `356124ee`, focused check `77a879822`, residual closure `0e0997213`.
**C14 historical snapshot:** content `f42b73abf2532f9a4ea589e7f80841e15585d8e1`; provenance `ea7e878a82e2343591724433fcd6b13910602c84`; 55 cases; `03` SHA-256 `f21823f83e6aed6a64695150bf4ed43df2e7fd88b3310ab26752476acc61a778`; external locator `C14_COMBINED_RETURN_INTAKE.json#content_snapshot,#provenance_commit`.
**C16 current `03`:** SHA-256 `a7aa9d1a3530755c755d526c61c2dfb252783d9478eb70f0851fa5ae189e14e7` (canonical = alias; distinct from historical C14 `f21823`). **C16 current content snapshot/provenance:** external C16 intake record/locator; no self-hash inside the content.
**Goal complete:** **false**. Whole #777 remains incomplete; C16 is documentary correction, not acceptance.

## 1. Write boundary

Writes are limited to affected top-level `00`, `01`, `02`, `03` canonical+alias, `04`, `05`, `06`, `08`, `09`, `10` and this `C16_EXACT_C15_CORRECTIONS/` directory.

**Not written:** `CHECKPOINT.json`, `FLIGHT_BOARD.json`, `COMMISSIONS/`, `PYAT_CONTROL_ROOM/`, `07_SECONDARY_AGENDA_NON_DROP_AND_WORKER_COLLISION.md`, C14/C15 historical snapshots/reviews, C7/C8/C9–C13 returns, production code, existing tests, peer/protected/HQ state. The HQ head `9651352a8` changed HQ control-room files; those are HQ writes, not C16 writes.

## 2. Changed files and counts

| File | Change | Rows/records |
|---|---|---:|
| `00_EXECUTIVE_REAL_OPERATIONS_AND_VERDICT.md` | C8/C14 lineage split, base labels, C9 wording/lineage, T3/T4 limit labels, T6 issue table, QUC qualification | 1 doc |
| `01_LEGACY_SELECTED_AUTHORITY_USE_AND_INCOMPLETE_CALLEE_COVERAGE.tsv` | F08 currentness qualification; C9 lineage crossref note | 94 data rows |
| `02_CURRENT_IMPLEMENTATIONS_PRE_FORGE_VS_WHOLE_PREV3.tsv` | F08 current-owner qualification; C9 acceptance-lineage status | 153 rows = 55 CASE + 26 FF + 16 deps + 15 post-FF + 11 seams + 30 #748 |
| `03_BIDIRECTIONAL_AUTHORITY_REQUIREMENT_AND_CONSUMPTION.jsonl` | C9 reviewed-target/correction/acceptance lineage; F08 QUC hold qualification | 55 records |
| `03_BIDIRECTIONAL_FUNCTION_AUTHORITY_CASES.jsonl` | exact-content alias | 55 records, byte-equal |
| `04_PROVED_EQUIVALENCES_AND_NO_BUILD_DECISIONS.md` | C9 wording/lineage; F08 QUC qualification; T3/T4 limit wording | 1 doc |
| `05_SEVERED_OR_INCOMPLETE_MINIMAL_OWNER_REPAIRS.tsv` | C9 evidence lineage; F03/F08 notes | 55 rows |
| `06_REAL_LOCAL_TEST_COMMANDS_OUTPUT_HASHES_AND_MUTATIONS.md` | C9 reviewed-target/correction/no-rereview lineage | 1 doc |
| `08_COVERAGE_DENOMINATORS_COLD_HANDOFF.tsv` | C9 review lineage, C15 review, T3/T4 limit rows | 63 rows |
| `09_INDEPENDENT_REVIEW_REQUEST_AND_EXACT_HEAD.md` | nonauthor independence, C8/C14 snapshot split, base labels, C9 lineage, external C14 provenance locator | 1 doc |
| `10_HQ_PRIORITY_AND_NEXT_WORK.md` | C9 lineage, T3/T4 limits, C16 next action | 1 doc |
| `C16_EXACT_C15_CORRECTIONS/00_RETURN.md` | this return | 1 doc |
| `C16_EXACT_C15_CORRECTIONS/FINDING_RESOLUTION.jsonl` | 10 C15 finding resolutions | 10 rows |
| `C16_EXACT_C15_CORRECTIONS/PARENT_ISSUE_DISPOSITIONS.jsonl` | 12 issue/PR dispositions | 12 rows |
| `C16_EXACT_C15_CORRECTIONS/GOAL_AUDIT.json` | updated six-criteria audit | 1 JSON |
| `C16_EXACT_C15_CORRECTIONS/VALIDATION.md` | exact validation commands/results | 1 doc |
| `C16_EXACT_C15_CORRECTIONS/validate_c16.py` | proportionate validation script (nonzero on failure) | 1 script |

## 3. Case identity and taxonomy preservation

- **51 historical case IDs/taxonomy preserved** from C14/C8: C1 1/C2 2/C3 10/C4 2/C5 7/C6 29; historical taxonomy **21 FUNCTION_CURRENT + 30 NOT_RUN**.
- **4 C9 cases preserved:** `C9-O08-QUERY-TARGET-USE`, `C9-O12-ISSUED-WORKLOAD`, `C9-O13-BATCH-RECEIVING`, `C9-P1-CANDIDATE-BOUNDARY`.
- **Current return: 55 unique cases** — C1 1/C2 2/C3 10/C4 2/C5 7/C6 29/C9 4; **25 FUNCTION_CURRENT + 30 NOT_RUN**; 0 historical-only; 0 implementation-inadequate; 0 original-wired; 0 qualified-equivalent; 0 proved-severance.
- All 55 retain nonempty A–J, `forward_walk`, `reverse_walk`, `exact_hold`, `frozen_taxonomy_verdict`.
- `02`/`03`/`05` case ID sets are identical; canonical/alias `03` are byte-equal.
- Historical denominators remain separate: 29/58/228/581/687; 42 selected-state/16 unresolved; 15/8/7/10/3; 26/16; 15/11; 154/1608; no magic sum. 17 A01–A17 gates remain open.

## 4. C15 10/10 correction mapping

| C15 finding | Resolution |
|---|---|
| **C14-G6-T6** | Blanket hold replaced by 12 issue/PR rows in `PARENT_ISSUE_DISPOSITIONS.jsonl` and the T6 table in `00`/`GOAL_AUDIT`. Each has exact record/cut, evidence grade, #777 disposition, retained hold, owner and precise next action. No issue closure/merge/semantic acceptance. |
| **C14-F01-C8-LINEAGE** | Removed stale "C8 review not performed"; recorded C8 review `356124ee`, focused `77a879822`, residual `0e0997213`, C8 content `55fca441`/03 `cc427562`, C14 historical `f42b73ab`/03 `f21823`, C16 current 03 `a7aa9d1a` separately. |
| **C14-F02-BASE-LINEAGE** | Original prepared base `e2fdd975`, C14 intake `46104b8d`, C15 base `ad2834435`, HQ head `9651352a8` distinguished. |
| **C14-F03-REVIEWER-INDEPENDENCE** | Replaced all-prior-reviewer ban with nonauthor-of-C14/fanin/implementations; prior C5 review `ea9ff9e54` disclosed; no fan-in write authority; model/effort verification retained. |
| **C14-F04-C9-LINEAGE** | All 4 C9 records separate reviewed target `d540cfcc` + review `05a750ad` `REVISE_SCOPED` from correction `02a13a5e`; HQ scoped acceptance after correction with no independent re-review; `review_targets_correction=false`, `correction_reviewed=false`. |
| **C14-F05-C6F08-QUC** | `NO_QUC_READER` removed/qualified everywhere; F08 exact hold now `UNPROVED_CURRENT_SELECTION__CURRENT_QUC_OWNER_AND_FIRST_CONSUMER_UNKNOWN_NOT_PROVED__NO_SELECTED_CURRENT_OPERATION__NO_ABSENCE_PROOF`; grade preserved `NOT_RUN`. |
| **C14-G3-T3** | T3 relabelled `SATISFIED_AS_LIMIT__ZERO_EQUIVALENCE_CLAIMS__NO_PRODUCT_POSITIVE_PROOF`. |
| **C14-G4-T4** | T4 relabelled `SATISFIED_AS_LIMIT__ZERO_PROVED_SEVERANCES__NO_PRODUCT_POSITIVE_PROOF`. |
| **C14-F06-C9-WORDING** | C9 now "real API path exercised in the sourcefree test-only harness; not a production/non-test selected operation"; `TEST_ONLY_SOURCEFREE` ceiling preserved. |
| **C14-F07-PROVENANCE-PLACEHOLDER** | Replaced moving branch-head placeholder with external C14 intake locator `C14_COMBINED_RETURN_INTAKE.json#content_snapshot,#provenance_commit` and exact C14 provenance `ea7e878a`; C8/C14/C16 hashes separate; no self-hash. |

## 5. T6 actual issue-by-issue disposition (full rows in `PARENT_ISSUE_DISPOSITIONS.jsonl`)

**Union/dedupe:** 12 unique rows = parents `#716/#748/#753` + post-765 Pyat scope `#765/#766/#767/#772` + associated PRs `#769/#770/#773/#774/#691`. Referenced within parent rows, not expanded as separate dispositions: `#764` (B6), `#771` (HQ recourt), `#736/#739/#741/#742/#744/#745` (legacy estate). No unrelated repository issues >=765 added.

| Issue/PR | Live state | #777 disposition | Retained hold | Owner / next action |
|---|---|---|---|---|
| **#716** | open | Parent scope retained; 29/58/228/581/687 historical coverage accounted; A01–A03 open | A01 dynamic/reflection residue; A02 22 crosswalk/issuer/custody; A03 actual historical operation/negative selector | Legacy L1–L4/asset/function owners; resolve exact gaps, no new archaeology |
| **#748** | open | 30 responsibilities mapped; R1/R2/R4 denominators retained; R5C/R5D holds | A11 F14/R5C integrity; A12 R5D pressure | R5C F14 owner; bind F13 receipt/membership + negatives; keep R5D numeric |
| **#753** | open | 27 B5 operations mapped; C9–C13 sourcefree/test-time evidence; T2 typed hold | Selected shared35/F03/QUC/issuer; A04/A05/A09/A14 | Pyat HQ + source/science/C11 owners; name selected operation + exact authority |
| **#765** | open | R7 sourcefree falsifiers accepted; T01 generic RED; no production repair | A06 T01 repair; A07 T02/T03 | C11/I03/FF owners; review #770, require kind/op/scope DENY + cold restore |
| **#766** | open | Historical AR-0007/0046 sourcefree parity; no selected R1/dememp consumer | A05/A14 selected issuer/current ingress | R8 owner; name selected current operation or NOT_RUN |
| **#767** | open | F13/F14 R5C D2 integrity material; S2 not run; R5D numeric/reference-only | A11/A12 | R5C F14 owner; polarity/zero-support/forged-row negatives; no pressure→I04 |
| **#772** | open | Q86 bounded canary; #774 open/unmerged/pending review; generic FF not proved | A08 #774 review/CI; A09 generic FF; A10 16-chain | Q86/FF/CI owners; exact source/hash/negatives review; no false CI green |
| **#769** | open PR, head `490fc5f8` | Historical AR-0007/0046→C11 necessity court; no current selected consumer | A05/A14 | R8 owner; selected operation/issuer or NOT_RUN; no merge |
| **#770** | open PR, head `392de04e` | Sourcefree first-consumer falsifiers; T01 RED; no production repair | A06/A07 | C11/I03/FF owners; review + cold restore; no production patch |
| **#773** | open PR, head `b3aae6aa` | Sourcefree AR-0007/0046 dememp→C11 parity; no current selected consumer | A05/A14 | R8 owner; selected operation/issuer or NOT_RUN; no merge |
| **#774** | open PR, head `9c776b35` | Q86 source-identity guard candidate; open/unmerged; independent review pending | A08/A09/A10 | Q86/FF/CI owners; exact review; no generic FF claim |
| **#691** | open PR, head `a6b815ec` | GF1 test-only/unmerged generic pair candidate; no selected non-test FF; no defect proved | A09/A10 | GF1/FF owner; named real operation + five-test court; no merge/engine |

Live GitHub state observed `2026-11-08T06:44:54.743614+00:00`; all 12 open; all PRs unmerged. No issue closure, merge, post message, fresh semantic acceptance or current issuer is created.

## 6. Exact remaining boundary

The single smallest substantive decision is to name **one actual selected current operation** and its exact competent authority:

- C9 P1/shared35: selected source/wave + current C11 release + I03 query/predicate; else `NOT_RUN__UNPROVED_SELECTION`.
- C9 O08/O12: exact current target-use permission and original/current source/science decision record; else sourcefree witness only.
- C10/C13 F03: selected current F03 operation + exact current authority/permission; else `F03=UNPROVED_CURRENT_SELECTION`.
- C11/C12 F08: selected current QUC operation + exact successor contract; else `UNPROVED`/`NOT_RUN`.

No new science gate, no retirement, no missing-engine inference, no 630 missing capabilities, no QUC absence proof. C9 empty C11 is expected as-built negative; 630 non-DIST are typed refusals.

## 7. Validation

Exact validation script and output: `C16_EXACT_C15_CORRECTIONS/validate_c16.py`, `C16_EXACT_C15_CORRECTIONS/VALIDATION.md`. The script checks 55 unique IDs/families/taxonomy, 51 historical ID/taxonomy preservation against C14, A–J/holds, canonical/alias byte equality, C9 lineage, F08 QUC qualification, 02/03/05 ID equality, 02 register counts, 01/08 row counts, 10 finding resolutions, 12 parent dispositions, T2/T3/T4/T6 statuses, goal false, no moving-HEAD placeholder, no unqualified NO_QUC_READER, 17 gates, and forbidden-path non-modification. It exits nonzero on any failure; no vacuous PASS.

## 8. Status

- **C15 verdict:** `REVISE`.
- **C16 correction:** ready for HQ intake.
- **New review authorized by C16:** no; HQ handles intake/disposition.
- **Whole #777:** incomplete; `goal_complete=false`; quota `UNKNOWN`.
- **No native/original35/science/actor/N11/N12, production adoption or protected merge.**
