# RESULT — RABOCHII 5 J01-A R2 Latinobarómetro / South Asia / LiTS Lane

## Disposition
**PASS at the available current-source ceiling.**

The exact current deep catalogs were recovered and hash-verified for all three assigned source families. The lane contains **536** current source structures, of which **242** are current J candidates. **65/65 frozen R1 rows** were re-courted exactly once: **64** are `R1_PRESERVED_EXACT` and **1** is `R1_PRESERVED_WITH_BINDING_CLOSURE`.

## Critical LiTS closure
LiTS III Q4.27 is source-real exactly as R1 said: q427a-q427f. R1 had incomplete/truncated current implementation binding. The exact current governed catalog now resolves all six member IDs, so the row is preserved semantically and closed at the binding layer rather than rewritten or deleted.

LiTS IV, absent from the frozen R1 lane, now has current-only source structures recovered from the official native questionnaire and exact current catalog. The lane also recovers R1-missed LiTS I/II/III relations from explicit source instructions and current parent relations.

The governing distinction was enforced throughout:

> **SOURCE-STRUCTURE EXISTENCE != EXACT CURRENT MEMBER BINDING**

Where a source-native relation exists but the current catalog does not expose item-level implementations (notably packed Latinobarómetro 2024 multiselects), the relation remains in `CURRENT_SOURCE_STRUCTURE_UNIVERSE_R2.csv` with an explicit incomplete-binding gap.

## Source ceiling / typed gaps
The lane does not counterfeit missing documents. Native bytes were not recovered for Latinobarómetro 2011/2024 codebooks, the South Asia W1 questionnaire, or the South Asia W2 codebook/questionnaire. Current canonical row authority and exact deep catalogs exist for those scopes, so admissible current structures remain preserved while the stronger native-document ceiling is recorded in `SOURCE_GAPS_R2.csv`.

LiTS IV contains several internal instruction-range inconsistencies (for example instructions naming wider letter ranges than the actually enumerated rows). The lane preserves the enumerated current source relation and records the inconsistency; it does not invent unseen members.

## Negative proof
No historical J carrier answer, historical expected count, C07-C10 semantic answer, historical V550J membership, historical P2 source-structure inventory content, sibling-worker output, J01-B work, neighboring-wave inference, or executable-J authorization was used. Accidental historical snippets/filenames encountered during broad retrieval are disclosed in `ANSWER_BLINDNESS_RECEIPT_R2.json` and were excluded from reasoning.

## Validation
`VALIDATION_R2.json`: **PASS**. Every bound current implementation ID resolves in the exact assigned family/wave catalog; the candidate carrier is an exact subset of the source carrier; jurisdiction contains only the nine assigned scopes.

## Lane token
`J01A_R2_LATIN_SOUTHASIA_LITS_LANE_COMPLETE_AT_AVAILABLE_CURRENT_SOURCE_CEILING`

This is a lane return only. It is not a global J freeze and does not authorize executable J.
## Exact large carrier identities
- `CURRENT_SOURCE_STRUCTURE_UNIVERSE_R2.csv`: Library `libfile_73f07c893360819198fab5af0b1e2a68`, 536 rows, 742633 bytes, SHA-256 `319806236b3ad05b6a3219e9338600ded8020aa2b0ef341e660aab3dd42a55da`.
- `CURRENT_J_CANDIDATE_UNIVERSE_R2.csv`: Library `libfile_3abb5ca1e1a08191b1825a8fc0737741`, 242 rows, 311626 bytes, SHA-256 `eeeed797c43df46544a11b450589dc7f346d85066892189f7c62a964688fb9ad`.

These are the exact carrier bytes validated by this lane; Git contains the binding metadata, not a substitute carrier.
