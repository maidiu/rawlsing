# REC-08 — C05-R2B Smallest Lawful Real Source/Release Candidate

Candidate source family: **LiTS I / LiTS-2006**

Candidate state: `SMALLEST_LAWFUL_REAL_SOURCE_CANDIDATE__SOURCE_SPECIFIC_RELEASE_NOT_YET_VALIDATED`

## Exact physical source identity

- source member: `LiTS_I.dta`
- Library transport named by the G-SR08 court: `LiTS_I.dta.zip`
- source SHA-256: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- transport SHA-256: `b2e90ee7ceefc230572e89687de28186544308949f8fd33c32b1d0ffb14b8feb`
- source bytes: `139531180`
- transport bytes: `7686379`
- rows: `29002`
- variables: `1198`
- exact frozen decoder used by the accepted continuation evidence: `decode_dta(source_path, encoding="latin1")`

Authority 82 accepts the exact physical execution facts for continuation purposes, including traversal of `34,744,396` physical cells and the exact physical replay frontier. It explicitly does **not** issue source certification.

## Why LiTS I is the smallest lawful candidate

REC-08 does not choose WVS7 merely because WVS7 is prominent or already stress-tested. LiTS I is a substantially smaller real survey source and already has a dedicated source-certification/recovery lineage, exact source identity, accepted LiTS-2006 semantic/structural authority inputs, hash-pinned response-option authority, and an HQ-defined path to a source-specific C11 release.

The remaining obstacle is semantic ownership, not physical transport: the questionnaire establishes distinct household reporter and selected-respondent roles within one source row. Authority 82 therefore forbids blindly projecting all 1,198 slots as one respondent's answers and requires the dedicated `GSR08R2_LITS1_C11_OWNERSHIP_AND_RESPONDENT_ROLE_BRIDGE` before local projection may resume.

## Candidate release definition

The later C05-R2B proving release must be one immutable, validated LiTS-I source-backed `C11LogicalRelease` built only after the GSR08R2 bridge is accepted and the source-specific `GovernedC11Projection` is mechanically constructed and validated.

For the proving scope, Authority 82 prefers **RAW / unweighted** unless a weight claim is positively needed. No default selection among `weight_0`, `weight_1`, and `weight_2` is authorized.

Therefore REC-08 selects LiTS I as the smallest lawful candidate **without pretending that a launchable release already exists**.
