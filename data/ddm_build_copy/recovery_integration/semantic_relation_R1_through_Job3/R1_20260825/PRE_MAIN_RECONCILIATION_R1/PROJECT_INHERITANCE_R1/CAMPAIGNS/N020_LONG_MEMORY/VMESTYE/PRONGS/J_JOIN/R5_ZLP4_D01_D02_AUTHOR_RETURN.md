# ZL-15 R5 — targeted P4-D01 / P4-D02 author repair

**State:** `AUTHOR_R5_DOCUMENTARY_CORRECTION_SUBMITTED__FRESH_P4_REVIEW_REQUIRED__NO_MERGE`. Existing ZL-15 draft [PR #864](https://github.com/maidiu/rawlsing/pull/864); reviewed immutable R4 `d10602355c77564b2b6d50601ebba4fed4ac7d58`; independent final P4 [PR #868](https://github.com/maidiu/rawlsing/pull/868), [#817 verdict](https://github.com/maidiu/rawlsing/issues/817#issuecomment-6751420923) `REVISE`. Protected source at startup `256d46bf425cc37e114465cddbe3c60e535766ab`. New R5 author HEAD must be taken from the actual PR branch after the CAS write, not self-embedded into its own file.

## Exactly two corrections

**P4-D01:** `DATA/RELATIONS.tsv` now has 8,503 rows, all within 23 protected relation types. The 4,841 exceptional R4 types are normalized in a reversible 4,841-key ledger, without any source/target, grade, predicate, negative, evidence, source-cut or comment mutation. ASTRA keeps 7 MUST and 26 IF; observed/functional dependences are not promoted to unconditional production or native execution. See `RELATION_TYPE_NORMALIZATION_R5.md` and `RELATION_TYPE_MIGRATION_R5.tsv`.

**P4-D02:** `DATA/FUNCTION_ATLAS.tsv` now explicitly classifies each of 44 LMX and 29 C6-F inherited seed identities with source-qualified historical state versus current unproved functional state, a source-evidenced matching finding and finite owner/falsifier in `SEED_CURRENT_DISPOSITIONS_R5.tsv`. 73/73 exact seed ID→existing label-only candidate→real evidence links verified, with immutable source identity fields unchanged. This is **not** claim of 73 new lost functions; Pyat and Long Memory owner receiving remains `NOT_RECEIVED`.

## Deterministic R5 S0–S1 in-memory court (author, not independent)

- R4 source relation/atlas blobs pinned as `c081eb73e7bd9523f0699769fedc68de2dafe7c0` / `98df0d9642a3c3f5fa1ecbf7a9cf7251e32b9fa0`.
- Full 8,503-row PK-by-PK relation check: all original non-type fields byte-identical, all 4,841 migration PKs uniquely reversible, 11 old exceptional kinds accounted, 0 forbidden types, 7 MUST and 26 IF conserved.
- Full 1,740-row atlas check: unchanged IDs, unchanged 1,667 nonseed rows; exactly 44+29 changed seed current-view rows, immutable original seed fields unchanged.
- All 73 exact candidate relation IDs, documentary evidence IDs and original source locators resolved; every current successor, actual reader, actual rule effect and refusal remains open/unproved.
- **12/12 hostile in-memory mutations were rejected:** illegal type, IF→MUST, MUST→IF, ledger omission, forged original type, negation promotion, lost conditional predicate, false current successor, fake owner receipt, deleted seed fate, forged evidence, original source mutation.
- Test source `VALIDATE_ZL15_R5.js` reproduces the court on a checkout with full Git history, loading original R4 tables by `git show`, validating their immutable Git blob hashes, and checking R5 files. The *pure verifier and hostile cases* were exercised against actual pinned GitHub blob text in this author session; the Node CLI wrapper/project CI, host-native S2, native S3, and original35 respondent/actor execution **were not run**.

## Preserved scope / expressly NOT repaired

P1 received corpus, 13 prongs, R2/R3/R4 historical records, #815/#816 previously accepted **R4 only**, historical F03/F08 guard distinction, 82 conditional seams, 4,420 stages (including 90 unresolved evidence holes), 332 unresolved actual first readers, 370 authority rows with 0 applied-rule YES / 0 enforced-refusal YES, 884 unreceived reciprocal decision events, 1,536 conflicts, 49 different-cut GAP aliases, 48 Sorok index-only bodies, 3,449 branch names/heads uninspected, finite estate-stop and cross-owner admission, F06/F11, historical FIABC 144 PASS / 3 FAIL, S2/S3/native source selection, science/source/actor/consent, original35 whole run and machine-zero-loss **all remain separately held**.

**Mandatory route:** exact new PR #864 R5 HEAD to a truly independent #817 P4 re-review of D01/D02. No inherited P3 acceptance for changed bytes, no owner adoption, no protected update/merge by this author. Verdict remains `REVISE` until independently re-adjudicated.
