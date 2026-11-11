# ZL-P0R independent hostile receiving — R2 corrected-head adjudication
Date: 2026-11-08 (America/New_York)
Commission: maidiu/rawlsing#799
Original reviewer return: draft PR #821 at original R1 HEAD `e560d83974023550d8b45185d6377137a795f49b`, verdict REVISE; preserve that historical finding and its R1 artifacts.
Current R2 verdict: **HOLD — S0–S1 documentation/crosswalk defects corrected; authorized S2 executable validator and negative controls still NOT_RUN.**
This is an independent re-review on the same isolated reviewer branch. Not P0 acceptance. P1 ZL-02–ZL-14 not released.

## Immutable source/candidate cuts and custody

- Protected `integration/pre-main-reconciliation-r1`: `2162d85db5e6822707e5cdff7aac2656ebef4761` (rechecked before R2; no protected write).
- ZL-00 #797 / draft PR #819: corrected HEAD `11047708a6e4b4050da351f4b6cc35f03cb8269b`; original reviewed HEAD `79f2d0142a0fbbb8f6d2fb039815dbd837a48c3b`.
- ZL-01 #798 / draft PR #820: corrected HEAD `3590b223c1c04df10d78b0c1df3fc2dfa2e32618`; original reviewed HEAD `96f14752a4aef5378462ca99b7f649b55aa7165e`.
- Reviewer isolated branch `review/vmestye-p0-independent-currentness-no-drop-r1`, draft PR #821. This additive R2 report and receipts are not merged. No write to #819/#820 branches.
- Exact G4 historical seam source: `7a5429ffbc48efd25e28c912da80c822e66bc182::PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/CURRENT_SEAM_STATES.jsonl#blob=5a951626c0dde91b682eb23216c88dbfc054808d`, 82 JSONL rows. Protected validator script blob `fb39e939ef4bdd21e52bce78d5a50825317acc6f` (unchanged).
- Current source census SHA via exact blob `ace431dde03fde7aa124c351d2549b6e9b2b587b`: 6,120 census rows, 25 fields, no duplicate five-field tuple. This is source-key identity, NOT 6,120 unique functions or complete live-machine discovery.
- Actual host/editor: ChatGPT authenticated GitHub connector for S0–S1 read and isolated documentation writes. Exact external editor/model/effort assertions are not independently attested. No authorized S2 runner established; no Python execution. No S3 actor/native/scientific or protected merger authority.

## R2 independent method and positive readback

Read corrected source blobs and human return files at the exact two candidate heads; parsed TSV literal headers and all row widths (not author summaries). Re-filtered the 6,120-row census on actual `estate_id`, `source_exact_id`, and `source_path`, compared ZL-01 anti-join evidence/unjoined/negative selectors, and compared original G4 JSONL directly to both the 82-row ZL-00 predicate contract and 82-row ZL-01 predicate receipts. Count and identity comparisons are documentary S0–S1 checks. They are not a substitute for the qualified executable validator, native execution, semantic succession, actual authority effects, or first-consumer proof.

- ZL-00 frozen anti-join requirements: 56 check IDs, unchanged in ZL-01's 110 checks. ZL-00 `P0_RM_CHECK_ID_BIJECTION_V1.tsv`: 30 unique source and canonical IDs. Each `AJ-RM01` through `AJ-RM30` maps to exactly one `RECENT_CAMPAIGN30/source_exact_id=RMxx` census row, with nonempty retained negative.
- D02–D07: 23 exact per-file selectors to grouped `D0x_SOURCE_PACKAGE` plus exact source path resolve to 364 total source census rows, without count mismatch; all `evidence_id`, `unjoined_ids`, and `negative_ids` now dereference nonempty source rows. Scope is each historical file, not a present-day function.
- G4: all 82 edge identities, source row ordinals, literal requiredness and predicates, G2 kind/condition and retained negatives equal the source; original G2 evidence pointer preserved where present, empty where absent. Exactly 26 `IF` predicates remain conditional and are not silently turned into unconditional prerequisites. Observed/reported seams remain observed/reported.
- Revised receipts: ZL-01 110 anti-joins (21 columns), 111 coverage receipts (17 columns), 82 seam predicate receipts (14 columns), 23 estate coverage rows (11 columns); all rows conform to respective headers. Digest values and counts are internally consistent with their declared source/output sets, but no independent qualified SHA256 program was run.
- Census: 6,120×25, 6,120 nonempty retained negative-status fields, no duplicate five-field source identity, and no current semantic/function/authority promotions. All 23 estate coverage rows retain `semantically_reconciled=0`, `authority_application_proved=0`, and `first_consumer_proved=0`.
- Schema: ZL-00 freezes `VMESTYE_P1_PRONG_TABLES_V1` and five literal table headers (OPERATION_TRACES 21 columns; AUTHORITY_USE 16; EVIDENCE 19; COVERAGE 16; UNJOINS 19), foreign-key/enum/sourcecut constraints, and disjoint 13-prong output-path leases. Static freeze PASS. Actual concurrent lease adherence still needs confirmation at P1 dispatch.
- ZL-00 revised return narrative corrects prior 53/57 contradiction. The correction has no power to establish S2 readiness.

