# README FIRST — Rawlsing V550J Semantic Authority Convergence Audit R3

## What R3 is

R3 is the first post-retrieval correction package.

It supersedes R2 **only** where R3 explicitly corrects:

1. the authoritative 35-wave enumeration;
2. the source-integrity status of the identified R14/R15 candidate objects;
3. the semantic adjudication queue denominator.

All other R2 authority-fitness conclusions remain in force.

## Start here

Read in this order:

1. `R14_SOURCE_INTEGRITY_AND_SCOPE_CORRECTION_REPORT_R3.md`
2. `CODEX_DELTA_SCOPE_AND_R14_REPAIR_R3.md`
3. `output/CANONICAL_35_WAVE_SCOPE_R3.csv`
4. `output/R14_SOURCE_NATIVE_CANDIDATE_INTEGRITY_AUDIT_R3.csv`
5. `output/R14_SOURCE_NATIVE_CORRECTION_OVERLAY_PROPOSED_R3.csv`
6. `output/SEMANTIC_EDGE_ADJUDICATION_QUEUE_R3_SOURCE_INTEGRITY_GATED.csv`
7. `output/ASB_W4_NATIVE_SOURCE_INTEGRITY_EVIDENCE_R3.csv`
8. the enrichment/support ledgers in `output/`

Run:

```bash
python validate_r3.py
```

Expected:

```text
PASS: R3 scope and source-integrity gate validated
```

## Critical scope correction

The current `wave_authority_registry_35wave_v1.json` is the governing scope authority.

The canonical scope is exactly 35 waves. R3 explicitly corrects an erroneous earlier assistant-authored prose list. Do not use the old prose list to modify the repository.

The corrected family/wave list is serialized in `output/CANONICAL_35_WAVE_SCOPE_R3.csv`.

## Retrieval package

R3 consumed:

`Rawlsing_RETRIEVAL_PACKAGE_UNDER512MB.zip`

SHA-256:

`706393a07facff1b60bc0ae4369bb8bdb7d065171d831f5bc59f2e3eaad4884f`

The retrieval ZIP itself is not re-embedded here because it is ~370 MB and the prior Codex/repository context already contains the source material. R3 records the hash and copies the retrieval README for provenance.

## Source-integrity result

Old semantic queue: 445 rows.

R3:
- 431 ready for typed semantic adjudication;
- 3 ready for semantic adjudication but runtime fail-closed;
- 7 hold for source-structure correction;
- 3 discovery-only non-joint source objects;
- 1 hold for legacy GSS normalization.

The six directly proven source defects are all Asian Barometer W4 objects and are documented against the recovered native ABS4 questionnaire.

## Historical authority policy

Do not mutate historical R14/P2/P3/P3C authority in place.

The correction file is a **proposed successor overlay**, not an installed rewrite.

## Prior cumulative package

`prior/Rawlsing_V550J_Semantic_Authority_Convergence_Audit_Codex_Ready_Cumulative_20260808_R2.zip`

is embedded for continuity.

