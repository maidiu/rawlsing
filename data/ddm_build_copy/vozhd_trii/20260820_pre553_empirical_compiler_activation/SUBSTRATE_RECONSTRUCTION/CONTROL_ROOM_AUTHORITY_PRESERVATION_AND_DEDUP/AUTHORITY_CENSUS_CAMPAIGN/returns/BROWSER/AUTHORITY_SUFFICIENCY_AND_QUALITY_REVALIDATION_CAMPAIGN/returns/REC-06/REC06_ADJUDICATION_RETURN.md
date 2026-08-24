# REC-06 adjudication return — Afrobarometer R5 Q60A-Q60G

Status: `BATTERY_DRIVER_VERDICT__RETURNED`  
TIR: `TIR-018`  
Jurisdiction: exactly seven rows, Q60A-Q60G.

## Dispositive worker finding

**Q60D is battery-patterned, not isolated.** All seven Q60 items ask the same measured predicate: perceived prevalence/extent of corruption among a named public actor or institution. The battery does not ask whether corruption is acceptable, whether the respondent trusts the actor, whether the actor performs well, or whether the respondent personally encountered bribery.

| Row | Target | Historical driver | Source support | Same-grain current R10G successor | Row state |
|---|---|---|---|---|---|
| Q60A | President/Prime Minister and office officials | `politicalStability` | DEFECT | none found | `CURRENT_SUCCESSOR_CANDIDATE_REQUIRED` |
| Q60B | Members of Parliament | `civicEngagement` | DEFECT | none found | `CURRENT_SUCCESSOR_CANDIDATE_REQUIRED` |
| Q60C | Government Officials | `corruptionTolerance` | DEFECT | none found | `CURRENT_SUCCESSOR_CANDIDATE_REQUIRED` |
| Q60D | Local government councilors | `corruptionTolerance` | DEFECT | none found | `CURRENT_SUCCESSOR_CANDIDATE_REQUIRED` |
| Q60E | Police | `politicalStability` | DEFECT | none found | `CURRENT_SUCCESSOR_CANDIDATE_REQUIRED` |
| Q60F | Tax Officials | `corruptionTolerance` | DEFECT | none found | `CURRENT_SUCCESSOR_CANDIDATE_REQUIRED` |
| Q60G | Judges and Magistrates | `corruptionTolerance` | DEFECT | none found | `CURRENT_SUCCESSOR_CANDIDATE_REQUIRED` |

## Battery pattern

The defect is not merely that four rows say `corruptionTolerance`. A single common source predicate was historically scattered across three different driver families: 2/7 `politicalStability`, 1/7 `civicEngagement`, and 4/7 `corruptionTolerance`. This finding is bounded to Q60A-Q60G and does not imply that the entire V525b lineage is invalid.

## Current succession

Historical defects already repaired by exact same-grain current R10G successors: **NONE (0/7).**

Exact source implementation IDs for all seven were checked against the sealed 3,324-row R10G S08 authority; no exact member/successor was found. A target-text match is insufficient: same-grain succession requires exact semantic-unit identity/edge.

The current QSM/P2 Q60 dispositions are other-grain `GOVERNED_NON_DIRECTIONAL_DISPOSITION` records and therefore cannot be promoted into same-grain R10G successors by REC-06.

## Exact remaining successor candidates

All seven rows remain candidates: `Q60A`, `Q60B`, `Q60C`, `Q60D`, `Q60E`, `Q60F`, `Q60G`.

The candidate ledger points only to existing R10G vocabulary:
`stateCapacityIntegrity` → `public_integrity_and_corruption` → `perceived_corruption_prevalence` → `axis__perceived_corruption_prevalence`.

That is a candidate for a later authorized same-grain installation court, not authority created here.

## Evidence ceiling

Source text and response semantics are sufficient to adjudicate the historical construct mismatch. Historical facet identity is not separately recovered on the R07/V525b-style assertion surface, so REC-06 does not invent one. Likewise, absence of an exact R10G Q60 member is recorded as missing same-grain succession, not as permission to silently install a candidate.

No local-machine execution. No broad V525b review. No unrelated Afrobarometer review. No authority mutation.