## Defect disposition against R1 (append-only)

| R1 defect | R2 independent result | Exact boundary |
| --- | --- | --- |
| D01 Frozen AJ-RM ID renamed | **PASS_S0_S1_CROSSWALK** | 56/56 frozen IDs, 30/30 bijection; mutation still D06 |
| D02 D02–D07 evidence/unjoined source selectors invalid | **PASS_S0_S1_DEREFERENCE** | 23 file selectors, 364 matching rows |
| D03 RM negative selectors invalid | **PASS_S0_S1_NEGATIVE** | 30/30 exact negative selectors resolve |
| D04 G4 edge-only missing IF predicate contract | **PASS_S0_S1_EXACT_PREDICATE** | 82 source and receipt tuples, 26 conditional IF, no functional claim |
| D05 P1 lane schema not frozen | **PASS_STATIC_SCHEMA** | five tables, typed rules, 13 disjoint named output leases; validate live leases at launch |
| D06 Actual validator/negative controls | **HOLD_NOT_RUN** | protected runner not verified; protected validator unchanged; stage-aware readback and 8 fixtures are specifications, not results |
| D07 53/57 contradiction | **PASS_NARRATIVE** | corrected to 57 rows, prior error acknowledged |

Machine-readable disposition: `P0_REREVIEW_DEFECT_DISPOSITIONS_R2.tsv`. Independently generated 58-row identity receipt: `P0_REREVIEW_ANTI_JOIN_RECEIPT_R2.tsv` (30 RM records; 23 D02–D07 files; 2 G4 summary tests; estate/no-promotion summary; census identity summary; executable HOLD summary). Source/receipt equality at S0–S1 does not discharge runnable negative controls.

## Still-blocking validator gate: D06

`P0_VALIDATOR_READBACK.md` now describes a stage-aware structural validator specification and eight negative fixtures. The protected implementation `validation/validate_vmestye.py` remains at blob `fb39e939ef4bdd21e52bce78d5a50825317acc6f`, including its protected pre-launch assumptions. No independently verified authorized S2 host was available for this reviewer; the actual Python baseline, stage migration and each of the eight mutations are **NOT_RUN**, not PASS. Do not run on an unapproved substitute host and do not infer success from prose.

To clear D06, an independently authorized runner/owner must (1) verify runner identity and authorization, (2) pin the protected and both corrected exact candidate HEADs plus the exact validator code SHA, (3) execute a genuine stage-aware baseline against the corrected files, (4) execute negative controls including alias/canonical ID substitution, missing D02 file, dangling filter, IF predicate deletion/IF-to-MUST, schema drift, false authority/consumer promotion, and status/branch-custody misreporting with expected fail-closed behavior, (5) return commands, exit codes, mutation/readback artifacts, stdout/stderr and hashes, and (6) request the **same independent reviewer** to receive that immutable return. Enumeration is a request for test coverage, not a claim that current script already implements these controls.

## Required status and next owner

**HOLD.** ZL-00/#819 and ZL-01/#820 are stronger source/doc candidates; six R1 documentary defects are corrected on their exact current heads. Neither candidate is independently accepted as full P0; do **not** merge, do **not** dispatch ZL-02–ZL-14, do **not** resume #777/#784/#786/#787–#790, do **not** claim all branches searched or current zero loss, original35 native operation, scientific semantics, original respondent authority, or actual first consumer.

**Next action:** Commission a qualified runner/owner to implement/execute and independently return the stage-aware P0 structural validator and eight negative controls, without breaching S0–S1 restrictions of this review. Re-review the immutable execution return and any new corrected candidate heads before deciding `ACCEPT_P0_SCHEMA_AND_ESTATE` versus further `REVISE`/`HOLD`. PR #821 remains a draft review return. This reviewer cannot self-promote P0 or merge the protected base.
