# C8 focused correction check — commands and evidence

**Scope:** mechanical confirmation of C8-001/002/003 only. No new whole-machine/schema court, no test replay, no source/native/S3/respondent/SAV/DTA/DB execution, no fan-in/protected/production write.

## Exact current cut and provenance

```sh
git rev-parse 55fca441d1c674c256473c264cabda48f2df0e52
# 55fca441d1c674c256473c264cabda48f2df0e52
git show --format='%H%n%P%n%s' --no-patch 55fca441d1c674c256473c264cabda48f2df0e52
# 55fca441... / parent c61f6368d5326c535930731743475518dcf20db9 / PYAT777 fix C8 derived taxonomy and exact lane lineage defects
git ls-remote origin refs/heads/agent/pyat-hq-pre-forge-to-prev3-authority-severance-functional-adequacy-20261107-r1
# 55fca441d1c674c256473c264cabda48f2df0e52
```

Current corrected cut `55fca`; prior exact target metadata `4ded573400ddc8cfa05d38374a1c7206e440f7f7`, content `5efb9fa33aa26e0cfb6bc7a03270e4c896411843`; prior content `ad4fe3c9cd67eed5bc79644bb399a7090846a8fe`; C7 `605e1cb67156a09f9ce4c0990e572fa3fda1fdd1`; prior C8 `356124ee452d8cababaae7f2f57d05e8f0d17deb`. The worktree fan-in files are the prior `4ded` cut; every current artifact was read with `git show 55fca441...:<path>`.

## Correction commit scope

```sh
git diff --name-status c61f6368d5326c535930731743475518dcf20db9 55fca441d1c674c256473c264cabda48f2df0e52
```

Only eight named mechanical files changed:

```text
M 02_CURRENT_IMPLEMENTATIONS_PRE_FORGE_VS_WHOLE_PREV3.tsv
M 03_BIDIRECTIONAL_AUTHORITY_REQUIREMENT_AND_CONSUMPTION.jsonl
M 03_BIDIRECTIONAL_FUNCTION_AUTHORITY_CASES.jsonl
M 06_REAL_LOCAL_TEST_COMMANDS_OUTPUT_HASHES_AND_MUTATIONS.md
M 09_INDEPENDENT_REVIEW_REQUEST_AND_EXACT_HEAD.md
M 11_C7_CORRECTION_AND_CLOSURE.md
A 12_C8_REPORTING_CORRECTION.md
M CHECKPOINT.json
```

No test, source, production, protected, C1–C7 evidence, commission or launch file changed in the correction commit. The broader `4ded..55fca` diff includes earlier HQ bookkeeping and the integrated prior C8 review files; that is not the correction commit.

## C8-001 / C8-002: 02 taxonomy synchronization

`git show 55fca...:02...` parsed as 149-row TSV (20 columns) and compared field-by-field with `git show 4ded...:02...`:

```text
02 rows old/new: 149 / 149
row types unchanged: CASE 51, FF_REGISTER 26, FF_DEPENDENCY 16,
  POST_FF_REGISTER 15, POST_FF_SEAM 11, 748_CURRENT_OWNER 30
changed rows: 26 (5 SOURCE_SHA + 23 EVIDENCE_GRADE; 2 rows in both categories)
old EVIDENCE_GRADE: FUNCTION_CURRENT 24, HISTORICAL_ONLY 19,
  IMPLEMENTATION_NOT_CURRENTLY_ADEQUATE 1, NOT_RUN 7
new EVIDENCE_GRADE: FUNCTION_CURRENT 21, NOT_RUN 30, HISTORICAL_ONLY 0,
  IMPLEMENTATION_NOT_CURRENTLY_ADEQUATE 0
```

All 51 `02` CASE `EVIDENCE_GRADE` values equal the canonical `03` `frozen_taxonomy_verdict`; zero mismatches. The 23 changed cases are C2-J02; C3-FF-04; C3-FF-05; C3-FF-06; C4-J02; C6-F03_QREL; C6-F05_RESP_OPTION; C6-F07_OVERLAY; C6-F08_Q_USE; C6-F13_V550_BRIDGE; C6-F14_V551_ATOMS; C6-F15_V551_COND; C6-F16_V552_STRUCT; C6-F18_J_PREPARED; C6-F19_J_PATTERN; C6-F20_J_PACKET; C6-F21_J_STRUCT; C6-F22_R3_REL; C6-F23_R3_NEG; C6-F25_LIFECYCLE; C6-F26_CACHE; C6-F27_DB_SOURCE; C6-F29_DIAGNOSTIC.

Specific checks:

```text
C3-FF-04 02 EVIDENCE_GRADE=NOT_RUN; CURRENT_STATUS=UNMERGED_TEST_ONLY_CANDIDATE__NO_SELECTED_NON_TEST_DEMAND__NO_DEFECT_PROVED; 03 tax=NOT_RUN
C6-F03_QREL 02/03=NOT_RUN
C6-F05_RESP_OPTION 02/03=NOT_RUN
C6-F08_Q_USE 02/03=NOT_RUN
03 taxonomy: FUNCTION_CURRENT 21, NOT_RUN 30
03/02/05 unique IDs 51/51/51; 03 IDs present in 05: 51; 05 unique: 51
```

