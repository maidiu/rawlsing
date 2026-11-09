# VMESTYE ZL-P4R #817 — independent R5 re-review (R2)

**Verdict:** `REVISE_R5_D02_CANONICAL_STATUS__D01_REPAIRED__ESTATE_RECIPROCAL_NATIVE_HELD__NO_MERGE`.

**Frozen author candidate:** ZL-15 draft PR #864 at `cc21762ac3c7b49e389835b669a578d48caa1fc4`. **Comparison baseline:** prior R4 author HEAD `d10602355c77564b2b6d50601ebba4fed4ac7d58`. Exactly one author R5 commit and nine changed paths separate these heads. **Protected law/base:** `integration/pre-main-reconciliation-r1@256d46bf425cc37e114465cddbe3c60e535766ab`. **Independent reviewer branch:** existing P4 review PR #868 based on protected PRE-MAIN; this R2 appends new review-only files without modifying or retracting historical R1 findings. Exact reviewer return HEAD is the PR branch HEAD after this report is committed (not self-embedded).

This is an independent S0–S1 documentary cold re-review, not a new author repair, formal GitHub independent-user APPROVE, Pyat/Long Memory owner receiving, source/native execution, or an authority/science/consent grant. Source files were fetched by their immutable Git blob SHAs; TSVs were parsed independently as literal records, including full R4/R5 tables and R5 migration and seed ledgers. The author validator was inspected but its successful return was **not** used as a proof premise.

## P4-D01 — repaired, independently verified

Protected `07_ATLAS_AND_RELATION_SCHEMA.md` (protected blob `f5e322b675b10fc83dfc8fa85f5a054873230694`) enumerates precisely 23 permitted relation types. Exact R4 `DATA/RELATIONS.tsv` blob `c081eb73e7bd9523f0699769fedc68de2dafe7c0` and R5 blob `c863a906382ee4bfa5d08b9d7c5f6ed7a055fa38` both have 8,503 unique relation PKs, 12 columns, zero width failures and identical row order. **4,841** rows changed, and **only** `relation_type` changed on each; all from/to IDs, source/generation, conditions, evidence ID, grade, negative and comment bytes remained unchanged. No relation PK was added or removed.

The 4,841-row `RELATION_TYPE_MIGRATION_R5.tsv` (blob `e263c8664e7df65b8eb328a3e3132856c498881a`) has one unique PK and exact old/new types for each altered row, with the correct R4 author HEAD and relation-blob fingerprint. Independently reversing the type values reconstructs the **complete R4 relation blob text byte-for-byte**, not just matching counts. R5 has exactly 0 out-of-vocabulary types: `ASSIGNED_TO=2,000`, `REQUIRES_AUTHORITY=452`, `HELD_BY=5,974`, `ALIAS_OF=30`, `IF_CONDITION=40`, `MUST_DEPENDENCY=7`. The 33 ASTRA dependencies still split into 7 literal MUST and 26 literal IF; the 14 functional dependencies retain 12 `FUNCTIONAL_OR_CONSUMES` and two `FUNCTIONAL_IF` qualifiers in preserved condition/grade fields, not falsely represented as ASTRA node DAG; 35 observed/reported edges remain source-graded assignments. All 82 seam predicate/negative literals are preserved.

**D01 receiving result: `PASS_REPAIRED_S0_S1_RELATION_SCHEMA`, strictly documentary.** `ASSIGNED_TO`, `HELD_BY` and `IF_CONDITION` are coarse carriers here: the unchanged grade, condition and comment must remain available to downstream readers; these are not affirmative execution, direct consumer or whole-product dependencies.

## P4-D02 — substantial improvement, one blocking schema defect

R4 and R5 `DATA/FUNCTION_ATLAS.tsv` blobs `98df0d9642a3c3f5fa1ecbf7a9cf7251e32b9fa0` and `b6d9ecd62a1080eb9a27e91581a129facec626d3` each have 1,740 unique PKs and 18 columns. Exactly **73** inherited identities changed (44 `LMX-001`–`LMX-044` plus all 29 `F01_QIDENTITY`–`F29_DIAGNOSTIC`), each in only four fields: `pyat_owner_ids`, `completeness_grade`, `disposition`, `next_step`. The other 1,667 atlas rows and all immutable historical/source identity fields are byte-invariant. Neither frozen inherited seed file was modified.

The 73-row `SEED_CURRENT_DISPOSITIONS_R5.tsv` (blob `6ebee656c48628451943697c9649b9af88f03365`) is genuinely useful: 73/73 exact baseline source locators and historical grades/debts matched the frozen `LMX44_SEED.tsv` and `LEGACY_F29_SEED.tsv`; 73/73 proposed finding→seed candidate relations point to the correct seed and real matching `DATA/EVIDENCE.tsv` PK, with `EXACT_LABEL_MATCH__NO_EQUIVALENCE` grade; 73/73 have finite seed-named action/falsifier text. Present owner is explicitly `NOT_RECEIVED`, current successor and rule/refusal proofs remain `NO_PROOF`, actual non-test first reader remains `UNRESOLVED`. These are *not* 73 demonstrated lost functions or 73 demonstrated successors. The two owner-route phrases are proposals only, not adopted Pyat IDs.

