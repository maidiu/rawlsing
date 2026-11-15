# ZL-17 independent R2 re-review — corrected ZL-15 R3

**Verdict: `ACCEPT_SCOPED_S0_S1_REVERSE_DOCUMENTARY__NATIVE_AUTHORITY_AND_FIRST_CONSUMERS_HELD`.**

Reviewed ZL-15 author [PR #864](https://github.com/maidiu/rawlsing/pull/864) at **exact HEAD `ffd994045319db496e642cd797b01b615cc85a24`** (not superseded `c946ae87...`). Protected PRE-MAIN base observed unchanged at `256d46bf425cc37e114465cddbe3c60e535766ab`. Prior ZL-17 R1 review evidence at reviewer commit `471e4587b1ae60a28da53aa63bedc0a76b734407` remains immutable in this branch.

This is an independently re-derived source/graph-level S0–S1 receiving verdict for the **four R17 blockers**, not an endorsement of ZL-16, native/sourcefree execution, original35 functional equivalence, current actor effect, or merge. I inspected immutable GitHub blobs and rebuilt table joins in memory, without using the author's PASS as a premise.

## Exact independently read witnesses

- Frozen G4 source: `PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/CURRENT_SEAM_STATES.jsonl` at source commit `7a5429ffbc48efd25e28c912da80c822e66bc182`, blob **`5a951626c0dde91b682eb23216c88dbfc054808d`**; all 82 JSONL rows read.
- Historical Sorok E001/E014 source: `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/15_W7_VERSIONED_SEAMS_AND_GATE_JOIN_CANDIDATES_R1.jsonl` at `37915a47ed3e33a71ad8334c0aa505f5d65796ca`, blob **`d31eef4f4bc3f4fc6a32ba3e6563c788713f6c47`**. R3 frozen copy under `PRONGS/J_JOIN/FROZEN_INPUTS/SOROK_VERSIONED_SEAMS_37915.jsonl` has the **same exact Git blob**. The current same-path Sorok content is not substituted.
- Protected empirical provider: `rawlsing_next/pre553_empirical_possibility_provider.py` at `256d46bf425cc37e114465cddbe3c60e535766ab`, blob **`23167aa25291fb148b1e3cf210ac33fe7769b783`**; line 574 directly calls `compose_positioned_subject_possibility`. Static call only, selected original source and first operative reader not established.
- Legacy F03: `data/ddm_build_copy/ddm_v550_question_relation_authority.py`, blob **`62084cbed10a5975f79bd504bf4fb99025e4e64e`**, lines 748–858; five QUC guards permit source-authority-row-None preservation, one false clears, explicit BLOCKED row clears. Not executed by this review.
- New canonical tables at exact HEAD: `RELATIONS` blob `2483f7b798352c118b4d208cbcf4c8c1772eb15a` (8,502 rows); `EVIDENCE` blob `75d6e2d29425b5f6438cd7808b1487bfd4e2691c` (2,720); `OPERATION_TRACES` `7fff7cf589f52d385dc1ecc9e03545cd3881eb9e` (332); `CONSUMER_EDGES` `a7c09ff0ebe8faa92357232725ce0a1adbb907af` (332); `AUTHORITY_APPLICATIONS` `bd833fd5d6e8a6f1cf54a691ef1df6316cdfdce8` (370).

## Four R17 findings — recheck results

| R1 finding | Independent R2 readback | Receiving status |
| --- | --- | --- |
| **D01** — 82 lost kind/condition seams | `SEAM_DEPENDENCIES.tsv` contains exactly 82 unique source-line identities. Against 82 frozen JSON objects, independently compared original edge ID, literal endpoints, original requiredness, original predicate, negative and source line: **zero mismatches**. Distribution: **7 MUST, 26 IF, 12 functional OR, 2 functional IF, 35 observed/reported**. All 82 canonical seam relation IDs and both normalized node endpoints resolve. `ASTRA:IF:N0:N4:0` retains the authority-not-bound predicate; `ASTRA:REQ:N10W:N11` remains separate MUST. | **Addressed at S0–S1.** Applicability is explicitly unknown until a selected scope is established. |
| **D02** — producer/consumer ID and reverse chain | **332/332** `OPERATION_TRACES.producer_edge_id` resolve to canonical `CONSUMER_EDGES.edge_id`; **332/332** producer-operation IDs resolve to normalized operations. **332/332** actual consumer IDs remain typed `UNRESOLVED`, with `OPEN_PROOF_GAP` and `NOT_PROVED` call-site SHA. Graph relations cover 332 candidate producer edges. Cold E001 walk: `SOROK:E001` ← N11/N12 owner-held candidate ← N10W→N11 source MUST. Cold N10E walk: candidate N10E→provider→composition, verified at source line 574, no runtime claim. | **Addressed as documentary candidates**, not actual current consumer proof. |
| **D03** — non-ID generic negative | **332/332** `negative_evidence_id` resolve to `EVIDENCE.evidence_id` (331 distinct refs), **67 DIRECT_SOURCE_EVIDENCE_ID** and **265 SAME_FINDING_SOURCE_NEGATIVE**, with separate per-edge negative scope; zero `SOURCE_NEGATIVE_CARRIED` markers. F03 row-none five-guard exception and E014 negative-only remain distinct. | **Addressed for typed documentary navigation.** Same-finding receipts must never be read as an observed negative or source-native enforcement receipt. |
| **D04** — report SHA masquerading as authority evidence | **370/370** authority rows hold either actual normalized evidence IDs or a typed unresolved marker: **59 direct, 306 same-finding, 5 `UNRESOLVED_EVIDENCE`**. No invalid positive ID; `rule_applied_to_output=YES` **0**; `negative_or_refusal_enforced=YES` **0**. Ten source-documentary `rule_selected_for_scope=YES` remain independent of application. | **Addressed for graded evidence traceability.** Actual rule applicability, issuer, applied effect and refusal remain unproved. |

Supplementary custody checks: `P0_LEFT_DISPOSITIONS` 6,125 exact identities / 4,256 `NONE_EXACT` left-only / zero new-function increments; `GENERATION_STAGE_COURT` 4,420 stage rows; canonical RELATIONS contains 1,868 HELD_BY links including 1,536 exact conflict target links and 241 source P0 anchors. These counts support graph integrity only, not downstream semantic acceptance.

## Independent hostile mutation court

Baseline joins: PASS. Individually mutated in-memory inputs and checked rejection without running project-native code:

1. Wrong held conflict target — REJECTED.
2. Unanchored P0 hold source — REJECTED.
3. Invented consumer operation ID — REJECTED.
4. Generic `SOURCE_NEGATIVE_CARRIED` evidence marker — REJECTED.
5. Report SHA used as authority evidence — REJECTED.
6. Fabricated `rule_applied_to_output=YES` — REJECTED.
7. Fabricated `negative_or_refusal_enforced=YES` — REJECTED.
8. Report label substituted into code-SHA field — REJECTED.
9. IF→MUST requiredness promotion — REJECTED.
10. Erased IF predicate — REJECTED.
11. Deleted P0 disposition — REJECTED.
12. P0 disposition function-count inflation — REJECTED.

**Independent court: 12/12 tampered alternatives refused; baseline PASS.** These tests were independently implemented against downloaded R3 tables and the frozen 82-source JSONL, not a claim that the author-side `VALIDATE_ZL15_R3.js` was executed in a repository checkout. The author's 11/11 is a separate, unadopted report.

## Surviving caveat and strict ceiling

This acceptance is narrow. The F03 consumer edge cites same-finding historical C6 provenance (`J-EV-ZL02-ZL02-E-C6-F03_QREL`); its more direct branch witness (`J-EV-ZL02-ZL02-E-SRC-F03_QREL-rel_apply`) is explicitly traversable through `CROSS_PRONG_BRIDGES.tsv`, not claimed as a native negative. An eventual semantic/effect receiving court should request explicit direct negative-evidence links in consumer edges where needed before asserting source-native parity. The present edge grade discloses that weakness and makes no positive execution claim; it does **not** block this S0–S1 *documentary ID/qualification* receiving verdict. The same caution applies to F08 source/authority use and the separately reported E014 GT0 negative; Sorok E001 C11 is not empirical PRE-MAIN C11.

No claim of current-machine zero-loss, original35 complete native run, executed authority/refusal, source-native semantic equivalence, first non-test consumer, owner assent, or functional adoption. S2/S3 NOT_RUN. No protected write, author branch change, reviewer R1 overwrite, PR acceptance-as-merge, or merge.

**ZL-17 gate:** `ZL17_R2_ACCEPT_SCOPED_S0_S1_REVERSE_DOCUMENTARY__ZL16_INDEPENDENT_GATE_SEPARATE__S2_S3_HELD__NO_MERGE`.

ZL-18/#817 remains contingent on its *own* commission prerequisites and separate ZL-16 verdict. This ZL-17 review alone does not authorize it.
