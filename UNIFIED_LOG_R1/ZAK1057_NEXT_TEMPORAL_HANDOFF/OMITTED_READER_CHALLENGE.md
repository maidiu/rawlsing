# OMITTED-READER CHALLENGE — did V554 read the keyed field elsewhere?

**Challenge:** the prior R7 case found no V554 read of `v553_temporal_pressure_field.parquet` or `v553_v554_handoff_index.parquet`. Could the keyed field be consumed through a helper, alternate callsite, renamed variable, or thin caller injection?

## Searches performed

1. Full-file literal read of `data/ddm_build_copy/ddm_v554_seed_contract.py` at `6a5c12f04323d74001f9632063ec907f4fc4468e` (blob `b11b73fc171f6b37976fa579d54700505a69f84c`, 1440 lines): all `input_root / ...` path declarations, all `_load_optional_frame`/`_load_json`/`read_table` calls, all uses of `country_year_pressure_df`, `v553_readiness`, `v553_harmonization_report`.
2. `git grep` for `v553_temporal_pressure_field`, `v553_v554_handoff_index`, `v553_downstream_v554_handoff_index`, `v553_country_year_pressure_field` across protected `data/ddm_build_copy/*.py`.
3. Tracked callers of `build_v554_seed_contract`: only `ddm_v5_thin_end_to_end.py` L28 import and L1815 call; inspected call arguments and surrounding input layer contract.
4. `git grep` for `ddm_v554_seed_contract` to catch alternate test/CLI callers.

## Result

- V554 declares paths for `v553_source_wave_anchor_manifest`, `v553_pressure_component_breakdown`, `v553_temporal_authority_ledger`, comparability/noncomparability/rupture audits and `v553_downstream_v554_handoff_index` at L912-L921, but never reads them.
- V554 does not declare `v553_temporal_pressure_field.parquet` or `v553_v554_handoff_index.parquet` at all.
- V554 reads `v553_country_year_pressure_field.parquet` (fallback `v553_year_indexed_pressure_over_time.parquet`) and uses only point estimate/status/penalty.
- The thin caller passes `input_root`, `output_root`, and `input_inspection`; it does not inject keyed rows.
- No alternate non-test V554 producer/reader path was found in the inspected source set.

## Verdict

**BOUNDED SOURCE-LEVEL NEGATIVE:** no V554 value read of the keyed authorized field or its handoff index was found. This is not global absence; a different callsite outside the named source set or a generated/renamed consumer remains possible.

## Falsifier

Find one V554 call path that opens either keyed artifact and passes per-key `pressure_level`/`temporal_status`/`key_authorization_status`/`unknown_gap` rows into `_build_seed_affordance_index` or another seed constructor. If found, the no-keyed-read finding falls.
