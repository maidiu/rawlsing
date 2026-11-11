# ZAK-02 / MCR-AF author return — historical V549b–V552J operation and first-consumer succession

**Disposition:** S0–S1 documentary investigation with qualified source findings, **INCOMPLETE for all nine independent MCR-C obligations**. No S2/native/first-reader/original35 proof; no S3, protected merge, authority promotion, self-receiving or HQ campaign redesign. This is a *candidate author return*, not a declaration of mission closure.

**Repository:** `maidiu/rawlsing`; author branch `agent/vmestye-zak02-mcr-20261110-r1`; draft [PR #904](https://github.com/maidiu/rawlsing/pull/904) targets unmerged parent branch. Source protected branch `integration/pre-main-reconciliation-r1` stayed at `9366b42a61a383808071106d70aa1255a769390a` when frozen. Commission baseline `9d24323494cc852ada078010f09bfcf9ceb911d9` with defective blob `daf8929a9a4fd96d288509aa18da5d752e59b925`; repaired complete commission blob `00402697f68d4c1364d59bcb059f9134b5d0c74a`, identical to unmerged parent PR #887 complete version and equal to attached text plus trailing newline. Four-document publication HEAD is the exact PR head, to be verified separately.

## Contract / authority and tool grade

- Adopted MCR §3A/MCR-AF/MCR-C: `CROSS_HQ_CONTROL_ROOM/HQ_JUDGMENT_BEARING_RETURNS_INTAKE_AND_DUAL_ECONOMY_COMMISSION_LAW_R1.md` @ PRE-MAIN `9366b42a`; official MCR-C validator `CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py` blob `6e16878e60e8e89bf8ab8001144ed84ad257f5fc`.
- The attached nine-obligation contract's structural parse returned `PASS_FORMAT_ONLY_NOT_AUTHORITY_OR_LAUNCH` with nine unique IDs, no format errors; contract SHA256 `d56570b3910a70bb8c36cfed07a89c22fdaeba117a20f1148e22b0925447089c`. Do not treat this as actual original source, reviewer, or S2 proof. GitHub Actions first preflight at initial exact attachment byte blob failed `verify_hq_a_narrow_conservation` because the file differed from parent by terminal newline; source-check step skipped. The normalized parent-identical contract permits rechecking the official workflow after this return commit.
- Evidence grade: frozen GitHub source inspection plus 13/13 claim-sensitive literal/absence assertions = **S1 source assertions**, not source-executed S2. No full native runner/rights; local `gh` not authenticated. No claims of Browser/GPT-6 High runtime selection verification are made; authenticated repository connector was used.

## Source cut and selected real code seams

All pinned below at historical commit `9253064bc9423a0f0ccda4fbdea43c2f54f800c6` (read through authenticated repository; Git blobs compared):

| Seam | Immutable path | Git blob | Source-level operation |
|---|---|---|---|
| V549b | `data/ddm_build_copy/build_question_response_attitude_cloud_summary_v549b.py` | `bf874a95ea5172817b0d1bdf21b43600aac5cbfe` | reporter candidate loops; parquet/DuckDB writing |
| F03 QRA | `data/ddm_build_copy/ddm_v550_question_relation_authority.py` | `62084cbed10a5975f79bd504bf4fb99025e4e64e` | qualified QUC no-match and coordinate clear |
| F08 override | `data/ddm_build_copy/ddm_v550_question_use.py` | `8d90a5116fd05b5db17e9b4645638a3aa6fc1131` | distinct override identity RuntimeError |
| V550J association | `data/ddm_build_copy/ddm_v550j_joint_patterns.py` | `644aab23675b26134040d1df5cc25538b613e163` | same-respondent join, answered-var risk set |
| V551J packets | `data/ddm_build_copy/ddm_v551j_packets.py` | `740bae4cfd4da7ed8aa2c9a2321c47f26ba7c7e8` | cross-contract components and certification gates |
| V552 pressure | `data/ddm_build_copy/ddm_v552_structural.py` | `0df56d70cb3880dee723df00aea2207acd525260` | count surface coverage and weighted signed score |
| V552J handoff | `data/ddm_build_copy/ddm_v552j_handoff.py` | `476e617370e8947ee1f38b0718243ecfc5ba9e5c` | structural facts scoring/tie order and downstream join |

First source-level consumers/callsites: `ddm_v550_bridge.py` @ `9253064bc9423a0f0ccda4fbdea43c2f54f800c6` blob `29edd5e24f095334683035f2ce1ec95674fe274b`, line 1008 calls F03; `compile_v551j_joint_evidence_packets.py` blob `2df97875172778c3f4616c0799c08667b57db407`, line 1304 consumes J pattern into packets; `compile_v552j_structural_handoff.py` blob `a3e6bf17386b58beb0c14b2d79d9e4a9e405c300`, line 152 calls V552J join. These are **callsites, not observed first non-test production readers**. V549b outputs at lines 1042–1045 but its first downstream reader remains unverified.

## Selected findings, actual source versus possible effect

- **V549b:** `build_answer_presence_anchors` conditionally logs each 50th candidate at lines 604–610. Its format string references unbound `answer_type` (and earlier `cand_item_id` before assignment), so this branch can raise `NameError`; a comparator successfully executing its other paths does not prove a completed run. The `main` pipeline writes outputs only after downstream processing (lines 969–1045). The source logic is identified; conditional native repro and actual first reader remain NOT_RUN/UNOBSERVED.
- **F03:** Six structural coordinates are `driver_id`, `driver_facet_id`, `question_block_id`, `structural_domain_id`, `relation_axis_id`, `target_entity_id` (49–56). No registry match preserves inbound QUC only when **all** `CERTIFIED`, `RELATION_EVIDENCE`, atom eligible, allowed_as_v551_relation_evidence and mapping COMPLETE; otherwise it clears six fields and polarity/eligibility (751–782). This does not certify that the inbound QUC is a valid original issuer. **F08:** `ddm_v550_question_use.py` 1106–1184 raises `RuntimeError` for duplicate or different matching manual override identities. Neither refusal nor preservation was natively replayed.
- **V550J→V551J:** `respondent_id_norm` inner join prevents association based merely on separate marginals; denominator `answered_var_within_pattern` uses target-variable answering pattern members, whereas `eligible_context` is the baseline (J 3505–3668, 3947–3950). V551J has a distinct ordered component-vector/cross-contract gate (`ddm_v551j_packets.py` 1400–1460, 1538–1586): ambiguous matches, conflicts, unexplained components or fewer than two relation components cannot be labeled certified joint relation. A label alone cannot stand in for compatible measurements. No native original run or selected real first reader.
- **V551/V552:** V552 `_surface` sees selected counts [1,1]/denom2 as COMPLETE coverage 1; [2,2]/denom2 as BLOCKED_RESPONSE_CATEGORY_COUNT_EXCEEDS_DENOMINATOR coverage 2 (130–136). Its separate score branch can still produce OBSERVED_* and `ALLOW` with eligible normalized signed components (159–175), regardless of that coverage label. Thus a BLOCKED coverage diagnostic must not be rewritten as either COMPLETE coverage or automatically DENY score. This is source-predicted arithmetic, **not** original production execution.
- **Hostile V552J:** Matching shared semantic identifiers carries scores 4+3+3+2=12; `_packet_structural_dimension_resolution` orders descending by score then fact ID and selects `[0]` without testing an equal-top-score collision (69–95). Two different exact-scope facts at 12 therefore yield a deterministic possible winner, not established semantic uniqueness. Required S2 twin-fact negative is NOT_RUN.

## Nine original obligation dispositions

| Obligation | Author artifact/source state | MCR-C disposition |
|---|---|---|
| `ZAK02-TASK-01` | S1 source inspected, S2 native NOT_RUN | **INCOMPLETE: minimum S2 and independent reviewer** |
| `ZAK02-TASK-02` | S1 F03/F08 branches inspected, S2 native NOT_RUN | **INCOMPLETE: minimum S2; QUC issuer not independently verified** |
| `ZAK02-TASK-03` | S1 J/V551J source inspected | **INCOMPLETE: independent S1 review and first consumer absent** |
| `ZAK02-TASK-04` | S1 V552 source inspected, native arithmetic inferred | **INCOMPLETE: S2 and independent reviewer absent** |
| `ZAK02-HOSTILE` | S1 V552J tie/negative inspected | **INCOMPLETE: S2 tie fixture and first-reader effect NOT_RUN** |
| `ZAK02-OUTPUT-01` | 00_RETURN.md authored; head readback pending | **INCOMPLETE until byte readback and independent review** |
| `ZAK02-OUTPUT-02` | HISTORIC_OPERATION_BEFORE_AFTER_NEGATIVE.tsv authored | **INCOMPLETE until exact-head readback and independent review** |
| `ZAK02-OUTPUT-03` | HIGH_IMPACT_EXCEPTION_PANEL.md authored | **INCOMPLETE until exact-head readback and independent review** |
| `ZAK02-OUTPUT-04` | ORIGINAL_RUN_AND_FIRST_READER_HOLDS.jsonl authored | **INCOMPLETE until exact-head readback and independent review** |

The nine IDs are conserved. Support receipts (one per `MCR_OBLIGATION` evidence path) deliberately state INCOMPLETE and actual S1 grade. `COVERED_IDS.txt` enumerates all nine identities; **coverage is not completion**. The official `--verify-return` cannot return `READY_FOR_INDEPENDENT_RECEIVING` absent S2 minimum grades and independent execution, and the source law explicitly calls it an author documentary readiness gate only.

## Full engineering / scientific / authority 3×5 courts (author-side, **not independent**)

| Court / check | What was examined | Actual evidence grade | Unresolved gate |
|---|---|---|---|
| E1 source / executable seam | Frozen source blobs and function anchors cross-checked | S1 STATIC; native and original35 NOT_RUN | Historical version selection remains qualified |
| E2 operation/input/output | 13 named cases separate before, deny, restore predictions | S1; no before/after runtime receipts | Do not infer original production from branch text |
| E3 adversarial negative | 13 exact source assertions and additional F03 permission mutant specified | S1 assertions, NOT S2 case replay | Unbound reporter and equal-top facts remain native falsifiers |
| E4 consumers / activation | Bridge and compiler callsites cited with immutable SHA | Callsite S1 only; real first reader UNOBSERVED | ZAK05/ZAK08 names are handoff targets |
| E5 repair / conservation | 6 noninverse IDs retained; exception panel and holds | INCOMPLETE whole-mission conservation | No new rules, no protected merge |
| S1 scientific construct | Semantic role / QUC 5-input conjunction documented | Source conditional only | No independent scientific issuer |
| S2 component measurement | J answered-var denominators and packet vector gates documented | S1 code and algebra | No original data/estimator trace |
| S3 structural pressure | V552 selected count coverage vs score permission distinguished | S1 source code | No empirical original35 authority |
| S4 V552J semantics | Two different facts tie at exact score 12; deterministic ID ordering | S1 source, S2 tie NOT_RUN | No semantic uniqueness claim |
| S5 scientific receiving | No empirical or source-owner qualification obtained | HOLD | Separate scientific/source owner required |
| A1 immutable authority | Commission baseline 9d missing contract; parent 887 has complete one; fixed exact contract on isolated branch | Source IDs verified | Protected PRE-MAIN not edited |
| A2 lease / writer | Own isolated branch created; no competing writer observed in connector view | Remote single-branch observation | External exclusive lease unverifiable |
| A3 permission boundaries | S0/S1 source only; S2 gated, S3 prohibited; no source/actor issuer | AUTHORIZED S0/S1 | No silent model or editor certification |
| A4 parent / downstream | Parent #888 independently unreceived, PR #887 still draft; downstream #814–817 separately owed | BLOCKED gate | No receiving/promotions |
| A5 independent MCR-C | No nonauthor 3×5 court or exact-head READY receipt | HOLD | Do not self-accept |

## Negative checks and whole mission conservation

The 13 S1 source assertions were executed against **frozen fetched source text**: 50th-candidate reporter and absent binding, five-condition QUC preservation and clear, distinct F08 override refusal, respondent-ID join, risk-set denominator basis, V551J incompatible component gate, V552 coverage overcount and separate ALLOW scoring branch, V552J deterministic sort and **absence** of a named equal-top veto. All 13 matched source; they are static inspections, not runtime tests. A separate proposed falsifier removes the `allowed_as_v551_relation_evidence` conjunct while retaining CERTIFIED; without full conjunct F03 must deny, not silently preserve. That mutant is **NOT_RUN**.

The full MCR-AF mission is not collapsed into this V549b/F03/J/V552 pilot: six fixed noninverse source candidates are individually conserved in the exception panel and JSONL (`T1-ZL03-ZL03-T11`, `T1-ZL07-TR-041`, `T1-ZL03-UNTRACED-ZL03-F16`, `T1-ZL05-ZL05-OP-003`, `T1-ZL08-ZL08-T-CODE-LMX-016`, `T1-ZL02-ZL02-T-F09_ROUTING`). Their inverse, selected source/owner, original world/actor effects and real first reader are unverified; no absence-of-current-function verdict follows. Other ZAK01/03/04/08 upstream and Long Memory/FF/Pyat/Sorok downstream court ownership is not transferred to this author. No false serial barrier is imposed on parallel authorized investigation.

## Explicit holds / handoff

1. **Original S2 operations**: no verified authorized native runner with historical inputs; no same-input before/refuse/restore traces for V549b, F03, F08, J/V551J, V552 or V552J; **NOT_RUN**.
2. **Source/scientific/authority**: original35 or source semantic/survey/actor issuers not verified. No new authority or actor model can be issued here.
3. **First consumers**: code-level callsites exist; original and live non-test reader acknowledgments not independently observed. ZAK05/ZAK08 handoff remains pending.
4. **Parent gate**: parent independent receiving issue #888 on PR #887 remains unresolved, and exclusive writer lease outside branch isolation cannot be established with this connector. Parent downstream #814–817 acknowledgments remain separate duties, not invented upstream prerequisites.
5. **Independent receiving**: qualified nonauthor engineering, scientific, authority 3×5 tests, exact committed outputs and negative/consumer verification remain outstanding. Do not self-accept or merge.
6. **CI gate**: first-run preflight failed the descendant byte equality after a one-newline difference and skipped official source-check. Normalized contract now restores parent exact blob. The unrelated governed court had 144 successes and 3 preexisting pin failures; neither grants ZAK-02 acceptance. Report final new-head CI independently.

**Handoff to receiving reviewer:** Freeze the actual PR #904 HEAD, fetch the four committed outputs and nine honest evidence paths; run official MCR-C source checks and the 94 descendant no-drop enumerator, then independently execute falsifiers on exactly frozen inputs where authority permits. Maintain `INCOMPLETE` until positive/denied/restored S2 and first-reader evidence are real. Return exact-head verdict with source/grade, engineering/scientific/authority challenge, qualified owners, and explicit no-drop conservation. Do not use this author's static checks as independent proof.
