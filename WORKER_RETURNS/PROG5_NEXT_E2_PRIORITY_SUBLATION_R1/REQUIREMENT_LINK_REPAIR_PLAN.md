# E2 — requirement→owner navigation repair, not 227 new functions

Source: [SAT-R immutable 345 navigation records](https://github.com/maidiu/rawlsing/blob/ed9c882a0683375bad70ee4abd1d662a61f1756b/PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/SATURATION_REQUIREMENT_OWNER_LINKS.jsonl), blob `f8806395bee8b94f9b63e2a5cb639ecb289cbec9` (origin M2). In this E2 no original guide/index has been edited. The rows are **pointers into the same 11 sections/51 child functions**, not a license to create additional runnable functions.

## Verified entire denominator

| Requirement family | Input rows | Primary covered | Additional section needed | Primary function owner link missing | J not distinct indexed |
|---|---:|---:|---:|---:|---:|
| Astra N0–N13 scope-conditioned nodes | 16 | 14 | 2 | 0 | 0 |
| Astra F1–F8 gates | 8 | 7 | 1 | 0 | 0 |
| Astra EE01–EE16 responsibilities | 16 | 6 | 3 | 7 | 0 |
| Whole-Machine G/S/P/Q/L/F/T/W/A | 101 | 62 | 19 | 20 | 0 |
| Original accepted 53 | 53 | 9 | 0 | 44 | 0 |
| Seven J anti-loss | 7 | 0 | 0 | 0 | 7 |
| LongMemory44 | 44 | 9 | 1 | 34 | 0 |
| Original35 30 axes template | 30 | 1 | 1 | 28 | 0 |
| 35 immutable source identities | 35 | 0 | 35 | 0 | 0 |
| 35 per-source acceptance cases | 35 | 3 | 32 | 0 | 0 |
| **All** | **345** | **111** | **94** | **133** | **7** |

**227** = **133 primary navigational owner links absent + 94 secondary/additional owner links needed**. These are NOT 227 missing engines or independently missing functions. Seven J functions are *not individually indexed* even though the J anti-loss role is recognized: they need links, not seven reimplementations. All 133 missing-primary and 94 additional records already have nonempty `existing_child_ids` and `additive_owner_sections` in the original ledger; no new guide ontology is required. The source G4 index has 782 typed IDs and G1 892 asset rows, neither number establishes an executed source-native function.

## Concrete navigation edits for later E-R/E-HQ receiver only

1. **Primary repair (133 rows):** For each row `verdict=NO_PRIMARY_FUNCTIONAL_SECTION_LINK`, keep `origin_key` and exact original source/pointer, add link(s) to existing `existing_child_ids` in the `additive_owner_sections`, retaining original G4 placement as a historical locator. Example: `ASTRA_EE:EE01` was in S04; primary Source identity/custody obligation belongs to S01.1 and S03.1. `WHOLE_MACHINE_101:G09` was in S01; owner N11 acceptance is S11.1/S11.4.
2. **Secondary repair (94 rows):** Preserve correct existing primary, add only cross-section dependency/reader links. `ASTRA_NODE:N0` adds S11 in addition to S01; `ASTRA_NODE:N4` adds S02/S11 in addition to S03/S04; `ASTRA_F_GATE:F1` adds S01 in addition to S04. Never duplicate a child.
3. **J non-indexed (7 rows):** Put `SEVEN_J_ANTI_LOSS:J1…J7` as distinct *reference keys* into the same existing Sxx/child/asset locator. Don't conflate seven anti-loss functions with accepted original 53 or create seven new processors. Original J owner and source cut remain authoritative.
4. **Recheck NOT_INDEXED / presumed primary:** For 111 `PRIMARY_SECTIONS_INCLUDED` rows, no link repair is proposed; track incidental source cut changes only if real code/consumer changes. For any edited navigation link, a click must resolve to an existing child and then the pinned original source—not merely a title match.

## Impact on autonomous next-work selection

Without the 133 repairs, a top-down EE or Whole101 acceptance query can land in a broadly topic-relevant S04 or S01 and never reach the actual owner leaf (source custody, C11, learned release, N11). Without the 94 secondary links, it can find its primary function but miss a second consumer or an AND acceptance prerequisite. The seven J navigation keys prevent anti-loss conservation from being mistaken for a generic new engine task. **These deficiencies are real locator friction, not a count of missing functionality.**

The safe workflow: `origin_key` → exact original source/proof → current `Sxx.child` + `GAP-nnn` → applicable one of 82 edges (MUST/IF/ALTERNATIVE; AND joins preserved) → current producer+actual reader+version+proof+authority → first still-unresolved leaf. Never let a repaired link automatically change `COMPONENT_STATUS.jsonl`, `CURRENT_SEAM_STATES.jsonl` or source authority.

## Receiver-ready deterministic repair specification (no mutation by E2)

- Consume the already-existing 345 rows in original order; assert unique `origin_key` and exact counts 111/94/133/7.
- For 133 and 94 rows, append existing child crossrefs only; retain original G4 section links, exact source blob/path and `conditional_dependencies` verbatim.
- For J1–J7, surface standalone clickable navigation IDs without asserting new code or modifying the 782 G2 identities.
- Flag 0 duplicate links, 0 dangling child destinations, 0 lost IF predicates, 0 promoted alternatives; if impossible to resolve a row at pinned source, mark **UNKNOWN**, don't route to a plausible title.
- Separate check: source first-reader and accepted review state must come from code/report, not locator row. Original source-native 35-wave occupancy remains 0 verified here; this E2 is not a measurement or native proof run.
- E-R is the receiving integrator, E-F independent cold reader. Neither may treat E2 author output as acceptance. No self-adoption.

## High-leverage examples from immutable row pointers

- `ASTRA_EE:EE01`: NO_PRIMARY_FUNCTIONAL_SECTION_LINK; old ROADMAP:S04 → add ROADMAP:S01,ROADMAP:S03; exact child IDs ROADMAP:S01.1,ROADMAP:S03.1; source `PYAT_CONTROL_ROOM/ASTRA_PYAT_INTEGRATED_DEVELOPMENT_ATLAS_R1/functions/EE01.md` at `378549b450be4825a34d5ec2fa8866877d13f76f`.
- `ASTRA_EE:EE09`: NO_PRIMARY_FUNCTIONAL_SECTION_LINK; old ROADMAP:S04 → add ROADMAP:S05; exact child IDs ROADMAP:S05.1,ROADMAP:S05.2; source `PYAT_CONTROL_ROOM/ASTRA_PYAT_INTEGRATED_DEVELOPMENT_ATLAS_R1/functions/EE09.md` at `378549b450be4825a34d5ec2fa8866877d13f76f`.
- `WHOLE_MACHINE_101:G09`: NO_PRIMARY_FUNCTIONAL_SECTION_LINK; old ROADMAP:S01 → add ROADMAP:S11; exact child IDs ROADMAP:S11.1,ROADMAP:S11.4; source `PYAT_CONTROL_ROOM/WHOLE_MACHINE_COMPLETION_R1/TASK_LEDGER_101_MACHINE.json` at `378549b450be4825a34d5ec2fa8866877d13f76f`.
- `WHOLE_MACHINE_101:G10`: NO_PRIMARY_FUNCTIONAL_SECTION_LINK; old ROADMAP:S01 → add ROADMAP:S04,ROADMAP:S11; exact child IDs ROADMAP:S04.5,ROADMAP:S11.2; source `PYAT_CONTROL_ROOM/WHOLE_MACHINE_COMPLETION_R1/TASK_LEDGER_101_MACHINE.json` at `378549b450be4825a34d5ec2fa8866877d13f76f`.
- `ASTRA_NODE:N0`: ADDITIONAL_OWNER_SECTIONS_NEEDED; old ROADMAP:S01 → add ROADMAP:S11; exact child IDs ROADMAP:S01.1,ROADMAP:S01.4,ROADMAP:S11.1; source `PYAT_CONTROL_ROOM/ASTRA_PYAT_INTEGRATED_DEVELOPMENT_ATLAS_R1/data/nodes.json` at `378549b450be4825a34d5ec2fa8866877d13f76f`.
- `ASTRA_NODE:N4`: ADDITIONAL_OWNER_SECTIONS_NEEDED; old ROADMAP:S03,ROADMAP:S04 → add ROADMAP:S02,ROADMAP:S11; exact child IDs ROADMAP:S02.2,ROADMAP:S03.3,ROADMAP:S03.4,ROADMAP:S11.2; source `PYAT_CONTROL_ROOM/ASTRA_PYAT_INTEGRATED_DEVELOPMENT_ATLAS_R1/data/nodes.json` at `378549b450be4825a34d5ec2fa8866877d13f76f`.
- `ASTRA_F_GATE:F1`: ADDITIONAL_OWNER_SECTIONS_NEEDED; old ROADMAP:S04 → add ROADMAP:S01; exact child IDs ROADMAP:S01.1,ROADMAP:S01.2,ROADMAP:S01.3,ROADMAP:S04.1; source `PYAT_CONTROL_ROOM/ASTRA_PYAT_INTEGRATED_DEVELOPMENT_ATLAS_R1/gates/F1.md` at `378549b450be4825a34d5ec2fa8866877d13f76f`.
- `SEVEN_J_ANTI_LOSS:J1`: NOT_INDEXED_AS_DISTINCT_RECORD; old unindexed → add ROADMAP:S04; exact child IDs ROADMAP:S04.4; source `PYAT_CONTROL_ROOM/23_HQD124_SIX_STAGE_SOURCE_FREE_ARCHITECTURE_COMPLETION.md` at `378549b450be4825a34d5ec2fa8866877d13f76f`.
