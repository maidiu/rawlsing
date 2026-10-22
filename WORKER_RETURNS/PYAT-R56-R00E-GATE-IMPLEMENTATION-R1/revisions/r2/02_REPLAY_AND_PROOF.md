# Replay and proof

- 36/36 frozen cases: `evidence/replay.json`.
- 8/8 reviewer defects repaired: `evidence/defect_matrix.json`.
- 24/24 tests: `evidence/junit/r00e_r2.xml`.
- Dependency fault: `evidence/dependency_fault.json` — separate-process baseline ALLOW → substituted policy operation REFUSE_FRONTIER → fresh restore ALLOW.
- Gate source scan: `evidence/imports.json` — no C00–C35 switch, no q301 literal blacklist, no fixture/OP.TEST/18-count branch.
- Policy identity: `evidence/policy_pin.json` — five R2 Git blobs and 18 operation identity digests.
- Mechanical proof witness: `evidence/proof_witness.json` — gate/test/replay/JUnit hashes, commands, 36/36 and 8/8 outcomes. This is a local execution record, not protected CI.
- Changed-test/proof-integrity: `evidence/changed_test_gate.json` (post-commit).