GF1 remains `gf1_status=CANDIDATE_EXISTS__PR_691_UNMERGED__NOT_RUNTIME_SELECTED__NO_DEFECT_PROVED`; no new defect/merge/reimplementation. The 19 historical-only cases are `NOT_RUN`; the three retyped C6 labels are `NOT_RUN`.

## C8-003: exact cuts and 03 integrity

`git show 55fca...:03...` vs `git show 4ded...:03...` parsed as JSONL:

```text
03 rows old/new: 51 / 51; IDs 51 / 51; only changed records: C4-J01, C4-J02
changed field: source_cut 0d548b03... -> 950ff275527a2963253336cbb05924a6c2943cd8
all A-J payloads, case_id, source_cut for C1/C2/C3/C5/C6, review_cut,
stable_legacy_ids, register_ids, unmatched_ids and all other fields unchanged
03 canonical/alias byte-equal: true
new SHA-256 both: cc4275628286f31ba3695d92910f52d639a3f2d54ca7d43852bbd9d12b614251
```

Cut checks at `55fca`:

```text
02 CASE SOURCE_SHA:
  C1 79c4f33c51e7d0146e06e12cac6ea903c79cb7b0
  C2 b132fa4a02b31ba539b33f24ad022846bb81acb8
  C4 950ff275527a2963253336cbb05924a6c2943cd8
  C5/C6 remain their valid source-observation cuts; no promotion
06 line 12 C4: 950ff275527a2963253336cbb05924a6c2943cd8
09 lines 61/62/64: C1 79c4f33; C2 b132fa4; C4 950ff275
03 C4-J01/C4-J02 source_cut: 950ff275
CHECKPOINT.source_cuts: C1 79c4f33; C2 b132fa4; C3 3fd285d6;
  C4 950ff275; C5 451f8d1e; C6 0d548b03
06/09/CHECKPOINT C5/C6 integration heads retained: 451f8d1e/0d548b03
```

03 hash references in `09` (C7-005), `11` (C7-005 and table 03 rows) and `CHECKPOINT.canonical_03` are `cc427...`; synchronized. The review has not re-audited the prior C8 PASS gates.

## Residual C8-003 reference/provenance defect

The `11` "Corrected artifact SHA-256" table still has pre-C8 rows at lines 138/143/146/148:

```text
02  table 4a16e86c57063fe02f9074ec6e07296feca5d4ee830b5b75036c109153c66e6b
    actual 64e9dc9d98c9e1c77332bf54dd0c8d002f3ad5f5fbe4f9b0e270e54b507e97a2
06  table 5be23983c960ba74952789cac2999ee6ccb78d0498157f2d2416956da7446c4c
    actual 45c1951015c57f235143d440ab50d1819e14c51001cc158e7c5f783cba0ff1f8
09  table 83bb4320cd9546a3f1c05fe00eb1b18a3d8b51135c6bbb2e98820087b23113ba
    actual 2a4469e75c3ff9c0e92143e953613129e1474a0928c23e72efd5bce140aa108b
CHECKPOINT table 5767fc529ab428522cbfe8eae18512a7f12ce2260ea5c29c53c2a6ac344b5e2a
    actual b4f7af4855a08455d4e4c5b72d85deb5823dfcd9189f9fbf077c3c9af69f7f3f
```

The 00/01/04/05/07/08/10 rows in the same table match their actual files; only the four corrected-file rows are stale. The table's 03 rows are `cc427...`.

`CHECKPOINT.json` at `55fca`:

```text
line 5 exact_output_head = 5efb9fa33aa26e0cfb6bc7a03270e4c896411843 (prior target)
line 261 final_independent_review.corrected_content_head = 5efb9fa... (prior target)
c8_correction: canonical_alias_sha256=cc427..., counts/cuts present,
  no corrected_content_head/correction_commit for 55fca
branch_head_note: says later bookkeeping does not alter reviewed fanin;
  the 55fca commit is a content correction, not only bookkeeping
```

The exact current correction cut `55fca` is therefore reported here by the reviewer, but is not recorded in the artifact's current-cut provenance. This is a mechanical reference-synchronization residual; no source/semantic/native decision is involved.

## Preserved limits and non-claims

- `07` remains 17 A01–A17 open gates; `00`/`04`/`05`/`07`/`08`/`10` unchanged from `4ded`; source/native/protected limits unchanged.
- 51 IDs preserved across `02`/`03`/`05`; 149 `02` rows; only two `03` source-cut fields changed; no A-J/IDs/review-cut/content promotion.
- Prior C8 review blobs at `55fca` are byte-identical to `356124ee` (00/01/02/03); preserved.
- No test replay/new archaeology/source court; no respondent/SAV/DTA/DB/source-byte copy/upload/S3/native/science/actor; no CI waiver/protected merge/generic FF live claim.
- Whole #777 remains incomplete; `goal_complete=false`. No new product acceptance or authority.
- Quota `UNKNOWN`; same provider/account/region/model/effort.
