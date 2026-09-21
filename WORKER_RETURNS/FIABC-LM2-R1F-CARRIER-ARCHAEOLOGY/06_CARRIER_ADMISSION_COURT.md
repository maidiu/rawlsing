# FIABC-LM2-R1F — Carrier Admission Court

## Governing object

The only admissible recovery target is:

`FIABC_LM2_R1E_FROZEN_Q291_PHYSICAL_CELL_CARRIER@1.0.0`

for exact WVS7 source SHA-256:

`2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`

## Admission predicates

A browser-recovered artifact may be admitted only if all of the following are proved from the artifact and accepted lineage, not inferred from names or hashes:

1. exact WVS7 source identity;
2. exactly 97,220 ordered source rows;
3. exact `Q291G5` and `Q291P5` physical cells for every row;
4. exact source row ordinal preservation;
5. exact variable identity/ordinal preservation, with frozen ordinals 388 and 394 respectively;
6. exact raw physical-value witness preservation under the current N1 opaque witness law;
7. exact physical missing state for every cell;
8. exact source missing declaration for every non-observed physical state where a declaration exists;
9. candidate-neutrality and zero Candidate A/B/C output parentage;
10. accepted WVS7 lineage or a mechanically proved exact-equivalence derivation;
11. deterministic no-SAV rehydration sufficient for the current R1E validator and common-C11 rematerializer.

Failure of any one predicate rejects the candidate.

## Candidate adjudication

| Candidate | Classification | Court holding |
| --- | --- | --- |
| J05 package/SAV recovery receipts | `IDENTITY_ONLY__NO_PAYLOAD` | Exact package and contained SAV are proved; no ordered Q291 physical cells are persisted. |
| D03/D12 respondent replay | `IDENTITY_ONLY__NO_PAYLOAD` | Row identity/replay is exact, but the historical 20-column decode excludes both Q291 targets. |
| LM2 structural preimage | `PARTIAL__INSUFFICIENT` | Preserves Q291G5 ordinal 388, Q291P5 ordinal 394, and their -5..-1 user-missing declarations; row values are absent. |
| LM2 physical-evidence material | `PARTIAL__INSUFFICIENT` | Preserves metadata/topology and replay identities, not Q291 row observations. |
| Full GSR07 R2 C11 receipts | `IDENTITY_ONLY__NO_PAYLOAD` | Release/ref/hash identities survive; public/internal object bodies do not. |
| GSR07 R2 Actions artifacts | `AGGREGATE_ONLY` | Workflow log proves each retained artifact contains only one 634/635-byte court receipt. |
| D11 source-local Actions artifact | `SEMANTIC_ONLY__NO_PHYSICAL_PAYLOAD` | Contains source-local admission authorities, empirical universes, and replay receipt; no responses. |
| P2F2 workload package | `SEMANTIC_ONLY__NO_PHYSICAL_PAYLOAD` | Exact response refs/predicates/tokens/query specs/Lock2 are semantic workload material, not row cells. |
| P2R6S projection/materializer | `SEMANTIC_ONLY__NO_PHYSICAL_PAYLOAD` | The accepted materializer explicitly does not inspect Q291 outcome values during projection-authority construction. |
| P2R6M persisted large snapshot | `WRONG_SOURCE_OR_SCOPE` | The 1.447 GB logical snapshot is LiTS 2006, source SHA `7cac43e2...`, not WVS7. |
| R5/SR07 historical real-source scratch | `PAYLOAD_UNAVAILABLE_OR_EXPIRED` | Physical data was processed transiently, but the relevant full/bounded carrier scratch was not committed and no surviving Actions payload contains it. |
| Recovery-reservoir WVS7 objects | `SEMANTIC_ONLY__NO_PHYSICAL_PAYLOAD` | WVS7 survives as questionnaire/source-structure evidence; respondent observations do not. |
| Generic large reservoir blobs | `WRONG_SOURCE_OR_SCOPE` | Every >=1 MB object was resolved through `OBJECT_INDEX.tsv`; provenance is ledgers/spines/source-structure/candidate accounting, not a Q291 row-cell carrier. |
| Generic binary payload/hash arrays | `AGGREGATE_ONLY` | Reference-hash arrays and unrelated transports do not contain raw Q291 physical values. |
| R1E exact-head Actions runs | `AGGREGATE_ONLY` | No artifact was uploaded; source-free preparation cannot manufacture the missing physical preimage. |

## Exact-equivalence court

No candidate qualifies as `EXACT_EQUIVALENT__REPACKAGING_REQUIRED`.

A lawful exact-equivalent artifact would have to expose enough physical preimage to reconstruct, without SAV access, the same ordered 194,440 Q291 cells including raw witness types, physical missing states, and source declarations. None of the surviving hashes, ExactRefs, release identities, row-binding digests, semantic comparator tokens, questionnaire records, or aggregate measurements contains that information.

Cryptographic digests authenticate an existing preimage; they do not invert to it.

## Court judgment

`EXACT_CARRIER`: **none**

`EXACT_EQUIVALENT__REPACKAGING_REQUIRED`: **none**

Browser recovery verdict:

`ABSENT__NO_BROWSER_ACCESSIBLE_EXACT_OR_EQUIVALENT_Q291_PHYSICAL_CELL_CARRIER`

The minimum remaining operation is the separately frozen single local extraction in files 08–10. This court does not authorize or execute it.
