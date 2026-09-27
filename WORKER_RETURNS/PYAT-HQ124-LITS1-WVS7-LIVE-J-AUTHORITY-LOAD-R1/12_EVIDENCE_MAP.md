# Evidence and replay map

- FROZEN_PREVALUE_SELECTION.json: exact current specimen/succession rows, native/current order, binder hashes and pre-value selection law; freeze commit 6744e3e0.
- CURRENT_J_CANDIDATE_UNIVERSE_FROZEN.csv and J01B_D5_EXACT_CARRIERS.zip: exact Library artifacts matching Git pointers. D5 extracted members retain exact bytes; historical residual and match files are retained for archive integrity, not role/selection authority.
- AUTHORITY_RECOVERY_PROVENANCE.json, J01A/J01B pointers, D2 crosswalk and user Library-presence receipt: input provenance. Library IDs libfile_3f6b0d93bb74819195702d808e3093ec and libfile_64dd382a81148191a7645c98972802f4.
- LITS_I_METADATA.json and WVS7_METADATA.json: preparation metadata-only receipts. LiTS_I_CURRENT_DECODER_METADATA.json: retained current-decoder metadata. No complete WVS7 current-decoder metadata digest is claimed after serialization failure.
- LiTS_I_PHYSICAL_EXECUTION.json and WVS7_PHYSICAL_EXECUTION.json: source hashes/shapes, read times, consumed columns, physical counts and exact local intermediate hashes. Physical nonmissing counts are not semantic denominators.
- LiTS_I_QUALIFIED_D03_ROOTS.json: adopted exact extensional R2/R7/R27, restricted to q301_2/q301_7; no outcome-derived applicability.
- WVS7_CURRENT_STRUCTURAL_INPUT.json: current materializer's exact ordinal/name/missing declarations and typed retained B_COUNTRY values. Replay through materialize_from_structural_input without SAV access. Country routing inputs are committed; Q291 outcome values are local only.
- WVS7_CURRENT_PROJECTION_BINDING.json: current carrier-neutral projection binding; two response slots, nine authority snapshots, 97220 respondent/row bindings and 194440 routing facts. This is not a full G-grid projection or M01 fact.
- WVS7_POST_DECODE_RECOVERY.json: exact serialization failure and zero-source-reread recovery. The full source decode and selected incidence retention succeeded before failure.
- LiTS_I_MISSING_ROLE_LOAD_CAV.json and WVS7_MISSING_ROLE_LOAD_CAV.json: reload-verified generic diagnostic missing-load receipts; every governed role binding missing. They are not named J2I role channels and provide no component value authority.
- LIVE_GATE_ADJUDICATION.json: actual L1–L7 gates; no manufactured validator/M1/determinant/release outcome.
- BOUNDED_RUNTIME_TESTS.txt: 89 current source-free CAV/J-role/M1/M2 tests, independent of live occupancy. Test code unchanged.
- HQ123_08_SOURCE_FREE_VS_LIVE_OCCUPANCY_BOUNDARY.md and HQ123_09_EXACT_REMAINING_GAPS.tsv: exact adopted court at e7e6fdb25031b8d0ebc1bc8b357460814f385f01.
- EVIDENCE_SHA256.json: committed evidence byte sizes/hashes, excluding itself. Local raw hashes are in execution receipts.

execute_physical_court.py verifies/reuses existing receipts without source rereads and refuses automatic rereads after interruption. recover_wvs_from_retained.py uses exact local incidence plus retained metadata. finalize_return.py regenerates ledgers and verifies diagnostic CAVs without decoding sources. prepare_return.py is disabled to protect the frozen carrier.

Local outcome extracts: local_intermediates/LiTS_I_selected_physical_incidence.json.gz and local_intermediates/WVS7_selected_physical_incidence.json.gz. Each retains exact physical type/float64 hex and original row ordinal; Git ignores them. Full physical replay requires their exact bytes or separately justified original-source access. Single-read discipline is backed by retained markers/hashes/receipts and documented session execution, not a cryptographic proof of read count.
