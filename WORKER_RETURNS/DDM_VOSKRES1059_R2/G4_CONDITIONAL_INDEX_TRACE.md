# G4 — Independent trace of the V551 conditional-determinicity index

## Result in one line

`LOCAL_UNCONSUMED_AUXILIARY_CAPABILITY`, not "global loss" and not "conserved". The producer function and its eligibility gates exist; no in-tree caller or reader is proved; V552 accepts and provenance-records the input but does not use it substantively; V551J does not ingest it. The nearest modern diagnostics are exact but diagnostic-only and are not name-equivalent successors.

## 1. Producer and eligibility (old source)

- `data/ddm_build_copy/ddm_v551_conditional.py:157-236` defines `build_conditional_determinicity_index(bridge, source_run_id="")`.
- It accepts only bridge rows with:
  - `v551_conditional_determinicity_eligible` true (`:196-198`);
  - `bridge_evidence_lane == "derived_determinicity"` (`:199-201`);
  - `question_use_contract_joined` true (`:202-204`);
  - `source_structure_fields_joined` true (`:205-207`);
  - `support_status == "sufficient_support"` (`:208-220`);
  - a unique conditional key over source/wave/canonical_wave/country/question/var/source_row_hash (`:221-227`).
- Output row fields include `conditional_id`, source/wave/country/question/var, source table/lane, response values/labels, direction/intensity, directionality/semantics status/hashes, `support_status`, `n_unweighted`, `n_weighted`, `pct_*`, `support_basis`, `compiler_status`, `source_row_hash`, `source_run_id`, schema version (`:103-154`).
- The index is therefore a V551-derived auxiliary table, not a V550J pattern table and not a V551 direct atom table.

## 2. Bridge eligibility is not production or consumption

- `ddm_v550_bridge.py:467` marks `conditional_determinicity` only for the derived lane with sufficient support; `:648` sets `v551_conditional_determinicity_eligible = derived_lane & common_relation_gates`; `:960` records the flag in the bridge payload.
- Those fields are eligibility metadata. They do not invoke `build_conditional_determinicity_index` and do not write the index.
- Independent search across the inspected historical tree found **no importer/caller** of `build_conditional_determinicity_index` and no `__main__` in `ddm_v551_conditional.py`. The only post-definition references are validators (`ddm_v550_validation.py:155-156`; `ddm_v551_conditional.py:238-243`).

## 3. V552 accepts the input but does not use it

- `compile_v552_structural_ddm.py:284-309` optionally reads the conditional parquet, verifies it as a canonical parquet, and passes `conditional_determinicity` to `build_v552_structural_outputs`; the input-provenance schema requires `conditional_determinicity_path`, `conditional_determinicity_hash`, `conditional_determinicity_row_count` (`ddm_v550_schema.py:1617-1631`).
- `ddm_v552_structural.py:253-259` shows the parameter in the function signature; the body's `empties` map creates an **empty** `conditional_determinicity_status_audit`; no row of the index is joined, filtered, scored, or emitted into V552 facts.
- This is a local dead socket inside the inspected function. It does not prove that no external caller could post-process the index; that remains `NOT_INSPECTED`.

## 4. V551J does not ingest it

- The V551J compiler's required inputs are V551 atoms/manifest/adjudication/coverage plus V550J pattern/item/relation/association/position/meaning and the registry (`compile_v551j_joint_evidence_packets.py:1140-1210`).
- `build_v551j_joint_outputs_v2` has no conditional-index parameter (`ddm_v551j_packets.py:1481-1505`).
- V551J's `conditional_support_packet`/context surfaces are derived from V550J association rows and atom joins (`ddm_v551j_packets.py:244-253,621-695,716-788`), not from the V551 conditional index.
- Therefore V551J cannot be used as evidence that the conditional index was historically consumed.

## 5. No same-grain modern successor verified

- Prior PROGRAMMA G3A function parity row `G1A-FUNC-012` classifies `V551_AUX_CONDITIONAL_SOCKET` as `NO_CURRENT_MATCH_VERIFIED`; it records the historical symbol `build_conditional_determinicity_index` at `ddm_v551_conditional.py:157`, blob `359665297677553a33556ce65c2e3d76b60b2cc1`, and states that no current same-name match or verified consumer was found (`PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/FUNCTION_PARITY.jsonl`, row 12; `.../SECTIONS/04_F1_F4_EMPIRICAL.md:182`).
- The modern `pre553_diagnostics.produce_governed_diagnostics` product is exact arity-2 H/MI/NMI from one complete joint cell projection (`pre553_diagnostics.py:243-365,493-650`), but it is `diagnostic_only=True`, carries no truth/frontier/structural/semantic authority, and requires a different grain (exact joint fact, not the V551 derived bridge row).
- Modern query conditioning (`execute_empirical_query` risk/conditioning) is not evidence of the old auxiliary index's historical production or consumption.

## 6. What would change the disposition

- A real in-tree or external producer invocation writing `conditional_determinicity_index` with a run id and nonempty rows.
- A real reader that numerically or structurally consumes `conditional_id` or its fields (not merely a schema/provenance reference).
- A lawful historical output row or manifest proving the index was produced for a selected scope.
- A qualified modern replacement with same-grain semantics and a named first reader.

## 7. Self-critical limits and held edges

- `NO_IN_TREE_CALLER` is a source-tree observation, not proof that no historical job invoked the function from an external script.
- V552's local non-use is not global loss; another downstream path could dereference the index outside the inspected files.
- The existence of V551J does not conserve the conditional index: V551J is a different same-person joint/component construction.
- The existence of a modern diagnostic product does not conserve the old index by name or by mathematical similarity.
- Historical execution, row counts and actual numerical effect are `NOT_ESTABLISHED`; no execution was performed.

**Disposition:** `HELD_LOCAL_UNCONSUMED_AUXILIARY_CAPABILITY_WITH_NO_PROVED_HISTORICAL_PRODUCER_OR_READER`. Do not promote either to global loss or to conservation.
