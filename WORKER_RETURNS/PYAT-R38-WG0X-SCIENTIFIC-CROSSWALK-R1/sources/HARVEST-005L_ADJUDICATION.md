# HARVEST-005L Adjudication — Local Question-Identity Carrier Delta

Status: `ADJUDICATED__LOCAL_DELTA_VALID__30_UNSEEN_IDENTITIES__P2_IDENTITY_ARCHITECTURE_RECOVERED__H005B_BROWSER_COURT_ENABLED`

Packet SHA-256: `17854e15e32028c7f782c20abd375dc557419fff8f47770749f283fd7b6fafc5`
Packet size: `10,510,567` bytes
Starting/checkout HEAD: `fa441632bab1f98c98c0383f78f4bfefe9013c7c`

## Integrity

Browser inspected the actual uploaded ZIP and independently verified:

- exact outer SHA-256 and byte size;
- ZIP integrity;
- all `38/38` internal checksum entries;
- 96 responsive physical occurrences;
- 37 distinct content identities;
- 30 Browser-unseen identities returned as exact bytes;
- 22 local-only identity surfaces;
- no cross-carrier computation and no source/authority mutation by the local worker.

The local worker obeyed the H005 split contract: Browser-held identical bytes were not needlessly repackaged, and H005B relational synthesis remained a Browser responsibility.

## High-value returned identity surfaces

H005L recovered exact bytes for identity-bearing surfaces including:

- final FQRA / QSM relation authority (`QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv`, 18,518 rows);
- `qsm_raw.csv` and `qsm_provenance.csv` (18,763 rows each before current-35 filtering);
- QSMv2 integrated 4,438-implementation / 3,196-unit authority ledgers;
- current and historical `questions_master.csv` variants;
- relation registries;
- all nine R14 codebook-scope indexes;
- semantic/driver index variants;
- `P2_Question_Node_Identity_and_Population_Contract_v1.json` SHA `6375b81e0c965bcbd46845a7eb8fabdab580fc3296b3c45729b20998c9c7a40a`.

## P2 identity architecture recovered

The returned P2 contract is not an isolated design sketch. Library lineage independently places it in the frozen P1.5 -> P2 architecture and records P2 as the governed 35-wave question-node population stage.

The recovered law distinguishes:

- `question_concept` — semantic meaning across one or more implementations;
- `question_implementation` — one exact source-family + wave + material instrument scope + source-variable implementation;
- `response_binding` — accepted response authority bound to an implementation;
- `source_structure` — source-native grouping/structure observed in one wave/instrument scope.

Source-variable identity is case-preserving; lowercasing is a search aid only. P2 population is defined from original/canonical codebooks plus accepted question/response authority; smoke selections, QSM heuristics, embeddings and diagnostics cannot define membership.

This is exactly the noncollapse identity separation that H004 independently proved is required.

## Existing Phase-0 population recovered from Library

Browser located and hash-verified the existing P2 Phase-0 skeleton:

- `Rawlsing_P2_Phase0_Question_Node_Skeleton_v1.csv`
- SHA-256 `d38301588fae27c66f6b8627c5007fb0d8ed4ac3d7eb25f32c74228c367b86b6`
- 18,276 rows / 17 columns;
- 18,276 unique `question_implementation_id` values;
- 18,276 unique `exact_identity_sha256` values;
- 35 active waves / 9 survey families.

The contemporaneous Phase-0 report records 12/12 validation PASS and explicitly states that the release is a shallow source/question implementation skeleton rather than a source-complete semantic/J-family release.

## H005B consequence

H005B must therefore test and reconcile existing identity authority, not invent a fresh question UID from helper masters.

The exact row-level candidate population is the recovered content-addressed P2 skeleton unless later higher-precedence R14/source-native evidence positively changes a member. Later QSR/semantic/driver/FQRA rows are projections, authority assertions, helper representations or crosswalk debt around that population; their presence alone does not create new question implementations.

Disposition:

`H005L_COMPLETE__BROWSER_H005B_RELATIONAL_AND_PRECEDENCE_COURT_ACTIVE`
