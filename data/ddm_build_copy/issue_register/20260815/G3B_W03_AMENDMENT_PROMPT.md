# W03-B — G3B Producer-Boundary Amendment

PR #15 is not yet mergeable as a G3B semantic gate. Preserve the current V551J implementation and address the blocking review already posted on PR #15.

The amendment is narrowly scoped to the V550J→V551J producer boundary. Vozhd explicitly permits W03-B to modify the minimum W03-owned V550J producer file(s), including `data/ddm_build_copy/compile_v550j_joint_response_patterns.py`, needed to close the boundary.

Required result:
- V550J producer declares exact post-serialization `artifact_file_sha256` for every governed table consumed by V551J;
- V550J declares an explicit supported producer contract/schema/compiler version, exact producer run/scope identity, and shared typed `run_integrity_status`, `evidence_status`, `downstream_permission_status`;
- V551J fails closed on missing/unknown/non-PASS required producer state, unsupported producer version, scope mismatch, or any producer-declared artifact hash mismatch;
- `LEGACY_V550J_PRODUCER_DOES_NOT_DECLARE_ARTIFACT_FILE_SHA256` is no longer an acceptable execution state;
- correct producer bytes/version/state pass; tampered bytes fail before semantic use; valid typed no-joint-evidence remains integrity-valid where applicable.

Do not redesign V550J or V551J semantics. Preserve the existing governed registry/publishability/threshold behavior and the current V551J V551-v3 repair-debt, neutral, low-support, zero-packet, and compatibility behavior. Do not touch V552/V552J, W05 files, Section85, or register governance.

Push the amendment to the existing branch `agent/v550-v552j-w03-v551j` and existing PR #15. Return the updated machine-readable worker report and terminal summary.