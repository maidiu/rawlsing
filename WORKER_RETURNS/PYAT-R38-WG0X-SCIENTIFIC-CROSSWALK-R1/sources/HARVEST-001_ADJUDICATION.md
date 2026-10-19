# HARVEST-001 Adjudication — Question Structure Register Lineage

Status: `ADJUDICATED__FOLLOW_UP_REQUIRED`

Packet SHA-256: `e283735f6af208578b373a2e30d8df7fc8ad3f86edc05874fa43e4be9092db78`

## Packet integrity

Browser independently verified the uploaded ZIP bytes, ZIP integrity, and all 114 entries in `SHA256SUMS.txt`. The packet contains 1,704 physical-manifest rows and 108 distinct packaged SHA identities.

## Holding 1 — G1A-B01 payload recovery is closed for the manual/source-topology obligation

Three exact 18,792-row `question_structure_register.csv` payloads were recovered:

- `f47c8adb65546b1c0a06dcd31dc0b827b59f8975a3806646f41a0742966c3d84` — 62 columns.
- `15f7b5613b7cb106c2d2db233925891d5392917b66eee19c1a5eff8e0655585b` — 69 columns.
- `9139c1ab77bf47a872f63ccae7784f3631f03a3e02a936b4ac41e75580c45219` — 69 columns and physically located at the current local `data/ddm_build_copy/manifests/question_structure_register.csv` path.

Across all three, the exact common 52-column pre-driver structure/manual projection is byte-identical after normalized CSV serialization:

`500f0022f5ccdec32008019bad642d62c3c5a77937bcbf9cef24fc67d23e6f85`

The 562 rows marked `needs_manual_review=yes` are also identical as a sorted row sequence:

`98a24a7bfecf573b5ef00329226f7210a2e6cb61ebaadd9b5e6127aff476c780`

The register-level current-scope population is likewise invariant: every version contains exactly 35 distinct source-family/wave pairs, includes EVS 1999, and excludes Asian Barometer W6.

Therefore the historical manually reviewed/source-topology capital is positively recovered. It may not be described as absent, and it may not be regenerated as if lost.

`EXP-001 -> EXISTS__ACCEPTED_AUTHORITY_MAPPED`

This holding is obligation-scoped. It does **not** claim that every semantic-driver field in every register version is identical.

## Holding 2 — semantic driver evolution is a separate authority lineage

The oldest 62-column register to the June 69-column register changes 13,330 cells across 2,148 rows. Every changed cell is confined to driver/semantic-master fields:

- `final_driver_id`: 879
- `final_driver_scope`: 1,870
- `final_driver_label`: 1,592
- `final_driver_origin`: 1,869
- `semantic_scope`: 1,870
- `semantic_primary_driver`: 1,296
- `semantic_secondary_driver`: 773
- `semantic_shared_driver`: 1,310
- `semantic_notes`: 1,871

No common pre-driver structural/manual field changes.

HARVEST-001 also recovered exact `questions_master_drivers.csv` identities:

- `53feb28296705d2005f8c3d2548c136e2c15fabd62c103694f05caa555063711`
- `d62accad0e956f739eada0718e4fb222429e7a90ed7889fff6f4f292b1a8a011`

This burden therefore remains under `EXP-006/EXP-007`; it must not be used to reopen the now-recovered question-structure/manual-review obligation.

## Holding 3 — June to Aug. 16 is a bounded deterministic GSS structure-classification delta

`15f7b561... -> 9139c1ab...` changes 131 cells across 117 rows, all GSS:

- 117 `source_structure_classification`
- 7 `source_structure_review_required`
- 7 `source_structure_confidence`

Classification transitions:

- 98 `open_text_excluded -> substantive_scale`
- 12 `substantive_single_choice -> substantive_scale`
- 7 `unknown -> substantive_scale`

The campaign-start `ddm_v550_source_structure.py` contains an explicit GSS-only SES relation-evidence derivation path that returns `substantive_scale`. The bounded delta is therefore classified as deterministic governed compilation, not newly invented manual semantic authority.

## Holding 4 — current-35 itinerary drift is isolated from the recovered register

The historical `question_wave_itinerary.csv` remains a real manual review/designation/document-reference authority surface, and it still has the known scope drift: Asian Barometer W6 present, EVS 1999 absent.

But every recovered question-structure register already has the correct 35 family-wave scope. Thus G1A-B02 is now isolated to the itinerary/manual-designation succession layer. It is not a defect in the recovered structure-register population.

Browser-side evidence additionally shows:

- the accepted source census contains EVS 1999 and excludes Asian W6;
- current respondent source/semantic registries contain explicit EVS 1999 authority;
- accepted PREP71 R04 EVS evidence binds the exact EVS 1999 source and official ZA3811 documentation;
- an Aug. 17 UID-bearing builder recovered in HARVEST-001 requires `source_structure_audit_binding_35wave_v1.json`, exactly 35 expected/observed wave UIDs, hash-bound audit artifacts, and fail-closed exclusion of Asian Barometer W6.

The referenced binding payload itself was not included in HARVEST-001. This is the narrow next recovery question.

## Holding 5 — the 54 negative path occurrences do not prove 54 missing objects

The 54 `MISSING_LINKED_PATH` occurrences in the packet collapse to repeated historical absolute-path references to three LiTS III/IV basenames. Independent Library-tree evidence shows case/alias-drifted LiTS III/IV audit files existed.

Accordingly:

`54 path misses != 54 lost authority objects`

No LiTS authority is classified missing from this evidence.

## Disposition

- `HARVEST-001`: `ADJUDICATED__FOLLOW_UP_REQUIRED`
- `EXP-001 QUESTION_STRUCTURE`: `EXISTS__ACCEPTED_AUTHORITY_MAPPED`
- `EXP-007 DRIVER_FACET`: remains `EXISTS__SUPERSESSION_NOT_PROVED`
- `EXP-002 CURRENT_35_SCOPE`: narrowed to current-scope successor / itinerary-preservation adjudication
- no new semantic authority creation is authorized.
