# P5 Hostile Closure

Disposition: `PASS`

Independent PASS-E parser: Python `csv.DictReader` over freshly reopened frozen bytes, separate from the first pandas-based round trip.

## Hostile invariants
- `terminal_total_1264`: `PASS`
- `terminal_unique_1264`: `PASS`
- `partition_counts_exact`: `PASS`
- `pairwise_disjoint`: `PASS`
- `reject_rows_697_unique`: `PASS`
- `reject_set_exact_terminal_subset`: `PASS`
- `no_accept_leakage`: `PASS`
- `no_blocked_leakage`: `PASS`
- `worker_union_1264_unique`: `PASS`
- `worker_rows_equal_central_all_fields`: `PASS`
- `denominator_rows_equal_central_anatomy`: `PASS`
- `defect_count_125`: `PASS`
- `successor_count_125_unique`: `PASS`
- `successor_exact_defect_set`: `PASS`
- `successor_obligations_not_truth`: `PASS`
- `successor_not_block_freeze`: `PASS`
- `reject_no_blocker_state`: `PASS`
- `reject_no_accept_relation_state`: `PASS`
- `all_decisive_reasons_present`: `PASS`
- `all_evidence_refs_present_and_json_valid`: `PASS`
- `all_identity_payload_json_valid`: `PASS`
- `all_implementation_ids_json_valid_nonempty`: `PASS`
- `blank_ceiling_count_preserved_46`: `PASS`
- `blank_prohibited_inference_count_preserved_46`: `PASS`
- `blank_confidence_count_preserved_46`: `PASS`
- `blank_defect_note_count_preserved_572`: `PASS`
- `nested_json_semantics_roundtrip_all`: `PASS`
- `normalized_reject_not_negative_all`: `PASS`
- `no_currentness_from_chronology`: `PASS`
- `all_697_have_source_context`: `PASS`
- `source_context_member_join_exact`: `PASS`
- `all_worker_return_zip_pins_match`: `PASS`
- `first_roundtrip_697_0_0`: `PASS`

## Independent semantic rerun
- Records re-normalized from fresh source parses: `697`
- PASS: `697`
- FAIL: `0`
- BLOCKED: `0`

## Null/empty/open-world hygiene
- All CSV schema fields remain explicitly present in the logical record; historical empty-string cells are tagged `EMPTY_STRING`, not coerced to null/missing/unresolved/not-applicable.
- Nested JSON is parsed without key-dropping; `null`, empty string, empty list/object, and absent keys retain distinct JSON semantics.
- 46 historical REJECT rows have empty candidate-unique `semantic_confidence`, `evidence_ceiling`, and `prohibited_inference` cells; those empties are preserved exactly. No missing text is invented. Global contract/rule closure remains separately referenced.
- 572 historical REJECT rows have an empty scope-defect note because the scope-defect flag is false; the empty value is preserved rather than normalized to a defect absence theorem beyond the explicit flag.

## Firewall
- `EXACT_CANDIDATE_REJECT` remains a non-truth-bearing adjudication disposition.
- No normalized record maps REJECT to `PROVEN_NEGATIVE`, `NONEDGE`, generic false, or universal relation absence.
- No current selection is inferred from chronology, commit order, filename order, or absence of a later row.
- All 125 successor obligations remain append-only obligations with `SUPPLIED_CANDIDATE_REMAINS_TERMINAL_REJECT`; no obligation becomes successor truth.
