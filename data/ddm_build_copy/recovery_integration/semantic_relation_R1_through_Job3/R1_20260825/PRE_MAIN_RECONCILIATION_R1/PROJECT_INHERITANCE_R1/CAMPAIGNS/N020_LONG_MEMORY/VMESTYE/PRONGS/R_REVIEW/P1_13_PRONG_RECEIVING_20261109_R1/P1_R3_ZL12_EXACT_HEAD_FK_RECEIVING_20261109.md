# VMESTYE #813 / ZL-12 — independent R3 exact-head foreign-key receiving

**Verdict:** `ACCEPT_AT_SCOPE__ZL12_R3_159_CENSUS_FK_REPAIR__DOCUMENTARY_ONLY`.

**Reviewed author PR:** [#850](https://github.com/maidiu/rawlsing/pull/850), exact head `bd278fd35693230929cbcc66a017efa403b70e83`. **Reviewed parent:** `0455b5e8d0b60f60d4d9013d84ced3ba4a7c6105`. GitHub compare shows one fast-forward descendant commit, **exactly three changed files** within the pre-existing `G_PROGRAMMA` author lease: `COVERAGE.tsv`, `EVIDENCE.tsv`, `UNJOINS.tsv`. Existing PR remains draft and unmerged. Reviewer operates on separate #859 branch; no author/protected/DATA edits.

## Exact independent comparison

The source bytes of both versions of all three TSVs were retrieved at their immutable Git blob hashes; the `EVIDENCE.tsv` bodies were fetched via Git-blob API because GitHub's normal contents wrapper yielded an empty string for this large UTF-8 file. The accepted frozen P0 census blob `65c1bbe4a602341c5caacca2d58dced31a23f382` was decoded directly (**6,125 records, 25 columns**). The frozen `VMESTYE_P1_PRONG_TABLES_V1` contract was separately read from `CONTROL/P0_SCHEMA_AND_LEASES.md`, and every remaining named P0 ID was compared against estate/source-cut/path/composite/grain, with source blob and row locator checked for evidence.

| File | Original rows / resulting rows | Exact field-level delta | New `UNRESOLVED` count | Other field deltas |
| --- | ---: | ---: | ---: | ---: |
| `COVERAGE.tsv` | 1,255 / 1,255 | 49 `census_id` -> `UNRESOLVED` | 49 | **0** |
| `EVIDENCE.tsv` | 1,265 / 1,265 | 51 `census_id` -> `UNRESOLVED` | 59 (8 were already unresolved) | **0** |
| `UNJOINS.tsv` | 59 / 59 | 59 `census_id` -> `UNRESOLVED` | 59 | **0** |
| **Total changed cells** | | **159/159, no extras** | | **0** |

All three headers are byte-for-byte identical to their parent; all rows have legal header widths and unique local primary IDs. No source-body, negative, authority, role or reader field was altered. Among the remaining non-UNRESOLVED IDs, **1,206 exact P0 five-tuple joins in COVERAGE and 1,206 in EVIDENCE** verified with zero mismatches; source blobs and row locators were also equal in those EVIDENCE rows. `EVIDENCE` frozen claim/evidence/proof enums contain zero invalid values.

The 49 `U-P0-CUT-001..049` same-blob/different-commit records each have a **unique** `attempted_target_id=ZL01-...` that is present in accepted P0. Cold crosscheck for each of 49: identical original path, JSON-array source composite, grain, row locator and source Git blob between P0 and current evidence, **distinct actual source commit** preserved; corresponding `COVERAGE` and `EVIDENCE` source keys are both now `UNRESOLVED`; the `UNJOINS` row still carries the exact attempted P0 target, same-blob alias explanation, `CENSUS` join type, `OWNER_HELD`, `negative_preserved=YES`, unresolved question and falsifier. **49/49 invariants pass**. The other ten original downstream `UNJOINS` also remain `OWNER_HELD`, with source-native/first-reader and two SR01 aggregate classifier evidence questions explicitly held. The two SR01 classifier evidence records remain represented; neither is converted into a fictional single P0 row.

## Grade, exclusion and receiving gate

This proves the scoped **documentary foreign-key repair** against the frozen V1 contract at this exact immutable PR #850 head. It **does not** independently qualify historical PROGRAMMA/Sorok meaning-operation succession, 82 conditional seam predicates, source-issuer-selected rule application, native original35 testing, source/science/actor permission, actual first non-test consumer, Sorok E001, or N11 original35 position acceptance. S2 repository execution and S3 original native remain **NOT_RUN**.

**Disposition:** ZL-12 #850 R2-D09 documentary foreign-key obstruction **CLOSED_AT_SCOPE**. Combined with the prior R2 documentary V1 correction and source-grade identity caveats, this prong is receivable by #813 as **`ACCEPT_SCOPED_P1_DOCUMENTARY_EVIDENCE__SEMANTIC_NATIVE_HELD`**. This is **not `ACCEPT_P1_PRONG_EVIDENCE` for the collective 13-prong court** and does **not** authorize ZL-15 #814, any protected PRE-MAIN merge, original survey/source use, or functional zero-loss certification. Previously identified independent per-prong receiving gaps remain separate, not re-created by this repair.

**Independence limitation:** this is a distinct receiving conversation/branch from the author correction, using read-only GitHub source observations, but the same linked GitHub account and connector do not establish a separately attested human/model/host review identity. No native test provenance is claimed.