**Remaining blocker — R2-D05 (`P4-D02` residual): illegal canonical `disposition` vocabulary on all 73 records.** Protected `04_EVIDENCE_AND_STATUS_LAW.md` (protected blob `971a182a7ff7be3d1f188009d09ff5b829dadfc9`) requires one of its ten explicit VMESTYE functional conservation statuses per row at a cut, including `OPEN_PROOF_GAP`; for final inherited Long Memory legal judgments it separately requires the six exact Authority39 classes. R5 put **six non-enumerated composite historical/current labels** in `DATA/FUNCTION_ATLAS.disposition`, covering **all 73** identities:

| Submitted noncanonical status | Records |
| --- | ---: |
| `HISTORICAL_PRESERVATION_DOCUMENTED__CURRENT_SUCCESSOR_PROOF_OPEN` | 30 |
| `INHERITED_REQUIRED_CAPABILITY__CURRENT_SUCCESSOR_PROOF_OPEN` | 8 |
| `HISTORICAL_BOUNDED_STATUS__CURRENT_SUCCESSOR_PROOF_OPEN` | 5 |
| `HISTORICAL_MECHANISM_RETIRED__FUNCTIONAL_CONCERN_CURRENT_PROOF_OPEN` | 1 |
| `HISTORICAL_SELECTION_RECORDED__CURRENT_SELECTION_EFFECT_PROOF_OPEN` | 9 |
| `HISTORICAL_UNSELECTED_OR_STATIC_ONLY__CURRENT_FUNCTION_PROOF_OPEN` | 20 |

Each is intelligible as **historical qualification** and explicitly remains proof-open; none is a permitted canonical terminal status. The author validator tests for the substrings `CURRENT_` and `OPEN` rather than membership in the protected functional-status vocabulary; therefore its 12/12 hostile mutation result does not establish this law. My independent baseline strict-status membership test fails `NONCANONICAL_DISPOSITION_73`. This is a real machine-consumer classification ambiguity, not merely typography: canonical status readers expecting `OPEN_PROOF_GAP` cannot reliably classify the new strings.

**Bounded author correction:** set the 73 canonical comparative `disposition` values to `OPEN_PROOF_GAP` at the R5 exact semantic ceiling; retain the six detailed historical qualification labels in the separate ledger (e.g. a `historical_qualification` field or existing human-facing fate field), and keep the per-seed proof/negative/owner-falsifier evidence. Change the author validator to enforce exact protected functional status membership and add a negative control that rejects an unfamiliar `*__OPEN` pseudo-status. For any eventual accepted Long Memory terminal legal disposition, the competent issuer must use Authority39's six exact classes; this review does not issue those judgments. Independent P4 must recheck the resulting immutable author HEAD.

Actual current owner **receipt** is still unreceived for all 73; that is honest and separately blocked under P4-D03, not license to invent a Pyat owner. A proposed route is useful for the finite queue but not owner acceptance. P4-D02 cannot be marked finally accepted while its canonical statuses fail protected law.

## Independent hostile checks and limits

An independent in-memory baseline check passed counts, unique PKs, widths, exact R4→R5 field conservation, migration relation PK/provenance/inversion, seed ID/source/legacy status, candidate relation/evidence-grade joins, 1,667 unchanged non-seed rows, and proof-negative/owner sentinels. **18/18 separate intentional false-ready mutations were rejected**, including illegal relation type, MUST↔IF flips, deleted IF condition or negative, missing/duplicate/forged migration, missing seed, forged source/current proof/owner/evidence, promoted label grade, tampered frozen seed, changed nonseed atlas row, invented first reader, and removed evidence PK. The separate **strict protected disposition law** fails on the unmutated R5 baseline (73/73). These checks do not run project CI, source execution, fixture tests or original/native actor paths; they do not imply successful behavioral proof. Details: `R2_R5_HOSTILE_CHECKS.tsv`.

The R4→R5 diff modifies no `OPERATION_TRACES`, `CONSUMER_EDGES`, `AUTHORITY_APPLICATIONS`, `IMPLEMENTATIONS`, `DECISION_EVENTS`, source seam corpus, 6,125 P0 dispositions, 1,536 conflicts, 2,607 observations or 884 reciprocal decision events. R1 negative receiving remains valid: all 332 current first readers unproved, no observed authority application/refusal among 370, 90 stage-evidence holes, 49 different-cut GAP aliases, 48 Sorok index-only source bodies, historical F06/F11 and FIABC 144 PASS/3 FAIL, and native original35/source/science/actor/consent evidence held. The 3,449 GitHub branch-ref name/head census was **not** a complete semantic estate countersearch; P4-D04 remains HOLD. All 884 owner reciprocal decisions remain NOT_REQUESTED_NOT_RECEIVED; P4-D03 remains HOLD. No further estate content search was asserted in this targeted R5 delta review.

## Receiving decision

**`REVISE`** at exact ZL-15 R5 `cc21762ac3c7b49e389835b669a578d48caa1fc4`: P4-D01 repaired and independently received; P4-D02 fact/source/finite-proof improvement affirmed but strict comparative status law still fails for 73 seeds. Send the one bounded `disposition`-enum correction back to the existing author PR #864; no campaign restart, no new author branch necessary. Keep the independent P4 reviewer PR #868 review-only and draft until a corrected author HEAD is returned. All finite-estate, Pyat/Sorok/Long Memory reciprocal, source/native, scientific and consent gates are separately held; **no protected PRE-MAIN write or merge authorized**.

Terminal: `ZLP4R_R2_REVISE_73_STATUS_ENUM__D01_S0S1_PASS__ESTATE_OWNER_NATIVE_HOLD__NO_MERGE`.
