# VMESTYE #813 — R2 exact-head re-receiving after the three author repairs

**Reviewer:** existing #813 P1R receiving context, separate from the ZL-09/11/12 author branches. **Source:** accepted P0 census blob `65c1bbe4a602341c5caacca2d58dced31a23f382` (6,125 rows, 25 columns). **Run surface:** authenticated GitHub immutable source and byte/field comparisons via connector + JavaScript; S2 repository-local, original respondent/native S3 and scientific/actor review **NOT_RUN**. No protected writes, mergers, or DATA normalization.

**Previously reviewed heads:** ZL-09 PR858 `1065eed3a4dbe5230f36db4138bd011fb3c6867d`; ZL-11 PR845 `2b49e692b9fc01974b462b9bba131b5653e72c2d`; ZL-12 PR850 `d02ec5d9ede9f16645d44f65f396c72c382b8ecc`.

## 1. Scope-specific dispositions

| Prong | New author head / exact comparison | Independent R2 result |
| --- | --- | --- |
| ZL-09 #858 | `24313ea4271472b007ab986f26392464e7d4ec07`, one descendant commit, exactly AUTHORITY_USE and COVERAGE | **PASS bounded V1 correction.** All 63 authority enum changes and 140 coverage-presence changes checked against old rows; 42 explanation cells retain the original qualifier. All revised legal, same headers/widths/counts. 35/35 historic P0 joins and 77 rights/non-test-reader/operation UNJOINS remain separately open. |
| ZL-11 #845 | `d29d092ef04ae3882c4db7b1f1dcc710159b36c5`, one descendant commit, UNJOINS only | **PASS bounded V1 correction.** Exactly 87 failure_code and 87 status cells changed; no other fields changed. Legal values `OTHER_TYPED` and `OPEN`; 106/106 original unresolved identities survive, including 19 source/authority cases and original 87 supplemental non-P0 source-grain distinctions. |
| ZL-12 #850 | `0455b5e8d0b60f60d4d9013d84ced3ba4a7c6105`, one descendant commit, six files | **PARTIAL PASS / REVISE exact census FK.** 1,265 EVIDENCE records and 1,255 COVERAGE records now have legal V1 enums. All 1,255 source composites use the literal P0 JSON-array representation and P0 locators; 300 source-grain discrepancies eliminated. **1,206/1,255 five-tuple joins exact**, with 49 same-blob/path/key records intentionally still at a different source commit and now explicitly `UNJOINED`. 49 typed cut-identity UNJOINS added, total 59 UNJOINS; no native/authority first-reader proof is manufactured. **Remaining failure below.** |

GitHub compare confirmed each new head descends from its reviewed parent by **one** commit. All modified files stay inside the original respective author lease. The three repairs do not change actual original35 source rights, source-scoped selection/application/refusal, native evidence or first non-test consumer proof.

## 2. New exact foreign-key blocker — ZL-12 R2-D09

The frozen `VMESTYE_P1_PRONG_TABLES_V1` (P0_SCHEMA_AND_LEASES §3B) states that a `census_id` must resolve to a **literal exact P0 five-tuple** or be `UNRESOLVED` with a typed `UNJOINS` attempt. A path/blob/key match under another pinned commit is not a literal source-tuple foreign key. This requirement was the reason for accepting typed alternate-cut UNJOINS rather than inventing full equivalence.

At #850 `0455b5e8...`, direct comparison to the accepted census establishes:

- **1,206 exact** `EVIDENCE` and `COVERAGE` five-tuples, including identical estate, immutable source commit, path, JSON-array composite, and record_grain. All cited original row locators also match; no conflicting source blob was observed.
- **49 GAP entries** preserve a different source commit, `9253064bc9423a0f0ccda4fbdea43c2f54f800c6` versus P0 `7a5429ffbc48efd25e28c912da80c822e66bc182`. Their `COVERAGE` status is correctly `UNJOINED` and 49 `UNJOINS` carry explicit `attempted_target_id=ZL01-...`, but the **COVERAGE, EVIDENCE, and UNJOINS `census_id` fields still contain that nonmatching ZL01 target**. That is **147** mismatched foreign-key cells, not 49 source losses.
- The other **10 UNJOINS** for 2 aggregate SR01 classifier carriers and 8 current code methods still carry descriptive `census_id` sentinels instead of `UNRESOLVED`. The corresponding two classifier `EVIDENCE` rows do likewise; eight code-evidence rows already use `UNRESOLVED`. **12** more invalid census-key cells.
- Therefore **159 census_id cells need normalization**: 49×3 different-commit source aliases, 10 noncensus UNJOINS, 2 noncensus EVIDENCE. This remains an **exact FK contract failure**, even though every substantive authority/negative distinction has a separate source-aware explanation. No other literal five-tuple mismatch found among the 1,206 exact rows, and no V1 enum violations remain in the six governed tables checked.

**Minimal author correction (same PR #850, no new schema or investigation):** change those **159 `census_id` fields** to literal `UNRESOLVED`; preserve each `U-P0-CUT-001..049` `attempted_target_id=ZL01-...`, original source commit/blob/row, `candidate_aliases`, `falsifier`, and `OWNER_HELD`. Preserve aggregate classifier counts 2,416 Pyat / 1,314 Sorok in narrative source evidence, not as a single fabricated P0 census key. Keep **1,206 exact joins, 49 cut-alias holds, 59 UNJOINS**. Change no source/authority/semantic conclusion. New immutable head and cold source-table comparison of these 159 cells required.

## 3. Gate

**Verdict at this R2 cut: `ZL09_BOUNDED_V1_PASS; ZL11_BOUNDED_V1_PASS; ZL12_REVISE_FK_D09; COLLECTIVE_P1_NOT_ACCEPTED; ZL15_HELD`.** This court tests documentary presence and provenance, not current-machine zero-loss, original35, Sorok actor or qualified science. The #859 R1 matrix remains immutable as the history of the previously reviewed heads; this file is the chronological R2 addendum.

The remaining P1 review obligations for ZL-02/04/10/13/14 and the semantic/first-reader anti-joins are not erased by these three repairs. They may be adjudicated at honest documentary scope, with native/issuer/actor edges explicitly held. Only the exact subsequent P1 receiving decision can release #814.
